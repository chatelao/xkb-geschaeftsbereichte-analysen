#!/usr/bin/env python3
"""Download annual and appendix PDF reports for AEK BANK 1826 (aek)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from shared.download_utils import download_catalog  # noqa: E402

CATALOG: dict[str, str] = {
    "aek-geschaeftsbericht-2016.pdf": "https://www.aekbank.ch/dam/jcr:7760ae7e-ca5d-40cc-a93a-221be6ce9d4a/Geschaeftsbericht_2016.2022-04-12-15-33-44.pdf",
    "aek-geschaeftsbericht-2016-anhang.pdf": "https://www.aekbank.ch/dam/jcr:f51b579c-d4c2-4bc7-8e0d-e62d81a24bd7/Geschaeftsbericht_Anhang_2016.2022-04-12-15-33-57.pdf",
    "aek-geschaeftsbericht-2017.pdf": "https://www.aekbank.ch/dam/jcr:1ffd3dad-ce10-482e-9eb5-1f8c2e901905/Geschaeftsbericht_2017.2022-04-12-15-34-38.pdf",
    "aek-geschaeftsbericht-2017-anhang.pdf": "https://www.aekbank.ch/dam/jcr:841b7125-4586-430e-82f0-65969d3a18bc/Geschaeftsbericht_Anhang_2017.2022-04-12-15-34-50.pdf",
    "aek-geschaeftsbericht-2018.pdf": "https://www.aekbank.ch/dam/jcr:5a8a92fa-614a-4ed7-964a-e76a80bdf7da/Gechaeftsbericht_2018.2022-04-12-15-34-56.pdf",
    "aek-geschaeftsbericht-2018-anhang.pdf": "https://www.aekbank.ch/dam/jcr:2cc7602f-90d6-4945-84d6-096e74033b9a/Gechaeftsbericht_Anhang_2018.2022-04-12-15-35-05.pdf",
    "aek-geschaeftsbericht-2019.pdf": "https://www.aekbank.ch/dam/jcr:d5d714ad-343a-4540-bf8f-3328ef55c206/Geschaeftsbericht_2019.2022-04-12-15-35-11.pdf",
    "aek-geschaeftsbericht-2019-anhang.pdf": "https://www.aekbank.ch/dam/jcr:4c261c24-54eb-4fd1-9d1e-a74891194c35/Geschaeftsbericht_Anhang_2019.2022-04-12-15-35-18.pdf",
    "aek-geschaeftsbericht-2020.pdf": "https://www.aekbank.ch/dam/jcr:82a45cde-b385-495d-8786-08947d3d5818/Geschaeftsbericht_2020.2022-04-12-15-35-23.pdf",
    "aek-geschaeftsbericht-2020-anhang.pdf": "https://www.aekbank.ch/dam/jcr:e6a190c2-90bd-43c4-888e-2cb42b789eae/Geschaeftsbericht_Anhang_2020.2022-04-12-15-35-36.pdf",
    "aek-geschaeftsbericht-2021.pdf": "https://www.aekbank.ch/dam/jcr:14146b35-5e57-4ad1-b2d0-a3a96efbcc6d/Gesch%C3%A4ftsbericht_2021.2022-04-12-15-35-44.pdf",
    "aek-geschaeftsbericht-2021-anhang.pdf": "https://www.aekbank.ch/dam/jcr:a5582ac7-5129-4563-a399-49d71d936a22/Gesch%C3%A4ftsbericht_Anhang_2021.2022-04-12-15-35-52.pdf",
    "aek-geschaeftsbericht-2022.pdf": "https://www.aekbank.ch/dam/jcr:2752dd56-8cc6-4532-a239-794ab989ee01/Gesch%C3%A4ftsbericht_2022.2023-02-17-08-13-39.pdf",
    "aek-geschaeftsbericht-2022-anhang.pdf": "https://www.aekbank.ch/dam/jcr:d7078fb5-71d0-4486-838e-7708a28d512d/Gesch%C3%A4ftsbericht_2022_Anhang.2023-02-17-08-13-35.pdf",
    "aek-geschaeftsbericht-2023.pdf": "https://www.aekbank.ch/dam/jcr:5c46da5a-bbe9-4d2e-9064-f620bad52c47/Gesch%C3%A4ftsbericht_2023.2024-02-15-09-25-39.pdf",
    "aek-geschaeftsbericht-2023-anhang.pdf": "https://www.aekbank.ch/dam/jcr:c40a4b29-d7de-4bf2-810e-7e11dd6bbcf4/Gesch%C3%A4ftsbericht_2023_Anhang.2024-02-15-09-25-42.pdf",
    "aek-geschaeftsbericht-2024.pdf": "https://www.aekbank.ch/dam/jcr:e85663d9-4c58-4244-b062-7df8e9e05858/Gesch%C3%A4ftsbericht_2024.2025-03-03-10-53-09.pdf",
    "aek-geschaeftsbericht-2024-anhang.pdf": "https://www.aekbank.ch/dam/jcr:0ffb636a-abeb-452a-992a-762cceb1a0c1/Gesch%C3%A4ftsbericht_Anhang_2024.2025-02-14-11-01-06.pdf",
    "aek-geschaeftsbericht-2025.pdf": "https://www.aekbank.ch/dam/jcr:21899c29-26ba-4d33-9e0a-3f8e3a4c9207/Gesch%C3%A4ftsbericht_2025.2026-02-11-08-02-41.pdf",
    "aek-geschaeftsbericht-2025-anhang.pdf": "https://www.aekbank.ch/dam/jcr:7eace410-cac3-4cb5-be08-55e2787261d8/Gesch%C3%A4ftsbericht_Anhang_2025.2026-02-11-08-02-38.pdf",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Lädt PDF-Berichte der AEK BANK 1826.")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force)


if __name__ == "__main__":
    main()
