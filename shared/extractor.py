#!/usr/bin/env python3
"""Stufe 2 der Hydrogen-Analysestrategie: Mehrsprachige atomare Extraktion (Map-Phase).

Liest vorbereitete Chunks aus <bank>/data/chunks/*.json und erzeugt für jeden Bericht
ein einheitliches JSON-Dokument unter <bank>/data/extracted/<stem>.json.

Backends:
  --backend gemini : Gemini Hydrogen (gemini-2.5-flash-lite) via Gemini REST API (GEMINI_API_KEY).
  --backend local  : Deterministischer DE/FR/EN-Tabellenparser mit identischem JSON-Schema & source_quote.
  --backend auto   : Wählt 'gemini' falls GEMINI_API_KEY gesetzt, sonst 'local'.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import urllib.request
from pathlib import Path

from shared.config import BankConfig, load_bank_config

DEFAULT_HYDROGEN_MODEL = "gemini-2.5-flash-lite"

HYDROGEN_SYSTEM_PROMPT = """Du bist ein präziser Finanzdaten-Extraktor für Schweizer Bankberichte (DE/FR/EN).
Regeln:
1. Extrahiere NUR Zahlen, die explizit im Text oder in der Tabelle stehen.
2. Rechne NICHT um und berechne KEINE Summen, Differenzen oder Quoten.
3. Gib für jeden Wert `value_current`, `value_prior_year`, `unit`, `currency` und `source_quote` zurück.
4. Wenn ein Wert im Ausschnitt nicht vorkommt, setze `value_current`: null.
5. Gib AUSSCHLIESSLICH valides JSON gemäss Schema zurück."""


def clean_cell(cell: str) -> str:
    txt = cell.replace("\xad", "").replace("’", "'")
    txt = re.sub(r"<sup>.*?</sup>", "", txt, flags=re.IGNORECASE)
    txt = re.sub(r"^(?:[il]\s*<br\s*/?>\s*)+", "", txt, flags=re.IGNORECASE)
    txt = re.sub(r"(?:\s*<br\s*/?>\s*(?:[il]|\d)\s*)+$", "", txt, flags=re.IGNORECASE)
    txt = re.sub(r"<br\s*/?>", " ", txt, flags=re.IGNORECASE)
    txt = re.sub(r"[*_`]", "", txt)
    txt = re.sub(r"^[•·]\s*", "", txt.strip())
    return re.sub(r"\s+", " ", txt).strip()


def parse_number(raw: str | None) -> float | None:
    """Parst DE/FR/EN-Zahlenformate deterministisch (Tausender: ', ’, Leerzeichen, Komma; Negativ: (), –, -)."""
    if raw is None:
        return None
    s = str(raw).replace("\xad", "").replace("\u00a0", " ")
    s = re.sub(r"<sup>.*?</sup>", "", s, flags=re.IGNORECASE)
    s = re.sub(r"<br\s*/?>\s*\d+\s*$", "", s, flags=re.IGNORECASE)
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.IGNORECASE)
    s = s.replace("*", "").replace("'", "").replace("’", "").replace("`", "").strip()
    if not s or s in {"-", "–", "—", "n.a.", "n.a", "N/A", "nd", "n.d."}:
        return None

    neg = False
    if s.startswith("(") and s.endswith(")"):
        neg = True
        s = s[1:-1].strip()
    if s.startswith(("–", "—", "-")):
        neg = True
        s = s[1:].strip()
    s = s.rstrip("%").strip()

    # Entferne nachgestellte Fussnoten wie "10.80 1"
    s = re.sub(r"\s+\d{1,2}$", "", s).strip()

    # Fall 1: Englisches Format mit Komma-Tausender & Punkt-Dezimal: 1,234,567.89 oder 1,234,567
    if re.fullmatch(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?", s):
        val = float(s.replace(",", ""))
        return -val if neg else val

    # Fall 2: Punkt-Tausender & Komma-Dezimal: 1.234.567,89
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+,\d+", s):
        val = float(s.replace(".", "").replace(",", "."))
        return -val if neg else val

    # Fall 3: Leerzeichen-Tausender oder Standard mit Punkt oder Komma als Dezimaltrennzeichen
    m = re.match(r"^(\d[\d\s]*)(?:[.,](\d+))?$", s)
    if not m:
        return None
    int_part = re.sub(r"\s+", "", m.group(1))
    dec_part = m.group(2)
    val = float(f"{int_part}.{dec_part}" if dec_part else int_part)
    return -val if neg else val


def split_md_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def is_year_header_cell(cell_text: str) -> bool:
    c = clean_cell(cell_text)
    if not c:
        return False
    if re.fullmatch(
        r"(?:[a-f]\s+)?(?:1\.1\.[\-–]\s*)?(?:\d{1,2}\.(?:\d{1,2}\.|\s*[A-Za-zäöüéèà]+\s*))?(?:19|20)\d{2}(?:\s+(?:in|en)\s+(?:CHF|USD))?",
        c,
        re.IGNORECASE,
    ):
        return True
    return bool(re.search(r"(?:30\.0?6\.|31\.12\.|1\.1\.[\-–]|30\.\s*Juni|31\.\s*Dezember|30\s+juin|31\s+d[ée]cembre|31\s+December)\s*(?:19|20)\d{2}", c, re.I))


def detect_unit_and_currency(text: str, default_currency: str = "CHF") -> tuple[str | None, str]:
    t = text.lower()
    curr = default_currency.upper()
    if re.search(r"\busd\b|\bus\s*dollar", t):
        curr = "USD"
    elif re.search(r"\bchf\b|franken|francs\s+suisses", t):
        curr = "CHF"

    if re.search(r"in\s+mrd\.|milliarden|en\s+milliards|in\s+(?:chf|usd)\s+billions|billions?\s+(?:of\s+)?(?:chf|usd)|\busd\s*bn\b", t):
        return f"Mrd. {curr}", curr
    if re.search(r"in\s+mio\.|millionen|en\s+millions|in\s+(?:chf|usd)\s+millions|millions?\s+(?:of\s+)?(?:chf|usd)|usd\s+million|\busd\s*m\b", t):
        return f"Mio. {curr}", curr
    if re.search(r"1\s*000|tchf|milliers|thousands", t):
        return f"T{curr}", curr
    if re.search(r"^(?:in|en)\s+(?:chf|usd)\s*$", t.strip()):
        return curr, curr
    return None, curr


def parse_markdown_tables(chunk_text: str, default_currency: str = "CHF") -> list[dict]:
    tables = []
    lines = chunk_text.splitlines()
    i = 0
    recent_unit: str | None = None
    recent_curr: str = default_currency
    recent_year_headers: list[str] | None = None

    while i < len(lines):
        line = lines[i].strip()
        u, c = detect_unit_and_currency(line, default_currency=recent_curr)
        if u:
            recent_unit = u
            recent_curr = c

        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|", lines[i + 1].strip()):
            header_cells = [clean_cell(x) for x in split_md_row(line)]
            unit = recent_unit
            curr = recent_curr
            for hc in header_cells:
                hu, hc_curr = detect_unit_and_currency(hc, default_currency=curr)
                if hu:
                    unit = hu
                    curr = hc_curr

            has_yr_hdr = any(is_year_header_cell(hc) for hc in header_cells)
            if has_yr_hdr:
                recent_year_headers = header_cells
            elif recent_year_headers and len(header_cells) == len(recent_year_headers):
                c0 = header_cells[0].lower()
                if any(k in c0 for k in ("leistungen an die öffentliche", "in millionen", "payments to the public")):
                    header_cells = list(recent_year_headers)

            rows = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append((lines[j].strip(), split_md_row(lines[j])))
                j += 1
            tables.append({"headers": header_cells, "unit": unit, "currency": curr, "rows": rows})
            i = j
            continue
        elif re.match(r"^\|[\s:|-]+\|$", line) and i + 1 < len(lines) and lines[i + 1].strip().startswith("|"):
            rows = []
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append((lines[j].strip(), split_md_row(lines[j])))
                j += 1
            tables.append({"headers": [], "unit": recent_unit, "currency": recent_curr, "rows": rows})
            i = j
            continue
        i += 1
    return tables


# Kanonische DE/FR/EN Zeilenmuster pro Kennzahl
METRIC_ROW_PATTERNS: dict[str, list[str]] = {
    # Bilanz
    "total_assets": [
        r"^total\s+(?:der\s+)?aktiven",
        r"^bilanzsumme",
        r"^total\s+(?:de\s+)?l'actif",
        r"^total\s+du\s+bilan",
        r"^actifs(?:\s+\d+(?:\.\d+)*(?:/\d+(?:\.\d+)*)*)?$",
        r"^total\s+assets\b",
    ],
    "mortgage_loans": [
        r"^hypothekarforderungen",
        r"^cr[ée]ances\s+hypoth[ée]caires",
        r"^mortgage\s+loans",
    ],
    "customer_loans_other": [
        r"^forderungen\s+gegen[üu]ber\s+kunden",
        r"^cr[ée]ances\s+sur\s+la\s+client[èe]le",
        r"^avances\s+[àa]\s+la\s+client[èe]le",
        r"^loans\s+and\s+advances\s+to\s+customers",
    ],
    "financial_investments": [
        r"^finanzanlagen",
        r"^immobilisations\s+financi[èe]res",
        r"^financial\s+investments",
    ],
    "customer_deposits": [
        r"^verpflichtungen\s+(?:aus\s+kundeneinlagen|gegen[üu]ber\s+kunden)",
        r"^engagements\s+(?:r[ée]sultant\s+des\s+d[ée]p[ôo]ts|envers\s+la\s+client[èe]le)",
        r"^d[ée]p[ôo]ts\s+de\s+la\s+client[èe]le",
        r"^customer\s+deposits",
    ],
    "kassenobligationen": [r"^kassenobligationen", r"^obligations\s+de\s+caisse"],
    "pfandbriefe_bonds": [
        r"^anleihen\s+und\s+pfandbriefdarlehen",
        r"^emprunts\s+et\s+pr[êe]ts\s+des\s+centrales",
    ],
    "reserves_banking_risks": [
        r"^reserven\s+f[üu]r\s+allgemeine\s+bankrisiken",
        r"^r[ée]serves\s+pour\s+risques\s+bancaires\s+g[ée]n[ée]raux",
    ],
    "shareholders_equity": [
        r"^total\s+(?:des\s+)?eigenkapital",
        r"^eigenkapital\s+total",
        r"^total\s+des\s+capitaux\s+propres",
        r"^fonds\s*propres$",
        r"^total\s+equity",
        r"^total\s+shareholders'?\s+equity",
        r"^equity\s*attributable\s+to\s+shareholders",
    ],
    # Erfolgsrechnung
    "net_interest_income": [
        r"^(?:subtotal\s+)?(?:netto-?)?erfolg\s+(?:aus\s+dem\s+)?zinsengesch[äa]ft",
        r"^netto-?zinserfolg",
        r"^(?:sous-total\s+)?r[ée]sult(?:at|ant)\s+(?:net\s+)?des\s+op[ée]rations\s+d'int[ée]r[êe]ts",
        r"^net\s+interest\s+income",
    ],
    "commission_income": [
        r"^(?:subtotal\s+)?erfolg\s+(?:aus\s+dem\s+)?kommissions",
        r"^(?:sous-total\s+)?r[ée]sult(?:at|ant)\s+des\s+op[ée]rations\s+de\s+commissions",
        r"^net\s+fee\s+and\s+commission\s+income",
    ],
    "trading_income": [
        r"^erfolg\s+aus\s+dem\s+handelsgesch[äa]ft",
        r"^r[ée]sultat\s+des\s+op[ée]rations\s+de\s+n[ée]goce",
        r"^other\s+net\s+income\s+from\s+financial\s+instruments",
    ],
    "other_ordinary_income": [
        r"^(?:subtotal\s+)?[üu]briger\s+ordentlicher\s+erfolg",
        r"^(?:sous-total\s+)?autres\s+r[ée]sultats\s+ordinaires",
    ],
    "total_operating_income": [
        r"^gesch[äa]ftsertrag\b",
        r"^betriebsertrag\s*netto$",
        r"^total\s+ertrag\b",
        r"^total\s+des\s*produits\s*d'exploitation",
        r"^total\s+des\s+r[ée]sultats\s+de\s+l'activit[ée]\s+bancaire\s+ordinaire",
        r"^produit\s+d'exploitation\s+net$",
        r"^total\s+operating\s+income",
        r"^operating\s*income$",
        r"^total\s+revenues$",
    ],
    "personnel_expenses": [r"^personalaufwand", r"^charges\s+de\s+personnel", r"^personnel\s+expenses"],
    "general_expenses": [r"^sachaufwand", r"^autres\s+charges\s+d'exploitation", r"^general\s+and\s+administrative"],
    "total_operating_expenses": [
        r"^(?:subtotal\s+)?(?:total\s+)?gesch[äa]ftsaufwand",
        r"^(?:sous-total\s+|total\s+des\s+)?charges\s+d'exploitation",
        r"^total\s+operating\s+expenses",
        r"^operating\s*expenses$",
    ],
    "operating_profit": [
        r"^gesch[äa]ftserfolg$",
        r"^bruttogewinn$",
        r"^r[ée]sultat\s+op[ée]rationnel",
        r"^b[ée]n[ée]fice\s+brut$",
        r"^operating\s+profit\s*(?:\(loss\))?\s*before\s+tax",
    ],
    "taxes": [r"^steuern$", r"^imp[ôo]ts", r"^tax\s+expense"],
    "net_profit": [
        r"^(?:jahresgewinn(?:\s+nach\s+steuern)?|konzerngewinn|gruppengewinn|reingewinn|gewinn)(?:\s*\(periodenerfolg\))?$",
        r"^(?:jahresgewinn\s*/\s*-?verlust(?:\s+nach\s+rvb)?|gewinn\s*/\s*verlust)$",
        r"^b[ée]n[ée]fice\s+(?:de\s+l'exercice|net|consolid[ée])",
        r"^r[ée]sultat\s+(?:de\s+la\s*p[ée]riode|net)$",
        r"^net\s*profit\s*(?:/\s*\(?loss\)?\s*)?attributable\s+to\s+shareholders",
        r"^net\s+profit$",
    ],
    # Volumen & Operatives
    "assets_under_management": [
        r"^(?:verwaltete|betreute)\s+verm[öo]gen",
        r"^masse\s+sous\s+gestion",
        r"^invested\s+assets",
        r"^assets\s+under\s+management",
    ],
    "net_new_money": [r"^netto-?neugeld", r"^afflux\s+nets\s+de\s+fonds", r"^net\s+new\s+(?:money|assets)"],
    "fte_count": [
        r"^personalbestand.*(?:vollzeit|fte|teilzeitbereinigt)?",
        r"^vollzeitstellen",
        r"^effectif\s+du\s+personnel",
        r"^employees\s*\(?full-time",
    ],
    "branch_count": [r"^gesch[äa]ftsstellen", r"^filialen", r"^succursales", r"^branches"],
    # Aktie & Ausschüttung
    "share_price_eoy": [r"^aktienkurs", r"^schlusskurs", r"^cours\s+de\s+l'action", r"^share\s+price"],
    "dividend_per_share": [r"^dividende.*je\s+(?:namen|inhaber)?aktie", r"^dividende\s+par\s+action", r"^dividend\s+per\s+share"],
    # Offenlegung (KM1 / OV1)
    "cet1_capital": [r"hartes\s+kernkapital\s*\(cet1\)|^1\s+hartes\s+kernkapital", r"fonds\s+propres\s+de\s+base\s+durs", r"common\s+equity\s+tier\s+1\s*\(cet1\)\s+capital"],
    "tier1_capital": [r"^2\s+kernkapital|^kernkapital\s*\(t1\)", r"fonds\s+propres\s+de\s+base\s*\(t1\)", r"^tier\s+1\s+capital"],
    "total_capital": [r"^3\s+gesamtkapital|^gesamtkapital", r"total\s+des\s+fonds\s+propres", r"^total\s+capital\b"],
    "rwa_total": [r"^4\s+total\s+risikogewichtete|^total\s+risikogewichtete", r"total\s+des\s+positions\s+pond[ée]r[ée]es", r"total\s+risk-weighted\s+assets"],
    "cet1_ratio_pct": [r"cet1-?quote|hartes\s+kernkapital\s+in\s+%", r"ratio\s+cet1", r"cet1\s+capital\s+ratio"],
    "total_capital_ratio_pct": [r"gesamtkapitalquote", r"ratio\s+global\s+de\s+fonds\s+propres", r"total\s+capital\s+ratio"],
    "leverage_ratio_pct": [r"leverage\s+ratio", r"ratio\s+de\s+levier"],
    "lcr_pct": [r"lcr\s*\(%?\)|quote\s+f[üu]r\s+kurzfristige\s+liquidit[äa]t", r"liquidity\s+coverage\s+ratio"],
    "nsfr_pct": [r"nsfr\s*\(%?\)|finanzierungsquote", r"net\s+stable\s+funding\s+ratio"],
}


def _find_year_columns(headers: list[str], target_year: int) -> tuple[int | None, int | None]:
    curr_col: int | None = None
    prev_col: int | None = None
    for idx, h in enumerate(headers):
        if idx == 0:
            continue
        if re.search(rf"\b{target_year}\b", h):
            if curr_col is None:
                curr_col = idx
        elif re.search(rf"\b{target_year - 1}\b", h):
            if prev_col is None:
                prev_col = idx
    return curr_col, prev_col


def extract_local_from_chunk(
    chunk_name: str,
    chunk_text: str,
    target_year: int,
    default_currency: str,
) -> dict[str, dict]:
    tables = parse_markdown_tables(chunk_text, default_currency=default_currency)
    found: dict[str, dict] = {}

    for tbl in tables:
        headers = tbl["headers"]
        curr_col, prev_col = _find_year_columns(headers, target_year)
        for raw_line, raw_cells in tbl["rows"]:
            if not raw_cells:
                continue
            label = clean_cell(raw_cells[0]).lower()
            if not label:
                continue

            for metric_id, patterns in METRIC_ROW_PATTERNS.items():
                if metric_id in found:
                    continue
                if not metric_id.endswith("_pct") and ("in %" in label or "%" in label or "quote" in label):
                    continue
                if any(re.search(pat, label, re.IGNORECASE) for pat in patterns):
                    c_idx = curr_col if (curr_col is not None and curr_col < len(raw_cells)) else None
                    p_idx = prev_col if (prev_col is not None and prev_col < len(raw_cells)) else None

                    if c_idx is None:
                        # Fallback: erste zwei numerische Spalten
                        num_cols = [
                            k for k in range(1, len(raw_cells)) if parse_number(raw_cells[k]) is not None
                        ]
                        if not num_cols:
                            continue
                        c_idx = num_cols[0]
                        if len(num_cols) > 1 and p_idx is None:
                            p_idx = num_cols[1]

                    val_curr = parse_number(raw_cells[c_idx])
                    val_prev = parse_number(raw_cells[p_idx]) if p_idx is not None and p_idx < len(raw_cells) else None
                    if val_curr is None and val_prev is None:
                        continue

                    unit = "%" if metric_id.endswith("_pct") else tbl["unit"]
                    found[metric_id] = {
                        "value_current": val_curr,
                        "value_prior_year": val_prev,
                        "unit": unit,
                        "currency": tbl["currency"],
                        "source_quote": raw_line[:240],
                        "chunk_name": chunk_name,
                    }
    return found


def extract_with_gemini_api(chunk_name: str, chunk_text: str, meta: dict, api_key: str) -> dict[str, dict]:
    prompt = (
        f"Bericht: {meta['stem']} ({meta['period']}, Währung: {meta['reporting_currency']})\n"
        f"Abschnitt: {chunk_name}\n"
        "Extrahiere alle relevanten Kennzahlen gemäss kanonischem Schema als JSON-Objekt "
        "{metric_id: {value_current, value_prior_year, unit, currency, source_quote}}.\n\n"
        f"{chunk_text}"
    )
    payload = {
        "systemInstruction": {"parts": [{"text": HYDROGEN_SYSTEM_PROMPT}]},
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.0, "responseMimeType": "application/json"},
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{DEFAULT_HYDROGEN_MODEL}:generateContent?key={api_key}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    raw_txt = data["candidates"][0]["content"]["parts"][0]["text"]
    parsed = json.loads(raw_txt)
    return parsed if isinstance(parsed, dict) else {}


def extract_bank(bank_id: str, backend: str = "auto") -> int:
    cfg: BankConfig = load_bank_config(bank_id)
    cfg.extracted_dir.mkdir(parents=True, exist_ok=True)
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    active_backend = ("gemini" if api_key else "local") if backend == "auto" else backend
    if active_backend == "gemini" and not api_key:
        raise RuntimeError("--backend gemini gewählt, aber GEMINI_API_KEY ist nicht gesetzt.")

    chunk_files = sorted(p for p in cfg.chunks_dir.glob("*.json") if p.name != "manifest.json")
    for cf in chunk_files:
        payload = json.loads(cf.read_text(encoding="utf-8"))
        meta = payload["meta"]
        metrics: dict[str, dict] = {}
        for chunk_name, chunk_text in payload.get("chunks", {}).items():
            if active_backend == "gemini":
                extracted = extract_with_gemini_api(chunk_name, chunk_text, meta, api_key)
            else:
                extracted = extract_local_from_chunk(
                    chunk_name, chunk_text, meta["year"], cfg.reporting_currency
                )
            for k, v in extracted.items():
                if k not in metrics and isinstance(v, dict):
                    metrics[k] = v

        out = {"meta": meta, "backend": active_backend, "metrics": metrics}
        (cfg.extracted_dir / f"{meta['stem']}.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    print(f"[OK] {cfg.bank_id}: {len(chunk_files)} Berichte extrahiert (Backend={active_backend}).")
    return len(chunk_files)


def main() -> None:
    parser = argparse.ArgumentParser(description="Stufe 2: DE/FR/EN Map-Extraktor.")
    parser.add_argument("--bank", required=True, help="Bank-ID")
    parser.add_argument("--backend", choices=["auto", "local", "gemini"], default="auto")
    args = parser.parse_args()
    extract_bank(args.bank, backend=args.backend)


if __name__ == "__main__":
    main()
