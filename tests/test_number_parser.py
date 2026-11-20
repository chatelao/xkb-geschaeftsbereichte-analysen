from shared.extractor import detect_unit_and_currency, parse_number


def test_swiss_apostrophe_and_space_thousands():
    assert parse_number("42'976.997") == 42976.997
    assert parse_number("42 976,997") == 42976.997
    assert parse_number("1’234’567") == 1234567.0


def test_english_comma_thousands():
    assert parse_number("1,234,567.89") == 1234567.89
    assert parse_number("27,712") == 27712.0


def test_negative_parentheses_and_dashes():
    assert parse_number("(280 848)") == -280848.0
    assert parse_number("(1,234.5)") == -1234.5
    assert parse_number("–12 345") == -12345.0
    assert parse_number("—") is None
    assert parse_number("n.a.") is None


def test_html_footnotes_and_percent():
    assert parse_number("100,7<br>2") == 100.7
    assert parse_number("18.28%") == 18.28
    assert parse_number("10.80 1") == 10.80


def test_unit_and_currency_detection():
    assert detect_unit_and_currency("in CHF 1 000") == ("TCHF", "CHF")
    assert detect_unit_and_currency("en millions de CHF") == ("Mio. CHF", "CHF")
    assert detect_unit_and_currency("in USD million") == ("Mio. USD", "USD")
    assert detect_unit_and_currency("in Mrd. CHF") == ("Mrd. CHF", "CHF")
