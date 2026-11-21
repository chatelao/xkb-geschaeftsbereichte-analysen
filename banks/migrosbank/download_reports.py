#!/usr/bin/env python3
"""Download annual and half-year PDF reports for Migros Bank AG (migrosbank)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from shared.download_utils import download_catalog  # noqa: E402

CATALOG: dict[str, str] = {
    "migrosbank-geschaeftsbericht-2010.pdf": "https://www.migrosbank.ch/dam/jcr:a5a02a07-b3b1-486b-86e2-a8455d33139f/geschaeftsbericht-2010.2014-03-11-14-14-36.pdf",
    "migrosbank-geschaeftsbericht-2011.pdf": "https://www.migrosbank.ch/dam/jcr:c96274a7-0f1c-4835-9cb3-4ae942798fc7/geschaeftsbericht-2011.2014-03-11-14-14-54.pdf",
    "migrosbank-geschaeftsbericht-2012.pdf": "https://www.migrosbank.ch/dam/jcr:ed3671c5-0bbf-4464-9da0-b6f21148ebe4/geschaeftsbericht-2012.2014-03-11-14-15-11.pdf",
    "migrosbank-geschaeftsbericht-2013.pdf": "https://www.migrosbank.ch/dam/jcr:d136b4ce-cbe3-4fd3-9675-a88247106597/geschaeftsbericht-2013.2014-03-11-14-15-28.pdf",
    "migrosbank-geschaeftsbericht-2014.pdf": "https://www.migrosbank.ch/dam/jcr:b4be9fcd-8068-4c60-8490-2adce7872813/geschaeftsbericht-2014.2020-08-19-13-16-07.pdf",
    "migrosbank-geschaeftsbericht-2015.pdf": "https://www.migrosbank.ch/dam/jcr:7deded5d-3633-49c7-9ccf-6a6002aea850/geschaeftsbericht-2015.2020-08-19-13-16-15.pdf",
    "migrosbank-geschaeftsbericht-2016.pdf": "https://www.migrosbank.ch/dam/jcr:a1dec5b8-5141-4b3c-a373-06f14f4b8ea2/geschaeftsbericht-2016.2020-08-19-13-16-30.PDF",
    "migrosbank-geschaeftsbericht-2017.pdf": "https://www.migrosbank.ch/dam/jcr:a0c55a7e-ed4f-4d2b-b6f0-d03d78917f11/geschaeftsbericht-2017.2020-08-19-13-16-42.pdf",
    "migrosbank-geschaeftsbericht-2018.pdf": "https://www.migrosbank.ch/dam/jcr:c52c353a-9e79-4a1c-af35-44442bdc2b7f/geschaeftsbericht-2018.2020-08-19-13-17-06.pdf",
    "migrosbank-geschaeftsbericht-2019.pdf": "https://www.migrosbank.ch/dam/jcr:df7c024e-742a-403c-a853-93a349423976/geschaeftsbericht-2019.2020-08-19-13-21-01.pdf",
    "migrosbank-geschaeftsbericht-2020.pdf": "https://www.migrosbank.ch/dam/jcr:968ce065-374a-4836-b957-37eb4825df44/geschaeftsbericht-2020.2021-03-30-09-37-13.pdf",
    "migrosbank-geschaeftsbericht-2021.pdf": "https://www.migrosbank.ch/dam/jcr:582640cf-5762-4091-9dc8-c8916527db17/GzD_363411_Geschaeftsbericht_2021_DE.2022-04-07-07-59-24.pdf",
    "migrosbank-geschaeftsbericht-2022.pdf": "https://www.migrosbank.ch/dam/jcr:e1e13b31-7970-43f8-8bab-a0c56947490f/GzD_380247_Geschaeftsbericht_2022_DE_V27.2023-04-04-16-53-27.pdf",
    "migrosbank-geschaeftsbericht-2023.pdf": "https://www.migrosbank.ch/dam/jcr:250ab837-87cc-4a9f-9e7b-a05047182504/GzD_390168_Geschaeftsbericht_2023_DE.2024-04-10-10-08-53.pdf",
    "migrosbank-geschaeftsbericht-2024.pdf": "https://www.migrosbank.ch/dam/jcr:65c52e0c-57f9-4cd5-821e-6c07c8153145/geschaeftsbericht-2024.2025-03-11-19-24-15.pdf",
    "migrosbank-geschaeftsbericht-2025.pdf": "https://www.migrosbank.ch/dam/jcr:8e369fc6-4534-4cc2-aada-f848e22c6b17/geschaeftsbericht-2025.2026-03-17-10-03-18.pdf",
    "migrosbank-semesterbericht-2023.pdf": "https://www.migrosbank.ch/dam/jcr:519b774e-acf0-452d-b48f-910aa07f7392/halbjahresbericht-2023.2023-08-23-00-29-47.pdf",
    "migrosbank-semesterbericht-2024.pdf": "https://www.migrosbank.ch/dam/jcr:9ca6ef5f-d6c9-4933-9f7d-2521958e321e/halbjahresbericht-2024.2024-08-26-22-30-45.pdf",
    "migrosbank-semesterbericht-2025.pdf": "https://www.migrosbank.ch/dam/jcr:6a69900a-c414-4097-80a3-0481d5112574/halbjahresbericht-2025-2.2025-08-26-05-58-04.pdf",
    "migrosbank-semesterbericht-2026.pdf": "https://www.migrosbank.ch/dam/jcr:268f3321-782c-41c1-96b3-c0a10c51258c/halbjahresbericht-2026_2.9c05c29ea6bf38f072a3a00ef35e5865.pdf",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Lädt PDF-Berichte der Migros Bank AG.")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force)


if __name__ == "__main__":
    main()
