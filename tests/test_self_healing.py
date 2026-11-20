from shared.validator_kpi import self_heal_series


def test_t_plus_1_self_healing_fills_gap():
    rows = [
        {"year": 2023, "total_assets_mio": None, "_healed": []},
        {"year": 2024, "total_assets_mio": 40499.255, "total_assets_mio__prior": 40053.489, "_healed": []},
    ]
    logs = self_heal_series(rows, ["total_assets_mio"])
    assert rows[0]["total_assets_mio"] == 40053.489
    assert "total_assets_mio" in rows[0]["_healed"]
    assert len(logs) == 1


def test_t_plus_1_logs_deviation_over_half_percent():
    rows = [
        {"year": 2023, "net_profit_mio": 100.0, "_healed": []},
        {"year": 2024, "net_profit_mio": 110.0, "net_profit_mio__prior": 102.0, "_healed": []},
    ]
    logs = self_heal_series(rows, ["net_profit_mio"])
    assert rows[0]["net_profit_mio"] == 100.0
    assert any("Abweichung" in l for l in logs)
