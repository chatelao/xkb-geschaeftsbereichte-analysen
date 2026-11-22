#!/usr/bin/env python3
"""Basellandschaftliche Kantonalbank (BLKB) Berichte Downloader (2007–2025)."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from shared.download_utils import download_catalog  # noqa: E402

CATALOG: dict[str, str | list[str]] = {
    # Finanzteile / Jahresrechnungen (2007–2018) & Geschäftsberichte (2019–2025)
    "blkb-geschaeftsbericht-2007.pdf": "https://www.blkb.ch/dam/pdf/archiv/2007/de/geschaeftsbericht-2007-finanzteil-deutsch.pdf",
    "blkb-geschaeftsbericht-2008.pdf": "https://www.blkb.ch/dam/pdf/archiv/2008/de/blkb_gb08_de_finanzteil.pdf",
    "blkb-geschaeftsbericht-2009.pdf": "https://www.blkb.ch/dam/pdf/archiv/2009/de/blkb_gb09_de_finanzteil.pdf",
    "blkb-geschaeftsbericht-2010.pdf": "https://www.blkb.ch/dam/pdf/archiv/2010/de/blkb_gb_2010_de_finanzteil.pdf",
    "blkb-geschaeftsbericht-2011.pdf": "https://www.blkb.ch/dam/pdf/archiv/2011/de/blkb_gb_2011_finanzbericht.pdf",
    "blkb-geschaeftsbericht-2013.pdf": "https://www.blkb.ch/dam/pdf/archiv/2013/de/blkb_gb13_finanzbericht.pdf",
    "blkb-geschaeftsbericht-2014.pdf": "https://www.blkb.ch/dam/pdf/archiv/2014/de/BLKB_GB14_Bilanz.pdf",
    "blkb-geschaeftsbericht-2016.pdf": "https://www.blkb.ch/dam/pdf/archiv/2016/de/BLKB_GB16_Jahresrechnung.pdf",
    "blkb-geschaeftsbericht-2017.pdf": "https://www.blkb.ch/dam/pdf/archiv/2017/de/BLKB_GB17_Jahresrechnung.pdf",
    "blkb-geschaeftsbericht-2018.pdf": "https://www.blkb.ch/dam/pdf/archiv/2018/de/BLKB_GB18_Jahresrechnung.pdf",
    "blkb-geschaeftsbericht-2019.pdf": "https://www.blkb.ch/dam/pdf/berichte/2019/de/BLKB_GB19_DE.pdf",
    "blkb-geschaeftsbericht-2020.pdf": "https://www.blkb.ch/dam/pdf/berichte/2020/de/BLKB_Geschaeftsbericht_2020_DE.pdf",
    "blkb-geschaeftsbericht-2021.pdf": "https://www.blkb.ch/dam/pdf/berichte/2021/BLKB_Geschaeftsbericht_2021.pdf",
    "blkb-geschaeftsbericht-2022.pdf": "https://www.blkb.ch/dam/pdf/berichte/2022/BLKB_Gesch-ftsbericht-2022-Stammhaus_Jahresrechnung.pdf",
    "blkb-geschaeftsbericht-2023.pdf": "https://www.blkb.ch/dam/pdf/berichte/2023/BLKB_Gesch-ftsbericht_2023_Jahresrechnung_Konzern.pdf",
    "blkb-geschaeftsbericht-2024.pdf": "https://www.blkb.ch/dam/pdf/berichte/2024/BLKB_Geschaeftsbericht_2024.pdf",
    "blkb-geschaeftsbericht-2025.pdf": "https://www.blkb.ch/dam/pdf/berichte/2025/BLKB_Geschaeftsbericht_2025.pdf",
    # Offenlegungsberichte (Pillar 3)
    "blkb-offenlegungsbericht-2014.pdf": "https://www.blkb.ch/dam/pdf/archiv/2014/de/GB14_Offenlegung.pdf",
    "blkb-offenlegungsbericht-2015.pdf": "https://www.blkb.ch/dam/pdf/archiv/2015/de/BLKB_15_Offenlegung_der_Eigenmittel.pdf",
    "blkb-offenlegungsbericht-2016.pdf": "https://www.blkb.ch/dam/pdf/archiv/2016/de/BLKB_GB16_Offenlegung.pdf",
    "blkb-offenlegungsbericht-2017.pdf": "https://www.blkb.ch/dam/pdf/archiv/2017/de/BLKB_GB17_Offenlegung.pdf",
    "blkb-offenlegungsbericht-2018.pdf": "https://www.blkb.ch/dam/pdf/archiv/2018/de/BLKB_GB18_Offenlegung.pdf",
    "blkb-offenlegungsbericht-2020.pdf": "https://www.blkb.ch/dam/pdf/berichte/2020/de/BLKB_Offenlegung-2020.pdf",
    "blkb-offenlegungsbericht-2021.pdf": "https://www.blkb.ch/dam/pdf/berichte/2021/de/Offenlegung_2021_de_final.pdf",
    "blkb-offenlegungsbericht-06-2022.pdf": "https://www.blkb.ch/dam/pdf/berichte/2022/Offenlegung-HJ22_final.pdf",
    "blkb-offenlegungsbericht-2023.pdf": "https://www.blkb.ch/dam/pdf/berichte/2023/BLKB_Offenlegung-2023.pdf",
    "blkb-offenlegungsbericht-2024.pdf": "https://www.blkb.ch/dam/pdf/berichte/2024/BLKB_Offenlegung_2024.pdf",
    "blkb-offenlegungsbericht-2025.pdf": "https://www.blkb.ch/dam/pdf/berichte/2025/BLKB_Offenlegung_2025.pdf",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Download BLKB PDF reports.")
    parser.add_argument("--force", action="store_true", help="Re-download existing PDFs")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force, sleep_sec=0.5)


if __name__ == "__main__":
    main()
