#!/usr/bin/env python3
"""Valiant Holding AG Berichte Downloader – lädt Annual-, Halbjahres- und Offenlegungsberichte (2016–2026)."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from shared.download_utils import download_catalog  # noqa: E402

CATALOG: dict[str, str | list[str]] = {
    # Annual Reports (2016–2025)
    "valiant-geschaeftsbericht-2016.pdf": "https://www.valiant.ch/documents/35003/141997/VH_Bericht+Gesch%C3%A4ftsjahr+2016.pdf",
    "valiant-geschaeftsbericht-2017.pdf": "https://www.valiant.ch/documents/35003/141873/VH_Bericht+Gesch%C3%A4ftsjahr+2017.pdf",
    "valiant-geschaeftsbericht-2018.pdf": "https://www.valiant.ch/documents/35003/141784/Valiant+Holding+AG+%E2%80%93+Bericht+zum+Gesch%C3%A4ftsjahr+2018.pdf",
    "valiant-geschaeftsbericht-2019.pdf": "https://www.valiant.ch/documents/35003/141695/Valiant+Holding+AG+%E2%80%93+Bericht+zum+Gesch%C3%A4ftsjahr+2019.pdf",
    "valiant-geschaeftsbericht-2020.pdf": "https://www.valiant.ch/documents/35003/1508360/Valiant+Holding+AG+-+Bericht+zum+Gesch%C3%A4ftsjahr+2020.pdf",
    "valiant-geschaeftsbericht-2021.pdf": "https://www.valiant.ch/documents/35003/2936433/Valiant+Holding+AG+-+Bericht+zum+Gesch%C3%A4ftsjahr+2021.pdf",
    "valiant-geschaeftsbericht-2022.pdf": "https://www.valiant.ch/documents/35003/4354208/Valiant+Holding+AG+%E2%80%93+Bericht+zum+Gesch%C3%A4ftsjahr+2022.pdf",
    "valiant-geschaeftsbericht-2023.pdf": "https://www.valiant.ch/documents/35003/7353422/Valiant+Holding+AG+%E2%80%93+Bericht+zum+Gesch%C3%A4ftsjahr+2023.pdf",
    "valiant-geschaeftsbericht-2024.pdf": "https://www.valiant.ch/documents/35003/11907684/Valiant+Holding+AG+%E2%80%93+Bericht+zum+Gesch%C3%A4ftsjahr+2024.pdf",
    "valiant-geschaeftsbericht-2025.pdf": "https://www.valiant.ch/documents/35003/13184863/Valiant+Holding+AG+%E2%80%93+Bericht+zum+Gesch%C3%A4ftsjahr+2025.pdf",
    # Half-Year Reports (2020–2026)
    "valiant-semesterbericht-2020.pdf": "https://www.valiant.ch/documents/35003/136660/Valiant+Holding+AG+-+Halbjahresbericht+per+30.+Juni+2020.pdf",
    "valiant-semesterbericht-2021.pdf": "https://www.valiant.ch/documents/35003/2097794/Valiant+Holding+AG+%E2%80%93+Halbjahresbericht+per+30.+Juni+2021.pdf",
    "valiant-semesterbericht-2022.pdf": "https://www.valiant.ch/documents/35003/3412032/Valiant+Holding+AG+%E2%80%93+Halbjahresbericht+per+30.+Juni+2022.pdf",
    "valiant-semesterbericht-2023.pdf": "https://www.valiant.ch/documents/35003/4955499/Valiant+Holding+AG+%E2%80%93+Halbjahresbericht+per+30.+Juni+2023.pdf",
    "valiant-semesterbericht-2024.pdf": "https://www.valiant.ch/documents/35003/8647338/Valiant+Holding+AG+%E2%80%93+Halbjahresbericht+per+30.+Juni+2024.pdf",
    "valiant-semesterbericht-2026.pdf": "https://www.valiant.ch/documents/35003/13319974/Valiant+Holding+AG+%E2%80%93+Halbjahresbericht+per+30.+Juni+2026.pdf",
    # Pillar 3 Disclosures (2020–2026)
    "valiant-offenlegungsbericht-2020.pdf": "https://www.valiant.ch/documents/35003/1508360/Valiant+Holding+AG+-+Offenlegung+der+Eigenmittel+und+der+Liquidit%C3%A4t+per+31.12.2020.pdf",
    "valiant-offenlegungsbericht-2021.pdf": "https://www.valiant.ch/documents/35003/2936433/Valiant+Holding+AG+-+Offenlegung+der+Eigenmittel+und+der+Liquidit%C3%A4t+per+31.12.2021.pdf",
    "valiant-offenlegungsbericht-2022.pdf": "https://www.valiant.ch/documents/35003/4354208/Valiant+Holding+AG+%E2%80%93+Offenlegung+der+Eigenmittel+und+der+Liquidit%C3%A4t+per+31.12.2022.pdf",
    "valiant-offenlegungsbericht-2023.pdf": "https://www.valiant.ch/documents/35003/7353422/Valiant+Holding+AG+%E2%80%93+Offenlegung+der+Eigenmittel+und+der+Liquidit%C3%A4t+per+31.12.2023.pdf",
    "valiant-offenlegungsbericht-2024.pdf": "https://www.valiant.ch/documents/35003/11907684/Valiant+Holding+AG+%E2%80%93+Offenlegung+der+Eigenmittel+und+der+Liquidit%C3%A4t+per+31.12.2024.pdf",
    "valiant-offenlegungsbericht-2025.pdf": "https://www.valiant.ch/documents/35003/13184863/Valiant+Holding+AG+%E2%80%93+Regulatorische+Offenlegung+per+31.12.2025.pdf",
    "valiant-offenlegungsbericht-06-2026.pdf": "https://www.valiant.ch/documents/35003/13319974/Valiant+Holding+AG+%E2%80%93+Offenlegung+der+Eigenmittel+und+der+Liquidit%C3%A4t+per+30.+Juni+2026.pdf",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Download Valiant Holding AG PDF reports.")
    parser.add_argument("--force", action="store_true", help="Re-download existing PDFs")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force, sleep_sec=0.5)


if __name__ == "__main__":
    main()
