#!/usr/bin/env python3
"""Luzerner Kantonalbank AG (LUKB) Berichte Downloader (2001–2026)."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from shared.download_utils import download_catalog  # noqa: E402

CATALOG: dict[str, str | list[str]] = {
    # Finanzberichte (2001–2016) & Geschäftsberichte (2017–2025)
    "lukb-geschaeftsbericht-2001.pdf": "https://www.lukb.ch/.dam/cd611165-8fcd-45b0-a4b9-8e3467e11ded/LUKB-Finanzbericht-2001.pdf",
    "lukb-geschaeftsbericht-2002.pdf": "https://www.lukb.ch/.dam/e7500679-d55a-4aa0-8128-9e33f83a618e/LUKB-Finanzbericht-2002.pdf",
    "lukb-geschaeftsbericht-2003.pdf": "https://www.lukb.ch/.dam/5261a35a-696f-4ef9-8e0e-9fe1319388b8/LUKB-Finanzbericht-2003.pdf",
    "lukb-geschaeftsbericht-2004.pdf": "https://www.lukb.ch/.dam/907f547f-6ea1-4cb4-95dc-dbec0220db25/LUKB-Finanzbericht-2004.pdf",
    "lukb-geschaeftsbericht-2005.pdf": "https://www.lukb.ch/.dam/bf44f4d3-473e-4c16-bbca-da32634a4582/LUKB-Finanzbericht-2005.pdf",
    "lukb-geschaeftsbericht-2006.pdf": "https://www.lukb.ch/.dam/2aee364d-61b8-4eb2-b083-b66f2d2b6e0e/LUKB-Finanzbericht-2006.pdf",
    "lukb-geschaeftsbericht-2007.pdf": "https://www.lukb.ch/.dam/9a15af34-ccab-49e9-9f44-5b1a2158456b/LUKB-Finanzbericht-2007.pdf",
    "lukb-geschaeftsbericht-2008.pdf": "https://www.lukb.ch/.dam/e922397f-fe93-4881-9f7f-ab5abeb7bb42/LUKB-Finanzbericht-2008.pdf",
    "lukb-geschaeftsbericht-2009.pdf": "https://www.lukb.ch/.dam/832ff87b-b057-464d-a574-f0e4f2eb48fb/LUKB-Finanzbericht-2009_1.pdf",
    "lukb-geschaeftsbericht-2010.pdf": "https://www.lukb.ch/.dam/64e91257-47c1-481f-8e96-58e7f5a80f7d/LUKB-Finanzbericht-2010.pdf",
    "lukb-geschaeftsbericht-2011.pdf": "https://www.lukb.ch/.dam/e5685a8a-e920-4236-a617-06eefe23478a/LUKB-Finanzbericht-2011.pdf",
    "lukb-geschaeftsbericht-2012.pdf": "https://www.lukb.ch/.dam/dc067dc9-ee30-493e-a644-5ae7086fc665/LUKB-Finanzbericht-2012.pdf",
    "lukb-geschaeftsbericht-2013.pdf": "https://www.lukb.ch/.dam/99f1c52f-1349-48d0-b486-b46fe891ab51/LUKB-Finanzbericht-2013.pdf",
    "lukb-geschaeftsbericht-2014.pdf": "https://www.lukb.ch/.dam/e2724c28-2c99-42f6-b75a-978ba1d6adb9/LUKB-Finanzbericht-2014.pdf",
    "lukb-geschaeftsbericht-2015.pdf": "https://www.lukb.ch/.dam/a450f199-27c2-4790-906a-670ec7a203bf/LUKB-Finanzbericht-2015.pdf",
    "lukb-geschaeftsbericht-2016.pdf": "https://www.lukb.ch/.dam/10a80266-bce1-42a6-9737-41ab9341a2ea/LUKB-Finanzbericht-2016.pdf",
    "lukb-geschaeftsbericht-2017.pdf": "https://www.lukb.ch/.dam/54e2c3a2-8d73-43d7-9e29-b636ea19757a/LUKB-Geschaeftsbericht-2017.pdf",
    "lukb-geschaeftsbericht-2018.pdf": "https://www.lukb.ch/.dam/c0c57904-2841-4b62-b038-fef1283c6ed3/LUKB-Geschaeftsbericht-2018.pdf",
    "lukb-geschaeftsbericht-2019.pdf": "https://www.lukb.ch/.dam/a579f55c-3729-4bf8-9a09-4c47b2c871cc/LUKB-Geschaeftsbericht-2019.pdf",
    "lukb-geschaeftsbericht-2020.pdf": "https://www.lukb.ch/.dam/e0190046-6e39-47eb-b87c-1855ef9c8b45/LUKB-Geschaeftsbericht-2020.pdf",
    "lukb-geschaeftsbericht-2021.pdf": "https://www.lukb.ch/.dam/960ada28-cb01-4184-8f05-06208e2c84bb/LUKB-Geschaeftsbericht-2021.pdf",
    "lukb-geschaeftsbericht-2022.pdf": "https://www.lukb.ch/.dam/e819b30d-7041-497a-bbe4-b0a167135df1/LUKB-Geschaeftsbericht-2022.pdf",
    "lukb-geschaeftsbericht-2023.pdf": "https://www.lukb.ch/.dam/0a4b5b2a-05dd-4f91-b801-6e9190e02405/LUKB-Geschaeftsbericht-2023.pdf",
    "lukb-geschaeftsbericht-2024.pdf": "https://www.lukb.ch/.dam/6bc67289-9150-403c-afdf-09d0eb276d56/LUKB-Geschaeftsbericht-2024.pdf",
    "lukb-geschaeftsbericht-2025.pdf": "https://www.lukb.ch/.dam/98099d6c-507b-4681-927d-b2140a88ba51/LUKB-Geschaeftsbericht-2025.pdf",
    # Halbjahresberichte (2025–2026)
    "lukb-semesterbericht-2025.pdf": "https://www.lukb.ch/.dam/fae0e3ac-6df3-4278-b63b-646a12ced553/LUKB-Halbjahresbericht-2025.pdf",
    "lukb-semesterbericht-2026.pdf": "https://www.lukb.ch/.dam/878413b8-f5dd-4b66-b8a2-2543a8fc5391/LUKB-Halbjahresbericht-2026.pdf",
    # Offenlegungsberichte (2017–06/2026)
    "lukb-offenlegungsbericht-2017.pdf": "https://www.lukb.ch/.dam/23e20e12-2591-42aa-9a8e-19c26263f1b5/LUKB-Offenlegungsbericht-2017.pdf",
    "lukb-offenlegungsbericht-2018.pdf": "https://www.lukb.ch/.dam/7c49d1f2-0913-4553-b8f7-b805b3ab5414/LUKB-Offenlegungsbericht-2018.pdf",
    "lukb-offenlegungsbericht-2019.pdf": "https://www.lukb.ch/.dam/bdc302b0-a048-4f33-84d3-91958d0b801c/LUKB-Offenlegungsbericht-2019.pdf",
    "lukb-offenlegungsbericht-2020.pdf": "https://www.lukb.ch/.dam/1b759c55-732b-427c-82c6-592f1f04e2ce/LUKB-Offenlegungsbericht-2020.pdf",
    "lukb-offenlegungsbericht-2021.pdf": "https://www.lukb.ch/.dam/8e9794b9-decc-46dd-9be9-a130c0e161c8/LUKB-Offenlegungsbericht-2021.pdf",
    "lukb-offenlegungsbericht-2022.pdf": "https://www.lukb.ch/.dam/be5a1de7-dcb0-446f-a93d-4c04fea106f5/LUKB-Offenlegungsbericht-2022.pdf",
    "lukb-offenlegungsbericht-2023.pdf": "https://www.lukb.ch/.dam/26e677cd-95b6-44c4-b609-2141ef30188d/LUKB-Offenlegungsbericht-2023.pdf",
    "lukb-offenlegungsbericht-2024.pdf": "https://www.lukb.ch/.dam/d5176f1c-7d12-4c67-bd6d-1772fccc392f/LUKB-Offenlegungsbericht-2024.pdf",
    "lukb-offenlegungsbericht-2025.pdf": "https://www.lukb.ch/.dam/55250631-6623-4ea3-9437-ce6a4c967f64/LUKB-Offenlegungsbericht-2025.pdf",
    "lukb-offenlegungsbericht-06-2026.pdf": "https://www.lukb.ch/.dam/07907fe3-243f-4075-a1ae-927e4a512dec/LUKB-Offenlegungsbericht-HJ26.pdf",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Download LUKB PDF reports.")
    parser.add_argument("--force", action="store_true", help="Re-download existing PDFs")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force, sleep_sec=0.5)


if __name__ == "__main__":
    main()
