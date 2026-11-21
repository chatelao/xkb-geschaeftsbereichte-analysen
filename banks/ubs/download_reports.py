#!/usr/bin/env python3
"""UBS Group AG Berichte Downloader – lädt verfügbare Annual-, 2Q-Interim- und Pillar-3-Berichte."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from shared.download_utils import download_catalog  # noqa: E402

WB26 = "https://web.archive.org/web/2026id_/"
DAM = "https://www.ubs.com/content/dam/assets/cc/investor-relations"

CATALOG: dict[str, str | list[str]] = {
    # Annual Reports UBS Group AG (2020–2025)
    "ubs-geschaeftsbericht-2020.pdf": "https://gb-rating.fra1.cdn.digitaloceanspaces.com/gb-rating2021/pdf/participants/ubs-group.pdf",
    "ubs-geschaeftsbericht-2021.pdf": f"{WB26}{DAM}/annual-report/2021/full-report-ubs-group-ag-and-ubs-ag-consolidated-2021-en.pdf",
    "ubs-geschaeftsbericht-2022.pdf": f"{WB26}{DAM}/annual-report/2022/full-report-ubs-group-ag-and-ubs-ag-consolidated-2022-en.pdf",
    "ubs-geschaeftsbericht-2023.pdf": f"{WB26}{DAM}/annual-report/2023/files/annual-report-ubs-group-2023.pdf",
    "ubs-geschaeftsbericht-2024.pdf": f"{WB26}{DAM}/annual-report/2024/annual-report-ubs-group-2024.pdf",
    "ubs-geschaeftsbericht-2025.pdf": f"{WB26}{DAM}/annual-report/2025/annual-report-ubs-group-2025.pdf",
    # Interim / Second Quarter Reports (2Q 2022–2025)
    "ubs-semesterbericht-2022.pdf": f"{WB26}{DAM}/quarterlies/2022/2q22/full-report-ubs-group-ag-consolidated-2q22.pdf",
    "ubs-semesterbericht-2023.pdf": f"{WB26}{DAM}/quarterlies/2023/2q23/full-report-ubs-group-ag-consolidated-2q23.pdf",
    "ubs-semesterbericht-2024.pdf": f"{WB26}{DAM}/quarterlies/2024/2q24/full-report-ubs-group-consolidated-2q24.pdf",
    "ubs-semesterbericht-2025.pdf": f"{WB26}{DAM}/quarterlies/2025/2q25/full-report-ubs-group-consolidated-2q25.pdf",
    # Pillar 3 Disclosures (06-2023, FY2023, FY2024, 06-2025)
    "ubs-offenlegungsbericht-06-2023.pdf": f"{WB26}{DAM}/quarterlies/2023/2q23/pillar-3-2q23.pdf",
    "ubs-offenlegungsbericht-2023.pdf": f"{WB26}{DAM}/annual-report/2023/files/annual-report-pillar3-2023.pdf",
    "ubs-offenlegungsbericht-2024.pdf": f"{WB26}{DAM}/annual-report/2024/annual-report-pillar3-2024.pdf",
    "ubs-offenlegungsbericht-06-2025.pdf": f"{WB26}{DAM}/quarterlies/2025/2q25/pillar-3-2q25.pdf",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Download UBS Group AG PDF reports.")
    parser.add_argument("--force", action="store_true", help="Re-download existing PDFs")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force, sleep_sec=1.5)


if __name__ == "__main__":
    main()
