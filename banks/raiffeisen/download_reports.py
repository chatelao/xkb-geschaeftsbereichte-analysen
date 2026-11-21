#!/usr/bin/env python3
"""Raiffeisen Gruppe Berichte Downloader – Geschäfts-, Zwischen- und Offenlegungsberichte."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from shared.download_utils import download_catalog  # noqa: E402

BASE = "https://www.raiffeisen.ch"

CATALOG: dict[str, str | list[str]] = {
    # Geschäftsberichte Raiffeisen Gruppe (2011–2025)
    "raiffeisen-geschaeftsbericht-2011.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2011/2011-geschaeftsbericht-finanzbericht-raiffeisen-gruppe.pdf",
    "raiffeisen-geschaeftsbericht-2012.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2012/2012-publikation-geschaeftsbericht-raiffeisen-gruppe.pdf",
    "raiffeisen-geschaeftsbericht-2013.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2013/2013-geschaeftsbericht-raiffeisen-gruppe.pdf",
    "raiffeisen-geschaeftsbericht-2014.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2014/2014-geschaeftsbericht-raiffeisen-gruppe.pdf",
    "raiffeisen-geschaeftsbericht-2015.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2015/2015-geschaeftsbericht-raiffeisen-gruppe.pdf",
    "raiffeisen-geschaeftsbericht-2016.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2016/2016-geschaeftsbericht-raiffeisen-gruppe.pdf",
    "raiffeisen-geschaeftsbericht-2017.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2017/2017-geschaeftsbericht-raiffeisen-gruppe-raiffeisen-schweiz.pdf.pdf",
    "raiffeisen-geschaeftsbericht-2018.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2018/2018-geschaeftsbericht-raiffeisen-gruppe.pdf",
    "raiffeisen-geschaeftsbericht-2019.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2019/2019-geschaeftsbericht-raiffeisen-gruppe.pdf",
    "raiffeisen-geschaeftsbericht-2020.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2020/2020-raiffeisen-gruppe-geschaeftsbericht.pdf",
    "raiffeisen-geschaeftsbericht-2021.pdf": f"{BASE}/content/dam/www/rch/ueber-uns/medien/medienmitteilungen/2022/de/geschaeftsbericht-2021-raiffeisen-gruppe.pdf",
    "raiffeisen-geschaeftsbericht-2022.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2022/raiffeisen-gruppe-geschaeftsbericht-2022.pdf",
    "raiffeisen-geschaeftsbericht-2023.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2023/geschaeftsbericht-2023-raiffeisen-gruppe.pdf",
    "raiffeisen-geschaeftsbericht-2024.pdf": f"{BASE}/content/dam/www/rch/pdf/ueber-uns/geschaeftsbericht/2024/geschaeftsbericht-2024-raiffeisen-gruppe.pdf",
    "raiffeisen-geschaeftsbericht-2025.pdf": f"{BASE}/content/dam/www/rch/ueber-uns/raiffeisen-gruppe/geschaeftsberichte/2025/geschaeftsbericht-2025-raiffeisen-gruppe.pdf",
    # Semesterberichte / Zwischenabschlüsse (2012–2026)
    "raiffeisen-semesterbericht-2012.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2012/2012-zwischenabschluss-raiffeisen-gruppe.pdf",
    "raiffeisen-semesterbericht-2013.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2013/2013-zwischenabschluss-raiffeisen-gruppe.pdf",
    "raiffeisen-semesterbericht-2014.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2014/2014-zwischenabschluss-raiffeisen-gruppe.pdf",
    "raiffeisen-semesterbericht-2015.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2015/2015-zwischenabschluss-raiffeisen-gruppe.pdf",
    "raiffeisen-semesterbericht-2016.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2016/raiffeisen-zwischenabschluss-2016-de.pdf",
    "raiffeisen-semesterbericht-2017.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2017/raiffeisen-zwischenabschluss-2017.pdf",
    "raiffeisen-semesterbericht-2018.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2018/zwischenabschluss-raiffeisen-gruppe-2018.pdf",
    "raiffeisen-semesterbericht-2019.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2019/zwischenabschluss-raiffeisen-gruppe-2019.pdf",
    "raiffeisen-semesterbericht-2020.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2020/zwischenabschluss-raiffeisen-gruppe-2020.pdf",
    "raiffeisen-semesterbericht-2021.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2021/zwischenabschluss-raiffeisen-gruppe-2021.pdf",
    "raiffeisen-semesterbericht-2022.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2022/zwischenabschluss-raiffeisen-gruppe-2022.pdf",
    "raiffeisen-semesterbericht-2023.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2023/raiffeisen-gruppe-zwischenabschluss-2023.pdf",
    "raiffeisen-semesterbericht-2024.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2024/20240630-raiffeisen-gruppe-zwischenabschluss-2024-de.pdf",
    "raiffeisen-semesterbericht-2025.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2025/20250630-raiffeisen-gruppe-zwischenbericht-2025-de.pdf",
    "raiffeisen-semesterbericht-2026.pdf": f"{BASE}/content/dam/www/rch/pdf/abschlusszahlen/de/2026/20260630-raiffeisen-gruppe-zwischenbericht-2026-de.pdf",
    # Offenlegungsberichte (06-2015–06-2026)
    "raiffeisen-offenlegungsbericht-06-2015.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2015/offenlegungsreport-30-06-2015.pdf",
    "raiffeisen-offenlegungsbericht-09-2015.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2015/offenlegungsreport-30-09-2015.pdf",
    "raiffeisen-offenlegungsbericht-2015.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2015/offenlegungsreport-31-12-2015.pdf",
    "raiffeisen-offenlegungsbericht-03-2016.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2016/offenlegungsreport-31-03-2016.pdf",
    "raiffeisen-offenlegungsbericht-06-2016.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2016/kapitaladaequanz-systemrelevanz-gruppe-30-06-2016.pdf",
    "raiffeisen-offenlegungsbericht-09-2016.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2016/offenlegung-eigenmittel-30-09-2016.pdf",
    "raiffeisen-offenlegungsbericht-2016.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2016/kapitaladaequanz-systemrelevanz-gruppe-31-12-2016.pdf",
    "raiffeisen-offenlegungsbericht-03-2017.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2017/offenlegung-systemrelevanz-31-03-2017.pdf",
    "raiffeisen-offenlegungsbericht-06-2017.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2017/offenlegung-systemrelevanz-30-06-2017.pdf",
    "raiffeisen-offenlegungsbericht-09-2017.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2017/offenlegung-systemrelevanz-30-09-2017.pdf",
    "raiffeisen-offenlegungsbericht-2017.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2017/offenlegung-systemrelevanz-31-12-2017.pdf",
    "raiffeisen-offenlegungsbericht-03-2018.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2018/em-offenlegung-q1-2018.pdf",
    "raiffeisen-offenlegungsbericht-06-2018.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2018/em-offenlegung-q2-2018.pdf",
    "raiffeisen-offenlegungsbericht-09-2018.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2018/em-offenlegung-q3-2018.pdf",
    "raiffeisen-offenlegungsbericht-2018.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2018/em-offenlegung-q4-2018.pdf",
    "raiffeisen-offenlegungsbericht-03-2019.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2019/em-offenlegung-q1-2019.pdf",
    "raiffeisen-offenlegungsbericht-06-2019.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2019/em-offenlegung-q2-2019.pdf",
    "raiffeisen-offenlegungsbericht-09-2019.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2019/em-offenlegung-q3-2019.pdf",
    "raiffeisen-offenlegungsbericht-2019.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2019/em-offenlegung-q4-2019.pdf",
    "raiffeisen-offenlegungsbericht-03-2020.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2020/em-offenlegung-q1-2020.pdf",
    "raiffeisen-offenlegungsbericht-06-2020.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2020/em-offenlegung-q2-2020.pdf",
    "raiffeisen-offenlegungsbericht-09-2020.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2020/em-offenlegung-q3-2020.pdf",
    "raiffeisen-offenlegungsbericht-2020.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2020/em-offenlegung-q4-2020.pdf",
    "raiffeisen-offenlegungsbericht-03-2021.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2021/em-offenlegung-q1-2021.pdf",
    "raiffeisen-offenlegungsbericht-06-2021.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2021/em-offenlegung-q2-2021.pdf",
    "raiffeisen-offenlegungsbericht-09-2021.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2021/em-offenlegung-q3-2021.pdf",
    "raiffeisen-offenlegungsbericht-2021.pdf": f"{BASE}/content/dam/www/rch/ueber-uns/medien/medienmitteilungen/2022/de/aufsichtsrechtliche-offenlegung-q4-2021.pdf",
    "raiffeisen-offenlegungsbericht-03-2022.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2022/em-offenlegung-q1-2022.pdf",
    "raiffeisen-offenlegungsbericht-06-2022.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2022/em-offenlegung-q2-2022.pdf",
    "raiffeisen-offenlegungsbericht-09-2022.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2022/em-offenlegung-q3-2022.pdf",
    "raiffeisen-offenlegungsbericht-2022.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2022/em-offenlegung-q4-2022.pdf",
    "raiffeisen-offenlegungsbericht-03-2023.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2023/em-offenlegung-q1-2023.pdf",
    "raiffeisen-offenlegungsbericht-06-2023.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2023/em-offenlegung-q2-2023.pdf",
    "raiffeisen-offenlegungsbericht-09-2023.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2023/em-offenlegung-q3-2023.pdf",
    "raiffeisen-offenlegungsbericht-2023.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2023/raiffeisen-gruppe-aufsichtsrechtliche-offenlegung-2023.pdf",
    "raiffeisen-offenlegungsbericht-03-2024.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2024/raiffeisen-gruppe-aufsichtsrechtliche-offenlegung-31032024.pdf",
    "raiffeisen-offenlegungsbericht-06-2024.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2024/aufsichtsrechtliche-offenlegung-per-30-06-2024-raiffeisen-gruppe.pdf",
    "raiffeisen-offenlegungsbericht-09-2024.pdf": f"{BASE}/content/dam/www/rch/pdf/raiffeisen-gruppe/mittel-risiko-haftung/de/2024/raiffeisen-gruppe-aufsichtsrechtliche-offenlegung-30-09-2024.pdf",
    "raiffeisen-offenlegungsbericht-2024.pdf": f"{BASE}/content/dam/www/rch/pdf/ueber-uns/geschaeftsbericht/2024/aufsichtsrechtliche-offenlegung-2024-raiffeisen-gruppe.pdf",
    "raiffeisen-offenlegungsbericht-03-2025.pdf": f"{BASE}/content/dam/www/rch/pdf/ueber-uns/geschaeftsbericht/2025/aufsichtsrechtliche-offenlegung-31032025-raiffeisen-gruppe.pdf",
    "raiffeisen-offenlegungsbericht-06-2025.pdf": f"{BASE}/content/dam/www/rch/pdf/ueber-uns/geschaeftsbericht/2025/aufsichtsrechtliche-offenlegung-30062025-raiffeisen-gruppe.pdf",
    "raiffeisen-offenlegungsbericht-09-2025.pdf": f"{BASE}/content/dam/www/rch/pdf/ueber-uns/geschaeftsbericht/2025/aufsichtsrechtliche-offenlegung-30092025-raiffeisen-gruppe.pdf",
    "raiffeisen-offenlegungsbericht-2025.pdf": f"{BASE}/content/dam/www/rch/ueber-uns/raiffeisen-gruppe/geschaeftsberichte/2025/aufsichtsrechtliche-offenlegung-2025-raiffeisen-gruppe.pdf",
    "raiffeisen-offenlegungsbericht-03-2026.pdf": f"{BASE}/content/dam/www/rch/ueber-uns/raiffeisen-gruppe/geschaeftsberichte/2026/aufsichtsrechtliche-offenlegung-31032026-raiffeisen-gruppe.pdf",
    "raiffeisen-offenlegungsbericht-06-2026.pdf": f"{BASE}/content/dam/www/rch/ueber-uns/raiffeisen-gruppe/geschaeftsberichte/2026/aufsichtsrechtliche-offenlegung-30062026-raiffeisen-gruppe.pdf",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Download Raiffeisen Gruppe PDF reports.")
    parser.add_argument("--force", action="store_true", help="Re-download existing PDFs")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force)


if __name__ == "__main__":
    main()
