#!/usr/bin/env python3
"""ZKB Berichte Downloader – lädt alle verfügbaren Geschäfts-, Halbjahres- und Offenlegungsberichte."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.download_utils import download_catalog  # noqa: E402

BASE = "https://www.zkb.ch"
WB = "https://web.archive.org/web"


def _zkb_and_wb(path: str, ts: str) -> list[str]:
    return [f"{BASE}{path}", f"{WB}/{ts}id_/{BASE}{path}"]


CATALOG: dict[str, str | list[str]] = {
    # Geschäftsberichte (2014–2025; 2025 inkl. Teilberichte)
    "zkb-geschaeftsbericht-2014.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/gesamtausgabe_2014.pdf",
    "zkb-geschaeftsbericht-2015.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/geschaeftsbericht_2015.pdf",
    "zkb-geschaeftsbericht-2016.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/geschaeftsbericht_2016.pdf",
    "zkb-geschaeftsbericht-2017.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/geschaeftsbericht_2017.pdf",
    "zkb-geschaeftsbericht-2018.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/geschaeftsbericht_2018.pdf",
    "zkb-geschaeftsbericht-2019.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/geschaeftsbericht_2019.pdf",
    "zkb-geschaeftsbericht-2020.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/geschaeftsbericht-2020.pdf",
    "zkb-geschaeftsbericht-2021.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/geschaeftsbericht-2021.pdf",
    "zkb-geschaeftsbericht-2022.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/geschaeftsbericht_2022.pdf",
    "zkb-geschaeftsbericht-2023.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/zkb_geschaeftsbericht_2023.pdf",
    "zkb-geschaeftsbericht-2024.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/zkb_geschaeftsbericht_2024.pdf",
    "zkb-geschaeftsbericht-2025.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/zkb_geschaeftsbericht_2025_de.pdf",
    "zkb-geschaeftsbericht-2025-finanzbericht.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/zkb_geschaeftsbericht_2025_finanzbericht_de.pdf",
    "zkb-geschaeftsbericht-2025-lagebericht.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/zkb_geschaeftsbericht_2025_lagebericht_de.pdf",
    "zkb-geschaeftsbericht-2025-corporate-governance.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/zkb_geschaeftsbericht_2025_corporate_governance_de.pdf",
    "zkb-geschaeftsbericht-2025-verguetungsbericht.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/zkb_geschaeftsbericht_2025_verguetungsbericht_de.pdf",
    # Halbjahresberichte (2013–2026)
    "zkb-semesterbericht-2013.pdf": _zkb_and_wb("/media/zkb/dokumente/investor-relations/halbjahresbericht_2013.pdf", "20240328075408"),
    "zkb-semesterbericht-2014.pdf": _zkb_and_wb("/media/zkb/dokumente/investor-relations/halbjahresbericht_2014.pdf", "20220121141504"),
    "zkb-semesterbericht-2015.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/halbjahresbericht_2015.pdf",
    "zkb-semesterbericht-2016.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/halbjahresbericht_2016.pdf",
    "zkb-semesterbericht-2017.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/halbjahresbericht_2017.pdf",
    "zkb-semesterbericht-2018.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/halbjahresbericht_2018.pdf",
    "zkb-semesterbericht-2019.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/halbjahresbericht_2019.pdf",
    "zkb-semesterbericht-2020.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/halbjahresbericht_2020.pdf",
    "zkb-semesterbericht-2021.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/zkb_hjb_2021.pdf",
    "zkb-semesterbericht-2022.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/halbjahresbericht_2022.pdf",
    "zkb-semesterbericht-2023.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/halbjahresbericht_2023.pdf",
    "zkb-semesterbericht-2024.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/zkb_halbjahresbericht_2024.pdf",
    "zkb-semesterbericht-2025.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/zkb_halbjahresbericht_2025_de.pdf",
    "zkb-semesterbericht-2026.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/zkb_halbjahresbericht_2026_de_web.pdf",
    # Offenlegungsberichte (2014–Q2 2026)
    "zkb-offenlegungsbericht-03-2014.pdf": _zkb_and_wb("/media/zkb/dokumente/investor-relations/offenlegungsreport_03_2014.pdf", "20220812133848"),
    "zkb-offenlegungsbericht-2014.pdf": _zkb_and_wb("/media/zkb/dokumente/investor-relations/offenlegungsreport_12_2014.pdf", "20220813081222"),
    "zkb-offenlegungsbericht-03-2015.pdf": _zkb_and_wb("/media/zkb/dokumente/investor-relations/offenlegungsreport_03_2015.pdf", "20220813021822"),
    "zkb-offenlegungsbericht-06-2015.pdf": _zkb_and_wb("/media/zkb/dokumente/investor-relations/offenlegung_juni_2015.pdf", "20220812164710"),
    "zkb-offenlegungsbericht-09-2015.pdf": _zkb_and_wb("/media/zkb/dokumente/investor-relations/offenlegung_september_2015.pdf", "20220812140409"),
    "zkb-offenlegungsbericht-03-2016.pdf": _zkb_and_wb("/media/zkb/dokumente/investor-relations/offenlegung_03_2016.pdf", "20220812132944"),
    "zkb-offenlegungsbericht-06-2016.pdf": _zkb_and_wb("/media/zkb/dokumente/investor-relations/offenlegung_06_2016.pdf", "20220812133628"),
    "zkb-offenlegungsbericht-09-2016.pdf": _zkb_and_wb("/media/zkb/dokumente/investor-relations/offenlegung_09_2016.pdf", "20220812114256"),
    "zkb-offenlegungsbericht-2016.pdf": _zkb_and_wb("/media/zkb/dokumente/investor-relations/offenlegung_12_2016.pdf", "20220812135348"),
    "zkb-offenlegungsbericht-03-2017.pdf": _zkb_and_wb("/media/zkb/dokumente/investor-relations/offenlegung_03_2017.pdf", "20220813015541"),
    "zkb-offenlegungsbericht-2017.pdf": _zkb_and_wb("/media/zkb/dokumente/investor-relations/offenlegungsreport_12_2017.pdf", "20220812161031"),
    "zkb-offenlegungsbericht-06-2018.pdf": _zkb_and_wb("/media/zkb/dokumente/investor-relations/offenlegungsreport_06_2018.pdf", "20220812192949"),
    "zkb-offenlegungsbericht-09-2018.pdf": _zkb_and_wb("/media/zkb/dokumente/investor-relations/offenlegungsreport_09_2018.pdf", "20220812153529"),
    "zkb-offenlegungsbericht-2018.pdf": _zkb_and_wb("/media/zkb/dokumente/investor-relations/offenlegung_31122018.pdf", "20220812152210"),
    "zkb-offenlegungsbericht-03-2019.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegung_03_2019.pdf",
    "zkb-offenlegungsbericht-06-2019.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegung_06_2019.pdf",
    "zkb-offenlegungsbericht-09-2019.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegung_09_2019.pdf",
    "zkb-offenlegungsbericht-2019.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegung_em_liq_31_12_2019.pdf",
    "zkb-offenlegungsbericht-03-2020.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegung_em_liq_31032020.pdf",
    "zkb-offenlegungsbericht-06-2020.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegung_06_2020.pdf",
    "zkb-offenlegungsbericht-09-2020.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegung_09_2020.pdf",
    "zkb-offenlegungsbericht-2020.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegungsreport-12-2020.pdf",
    "zkb-offenlegungsbericht-03-2021.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegungsreport_03_2021.pdf",
    "zkb-offenlegungsbericht-06-2021.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegungsreport_06_2021.pdf",
    "zkb-offenlegungsbericht-09-2021.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegungsreport_09_2021.pdf",
    "zkb-offenlegungsbericht-2021.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegungsreport_12_2021.pdf",
    "zkb-offenlegungsbericht-03-2022.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegungsreport_03_2022.pdf",
    "zkb-offenlegungsbericht-06-2022.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegungsreport_06_2022.pdf",
    "zkb-offenlegungsbericht-09-2022.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegungsreport_09_2022.pdf",
    "zkb-offenlegungsbericht-2022.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegungsreport_12_2022.pdf",
    "zkb-offenlegungsbericht-03-2023.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegungsreport_03_2023.pdf",
    "zkb-offenlegungsbericht-06-2023.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegungsreport_06_2023.pdf",
    "zkb-offenlegungsbericht-09-2023.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegungsreport_09_2023.pdf",
    "zkb-offenlegungsbericht-2023.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegungsreport_12_2023.pdf",
    "zkb-offenlegungsbericht-03-2024.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegungsreport_03_2024.pdf",
    "zkb-offenlegungsbericht-06-2024.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/offenlegung_06_2024.pdf",
    "zkb-offenlegungsbericht-09-2024.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/zkb_offenlegung_q3_2024_de.pdf",
    "zkb-offenlegungsbericht-2024.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/zkb_offenlegung_2024_q4_de.pdf",
    "zkb-offenlegungsbericht-03-2025.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/zkb_offenlegung_2025_q1_de.pdf",
    "zkb-offenlegungsbericht-06-2025.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/zkb_offenlegung_2025_q2_de.pdf",
    "zkb-offenlegungsbericht-09-2025.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/zkb_offenlegung_2025_q3_de.pdf",
    "zkb-offenlegungsbericht-2025.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/ZKB%20Offenlegung%20Q4%202025_de%20final_ok.pdf",
    "zkb-offenlegungsbericht-03-2026.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/zkb_offenlegung_2026_q1_de.pdf",
    "zkb-offenlegungsbericht-06-2026.pdf": f"{BASE}/media/zkb/dokumente/investor-relations/zkb_offenlegung_2026_q2_de_web.pdf",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Download ZKB PDF reports.")
    parser.add_argument("--force", action="store_true", help="Re-download existing PDFs")
    args = parser.parse_args()
    download_catalog(CATALOG, Path(__file__).resolve().parent / "pdf", force=args.force)


if __name__ == "__main__":
    main()
