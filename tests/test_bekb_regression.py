import csv
from pathlib import Path
import pytest

BEKB_DIR = Path(__file__).resolve().parent.parent / "bekb"


def test_bekb_panel_regression():
    panel_csv = BEKB_DIR / "data" / "bekb_panel_annual.csv"
    assert panel_csv.exists(), "bekb_panel_annual.csv fehlt"
    with panel_csv.open(encoding="utf-8") as f:
        rows = {int(r["year"]): r for r in csv.DictReader(f)}

    assert len(rows) == 23
    # Referenzwerte aus chatelao/bekb-geschaeftsbereichte-analysen
    assert float(rows[2025]["total_assets_mio"]) == pytest.approx(42976.997, rel=1e-4)
    assert float(rows[2025]["total_operating_income_mio"]) == pytest.approx(547.297, rel=1e-4)
    assert float(rows[2025]["net_profit_mio"]) == pytest.approx(175.355, rel=1e-4)

    assert float(rows[2024]["total_assets_mio"]) == pytest.approx(40499.255, rel=1e-4)
    assert float(rows[2024]["net_profit_mio"]) == pytest.approx(180.666, rel=1e-4)

    assert float(rows[2015]["total_assets_mio"]) == pytest.approx(28034.674, rel=1e-4)
    assert float(rows[2003]["total_assets_mio"]) == pytest.approx(20117.0, rel=1e-3)


def test_bekb_reports_and_charts_count():
    reports = list((BEKB_DIR / "reports").glob("0*.md"))
    charts = list((BEKB_DIR / "reports" / "charts").glob("*.png"))
    assert len(reports) == 7
    assert len(charts) == 13
