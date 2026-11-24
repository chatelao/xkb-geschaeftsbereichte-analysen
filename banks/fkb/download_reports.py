#!/usr/bin/env python3
"""Freiburger Kantonalbank (FKB / BCF) Berichte Downloader (2015–2026)."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from shared.download_utils import download_catalog  # noqa: E402

CATALOG: dict[str, str | list[str]] = {
    # Geschäftsberichte (2015–2025)
    "fkb-geschaeftsbericht-2015.pdf": "https://www.bcf.ch/sites/default/files/fkb-geschaeftsbericht-2015.pdf",
    "fkb-geschaeftsbericht-2016.pdf": "https://www.bcf.ch/sites/default/files/documents/news/fkb-geschaeftsbericht-2016.pdf",
    "fkb-geschaeftsbericht-2017.pdf": "https://www.bcf.ch/sites/default/files/documents/news/fkb-geschaeftsbericht-2017.pdf",
    "fkb-geschaeftsbericht-2018.pdf": "https://www.bcf.ch/sites/default/files/documents/news/fkb-geschaeftsbericht-2018.pdf",
    "fkb-geschaeftsbericht-2019.pdf": "https://www.bcf.ch/sites/default/files/documents/news/fkb-geschaeftsbericht-2019.pdf",
    "fkb-geschaeftsbericht-2020.pdf": "https://www.bcf.ch/sites/default/files/documents/news/fkb-geschaeftsbericht-2020.pdf",
    "fkb-geschaeftsbericht-2021.pdf": "https://www.bcf.ch/sites/default/files/documents/news/fkb-geschaeftsbericht-2021.pdf",
    "fkb-geschaeftsbericht-2022.pdf": "https://www.bcf.ch/sites/default/files/medias/documents/fkb-geschaeftsbericht-2022.pdf",
    "fkb-geschaeftsbericht-2023.pdf": "https://www.bcf.ch/sites/default/files/medias/documents/fkb-geschaeftsbericht-2023.pdf",
    "fkb-geschaeftsbericht-2024.pdf": "https://www.bcf.ch/sites/default/files/medias/documents/fkb-geschaeftsbericht-2024.pdf",
    "fkb-geschaeftsbericht-2025.pdf": "https://www.bcf.ch/sites/default/files/medias/documents/fkb-geschaeftsbericht-2025.pdf",
    # Semesterberichte / Zwischenberichte (2015–2026)
    "fkb-semesterbericht-2015.pdf": "https://www.bcf.ch/sites/default/files/fkb-zwischenbericht-2015.pdf",
    "fkb-semesterbericht-2016.pdf": "https://www.bcf.ch/sites/default/files/fkb-zwischenbericht-2016.pdf",
    "fkb-semesterbericht-2017.pdf": "https://www.bcf.ch/sites/default/files/fkb-zwischenbericht-2017.pdf",
    "fkb-semesterbericht-2018.pdf": "https://www.bcf.ch/sites/default/files/documents/news/rapport-intermediaire-bcf-2018.pdf",
    "fkb-semesterbericht-2019.pdf": "https://www.bcf.ch/sites/default/files/documents/news/rapport-intermediaire-bcf-2019.pdf",
    "fkb-semesterbericht-2020.pdf": "https://www.bcf.ch/sites/default/files/documents/news/fkb-zwischenbericht-2020.pdf",
    "fkb-semesterbericht-2021.pdf": "https://www.bcf.ch/sites/default/files/documents/news/fkb-zwischenbericht-2021.pdf",
    "fkb-semesterbericht-2022.pdf": "https://www.bcf.ch/sites/default/files/documents/news/rapport-intermediaire-bcf-2022.pdf",
    "fkb-semesterbericht-2023.pdf": "https://www.bcf.ch/sites/default/files/medias/documents/fkb-zwischenbericht-2023.pdf",
    "fkb-semesterbericht-2024.pdf": "https://www.bcf.ch/sites/default/files/medias/documents/fkb-zwischenbericht-2024.pdf",
    "fkb-semesterbericht-2025.pdf": "https://www.bcf.ch/sites/default/files/medias/documents/fkb-zwischenbericht-2025.pdf",
    "fkb-semesterbericht-2026.pdf": "https://www.bcf.ch/sites/default/files/medias/documents/fkb-zwischenbericht-2026.pdf",
    # Aufsichtsrechtliche Offenlegung (Pillar 3, 2019–2026)
    "fkb-offenlegungsbericht-06-2019.pdf": "https://www.bcf.ch/sites/default/files/fkb-eigenmittel-300619.pdf",
    "fkb-offenlegungsbericht-2019.pdf": "https://www.bcf.ch/sites/default/files/fkb-eigenmittel-311219.pdf",
    "fkb-offenlegungsbericht-06-2020.pdf": "https://www.bcf.ch/sites/default/files/fkb-eigenmittel-300620.pdf",
    "fkb-offenlegungsbericht-2020.pdf": "https://www.bcf.ch/sites/default/files/fkb-eigenmittel-311220.pdf",
    "fkb-offenlegungsbericht-06-2021.pdf": "https://www.bcf.ch/sites/default/files/fkb-eigenmittel-300621.pdf",
    "fkb-offenlegungsbericht-2021.pdf": "https://www.bcf.ch/sites/default/files/fkb-eigenmittel-311221.pdf",
    "fkb-offenlegungsbericht-06-2022.pdf": "https://www.bcf.ch/sites/default/files/fkb-eigenmittel-300622.pdf",
    "fkb-offenlegungsbericht-2022.pdf": "https://www.bcf.ch/sites/default/files/medias/documents/fkb-eigenmittel-311222.pdf",
    "fkb-offenlegungsbericht-06-2023.pdf": "https://www.bcf.ch/sites/default/files/medias/documents/fkb-eigenmittel-300623.pdf",
    "fkb-offenlegungsbericht-2023.pdf": "https://www.bcf.ch/sites/default/files/medias/documents/fkb-eigenmittel-311223.pdf",
    "fkb-offenlegungsbericht-06-2024.pdf": "https://www.bcf.ch/sites/default/files/medias/documents/fkb-eigenmittel-300624.pdf",
    "fkb-offenlegungsbericht-2024.pdf": "https://www.bcf.ch/sites/default/files/medias/documents/fkb-eigenmittel-311224.pdf",
    "fkb-offenlegungsbericht-06-2025.pdf": "https://www.bcf.ch/sites/default/files/medias/documents/fkb-eigenmittel-300625.pdf",
    "fkb-offenlegungsbericht-2025.pdf": "https://www.bcf.ch/sites/default/files/medias/documents/fkb-eigenmittel-311225.pdf",
    "fkb-offenlegungsbericht-06-2026.pdf": "https://www.bcf.ch/sites/default/files/medias/documents/fkb-eigenmittel-300626.pdf",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Download FKB PDF reports.")
    parser.add_argument("--force", action="store_true", help="Re-download existing PDFs")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force, sleep_sec=0.3)


if __name__ == "__main__":
    main()
