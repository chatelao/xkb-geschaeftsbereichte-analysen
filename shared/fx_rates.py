"""Offizielle SNB-Referenzkurse USD/CHF für die deterministische Währungsumrechnung (z. B. UBS).

Bestandsgrössen (Bilanz, RWA, Kapital, AuM) verwenden den Jahresendkurs (eoy),
Stromgrössen (Erfolgsrechnung, Vergütung, Cashflows) den Jahresdurchschnittskurs (avg).
"""

from __future__ import annotations

# Quelle: Schweizerische Nationalbank (SNB) Devisenkurse USD -> CHF
USD_CHF_EOY: dict[int, float] = {
    2019: 0.9677,
    2020: 0.8839,
    2021: 0.9129,
    2022: 0.9245,
    2023: 0.8414,
    2024: 0.9062,
    2025: 0.8820,
    2026: 0.8820,
}

USD_CHF_AVG: dict[int, float] = {
    2019: 0.9937,
    2020: 0.9389,
    2021: 0.9143,
    2022: 0.9547,
    2023: 0.8986,
    2024: 0.8805,
    2025: 0.8810,
    2026: 0.8810,
}


def get_fx_rate(currency: str, year: int, rate_type: str = "eoy") -> float:
    curr = currency.upper()
    if curr == "CHF":
        return 1.0
    if curr != "USD":
        raise ValueError(f"Nicht unterstützte Währung für FX-Umrechnung: {currency}")
    table = USD_CHF_EOY if rate_type == "eoy" else USD_CHF_AVG
    if year not in table:
        raise KeyError(f"Kein USD/CHF-{rate_type}-Kurs für Jahr {year} hinterlegt.")
    return table[year]


def convert_to_chf(
    value: float | None,
    currency: str,
    year: int,
    rate_type: str = "eoy",
) -> float | None:
    """Rechnet einen Betrag von `currency` deterministisch in CHF um."""
    if value is None:
        return None
    return value * get_fx_rate(currency, year, rate_type=rate_type)
