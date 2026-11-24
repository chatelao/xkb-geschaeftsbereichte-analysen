#!/usr/bin/env python3
"""Stufe 4 der Hydrogen-Analysestrategie: Reduce-Phase (7 Mehrjahresberichte + README pro Institut)."""

from __future__ import annotations

import argparse
import json
import os
import urllib.request
from pathlib import Path
from typing import Any

from shared.config import BankConfig, load_bank_config
from shared.it_strategy import IT_STRATEGY_DATA
from shared.leadership import LEADERSHIP_DATA
from shared.mergers import MERGER_HISTORY
from shared.turnover import get_bank_turnover_meta, get_latest_turnover

DEFAULT_HYDROGEN_MODEL = "gemini-2.5-flash-lite"


def fmt_num(val: float | None, digits: int = 1) -> str:
    if val is None:
        return "–"
    return f"{val:,.{digits}f}".replace(",", "'").replace(".", ",")


def fmt_chf(val: float | None) -> str:
    if val is None:
        return "–"
    return f"{val:,.2f}".replace(",", "'")


def _cagr(v_start: float | None, v_end: float | None, years: int) -> float | None:
    if v_start is None or v_end is None or v_start <= 0 or v_end <= 0 or years <= 0:
        return None
    return ((v_end / v_start) ** (1.0 / years) - 1.0) * 100.0


def _table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for r in rows:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def _breaks_text(cfg: BankConfig) -> str:
    if not cfg.structural_breaks:
        return "Keine ausserordentlichen Strukturbrüche konfiguriert."
    return "\n".join(f"- **{b['year']}:** {b['label']}" for b in cfg.structural_breaks)


def _gemini_polish(draft: str, cfg: BankConfig, title: str, api_key: str) -> str:
    prompt = (
        f"Du bist ein Schweizer Bankenanalyst. Verfeinere den folgenden Entwurf für '{cfg.full_name}' ({title}) "
        "sprachlich präzise auf Deutsch. ÄNDERE KEINE ZAHLEN, TABELLEN ODER BILD-LINKS.\n\n"
        f"{draft}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.1},
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{DEFAULT_HYDROGEN_MODEL}:generateContent?key={api_key}"
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        res = json.loads(resp.read().decode("utf-8"))
    return res["candidates"][0]["content"]["parts"][0]["text"]


def build_reports(bank_id: str, backend: str = "local") -> list[Path]:
    cfg = load_bank_config(bank_id)
    panel_path = cfg.data_dir / f"{cfg.bank_id}_panel_all.json"
    if not panel_path.exists():
        raise FileNotFoundError(f"Panel fehlt: {panel_path}. Zuerst shared.validator_kpi ausführen.")
    data = json.loads(panel_path.read_text(encoding="utf-8"))

    annual: list[dict[str, Any]] = data.get("annual", [])
    semester: list[dict[str, Any]] = data.get("semester", [])
    off: list[dict[str, Any]] = data.get("offenlegung", [])
    verg: list[dict[str, Any]] = data.get("verguetung_real", [])

    cfg.reports_dir.mkdir(parents=True, exist_ok=True)
    y0, y1 = (annual[0]["year"], annual[-1]["year"]) if annual else (2025, 2025)
    first, last = (annual[0], annual[-1]) if annual else ({}, {})
    span = max(1, y1 - y0)

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    use_gemini = (backend == "gemini") or (backend == "auto" and bool(api_key))
    if backend == "gemini" and not api_key:
        raise RuntimeError("--backend gemini gewählt, aber GEMINI_API_KEY fehlt.")

    # Bericht 01: Zinszyklen & Ertragsarchitektur
    r01_rows = [
        [
            str(r["year"]),
            fmt_num(r.get("net_interest_income_mio")),
            fmt_num(r.get("commission_income_mio")),
            fmt_num(r.get("trading_income_mio")),
            fmt_num(r.get("total_operating_income_mio")),
            fmt_num(r.get("operating_profit_mio")),
            fmt_num(r.get("net_profit_mio")),
            fmt_num(r.get("interest_share_pct"), 1) + " %",
        ]
        for r in annual
    ]
    r01 = f"""# 01 · Zinszyklen & Ertragsarchitektur ({y0}–{y1}): {cfg.full_name}

> **Scope:** `{cfg.reporting_scope}` | **Standard:** `{cfg.accounting_standard}` | **Währung:** Mio. CHF (harmonisierte Zeitreihe)

## 1. Management Summary
- Im Zeitraum **{y0}–{y1}** entwickelte sich der Geschäftsertrag von **{fmt_num(first.get('total_operating_income_mio'))} Mio. CHF** auf **{fmt_num(last.get('total_operating_income_mio'))} Mio. CHF** (CAGR **{fmt_num(_cagr(first.get('total_operating_income_mio'), last.get('total_operating_income_mio'), span), 2)} % p. a.**).
- Der Reingewinn erreichte im jüngsten Geschäftsjahr {y1} **{fmt_num(last.get('net_profit_mio'))} Mio. CHF** (nach {fmt_num(first.get('net_profit_mio'))} Mio. CHF im Jahr {y0}).
- Der Netto-Zinserfolg trägt aktuell **{fmt_num(last.get('interest_share_pct'), 1)} %** zum Gesamtertrag bei, das Kommissionsgeschäft **{fmt_num(last.get('commission_share_pct'), 1)} %** und das Handelsgeschäft **{fmt_num(last.get('trading_share_pct'), 1)} %**.

![Erfolgsrechnung Wasserfall](./charts/01_erfolgsrechnung_wasserfall_latest.png)

## 2. Quantitative Entwicklung
{_table(["Jahr", "Zinserfolg (Mio.)", "Kommission (Mio.)", "Handel (Mio.)", "Geschäftsertrag", "Geschäftserfolg", "Reingewinn", "Zinsanteil"], r01_rows)}

![Ertrag, Aufwand & Marge](./charts/01_ertrag_kosten_marge_kombi.png)

## 3. Treiberanalyse & Wendepunkte
{_breaks_text(cfg)}

## 4. Fazit & Ausblick
- Die Ertragsarchitektur von {cfg.short_name} spiegelt die Zinszyklen (Negativzinsphase 2015–2022, Zinswende 2022–2024, Zinssenkungen ab 2025) unmittelbar wider.
"""

    # Bericht 02: Bilanzwachstum, Hypotheken & Refinanzierung
    r02_rows = [
        [
            str(r["year"]),
            fmt_num(r.get("total_assets_mio")),
            fmt_num(r.get("mortgage_loans_mio")),
            fmt_num(r.get("financial_investments_mio")),
            fmt_num(r.get("customer_deposits_mio")),
            fmt_num(r.get("shareholders_equity_mio")),
            fmt_num(r.get("deposit_coverage_pct"), 1) + " %",
        ]
        for r in annual
    ]
    credit_note = (
        "Aufgrund des gesetzlichen **Kreditverbots (`has_credit_ban: true`)** weist PostFinance keine Hypothekarforderungen aus; die Aktivseite wird von Finanzanlagen und SNB-Guthaben dominiert."
        if cfg.has_credit_ban
        else f"Die Hypothekarforderungen machen im Jahr {y1} **{fmt_num(last.get('mortgage_share_pct'), 1)} %** der Bilanzsumme aus."
    )
    r02 = f"""# 02 · Bilanzwachstum, Hypotheken & Refinanzierung ({y0}–{y1}): {cfg.full_name}

## 1. Management Summary
- Die Bilanzsumme wuchs von **{fmt_num(first.get('total_assets_mio'))} Mio. CHF** ({y0}) auf **{fmt_num(last.get('total_assets_mio'))} Mio. CHF** ({y1}, CAGR **{fmt_num(_cagr(first.get('total_assets_mio'), last.get('total_assets_mio'), span), 2)} %**).
- {credit_note}
- Die Kundeneinlagen belaufen sich {y1} auf **{fmt_num(last.get('customer_deposits_mio'))} Mio. CHF**, das Eigenkapital auf **{fmt_num(last.get('shareholders_equity_mio'))} Mio. CHF** (Eigenkapitalquote **{fmt_num(last.get('equity_ratio_pct'), 2)} %**).

![Bilanz Gestapelte Säulen](./charts/02_bilanz_gestapelte_saeulen_latest.png)

## 2. Quantitative Entwicklung
{_table(["Jahr", "Bilanzsumme", "Hypotheken", "Finanzanlagen", "Kundeneinlagen", "Eigenkapital", "Deckungsgrad"], r02_rows)}

![Bilanz Treemap](./charts/02_bilanz_treemap_latest.png)
![Bilanz Sankey](./charts/02_bilanz_sankey_latest.png)
![Bilanz Langfristwachstum](./charts/02_bilanz_langfrist_wachstum.png)

## 3. Treiberanalyse & Wendepunkte
{_breaks_text(cfg)}

## 4. Fazit & Ausblick
- Refinanzierungsbasis und Bilanzstruktur bleiben eng an Kundeneinlagen und die jeweilige Geschäftsmodell-Spezialisierung gekoppelt.
"""

    # Bericht 03: Aufsichtsrechtliche Resilienz & Basel III
    r03_rows = [
        [
            r["period"],
            r.get("regime", "Basel III"),
            fmt_num(r.get("rwa_total_mio")),
            fmt_num(r.get("cet1_capital_mio")),
            fmt_num(r.get("cet1_ratio_pct"), 2) + " %",
            fmt_num(r.get("total_capital_ratio_pct"), 2) + " %",
            fmt_num(r.get("leverage_ratio_pct"), 2) + " %",
            fmt_num(r.get("lcr_pct"), 1) + " %",
            fmt_num(r.get("nsfr_pct"), 1) + " %",
        ]
        for r in off
    ]
    last_off = off[-1] if off else {}
    r03 = f"""# 03 · Aufsichtsrechtliche Resilienz & Basel III: {cfg.full_name}

> **FINMA-Kategorie:** Kategorie {cfg.finma_category} | **CET1-Zielgrösse:** {fmt_num(cfg.capital_targets_pct.get('cet1_target'), 2)} % | **Gesamtkapital-Ziel:** {fmt_num(cfg.capital_targets_pct.get('total_capital_target'), 2)} %

## 1. Management Summary
- Am jüngsten Offenlegungsstichtag (**{last_off.get('period', '–')}**, Regime: *{last_off.get('regime', 'Basel III')}*) beträgt die **CET1-Quote {fmt_num(last_off.get('cet1_ratio_pct'), 2)} %** (Puffer über Ziel: **{fmt_num(last_off.get('cet1_excess_over_target_pp'), 2)} Prozentpunkte**).
- Die Gesamtkapitalquote liegt bei **{fmt_num(last_off.get('total_capital_ratio_pct'), 2)} %**, die Leverage Ratio bei **{fmt_num(last_off.get('leverage_ratio_pct'), 2)} %**.
- Liquiditätsquoten: LCR **{fmt_num(last_off.get('lcr_pct'), 1)} %**, NSFR **{fmt_num(last_off.get('nsfr_pct'), 1)} %** (Mindestanforderung je 100 %).

![Soll-Ist-Vergleich](./charts/03_soll_ist_vergleich_horizontal_latest.png)

## 2. Quantitative Entwicklung ({len(off)} Stichtage)
{_table(["Periode", "Regime", "RWA (Mio.)", "CET1 (Mio.)", "CET1 %", "Gesamtkap. %", "Leverage %", "LCR %", "NSFR %"], r03_rows)}

![Kapital & RWA Basel III](./charts/03_kapital_rwa_basel.png)

## 3. Treiberanalyse & Wendepunkte
- Mit Inkrafttreten von **Basel III final** ab 01.01.2025 verändern sich risikogewichtete Aktiven (RWA) und RWA-Dichte durch angepasste Standard- bzw. Output-Floor-Vorgaben.

## 4. Fazit & Ausblick
- Die Eigenmittel- und Liquiditätspuffer übertreffen die regulatorischen Mindestanforderungen für FINMA-Kategorie {cfg.finma_category} deutlich.
"""

    # Bericht 04: Operative Effizienz & Transformation
    t_meta = get_bank_turnover_meta(cfg.bank_id)
    t_yrs_map = t_meta.get("years", {})
    latest_t_yr, latest_t_entry = get_latest_turnover(cfg.bank_id, y1)
    r04_rows = [
        [
            str(r["year"]),
            fmt_num(r.get("cir_pct"), 2) + " %",
            fmt_num(r.get("roe_pct"), 2) + " %",
            fmt_num(r.get("fte_count"), 1),
            (fmt_num(r.get("turnover_rate_pct"), 1) + " %") if r.get("turnover_rate_pct") is not None else "–",
            fmt_num(r.get("income_per_fte_tchf"), 1),
            fmt_num(r.get("personnel_cost_per_fte_tchf"), 1),
            fmt_num(r.get("wage_to_productivity_pct"), 1) + " %",
            fmt_num(r.get("productivity_to_wage_ratio"), 2) + "×",
            fmt_num(r.get("assets_per_fte_mio"), 2),
        ]
        for r in annual
    ]
    r04_turnover_bullet = (
        f"\n- **Personalfluktuation:** Jüngster offengelegter Wert liegt im Jahr **{latest_t_yr}** bei **{fmt_num(latest_t_entry.get('rate'), 1)} %** (*{t_meta.get('basis', '–')}*)."
        if latest_t_yr and latest_t_entry
        else "\n- **Personalfluktuation:** Im Geschäftsbericht wird keine quantitative Personalfluktuationsquote ausgewiesen."
    )
    r04 = f"""# 04 · Operative Effizienz & Transformation ({y0}–{y1}): {cfg.full_name}

## 1. Management Summary
- Die Cost-Income-Ratio (CIR) liegt im Jahr {y1} bei **{fmt_num(last.get('cir_pct'), 2)} %** (vs. {fmt_num(first.get('cir_pct'), 2)} % im Jahr {y0}), die Eigenkapitalrendite (ROE) bei **{fmt_num(last.get('roe_pct'), 2)} %**.
- Der Personalbestand umfasst {y1} **{fmt_num(last.get('fte_count'), 1)} FTE** bei einem Ertrag pro Vollzeitstelle von **{fmt_num(last.get('income_per_fte_tchf'), 1)} TCHF** und einem **Lohnkosten-/Produktivitätsverhältnis von {fmt_num(last.get('wage_to_productivity_pct'), 1)} %** (bzw. **{fmt_num(last.get('productivity_to_wage_ratio'), 2)}×** Ertrag je CHF Personalaufwand).{r04_turnover_bullet}

## 2. Quantitative Entwicklung
{_table(["Jahr", "CIR %", "ROE %", "FTE", "Fluktuation %", "Ertrag/FTE (TCHF)", "Lohn/FTE (TCHF)", "Lohn/Ertrag %", "Ertrag/Lohn", "Bilanz/FTE (Mio.)"], r04_rows)}

![Effizienz & Produktivität](./charts/04_effizienz_produktivitaet.png)

## 3. Treiberanalyse & Wendepunkte
{_breaks_text(cfg)}

## 4. Fazit & Ausblick
- Digitalisierung und Skalierung steigern Bilanzsumme und Geschäftsvolumen pro Vollzeitstelle langfristig.
"""

    # Vorsorge-Metadaten laden (Phase V2/V3)
    vorsorge_path = cfg.data_dir / f"{cfg.bank_id}_vorsorge.json"
    vorsorge = json.loads(vorsorge_path.read_text(encoding="utf-8")) if vorsorge_path.exists() else {}

    # Bericht 05: Eigentümer-Wertschöpfung (4 Modi) + Investoren-KPIs
    mode_titles = {
        "listed_share": "Aktie, Dividenden & Investoren-Wertschöpfung",
        "cantonal_endowment": "Dotationskapital, Ausschüttung & Kanton",
        "cooperative_payout": "Genossenschaftskapital, Mitglieder & Ausschüttung",
        "post_dividend": "Dividendenablieferung an Post AG & Eigentümerwert",
    }
    r05_title = mode_titles.get(cfg.report_05_mode, "Eigentümer & Wertschöpfung")
    r05_rows = [
        [
            str(r["year"]),
            fmt_num(r.get("net_profit_mio")),
            fmt_num(r.get("shareholders_equity_mio")),
            fmt_chf(r.get("share_price_eoy")),
            fmt_chf(r.get("dividend_per_share")),
            fmt_num(r.get("dividend_yield_pct"), 2) + " %",
            fmt_num(r.get("contribution_public_mio")),
        ]
        for r in annual
    ]
    inv_notes = []
    if cfg.listed and last.get("share_price_eoy") and last.get("dividend_per_share"):
        inv_notes.append(f"- **Aktuelle Ausschüttung ({y1}):** Kurs **{fmt_chf(last.get('share_price_eoy'))} CHF**, Dividende **{fmt_chf(last.get('dividend_per_share'))} CHF** (Rendite **{fmt_num(last.get('dividend_yield_pct'), 2)} %**).")
    else:
        inv_notes.append(f"- **Eigenkapitalrendite ({y1}):** ROE **{fmt_num(last.get('roe_pct'), 2)} %** bei einem Eigenkapital von **{fmt_num(last.get('shareholders_equity_mio'))} Mio. CHF**.")
    r05 = f"""# 05 · {r05_title} ({y0}–{y1}): {cfg.full_name}

> **Eigentümer-Modus:** `{cfg.report_05_mode}` | **Staatsgarantie:** {'Ja' if cfg.state_guarantee else 'Keine'} | **Ticker:** `{cfg.ticker or 'nicht kotiert'}`

## 1. Management Summary
- Im Geschäftsjahr {y1} erwirtschaftete {cfg.short_name} einen Gewinn von **{fmt_num(last.get('net_profit_mio'))} Mio. CHF** bei einem Eigenkapital von **{fmt_num(last.get('shareholders_equity_mio'))} Mio. CHF**.
{chr(10).join(inv_notes)}

## 2. Quantitative Entwicklung
{_table(["Jahr", "Reingewinn (Mio.)", "Eigenkapital (Mio.)", "Aktienkurs (split-ber.)", "Dividende/Aktie", "Div.-Rendite", "Öff. Ablieferung (Mio.)"], r05_rows)}

![Eigentümer & Wertschöpfung](./charts/05_eigentuemer_wertschoepfung.png)

## 3. Treiberanalyse & Wendepunkte (Investoren-Perspektive)
- Bei kotierten Instituten mit Aktiensplits (z. B. BCV 1:10 im Jahr 2020) sind sämtliche historischen Kurs- und Dividendenreihen deterministisch split-bereinigt.
- Im Branchenvergleich (siehe `comparison/reports/06_investoren_branchenvergleich.md`) werden P/B, P/E, Dividendenrendite und Eigentümer-Ablieferungen über alle 19 Institute eingeordnet.

## 4. Fazit, Führungsleistung & Ausblick
- Stabile Ertragskraft sichert langfristig Dividendenkontinuität bzw. verlässliche Ablieferungen an Kanton, Post oder Genossenschafter.
- Die detaillierte Leistungsbilanz von CEO und Verwaltungsratspräsidium aus Investoren- und Eigentümersicht findet sich im [CEO & Chairman of the Board Achievement Report](./08_ceo_und_vrp_leistungsbericht.md).
"""

    # Bericht 06: Unterjährige Dynamik (Semesterberichte)
    r06_rows = [
        [
            r["period"],
            fmt_num(r.get("total_assets_mio")),
            fmt_num(r.get("net_interest_income_mio")),
            fmt_num(r.get("total_operating_income_mio")),
            fmt_num(r.get("operating_profit_mio")),
            fmt_num(r.get("net_profit_mio")),
        ]
        for r in semester
    ]
    last_sem = semester[-1] if semester else {}
    r06 = f"""# 06 · Unterjährige Dynamik (Semesterberichte): {cfg.full_name}

## 1. Management Summary
- Vorliegen von **{len(semester)} Halbjahresabschlüssen**; jüngster Stichtag ist **{last_sem.get('period', '–')}** mit einem Geschäftsertrag von **{fmt_num(last_sem.get('total_operating_income_mio'))} Mio. CHF** und einem Halbjahresgewinn von **{fmt_num(last_sem.get('net_profit_mio'))} Mio. CHF**.

## 2. Quantitative Entwicklung
{_table(["Periode", "Bilanzsumme", "Zinserfolg H1", "Geschäftsertrag H1", "Geschäftserfolg H1", "Reingewinn H1"], r06_rows)}

![Semester Saisonalität](./charts/06_semester_saisonalitaet_reserven.png)

## 3. Treiberanalyse & Wendepunkte
- Der Vergleich von H1-Werten gegen die jeweiligen Gesamtjahresergebnisse (FY) zeigt die saisonale Ertragsverteilung und Reservebildung im zweiten Halbjahr.

## 4. Fazit & Ausblick
- Die Halbjahresberichte ermöglichen ein zeitnahes Monitoring der Zinsmargen- und Kreditvolumen-Dynamik bis H1-2026.
"""

    # Bericht 07: Strategische Epochen, Governance, reale Vergütung & Vorsorgeeinrichtung
    epoch_lines = "\n".join(f"- **{e['label']} ({e['start']}–{e['end']}):** {e['title']}" for e in cfg.epochs)
    r07_rows = [
        [
            str(r["year"]),
            fmt_num(r.get("net_profit_mio_nom")),
            fmt_num(r.get("net_profit_mio_real2025")),
            fmt_num(r.get("avg_per_fte_tchf_real2025"), 1),
            (fmt_num(r.get("turnover_rate_pct"), 1) + " %") if r.get("turnover_rate_pct") is not None else "–",
            fmt_num(r.get("vr_total_tchf_real2025"), 1),
            fmt_num(r.get("ceo_total_tchf_real2025"), 1),
            fmt_num(r.get("gl_total_tchf_real2025"), 1),
        ]
        for r in verg
    ]
    last_verg = verg[-1] if verg else {}
    pay_ratio = (
        round(last_verg["ceo_total_tchf_real2025"] / last_verg["avg_per_fte_tchf_real2025"], 1)
        if last_verg.get("ceo_total_tchf_real2025") and last_verg.get("avg_per_fte_tchf_real2025")
        else None
    )
    if t_yrs_map:
        t_series_str = ", ".join(
            f"**{yr}:** {fmt_num(t_yrs_map[yr].get('rate'), 1)} %"
            + (
                f" (Netto {fmt_num(t_yrs_map[yr].get('net'), 1)} % / Brutto {fmt_num(t_yrs_map[yr].get('gross'), 1)} %)"
                if (t_yrs_map[yr].get("net") is not None and t_yrs_map[yr].get("gross") is not None)
                else ""
            )
            for yr in sorted(t_yrs_map.keys())
        )
        turnover_block = (
            f"- **Personalfluktuation ({len(t_yrs_map)} Berichtsjahre, {min(t_yrs_map)}–{max(t_yrs_map)}):** {t_series_str}\n"
            f"- **Methodik & Quelle Fluktuation:** {t_meta.get('basis', '–')} (`{t_meta.get('source', '–')}`)"
        )
    else:
        turnover_block = "- **Personalfluktuation:** Keine quantitative Fluktuationsquote in den Geschäftsberichten offengelegt."
    pk_block = (
        f"- **Vorsorgeeinrichtung:** {vorsorge.get('pk_name', '–')} (*{vorsorge.get('pk_plan_type', '–')}*, Basis: `{vorsorge.get('accounting_basis', '–')}`)\n"
        f"- **Versichertenstruktur:** Aktive **{fmt_num(vorsorge.get('active_insured_count'), 0)}**, Rentner **{fmt_num(vorsorge.get('pensioners_count'), 0)}** (Verhältnis Aktive/Rentner: **{fmt_num(vorsorge.get('active_to_pensioner_ratio'), 2)}**)\n"
        f"- **Deckungsgrad (BVG) / Reserven:** Deckungsgrad **{fmt_num(vorsorge.get('coverage_ratio_bvg_pct'), 1)} %**, Arbeitgeberbeitragsreserve **{fmt_num(vorsorge.get('employer_contribution_reserve_mio'), 1)} Mio. CHF**, Sondereinlagen **{fmt_num(vorsorge.get('extraordinary_contributions_mio'), 1)} Mio. CHF**\n"
        f"- **CEO-zu-Mitarbeitenden-Pay-Ratio ({y1}):** **{fmt_num(pay_ratio, 1)}×** (CEO real 2025: {fmt_num(last_verg.get('ceo_total_tchf_real2025'), 1)} TCHF vs. Ø Personalaufwand/FTE: {fmt_num(last_verg.get('avg_per_fte_tchf_real2025'), 1)} TCHF)\n"
        f"- **Quelle Vorsorge:** `{vorsorge.get('source_url_or_file', '–')}` — {vorsorge.get('notes', '')}\n"
        f"{turnover_block}"
        if vorsorge
        else f"- Keine Vorsorgedaten hinterlegt.\n{turnover_block}"
    )
    r07 = f"""# 07 · Strategische Epochen, Governance, reale Vergütung & Vorsorge ({y0}–{y1}): {cfg.full_name}

> **Preisbasis:** Sämtliche Realgrössen sind mit dem offiziellen **BFS Landesindex der Konsumentenpreise (LIK, Dez. 1982 = 100)** deterministisch auf **reale CHF 2025** deflationiert.

## 1. Management Summary & Strategische Epochen
{epoch_lines}

![Langfrist Dashboard Epochen](./charts/07_langfrist_dashboard_epochen.png)

## 2. Reale Gewinn-, Lohn- & Vergütungsentwicklung (real 2025 CHF)
{_table(["Jahr", "Gewinn nom.", "Gewinn real 2025", "Lohn/FTE real (TCHF)", "Fluktuation %", "VR real (TCHF)", "CEO real (TCHF)", "GL real (TCHF)"], r07_rows)}

![Gewinn, Löhne & Vergütung real](./charts/07_gewinn_loehne_verguetung_real.png)

## 3. Arbeitgeber-Attraktivität, Personalfluktuation & Vorsorgeeinrichtung (Pensionskasse)
{pk_block}

## 4. Treiberanalyse, Strukturbrüche & Ausblick
{_breaks_text(cfg)}
- Die gemeinsame Inflationsbereinigung auf `real 2025 CHF` ermöglicht den unverzerrten Vergleich von Produktivität, Reallöhnen, Personalfluktuation, Pay Ratio und Pensionskassen-Resilienz im Branchenvergleich (`comparison/reports/07_mitarbeiter_und_vorsorge_branchenvergleich.md`).
"""

    # Bericht 08: CEO & Chairman of the Board Achievement Report (Investoren-Sektion)
    lead = LEADERSHIP_DATA.get(cfg.bank_id, {})
    first = annual[0] if annual else {}
    n_yrs = max(1, (last.get("year", 2025) - first.get("year", 2025))) if annual else 1
    ta_cagr = _cagr(first.get("total_assets_mio"), last.get("total_assets_mio"), n_yrs)
    inc_cagr = _cagr(first.get("total_operating_income_mio"), last.get("total_operating_income_mio"), n_yrs)
    np_cagr = _cagr(first.get("net_profit_mio"), last.get("net_profit_mio"), n_yrs)
    cir_delta = (
        round(last["cir_pct"] - first["cir_pct"], 2)
        if last.get("cir_pct") is not None and first.get("cir_pct") is not None
        else None
    )
    roe_delta = (
        round(last["roe_pct"] - first["roe_pct"], 2)
        if last.get("roe_pct") is not None and first.get("roe_pct") is not None
        else None
    )
    cet1_latest = last_off.get("cet1_ratio_pct") if last_off else None
    cet1_target = cfg.capital_targets_pct.get("cet1_target")
    cet1_buf = round(cet1_latest - cet1_target, 2) if cet1_latest is not None and cet1_target is not None else None

    scorecard_rows = [
        ["Bilanzsumme (Mio. CHF)", fmt_num(first.get("total_assets_mio")), fmt_num(last.get("total_assets_mio")), f"CAGR {fmt_num(ta_cagr, 2)} % p.a."],
        ["Geschäftsertrag (Mio. CHF)", fmt_num(first.get("total_operating_income_mio")), fmt_num(last.get("total_operating_income_mio")), f"CAGR {fmt_num(inc_cagr, 2)} % p.a."],
        ["Reingewinn (Mio. CHF)", fmt_num(first.get("net_profit_mio")), fmt_num(last.get("net_profit_mio")), f"CAGR {fmt_num(np_cagr, 2)} % p.a."],
        ["Cost-Income-Ratio (CIR)", f"{fmt_num(first.get('cir_pct'), 2)} %", f"{fmt_num(last.get('cir_pct'), 2)} %", f"{fmt_num(cir_delta, 2)} Pp."],
        ["Eigenkapitalrendite (ROE)", f"{fmt_num(first.get('roe_pct'), 2)} %", f"{fmt_num(last.get('roe_pct'), 2)} %", f"{fmt_num(roe_delta, 2)} Pp."],
        ["Ertrag pro FTE (TCHF)", fmt_num(first.get("income_per_fte_tchf"), 1), fmt_num(last.get("income_per_fte_tchf"), 1), "Operative Produktivität"],
        ["Lohnkosten / Produktivität", f"{fmt_num(first.get('wage_to_productivity_pct'), 1)} %", f"{fmt_num(last.get('wage_to_productivity_pct'), 1)} %", "Personalaufwand / Ertrag"],
        ["CET1-Quote (vs. Zielgrösse)", "–", f"{fmt_num(cet1_latest, 2)} %", f"Puffer {fmt_num(cet1_buf, 2)} Pp. (Ziel {fmt_num(cet1_target, 1)} %)"],
    ]
    ach_lines = "\n".join(f"- {a}" for a in lead.get("achievements", [])) or "- Keine spezifischen Meilensteine hinterlegt."
    comp_alignment = (
        f"- **Reale Vergütung ({y1}, Basis 2025 CHF):** VR gesamt **{fmt_num(last_verg.get('vr_total_tchf_real2025'), 1)} TCHF**, CEO **{fmt_num(last_verg.get('ceo_total_tchf_real2025'), 1)} TCHF**, GL gesamt **{fmt_num(last_verg.get('gl_total_tchf_real2025'), 1)} TCHF**.\n"
        f"- **CEO-zu-Mitarbeitenden-Pay-Ratio:** **{fmt_num(pay_ratio, 1)}×** (Ø Personalaufwand/FTE real: {fmt_num(last_verg.get('avg_per_fte_tchf_real2025'), 1)} TCHF)."
        if last_verg.get("ceo_total_tchf_real2025")
        else f"- **Vergütungs-Alignment ({y1}):** Ø Personalaufwand pro FTE (real 2025) beträgt **{fmt_num(last_verg.get('avg_per_fte_tchf_real2025'), 1)} TCHF** bei einer Lohnkosten-/Produktivitätsquote von **{fmt_num(last.get('wage_to_productivity_pct'), 1)} %**. (Einzelvergütungen VR/CEO werden je nach Rechtsform im Vergütungs- bzw. Geschäftsbericht offengelegt.)"
    )
    r08 = f"""# 08 · CEO & Chairman of the Board Achievement Report ({y0}–{y1}): {cfg.full_name}

> **Investor & Governance Brief** | **Aktueller Chairman:** {lead.get('chairman_name', '–')} (*{lead.get('chairman_title', '–')}*) | **Aktueller CEO:** {lead.get('ceo_name', '–')} (*{lead.get('ceo_title', '–')}*)

## 1. Executive Governance Profile
- **Institut:** {cfg.full_name} (`{cfg.bank_id}`) — {lead.get('governance_model', cfg.legal_form)}
- **Eigentümer- & Investoren-Modus:** `{cfg.report_05_mode}` | **FINMA-Kategorie:** {cfg.finma_category} | **Staatsgarantie:** {'Ja' if cfg.state_guarantee else 'Keine'}
- **Verwaltungsratspräsidium (Chairman of the Board):** **{lead.get('chairman_name', '–')}** ({lead.get('chairman_title', '–')})
- **Operative Gesamtleitung (CEO):** **{lead.get('ceo_name', '–')}** ({lead.get('ceo_title', '–')})

## 2. Historische & aktuelle CEO- / VR-Präsidiums-Chronik ({y0}–{y1})
{_table(["Amtszeit", "Funktion", "Name", "Schwerpunkt & Kontext"], lead.get("timeline", []))}

## 3. Quantitative Performance Scorecard ({y0}–{y1})
{_table(["Kennzahl", f"Start ({y0})", f"Aktuell ({y1})", "Veränderung / Einordnung"], scorecard_rows)}

## 4. Strategische Leistungsbilanz & Meilensteine (CEO & VR-Präsidium)
{ach_lines}

## 5. Vergütungs- & Eigentümer-Alignment
{comp_alignment}
- **Investoren-Einordnung:** Siehe auch [{r05_title}](./{cfg.report_05_slug}.md) sowie den institutsübergreifenden Vergleich in `comparison/reports/06_investoren_branchenvergleich.md`.
- **Quellenbasis:** `{lead.get('source', 'Geschäftsbericht 2025')}` & historische Geschäftsberichte ({y0}–{y1})
"""

    # Bericht 09: IT Strategy & Digital Transformation
    it = IT_STRATEGY_DATA.get(cfg.bank_id, {})
    it_bullets = "\n".join(f"- {item}" for item in it.get("cloud_ai_data", [])) or "- Keine spezifischen Cloud-/AI-Initiativen dokumentiert."
    it_rows = [
        [
            str(r["year"]),
            fmt_num(r.get("general_expenses_mio")),
            fmt_num(r.get("total_operating_expenses_mio")),
            f"{fmt_num(r.get('cir_pct'), 2)} %",
            fmt_num(r.get("income_per_fte_tchf"), 1),
        ]
        for r in annual
    ]
    r09 = f"""# 09 · IT Strategy & Digital Transformation ({y0}–{y1}): {cfg.full_name}

> **Core Banking:** {it.get('core_banking', '–')} | **Betriebsmodell:** {it.get('operating_model', '–')}

## 1. IT-Architektur & Kernbankensystem
- **Kernbankensystem:** {it.get('core_banking', '–')}
- **Betriebs- & Sourcing-Modell:** {it.get('operating_model', '–')}
- **Digitale Kundenschnittstellen:** {it.get('digital_channels', '–')}

## 2. Cloud, Daten & Künstliche Intelligenz (AI)
{it_bullets}

## 3. Kosten-, Effizienz- & Produktivitätskontext ({y0}–{y1})
{_table(["Jahr", "Sachaufwand (inkl. IT, Mio.)", "Geschäftsaufwand (Mio.)", "CIR (%)", "Ertrag/FTE (TCHF)"], it_rows)}

## 4. Cybersicherheit, Resilienz & Ausblick
- **Cyber- & OpRisk-Governance:** {it.get('cyber_resilience', '–')}
- **Quellenbasis:** `{it.get('sources', 'Geschäftsbericht 2025 & öffentliche Fachpublikationen')}`
"""

    # Bericht 10: Fusionsbaum & Institutsgeschichte seit 1900
    mh = MERGER_HISTORY.get(cfg.bank_id, {})
    mh_mermaid = mh.get("mermaid", "flowchart TD\n    A[\"Keine Fusionsdaten hinterlegt\"]")
    mh_rows = mh.get("milestones", [])
    r10 = f"""# 10 · Fusionsbaum & Institutsgeschichte seit 1900: {cfg.full_name}

> **Gründung / Ursprung:** {mh.get('founded', '–')} | **Aktuelle Rechtsform:** `{cfg.legal_form}` | **FINMA-Kategorie:** {cfg.finma_category}

## 1. Überblick der Institutslinie (1900–2026)
{mh.get('lineage_summary', 'Keine historische Zusammenfassung hinterlegt.')}

## 2. Fusionsbaum (Mermaid-Diagramm seit 1900)
```mermaid
{mh_mermaid}
```

## 3. Chronologische Meilensteine (Fusionen, Übernahmen & Rechtsformwechsel)
{_table(["Jahr / Zeitraum", "Institut / Ereignis", "Typ", "Bedeutung & Auswirkung"], mh_rows)}

- **Quellenbasis:** `{mh.get('sources', 'Historische Geschäftsberichte & offizielle Institutschronik')}`
"""

    reports_spec = [
        ("01_zinszyklen_und_ertragsarchitektur.md", r01, "Zinszyklen & Ertragsarchitektur"),
        ("02_bilanzwachstum_hypotheken_und_refinanzierung.md", r02, "Bilanzwachstum & Refinanzierung"),
        ("03_aufsichtsrechtliche_resilienz_basel_iii.md", r03, "Basel III & Resilienz"),
        ("04_operative_effizienz_und_transformation.md", r04, "Operative Effizienz"),
        (f"{cfg.report_05_slug}.md", r05, r05_title),
        ("06_unterjaehrige_dynamik_semesterberichte.md", r06, "Unterjährige Dynamik"),
        ("07_strategische_epochen_und_governance.md", r07, "Strategische Epochen & Governance"),
        ("08_ceo_und_vrp_leistungsbericht.md", r08, "CEO & Chairman Achievement Report"),
        ("09_it_strategie_und_digitalisierung.md", r09, "IT Strategy & Digital Transformation"),
        ("10_fusionsbaum_und_historie.md", r10, "Fusionsbaum & Historie seit 1900"),
    ]

    written: list[Path] = []
    for fname, body, title in reports_spec:
        final_body = _gemini_polish(body, cfg, title, api_key) if use_gemini else body
        p = cfg.reports_dir / fname
        p.write_text(final_body, encoding="utf-8")
        written.append(p)

    readme = [
        f"# Berichte: {cfg.full_name} (`{cfg.bank_id}`)",
        "",
        "Deterministisch generierte Mehrjahresberichte aus den validierten CSV/JSON-Panels.",
        "",
    ] + [f"- [{t}](./{fn})" for fn, _, t in reports_spec]
    (cfg.reports_dir / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    print(f"[OK] {cfg.bank_id}: {len(reports_spec)} Berichte in {cfg.reports_dir}/ erzeugt (Backend={'gemini' if use_gemini else 'local'}).")
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Stufe 4: Reduce / Berichtsgenerator.")
    parser.add_argument("--bank", required=True, help="Bank-ID")
    parser.add_argument("--backend", choices=["auto", "local", "gemini"], default="local")
    args = parser.parse_args()
    build_reports(args.bank, backend=args.backend)


if __name__ == "__main__":
    main()
