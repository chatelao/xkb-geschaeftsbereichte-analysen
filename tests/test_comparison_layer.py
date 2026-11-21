import csv
from pathlib import Path
from shared.config import VALID_BANKS

ROOT = Path(__file__).resolve().parent.parent
COMP_DIR = ROOT / "comparison"


def test_all_8_banks_reports_and_charts():
    for b in VALID_BANKS:
        assert (ROOT / b / "bank_config.yaml").exists()
        assert len(list((ROOT / b / "reports").glob("[01]*.md"))) == 10, f"{b} hat keine 10 Berichte"
        assert len(list((ROOT / b / "reports" / "charts").glob("*.png"))) == 13, f"{b} hat keine 13 Grafiken"


def test_comparison_layer_outputs():
    annual_csv = COMP_DIR / "data" / "xkb_comparison_annual.csv"
    assert annual_csv.exists()
    with annual_csv.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    banks_present = {r["bank_id"] for r in rows}
    assert banks_present == set(VALID_BANKS)
    assert any(r["bank_id"] == "ubs" and r["extraordinary_flag"] == "CS_NEGATIVE_GOODWILL" for r in rows)

    assert len(list((COMP_DIR / "reports").glob("0*.md"))) == 7
    assert len(list((COMP_DIR / "reports" / "charts").glob("*.png"))) == 13
