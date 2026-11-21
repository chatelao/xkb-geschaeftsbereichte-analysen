import csv
from pathlib import Path
from shared.config import VALID_BANKS

ROOT = Path(__file__).resolve().parent.parent


def test_2025_core_completeness_and_plausibility():
    required_2025 = [
        "total_assets_mio",
        "shareholders_equity_mio",
        "net_interest_income_mio",
        "commission_income_mio",
        "total_operating_income_mio",
        "total_operating_expenses_mio",
        "net_profit_mio",
        "cir_pct",
        "roe_pct",
        "fte_count",
    ]
    for b in VALID_BANKS:
        with (ROOT / "banks" / b / "data" / f"{b}_panel_annual.csv").open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        r25 = next((r for r in rows if r["year"] == "2025"), None)
        assert r25 is not None, f"{b}: 2025 fehlt"
        for col in required_2025:
            assert r25.get(col) not in (None, ""), f"{b} 2025: {col} fehlt"
        roe = float(r25["roe_pct"])
        cir = float(r25["cir_pct"])
        wtp = float(r25["wage_to_productivity_pct"])
        ptw = float(r25["productivity_to_wage_ratio"])
        assert 0.5 < roe < 25.0, f"{b} 2025 ROE unplausibel: {roe}"
        assert 30.0 < cir < 95.0, f"{b} 2025 CIR unplausibel: {cir}"
        assert 15.0 < wtp < 70.0, f"{b} 2025 Lohn/Produktivität unplausibel: {wtp}"
        assert 1.5 < ptw < 6.0, f"{b} 2025 Produktivität/Lohn unplausibel: {ptw}"


def test_vorsorgeeinrichtungen_dataset():
    csv_path = ROOT / "comparison" / "data" / "xkb_vorsorgeeinrichtungen.csv"
    assert csv_path.exists()
    with csv_path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert {r["bank_id"] for r in rows} == set(VALID_BANKS)
    for r in rows:
        assert r["pk_name"]
        assert r["source_url_or_file"]
        if r.get("coverage_ratio_bvg_pct"):
            cov = float(r["coverage_ratio_bvg_pct"])
            assert 80.0 < cov < 180.0
