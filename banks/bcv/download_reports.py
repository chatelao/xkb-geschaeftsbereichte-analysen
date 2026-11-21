#!/usr/bin/env python3
"""BCV Berichte Downloader – lädt alle verfügbaren Geschäfts-, Semester- und Pilier-3-Berichte."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from shared.download_utils import download_catalog  # noqa: E402

BASE = "https://www.bcv.ch"


def _u(path: str) -> str:
    return BASE + quote(path, safe="/-_.~()")


CATALOG: dict[str, str | list[str]] = {
    # Geschäftsberichte (2007–2025)
    "bcv-geschaeftsbericht-2007.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2007/RapportAnnuel_BCV_2007 (1).pdf"),
    "bcv-geschaeftsbericht-2008.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2008/RapportAnnuel_BCV_2008 (1).pdf"),
    "bcv-geschaeftsbericht-2009.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2009/RapportAnnuel_BCV_2009.pdf"),
    "bcv-geschaeftsbericht-2010.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2010/RapportAnnuel_BCV_2010.pdf"),
    "bcv-geschaeftsbericht-2011.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2011/RapportAnnuel_BCV_2011.pdf"),
    "bcv-geschaeftsbericht-2012.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2012/RapportAnnuel_BCV_2012.pdf"),
    "bcv-geschaeftsbericht-2013.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2013/RapportAnnuel_BCV_2013.pdf"),
    "bcv-geschaeftsbericht-2014.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2014/Rapport-20annuel_2014-bd.pdf"),
    "bcv-geschaeftsbericht-2015.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2015/Rapport-annuel-BCV-2015-fr.pdf"),
    "bcv-geschaeftsbericht-2016.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2016/Rapport-annuel-BCV-2016-fr.pdf"),
    "bcv-geschaeftsbericht-2017.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2017/FRA - BCV_Rapport_annuel_2017.pdf"),
    "bcv-geschaeftsbericht-2018.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2018/FRA-BCV_Rapport_annuel_2018.pdf"),
    "bcv-geschaeftsbericht-2019.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2019/FRA-BCV_Rapport_annuel_2019.pdf"),
    "bcv-geschaeftsbericht-2020.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2020/FR_BCV_Rapport_annuel_2020.pdf"),
    "bcv-geschaeftsbericht-2021.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2021/Rapport_annuel_BCV_2021_fr.pdf"),
    "bcv-geschaeftsbericht-2022.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2022/bcv-rapport-annuel-2022-fr.pdf"),
    "bcv-geschaeftsbericht-2023.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2023/Rapport-annuel-BCV-2023-fr.pdf"),
    "bcv-geschaeftsbericht-2024.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2024/Rapport-annuel-BCV-2024-fr.pdf"),
    "bcv-geschaeftsbericht-2025.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2025/2025_rapport-annuel-bcv_fr_web.pdf"),
    # Semesterberichte (2008–2026)
    "bcv-semesterbericht-2008.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2008/RapportSemestriel_lettre-actionnaires-2008 (1).pdf"),
    "bcv-semesterbericht-2009.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2009/RapportSemestriel_lettre-actionnaires-2009 (1).pdf"),
    "bcv-semesterbericht-2010.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2010/RapportSemestriel_lettre-actionnaires-2010.pdf"),
    "bcv-semesterbericht-2011.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2011/RapportSemestriel_lettre-actionnaires-2011.pdf"),
    "bcv-semesterbericht-2012.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2012/RapportSemestriel_30-06-121.pdf"),
    "bcv-semesterbericht-2013.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2013/RapportSemestriel_30-06-13.pdf"),
    "bcv-semesterbericht-2014.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2014/RapportSemestriel_2014.pdf"),
    "bcv-semesterbericht-2015.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2015/RapportSemestriel_2015.pdf"),
    "bcv-semesterbericht-2016.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2016/20180818-Rapport_intermediaire_2016-fr.pdf"),
    "bcv-semesterbericht-2017.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2017/Rapport_intermediaire_2017_FR.pdf"),
    "bcv-semesterbericht-2018.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2018/Rapport_intermediaire_2018_FR.pdf"),
    "bcv-semesterbericht-2019.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2019/20190822-Rapport-intermediaire-2019-fr.pdf"),
    "bcv-semesterbericht-2020.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2020/Rapport_intermédaire_2020_FR (2).pdf"),
    "bcv-semesterbericht-2021.pdf": [
        _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2021/Rapport-intermediaire-2021-FR"),
        "https://web.archive.org/web/20260119084743id_/https://www.bcv.ch/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2021/Rapport-intermediaire-2021-FR",
        "https://web.archive.org/web/20260119085811id_/https://www.bcv.ch/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2021/BCV_Rapport_interm-C3-A9diaire_2021_en.pdf",
    ],
    "bcv-semesterbericht-2022.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2022/FRA - BCV S1 2022 - Rapport intermédiaire.pdf"),
    "bcv-semesterbericht-2023.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2023/rapport-intermedaire-2023-fr.pdf"),
    "bcv-semesterbericht-2024.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2024/Rapport_intermédaire_2024_fr_web.pdf"),
    "bcv-semesterbericht-2025.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2025/BCV_Rapport_intermédaire_2025_fr.pdf"),
    "bcv-semesterbericht-2026.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/rapports-annuels-et-intermediaires/2026/Rapport_intermédaire_2026_fr.pdf"),
    # Offenlegungsberichte / Bâle III Pilier 3 (2009–06-2026)
    "bcv-offenlegungsbericht-06-2009.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2009/RapportBale_2emePilier_3.pdf"),
    "bcv-offenlegungsbericht-2009.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2009/RapportBale_2emePilier_3_31122009 (1).pdf"),
    "bcv-offenlegungsbericht-06-2010.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2010/RapportBale_2emePilier_3_30062010.pdf"),
    "bcv-offenlegungsbericht-2010.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2010/RapportBale_2emePilier_3_31122010.pdf"),
    "bcv-offenlegungsbericht-06-2011.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2011/RapportBale_2emePilier_3_30062011 (1).pdf"),
    "bcv-offenlegungsbericht-2011.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2011/RapportBale_2emePilier_3_31122011 (2).pdf"),
    "bcv-offenlegungsbericht-06-2012.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2012/RapportBale_2emePilier_330062012.pdf"),
    "bcv-offenlegungsbericht-2012.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2012/RapportBale_2emePilier_3_31122012.pdf"),
    "bcv-offenlegungsbericht-06-2013.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2013/RapportBale_2emePilier_3_30062013 (1).pdf"),
    "bcv-offenlegungsbericht-2013.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2013/RapportBale_3emePilier_3_30122013 (1).pdf"),
    "bcv-offenlegungsbericht-06-2014.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2014/RapportBale_3emePilier_3_30062014 (1).pdf"),
    "bcv-offenlegungsbericht-2014.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2014/rapport-bale-iii-pilier-3-31122014-fr (1).pdf"),
    "bcv-offenlegungsbericht-06-2015.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2015/rapport-bale-iii-pilier-3-30062015-fr.pdf"),
    "bcv-offenlegungsbericht-2015.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2015/rapport-bale-iii-pilier-3-31122015-fr (1).pdf"),
    "bcv-offenlegungsbericht-06-2016.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2016/rapport-bale-iii-pilier-3-30062016-fr.pdf"),
    "bcv-offenlegungsbericht-2016.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2016/rapport-bale-iii-pilier-3-31122016-fr.pdf"),
    "bcv-offenlegungsbericht-06-2017.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2017/rapport-bale-iii-pilier-3-30062017-fr.pdf"),
    "bcv-offenlegungsbericht-2017.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2017/BCV Bâle III - Pilier 3 au 31.12.2017-fr.pdf"),
    "bcv-offenlegungsbericht-06-2018.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2018/BCV_Rapport_Bâle_III-Pilier_3_au_30-06-2018_fr.pdf"),
    "bcv-offenlegungsbericht-2018.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2018/BCV Bâle III - Pilier 3 au 31.12.2018-fr.pdf"),
    "bcv-offenlegungsbericht-06-2019.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2019/BCV Bâle III - Pilier 3 au 30.06.2019-fr (1).pdf"),
    "bcv-offenlegungsbericht-2019.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2019/BCV 20 02 25 Bâle III - Pilier 3 au 31.12.2019 (1).pdf"),
    "bcv-offenlegungsbericht-06-2020.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2020/BCV 20 08 19 Bâle III - Pilier 3 au 30.6.2020.pdf"),
    "bcv-offenlegungsbericht-2020.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2020/BCV 21 02 17 Bâle III - Pilier 3 au 31.12.2020-fr (1).pdf"),
    "bcv-offenlegungsbericht-06-2021.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2021/BCV-2021-2008-2017-20B-C3-A2le-20III-20--20Pilier-203-20au-2030.06.2021-fr.pdf"),
    "bcv-offenlegungsbericht-2021.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2021/BCV-2022-2002-2005-20B-C3-A2le-20III-20--20Pilier-203-20au-2031.12.2021-fr.pdf"),
    "bcv-offenlegungsbericht-06-2022.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2022/BCV 22 08 18 Bâle III - Pilier 3 au 30.06.2022.pdf"),
    "bcv-offenlegungsbericht-2022.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2023/09022023-bcv-bale-iii-pilier-3-au-31-12-2022-fr.pdf"),
    "bcv-offenlegungsbericht-06-2023.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2023/17082023-bcv-bale-iii-pilier-3-au-30-06-2023-fr.pdf"),
    "bcv-offenlegungsbericht-2023.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2024/08022024-bcv-bale-iii-pilier-3-au-31-12-2023-fr.pdf"),
    "bcv-offenlegungsbericht-06-2024.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2024/BCV 24 08 15 Bâle III - Pilier 3 au 30.06.2024 v2.0.pdf"),
    "bcv-offenlegungsbericht-2024.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2025/13022025-bcv-bale-iii-pilier-3-au-31-12-2024-fr.pdf"),
    "bcv-offenlegungsbericht-06-2025.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2025/BCV-250819-Bale-III-Final-Pilier-3-au-30062025-fr.pdf"),
    "bcv-offenlegungsbericht-2025.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2026/BCV-26-02-09-Bale-III-Final-Pilier-3-au-31-12-2025.pdf"),
    "bcv-offenlegungsbericht-06-2026.pdf": _u("/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/ra-et-rse/bale-iii/2026/BCV 26 08 17 Bâle III Final - Pilier 3 au 30.06.2026 v1.0.pdf"),
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Download BCV PDF reports.")
    parser.add_argument("--force", action="store_true", help="Re-download existing PDFs")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force)


if __name__ == "__main__":
    main()
