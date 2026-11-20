import pytest
from shared.cpi_bfs import cpi_factor_2025, deflate_to_real_2025, get_cpi_index


def test_bfs_cpi_values_and_deflation():
    assert get_cpi_index(2003) == 150.7
    assert get_cpi_index(2025) == 169.7
    assert cpi_factor_2025(2025) == 1.0
    real_2003 = deflate_to_real_2025(100.0, 2003)
    assert real_2003 == pytest.approx(100.0 * (169.7 / 150.7), rel=1e-6)
    assert deflate_to_real_2025(None, 2003) is None
