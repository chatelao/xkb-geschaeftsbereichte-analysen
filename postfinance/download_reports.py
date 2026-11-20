#!/usr/bin/env python3
"""PostFinance AG Berichte Downloader – Geschäfts-, Halbjahres- und Offenlegungsberichte."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.download_utils import download_catalog  # noqa: E402

BASE = "https://www.postfinance.ch"

CATALOG: dict[str, str | list[str]] = {
    # Geschäftsberichte (2013–2025, seit Gründung der PostFinance AG 2013)
    "postfinance-geschaeftsbericht-2013.pdf": f"{BASE}/content/dam/pfch/doc/440_459/450_01_2013_de.pdf",
    "postfinance-geschaeftsbericht-2014.pdf": f"{BASE}/content/dam/pfch/doc/440_459/450_01_2014_de.pdf",
    "postfinance-geschaeftsbericht-2015.pdf": f"{BASE}/content/dam/pfch/doc/440_459/450_01_2015_de.pdf",
    "postfinance-geschaeftsbericht-2016.pdf": f"{BASE}/content/dam/pfch/doc/440_459/450_01_2016_de.pdf",
    "postfinance-geschaeftsbericht-2017.pdf": f"{BASE}/content/dam/pfch/doc/440_459/450_01_2017_de.pdf",
    "postfinance-geschaeftsbericht-2018.pdf": f"{BASE}/content/dam/pfch/doc/440_459/450_01_2018_de.pdf",
    "postfinance-geschaeftsbericht-2019.pdf": f"{BASE}/content/dam/pfch/doc/440_459/450_01_2019_de.pdf",
    "postfinance-geschaeftsbericht-2020.pdf": f"{BASE}/content/dam/pfch/doc/440_459/450_01_2020_de.pdf",
    "postfinance-geschaeftsbericht-2021.pdf": f"{BASE}/content/dam/pfch/doc/440_459/450_01_2021_de.pdf",
    "postfinance-geschaeftsbericht-2022.pdf": f"{BASE}/content/dam/pfch/doc/440_459/450_01_2022_de.pdf",
    "postfinance-geschaeftsbericht-2023.pdf": f"{BASE}/content/dam/pfch/doc/440_459/450_01_2023_de.pdf",
    "postfinance-geschaeftsbericht-2024.pdf": f"{BASE}/content/dam/pfch/doc/440_459/450_01_2024_de.pdf",
    "postfinance-geschaeftsbericht-2025.pdf": f"{BASE}/content/dam/pfch/doc/440_459/450_01_2025_de.pdf",
    # Halbjahresberichte (verfügbare Einzelberichte)
    "postfinance-semesterbericht-2022.pdf": f"{BASE}/content/dam/pfch/doc/440_459/450_01_interim_2022_de.pdf",
    "postfinance-semesterbericht-2026.pdf": f"{BASE}/content/dam/pfch/doc/440_459/450_01_interim_2026_de.pdf",
    # Offenlegungsberichte / Eigenmitteloffenlegung (2013–06-2026)
    "postfinance-offenlegungsbericht-2013.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_dec_2013_de.pdf",
    "postfinance-offenlegungsbericht-06-2014.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_jun_2014_de.pdf",
    "postfinance-offenlegungsbericht-2014.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_dec_2014_de.pdf",
    "postfinance-offenlegungsbericht-06-2015.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_jun_2015_de.pdf",
    "postfinance-offenlegungsbericht-2015.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_dec_2015_de.pdf",
    "postfinance-offenlegungsbericht-06-2016.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_jun_2016_de.pdf",
    "postfinance-offenlegungsbericht-2016.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_dec_2016_de.pdf",
    "postfinance-offenlegungsbericht-03-2017.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_mar_2017_de.pdf",
    "postfinance-offenlegungsbericht-06-2017.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_jun_2017_de.pdf",
    "postfinance-offenlegungsbericht-09-2017.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_sep_2017_de.pdf",
    "postfinance-offenlegungsbericht-2017.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_dec_2017_de.pdf",
    "postfinance-offenlegungsbericht-03-2018.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_mar_2018_de.pdf",
    "postfinance-offenlegungsbericht-06-2018.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_jun_2018_de.pdf",
    "postfinance-offenlegungsbericht-09-2018.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_sep_2018_de.pdf",
    "postfinance-offenlegungsbericht-2018.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_dec_2018_de.pdf",
    "postfinance-offenlegungsbericht-03-2019.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_mar_2019_de.pdf",
    "postfinance-offenlegungsbericht-06-2019.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_jun_2019_de.pdf",
    "postfinance-offenlegungsbericht-09-2019.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_sep_2019_de.pdf",
    "postfinance-offenlegungsbericht-2019.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_dec_2019_de.pdf",
    "postfinance-offenlegungsbericht-03-2020.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_mar_2020_de.pdf",
    "postfinance-offenlegungsbericht-06-2020.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_jun_2020_de.pdf",
    "postfinance-offenlegungsbericht-09-2020.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_sep_2020_de.pdf",
    "postfinance-offenlegungsbericht-2020.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_dec_2020_de.pdf",
    "postfinance-offenlegungsbericht-03-2021.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_mar_2021_de.pdf",
    "postfinance-offenlegungsbericht-06-2021.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_jun_2021_de.pdf",
    "postfinance-offenlegungsbericht-09-2021.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_sep_2021_de.pdf",
    "postfinance-offenlegungsbericht-2021.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_dec_2021_de.pdf",
    "postfinance-offenlegungsbericht-03-2022.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_mar_2022_de.pdf",
    "postfinance-offenlegungsbericht-06-2022.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_jun_2022_de.pdf",
    "postfinance-offenlegungsbericht-09-2022.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_sep_2022_de.pdf",
    "postfinance-offenlegungsbericht-2022.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_dec_2022_de.pdf",
    "postfinance-offenlegungsbericht-03-2023.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_mar_2023_de.pdf",
    "postfinance-offenlegungsbericht-06-2023.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_jun_2023_de.pdf",
    "postfinance-offenlegungsbericht-09-2023.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_sep_2023_de.pdf",
    "postfinance-offenlegungsbericht-2023.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_dec_2023_de.pdf",
    "postfinance-offenlegungsbericht-03-2024.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_mar_2024_de.pdf",
    "postfinance-offenlegungsbericht-06-2024.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_jun_2024_de.pdf",
    "postfinance-offenlegungsbericht-09-2024.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_sep_2024_de.pdf",
    "postfinance-offenlegungsbericht-2024.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_dec_2024_de.pdf",
    "postfinance-offenlegungsbericht-03-2025.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_mar_2025_de.pdf",
    "postfinance-offenlegungsbericht-06-2025.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_jun_2025_de.pdf",
    "postfinance-offenlegungsbericht-09-2025.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_sept_2025_de.pdf",
    "postfinance-offenlegungsbericht-2025.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_dec_2025_de.pdf",
    "postfinance-offenlegungsbericht-03-2026.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_mar_2026_de.pdf",
    "postfinance-offenlegungsbericht-06-2026.pdf": f"{BASE}/content/dam/pfch/doc/440_459/457_00_2_capital_adequacy_disclosure_jun_2026_de.pdf",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Download PostFinance AG PDF reports.")
    parser.add_argument("--force", action="store_true", help="Re-download existing PDFs")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force)


if __name__ == "__main__":
    main()
