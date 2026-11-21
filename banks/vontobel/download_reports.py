#!/usr/bin/env python3
"""Download annual, half-year, and disclosure PDF reports for Vontobel Holding AG (vontobel)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from shared.download_utils import download_catalog  # noqa: E402

CATALOG: dict[str, str] = {
    "vontobel-geschaeftsbericht-2020.pdf": "https://www.vontobel.com/siteassets/about-vontobel/investor-relations/reports--presentations/2020/ar/2021-02-11_fr_full-year-report_en.pdf",
    "vontobel-geschaeftsbericht-2024.pdf": "https://www.vontobel.com/siteassets/about-vontobel/investor-relations/reports--presentations/2024/fyr/full-year-report-2024_en-mjayntaymdc.pdf",
    "vontobel-geschaeftsbericht-2025.pdf": "https://www.vontobel.com/siteassets/about-vontobel/investor-relations/reports--presentations/2025/fyr/full-year-report-2025_en-mjaynjaymdy.pdf",
    "vontobel-semesterbericht-2023.pdf": "https://www.vontobel.com/siteassets/about-vontobel/investor-relations/reports--presentations/2023/hyr/2023-07-27_hyr2023_half-year-report_en.pdf",
    "vontobel-semesterbericht-2024.pdf": "https://www.vontobel.com/siteassets/about-vontobel/investor-relations/reports--presentations/2024/hyr/half-year-report-2024_en-mjaynda3mjy.pdf",
    "vontobel-semesterbericht-2025.pdf": "https://www.vontobel.com/siteassets/about-vontobel/investor-relations/reports--presentations/2025/hyr/half-year-report-2025_en-mjaynta3mjq.pdf",
    "vontobel-semesterbericht-2026.pdf": "https://www.vontobel.com/siteassets/about-vontobel/investor-relations/reports--presentations/2026/hyr/hyr2026-halfyear-report_en-mjaynja3mjq.pdf",
    "vontobel-offenlegungsbericht-2023.pdf": "https://www.vontobel.com/siteassets/about-vontobel/investor-relations/reports--presentations/2023/bvt_disclosure-report-2023_en.pdf",
    "vontobel-offenlegungsbericht-2024.pdf": "https://www.vontobel.com/siteassets/about-vontobel/investor-relations/reports--presentations/2024/disclosure-report-2024_en_final-1.pdf",
    "vontobel-offenlegungsbericht-2025.pdf": "https://www.vontobel.com/siteassets/about-vontobel/investor-relations/reports--presentations/2025/fyr/disclosures_vontobel_fy2025.pdf",
    "vontobel-offenlegungsbericht-06-2025.pdf": "https://www.vontobel.com/siteassets/about-vontobel/investor-relations/reports--presentations/2025/hyr/disclosures_vontobel_hy2025.pdf",
    "vontobel-offenlegungsbericht-06-2026.pdf": "https://www.vontobel.com/siteassets/about-vontobel/investor-relations/reports--presentations/2026/hyr/disclosures_vontobel_hy2026.pdf",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Lädt PDF-Berichte von Vontobel.")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force)


if __name__ == "__main__":
    main()
