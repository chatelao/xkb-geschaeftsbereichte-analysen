#!/usr/bin/env python3
"""St.Galler Kantonalbank AG (SGKB) Berichte Downloader (2018–2026)."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from shared.download_utils import download_catalog  # noqa: E402

CATALOG: dict[str, str | list[str]] = {
    # Geschäftsberichte (2018–2025)
    "sgkb-geschaeftsbericht-2018.pdf": "https://www.sgkb.ch/.dam/ec945333-50c3-4c46-a68b-3cef1fc993d8/SGKB-Geschaeftsbericht-2018.pdf",
    "sgkb-geschaeftsbericht-2019.pdf": "https://www.sgkb.ch/.dam/f2815456-1c25-4f30-8c31-e6b7d3e179d8/sgkb-geschaeftsbericht2019.pdf",
    "sgkb-geschaeftsbericht-2020.pdf": "https://www.sgkb.ch/.dam/d77a8196-d91c-4bbe-a2d2-065089d8ad3e/SGKB-Geschaeftsbericht-2020_1.pdf",
    "sgkb-geschaeftsbericht-2021.pdf": "https://www.sgkb.ch/.dam/cbb779d5-3c68-4377-895e-40ac95dafeb5/SGKB-Geschaeftsbericht2021.pdf",
    "sgkb-geschaeftsbericht-2022.pdf": "https://www.sgkb.ch/.dam/5372ea71-d9c0-4df0-104c-08db19b798a0/SGKB-Geschaeftsbericht-2022.pdf",
    "sgkb-geschaeftsbericht-2023.pdf": "https://www.sgkb.ch/.dam/9a6bb5d6-1ce5-4458-980d-5ae8eda813ba/SGKB-Geschaeftsbericht-2023.pdf",
    "sgkb-geschaeftsbericht-2024.pdf": "https://www.sgkb.ch/.dam/771da17f-8f03-4073-91cb-62a5647572ba/SGKB-Geschaeftsbericht-2024.pdf",
    "sgkb-geschaeftsbericht-2025.pdf": "https://www.sgkb.ch/.dam/814f346b-7f11-49a0-af0c-b0f05eafeca5/SGKB-Geschaeftsbericht-2025.pdf",
    # Semesterberichte / Zwischenabschlüsse
    "sgkb-semesterbericht-2022.pdf": "https://www.sgkb.ch/.dam/dd43f5a9-7456-423c-2ad1-08da9638c53b/SGKB-Zwischenabschluss-FINMA-Q22022.pdf",
    "sgkb-semesterbericht-2025.pdf": "https://www.sgkb.ch/.dam/4697c251-345c-40ab-b3c0-1b36489e1d84/hy2025-zwischenabschluss-sgkb.pdf",
    "sgkb-semesterbericht-2026.pdf": "https://www.sgkb.ch/.dam/90950727-9b1c-4603-b2bd-db539be1d4e3/hy2026-zwischenabschluss-sgkb.pdf",
    # Aufsichtsrechtliche Offenlegung (Pillar 3)
    "sgkb-offenlegungsbericht-06-2023.pdf": "https://www.sgkb.ch/.dam/0fad080d-1b6c-4318-411c-08db9f38087e/SGKB_Offenlegung_HJB_2023_20230726.pdf",
    "sgkb-offenlegungsbericht-2024.pdf": "https://www.sgkb.ch/.dam/287bc7c4-26ef-4590-83b8-6060df95783b/sgkb-aufsichtsrechtliche-offenlegung-2024-12.pdf",
    "sgkb-offenlegungsbericht-2025.pdf": "https://www.sgkb.ch/.dam/4102b856-81d9-4e07-9b70-119c9270b4d2/sgkb-aufsichtsrechtliche-offenlegung-2025-12.pdf",
    "sgkb-offenlegungsbericht-06-2026.pdf": "https://www.sgkb.ch/.dam/e45f43e6-7d5a-4411-b850-c40f8bff36e3/sgkb-aufsichtsrechtliche-offenlegung-2026-06.pdf",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Download SGKB PDF reports.")
    parser.add_argument("--force", action="store_true", help="Re-download existing PDFs")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force, sleep_sec=0.5)


if __name__ == "__main__":
    main()
