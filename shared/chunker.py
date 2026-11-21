#!/usr/bin/env python3
"""Stufe 1 der Hydrogen-Analysestrategie: Mehrsprachiger deterministischer Markdown-Chunker.

Zerlegt alle Berichte eines Instituts (<bank>/.md/*.md) anhand von Überschriften,
Tabellenankern und Scope-Regeln (Konzern vs. Einzelabschluss) in kompakte Chunks (< 2.500 Tokens),
damit Gemini Hydrogen oder der deterministische lokale Parser sie präzise auslesen kann.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from shared.config import BankConfig, load_bank_config

MAX_CHUNK_CHARS = 9500  # ~2.200–2.400 Tokens

DEFAULT_ANCHORS = {
    "bilanz": [
        r"Hypothekarforderungen|Créances hypothécaires|Mortgage loans|Loans and advances to customers",
        r"Verpflichtungen aus Kundeneinlagen|Verpflichtungen gegenüber Kunden|Engagements résultant des dépôts|Engagements envers la clientèle|Customer deposits",
        r"Total Aktiven|Total Bilanzsumme|Total de l'actif|TOTAL ACTIF|Total assets",
        r"Total Eigenkapital|Total Passiven|Total des capitaux propres|Total du passif|Total equity|Total liabilities and equity",
    ],
    "erfolgsrechnung": [
        r"Zins- und Diskontertrag|Subtotal (?:Netto-)?Erfolg Zinsengeschäft|Netto-?Erfolg aus dem Zinsengeschäft|^\|\*\*Erfolg aus dem Zinsengeschäft",
        r"Résultat net des opérations d'intérêts|Produits des intérêts|Net interest income|Subtotal net result from interest operations",
        r"Erfolg aus dem Kommissions|Kommissions- und Dienstleistungsgeschäft|Résultat des opérations de commissions|Net fee and commission income|Subtotal operating income",
    ],
    "mehrjahresvergleich": [
        r"Personalbestand|Vollzeitstellen|Effectif du personnel|Full-time equivalents|Employees",
        r"Geschäftsstellen|Filialen|Succursales|Branches",
        r"Mehrjahresvergleich|Fünfjahresvergleich|Zehnjahresvergleich|Kennzahlen|Chiffres-clés|Key figures|Financial highlights",
    ],
    "aktie_basisdaten": [
        r"Dividende\s*(?:\([^)]+\))?\s*je\s*(?:Namen)?aktie|Dividende par action|Dividend per share",
        r"Aktienkurs|Cours de l'action|Share price|Börsenkapitalisierung|Dotationskapital|Anteilscheine",
    ],
    "betreute_vermoegen": [
        r"Netto-Neugeld|Afflux nets|Net new money|Net new assets",
        r"Verwaltete Vermögen|Betreute Vermögen|Masse sous gestion|Assets under management|Invested assets",
    ],
    "verguetung": [
        r"Vergütung(?:en)? des Verwaltungsrat|Rémunération du Conseil d'administration|Board of Directors.*compensation",
        r"Vergütung(?:en)? der Geschäftsleitung|Rémunération de la Direction générale|Group Executive Board.*compensation",
        r"Höchste Einzelvergütung|CEO|Chief Executive Officer|Präsident der Geschäftsleitung",
    ],
    "km1_eigenmittel": [
        r"Hartes Kernkapital|CET1-Quote|CET1­Quote|Fonds propres de base durs|Common Equity Tier 1|CET1 capital",
        r"Gesamtkapitalquote|Ratio global de fonds propres|Total capital ratio|TLAC",
        r"Leverage Ratio|Ratio de levier|Quote für kurzfristige Liquidität|LCR|NSFR",
    ],
    "ov1_rwa": [
        r"Total\s*\(.*RWA|Total risikogewichtete|Total des positions pondérées|Total risk-weighted assets|Risk-weighted assets",
    ],
}

CONSOLIDATED_HINTS = re.compile(
    r"Konzern|Groupe|Consolid[ée]|Consolidated|Group\b",
    re.IGNORECASE,
)
STANDALONE_HINTS = re.compile(
    r"Stammhaus|Einzelabschluss|Maison-m[èe]re|Parent bank|Standalone",
    re.IGNORECASE,
)


def detect_report_meta(filename: str, file_prefix: str | None = None) -> dict:
    stem = Path(filename).stem
    prefix = re.escape(file_prefix) if file_prefix else r"[a-z0-9]+"

    m = re.fullmatch(rf"({prefix})-geschaeftsbericht-(\d{{4}})(?:-(.+))?", stem)
    if m:
        year = int(m.group(2))
        part = m.group(3)
        return {
            "stem": stem,
            "report_type": "annual",
            "year": year,
            "period": f"FY{year}",
            "part": part,
        }

    m = re.fullmatch(rf"({prefix})-semesterbericht-(\d{{4}})", stem)
    if m:
        year = int(m.group(2))
        return {
            "stem": stem,
            "report_type": "semester",
            "year": year,
            "period": f"H1-{year}",
            "part": None,
        }

    m = re.fullmatch(rf"({prefix})-offenlegungsbericht-(\d{{2}})-(\d{{4}})", stem)
    if m:
        month = m.group(2)
        year = int(m.group(3))
        if month == "06":
            rtype, period = "offenlegung_h1", f"H1-{year}"
        elif month == "03":
            rtype, period = "offenlegung_q1", f"Q1-{year}"
        elif month == "09":
            rtype, period = "offenlegung_q3", f"Q3-{year}"
        else:
            rtype, period = "offenlegung_fy", f"FY{year}"
        return {"stem": stem, "report_type": rtype, "year": year, "period": period, "part": None}

    m = re.fullmatch(rf"({prefix})-offenlegungsbericht-(\d{{4}})", stem)
    if m:
        year = int(m.group(2))
        return {
            "stem": stem,
            "report_type": "offenlegung_fy",
            "year": year,
            "period": f"FY{year}",
            "part": None,
        }

    raise ValueError(f"Unbekannter Dateiname für Chunker: {filename}")


def is_toc_region(lines: list[str], idx: int) -> bool:
    window = "\n".join(lines[max(0, idx - 15) : min(len(lines), idx + 4)])
    return bool(
        re.search(
            r"Tabellenbezeichnung|Publikationsh[äa]ufigkeit|Nicht verwendete Tabellen|Glossar|Begriff\s*/\s*Abk[üu]rzung|[ÜU]bersicht der Tabellen|Inhaltsverzeichnis|Table of contents|Sommaire",
            window,
            re.IGNORECASE,
        )
    )


def _score_anchor(lines: list[str], idx: int, reporting_scope: str) -> int:
    ctx = "\n".join(lines[max(0, idx - 25) : min(len(lines), idx + 5)])
    has_cons = bool(CONSOLIDATED_HINTS.search(ctx))
    has_stand = bool(STANDALONE_HINTS.search(ctx))
    if reporting_scope == "consolidated":
        if has_cons and not has_stand:
            return 3
        if has_stand and not has_cons:
            return -2
        return 1
    else:
        if has_stand and not has_cons:
            return 3
        if has_cons and not has_stand:
            return -1
        return 1


def find_window(
    lines: list[str],
    patterns: list[str],
    before: int = 14,
    after: int = 90,
    require_pipe: bool = True,
    prefer_last: bool = False,
    skip_toc: bool = False,
    reporting_scope: str = "consolidated",
) -> str:
    candidates: list[tuple[int, int]] = []
    for idx, line in enumerate(lines):
        if require_pipe and "|" not in line:
            continue
        if skip_toc and is_toc_region(lines, idx):
            continue
        if any(re.search(pat, line, re.IGNORECASE) for pat in patterns):
            candidates.append((idx, _score_anchor(lines, idx, reporting_scope)))

    if not candidates:
        return ""

    best_score = max(s for _, s in candidates)
    best_indices = [idx for idx, s in candidates if s == best_score]
    anchor = best_indices[-1] if prefer_last else best_indices[0]
    start = max(0, anchor - before)
    end = min(len(lines), anchor + after)
    text = "\n".join(lines[start:end]).strip()
    return text[:MAX_CHUNK_CHARS] if len(text) > MAX_CHUNK_CHARS else text


def find_all_matching_windows(
    lines: list[str],
    patterns: list[str],
    before: int = 14,
    after: int = 55,
    require_pipe: bool = True,
    max_windows: int = 3,
    skip_toc: bool = False,
    reporting_scope: str = "consolidated",
) -> str:
    hits: list[tuple[int, int]] = []
    for idx, line in enumerate(lines):
        if require_pipe and "|" not in line:
            continue
        if skip_toc and is_toc_region(lines, idx):
            continue
        if any(re.search(pat, line, re.IGNORECASE) for pat in patterns):
            hits.append((idx, _score_anchor(lines, idx, reporting_scope)))

    if not hits:
        return ""

    # Sortiere primär nach Scope-Score (absteigend), sekundär nach Position
    hits_sorted = sorted(hits, key=lambda x: (-x[1], x[0]))
    selected_indices: list[int] = []
    for idx, _ in hits_sorted:
        if all(abs(idx - prev) > 35 for prev in selected_indices):
            selected_indices.append(idx)
        if len(selected_indices) >= max_windows:
            break
    selected_indices.sort()

    blocks = [
        "\n".join(lines[max(0, idx - before) : min(len(lines), idx + after)]).strip()
        for idx in selected_indices
    ]
    joined = "\n\n---\n\n".join(b for b in blocks if b)
    return joined[:MAX_CHUNK_CHARS] if len(joined) > MAX_CHUNK_CHARS else joined


def extract_lagebericht_excerpt(lines: list[str], max_chars: int = 7000) -> str:
    collected = []
    total = 0
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("![](") or stripped.startswith("|") or stripped.startswith("<!--"):
            continue
        if re.fullmatch(r"\d{1,3}", stripped):
            continue
        if any(k in stripped.lower() for k in ["impressum", "fotografie", "konzept und design", "druck", "titelbild"]):
            continue
        if len(stripped) > 40 or stripped.startswith("#"):
            collected.append(stripped)
            total += len(stripped) + 1
            if total >= max_chars:
                break
    return "\n".join(collected)


def chunk_report(md_path: Path, cfg: BankConfig) -> dict:
    meta = detect_report_meta(md_path.name, file_prefix=cfg.file_prefix)
    text = md_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    scope = cfg.reporting_scope
    chunks: dict[str, str] = {}

    def anchors_for(key: str) -> list[str]:
        custom = cfg.chunk_anchors.get(key, [])
        return list(custom) if custom else list(DEFAULT_ANCHORS.get(key, []))

    if meta["report_type"] == "annual":
        chunks["bilanz"] = find_all_matching_windows(
            lines, anchors_for("bilanz"), before=18, after=48, max_windows=3, skip_toc=True, reporting_scope=scope
        )
        chunks["erfolgsrechnung"] = find_window(
            lines, anchors_for("erfolgsrechnung"), before=14, after=85, skip_toc=True, reporting_scope=scope
        )
        chunks["mehrjahresvergleich"] = find_window(
            lines,
            anchors_for("mehrjahresvergleich"),
            before=38,
            after=50,
            prefer_last=(meta["year"] >= 2012),
            skip_toc=True,
            reporting_scope=scope,
        )
        chunks["aktie_basisdaten"] = find_window(
            lines, anchors_for("aktie_basisdaten"), before=20, after=42, prefer_last=True, skip_toc=True, reporting_scope=scope
        )
        chunks["betreute_vermoegen"] = find_window(
            lines, anchors_for("betreute_vermoegen"), before=10, after=30, skip_toc=True, reporting_scope=scope
        )
        chunks["verguetung"] = find_all_matching_windows(
            lines, anchors_for("verguetung"), before=10, after=55, max_windows=2, skip_toc=True, reporting_scope=scope
        )
        chunks["lagebericht_strategie"] = extract_lagebericht_excerpt(lines)
    elif meta["report_type"] == "semester":
        chunks["bilanz"] = find_all_matching_windows(
            lines, anchors_for("bilanz"), before=16, after=42, max_windows=2, skip_toc=True, reporting_scope=scope
        )
        chunks["erfolgsrechnung"] = find_window(
            lines, anchors_for("erfolgsrechnung"), before=14, after=80, skip_toc=True, reporting_scope=scope
        )
        chunks["lagebericht_strategie"] = extract_lagebericht_excerpt(lines, max_chars=5500)
    else:
        chunks["km1_eigenmittel"] = find_all_matching_windows(
            lines, anchors_for("km1_eigenmittel"), before=14, after=55, max_windows=4, skip_toc=True, reporting_scope=scope
        )
        chunks["ov1_rwa"] = find_window(
            lines, anchors_for("ov1_rwa"), before=10, after=45, skip_toc=True, reporting_scope=scope
        )

    return {
        "meta": {
            **meta,
            "bank_id": cfg.bank_id,
            "reporting_scope": cfg.reporting_scope,
            "reporting_currency": cfg.reporting_currency,
            "source_file": str(md_path.relative_to(cfg.bank_dir)),
            "total_chars": len(text),
            "total_lines": len(lines),
        },
        "chunks": {k: v for k, v in chunks.items() if v},
    }


def chunk_bank(bank_id: str) -> dict:
    cfg = load_bank_config(bank_id)
    cfg.chunks_dir.mkdir(parents=True, exist_ok=True)
    md_files = sorted(cfg.md_dir.glob("*.md"))
    manifest = {"bank_id": cfg.bank_id, "total_reports": len(md_files), "reports": []}

    for md_path in md_files:
        payload = chunk_report(md_path, cfg)
        out_path = cfg.chunks_dir / f"{md_path.stem}.json"
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        chunk_stats = {
            name: {"chars": len(content), "approx_tokens": max(1, len(content) // 4)}
            for name, content in payload["chunks"].items()
        }
        manifest["reports"].append(
            {
                "stem": md_path.stem,
                "report_type": payload["meta"]["report_type"],
                "year": payload["meta"]["year"],
                "period": payload["meta"]["period"],
                "part": payload["meta"]["part"],
                "chunks": chunk_stats,
            }
        )

    (cfg.chunks_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    max_tok = max(
        (c["approx_tokens"] for r in manifest["reports"] for c in r["chunks"].values()),
        default=0,
    )
    print(f"[OK] {cfg.bank_id}: {len(md_files)} Berichte in {cfg.chunks_dir}/ gechunkt (max ~{max_tok} Tokens).")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Stufe 1: Deterministischer DE/FR/EN Chunker.")
    parser.add_argument("--bank", required=True, help="Bank-ID (z. B. bekb, vskb, zkb, bcv, gekb, raiffeisen, postfinance, ubs)")
    args = parser.parse_args()
    chunk_bank(args.bank)


if __name__ == "__main__":
    main()
