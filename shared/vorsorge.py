#!/usr/bin/env python3
"""Phase V2: Strukturierter Datensatz der zugehörigen Vorsorgeeinrichtungen (Pensionskassen) aller 8 Institute.

Quellenbasis: Primär die Vorsorge-Anhänge (Swiss GAAP FER 16 / ARB bzw. IAS 19 Note 25/26 bei UBS)
in den jeweiligen Geschäftsberichten (<bank>/.md/). Nicht im Bank-Geschäftsbericht ausgewiesene
BVG-Einzelgrössen sind explizit als null/None markiert (keine Schätzwerte).
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from shared.config import REPO_ROOT, VALID_BANKS

VORSORGE_RECORDS: list[dict] = [
    {
        "bank_id": "bekb",
        "short_name": "BEKB",
        "pk_name": "Pensionskasse der Berner Kantonalbank AG",
        "pk_plan_type": "Beitragsprimat (umhüllend)",
        "accounting_basis": "Swiss GAAP FER 16 / ARB",
        "reference_year": 2024,
        "active_insured_count": 1593,
        "pensioners_count": 791,
        "active_to_pensioner_ratio": 2.01,
        "pk_assets_mio": 1205.1,
        "coverage_ratio_bvg_pct": 126.0,
        "technical_interest_rate_pct": 1.5,
        "interest_crediting_pct": None,
        "conversion_rate_65_pct": None,
        "employer_contribution_mio": None,
        "employer_share_pct": 60.0,
        "employer_contribution_reserve_mio": None,
        "extraordinary_contributions_mio": 83.8,
        "notes": "Schwankungsreserve 17,3 %, Freie Mittel 3,1 % (31.12.2024; 2023 Deckungsgrad 120,2 %); 2015 einmalige PK-Sanierungseinlage 83,8 Mio. CHF.",
        "source_url_or_file": "bekb/.md/bekb-geschaeftsbericht-2024.md (Anhang Vorsorgeeinrichtungen, S. 159)",
    },
    {
        "bank_id": "vskb",
        "short_name": "WKB (VSKB)",
        "pk_name": "Pensions- und Vorsorgekasse für das Personal der Walliser Kantonalbank",
        "pk_plan_type": "Beitragsprimat (umhüllend)",
        "accounting_basis": "Swiss GAAP FER 16 / ARB",
        "reference_year": 2024,
        "active_insured_count": None,
        "pensioners_count": None,
        "active_to_pensioner_ratio": None,
        "pk_assets_mio": None,
        "coverage_ratio_bvg_pct": None,
        "technical_interest_rate_pct": None,
        "interest_crediting_pct": None,
        "conversion_rate_65_pct": None,
        "employer_contribution_mio": None,
        "employer_share_pct": None,
        "employer_contribution_reserve_mio": None,
        "extraordinary_contributions_mio": 29.0,
        "notes": "2020 Sondereinlage 29,0 Mio. CHF in Pensions- und Vorsorgekasse für das Personal der WKB (GB 2021 Ziff. 8.13/10.3).",
        "source_url_or_file": "vskb/.md/vskb-geschaeftsbericht-2021.md; vskb/.md/vskb-geschaeftsbericht-2024.md",
    },
    {
        "bank_id": "zkb",
        "short_name": "ZKB",
        "pk_name": "Pensionskasse der Zürcher Kantonalbank",
        "pk_plan_type": "Beitragsprimat (umhüllend)",
        "accounting_basis": "Swiss GAAP FER 16 / ARB",
        "reference_year": 2025,
        "active_insured_count": 6179,
        "pensioners_count": 2308,
        "active_to_pensioner_ratio": 2.68,
        "pk_assets_mio": None,
        "coverage_ratio_bvg_pct": None,
        "technical_interest_rate_pct": None,
        "interest_crediting_pct": None,
        "conversion_rate_65_pct": None,
        "employer_contribution_mio": None,
        "employer_share_pct": None,
        "employer_contribution_reserve_mio": None,
        "extraordinary_contributions_mio": 0.0,
        "notes": "2025: 6'179 Aktive / 2'308 Rentner (2024: 6'039 / 2'282). Eigene autonome Kasse mit Arbeitnehmervertretung.",
        "source_url_or_file": "zkb/.md/zkb-geschaeftsbericht-2025.md (S. 99 / Personalbericht)",
    },
    {
        "bank_id": "bcv",
        "short_name": "BCV",
        "pk_name": "Caisse de pensions de la Banque Cantonale Vaudoise",
        "pk_plan_type": "Beitragsprimat (umhüllend / enveloppante)",
        "accounting_basis": "Swiss GAAP FER 16 / ARB",
        "reference_year": 2024,
        "active_insured_count": 2210,
        "pensioners_count": 1479,
        "active_to_pensioner_ratio": 1.49,
        "pk_assets_mio": None,
        "coverage_ratio_bvg_pct": None,
        "technical_interest_rate_pct": None,
        "interest_crediting_pct": None,
        "conversion_rate_65_pct": None,
        "employer_contribution_mio": None,
        "employer_share_pct": None,
        "employer_contribution_reserve_mio": None,
        "extraordinary_contributions_mio": 0.0,
        "notes": "2024: 2'210 aktive Versicherte (davon 1'964 Stammhaus) und 1'479 Rentner; umhüllender Vorsorgeplan.",
        "source_url_or_file": "bcv/.md/bcv-geschaeftsbericht-2024.md (Rapport social, S. 732-734)",
    },
    {
        "bank_id": "gekb",
        "short_name": "BCGE (GEKB)",
        "pk_name": "Fondation de prévoyance professionnelle de la BCGE",
        "pk_plan_type": "Beitragsprimat (umhüllend)",
        "accounting_basis": "Swiss GAAP FER 16 / ARB",
        "reference_year": 2025,
        "active_insured_count": None,
        "pensioners_count": None,
        "active_to_pensioner_ratio": None,
        "pk_assets_mio": None,
        "coverage_ratio_bvg_pct": None,
        "technical_interest_rate_pct": None,
        "interest_crediting_pct": None,
        "conversion_rate_65_pct": None,
        "employer_contribution_mio": None,
        "employer_share_pct": None,
        "employer_contribution_reserve_mio": None,
        "extraordinary_contributions_mio": 0.0,
        "notes": "Haupt-Vorsorgeeinrichtung der BCGE-Gruppe, deckt alle Mitarbeitenden des Stammhauses ab.",
        "source_url_or_file": "gekb/.md/gekb-geschaeftsbericht-2024.md; gekb/.md/gekb-geschaeftsbericht-2025.md",
    },
    {
        "bank_id": "raiffeisen",
        "short_name": "Raiffeisen",
        "pk_name": "Raiffeisen Pensionskasse Genossenschaft (+ Arbeitgeberstiftung)",
        "pk_plan_type": "Beitragsprimat (umhüllend)",
        "accounting_basis": "Swiss GAAP FER 16 / ARB",
        "reference_year": 2025,
        "active_insured_count": None,
        "pensioners_count": None,
        "active_to_pensioner_ratio": None,
        "pk_assets_mio": None,
        "coverage_ratio_bvg_pct": None,
        "technical_interest_rate_pct": None,
        "interest_crediting_pct": None,
        "conversion_rate_65_pct": None,
        "employer_contribution_mio": None,
        "employer_share_pct": None,
        "employer_contribution_reserve_mio": 179.102,
        "extraordinary_contributions_mio": 0.0,
        "notes": "Arbeitgeberbeitragsreserve (AGBR) Ende 2025: 179,1 Mio. CHF (2024: 178,2 Mio. CHF); Verpflichtungen gegenüber eigenen Vorsorgeeinrichtungen: 302,2 Mio. CHF.",
        "source_url_or_file": "raiffeisen/.md/raiffeisen-geschaeftsbericht-2025.md (Anhang Ziff. 12, S. 124)",
    },
    {
        "bank_id": "postfinance",
        "short_name": "PostFinance",
        "pk_name": "Pensionskasse Post (Sammelstiftung Konzern Post)",
        "pk_plan_type": "Beitragsprimat (umhüllend)",
        "accounting_basis": "Swiss GAAP FER 16 / FER 26",
        "reference_year": 2025,
        "active_insured_count": 37516,
        "pensioners_count": 28703,
        "active_to_pensioner_ratio": 1.31,
        "pk_assets_mio": None,
        "coverage_ratio_bvg_pct": None,
        "technical_interest_rate_pct": None,
        "interest_crediting_pct": None,
        "conversion_rate_65_pct": None,
        "employer_contribution_mio": 46.0,
        "employer_share_pct": None,
        "employer_contribution_reserve_mio": 36.0,
        "extraordinary_contributions_mio": 0.0,
        "notes": "Keine eigene PK; Anschluss an Pensionskasse Post (37'516 Aktive, 28'703 Rentner Konzern). Vorsorgeaufwand PostFinance 2025: 46 Mio. CHF (2024: 44 Mio. CHF); AGBR: 36 Mio. CHF.",
        "source_url_or_file": "postfinance/.md/postfinance-geschaeftsbericht-2025.md (Anhang Ziff. 15, S. 77)",
    },
    {
        "bank_id": "ubs",
        "short_name": "UBS",
        "pk_name": "Pensionskasse der UBS (+ Credit Suisse Swiss Plan)",
        "pk_plan_type": "Beitragsprimat (IAS 19: Defined Benefit)",
        "accounting_basis": "IFRS / IAS 19 (vs. BVV 2 lokal)",
        "reference_year": 2025,
        "active_insured_count": None,
        "pensioners_count": None,
        "active_to_pensioner_ratio": None,
        "pk_assets_mio": None,
        "coverage_ratio_bvg_pct": None,
        "technical_interest_rate_pct": None,
        "interest_crediting_pct": None,
        "conversion_rate_65_pct": None,
        "employer_contribution_mio": None,
        "employer_share_pct": None,
        "employer_contribution_reserve_mio": None,
        "extraordinary_contributions_mio": 0.0,
        "notes": "Konzernrechnung weist Schweizer Pläne (UBS Swiss Plan & CS Swiss Plan) nach IAS 19 aus (Note 25/26); direkter Vergleich mit FER-16-Banken erfordert BVG-Deckungsgrad gemäss Art. 44 BVV 2.",
        "source_url_or_file": "ubs/.md/ubs-geschaeftsbericht-2025.md (Note 25 Post-employment benefit plans, S. 339)",
    },
]


def export_vorsorge_data() -> Path:
    comp_data = REPO_ROOT / "comparison" / "data"
    comp_data.mkdir(parents=True, exist_ok=True)
    for rec in VORSORGE_RECORDS:
        b = rec["bank_id"]
        b_data = REPO_ROOT / b / "data"
        b_data.mkdir(parents=True, exist_ok=True)
        (b_data / f"{b}_vorsorge.json").write_text(
            json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    csv_path = comp_data / "xkb_vorsorgeeinrichtungen.csv"
    cols = list(VORSORGE_RECORDS[0].keys())
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(VORSORGE_RECORDS)
    print(f"[OK] Vorsorgeeinrichtungen: {len(VORSORGE_RECORDS)} Institute nach {csv_path} exportiert.")
    return csv_path


if __name__ == "__main__":
    export_vorsorge_data()
