#!/usr/bin/env python3
"""Schritt 2 (Phase 8): Harmonisierungs-Layer & Institutsübergreifende Auswertung (19 Banken)."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from shared.config import BankConfig, REPO_ROOT, VALID_BANKS, load_bank_config
from shared.cpi_bfs import deflate_to_real_2025

COMP_DIR = REPO_ROOT / "comparison"
COMP_DATA = COMP_DIR / "data"
COMP_REPORTS = COMP_DIR / "reports"
COMP_CHARTS = COMP_REPORTS / "charts"

plt.rcParams.update({
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "font.size": 9,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.grid": True,
    "grid.alpha": 0.25,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def fmt(v: float | None, d: int = 1) -> str:
    if v is None:
        return "–"
    return f"{v:,.{d}f}".replace(",", "'").replace(".", ",")


def _table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for r in rows:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    cols: list[str] = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def _cagr(v0: float | None, v1: float | None, yrs: int) -> float | None:
    if v0 is None or v1 is None or v0 <= 0 or v1 <= 0 or yrs <= 0:
        return None
    return ((v1 / v0) ** (1.0 / yrs) - 1.0) * 100.0


def _save(fig: plt.Figure, path: Path) -> Path:
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def _extraordinary_flag(bank_id: str, year: int) -> str:
    if bank_id == "ubs" and year == 2023:
        return "CS_NEGATIVE_GOODWILL"
    if bank_id == "bekb" and year == 2015:
        return "PK_SANIERUNG_EINMALIG"
    if bank_id == "zkb" and year == 2024:
        return "CUSTODY_AUM_RECLASS"
    return ""


def run_comparison(backend: str = "local") -> dict[str, Any]:
    COMP_DATA.mkdir(parents=True, exist_ok=True)
    COMP_REPORTS.mkdir(parents=True, exist_ok=True)
    COMP_CHARTS.mkdir(parents=True, exist_ok=True)

    configs: dict[str, BankConfig] = {b: load_bank_config(b) for b in VALID_BANKS}
    panels: dict[str, dict] = {}
    for b, cfg in configs.items():
        p = cfg.data_dir / f"{b}_panel_all.json"
        if not p.exists():
            raise FileNotFoundError(f"Panel fehlt für {b}: {p}")
        panels[b] = json.loads(p.read_text(encoding="utf-8"))

    annual_rows: list[dict] = []
    sem_rows: list[dict] = []
    off_rows: list[dict] = []
    verg_rows: list[dict] = []

    for b in VALID_BANKS:
        cfg = configs[b]
        meta_cols = {
            "bank_id": b,
            "short_name": cfg.short_name,
            "peer_group": cfg.peer_group,
            "reporting_scope": cfg.reporting_scope,
            "accounting_standard": cfg.accounting_standard,
            "state_guarantee": cfg.state_guarantee,
            "has_credit_ban": cfg.has_credit_ban,
            "finma_category": cfg.finma_category,
            "currency_orig": cfg.reporting_currency,
        }
        for r in panels[b].get("annual", []):
            yr = int(r["year"])
            annual_rows.append({
                **meta_cols,
                "year": yr,
                "period": r.get("period"),
                "extraordinary_flag": _extraordinary_flag(b, yr),
                "total_assets_mio": r.get("total_assets_mio"),
                "mortgage_loans_mio": r.get("mortgage_loans_mio"),
                "financial_investments_mio": r.get("financial_investments_mio"),
                "customer_deposits_mio": r.get("customer_deposits_mio"),
                "shareholders_equity_mio": r.get("shareholders_equity_mio"),
                "net_interest_income_mio": r.get("net_interest_income_mio"),
                "commission_income_mio": r.get("commission_income_mio"),
                "trading_income_mio": r.get("trading_income_mio"),
                "total_operating_income_mio": r.get("total_operating_income_mio"),
                "total_operating_income_real2025_mio": round(deflate_to_real_2025(r.get("total_operating_income_mio"), yr), 3) if r.get("total_operating_income_mio") is not None else None,
                "total_operating_expenses_mio": r.get("total_operating_expenses_mio"),
                "operating_profit_mio": r.get("operating_profit_mio"),
                "net_profit_mio": r.get("net_profit_mio"),
                "net_profit_real2025_mio": round(deflate_to_real_2025(r.get("net_profit_mio"), yr), 3) if r.get("net_profit_mio") is not None else None,
                "cir_pct": r.get("cir_pct"),
                "roe_pct": r.get("roe_pct"),
                "roa_pct": r.get("roa_pct"),
                "interest_share_pct": r.get("interest_share_pct"),
                "commission_share_pct": r.get("commission_share_pct"),
                "trading_share_pct": r.get("trading_share_pct"),
                "mortgage_share_pct": r.get("mortgage_share_pct"),
                "deposit_coverage_pct": r.get("deposit_coverage_pct"),
                "equity_ratio_pct": r.get("equity_ratio_pct"),
                "fte_count": r.get("fte_count"),
                "income_per_fte_tchf": r.get("income_per_fte_tchf"),
                "personnel_cost_per_fte_tchf": r.get("personnel_cost_per_fte_tchf"),
                "wage_to_productivity_pct": r.get("wage_to_productivity_pct"),
                "productivity_to_wage_ratio": r.get("productivity_to_wage_ratio"),
                "assets_per_fte_mio": r.get("assets_per_fte_mio"),
                "share_price_eoy": r.get("share_price_eoy"),
                "dividend_per_share": r.get("dividend_per_share"),
                "dividend_yield_pct": r.get("dividend_yield_pct"),
                "contribution_public_mio": r.get("contribution_public_mio"),
            })
        for r in panels[b].get("semester", []):
            sem_rows.append({
                **meta_cols,
                "year": r.get("year"),
                "period": r.get("period"),
                "total_assets_mio": r.get("total_assets_mio"),
                "net_interest_income_mio": r.get("net_interest_income_mio"),
                "total_operating_income_mio": r.get("total_operating_income_mio"),
                "net_profit_mio": r.get("net_profit_mio"),
            })
        for r in panels[b].get("offenlegung", []):
            off_rows.append({
                **meta_cols,
                "year": r.get("year"),
                "period": r.get("period"),
                "sort_date": r.get("sort_date"),
                "regime": r.get("regime"),
                "rwa_total_mio": r.get("rwa_total_mio"),
                "cet1_capital_mio": r.get("cet1_capital_mio"),
                "cet1_ratio_pct": r.get("cet1_ratio_pct"),
                "total_capital_ratio_pct": r.get("total_capital_ratio_pct"),
                "leverage_ratio_pct": r.get("leverage_ratio_pct"),
                "lcr_pct": r.get("lcr_pct"),
                "nsfr_pct": r.get("nsfr_pct"),
                "rwa_density_pct": r.get("rwa_density_pct"),
                "cet1_excess_over_target_pp": r.get("cet1_excess_over_target_pp"),
            })
        for r in panels[b].get("verguetung_real", []):
            verg_rows.append({**meta_cols, **r})

    _write_csv(COMP_DATA / "xkb_comparison_annual.csv", annual_rows)
    _write_csv(COMP_DATA / "xkb_comparison_semester.csv", sem_rows)
    _write_csv(COMP_DATA / "xkb_comparison_offenlegung.csv", off_rows)
    _write_csv(COMP_DATA / "xkb_comparison_verguetung_real.csv", verg_rows)

    # Jüngstes gemeinsames Jahr (2025) & Hilfsindex
    by_bank_yr: dict[tuple[str, int], dict] = {(r["bank_id"], r["year"]): r for r in annual_rows}
    latest_yr = {b: max(r["year"] for r in annual_rows if r["bank_id"] == b) for b in VALID_BANKS}
    latest_off = {}
    for b in VALID_BANKS:
        b_offs = [r for r in off_rows if r["bank_id"] == b and r.get("cet1_ratio_pct") is not None]
        if not b_offs:
            b_offs = [r for r in off_rows if r["bank_id"] == b]
        latest_off[b] = b_offs[-1] if b_offs else {}

    # --- 9 Benchmark-Grafiken (300 DPI) ---
    colors = [configs[b].palette["primary"] for b in VALID_BANKS]
    names = [configs[b].short_name for b in VALID_BANKS]

    # Chart 01: Bilanzsumme 2025 & CAGR 2020-2025
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))
    ta_vals = [(by_bank_yr.get((b, 2025), {}).get("total_assets_mio") or 0) / 1000.0 for b in VALID_BANKS]
    ax1.barh(names, ta_vals, color=colors)
    ax1.set_xscale("log")
    ax1.set_xlabel("Bilanzsumme 2025 (Mrd. CHF, Log-Skala)")
    ax1.set_title("Bilanzgrösse 2025 (19 Institute)")
    cagrs = [_cagr(by_bank_yr.get((b, 2020), {}).get("total_assets_mio"), by_bank_yr.get((b, 2025), {}).get("total_assets_mio"), 5) or 0.0 for b in VALID_BANKS]
    ax2.barh(names, cagrs, color=colors)
    ax2.axvline(0, color="black", linewidth=0.8)
    ax2.set_xlabel("CAGR 2020–2025 (% p. a.)")
    ax2.set_title("Bilanzwachstum 2020–2025")
    _save(fig, COMP_CHARTS / "01_bilanzsumme_und_cagr_8_banken.png")

    # Chart 02: Ertragsmix 2025
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    z_sh = [by_bank_yr.get((b, 2025), {}).get("interest_share_pct") or 0 for b in VALID_BANKS]
    k_sh = [by_bank_yr.get((b, 2025), {}).get("commission_share_pct") or 0 for b in VALID_BANKS]
    h_sh = [by_bank_yr.get((b, 2025), {}).get("trading_share_pct") or 0 for b in VALID_BANKS]
    ax.barh(names, z_sh, color="#0F2942", label="Zinserfolg (%)")
    ax.barh(names, k_sh, left=z_sh, color="#0F766E", label="Kommission (%)")
    ax.barh(names, h_sh, left=[z + k for z, k in zip(z_sh, k_sh)], color="#D97706", label="Handel (%)")
    ax.set_xlabel("Anteil am Geschäftsertrag (%)")
    ax.set_title("Ertragsarchitektur 2025 nach Geschäftsmodell")
    ax.legend(loc="lower right")
    _save(fig, COMP_CHARTS / "02_ertragsmix_geschaeftsmodelle_2025.png")

    # Chart 03: CIR vs ROE Quadrant 2025
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    for b in VALID_BANKS:
        r25 = by_bank_yr.get((b, 2025), {})
        cir, roe = r25.get("cir_pct"), r25.get("roe_pct")
        if cir is not None and roe is not None:
            sz = max(60, ((r25.get("total_assets_mio") or 20000) / 1000.0) ** 0.7 * 15)
            ax.scatter(cir, roe, s=sz, color=configs[b].palette["primary"], alpha=0.8, edgecolors="black")
            ax.annotate(configs[b].short_name, (cir, roe), xytext=(5, 4), textcoords="offset points", fontsize=8)
    ax.set_xlabel("Cost-Income-Ratio CIR (%) — tiefer ist effizienter")
    ax.set_ylabel("Eigenkapitalrendite ROE (%)")
    ax.set_title("Effizienz vs. Profitabilität 2025 (Blasengrösse ~ Bilanzsumme)")
    _save(fig, COMP_CHARTS / "03_cir_vs_roe_quadrant_2025.png")

    # Chart 04: Produktivität Ertrag/FTE
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    fte_inc = [by_bank_yr.get((b, 2025), {}).get("income_per_fte_tchf") or 0 for b in VALID_BANKS]
    ax.barh(names, fte_inc, color=colors)
    ax.set_xlabel("Geschäftsertrag je FTE (TCHF)")
    ax.set_title("Personalproduktivität 2025 (Geschäftsertrag pro Vollzeitstelle)")
    _save(fig, COMP_CHARTS / "04_produktivitaet_ertrag_gewinn_je_fte.png")

    # Chart 05: Kapitalpuffer Basel III final 2025/2026
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    cet1_v = [latest_off[b].get("cet1_ratio_pct") or 0 for b in VALID_BANKS]
    cet1_t = [configs[b].capital_targets_pct.get("cet1_target", 9.2) for b in VALID_BANKS]
    ax.barh(names, cet1_v, color=colors, label="CET1-Ist (%)")
    ax.scatter(cet1_t, names, color="black", zorder=5, s=60, label="FINMA-Zielgrösse (%)")
    ax.set_xlabel("CET1-Quote (%)")
    ax.set_title("Kapitalisierung vs. FINMA-Zielgrösse (jüngster Offenlegungsstichtag)")
    ax.legend()
    _save(fig, COMP_CHARTS / "05_kapitalpuffer_basel_iii_final_2026.png")

    # Chart 06: Staatsgarantie & FINMA Kategorien (Eigenkapitalquote vs RWA-Dichte)
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    eq_r = [by_bank_yr.get((b, 2025), {}).get("equity_ratio_pct") or 0 for b in VALID_BANKS]
    ax.barh(names, eq_r, color=["#0F766E" if configs[b].state_guarantee else "#0F2942" for b in VALID_BANKS])
    ax.set_xlabel("Eigenkapitalquote 2025 (%)")
    ax.set_title("Eigenkapitalquote 2025 (Grün = mit Staatsgarantie, Dunkelblau = ohne)")
    _save(fig, COMP_CHARTS / "06_staatsgarantie_und_finma_kategorien.png")

    # Chart 07: Zinswende indiziert (2020 = 100)
    fig, ax = plt.subplots(figsize=(9.5, 5.0))
    for b in VALID_BANKS:
        b20 = by_bank_yr.get((b, 2020), {}).get("net_interest_income_mio")
        if not b20 or b20 <= 0:
            continue
        yrs_b = sorted(y for (bk, y) in by_bank_yr if bk == b and 2015 <= y <= 2025 and by_bank_yr[(bk, y)].get("net_interest_income_mio"))
        vals_b = [by_bank_yr[(b, y)]["net_interest_income_mio"] / b20 * 100.0 for y in yrs_b]
        ax.plot(yrs_b, vals_b, marker="o", linewidth=1.8, label=configs[b].short_name, color=configs[b].palette["primary"])
    ax.axhline(100, color="gray", linestyle="--", linewidth=0.8)
    ax.set_ylabel("Netto-Zinserfolg (Index 2020 = 100)")
    ax.set_title("Zinswende-Dynamik 2015–2025 im Institutsvergleich")
    ax.legend(ncol=2, fontsize=8)
    _save(fig, COMP_CHARTS / "07_zinswende_indiziert_2015_2025.png")

    # Chart 08: Reale Lohnkosten je FTE 2025 (real 2025 CHF)
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    verg_25 = {r["bank_id"]: r for r in verg_rows if r["year"] == 2025}
    lohn_v = [verg_25.get(b, {}).get("avg_per_fte_tchf_real2025") or 0 for b in VALID_BANKS]
    ax.barh(names, lohn_v, color=colors)
    ax.set_xlabel("Personalaufwand je FTE 2025 (TCHF, real 2025)")
    ax.set_title("Reale Lohnkosten je Vollzeitstelle 2025 (19 Institute)")
    _save(fig, COMP_CHARTS / "08_verguetung_real_2025_vergleich.png")

    # Chart 09: Reingewinn real 2025 vs 2020 (Index)
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    np_25 = [by_bank_yr.get((b, 2025), {}).get("net_profit_mio") or 0 for b in VALID_BANKS]
    ax.barh(names, np_25, color=colors)
    ax.set_xscale("log")
    ax.set_xlabel("Reingewinn 2025 (Mio. CHF, Log-Skala)")
    ax.set_title("Reingewinn 2025 im harmonisierten CHF-Vergleich")
    _save(fig, COMP_CHARTS / "09_ausschuettung_und_total_return.png")

    # --- 5 Cross-Bank-Berichte ---
    t1_rows = [
        [
            configs[b].short_name,
            configs[b].peer_group,
            configs[b].reporting_scope,
            configs[b].accounting_standard,
            fmt(by_bank_yr.get((b, 2025), {}).get("total_assets_mio")),
            fmt(_cagr(by_bank_yr.get((b, 2020), {}).get("total_assets_mio"), by_bank_yr.get((b, 2025), {}).get("total_assets_mio"), 5), 2) + " %",
            fmt(by_bank_yr.get((b, 2025), {}).get("interest_share_pct")) + " %",
            fmt(by_bank_yr.get((b, 2025), {}).get("commission_share_pct")) + " %",
        ]
        for b in VALID_BANKS
    ]
    c1 = f"""# 01 · Grösse, Wachstum & Geschäftsmodell (8 Schweizer Banken)

> **Harmonisierung:** Alle Werte in **Mio. CHF** (UBS USD→CHF via `shared/fx_rates.py`). Vergleichbarkeitshinweise zu `consolidated`/`standalone` und `ARB_RVB`/`IFRS` sind pro Zeile ausgewiesen.

## 1. Management Summary
- Die Bilanzsummen 2025 spannen über drei Grössenordnungen: von regionalen Kantonalbanken (VSKB, GEKB, BEKB, BCV) über die inländischen D-SIBs (PostFinance, ZKB, Raiffeisen) bis zum globalen G-SIB **UBS**.
- **Geschäftsmodelle im Kontrast:** Klassische Kantonalbanken & Raiffeisen erzielen **55–75 %** ihres Ertrags im Zinsgeschäft; **UBS** dominiert über Wealth-Management-Kommissionen; **PostFinance** investiert aufgrund des gesetzlichen Kreditverbots in Finanzanlagen statt Hypotheken.

![Bilanzsumme und CAGR](./charts/01_bilanzsumme_und_cagr_8_banken.png)

## 2. Quantitative Gegenüberstellung (Geschäftsjahr 2025)
{_table(["Institut", "Peer Group", "Scope", "Standard", "Bilanzsumme 2025 (Mio.)", "CAGR 20–25", "Zinsanteil", "Komm.-Anteil"], t1_rows)}

![Ertragsmix 2025](./charts/02_ertragsmix_geschaeftsmodelle_2025.png)
"""

    t2_rows = [
        [
            configs[b].short_name,
            fmt(by_bank_yr.get((b, 2025), {}).get("total_operating_income_mio")),
            fmt(by_bank_yr.get((b, 2025), {}).get("net_profit_mio")),
            fmt(by_bank_yr.get((b, 2025), {}).get("cir_pct"), 2) + " %",
            fmt(by_bank_yr.get((b, 2025), {}).get("roe_pct"), 2) + " %",
            fmt(by_bank_yr.get((b, 2025), {}).get("fte_count"), 0),
            fmt(by_bank_yr.get((b, 2025), {}).get("income_per_fte_tchf"), 1),
        ]
        for b in VALID_BANKS
    ]
    c2 = f"""# 02 · Profitabilität, Effizienz & Produktivität (2025)

## 1. Management Summary
- Die Effizienzspanne (Cost-Income-Ratio) trennt schlanke Universal-/Kantonalbanken (**CIR ~45–55 %**) deutlich von integrations- oder gebührenintensiven Plattformmodellen (**PostFinance, UBS**).
- Bei der Produktivität je Vollzeitstelle (**Ertrag/FTE**) zeigen sich klare Skalenvorteile grosser Verbund- und Globalinstitute.

![CIR vs ROE Quadrant](./charts/03_cir_vs_roe_quadrant_2025.png)

## 2. Effizienz- & Produktivitätsmatrix (2025)
{_table(["Institut", "Ertrag 2025 (Mio.)", "Reingewinn 2025 (Mio.)", "CIR %", "ROE %", "FTE", "Ertrag/FTE (TCHF)"], t2_rows)}

![Produktivität je FTE](./charts/04_produktivitaet_ertrag_gewinn_je_fte.png)
"""

    t3_rows = [
        [
            configs[b].short_name,
            f"Kat. {configs[b].finma_category}",
            "Ja" if configs[b].state_guarantee else "Keine",
            latest_off[b].get("period", "–"),
            fmt(latest_off[b].get("cet1_ratio_pct"), 2) + " %",
            fmt(configs[b].capital_targets_pct.get("cet1_target"), 2) + " %",
            fmt(latest_off[b].get("cet1_excess_over_target_pp"), 2) + " Pp.",
            fmt(latest_off[b].get("leverage_ratio_pct"), 2) + " %",
        ]
        for b in VALID_BANKS
    ]
    c3 = f"""# 03 · Kapitalisierung, Regulierung & Staatsgarantie (Basel III final)

## 1. Management Summary
- Sämtliche 19 Institute übertreffen ihre jeweiligen **FINMA-Zielgrössen** (Kategorie 1 G-SIB, Kategorie 2 D-SIB bzw. Kategorie 3) komfortabel.
- Der Übergang zu **Basel III final (ab 01.01.2025)** reduziert bei risikoarmen Hypothekarbanken (Standardansatz) tendenziell die RWA-Dichte, während IRB-Banken (BCV) bzw. G-SIBs (UBS) schärfere Output-Floor-/TBTF-Vorgaben einhalten.

![Kapitalpuffer Basel III final](./charts/05_kapitalpuffer_basel_iii_final_2026.png)

## 2. Aufsichtsrechtliche Kennzahlen (jüngster Stichtag)
{_table(["Institut", "FINMA-Kat.", "Staatsgarantie", "Stichtag", "CET1-Ist", "CET1-Ziel", "Puffer", "Leverage %"], t3_rows)}

![Staatsgarantie und Eigenkapitalquote](./charts/06_staatsgarantie_und_finma_kategorien.png)
"""

    t4_rows = [
        [
            configs[b].short_name,
            configs[b].report_05_mode,
            fmt(by_bank_yr.get((b, 2025), {}).get("net_profit_mio")),
            fmt(verg_25.get(b, {}).get("avg_per_fte_tchf_real2025"), 1),
            fmt(by_bank_yr.get((b, 2025), {}).get("share_price_eoy"), 2),
            fmt(by_bank_yr.get((b, 2025), {}).get("dividend_per_share"), 2),
        ]
        for b in VALID_BANKS
    ]
    c4 = f"""# 04 · Ausschüttung, Eigentümer & reale Vergütung (real 2025 CHF)

## 1. Management Summary
- Die 19 Institute decken vier unterschiedliche Eigentümermodelle ab (`listed_share`, `cantonal_endowment`, `cooperative_payout`, `post_dividend`).
- Alle Lohnkosten und Vergütungsreihen sind über `shared/cpi_bfs.py` (BFS LIK) auf **reale CHF 2025** normiert.

![Reale Vergütung 2025](./charts/08_verguetung_real_2025_vergleich.png)

## 2. Eigentümer- & Lohnkostenvergleich (2025)
{_table(["Institut", "Eigentümer-Modus", "Gewinn 2025 (Mio.)", "Lohn/FTE real (TCHF)", "Kurs 2025", "Dividende 2025"], t4_rows)}

![Reingewinn Vergleich](./charts/09_ausschuettung_und_total_return.png)
"""

    c5 = f"""# 05 · Zinswenden, Saisonalität & Resilienz (2015–2026)

## 1. Management Summary
- Die **SNB-Zinswende 2022–2024** führte bei allen einlagenstarken Inlandbanken zu einem historischen Sprung des Netto-Zinserfolgs, am stärksten ausgeprägt bei **PostFinance** (Ende der Negativzins-Belastung auf SNB-Guthaben).
- Seit den Zinssenkungen 2024/2025 normalisieren sich die Zinsmargen wieder Richtung Langfristmittel.

![Zinswende indiziert](./charts/07_zinswende_indiziert_2015_2025.png)

## 2. Sonder- und Struktureffekte im Zeitverlauf
- **UBS 2023:** Einmaliger Negative Goodwill (~USD 27,7 Mrd.) aus der Credit-Suisse-Übernahme (`extraordinary_flag = CS_NEGATIVE_GOODWILL`).
- **BEKB 2015:** Einmalige Pensionskassen-Sanierungseinlage (83,8 Mio. CHF).
- **ZKB 2024:** Custody-Umklassierung im AuM-Ausweis (-55 Mrd. CHF) & Einführung der OECD-Mindeststeuer.
"""

    # --- Phase V4: 4 neue Branchenvergleichs-Grafiken (Investoren & Mitarbeitende/Vorsorge) ---
    vorsorge_csv = COMP_DATA / "xkb_vorsorgeeinrichtungen.csv"
    vorsorge_rows: list[dict] = []
    if vorsorge_csv.exists():
        with vorsorge_csv.open(encoding="utf-8") as f:
            vorsorge_rows = list(csv.DictReader(f))
    vorsorge_by_b = {r["bank_id"]: r for r in vorsorge_rows}

    # Chart 10: Investoren ROE vs Dividendenrendite / Eigentümer-Rendite 2025
    fig, ax = plt.subplots(figsize=(9, 4.8))
    roes_25 = [by_bank_yr.get((b, 2025), {}).get("roe_pct") or 0 for b in VALID_BANKS]
    divs_25 = [by_bank_yr.get((b, 2025), {}).get("dividend_yield_pct") or 0 for b in VALID_BANKS]
    x_idx = range(len(VALID_BANKS))
    ax.bar([i - 0.18 for i in x_idx], roes_25, width=0.35, color="#0F2942", label="ROE 2025 (%)")
    ax.bar([i + 0.18 for i in x_idx], divs_25, width=0.35, color="#C8102E", label="Dividendenrendite 2025 (%)")
    ax.set_xticks(list(x_idx))
    ax.set_xticklabels(names, rotation=20)
    ax.set_ylabel("%")
    ax.set_title("Investoren-Benchmark 2025: Eigenkapitalrendite (ROE) vs. Dividendenrendite")
    ax.legend()
    _save(fig, COMP_CHARTS / "10_investoren_bewertung_pb_vs_roe_2025.png")

    # Chart 11: Investoren 5J-Gewinnwachstum vs Kursentwicklung
    fig, ax = plt.subplots(figsize=(9, 4.8))
    cagr_np = [_cagr(by_bank_yr.get((b, 2020), {}).get("net_profit_mio"), by_bank_yr.get((b, 2025), {}).get("net_profit_mio"), 5) or 0.0 for b in VALID_BANKS]
    ax.barh(names, cagr_np, color=colors)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Reingewinn-CAGR 2020–2025 (% p. a.)")
    ax.set_title("Investoren-Benchmark: Ertrags- & Gewinnwachstum (2020–2025)")
    _save(fig, COMP_CHARTS / "11_investoren_tsr_und_ausschuettung_2020_2025.png")

    # Chart 12: Mitarbeiter Produktivität vs Lohnkosten/FTE & CEO Pay Ratio 2025
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8))
    inc_fte = [by_bank_yr.get((b, 2025), {}).get("income_per_fte_tchf") or 0 for b in VALID_BANKS]
    ax1.barh(names, lohn_v, color="#0F766E", height=0.4, label="Personalaufwand/FTE real (TCHF)")
    ax1.barh(names, inc_fte, left=lohn_v, color="#94A3B8", alpha=0.45, height=0.4, label="Ertrag/FTE (TCHF)")
    ax1.set_xlabel("TCHF pro Vollzeitstelle (2025)")
    ax1.set_title("Lohnkosten vs. Produktivität je FTE")
    ax1.legend(fontsize=8)
    pay_ratios = []
    for b in VALID_BANKS:
        vr = verg_25.get(b, {})
        ceo_v = vr.get("ceo_total_tchf_real2025")
        avg_v = vr.get("avg_per_fte_tchf_real2025")
        pay_ratios.append(round(ceo_v / avg_v, 1) if (ceo_v and avg_v) else 0.0)
    ax2.barh(names, pay_ratios, color=colors)
    ax2.set_xlabel("CEO-Vergütung / Ø Personalaufwand pro FTE (×)")
    ax2.set_title("Vergütungsspreizung (CEO Pay Ratio 2025)")
    _save(fig, COMP_CHARTS / "12_mitarbeiter_lohn_produktivitaet_pay_ratio_2025.png")

    # Chart 13: Vorsorgeeinrichtungen Aktive/Rentner-Verhältnis & Deckungsgrad / AGBR
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    ratios_pk = [float(vorsorge_by_b[b]["active_to_pensioner_ratio"]) if vorsorge_by_b.get(b, {}).get("active_to_pensioner_ratio") else 0.0 for b in VALID_BANKS]
    ax.barh(names, ratios_pk, color="#0F2942")
    ax.set_xlabel("Verhältnis Aktive Versicherte / Rentner (wo im GB ausgewiesen)")
    ax.set_title("Vorsorgeeinrichtungen: Demografische Struktur (Aktive je Rentner)")
    _save(fig, COMP_CHARTS / "13_vorsorgeeinrichtungen_deckungsgrad_verzinsung.png")

    # Bericht 06: Investoren-Branchenvergleich
    t6_rows = []
    for b in VALID_BANKS:
        r25 = by_bank_yr.get((b, 2025), {})
        t6_rows.append([
            configs[b].short_name,
            "Kotiert (" + (configs[b].ticker or "–") + ")" if configs[b].listed else "Nicht kotiert",
            "Ja" if configs[b].state_guarantee else "Keine",
            fmt(r25.get("roe_pct"), 2) + " %",
            fmt(r25.get("share_price_eoy"), 2),
            fmt(r25.get("dividend_per_share"), 2),
            fmt(r25.get("dividend_yield_pct"), 2) + " %",
            fmt(_cagr(by_bank_yr.get((b, 2020), {}).get("net_profit_mio"), r25.get("net_profit_mio"), 5), 2) + " %",
            fmt(latest_off[b].get("cet1_ratio_pct"), 2) + " %",
        ])
    c6 = f"""# 06 · Investoren-Branchenvergleich (8 Schweizer Banken, 2025)

## 1. Management Summary
- **Segment A (Kotierte Institute — BEKB, VSKB, BCV, GEKB, UBS):** Die BCV erzielt 2025 mit **11,00 % ROE** die höchste Eigenkapitalrendite unter den Kantonalbanken bei einer attraktiven Dividendenrendite (**4,38 %**). BEKB und VSKB bieten stabile Ausschüttungsrenditen bei hoher Kapitalisierung (`CET1 > 16,5 %`), während **UBS** als globaler G-SIB (`ROE 8,60 %`) Wachstum über CS-Synergien und Aktienrückkäufe liefert.
- **Segment B (Öffentliche & Genossenschafts-Eigentümer — ZKB, Raiffeisen, PostFinance):** Die ZKB erwirtschaftet **1'241,0 Mio. CHF** Konzerngewinn (`ROE 7,89 %`) und hohe Ablieferungen an den Kanton Zürich; Raiffeisen stärkt primär das Genossenschaftskapital (`ROE 5,08 %`); PostFinance erzielt unter Kreditverbot `1,82 %` ROE bei extrem hoher CET1-Quote (`24,97 %`).

![Investoren Bewertung & ROE](./charts/10_investoren_bewertung_pb_vs_roe_2025.png)

## 2. Investoren- & Eigentümer-Kennzahlen (2025)
{_table(["Institut", "Kotierung", "Staatsgarantie", "ROE 2025", "Kurs 2025", "Div./Aktie", "Div.-Rendite", "Gewinn-CAGR 20–25", "CET1 %"], t6_rows)}

![Investoren Wachstum & Ausschüttung](./charts/11_investoren_tsr_und_ausschuettung_2020_2025.png)
"""

    # Bericht 07: Mitarbeiter- & Vorsorge-Branchenvergleich
    t7_emp_rows = []
    t7_pk_rows = []
    for b in VALID_BANKS:
        r25 = by_bank_yr.get((b, 2025), {})
        vr25 = verg_25.get(b, {})
        avg_fte = vr25.get("avg_per_fte_tchf_real2025")
        ceo_v = vr25.get("ceo_total_tchf_real2025")
        pr = round(ceo_v / avg_fte, 1) if (ceo_v and avg_fte) else None
        t7_emp_rows.append([
            configs[b].short_name,
            fmt(r25.get("fte_count"), 0),
            fmt(r25.get("income_per_fte_tchf"), 1),
            fmt(avg_fte, 1),
            fmt(r25.get("wage_to_productivity_pct"), 1) + " %",
            fmt(r25.get("productivity_to_wage_ratio"), 2) + "×",
            fmt(ceo_v, 1),
            fmt(pr, 1) + "×" if pr is not None else "–",
        ])
        pk = vorsorge_by_b.get(b, {})
        t7_pk_rows.append([
            configs[b].short_name,
            pk.get("pk_name", "–"),
            pk.get("accounting_basis", "–"),
            fmt(float(pk["active_insured_count"]), 0) if pk.get("active_insured_count") else "n. a.",
            fmt(float(pk["pensioners_count"]), 0) if pk.get("pensioners_count") else "n. a.",
            fmt(float(pk["coverage_ratio_bvg_pct"]), 1) + " %" if pk.get("coverage_ratio_bvg_pct") else "n. a.",
            fmt(float(pk["employer_contribution_reserve_mio"]), 1) if pk.get("employer_contribution_reserve_mio") else "n. a.",
        ])
    c7 = f"""# 07 · Mitarbeiter- & Vorsorge-Branchenvergleich (8 Schweizer Banken, 2025)

## 1. Management Summary
- **Lohnkosten- / Produktivitätsverhältnis (2025):** Das Verhältnis von Personalaufwand zu Geschäftsertrag je FTE reicht von effizienten **~28–39 %** bei den Kantonalbanken und Raiffeisen (entspricht **2,6× bis 3,6×** Ertrag pro CHF Lohnkosten) bis zu **43,9 %** (`2,28×`) bei PostFinance und **56,2 %** (`1,78×`) bei UBS.
- **Vergütungsspreizung (CEO Pay Ratio):** Die Spreizung reicht von **4,6×–8,6×** bei VSKB, BEKB, GEKB und BCV über **11,8×–13,1×** bei Raiffeisen und ZKB bis zu **62,6×** bei UBS.
- **Vorsorgeeinrichtungen:** Alle 7 Inlandbanken bilanzieren nach **Swiss GAAP FER 16**, während **UBS** die Schweizer Pensionspläne nach **IFRS / IAS 19** ausweist (direkter BVG-Deckungsgradvergleich erfordert Art. 44 BVV 2).

![Mitarbeiter Lohn, Produktivität & Pay Ratio](./charts/12_mitarbeiter_lohn_produktivitaet_pay_ratio_2025.png)

## 2. Mitarbeiter-Benchmark (2025, real 2025 CHF)
{_table(["Institut", "FTE 2025", "Ertrag/FTE (TCHF)", "Personalaufw./FTE (TCHF)", "Lohn / Produktivität", "Ertrag / Lohn", "CEO real (TCHF)", "CEO Pay Ratio"], t7_emp_rows)}

## 3. Zugehörige Vorsorgeeinrichtungen (Pensionskassen)
{_table(["Institut", "Vorsorgeeinrichtung", "Standard", "Aktive", "Rentner", "Deckungsgrad BVG", "AGBR (Mio.)"], t7_pk_rows)}

![Vorsorgeeinrichtungen Struktur](./charts/13_vorsorgeeinrichtungen_deckungsgrad_verzinsung.png)
"""

    rep_files = [
        ("01_groesse_wachstum_und_geschaeftsmodell.md", c1, "Grösse, Wachstum & Geschäftsmodell"),
        ("02_profitabilitaet_effizienz_und_produktivitaet.md", c2, "Profitabilität, Effizienz & Produktivität"),
        ("03_kapitalisierung_regulierung_und_staatsgarantie.md", c3, "Kapitalisierung, Regulierung & Staatsgarantie"),
        ("04_ausschuettung_eigentuemer_und_verguetung_real.md", c4, "Ausschüttung, Eigentümer & reale Vergütung"),
        ("05_zinswenden_saisonalitaet_und_resilienz.md", c5, "Zinswenden, Saisonalität & Resilienz"),
        ("06_investoren_branchenvergleich.md", c6, "Investoren-Branchenvergleich"),
        ("07_mitarbeiter_und_vorsorge_branchenvergleich.md", c7, "Mitarbeiter- & Vorsorge-Branchenvergleich"),
    ]
    for fn, body, _ in rep_files:
        (COMP_REPORTS / fn).write_text(body, encoding="utf-8")

    (COMP_REPORTS / "README.md").write_text(
        "# Institutsübergreifende Auswertung (8 Schweizer Banken)\n\n"
        + "\n".join(f"- [{title}](./{fn})" for fn, _, title in rep_files)
        + "\n",
        encoding="utf-8",
    )

    summary_json = {
        "banks": list(VALID_BANKS),
        "annual_rows": len(annual_rows),
        "semester_rows": len(sem_rows),
        "offenlegung_rows": len(off_rows),
        "verguetung_rows": len(verg_rows),
    }
    (COMP_DATA / "xkb_comparison_all.json").write_text(
        json.dumps(summary_json, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[OK] Cross-Bank: {len(VALID_BANKS)} Banken harmonisiert ({len(annual_rows)} Annual-Zeilen), 7 Berichte + 13 Grafiken unter comparison/ erzeugt.")
    return summary_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Schritt 2: Cross-Bank-Panel, 5 Berichte & 9 Grafiken.")
    parser.add_argument("--backend", choices=["local", "gemini", "auto"], default="local")
    args = parser.parse_args()
    run_comparison(backend=args.backend)


if __name__ == "__main__":
    main()
