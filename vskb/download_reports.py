#!/usr/bin/env python3
"""VSKB (WKB / BCVs) Berichte Downloader – lädt alle verfügbaren Geschäfts-, Semester- und Offenlegungsberichte."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.download_utils import download_catalog  # noqa: E402

BASE = "https://www.bcvs.ch"

CATALOG: dict[str, str | list[str]] = {
    # Geschäftsberichte (2007, 2009–2010, 2014–2025)
    "vskb-geschaeftsbericht-2007.pdf": f"{BASE}/fileadmin/user_upload/site/archives/publications/publications/2007/DE/WKB_Geschaeftsbericht_2007_DE.pdf",
    "vskb-geschaeftsbericht-2009.pdf": f"{BASE}/fileadmin/user_upload/site/archives/publications/publications/2009/DE/WKB_Geschaeftsbericht_2009_DE.pdf",
    "vskb-geschaeftsbericht-2010.pdf": f"{BASE}/fileadmin/user_upload/site/archives/publications/publications/2010/DE/WKB_Geschaeftsbericht_2010_DE.pdf",
    "vskb-geschaeftsbericht-2014.pdf": f"{BASE}/fileadmin/user_upload/site/publications/rapport-gestion/archives/DE/RA2014/Geschaeftsbericht2014WKB.pdf",
    "vskb-geschaeftsbericht-2015.pdf": f"{BASE}/fileadmin/user_upload/site/publications/rapport-gestion/archives/Rapport_annuel/Geschaeftsbericht_2015.pdf",
    "vskb-geschaeftsbericht-2016.pdf": f"{BASE}/fileadmin/user_upload/site/publications/rapport-gestion/archives/Rapport_annuel/Gesch%C3%A4ftsbericht_2016_der_WKB_-_Voll_Version.pdf",
    "vskb-geschaeftsbericht-2017.pdf": f"{BASE}/fileadmin/user_upload/site/publications/rapport-gestion/archives/Rapport_annuel/Gesch%C3%A4ftsbericht_WKB_2017.pdf",
    "vskb-geschaeftsbericht-2018.pdf": f"{BASE}/fileadmin/user_upload/site/publications/rapport-gestion/archives/Rapport_annuel/Gesch%C3%A4ftsbericht_WKB_2018.pdf",
    "vskb-geschaeftsbericht-2019.pdf": f"{BASE}/fileadmin/user_upload/site/publications/rapport-gestion/2019/WEB_Rapport_annuel_BCVs_2019_Allemand.pdf",
    "vskb-geschaeftsbericht-2020.pdf": f"{BASE}/fileadmin/user_upload/site/publications/rapport-gestion/2020/Geschaeftsbericht_WKB_2020.pdf",
    "vskb-geschaeftsbericht-2021.pdf": f"{BASE}/fileadmin/user_upload/site/publications/rapport-gestion/2021/WKB_Geschaeftsbericht_2021.pdf",
    "vskb-geschaeftsbericht-2022.pdf": f"{BASE}/fileadmin/user_upload/site/publications/rapport-gestion/2022/WKB_Geschaftsbericht_2022.pdf",
    "vskb-geschaeftsbericht-2023.pdf": f"{BASE}/fileadmin/user_upload/site/publications/rapport-gestion/2023/WKB_Geschaeftsbericht_2023.pdf",
    "vskb-geschaeftsbericht-2024.pdf": f"{BASE}/fileadmin/user_upload/site/publications/rapport-gestion/2024/WKB-Geschaeftsbericht_2024.pdf",
    "vskb-geschaeftsbericht-2025.pdf": f"{BASE}/fileadmin/user_upload/site/publications/rapport-gestion/2025/WKB_Geschaeftsbericht_2025.pdf",
    # Semesterberichte (2015–2026)
    "vskb-semesterbericht-2015.pdf": f"{BASE}/fileadmin/user_upload/site/medias/communiques-presse/archives/communiques_de_presse/2015/DE/Halbjahresergebnisse_2015_der_WKB.pdf",
    "vskb-semesterbericht-2016.pdf": f"{BASE}/fileadmin/user_upload/site/medias/communiques-presse/archives/communiques_de_presse/2016/DE/WKB-BilanPP30062016.pdf",
    "vskb-semesterbericht-2017.pdf": f"{BASE}/fileadmin/user_upload/site/medias/communiques-presse/archives/communiques_de_presse/2017/DE/Halbjahresergebnisse_2017_der_WKB_-_Bilanz_und_Erfolgsrechnung.pdf",
    "vskb-semesterbericht-2018.pdf": f"{BASE}/fileadmin/user_upload/site/medias/communiques-presse/archives/communiques_de_presse/2018/DE/Halbjahresergebnisse_2018_der_WKB_-_Bilanz_und_Erfolgsrechnung.pdf",
    "vskb-semesterbericht-2019.pdf": f"{BASE}/fileadmin/user_upload/site/medias/communiques-presse/archives/communiques_de_presse/2019/DE/WKB_30.06.2019_-_Bilan_et_PP.pdf",
    "vskb-semesterbericht-2020.pdf": f"{BASE}/fileadmin/user_upload/site/medias/communiques-presse/2020/DE/Mediendossier_-_Halbjahresergebnis_2020.pdf",
    "vskb-semesterbericht-2021.pdf": f"{BASE}/fileadmin/user_upload/site/medias/communiques-presse/2021/DE/WKB-Halbjahresergebnisse_2021_-_Bilanz_und_Erfolgsrechnung.pdf",
    "vskb-semesterbericht-2022.pdf": f"{BASE}/fileadmin/user_upload/site/medias/communiques-presse/2022/DE/WKB-Halbjahresergebnisse_2022_-_Bilanz_und_Erfolgsrechnung.pdf",
    "vskb-semesterbericht-2023.pdf": f"{BASE}/fileadmin/user_upload/site/medias/communiques-presse/2023/DE/WKB_Halbjahresergebnisse_2023_-_Bilanz_und_Erfolgsrechnung.pdf",
    "vskb-semesterbericht-2024.pdf": f"{BASE}/fileadmin/user_upload/site/medias/communiques-presse/2024/DE/WKB-Halbjahresergebnisse_2024_-_Bilanz_und_Erfolgsrechnung.pdf",
    "vskb-semesterbericht-2025.pdf": f"{BASE}/fileadmin/user_upload/site/medias/communiques-presse/2025/resultats-semestriels2025/WKB-Halbjahresergebnisse_2025_-_Bilanz_und_Erfolgsrechnung.pdf",
    "vskb-semesterbericht-2026.pdf": f"{BASE}/fileadmin/user_upload/site/medias/communiques-presse/2026/resulats_semestriels2026/WKB-Halbjahresergebnisse_2026_-_Bilanz-_und_Erfolgsrechnung.pdf",
    # Offenlegungsberichte (06-2020–06-2026)
    "vskb-offenlegungsbericht-06-2020.pdf": f"{BASE}/fileadmin/user_upload/site/publications/conditions-infos-juridiques/PrescriptionsFondsPropres/Publikation_-_Aufsichtsrechtliche_Offenlegungspflichten_am_30.06.2020.pdf",
    "vskb-offenlegungsbericht-2020.pdf": f"{BASE}/fileadmin/user_upload/site/publications/conditions-infos-juridiques/PrescriptionsFondsPropres/Publikation_-_Aufsichtsrechtliche_Offenlegungspflichten_am_31.12.2020.pdf",
    "vskb-offenlegungsbericht-06-2021.pdf": f"{BASE}/fileadmin/user_upload/site/publications/conditions-infos-juridiques/PrescriptionsFondsPropres/Publikation_-_Aufsichtsrechtliche_Offenlegungspflichten_am_30.06.2021.pdf",
    "vskb-offenlegungsbericht-2021.pdf": f"{BASE}/fileadmin/user_upload/site/publications/conditions-infos-juridiques/PrescriptionsFondsPropres/Publikation_-_Aufsichtsrechtliche_Offenlegungspflichten_am_31.12.2021.pdf",
    "vskb-offenlegungsbericht-06-2022.pdf": f"{BASE}/fileadmin/user_upload/site/publications/conditions-infos-juridiques/PrescriptionsFondsPropres/Publikation_-_Aufsichtsrechtliche_Offenlegungspflichten_am_30.06.2022.pdf",
    "vskb-offenlegungsbericht-2022.pdf": f"{BASE}/fileadmin/user_upload/site/publications/conditions-infos-juridiques/PrescriptionsFondsPropres/Publikation_-_Aufsichtsrechtliche_Offenlegungspflichten_am_31.12.2022.pdf",
    "vskb-offenlegungsbericht-06-2023.pdf": f"{BASE}/fileadmin/user_upload/site/publications/conditions-infos-juridiques/PrescriptionsFondsPropres/Publikation_-_Aufsichtsrechtliche_Offenlegungspflichten_am_30.06.2023.pdf",
    "vskb-offenlegungsbericht-2023.pdf": f"{BASE}/fileadmin/user_upload/site/publications/conditions-infos-juridiques/PrescriptionsFondsPropres/Publikation_-_Aufsichtsrechtliche_Offenlegungspflichten_am_31.12.2023.pdf",
    "vskb-offenlegungsbericht-06-2024.pdf": f"{BASE}/fileadmin/user_upload/site/publications/conditions-infos-juridiques/PrescriptionsFondsPropres/Publikation_-_Aufsichtsrechtliche_Offenlegungspflichten_am_30.06.2024.pdf",
    "vskb-offenlegungsbericht-2024.pdf": f"{BASE}/fileadmin/user_upload/site/publications/conditions-infos-juridiques/PrescriptionsFondsPropres/WKB_Aufsichtsrechtliche_Offenlegungspfliten_am_31122024.pdf",
    "vskb-offenlegungsbericht-06-2025.pdf": f"{BASE}/fileadmin/user_upload/site/publications/conditions-infos-juridiques/PrescriptionsFondsPropres/WKB_Aufsichtsrechtliche_Offenlegungspflichten_30-06-2025.pdf",
    "vskb-offenlegungsbericht-2025.pdf": f"{BASE}/fileadmin/user_upload/site/publications/conditions-infos-juridiques/PrescriptionsFondsPropres/WKB_Aufsichtsrechtliche_Offenlegungspfliten_am_31122025.pdf",
    "vskb-offenlegungsbericht-06-2026.pdf": f"{BASE}/fileadmin/user_upload/site/publications/conditions-infos-juridiques/PrescriptionsFondsPropres/WKB_Aufsichtsrechtliche-Offenlegungspflichten_06-2026.pdf",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Download VSKB (WKB) PDF reports.")
    parser.add_argument("--force", action="store_true", help="Re-download existing PDFs")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force)


if __name__ == "__main__":
    main()
