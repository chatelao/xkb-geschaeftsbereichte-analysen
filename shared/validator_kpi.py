#!/usr/bin/env python3
"""Stufe 3 der Hydrogen-Analysestrategie: Normierung, FX, t+1-Selbstheilung, Split-Bereinigung & KPI-Engine."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from shared.config import BankConfig, load_bank_config
from shared.cpi_bfs import cpi_factor_2025, deflate_to_real_2025, get_cpi_index
from shared.fx_rates import convert_to_chf, get_fx_rate
from shared.turnover import get_turnover_for_year

STOCK_METRICS = {
    "total_assets",
    "mortgage_loans",
    "customer_loans_other",
    "financial_investments",
    "customer_deposits",
    "kassenobligationen",
    "pfandbriefe_bonds",
    "reserves_banking_risks",
    "shareholders_equity",
    "assets_under_management",
    "cet1_capital",
    "tier1_capital",
    "total_capital",
    "rwa_total",
}

FLOW_METRICS = {
    "net_interest_income",
    "commission_income",
    "trading_income",
    "other_ordinary_income",
    "total_operating_income",
    "personnel_expenses",
    "general_expenses",
    "total_operating_expenses",
    "operating_profit",
    "reserves_change",
    "taxes",
    "net_profit",
    "net_new_money",
    "free_cash_flow",
    "vr_total_comp",
    "gl_total_comp",
    "ceo_total_comp",
}

MIO_INPUT_METRICS = {
    "assets_under_management",
    "net_new_money",
    "free_cash_flow",
    "taxes_public_mio",
    "dividend_canton_mio",
    "canton_guarantee_fee_mio",
    "public_contribution_total_mio",
}

PCT_OR_UNITLESS_METRICS = {
    "cet1_ratio_pct",
    "tier1_ratio_pct",
    "total_capital_ratio_pct",
    "tlac_ratio_pct",
    "leverage_ratio_pct",
    "lcr_pct",
    "nsfr_pct",
    "fte_count",
    "headcount",
    "branch_count",
    "share_price_eoy",
    "dividend_per_share",
    "payout_ratio_pct",
    "coop_members_count",
    "turnover_rate_pct",
    "turnover_net_pct",
    "turnover_gross_pct",
}


def safe_div(num: float | None, den: float | None, scale: float = 1.0) -> float | None:
    if num is None or den is None or den == 0:
        return None
    return (num / den) * scale


def r_round(val: float | None, digits: int = 3) -> float | None:
    return None if val is None else round(val, digits)


def normalize_to_mio(metric: str, val: float | None, unit: str | None, default_curr: str) -> float | None:
    """Normiert TCHF/Mio./Mrd. auf Mio. (in Originalwährung)."""
    if val is None:
        return None
    if metric in PCT_OR_UNITLESS_METRICS:
        return val
    u = (unit or "").lower()
    if "mrd" in u or "billion" in u:
        return val * 1000.0
    if "mio" in u or "million" in u:
        return val
    if u.startswith("t") or "1 000" in u or "millier" in u or "thousand" in u:
        return val / 1000.0
    # Fallback wenn unit fehlt:
    if metric in MIO_INPUT_METRICS:
        return val
    return val / 1000.0


def apply_share_splits(year: int, share_price: float | None, dividend: float | None, splits: list[dict]) -> tuple[float | None, float | None, float]:
    """Teilt historische Kurse/Dividenden vor Split-Datum deterministisch durch den kumulierten Split-Faktor."""
    factor = 1.0
    for sp in splits:
        sp_year = int(str(sp["date"])[:4])
        if year < sp_year:
            factor *= float(sp["ratio"])
    sp_adj = r_round(share_price / factor, 2) if share_price is not None else None
    div_adj = r_round(dividend / factor, 2) if dividend is not None else None
    return sp_adj, div_adj, factor


def self_heal_series(rows: list[dict], metrics_to_heal: list[str]) -> list[str]:
    """Füllt Lücken im Jahr t deterministisch aus value_prior_year von t+1 und protokolliert Abweichungen > 0.5%."""
    audit_logs: list[str] = []
    by_year = {r["year"]: r for r in rows}
    for yr in sorted(by_year.keys()):
        if (yr + 1) not in by_year:
            continue
        curr_r = by_year[yr]
        next_r = by_year[yr + 1]
        healed = set(curr_r.get("_healed", []))
        for m in metrics_to_heal:
            val_t = curr_r.get(m)
            val_prev_next = next_r.get(f"{m}__prior")
            if val_prev_next is None:
                continue
            if val_t is None:
                curr_r[m] = val_prev_next
                healed.add(m)
                audit_logs.append(f"{yr} `{m}`: Lücke durch Vorjahreswert aus {yr+1} geschlossen ({val_prev_next}).")
            elif abs(val_t) > 1e-6:
                rel_diff = abs(val_t - val_prev_next) / abs(val_t)
                if rel_diff > 0.005:
                    audit_logs.append(
                        f"{yr} `{m}`: Abweichung {rel_diff*100:.2f}% (Bericht {yr}: {val_t} vs. Vorjahr in {yr+1}: {val_prev_next})."
                    )
        curr_r["_healed"] = sorted(healed)
    return audit_logs


def _load_overrides(cfg: BankConfig) -> dict[str, Any]:
    ov_path = cfg.bank_dir / "overrides.json"
    if not ov_path.exists():
        return {}
    return json.loads(ov_path.read_text(encoding="utf-8"))


def _merge_extracted_by_period(extracted_dir: Path) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {"annual": [], "semester": [], "offenlegung": []}
    by_key: dict[tuple[str, str], dict] = {}

    for jf in sorted(extracted_dir.glob("*.json")):
        doc = json.loads(jf.read_text(encoding="utf-8"))
        meta = doc["meta"]
        rtype = meta["report_type"]
        bucket = "annual" if rtype == "annual" else ("semester" if rtype == "semester" else "offenlegung")
        key = (bucket, meta["period"])
        if key not in by_key:
            by_key[key] = {
                "year": int(meta["year"]),
                "period": meta["period"],
                "report_type": rtype,
                "report_file": meta["source_file"],
                "metrics": {},
            }
        else:
            # Bei Split-PDFs (z. B. ZKB 2025) Quellenliste erweitern
            if meta["source_file"] not in by_key[key]["report_file"]:
                by_key[key]["report_file"] += f"; {meta['source_file']}"
        for m_id, m_val in doc.get("metrics", {}).items():
            if m_id not in by_key[key]["metrics"]:
                by_key[key]["metrics"][m_id] = m_val

    for (bucket, _), entry in by_key.items():
        grouped[bucket].append(entry)
    for b in grouped:
        grouped[b].sort(key=lambda r: (r["year"], r["period"]))
    return grouped


def _extract_row_values(entry: dict, cfg: BankConfig, ov_period: dict) -> dict[str, Any]:
    yr = entry["year"]
    row: dict[str, Any] = {
        "bank_id": cfg.bank_id,
        "year": yr,
        "period": entry["period"],
        "report_type": entry["report_type"],
        "report_file": entry["report_file"],
        "currency_orig": cfg.reporting_currency,
        "_healed": [],
    }
    raw_metrics = entry["metrics"]
    all_keys = set(raw_metrics.keys()) | set(ov_period.keys())

    for m_id in all_keys:
        if m_id in ov_period and ov_period[m_id] is not None:
            val_orig = float(ov_period[m_id])
            prev_orig = None
            row["_healed"].append(f"{m_id}(override)")
        else:
            mdict = raw_metrics.get(m_id, {})
            unit = mdict.get("unit")
            val_orig = normalize_to_mio(m_id, mdict.get("value_current"), unit, cfg.reporting_currency)
            prev_orig = normalize_to_mio(m_id, mdict.get("value_prior_year"), unit, cfg.reporting_currency)

        # Währungsumrechnung für Cross-Bank-Kompatibilität (Mio. CHF)
        rate_type = "avg" if m_id in FLOW_METRICS else "eoy"
        if m_id in PCT_OR_UNITLESS_METRICS:
            val_chf = val_orig
            prev_chf = prev_orig
        else:
            val_chf = convert_to_chf(val_orig, cfg.reporting_currency, yr, rate_type=rate_type)
            prev_chf = convert_to_chf(prev_orig, cfg.reporting_currency, yr - 1, rate_type=rate_type) if prev_orig is not None else None

        out_key = f"{m_id}_mio" if (m_id not in PCT_OR_UNITLESS_METRICS and not m_id.endswith("_mio")) else m_id
        row[out_key] = r_round(val_chf, 3)
        if prev_chf is not None:
            row[f"{out_key}__prior"] = r_round(prev_chf, 3)
        if cfg.reporting_currency != "CHF" and m_id not in PCT_OR_UNITLESS_METRICS:
            row[f"{out_key}_orig"] = r_round(val_orig, 3)

    # Deterministische Einheiten-Disambiguierung gegen plausibility_bounds_chf_mio
    # (z. B. wenn VSKB in exakten CHF, Raiffeisen/PostFinance in Mio. ohne Header oder Mrd.-Highlights vorliegen)
    min_ta = cfg.plausibility_bounds_chf_mio.get("total_assets_min")
    max_ta = cfg.plausibility_bounds_chf_mio.get("total_assets_max")
    ta = row.get("total_assets_mio")
    if entry["report_type"] == "annual" and ta is not None and min_ta is not None and max_ta is not None:
        if not (min_ta <= ta <= max_ta):
            for factor in (1e-3, 1e-6, 1e-9, 1000.0):
                if min_ta <= ta * factor <= max_ta:
                    ta_unit = raw_metrics.get("total_assets", {}).get("unit")
                    for m_id in raw_metrics:
                        if m_id in PCT_OR_UNITLESS_METRICS or m_id in ov_period:
                            continue
                        if raw_metrics[m_id].get("unit") == ta_unit:
                            k = f"{m_id}_mio" if not m_id.endswith("_mio") else m_id
                            if row.get(k) is not None:
                                row[k] = r_round(row[k] * factor, 3)
                            if row.get(f"{k}__prior") is not None:
                                row[f"{k}__prior"] = r_round(row[f"{k}__prior"] * factor, 3)
                    row["_healed"].append(f"unit_scale({factor:g})")
                    break

    return row


def _enrich_annual_kpis(rows: list[dict], cfg: BankConfig) -> list[str]:
    plausibility_warnings: list[str] = []
    min_ta = cfg.plausibility_bounds_chf_mio.get("total_assets_min")
    max_ta = cfg.plausibility_bounds_chf_mio.get("total_assets_max")

    for i, r in enumerate(rows):
        yr = r["year"]
        ta = r.get("total_assets_mio")
        if ta is not None:
            if min_ta is not None and ta < min_ta:
                plausibility_warnings.append(f"{yr}: Bilanzsumme {ta:.1f} Mio. CHF unter Minimum {min_ta}!")
            if max_ta is not None and ta > max_ta:
                plausibility_warnings.append(f"{yr}: Bilanzsumme {ta:.1f} Mio. CHF über Maximum {max_ta}!")

        mort = r.get("mortgage_loans_mio") or 0.0
        other_l = r.get("customer_loans_other_mio") or 0.0
        tot_loans = (mort + other_l) if (r.get("mortgage_loans_mio") is not None or r.get("customer_loans_other_mio") is not None) else None
        r["total_customer_loans_mio"] = r_round(tot_loans, 3)

        inc = r.get("total_operating_income_mio")
        if inc is None and r.get("net_interest_income_mio") is not None and r.get("commission_income_mio") is not None:
            inc = r_round(
                (r.get("net_interest_income_mio") or 0.0)
                + (r.get("commission_income_mio") or 0.0)
                + (r.get("trading_income_mio") or 0.0)
                + (r.get("other_ordinary_income_mio") or 0.0),
                3,
            )
            r["total_operating_income_mio"] = inc
            r.setdefault("_healed", []).append("total_operating_income_mio(sum_components)")
        elif inc is None and r.get("operating_profit_mio") is not None and r.get("total_operating_expenses_mio") is not None:
            inc = r_round(r["operating_profit_mio"] + abs(r["total_operating_expenses_mio"]), 3)
            r["total_operating_income_mio"] = inc
            r.setdefault("_healed", []).append("total_operating_income_mio(op_plus_exp)")
        exp = r.get("total_operating_expenses_mio")
        if exp is not None and inc is not None and inc > 0:
            if abs(exp) > inc * 50.0:
                exp = r_round(exp / 1000.0, 3)
                r["total_operating_expenses_mio"] = exp
            elif 0 < abs(exp) < inc * 0.01:
                exp = r_round(exp * 1000.0, 3)
                r["total_operating_expenses_mio"] = exp
        exp_abs = abs(exp) if exp is not None else None
        if inc is not None and inc > 0 and r.get("net_profit_mio") is not None and abs(r["net_profit_mio"]) > inc * 5.0:
            r["net_profit_mio"] = r_round(r["net_profit_mio"] / 1000.0, 3)
        r["cir_pct"] = r_round(safe_div(exp_abs, inc, 100.0), 2)
        r["interest_share_pct"] = r_round(safe_div(r.get("net_interest_income_mio"), inc, 100.0), 2)
        r["commission_share_pct"] = r_round(safe_div(r.get("commission_income_mio"), inc, 100.0), 2)
        r["trading_share_pct"] = r_round(safe_div(r.get("trading_income_mio"), inc, 100.0), 2)

        r["mortgage_share_pct"] = 0.0 if cfg.has_credit_ban else r_round(safe_div(r.get("mortgage_loans_mio"), ta, 100.0), 2)
        r["deposit_to_mortgage_pct"] = None if cfg.has_credit_ban else r_round(safe_div(r.get("customer_deposits_mio"), r.get("mortgage_loans_mio"), 100.0), 2)
        r["deposit_coverage_pct"] = r_round(safe_div(r.get("customer_deposits_mio"), tot_loans, 100.0), 2)
        eq = r.get("shareholders_equity_mio")
        if eq is not None and ta is not None and ta > 0:
            if eq > ta * 0.50 and (ta * 0.02 <= eq / 1000.0 <= ta * 0.35):
                eq = r_round(eq / 1000.0, 3)
                r["shareholders_equity_mio"] = eq
                r.setdefault("_healed", []).append("shareholders_equity_mio(/1000)")
            elif eq < ta * 0.01 and (ta * 0.02 <= eq * 1000.0 <= ta * 0.35):
                eq = r_round(eq * 1000.0, 3)
                r["shareholders_equity_mio"] = eq
                r.setdefault("_healed", []).append("shareholders_equity_mio(x1000)")
            elif eq < ta * 0.015 or eq > ta * 0.50:
                eq = None
                r["shareholders_equity_mio"] = None
        r["equity_ratio_pct"] = r_round(safe_div(eq, ta, 100.0), 2)
        r["roe_pct"] = r_round(safe_div(r.get("net_profit_mio"), eq, 100.0), 2)
        r["roa_pct"] = r_round(safe_div(r.get("net_profit_mio"), ta, 100.0), 3)
        r["net_interest_margin_bps"] = r_round(safe_div(r.get("net_interest_income_mio"), ta, 10000.0), 1)

        fte = r.get("fte_count")
        inc_fte = safe_div(inc, fte, 1000.0)
        pers_abs = abs(r["personnel_expenses_mio"]) if r.get("personnel_expenses_mio") is not None else None
        pers_fte = safe_div(pers_abs, fte, 1000.0)
        r["income_per_fte_tchf"] = r_round(inc_fte, 1)
        r["personnel_cost_per_fte_tchf"] = r_round(pers_fte, 1)
        r["wage_to_productivity_pct"] = r_round(safe_div(pers_fte, inc_fte, 100.0), 1)
        r["productivity_to_wage_ratio"] = r_round(safe_div(inc_fte, pers_fte, 1.0), 2)
        r["op_profit_per_fte_tchf"] = r_round(safe_div(r.get("operating_profit_mio"), fte, 1000.0), 1)
        r["assets_per_fte_mio"] = r_round(safe_div(ta, fte, 1.0), 2)

        t_info = get_turnover_for_year(cfg.bank_id, yr)
        if t_info:
            if r.get("turnover_rate_pct") is None:
                r["turnover_rate_pct"] = t_info.get("rate")
            if r.get("turnover_net_pct") is None:
                r["turnover_net_pct"] = t_info.get("net")
            if r.get("turnover_gross_pct") is None:
                r["turnover_gross_pct"] = t_info.get("gross")
        else:
            r.setdefault("turnover_rate_pct", None)
            r.setdefault("turnover_net_pct", None)
            r.setdefault("turnover_gross_pct", None)

        sp_raw = r.get("share_price_eoy")
        div_raw = r.get("dividend_per_share")
        if cfg.share_splits and (sp_raw is not None or div_raw is not None):
            r["share_price_eoy_raw"] = sp_raw
            r["dividend_per_share_raw"] = div_raw
            sp_adj, div_adj, factor = apply_share_splits(yr, sp_raw, div_raw, cfg.share_splits)
            r["share_price_eoy"] = sp_adj
            r["dividend_per_share"] = div_adj
            r["split_factor_applied"] = factor
        else:
            r["split_factor_applied"] = 1.0

        r["dividend_yield_pct"] = r_round(safe_div(r.get("dividend_per_share"), r.get("share_price_eoy"), 100.0), 2)

        # YoY-Wachstumsraten
        if i > 0:
            prev = rows[i - 1]
            r["yoy_assets_pct"] = r_round(safe_div((ta - prev["total_assets_mio"]) if (ta is not None and prev.get("total_assets_mio") is not None) else None, prev.get("total_assets_mio"), 100.0), 2)
            r["yoy_income_pct"] = r_round(safe_div((inc - prev["total_operating_income_mio"]) if (inc is not None and prev.get("total_operating_income_mio") is not None) else None, prev.get("total_operating_income_mio"), 100.0), 2)
            np_curr, np_prev = r.get("net_profit_mio"), prev.get("net_profit_mio")
            r["yoy_net_profit_pct"] = r_round(safe_div((np_curr - np_prev) if (np_curr is not None and np_prev is not None) else None, abs(np_prev) if np_prev else None, 100.0), 2)

    return plausibility_warnings


def _enrich_offenlegung(rows: list[dict], cfg: BankConfig, annual_by_year: dict[int, dict]) -> None:
    cet1_target = cfg.capital_targets_pct.get("cet1_target")
    tot_target = cfg.capital_targets_pct.get("total_capital_target")
    for r in rows:
        yr = r["year"]
        r["sort_date"] = f"{yr}-06-30" if "H1" in r["period"] else (f"{yr}-03-31" if "Q1" in r["period"] else (f"{yr}-09-30" if "Q3" in r["period"] else f"{yr}-12-31"))
        r["regime"] = "Basel III final" if yr >= 2025 else "Basel III"
        ann_r = annual_by_year.get(yr)
        ta = ann_r.get("total_assets_mio") if ann_r else None
        r["matched_total_assets_mio"] = ta
        r["rwa_density_pct"] = r_round(safe_div(r.get("rwa_total_mio"), ta, 100.0), 2)
        if cet1_target is not None and r.get("cet1_ratio_pct") is not None:
            r["cet1_excess_over_target_pp"] = r_round(r["cet1_ratio_pct"] - cet1_target, 2)
        if tot_target is not None and r.get("total_capital_ratio_pct") is not None:
            r["total_cap_excess_over_target_pp"] = r_round(r["total_capital_ratio_pct"] - tot_target, 2)
        # Rückspiegelung der Jahresend-Offenlegung (12-31) in das Annual-Panel, falls dort leer
        if ann_r is not None and r["sort_date"].endswith("-12-31"):
            for k in (
                "cet1_capital_mio",
                "tier1_capital_mio",
                "total_capital_mio",
                "rwa_total_mio",
                "cet1_ratio_pct",
                "total_capital_ratio_pct",
                "leverage_ratio_pct",
                "lcr_pct",
                "nsfr_pct",
            ):
                if ann_r.get(k) is None and r.get(k) is not None:
                    ann_r[k] = r[k]
                    ann_r.setdefault("_healed", []).append(f"{k}(from_offenlegung)")
    rows.sort(key=lambda x: x["sort_date"])


def _build_verguetung_real(annual_rows: list[dict], overrides: dict) -> list[dict]:
    comp_ov = overrides.get("compensation", {})
    out = []
    for r in annual_rows:
        yr = r["year"]
        if yr not in range(2001, 2027):
            continue
        cpi = get_cpi_index(yr)
        factor = cpi_factor_2025(yr)
        np_nom = r.get("net_profit_mio")
        pers_nom_tchf = (abs(r["personnel_expenses_mio"]) * 1000.0) if r.get("personnel_expenses_mio") is not None else None
        fte = r.get("fte_count")
        avg_fte_nom = safe_div(pers_nom_tchf, fte)
        inc_fte_nom = r.get("income_per_fte_tchf")
        c_yr = comp_ov.get(str(yr), {})
        vr_tot = c_yr.get("vr_total_tchf") or (r.get("vr_total_comp_mio") * 1000.0 if r.get("vr_total_comp_mio") else None)
        ceo_tot = c_yr.get("ceo_total_tchf") or (r.get("ceo_total_comp_mio") * 1000.0 if r.get("ceo_total_comp_mio") else None)
        gl_tot = c_yr.get("gl_total_tchf") or (r.get("gl_total_comp_mio") * 1000.0 if r.get("gl_total_comp_mio") else None)

        out.append(
            {
                "year": yr,
                "bfs_lik_dez1982": cpi,
                "cpi_factor_2025": round(factor, 6),
                "net_profit_mio_nom": np_nom,
                "net_profit_mio_real2025": r_round(deflate_to_real_2025(np_nom, yr), 3),
                "personnel_tchf_nom": r_round(pers_nom_tchf, 1),
                "personnel_mio_real2025": r_round(deflate_to_real_2025(safe_div(pers_nom_tchf, 1000.0), yr), 3),
                "fte_count": fte,
                "turnover_rate_pct": r.get("turnover_rate_pct"),
                "turnover_net_pct": r.get("turnover_net_pct"),
                "turnover_gross_pct": r.get("turnover_gross_pct"),
                "avg_per_fte_tchf_nom": r_round(avg_fte_nom, 2),
                "avg_per_fte_tchf_real2025": r_round(deflate_to_real_2025(avg_fte_nom, yr), 2),
                "income_per_fte_tchf_nom": inc_fte_nom,
                "income_per_fte_tchf_real2025": r_round(deflate_to_real_2025(inc_fte_nom, yr), 2),
                "wage_to_productivity_pct": r.get("wage_to_productivity_pct"),
                "productivity_to_wage_ratio": r.get("productivity_to_wage_ratio"),
                "vr_total_tchf_nom": vr_tot,
                "vr_total_tchf_real2025": r_round(deflate_to_real_2025(vr_tot, yr), 1),
                "ceo_total_tchf_nom": ceo_tot,
                "ceo_total_tchf_real2025": r_round(deflate_to_real_2025(ceo_tot, yr), 1),
                "gl_total_tchf_nom": gl_tot,
                "gl_total_tchf_real2025": r_round(deflate_to_real_2025(gl_tot, yr), 1),
                "notes": c_yr.get("notes", ""),
            }
        )
    return out


def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    clean_rows = []
    cols: list[str] = []
    for r in rows:
        cr = {k: (";".join(v) if isinstance(v, list) else v) for k, v in r.items() if not k.endswith("__prior")}
        clean_rows.append(cr)
        for k in cr:
            if k not in cols:
                cols.append(k)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for cr in clean_rows:
            w.writerow(cr)


def validate_bank(bank_id: str, strict_audit: bool = False) -> dict[str, Any]:
    cfg = load_bank_config(bank_id)
    cfg.data_dir.mkdir(parents=True, exist_ok=True)
    overrides = _load_overrides(cfg)
    grouped = _merge_extracted_by_period(cfg.extracted_dir)

    annual_rows = [_extract_row_values(e, cfg, overrides.get("annual", {}).get(str(e["year"]), {})) for e in grouped["annual"]]
    semester_rows = [_extract_row_values(e, cfg, overrides.get("semester", {}).get(str(e["year"]), {})) for e in grouped["semester"]]
    off_rows = [_extract_row_values(e, cfg, overrides.get("offenlegung", {}).get(e["period"], {})) for e in grouped["offenlegung"]]

    heal_metrics = [
        "total_assets_mio",
        "mortgage_loans_mio",
        "customer_deposits_mio",
        "shareholders_equity_mio",
        "net_interest_income_mio",
        "commission_income_mio",
        "total_operating_income_mio",
        "total_operating_expenses_mio",
        "operating_profit_mio",
        "net_profit_mio",
        "fte_count",
    ]
    audit_logs = self_heal_series(annual_rows, heal_metrics)
    plausibility_warnings = _enrich_annual_kpis(annual_rows, cfg)
    annual_by_year = {r["year"]: r for r in annual_rows}
    _enrich_offenlegung(off_rows, cfg, annual_by_year)
    verg_rows = _build_verguetung_real(annual_rows, overrides)

    for r in annual_rows:
        r["self_healed_fields"] = ";".join(r.pop("_healed", []))
    for r in semester_rows + off_rows:
        r["self_healed_fields"] = ";".join(r.pop("_healed", []))

    _write_csv(cfg.data_dir / f"{cfg.bank_id}_panel_annual.csv", annual_rows)
    _write_csv(cfg.data_dir / f"{cfg.bank_id}_panel_semester.csv", semester_rows)
    _write_csv(cfg.data_dir / f"{cfg.bank_id}_panel_offenlegung.csv", off_rows)
    _write_csv(cfg.data_dir / f"{cfg.bank_id}_verguetung_real.csv", verg_rows)

    all_payload = {
        "bank_id": cfg.bank_id,
        "full_name": cfg.full_name,
        "reporting_scope": cfg.reporting_scope,
        "reporting_currency": cfg.reporting_currency,
        "accounting_standard": cfg.accounting_standard,
        "annual": [{k: v for k, v in r.items() if not k.endswith("__prior")} for r in annual_rows],
        "semester": [{k: v for k, v in r.items() if not k.endswith("__prior")} for r in semester_rows],
        "offenlegung": [{k: v for k, v in r.items() if not k.endswith("__prior")} for r in off_rows],
        "verguetung_real": verg_rows,
        "audit_logs": audit_logs,
        "plausibility_warnings": plausibility_warnings,
    }
    (cfg.data_dir / f"{cfg.bank_id}_panel_all.json").write_text(
        json.dumps(all_payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Validation Report schreiben
    missing_core = []
    for r in annual_rows:
        for req in ("total_assets_mio", "total_operating_income_mio", "net_profit_mio"):
            if r.get(req) is None:
                missing_core.append(f"{r['period']}: `{req}` fehlt")
        roe = r.get("roe_pct")
        if roe is not None and not (r["bank_id"] == "ubs" and r["year"] == 2023):
            if not (-20.0 < roe < 35.0):
                plausibility_warnings.append(f"{r['year']}: ROE {roe:.2f} % ausserhalb [-20, 35] %!")
        cir = r.get("cir_pct")
        if cir is not None and not (25.0 < cir < 110.0):
            plausibility_warnings.append(f"{r['year']}: CIR {cir:.2f} % ausserhalb [25, 110] %!")
        div = r.get("dividend_per_share")
        if div is not None and not (0.0 <= div < 250.0):
            plausibility_warnings.append(f"{r['year']}: Dividende/Aktie {div:.2f} CHF unplausibel!")

    for r in off_rows:
        cet1 = r.get("cet1_ratio_pct")
        if cet1 is not None and not (8.0 < cet1 < 40.0):
            plausibility_warnings.append(f"{r['period']} Offenlegung: CET1 {cet1:.2f} % unplausibel!")
        lev = r.get("leverage_ratio_pct")
        if lev is not None and not (2.0 < lev < 20.0):
            plausibility_warnings.append(f"{r['period']} Offenlegung: Leverage Ratio {lev:.2f} % unplausibel!")

    rep_lines = [
        f"# Validierungs- & Selbstheilungsbericht: {cfg.full_name} (`{cfg.bank_id}`)",
        "",
        f"- **Scope:** `{cfg.reporting_scope}` | **Standard:** `{cfg.accounting_standard}` | **Währung:** `{cfg.reporting_currency}` (harmonisiert in Mio. CHF)",
        f"- **Abgedeckte Perioden:** {len(annual_rows)} Geschäftsjahre, {len(semester_rows)} Semesterberichte, {len(off_rows)} Offenlegungsstichtage",
        "",
        "## Plausibilitätsprüfung",
        *(["- Keine Plausibilitätsverletzungen."] if not plausibility_warnings else [f"- **WARNUNG:** {w}" for w in plausibility_warnings]),
        "",
        "## Kernkennzahlen-Vollständigkeit (`total_assets_mio`, `total_operating_income_mio`, `net_profit_mio`)",
        *(["- Alle Geschäftsjahre vollständig."] if not missing_core else [f"- {m}" for m in missing_core]),
        "",
        "## Vorjahres-Selbstheilung (`t → t+1`) & Abweichungen (> 0.5 %)",
        *(["- Keine Lücken oder Abweichungen > 0.5 % protokolliert."] if not audit_logs else [f"- {a}" for a in audit_logs]),
    ]
    (cfg.data_dir / "validation_report.md").write_text("\n".join(rep_lines) + "\n", encoding="utf-8")

    print(
        f"[OK] {cfg.bank_id}: {len(annual_rows)} Annual, {len(semester_rows)} Semester, "
        f"{len(off_rows)} Offenlegung validiert (Warnungen={len(plausibility_warnings)}, Lücken={len(missing_core)})."
    )
    if strict_audit and (plausibility_warnings or missing_core):
        raise SystemExit(f"[STRICT-AUDIT FAIL] {cfg.bank_id}: Warnungen={len(plausibility_warnings)}, Lücken={len(missing_core)}")
    return all_payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Stufe 3: Validator & KPI-Engine.")
    parser.add_argument("--bank", required=True, help="Bank-ID")
    parser.add_argument("--strict-audit", action="store_true", help="Bricht bei Plausibilitäts- oder Kernlücken ab.")
    args = parser.parse_args()
    validate_bank(args.bank, strict_audit=args.strict_audit)


if __name__ == "__main__":
    main()
