#!/usr/bin/env python3
"""Entris Holding AG (ehem. RBA-Holding AG) Berichte Downloader (2021–2025)."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from shared.download_utils import download_catalog  # noqa: E402

CATALOG: dict[str, str | list[str]] = {
    "entris-geschaeftsbericht-2021.pdf": "https://www.datocms-assets.com/207097/1791977720-entrisholding_gb21_de_20220325.pdf",
    "entris-geschaeftsbericht-2022.pdf": "https://www.datocms-assets.com/207097/1791977683-entrisholding_gb22_20230314_final.pdf",
    "entris-geschaeftsbericht-2023.pdf": "https://www.datocms-assets.com/207097/1791977666-entrisholding_gb23_final_web.pdf",
    "entris-geschaeftsbericht-2024.pdf": "https://www.datocms-assets.com/207097/1791977649-entrisholding_gb24_def.pdf",
    "entris-geschaeftsbericht-2025.pdf": "https://www.datocms-assets.com/207097/1791977630-entrisholding_gb25_final.pdf",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Download Entris Holding AG (RBA-Holding) PDF reports.")
    parser.add_argument("--force", action="store_true", help="Re-download existing PDFs")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force, sleep_sec=0.5)


if __name__ == "__main__":
    main()
