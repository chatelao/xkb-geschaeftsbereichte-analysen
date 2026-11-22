#!/usr/bin/env python3
"""Datengetriebene 300-DPI-Chart-Engine: Erzeugt exakt 13 standardisierte Grafiken pro Institut."""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from shared.config import BankConfig, load_bank_config

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


def _xy(rows: list[dict], key: str) -> tuple[list, list[float]]:
    xs, ys = [], []
    for r in rows:
        v = r.get(key)
        if v is not None:
            xs.append(r["year"])
            ys.append(float(v))
    return xs, ys


def _save(fig: plt.Figure, path: Path) -> Path:
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def _placeholder(path: Path, title: str, msg: str, color: str) -> Path:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.text(0.5, 0.5, msg, ha="center", va="center", fontsize=11, color=color, transform=ax.transAxes)
    ax.set_title(title)
    ax.axis("off")
    return _save(fig, path)


def generate_charts(bank_id: str) -> list[Path]:
    cfg: BankConfig = load_bank_config(bank_id)
    panel_path = cfg.data_dir / f"{cfg.bank_id}_panel_all.json"
    if not panel_path.exists():
        raise FileNotFoundError(f"Panel fehlt: {panel_path}")
    data = json.loads(panel_path.read_text(encoding="utf-8"))

    annual: list[dict[str, Any]] = data.get("annual", [])
    semester: list[dict[str, Any]] = data.get("semester", [])
    off: list[dict[str, Any]] = data.get("offenlegung", [])
    verg: list[dict[str, Any]] = data.get("verguetung_real", [])

    cfg.charts_dir.mkdir(parents=True, exist_ok=True)
    p = cfg.palette
    c_prim = p.get("primary", "#C8102E")
    c_sec = p.get("secondary", "#0F2942")
    c_acc = p.get("accent", "#0F766E")
    c_mut = p.get("muted", "#64748B")

    last = annual[-1] if annual else {}
    y1 = last.get("year", 2025)
    created: list[Path] = []

    # 1. 01_erfolgsrechnung_wasserfall_latest.png
    p1 = cfg.charts_dir / "01_erfolgsrechnung_wasserfall_latest.png"
    nii = last.get("net_interest_income_mio") or 0.0
    com = last.get("commission_income_mio") or 0.0
    trd = last.get("trading_income_mio") or 0.0
    inc = last.get("total_operating_income_mio") or (nii + com + trd)
    exp = -abs(last.get("total_operating_expenses_mio") or 0.0)
    np = last.get("net_profit_mio") or 0.0
    rest = np - (inc + exp)
    if inc:
        fig, ax = plt.subplots(figsize=(9, 4.8))
        labels = ["Zinserfolg", "Kommission", "Handel", "Geschäftsertrag", "Aufwand", "Steuern/Übr.", "Reingewinn"]
        vals = [nii, com, trd, inc, exp, rest, np]
        bottoms = [0, nii, nii + com, 0, inc, inc + exp, 0]
        heights = [nii, com, trd, inc, exp, rest, np]
        colors = [c_sec, c_acc, c_mut, c_prim, "#DC2626", "#94A3B8", c_sec]
        for idx, (lbl, b, h, col) in enumerate(zip(labels, bottoms, heights, colors)):
            ax.bar(idx, h, bottom=b, color=col, width=0.6)
            ax.text(idx, b + h + (inc * 0.02 if h >= 0 else -inc * 0.05), f"{h:,.0f}".replace(",", "'"), ha="center", fontsize=8)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=15)
        ax.set_ylabel("Mio. CHF")
        ax.set_title(f"{cfg.short_name}: Erfolgsrechnung {y1} – Wasserfall (Mio. CHF)")
        created.append(_save(fig, p1))
    else:
        created.append(_placeholder(p1, f"{cfg.short_name}: Erfolgsrechnung", "Keine Daten", c_mut))

    # 2. 01_ertrag_kosten_marge_kombi.png
    p2 = cfg.charts_dir / "01_ertrag_kosten_marge_kombi.png"
    xs, ys_inc = _xy(annual, "total_operating_income_mio")
    _, ys_np = _xy(annual, "net_profit_mio")
    if xs:
        fig, ax1 = plt.subplots(figsize=(9.5, 4.8))
        ax1.bar([x - 0.18 for x in xs], ys_inc, width=0.35, color=c_sec, label="Geschäftsertrag (Mio. CHF)")
        ax1.bar([x + 0.18 for x in xs], [r.get("net_profit_mio") or 0 for r in annual if r.get("total_operating_income_mio") is not None], width=0.35, color=c_prim, label="Reingewinn (Mio. CHF)")
        ax1.set_ylabel("Mio. CHF")
        ax2 = ax1.twinx()
        xs_cir, ys_cir = _xy(annual, "cir_pct")
        if xs_cir:
            ax2.plot(xs_cir, ys_cir, color=c_acc, marker="o", linewidth=2, label="CIR (%)")
            ax2.set_ylabel("Cost-Income-Ratio (%)")
        ax1.set_title(f"{cfg.short_name}: Ertrag, Reingewinn & CIR")
        ax1.legend(loc="upper left")
        created.append(_save(fig, p2))
    else:
        created.append(_placeholder(p2, f"{cfg.short_name}: Ertrag & Marge", "Keine Daten", c_mut))

    # 3. 02_bilanz_gestapelte_saeulen_latest.png
    p3 = cfg.charts_dir / "02_bilanz_gestapelte_saeulen_latest.png"
    ta = last.get("total_assets_mio") or 0.0
    if ta > 0:
        fig, ax = plt.subplots(figsize=(7.5, 4.8))
        mort = last.get("mortgage_loans_mio") or 0.0
        oth_l = last.get("customer_loans_other_mio") or 0.0
        finv = last.get("financial_investments_mio") or 0.0
        rem_a = max(0.0, ta - mort - oth_l - finv)
        dep = last.get("customer_deposits_mio") or 0.0
        eq = last.get("shareholders_equity_mio") or 0.0
        rem_p = max(0.0, ta - dep - eq)
        ax.bar(["Aktiven", "Passiven"], [mort, dep], color=c_sec, label="Hypotheken / Kundeneinlagen")
        ax.bar(["Aktiven", "Passiven"], [oth_l + finv, eq], bottom=[mort, dep], color=c_acc, label="Übr. Kredite & Finanzanl. / Eigenkapital")
        ax.bar(["Aktiven", "Passiven"], [rem_a, rem_p], bottom=[mort + oth_l + finv, dep + eq], color=c_mut, label="Übrige Bilanzpositionen")
        ax.set_ylabel("Mio. CHF")
        ax.set_title(f"{cfg.short_name}: Bilanzstruktur {y1} (Total {ta:,.0f} Mio. CHF)".replace(",", "'"))
        ax.legend(loc="upper right", fontsize=8)
        created.append(_save(fig, p3))
    else:
        created.append(_placeholder(p3, f"{cfg.short_name}: Bilanzstruktur", "Keine Daten", c_mut))

    # 4. 02_bilanz_treemap_latest.png (proportionale horizontale Block-Darstellung ohne Zusatz-Dependency)
    p4 = cfg.charts_dir / "02_bilanz_treemap_latest.png"
    if ta > 0:
        fig, ax = plt.subplots(figsize=(8.5, 4.5))
        parts = [
            ("Hypotheken", last.get("mortgage_loans_mio") or 0.0, c_sec),
            ("Kundenkredite", last.get("customer_loans_other_mio") or 0.0, c_acc),
            ("Finanzanlagen", last.get("financial_investments_mio") or 0.0, c_prim),
        ]
        used = sum(v for _, v, _ in parts)
        if ta > used:
            parts.append(("Flüssige Mittel & Übr.", ta - used, c_mut))
        parts = sorted([(l, v, col) for l, v, col in parts if v > 0], key=lambda x: x[1], reverse=True)
        x_cur = 0.0
        for lbl, val, col in parts:
            w = val / ta * 100.0
            ax.add_patch(patches.Rectangle((x_cur, 0), w, 10, facecolor=col, edgecolor="white", linewidth=2))
            if w > 6:
                ax.text(x_cur + w / 2, 5, f"{lbl}\n{val:,.0f} Mio.\n({w:.1f}%)".replace(",", "'"), ha="center", va="center", color="white", fontsize=8, fontweight="bold")
            x_cur += w
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 10)
        ax.axis("off")
        ax.set_title(f"{cfg.short_name}: Aktivseite Proportional ({y1})")
        created.append(_save(fig, p4))
    else:
        created.append(_placeholder(p4, f"{cfg.short_name}: Bilanz-Treemap", "Keine Daten", c_mut))

    # 5. 02_bilanz_sankey_latest.png (Fluss-Diagramm Refinanzierung -> Aktiven)
    p5 = cfg.charts_dir / "02_bilanz_sankey_latest.png"
    if ta > 0:
        fig, ax = plt.subplots(figsize=(8.5, 4.5))
        dep = last.get("customer_deposits_mio") or 0.0
        eq = last.get("shareholders_equity_mio") or 0.0
        mort = last.get("mortgage_loans_mio") or 0.0
        finv = last.get("financial_investments_mio") or 0.0
        ax.barh(["Kundeneinlagen", "Eigenkapital"], [dep, eq], color=[c_sec, c_acc], height=0.45)
        ax.barh(["Hypotheken", "Finanzanlagen"], [-mort, -finv], color=[c_prim, c_mut], height=0.45)
        ax.axvline(0, color="black", linewidth=1)
        ax.set_xlabel("Aktiven (-)  |  Passiven (+) in Mio. CHF")
        ax.set_title(f"{cfg.short_name}: Mittelherkunft & Mittelverwendung ({y1})")
        created.append(_save(fig, p5))
    else:
        created.append(_placeholder(p5, f"{cfg.short_name}: Bilanz-Fluss", "Keine Daten", c_mut))

    # 6. 02_bilanz_langfrist_wachstum.png
    p6 = cfg.charts_dir / "02_bilanz_langfrist_wachstum.png"
    xs_ta, ys_ta = _xy(annual, "total_assets_mio")
    xs_dep, ys_dep = _xy(annual, "customer_deposits_mio")
    xs_m, ys_m = _xy(annual, "mortgage_loans_mio")
    if xs_ta:
        fig, ax = plt.subplots(figsize=(9.5, 4.8))
        ax.plot(xs_ta, ys_ta, marker="o", color=c_sec, linewidth=2, label="Bilanzsumme")
        if xs_dep:
            ax.plot(xs_dep, ys_dep, marker="s", color=c_acc, linewidth=1.8, label="Kundeneinlagen")
        if xs_m and not cfg.has_credit_ban:
            ax.plot(xs_m, ys_m, marker="^", color=c_prim, linewidth=1.8, label="Hypotheken")
        ax.set_ylabel("Mio. CHF")
        ax.set_title(f"{cfg.short_name}: Langfristiges Bilanzwachstum")
        ax.legend()
        created.append(_save(fig, p6))
    else:
        created.append(_placeholder(p6, f"{cfg.short_name}: Bilanzwachstum", "Keine Daten", c_mut))

    # 7. 03_soll_ist_vergleich_horizontal_latest.png
    p7 = cfg.charts_dir / "03_soll_ist_vergleich_horizontal_latest.png"
    last_off = off[-1] if off else {}
    if last_off:
        fig, ax = plt.subplots(figsize=(8.5, 4.5))
        items = sorted([
            ("CET1-Quote (%)", last_off.get("cet1_ratio_pct") or 0.0, cfg.capital_targets_pct.get("cet1_target", 9.2)),
            ("Gesamtkapital (%)", last_off.get("total_capital_ratio_pct") or 0.0, cfg.capital_targets_pct.get("total_capital_target", 13.4)),
            ("Leverage Ratio (%)", last_off.get("leverage_ratio_pct") or 0.0, cfg.capital_targets_pct.get("leverage_min", 3.0)),
        ], key=lambda x: x[1], reverse=True)
        y_pos = range(len(items))
        ax.barh(y_pos, [x[1] for x in items], color=c_sec, height=0.5, label="Ist-Wert")
        ax.scatter([x[2] for x in items], y_pos, color=c_prim, zorder=5, s=70, label="FINMA-Ziel / Min.")
        ax.set_yticks(list(y_pos))
        ax.set_yticklabels([x[0] for x in items])
        ax.invert_yaxis()
        ax.set_xlabel("%")
        ax.set_title(f"{cfg.short_name}: Aufsichtsrechtlicher Soll-Ist-Vergleich ({last_off.get('period')})")
        ax.legend()
        created.append(_save(fig, p7))
    else:
        created.append(_placeholder(p7, f"{cfg.short_name}: Soll-Ist-Vergleich", "Keine Offenlegungsdaten", c_mut))

    # 8. 03_kapital_rwa_basel.png
    p8 = cfg.charts_dir / "03_kapital_rwa_basel.png"
    off_p = [r["period"] for r in off if r.get("cet1_ratio_pct") is not None]
    off_cet1 = [r["cet1_ratio_pct"] for r in off if r.get("cet1_ratio_pct") is not None]
    if off_p:
        fig, ax = plt.subplots(figsize=(9.5, 4.5))
        ax.plot(range(len(off_p)), off_cet1, marker="o", color=c_sec, linewidth=2, label="CET1-Quote (%)")
        ax.axhline(cfg.capital_targets_pct.get("cet1_target", 9.2), color=c_prim, linestyle="--", label="CET1-Zielgrösse")
        step = max(1, len(off_p) // 10)
        ax.set_xticks(range(0, len(off_p), step))
        ax.set_xticklabels([off_p[i] for i in range(0, len(off_p), step)], rotation=25)
        ax.set_ylabel("%")
        ax.set_title(f"{cfg.short_name}: Kapitalquoten-Verlauf (Basel III / Basel III final)")
        ax.legend()
        created.append(_save(fig, p8))
    else:
        created.append(_placeholder(p8, f"{cfg.short_name}: Basel III Verlauf", "Keine Offenlegungsdaten", c_mut))

    # 9. 04_effizienz_produktivitaet.png
    p9 = cfg.charts_dir / "04_effizienz_produktivitaet.png"
    xs_c, ys_c = _xy(annual, "cir_pct")
    xs_f, ys_f = _xy(annual, "income_per_fte_tchf")
    if xs_c or xs_f:
        fig, ax1 = plt.subplots(figsize=(9.5, 4.8))
        if xs_c:
            ax1.plot(xs_c, ys_c, marker="o", color=c_prim, linewidth=2, label="CIR (%)")
            ax1.set_ylabel("CIR (%)", color=c_prim)
        ax2 = ax1.twinx()
        if xs_f:
            ax2.bar(xs_f, ys_f, alpha=0.35, color=c_sec, label="Ertrag / FTE (TCHF)")
            ax2.set_ylabel("Ertrag / FTE (TCHF)", color=c_sec)
        ax1.set_title(f"{cfg.short_name}: Operative Effizienz (CIR) & Produktivität je FTE")
        created.append(_save(fig, p9))
    else:
        created.append(_placeholder(p9, f"{cfg.short_name}: Effizienz & FTE", "Keine Daten", c_mut))

    # 10. 05_eigentuemer_wertschoepfung.png
    p10 = cfg.charts_dir / "05_eigentuemer_wertschoepfung.png"
    xs_sp, ys_sp = _xy(annual, "share_price_eoy")
    xs_np, ys_np = _xy(annual, "net_profit_mio")
    if xs_sp or xs_np:
        fig, ax = plt.subplots(figsize=(9.5, 4.8))
        if xs_sp:
            ax.plot(xs_sp, ys_sp, marker="o", color=c_prim, linewidth=2, label="Aktienkurs split-bereinigt (CHF)")
            ax.set_ylabel("CHF")
        else:
            ax.bar(xs_np, ys_np, color=c_sec, label="Reingewinn (Mio. CHF)")
            ax.set_ylabel("Mio. CHF")
        ax.set_title(f"{cfg.short_name}: Eigentümer-Wertschöpfung ({cfg.report_05_mode})")
        ax.legend()
        created.append(_save(fig, p10))
    else:
        created.append(_placeholder(p10, f"{cfg.short_name}: Eigentümer-Wertschöpfung", "Keine Daten", c_mut))

    # 11. 06_semester_saisonalitaet_reserven.png
    p11 = cfg.charts_dir / "06_semester_saisonalitaet_reserven.png"
    xs_s, ys_s = _xy(semester, "net_profit_mio")
    if xs_s:
        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.bar(xs_s, ys_s, color=c_acc, width=0.6, label="Halbjahresgewinn H1 (Mio. CHF)")
        m_s = statistics.mean(ys_s)
        ax.axhline(m_s, color=c_prim, linestyle="--", linewidth=1.4, label=f"Mittelwert (Ø): {m_s:,.1f} Mio.".replace(",", "'"))
        ax.set_ylabel("Mio. CHF")
        ax.set_title(f"{cfg.short_name}: Semester-Entwicklung (H1)")
        ax.legend()
        created.append(_save(fig, p11))
    else:
        created.append(_placeholder(p11, f"{cfg.short_name}: Semesterberichte", "Keine Semesterberichte vorhanden", c_mut))

    # 12. 07_langfrist_dashboard_epochen.png
    p12 = cfg.charts_dir / "07_langfrist_dashboard_epochen.png"
    if xs_ta and ys_ta[0] > 0:
        fig, ax = plt.subplots(figsize=(9.5, 4.8))
        base_ta = ys_ta[0]
        ax.plot(xs_ta, [y / base_ta * 100.0 for y in ys_ta], marker="o", color=c_sec, linewidth=2, label=f"Bilanzsumme ({xs_ta[0]} = 100)")
        if xs_np and ys_np[0] > 0:
            base_np = ys_np[0]
            ax.plot(xs_np, [y / base_np * 100.0 for y in ys_np], marker="s", color=c_prim, linewidth=2, label=f"Reingewinn ({xs_np[0]} = 100)")
        for ep in cfg.epochs:
            ax.axvspan(ep["start"] - 0.4, ep["end"] + 0.4, alpha=0.06, color=c_acc)
        ax.set_ylabel("Index (Basis = 100)")
        ax.set_title(f"{cfg.short_name}: Langfrist-Index & Strategische Epochen")
        ax.legend()
        created.append(_save(fig, p12))
    else:
        created.append(_placeholder(p12, f"{cfg.short_name}: Epochen-Dashboard", "Keine Daten", c_mut))

    # 13. 07_gewinn_loehne_verguetung_real.png
    p13 = cfg.charts_dir / "07_gewinn_loehne_verguetung_real.png"
    xs_v = [r["year"] for r in verg if r.get("net_profit_mio_real2025") is not None]
    ys_vr = [r["net_profit_mio_real2025"] for r in verg if r.get("net_profit_mio_real2025") is not None]
    if xs_v:
        fig, ax = plt.subplots(figsize=(9.5, 4.8))
        ax.plot(xs_v, ys_vr, marker="o", color=c_prim, linewidth=2, label="Reingewinn real 2025 (Mio. CHF)")
        xs_l = [r["year"] for r in verg if r.get("avg_per_fte_tchf_real2025") is not None]
        ys_l = [r["avg_per_fte_tchf_real2025"] for r in verg if r.get("avg_per_fte_tchf_real2025") is not None]
        if xs_l:
            ax2 = ax.twinx()
            ax2.plot(xs_l, ys_l, marker="^", color=c_sec, linestyle="--", label="Personalaufwand/FTE real 2025 (TCHF)")
            ax2.set_ylabel("TCHF real 2025")
        ax.set_ylabel("Mio. CHF real 2025")
        ax.set_title(f"{cfg.short_name}: Reale Gewinn- & Lohnentwicklung (BFS LIK, Basis 2025)")
        ax.legend(loc="upper left")
        created.append(_save(fig, p13))
    else:
        created.append(_placeholder(p13, f"{cfg.short_name}: Reale Vergütung", "Keine Daten", c_mut))

    print(f"[OK] {cfg.bank_id}: {len(created)} Grafiken (300 DPI) in {cfg.charts_dir}/ erzeugt.")
    return created


def main() -> None:
    parser = argparse.ArgumentParser(description="Stufe 4: 300-DPI-Chart-Engine (13 Grafiken pro Bank).")
    parser.add_argument("--bank", required=True, help="Bank-ID")
    args = parser.parse_args()
    generate_charts(args.bank)


if __name__ == "__main__":
    main()
