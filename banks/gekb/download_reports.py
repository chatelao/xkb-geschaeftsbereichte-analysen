#!/usr/bin/env python3
"""GEKB (BCGE) Berichte Downloader – lädt alle verfügbaren Geschäfts-, Semester- und Pilier-3-Berichte."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from shared.download_utils import download_catalog  # noqa: E402

CATALOG: dict[str, str] = {
    # Geschäftsberichte (2003–2025)
    "gekb-geschaeftsbericht-2003.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2003.pdf/d044fb2e-85e1-73a1-df00-13e50d53a93d?t=1574861505866",
    "gekb-geschaeftsbericht-2004.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2004.pdf/ebd2db48-463b-866c-19f7-82639175799e?t=1583759710959",
    "gekb-geschaeftsbericht-2005.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2005.pdf/a2e3682e-fb18-0255-1f58-4da8ad543bff?t=1574861430571",
    "gekb-geschaeftsbericht-2006.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2006.pdf/b04e3d1d-3de4-df6d-7219-c332cb0d6aa7?t=1574861379049",
    "gekb-geschaeftsbericht-2007.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2007.pdf/91869330-ec08-5356-fdf5-7b896a6f0715?t=1574861330962",
    "gekb-geschaeftsbericht-2008.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2008.pdf/fd3bf794-55cf-886a-6de8-16d9a7e01415?t=1574861110228",
    "gekb-geschaeftsbericht-2009.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2009.pdf/e78ce894-a252-6fdf-329b-f3bb2d8546a5?t=1574860435397",
    "gekb-geschaeftsbericht-2010.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2010.pdf/181fcc5e-c903-2926-b305-ff05276052d0?t=1574859747899",
    "gekb-geschaeftsbericht-2011.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2011.pdf/e9d02faf-425f-8084-f451-6a40246f8bcb?t=1574845579343",
    "gekb-geschaeftsbericht-2012.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2012.pdf/75af1857-5a41-13df-aa8a-7bfaabd4f784?t=1574844795133",
    "gekb-geschaeftsbericht-2013.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2013.pdf/2f19faa3-a214-a58a-cadf-84dc0e63e135?t=1574844438686",
    "gekb-geschaeftsbericht-2014.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2014.pdf/d8f7347e-2c17-54d7-d791-ce47138d49a3?t=1574844198147",
    "gekb-geschaeftsbericht-2015.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2015.pdf/dd04fbb8-7192-1be2-1e29-a266babe6217?t=1574843886938",
    "gekb-geschaeftsbericht-2016.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2016.pdf/501e9b7c-ac3f-3601-a64a-ce50abb584b6?t=1574254666611",
    "gekb-geschaeftsbericht-2017.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2017.pdf/3dec1314-b5f1-d812-80b1-a4c44a70ec41?t=1574253966473",
    "gekb-geschaeftsbericht-2018.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2018.pdf/39135a49-d83b-ff5d-2dd6-1f3309e36738?t=1574253376967",
    "gekb-geschaeftsbericht-2019.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2019.pdf/259af8ab-3596-788b-7485-5f1d41667508?t=1585907601079",
    "gekb-geschaeftsbericht-2020.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2020.pdf/530ac9f9-3a6d-0337-8ede-c0ee7aea2a9b?t=1616687899651",
    "gekb-geschaeftsbericht-2021.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2021.pdf/463b513c-94fe-5f23-338c-7ca672ff2be8?t=1648565082951",
    "gekb-geschaeftsbericht-2022.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2022.pdf/b38a24e2-1e39-2d63-1542-22f37b885e4d?t=1680064735520",
    "gekb-geschaeftsbericht-2023.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2023.pdf/77568ece-c0d8-0938-c6bc-8003e3849bdd?t=1718029622493",
    "gekb-geschaeftsbericht-2024.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2024.pdf/791431ea-73df-ce98-42ad-e78f7f4469f2?t=1743598295191",
    "gekb-geschaeftsbericht-2025.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_rapport_annuel_2025.pdf/558bfc07-a33b-4750-7b4b-a278667f139b?t=1773853170666",
    # Semesterberichte (2008–2026)
    "gekb-semesterbericht-2008.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_comptes_semestriels_consolides_2008.pdf/a4eff49e-fd94-fa9e-62e2-0914831ce72b?t=1574861158459",
    "gekb-semesterbericht-2009.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_comptes_semestriels_consolides_2009.pdf/0d67eed4-b08c-a1a8-7380-c8374736e8cd?t=1583759192916",
    "gekb-semesterbericht-2010.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_comptes_semestriels_consolides_2010.pdf/d81c6fe6-072b-8c94-65da-9465a2237bfa?t=1574860167809",
    "gekb-semesterbericht-2011.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_comptes_semestriels_consolides_2011.pdf/63b3f55e-56ab-5b49-45cb-0eb4c3d01b2c?t=1574847025455",
    "gekb-semesterbericht-2012.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_comptes_semestriels_consolides_2012.pdf/3167b8a0-0fa2-7219-7ca4-2f1193c3da5b?t=1574844842296",
    "gekb-semesterbericht-2013.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_comptes_semestriels_consolides_2013.pdf/423d5950-f689-2a0c-9e58-5aebdd8d2150?t=1574844496729",
    "gekb-semesterbericht-2014.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_comptes_semestriels_consolides_2014.pdf/26a5176a-1e61-5c56-17d2-99e47b0b3f5e?t=1574844247909",
    "gekb-semesterbericht-2015.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_etats_financiers_30062015.pdf/49b0485c-2442-7ab0-5aa5-7bd589828a37?t=1574254746476",
    "gekb-semesterbericht-2017.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_etats_financiers_30062017.pdf/5f4985af-6941-64ac-7b5f-3eab708aec7c?t=1574254174268",
    "gekb-semesterbericht-2018.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_etats_financiers_30062018.pdf/bce8b723-ad29-3d6f-c1c3-68bb24fb88e4?t=1574253492516",
    "gekb-semesterbericht-2019.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_etats_financiers_30062019.pdf/901071a8-545e-4ff0-ab32-a1ee06d1152a?t=1574249924832",
    "gekb-semesterbericht-2020.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_etats_financiers_30062020.pdf/cfe8c61f-b755-03b5-2b27-defd044602c9?t=1598861759412",
    "gekb-semesterbericht-2021.pdf": "https://www.bcge.ch/documents/395713/397202/BCGE_resultats_semestriels_2021.pdf/8cd7a4f0-0a15-2cd3-6e62-1e76b62f4385?t=1628570595500",
    "gekb-semesterbericht-2022.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_resultats_semestriels_2022.pdf/c10aad1f-c1c7-79b5-d290-79874e5da54d?t=1659989327463",
    "gekb-semesterbericht-2023.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_restultats_semestriels_2023.pdf/1758959c-0f64-4540-3b3c-06a0e77136a0?t=1693220187787",
    "gekb-semesterbericht-2024.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE+%E2%80%93+R%C3%A9sultats+semestriels+au+30.06.24_fr.pdf/f9b38a4a-d642-7162-9476-d8baae999289?t=1723553316655",
    "gekb-semesterbericht-2025.pdf": "https://www.bcge.ch/documents/395713/2773256/BCGE_resultats_semestriels_2025_fr.pdf/302036a7-0338-2d1d-833a-15b4c58d471f?t=1755543020353",
    "gekb-semesterbericht-2026.pdf": "https://www.bcge.ch/documents/395713/3314668/BCGE_resultats_semestriels_2026_fr.pdf/842bb76d-4dbd-7bc9-2451-4813d7ceaeab?t=1787631136402",
    # Offenlegungsberichte / Pilier III (2010–2025 & H1 2019–2026)
    "gekb-offenlegungsbericht-2010.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_texte_Pilier_III_31_Dec_2010_Conso.pdf/ccb40dc1-a7ea-cdbe-b89c-785ad12134df?t=1574860142885",
    "gekb-offenlegungsbericht-2011.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_texte_Pilier_III_31_Dec_2011_Conso.pdf/c9ce235f-0497-2b9c-6680-6af7b7ae8ca4?t=1574846992827",
    "gekb-offenlegungsbericht-2012.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_texte_Pilier_III_31_Dec_2012_Conso.pdf/5e85db81-d88b-a119-05c4-ed96f99e1565?t=1574844817576",
    "gekb-offenlegungsbericht-2013.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_texte_Pilier_III_31_Dec_2013_Conso.pdf/f52b847c-047a-86fd-3ddd-2d35e546016b?t=1574844463904",
    "gekb-offenlegungsbericht-2014.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_texte_Pilier_III_31_Dec_2014_Conso.pdf/36539ea5-1ec6-5f1e-6349-3a93821d10a4?t=1574844218686",
    "gekb-offenlegungsbericht-2015.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_texte_Pilier_III_31_Dec_2015_Conso.pdf/68a10986-0947-7427-2f3e-86df76654ea1?t=1574843937687",
    "gekb-offenlegungsbericht-2016.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_texte_Pilier_III_31_Dec_2016_Conso.pdf/c22f00b7-798f-8ea3-5ab5-5409cd328d08?t=1574254720974",
    "gekb-offenlegungsbericht-2017.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_texte_Pilier_III_31_Dec_2017_Conso.pdf/6ef52697-dc61-134a-9838-48c687d72538?t=1574253992209",
    "gekb-offenlegungsbericht-2018.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_texte_Pilier_III_31_Dec_2018_Conso.pdf/c94405d6-2637-14f5-8d0c-ef925344cbcc?t=1574253435779",
    "gekb-offenlegungsbericht-2019.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_texte_Pilier_III_31_dec_2019_Conso.pdf/528adbe7-2d93-d112-46a0-b7e9c362c1ff?t=1574249963375",
    "gekb-offenlegungsbericht-2020.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_texte_Pilier_III_31_dec_2020.pdf/7ecfbc51-48ec-b785-71a2-07679a1edd90?t=1669819110468",
    "gekb-offenlegungsbericht-2021.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_texte_Pilier_III_31_dec_2021.pdf/4c17f8ce-ff36-0d59-03c6-8c97ea8c2a20?t=1669819109651",
    "gekb-offenlegungsbericht-2022.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE+texte_Pilier_III_31_Dec_2022.pdf/b06aff8e-8f4e-ea4d-cd98-0be2bcf34e30?t=1682598031529",
    "gekb-offenlegungsbericht-2023.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_texte_Pilier_III_31_Dec_2023.pdf/60c8b3f9-482d-2d5e-c0b0-888da8799b29?t=1718026972347",
    "gekb-offenlegungsbericht-2024.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_texte_Pilier_III_31.12.2024.pdf/5fe59319-f8c3-9b49-cd9d-49eda25e0ea5?t=1745573331173",
    "gekb-offenlegungsbericht-2025.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_Pilier_III_au_31122025.pdf/e7ad61b8-118c-f0ce-6a11-6772fc05fe0d?t=1777040907880",
    "gekb-offenlegungsbericht-06-2019.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_texte_Pilier_III_30_Juin_2019.pdf/2951142d-2b45-01fd-0679-0cb054cd58c3?t=1684926013877",
    "gekb-offenlegungsbericht-06-2020.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_texte_Pilier_III_30_Juin_2020.pdf/186172a2-8434-ecd0-3533-cc291074079a?t=1598861758776",
    "gekb-offenlegungsbericht-06-2021.pdf": "https://www.bcge.ch/documents/395713/396737/BCGE_texte_Pilier_III_30_Juin_2021_en.pdf/f487d8f5-0202-ae55-d604-c94aadb2d9f5?t=1632994280117",
    "gekb-offenlegungsbericht-06-2022.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE+texte_Pilier_III_30_Juin_2022.pdf/42f2caad-998d-b846-2163-05ab1cc9fc1c?t=1661502674460",
    "gekb-offenlegungsbericht-06-2023.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_texte_Pilier_III_30_Juin_2023.pdf/1793c90c-6638-10d3-54c7-b1eaff50162b?t=1693220188307",
    "gekb-offenlegungsbericht-06-2024.pdf": "https://www.bcge.ch/documents/395713/2159788/BCGE+-+publication+du+Pilier+III+au+30+Juin+2024.pdf/9dd5418e-9daf-e855-33dc-5b07e9414517?t=1725261857403",
    "gekb-offenlegungsbericht-06-2025.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_texte_Pilier_III_au_30.06.2025.pdf/931f85e0-fe6b-0958-936f-fc253db9b518?t=1756386838489",
    "gekb-offenlegungsbericht-06-2026.pdf": "https://www.bcge.ch/documents/395713/396740/BCGE_Pilier_III_au_30062026.pdf/9a476d70-184e-ac4f-68d8-c0c02e1553d5?t=1788191622292",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Download GEKB (BCGE) PDF reports.")
    parser.add_argument("--force", action="store_true", help="Re-download existing PDFs")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force)


if __name__ == "__main__":
    main()
