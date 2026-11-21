#!/usr/bin/env python3
"""Download annual and half-year PDF reports for Pictet Group (pictet)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from shared.download_utils import download_catalog  # noqa: E402

CATALOG: dict[str, str] = {
    "pictet-geschaeftsbericht-2018.pdf": "https://www.pictet.com/content/dam/www/documents/publications/annual-review/Pictet-AnnualReport-2018-EN.pdf.coredownload.pdf",
    "pictet-geschaeftsbericht-2019.pdf": "https://www.pictet.com/content/dam/www/documents/publications/annual-review/Pictet-AR2019-Financial-annual-report-EN.pdf.coredownload.pdf",
    "pictet-geschaeftsbericht-2021.pdf": "https://www.pictet.com/content/dam/www/documents/publications/annual-review/Pictet-Group_Annual-report-2021-EN.pdf.coredownload.pdf",
    "pictet-geschaeftsbericht-2022.pdf": "https://www.pictet.com/content/dam/www/documents/publications/financial-reports/Pictet%20Group%20-%202022%20Annual%20Report.pdf.coredownload.pdf",
    "pictet-geschaeftsbericht-2023.pdf": "https://www.pictet.com/content/dam/www/documents/publications/financial-reports/PictetGroup-2023-Annual-Report.pdf.coredownload.pdf",
    "pictet-geschaeftsbericht-2024.pdf": "https://www.pictet.com/content/dam/www/documents/publications/financial-reports/PictetGroup-2024-Annual-Report.pdf.coredownload.pdf",
    "pictet-geschaeftsbericht-2025.pdf": "https://www.pictet.com/content/dam/www/documents/publications/financial-reports/PictetGroup-2025-Annual-Report.pdf.coredownload.pdf",
    "pictet-semesterbericht-2025.pdf": "https://www.pictet.com/content/dam/www/documents/publications/annual-review/2025/PictetGroup-2025-half-year-financial-report-EN.pdf.coredownload.pdf",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Lädt PDF-Berichte der Pictet Gruppe.")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force)


if __name__ == "__main__":
    main()
