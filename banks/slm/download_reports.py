#!/usr/bin/env python3
"""Download annual, half-year, and disclosure PDF reports for Bank SLM AG (slm)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from shared.download_utils import download_catalog  # noqa: E402

CATALOG: dict[str, str] = {
    "slm-geschaeftsbericht-2012.pdf": "https://bankslm.ch/app/uploads/2017/07/Geschaeftsbericht_2012.pdf",
    "slm-geschaeftsbericht-2013.pdf": "https://bankslm.ch/app/uploads/2017/07/Gesch%C3%A4ftsbericht_2013.pdf",
    "slm-geschaeftsbericht-2014.pdf": "https://bankslm.ch/app/uploads/2017/07/Gesch%C3%A4ftsbericht_2014.pdf",
    "slm-geschaeftsbericht-2015.pdf": "https://bankslm.ch/app/uploads/2017/07/Geschaeftsbericht2015.pdf",
    "slm-geschaeftsbericht-2016.pdf": "https://bankslm.ch/app/uploads/2017/07/slm_GB_2016_Langversion_web01-1.pdf",
    "slm-geschaeftsbericht-2017.pdf": "https://bankslm.ch/app/uploads/2018/03/Gesch%C3%A4ftsbericht-2017.pdf",
    "slm-geschaeftsbericht-2018.pdf": "https://bankslm.ch/app/uploads/2019/03/slm_GB_2018_Langversion_web02_es.pdf",
    "slm-geschaeftsbericht-2019.pdf": "https://bankslm.ch/app/uploads/2020/03/slm_GB_2019_Langversion_web01.pdf",
    "slm-geschaeftsbericht-2020.pdf": "https://bankslm.ch/app/uploads/2021/03/slm_GB_2020_Langversion_web01.pdf",
    "slm-geschaeftsbericht-2021.pdf": "https://bankslm.ch/app/uploads/2022/03/slm_GB_2021_Langversion_web01.pdf",
    "slm-geschaeftsbericht-2022.pdf": "https://bankslm.ch/app/uploads/2023/03/slm_GB_2022_Langversion_web03.pdf",
    "slm-geschaeftsbericht-2023.pdf": "https://bankslm.ch/app/uploads/2024/03/slm_GB_2023_Langversion_web01.pdf",
    "slm-geschaeftsbericht-2024.pdf": "https://bankslm.ch/app/uploads/2025/03/slm_GB_2024_Langversion_web01.pdf",
    "slm-geschaeftsbericht-2025.pdf": "https://bankslm.ch/app/uploads/2026/03/slm_GB_2025_Langversion_web.pdf",
    "slm-semesterbericht-2021.pdf": "https://bankslm.ch/app/uploads/2021/09/Geschaeftsbericht_30.06.2021.pdf",
    "slm-semesterbericht-2022.pdf": "https://bankslm.ch/app/uploads/2017/05/Halbjahresabschluss-2022.pdf",
    "slm-semesterbericht-2024.pdf": "https://bankslm.ch/app/uploads/2017/05/Geschaeftsbericht-Halbjahresabschluss-2024.pdf",
    "slm-semesterbericht-2025.pdf": "https://bankslm.ch/app/uploads/2025/08/Geschaeftsbericht_30.06.2025.pdf",
    "slm-offenlegungsbericht-2020.pdf": "https://bankslm.ch/app/uploads/2021/02/slm_Offenlegung_2020_web.pdf",
    "slm-offenlegungsbericht-2021.pdf": "https://bankslm.ch/app/uploads/2023/03/slm_Offenlegung_2021_ew01.pdf",
    "slm-offenlegungsbericht-2022.pdf": "https://bankslm.ch/app/uploads/2023/03/slm_Offenlegung_31.12.2022_rz02_web-1.pdf",
    "slm-offenlegungsbericht-2023.pdf": "https://bankslm.ch/app/uploads/2024/03/slm_Offenlegung_31.12.2023_web01.pdf",
    "slm-offenlegungsbericht-2024.pdf": "https://bankslm.ch/app/uploads/2025/03/slm_Offenlegung_2024_web02.pdf",
    "slm-offenlegungsbericht-2025.pdf": "https://bankslm.ch/app/uploads/2026/08/Offenlegung-31.12.2025.pdf",
    "slm-offenlegungsbericht-06-2026.pdf": "https://bankslm.ch/app/uploads/2026/08/slm_Offenlegung_01.06.2026_web.pdf",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Lädt PDF-Berichte der Bank SLM AG.")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force)


if __name__ == "__main__":
    main()
