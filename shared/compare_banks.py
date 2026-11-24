#!/usr/bin/env python3
"""Schritt 2 (Phase 8): Harmonisierungs-Layer & Institutsübergreifende Auswertung (19 Banken)."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from shared.config import BankConfig, REPO_ROOT, VALID_BANKS, load_bank_config
from shared.cpi_bfs import deflate_to_real_2025
from shared.turnover import TURNOVER_DATA, export_turnover_data, get_bank_turnover_meta, get_latest_turnover

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
                "turnover_rate_pct": r.get("turnover_rate_pct"),
                "turnover_net_pct": r.get("turnover_net_pct"),
                "turnover_gross_pct": r.get("turnover_gross_pct"),
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

    # --- 13 Benchmark-Grafiken (300 DPI, absteigend sortiert + Median / Mittelwert) ---
    def _ref_v(ax: plt.Axes, vals: list[float], use_median: bool, unit: str = "", d: int = 1, color: str = "#DC2626", label_prefix: str = "") -> float | None:
        clean = [v for v in vals if v is not None]
        if not clean:
            return None
        stat_val = statistics.median(clean) if use_median else statistics.mean(clean)
        kind = "Median" if use_median else "Mittelwert (Ø)"
        pref = f"{label_prefix} " if label_prefix else ""
        val_txt = f"{stat_val:,.{d}f}".replace(",", "'")
        ax.axvline(stat_val, color=color, linestyle="--", linewidth=1.5, zorder=6, label=f"{pref}{kind}: {val_txt}{unit}")
        return stat_val

    def _ref_h(ax: plt.Axes, vals: list[float], use_median: bool, unit: str = "", d: int = 1, color: str = "#DC2626", label_prefix: str = "") -> float | None:
        clean = [v for v in vals if v is not None]
        if not clean:
            return None
        stat_val = statistics.median(clean) if use_median else statistics.mean(clean)
        kind = "Median" if use_median else "Mittelwert (Ø)"
        pref = f"{label_prefix} " if label_prefix else ""
        val_txt = f"{stat_val:,.{d}f}".replace(",", "'")
        ax.axhline(stat_val, color=color, linestyle="--", linewidth=1.5, zorder=6, label=f"{pref}{kind}: {val_txt}{unit}")
        return stat_val

    # Chart 01: Bilanzsumme 2025 & CAGR 2020-2025 (jeweils absteigend sortiert + Median wegen Rechtsschiefe/Ausreisser)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6.2))
    ta_items = sorted(
        [(configs[b].short_name, (by_bank_yr.get((b, 2025), {}).get("total_assets_mio") or 0) / 1000.0, configs[b].palette["primary"]) for b in VALID_BANKS],
        key=lambda x: x[1],
        reverse=True,
    )
    ax1.barh([x[0] for x in ta_items], [x[1] for x in ta_items], color=[x[2] for x in ta_items])
    ax1.invert_yaxis()
    ax1.set_xscale("log")
    _ref_v(ax1, [x[1] for x in ta_items if x[1] > 0], use_median=True, unit=" Mrd.", d=1)
    ax1.set_xlabel("Bilanzsumme 2025 (Mrd. CHF, Log-Skala)")
    ax1.set_title("Bilanzgrösse 2025 (19 Institute, absteigend)")
    ax1.legend(loc="lower right", fontsize=8)

    cagr_items = sorted(
        [
            (
                configs[b].short_name,
                cval,
                configs[b].palette["primary"],
            )
            for b in VALID_BANKS
            if (cval := _cagr(by_bank_yr.get((b, 2020), {}).get("total_assets_mio"), by_bank_yr.get((b, 2025), {}).get("total_assets_mio"), 5)) is not None
        ],
        key=lambda x: x[1],
        reverse=True,
    )
    ax2.barh([x[0] for x in cagr_items], [x[1] for x in cagr_items], color=[x[2] for x in cagr_items])
    ax2.invert_yaxis()
    ax2.axvline(0, color="black", linewidth=0.8)
    _ref_v(ax2, [x[1] for x in cagr_items], use_median=True, unit=" %", d=2)
    ax2.set_xlabel("CAGR 2020–2025 (% p. a.)")
    ax2.set_title("Bilanzwachstum 2020–2025 (absteigend)")
    ax2.legend(loc="lower right", fontsize=8)
    _save(fig, COMP_CHARTS / "01_bilanzsumme_und_cagr_8_banken.png")

    # Chart 02: Ertragsmix 2025 (absteigend nach Zinsanteil + Median wegen Privatbanken-Schiefe)
    fig, ax = plt.subplots(figsize=(10, 6.2))
    mix_items = sorted(
        [
            (
                configs[b].short_name,
                by_bank_yr.get((b, 2025), {}).get("interest_share_pct") or 0.0,
                by_bank_yr.get((b, 2025), {}).get("commission_share_pct") or 0.0,
                by_bank_yr.get((b, 2025), {}).get("trading_share_pct") or 0.0,
            )
            for b in VALID_BANKS
        ],
        key=lambda x: x[1],
        reverse=True,
    )
    m_names = [x[0] for x in mix_items]
    z_sh = [x[1] for x in mix_items]
    k_sh = [x[2] for x in mix_items]
    h_sh = [x[3] for x in mix_items]
    ax.barh(m_names, z_sh, color="#0F2942", label="Zinserfolg (%)")
    ax.barh(m_names, k_sh, left=z_sh, color="#0F766E", label="Kommission (%)")
    ax.barh(m_names, h_sh, left=[z + k for z, k in zip(z_sh, k_sh)], color="#D97706", label="Handel (%)")
    ax.invert_yaxis()
    _ref_v(ax, z_sh, use_median=True, unit=" %", d=1, label_prefix="Zinsanteil")
    ax.set_xlabel("Anteil am Geschäftsertrag (%)")
    ax.set_title("Ertragsarchitektur 2025 nach Geschäftsmodell (absteigend nach Zinsanteil)")
    ax.legend(loc="lower right", fontsize=8)
    _save(fig, COMP_CHARTS / "02_ertragsmix_geschaeftsmodelle_2025.png")

    # Chart 03: CIR vs ROE Quadrant 2025 (Median-Fadenkreuz wegen Ausreisser-Schiefe)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    cirs_all, roes_all = [], []
    for b in VALID_BANKS:
        r25 = by_bank_yr.get((b, 2025), {})
        cir, roe = r25.get("cir_pct"), r25.get("roe_pct")
        if cir is not None and roe is not None:
            cirs_all.append(cir)
            roes_all.append(roe)
            sz = max(60, ((r25.get("total_assets_mio") or 20000) / 1000.0) ** 0.7 * 15)
            ax.scatter(cir, roe, s=sz, color=configs[b].palette["primary"], alpha=0.8, edgecolors="black")
            ax.annotate(configs[b].short_name, (cir, roe), xytext=(5, 4), textcoords="offset points", fontsize=8)
    _ref_v(ax, cirs_all, use_median=True, unit=" %", d=1, color="#0F2942", label_prefix="CIR")
    _ref_h(ax, roes_all, use_median=True, unit=" %", d=2, color="#DC2626", label_prefix="ROE")
    ax.set_xlabel("Cost-Income-Ratio CIR (%) — tiefer ist effizienter")
    ax.set_ylabel("Eigenkapitalrendite ROE (%)")
    ax.set_title("Effizienz vs. Profitabilität 2025 (Blasengrösse ~ Bilanzsumme)")
    ax.legend(loc="upper right", fontsize=8)
    _save(fig, COMP_CHARTS / "03_cir_vs_roe_quadrant_2025.png")

    # Chart 04: Produktivität Ertrag/FTE (absteigend + Mittelwert da symmetrisch verteilt)
    fig, ax = plt.subplots(figsize=(10, 6.2))
    fte_items = sorted(
        [(configs[b].short_name, by_bank_yr.get((b, 2025), {}).get("income_per_fte_tchf") or 0.0, configs[b].palette["primary"]) for b in VALID_BANKS],
        key=lambda x: x[1],
        reverse=True,
    )
    ax.barh([x[0] for x in fte_items], [x[1] for x in fte_items], color=[x[2] for x in fte_items])
    ax.invert_yaxis()
    _ref_v(ax, [x[1] for x in fte_items if x[1] > 0], use_median=False, unit=" TCHF", d=1)
    ax.set_xlabel("Geschäftsertrag je FTE (TCHF)")
    ax.set_title("Personalproduktivität 2025 (Geschäftsertrag pro Vollzeitstelle, absteigend)")
    ax.legend(loc="lower right", fontsize=8)
    _save(fig, COMP_CHARTS / "04_produktivitaet_ertrag_gewinn_je_fte.png")

    # Chart 05: Kapitalpuffer Basel III final 2025/2026 (nur Institute mit ausgewiesener CET1-Quote, absteigend + Mittelwert)
    fig, ax = plt.subplots(figsize=(10, 5.6))
    cet1_items = sorted(
        [
            (
                configs[b].short_name,
                float(latest_off[b]["cet1_ratio_pct"]),
                configs[b].capital_targets_pct.get("cet1_target", 9.2),
                configs[b].palette["primary"],
            )
            for b in VALID_BANKS
            if latest_off.get(b, {}).get("cet1_ratio_pct") is not None
        ],
        key=lambda x: x[1],
        reverse=True,
    )
    c_names = [x[0] for x in cet1_items]
    c_vals = [x[1] for x in cet1_items]
    ax.barh(c_names, c_vals, color=[x[3] for x in cet1_items], label="CET1-Ist (%)")
    ax.scatter([x[2] for x in cet1_items], c_names, color="black", zorder=5, s=60, label="FINMA-Zielgrösse (%)")
    ax.invert_yaxis()
    _ref_v(ax, c_vals, use_median=False, unit=" %", d=2)
    ax.set_xlabel("CET1-Quote (%)")
    ax.set_title("Kapitalisierung vs. FINMA-Zielgrösse (jüngster Offenlegungsstichtag, absteigend)")
    ax.legend(loc="lower right", fontsize=8)
    _save(fig, COMP_CHARTS / "05_kapitalpuffer_basel_iii_final_2026.png")

    # Chart 06: Staatsgarantie & Eigenkapitalquote 2025 (absteigend + Mittelwert da symmetrisch verteilt)
    fig, ax = plt.subplots(figsize=(10, 6.2))
    eq_items = sorted(
        [
            (
                configs[b].short_name,
                by_bank_yr.get((b, 2025), {}).get("equity_ratio_pct") or 0.0,
                "#0F766E" if configs[b].state_guarantee else "#0F2942",
            )
            for b in VALID_BANKS
        ],
        key=lambda x: x[1],
        reverse=True,
    )
    ax.barh([x[0] for x in eq_items], [x[1] for x in eq_items], color=[x[2] for x in eq_items])
    ax.invert_yaxis()
    _ref_v(ax, [x[1] for x in eq_items if x[1] > 0], use_median=False, unit=" %", d=2)
    ax.set_xlabel("Eigenkapitalquote 2025 (%)")
    ax.set_title("Eigenkapitalquote 2025 (absteigend; Grün = mit Staatsgarantie, Dunkelblau = ohne)")
    ax.legend(loc="lower right", fontsize=8)
    _save(fig, COMP_CHARTS / "06_staatsgarantie_und_finma_kategorien.png")

    # Chart 07: Zinswende indiziert (2020 = 100; Legende absteigend nach 2025 + Median-Verlauf über alle Banken)
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    series_07 = []
    by_yr_idx: dict[int, list[float]] = {}
    for b in VALID_BANKS:
        b20 = by_bank_yr.get((b, 2020), {}).get("net_interest_income_mio")
        if not b20 or b20 <= 0:
            continue
        yrs_b = sorted(y for (bk, y) in by_bank_yr if bk == b and 2015 <= y <= 2025 and by_bank_yr[(bk, y)].get("net_interest_income_mio"))
        vals_b = [by_bank_yr[(b, y)]["net_interest_income_mio"] / b20 * 100.0 for y in yrs_b]
        if not yrs_b:
            continue
        for y, val in zip(yrs_b, vals_b):
            by_yr_idx.setdefault(y, []).append(val)
        val_25 = vals_b[-1] if yrs_b[-1] == 2025 else 0.0
        series_07.append((val_25, configs[b].short_name, yrs_b, vals_b, configs[b].palette["primary"]))
    series_07.sort(key=lambda x: x[0], reverse=True)
    for _, sname, yrs_b, vals_b, scol in series_07:
        ax.plot(yrs_b, vals_b, marker="o", markersize=3.5, linewidth=1.4, alpha=0.8, label=sname, color=scol)
    med_yrs = sorted(by_yr_idx.keys())
    med_vals = [statistics.median(by_yr_idx[y]) for y in med_yrs]
    ax.plot(med_yrs, med_vals, color="black", linestyle="--", linewidth=2.4, zorder=10, label=f"Median (Alle, 2025: {med_vals[-1]:.1f})")
    ax.axhline(100, color="gray", linestyle=":", linewidth=0.8)
    ax.set_ylabel("Netto-Zinserfolg (Index 2020 = 100)")
    ax.set_title("Zinswende-Dynamik 2015–2025 im Institutsvergleich (Legende absteigend nach 2025)")
    ax.legend(ncol=3, fontsize=7.5, loc="upper left")
    _save(fig, COMP_CHARTS / "07_zinswende_indiziert_2015_2025.png")

    # Chart 08: Reale Lohnkosten je FTE 2025 (absteigend + Mittelwert da symmetrisch verteilt)
    fig, ax = plt.subplots(figsize=(10, 6.2))
    verg_25 = {r["bank_id"]: r for r in verg_rows if r["year"] == 2025}
    lohn_items = sorted(
        [(configs[b].short_name, verg_25.get(b, {}).get("avg_per_fte_tchf_real2025") or 0.0, configs[b].palette["primary"]) for b in VALID_BANKS],
        key=lambda x: x[1],
        reverse=True,
    )
    ax.barh([x[0] for x in lohn_items], [x[1] for x in lohn_items], color=[x[2] for x in lohn_items])
    ax.invert_yaxis()
    _ref_v(ax, [x[1] for x in lohn_items if x[1] > 0], use_median=False, unit=" TCHF", d=1)
    ax.set_xlabel("Personalaufwand je FTE 2025 (TCHF, real 2025)")
    ax.set_title("Reale Lohnkosten je Vollzeitstelle 2025 (19 Institute, absteigend)")
    ax.legend(loc="lower right", fontsize=8)
    _save(fig, COMP_CHARTS / "08_verguetung_real_2025_vergleich.png")

    # Chart 09: Reingewinn 2025 (absteigend + Median wegen extremer Rechtsschiefe)
    fig, ax = plt.subplots(figsize=(10, 6.2))
    np_items = sorted(
        [(configs[b].short_name, by_bank_yr.get((b, 2025), {}).get("net_profit_mio") or 0.0, configs[b].palette["primary"]) for b in VALID_BANKS],
        key=lambda x: x[1],
        reverse=True,
    )
    ax.barh([x[0] for x in np_items], [x[1] for x in np_items], color=[x[2] for x in np_items])
    ax.invert_yaxis()
    ax.set_xscale("log")
    _ref_v(ax, [x[1] for x in np_items if x[1] > 0], use_median=True, unit=" Mio.", d=1)
    ax.set_xlabel("Reingewinn 2025 (Mio. CHF, Log-Skala)")
    ax.set_title("Reingewinn 2025 im harmonisierten CHF-Vergleich (absteigend)")
    ax.legend(loc="lower right", fontsize=8)
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
    c1 = f"""# 01 · Grösse, Wachstum & Geschäftsmodell ({len(VALID_BANKS)} Schweizer Banken)

> **Harmonisierung:** Alle Werte in **Mio. CHF** (UBS USD→CHF via `shared/fx_rates.py`). Vergleichbarkeitshinweise zu `consolidated`/`standalone` und `ARB_RVB`/`IFRS` sind pro Zeile ausgewiesen.

## 1. Management Summary
- Die Bilanzsummen 2025 spannen über vier Grössenordnungen: von regionalen Sparkassen und Kantonalbanken über die inländischen D-SIBs (**PostFinance, ZKB, Raiffeisen**) bis zum globalen G-SIB **UBS**.
- **Geschäftsmodelle im Kontrast:** Klassische Kantonalbanken, Regionalbanken & Raiffeisen erzielen **55–93 %** ihres Ertrags im Zinsgeschäft; **UBS, Pictet & Vontobel** dominieren über Wealth-Management-Kommissionen; **PostFinance** investiert aufgrund des gesetzlichen Kreditverbots in Finanzanlagen statt Hypotheken.

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
- Die Effizienzspanne (Cost-Income-Ratio) trennt schlanke Regional- und Kantonalbanken (**CIR ~38–55 %**) deutlich von integrations- oder gebührenintensiven Plattform- und Wealth-Modellen (**PostFinance, UBS, Vontobel, Pictet**).
- Bei der Produktivität je Vollzeitstelle (**Ertrag/FTE**) liegen spezialisierte Verbund-, Gross- und Kantonalbanken über dem Branchenmittelwert.

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
- Sämtliche 19 Institute übertreffen ihre jeweiligen **FINMA-Zielgrössen** (Kategorie 1 G-SIB, Kategorie 2 D-SIB bzw. Kategorie 3/4/5) komfortabel.
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

    # Chart 10: Investoren ROE vs Dividendenrendite 2025 (absteigend nach ROE + Median ROE & Mittelwert Div.-Rendite)
    fig, ax = plt.subplots(figsize=(11, 5.2))
    roe_div_items = sorted(
        [
            (
                configs[b].short_name,
                by_bank_yr.get((b, 2025), {}).get("roe_pct") or 0.0,
                by_bank_yr.get((b, 2025), {}).get("dividend_yield_pct") or 0.0,
            )
            for b in VALID_BANKS
        ],
        key=lambda x: x[1],
        reverse=True,
    )
    x_idx = range(len(roe_div_items))
    roes_25 = [x[1] for x in roe_div_items]
    divs_25 = [x[2] for x in roe_div_items]
    ax.bar([i - 0.18 for i in x_idx], roes_25, width=0.35, color="#0F2942", label="ROE 2025 (%)")
    ax.bar([i + 0.18 for i in x_idx], divs_25, width=0.35, color="#C8102E", label="Dividendenrendite 2025 (%)")
    _ref_h(ax, [v for v in roes_25 if v > 0], use_median=True, unit=" %", d=2, color="#0F2942", label_prefix="ROE")
    _ref_h(ax, [v for v in divs_25 if v > 0], use_median=False, unit=" %", d=2, color="#DC2626", label_prefix="Div.-Rendite")
    ax.set_xticks(list(x_idx))
    ax.set_xticklabels([x[0] for x in roe_div_items], rotation=28, ha="right")
    ax.set_ylabel("%")
    ax.set_title("Investoren-Benchmark 2025: Eigenkapitalrendite (ROE) vs. Dividendenrendite (absteigend nach ROE)")
    ax.legend(fontsize=8)
    _save(fig, COMP_CHARTS / "10_investoren_bewertung_pb_vs_roe_2025.png")

    # Chart 11: Investoren 5J-Gewinnwachstum 2020-2025 (absteigend + Median wegen Ausreisser-Schiefe)
    fig, ax = plt.subplots(figsize=(10, 6.0))
    np_cagr_items = sorted(
        [
            (
                configs[b].short_name,
                cval,
                configs[b].palette["primary"],
            )
            for b in VALID_BANKS
            if (cval := _cagr(by_bank_yr.get((b, 2020), {}).get("net_profit_mio"), by_bank_yr.get((b, 2025), {}).get("net_profit_mio"), 5)) is not None
        ],
        key=lambda x: x[1],
        reverse=True,
    )
    ax.barh([x[0] for x in np_cagr_items], [x[1] for x in np_cagr_items], color=[x[2] for x in np_cagr_items])
    ax.invert_yaxis()
    ax.axvline(0, color="black", linewidth=0.8)
    _ref_v(ax, [x[1] for x in np_cagr_items], use_median=True, unit=" %", d=2)
    ax.set_xlabel("Reingewinn-CAGR 2020–2025 (% p. a.)")
    ax.set_title("Investoren-Benchmark: Ertrags- & Gewinnwachstum 2020–2025 (absteigend)")
    ax.legend(loc="lower right", fontsize=8)
    _save(fig, COMP_CHARTS / "11_investoren_tsr_und_ausschuettung_2020_2025.png")

    # Chart 12: Mitarbeiter Produktivität vs Lohnkosten/FTE (absteigend nach Ertrag/FTE + Mittelwerte) & CEO Pay Ratio (absteigend + Median)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6.2))
    emp_items = sorted(
        [
            (
                configs[b].short_name,
                by_bank_yr.get((b, 2025), {}).get("income_per_fte_tchf") or 0.0,
                verg_25.get(b, {}).get("avg_per_fte_tchf_real2025") or 0.0,
            )
            for b in VALID_BANKS
        ],
        key=lambda x: x[1],
        reverse=True,
    )
    e_names = [x[0] for x in emp_items]
    e_inc = [x[1] for x in emp_items]
    e_lohn = [x[2] for x in emp_items]
    ax1.barh(e_names, e_inc, color="#94A3B8", alpha=0.65, height=0.55, label="Ertrag/FTE (TCHF)")
    ax1.barh(e_names, e_lohn, color="#0F766E", height=0.55, label="Personalaufwand/FTE real (TCHF)")
    ax1.invert_yaxis()
    _ref_v(ax1, [v for v in e_inc if v > 0], use_median=False, unit=" TCHF", d=1, color="#0F2942", label_prefix="Ertrag/FTE")
    _ref_v(ax1, [v for v in e_lohn if v > 0], use_median=False, unit=" TCHF", d=1, color="#DC2626", label_prefix="Lohn/FTE")
    ax1.set_xlabel("TCHF pro Vollzeitstelle (2025)")
    ax1.set_title("Lohnkosten vs. Produktivität je FTE (absteigend)")
    ax1.legend(loc="lower right", fontsize=7.5)

    pr_items = []
    for b in VALID_BANKS:
        vr = verg_25.get(b, {})
        ceo_v = vr.get("ceo_total_tchf_real2025")
        avg_v = vr.get("avg_per_fte_tchf_real2025")
        if ceo_v and avg_v:
            pr_items.append((configs[b].short_name, round(ceo_v / avg_v, 1), configs[b].palette["primary"]))
    pr_items.sort(key=lambda x: x[1], reverse=True)
    ax2.barh([x[0] for x in pr_items], [x[1] for x in pr_items], color=[x[2] for x in pr_items])
    ax2.invert_yaxis()
    _ref_v(ax2, [x[1] for x in pr_items], use_median=True, unit="×", d=1)
    ax2.set_xlabel("CEO-Vergütung / Ø Personalaufwand pro FTE (×)")
    ax2.set_title("Vergütungsspreizung (CEO Pay Ratio 2025, absteigend)")
    ax2.legend(loc="lower right", fontsize=8)
    _save(fig, COMP_CHARTS / "12_mitarbeiter_lohn_produktivitaet_pay_ratio_2025.png")

    # Chart 13: Vorsorgeeinrichtungen BVG-Deckungsgrad (absteigend + Mittelwert) & Arbeitgeberbeiträge (absteigend + Median)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.8))
    cov_items = sorted(
        [
            (configs[b].short_name, float(vorsorge_by_b[b]["coverage_ratio_bvg_pct"]), configs[b].palette["primary"])
            for b in VALID_BANKS
            if vorsorge_by_b.get(b, {}).get("coverage_ratio_bvg_pct")
        ],
        key=lambda x: x[1],
        reverse=True,
    )
    ax1.barh([x[0] for x in cov_items], [x[1] for x in cov_items], color=[x[2] for x in cov_items])
    ax1.invert_yaxis()
    ax1.axvline(100.0, color="black", linestyle=":", linewidth=1.2, label="BVG-Minimum: 100.0 %")
    _ref_v(ax1, [x[1] for x in cov_items], use_median=False, unit=" %", d=1)
    ax1.set_xlim(90, max([x[1] for x in cov_items] + [135]) + 4)
    ax1.set_xlabel("BVG-Deckungsgrad (%)")
    ax1.set_title("Pensionskassen: BVG-Deckungsgrad 2025 (absteigend)")
    ax1.legend(loc="lower right", fontsize=8)

    emp_c_items = sorted(
        [
            (configs[b].short_name, float(vorsorge_by_b[b]["employer_contribution_mio"]), configs[b].palette["primary"])
            for b in VALID_BANKS
            if vorsorge_by_b.get(b, {}).get("employer_contribution_mio")
        ],
        key=lambda x: x[1],
        reverse=True,
    )
    ax2.barh([x[0] for x in emp_c_items], [x[1] for x in emp_c_items], color=[x[2] for x in emp_c_items])
    ax2.invert_yaxis()
    _ref_v(ax2, [x[1] for x in emp_c_items], use_median=True, unit=" Mio.", d=1)
    ax2.set_xlabel("Arbeitgeberbeiträge / Vorsorgeaufwand 2025 (Mio. CHF)")
    ax2.set_title("Pensionskassen: Arbeitgeberbeiträge 2025 (absteigend)")
    ax2.legend(loc="lower right", fontsize=8)
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
    c6 = f"""# 06 · Investoren-Branchenvergleich ({len(VALID_BANKS)} Schweizer Banken, 2025)

## 1. Management Summary
- **Segment A (Kotierte & Zertifikats-Institute):** Die **BCV** erzielt 2025 mit **11,00 % ROE** die höchste Eigenkapitalrendite unter den Kantonalbanken bei attraktiver Dividendenrendite (**4,38 %**); **Vontobel (10,57 %)**, **GEKB (8,84 %)**, **UBS (8,60 %)**, **SGKB (7,28 %, Rendite 4,60 %)** und **LUKB (6,99 %)** folgen mit soliden Ausschüttungen.
- **Segment B (Öffentliche & Genossenschafts-Eigentümer):** **ZKB (1'241,0 Mio. CHF)** und **Raiffeisen (1'208,0 Mio. CHF)** erzielen die höchsten Inlandgewinne; **PostFinance** erzielt unter Kreditverbot `1,82 %` ROE bei höchster CET1-Quote (`24,97 %`).

![Investoren Bewertung & ROE](./charts/10_investoren_bewertung_pb_vs_roe_2025.png)

## 2. Investoren- & Eigentümer-Kennzahlen (2025)
{_table(["Institut", "Kotierung", "Staatsgarantie", "ROE 2025", "Kurs 2025", "Div./Aktie", "Div.-Rendite", "Gewinn-CAGR 20–25", "CET1 %"], t6_rows)}

![Investoren Wachstum & Ausschüttung](./charts/11_investoren_tsr_und_ausschuettung_2020_2025.png)
"""

    # Bericht 07: Mitarbeiter- & Vorsorge-Branchenvergleich
    export_turnover_data()
    t7_emp_rows = []
    t7_pk_rows = []
    t7_turn_rows = []
    turn_years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

    for b in VALID_BANKS:
        r25 = by_bank_yr.get((b, 2025), {})
        vr25 = verg_25.get(b, {})
        avg_fte = vr25.get("avg_per_fte_tchf_real2025")
        ceo_v = vr25.get("ceo_total_tchf_real2025")
        pr = round(ceo_v / avg_fte, 1) if (ceo_v and avg_fte) else None
        lat_y, lat_e = get_latest_turnover(b, 2025)
        turn_25_str = (
            f"{fmt(lat_e['rate'], 1)} %" if (lat_y == 2025 and lat_e) else (f"{fmt(lat_e['rate'], 1)} % ({lat_y})" if (lat_y and lat_e) else "n. a.")
        )
        t7_emp_rows.append([
            configs[b].short_name,
            fmt(r25.get("fte_count"), 0),
            turn_25_str,
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
            fmt(float(pk["employer_contribution_mio"]), 2) if pk.get("employer_contribution_mio") else "n. a.",
        ])
        t_meta = get_bank_turnover_meta(b)
        yrs_map = t_meta.get("years", {})
        if yrs_map:
            earlier_yrs = [y for y in sorted(yrs_map.keys()) if y < 2016]
            earlier_str = (
                ", ".join(f"{y}: {fmt(yrs_map[y]['rate'], 1)} %" for y in earlier_yrs)
                if earlier_yrs
                else "–"
            )
            t7_turn_rows.append(
                [configs[b].short_name]
                + [
                    (fmt(yrs_map[y]["rate"], 1) + " %") if y in yrs_map and yrs_map[y].get("rate") is not None else "–"
                    for y in turn_years
                ]
                + [earlier_str, t_meta.get("basis", "–")]
            )

    total_t_vals = sum(len(get_bank_turnover_meta(b).get("years", {})) for b in VALID_BANKS)
    c7 = f"""# 07 · Mitarbeiter- & Vorsorge-Branchenvergleich ({len(VALID_BANKS)} Schweizer Banken, 2025)

## 1. Management Summary
- **Lohnkosten- / Produktivitätsverhältnis (2025):** Bei den **{len(VALID_BANKS)} Instituten** liegt der durchschnittliche Geschäftsertrag je FTE bei **525,3 TCHF** (bei realen Lohnkosten je FTE von **Ø 177,8 TCHF**).
- **Personalfluktuation (Employee Turnover):** **{len(TURNOVER_DATA)} von {len(VALID_BANKS)} Instituten** legen in ihren Geschäfts- bzw. separaten Nachhaltigkeitsberichten (GRI 401-1) quantitative Fluktuationsquoten offen (**{total_t_vals} Instituts-Jahreswerte** von 2003 bis 2025). Alle 15 berichtenden Institute verfügen über einen aktuellen Wert für **2025**: Die Bandbreite reicht von **4,3 % Netto / 7,8 % Brutto (LUKB)**, **4,6 % Netto (FKB)** und **5,0 % (ZKB)** über **6,9 % (BCV)**, **7,0 % (BEKB; aity AG: 2,0 %)**, **7,1 % Voluntary / 12,6 % Overall (UBS)**, **7,4 % Netto / 9,7 % Gesamt (Raiffeisen)**, **7,7 % (SGKB)**, **7,8 % Netto / 11,9 % Brutto (BLKB)**, **7,99 % (WKB/BCVS)**, **8,2 % (Pictet)**, **9,4 % (Valiant)** und **9,73 % (GEKB/BCGE)** bis **10,8 % (Vontobel)** und **11,1 % (Migros Bank)**.
- **Vorsorgeeinrichtungen:** Alle Schweizer Banken mit Swiss-GAAP-FER-Ausweis weisen solide **BVG-Deckungsgrade** auf (Ø **120,3 %** über 14 berichtende Kassen, von **110,0 %** bis **133,3 %** bei BEKB).

![Mitarbeiter Lohn, Produktivität & Pay Ratio](./charts/12_mitarbeiter_lohn_produktivitaet_pay_ratio_2025.png)

## 2. Mitarbeiter-Benchmark (2025, real 2025 CHF)
{_table(["Institut", "FTE 2025", "Fluktuation (jüngst)", "Ertrag/FTE (TCHF)", "Personalaufw./FTE (TCHF)", "Lohn / Produktivität", "Ertrag / Lohn", "CEO real (TCHF)", "CEO Pay Ratio"], t7_emp_rows)}

## 3. Bekannte Personalfluktuationen pro Jahr (offengelegte Zeitreihen, in %)
> **Methodik-Hinweis:** Vollständiger Datensatz in `comparison/data/xkb_personalfluktuation.csv` sowie in den jeweiligen Instituts-Panels (`turnover_rate_pct`, `turnover_net_pct`, `turnover_gross_pct`). Mehrere Institute haben den Ausweis der Personalfluktuation (GRI 401-1) in separate **Nachhaltigkeits- bzw. CSR/RSE-Berichte** ausgelagert: **BEKB** (NHB 2015–2025 für 2011–2025), **BLKB** (GNB/NHB 2010–2025; ab 2023 sowohl Netto- als auch Bruttofluktuation für den Gesamtkonzern), **FKB** (NHB 2023–2025 für 2019–2025; Fluktuationsrate netto, Zielwert `< 5 %`), **GEKB/BCGE** (*Rapport RSE* 2023–2025 für *BCGE Maison-mère* und *BCGE France*), **LUKB** (NHB 2024–2025 mit Netto- und Bruttofluktuation), **Migros Bank** (NHB 2024–2025; natürliche Austritte exkl. Pensionierungen/Tod), **Pictet** (*Group Sustainability Report* 2023–2025), **UBS** (*Sustainability Report Supplement* 2024–2025: *Voluntary turnover* in `rate`/`net`, *Overall turnover* inkl. Restrukturierung/CS-Integration in `gross`), **Valiant** (NHB 2023–2025) und **WKB/BCVS** (*Rapport RSE / CSR Report* 2023–2025; für 2021–2024 sind sowohl die Netto-Fluktuationsrate aus dem GB als auch die GRI-401-1-Gesamtrotationsrate inkl. Lernenden dokumentiert). Lediglich **5 von 20 Instituten** (PostFinance sowie die vier nicht GRI-berichtspflichtigen Regional-/Infrastrukturbanken AEK Thun, Bank SLM, EK Speicher, Entris) weisen keine institutsspezifische Fluktuationsquote aus (`n. a.`).

{_table(["Institut"] + [str(y) for y in turn_years] + ["Frühere Jahrgänge (2003–2015)", "Definition / Methodik"], t7_turn_rows)}

## 4. Zugehörige Vorsorgeeinrichtungen (Pensionskassen)
{_table(["Institut", "Vorsorgeeinrichtung", "Standard", "Aktive", "Rentner", "Deckungsgrad BVG", "AG-Beiträge (Mio.)"], t7_pk_rows)}

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
        f"# Institutsübergreifende Auswertung ({len(VALID_BANKS)} Schweizer Banken)\n\n"
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
