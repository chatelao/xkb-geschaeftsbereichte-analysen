#!/usr/bin/env python3
"""Download annual and half-year PDF reports for Ersparniskasse Speicher (eks)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from shared.download_utils import download_catalog  # noqa: E402

CATALOG: dict[str, str] = {
    "eks-geschaeftsbericht-2007.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2018/12/EKS_Geschaeftsbericht_2009.pdf",
    "eks-geschaeftsbericht-2008.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2018/12/EKS_Geschaeftsbericht_2008.pdf",
    "eks-geschaeftsbericht-2009.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2018/12/Jahresbericht_09-10.pdf",
    "eks-geschaeftsbericht-2010.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2018/12/EKS_Geschaeftsbericht_2010.pdf",
    "eks-geschaeftsbericht-2011.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2018/12/EKS_Geschaeftsbericht_2011.pdf",
    "eks-geschaeftsbericht-2012.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2018/12/EKS_Geschaeftsbericht_2012.pdf",
    "eks-geschaeftsbericht-2013.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2018/12/EKS_Geschaeftsbericht_2013.pdf",
    "eks-geschaeftsbericht-2014.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2018/12/EKS_Geschaeftsbericht_2014.pdf",
    "eks-geschaeftsbericht-2015.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2018/12/EKS_Geschaeftsbericht_2015.pdf",
    "eks-geschaeftsbericht-2016.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2018/12/EKS_Geschaeftsbericht_2016.pdf",
    "eks-geschaeftsbericht-2017.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2018/08/Jahresbericht_eks_2017_Web.pdf",
    "eks-geschaeftsbericht-2018.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2019/02/Jahresbericht_eks_2018_low.pdf",
    "eks-geschaeftsbericht-2019.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2020/03/Jahresbericht_eks_2019.pdf",
    "eks-geschaeftsbericht-2020.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2021/02/Jahresbericht_eks_2020.pdf",
    "eks-geschaeftsbericht-2021.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2022/02/Jahresbericht_eks_2021_v6_final.pdf",
    "eks-geschaeftsbericht-2022.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2023/02/Jahresbericht_eks_2022_PDF.pdf",
    "eks-geschaeftsbericht-2023.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2024/03/Geschaeftsbericht-2023.pdf",
    "eks-geschaeftsbericht-2024.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2025/02/Jahresbericht-2024.pdf",
    "eks-geschaeftsbericht-2025.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2026/02/Jahresbericht_2025_Web.pdf",
    "eks-semesterbericht-2020.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2020/07/EkS_Halbjahresabschluss_2020_V1.pdf",
    "eks-semesterbericht-2021.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2021/07/EkS_Halbjahresabschluss_2021_V1.pdf",
    "eks-semesterbericht-2022.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2022/07/EkS_Halbjahresabschluss_2022.pdf",
    "eks-semesterbericht-2023.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2023/07/EkS_Halbjahresabschluss_2023.pdf",
    "eks-semesterbericht-2024.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2024/08/EkS_Halbjahresabschluss_2024.pdf",
    "eks-semesterbericht-2025.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2025/07/Halbjahresabschluss_2025-1.pdf",
    "eks-semesterbericht-2026.pdf": "https://www.ersparniskassespeicher.ch/wp-content/uploads/2026/08/Halbjahresabschluss-2026.pdf",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Lädt PDF-Berichte der Ersparniskasse Speicher.")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force)


if __name__ == "__main__":
    main()
