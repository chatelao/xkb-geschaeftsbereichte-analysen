from shared.fx_rates import convert_to_chf, get_fx_rate
from shared.validator_kpi import apply_share_splits, normalize_to_mio


def test_normalize_to_mio():
    assert normalize_to_mio("total_assets", 42976997.0, "TCHF", "CHF") == 42976.997
    assert normalize_to_mio("total_assets", 42.977, "Mrd. CHF", "CHF") == 42977.0
    assert normalize_to_mio("net_profit", 175.355, "Mio. CHF", "CHF") == 175.355
    assert normalize_to_mio("cet1_ratio_pct", 18.28, "%", "CHF") == 18.28


def test_fx_conversion_usd_to_chf():
    assert get_fx_rate("CHF", 2025) == 1.0
    chf_eoy = convert_to_chf(1000.0, "USD", 2024, rate_type="eoy")
    chf_avg = convert_to_chf(1000.0, "USD", 2024, rate_type="avg")
    assert chf_eoy == 906.2
    assert chf_avg == 880.5


def test_bcv_share_split_1_to_10():
    splits = [{"date": "2020-05-28", "ratio": 10}]
    sp_2019, div_2019, f_2019 = apply_share_splits(2019, 789.0, 36.0, splits)
    assert f_2019 == 10.0
    assert sp_2019 == 78.9
    assert div_2019 == 3.6

    sp_2020, div_2020, f_2020 = apply_share_splits(2020, 96.4, 3.6, splits)
    assert f_2020 == 1.0
    assert sp_2020 == 96.4
    assert div_2020 == 3.6
