"""Offizieller Schweizer Landesindex der Konsumentenpreise (BFS LIK, Basis Dez. 1982 = 100).

Single Source of Truth für die Inflationsbereinigung auf reale CHF 2025 über alle 8 Institute.
"""

from __future__ import annotations

BFS_LIK_DEZ1982: dict[int, float] = {
    2003: 150.7,
    2004: 152.0,
    2005: 153.7,
    2006: 155.4,
    2007: 156.5,
    2008: 160.3,
    2009: 159.5,
    2010: 160.6,
    2011: 161.0,
    2012: 159.9,
    2013: 159.5,
    2014: 159.5,
    2015: 157.7,
    2016: 157.0,
    2017: 157.8,
    2018: 159.3,
    2019: 159.9,
    2020: 158.7,
    2021: 159.7,
    2022: 164.2,
    2023: 167.7,
    2024: 169.5,
    2025: 169.7,
    2026: 169.7,  # Vorläufiger Referenzwert für H1-2026 (Basis real 2025 CHF)
}

BASE_YEAR = 2025
BASE_INDEX = BFS_LIK_DEZ1982[BASE_YEAR]


def get_cpi_index(year: int) -> float:
    if year not in BFS_LIK_DEZ1982:
        raise KeyError(f"Kein BFS LIK Index für Jahr {year} hinterlegt.")
    return BFS_LIK_DEZ1982[year]


def cpi_factor_2025(year: int) -> float:
    """Multiplikator, um einen Nominalbetrag aus `year` in reale CHF 2025 umzurechnen."""
    return BASE_INDEX / get_cpi_index(year)


def deflate_to_real_2025(value: float | None, year: int) -> float | None:
    """Rechnet einen Nominalbetrag aus `year` deterministisch in reale CHF 2025 um."""
    if value is None:
        return None
    return value * cpi_factor_2025(year)
