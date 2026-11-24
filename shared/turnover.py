#!/usr/bin/env python3
"""Strukturierter Datensatz der offengelegten Personalfluktuationen (Employee Turnover) pro Jahr.

Quellenbasis: Primär die Geschäfts-, Personal- und Nachhaltigkeitsberichte (GRI 401-1)
in `banks/<bank>/.md/`. Nicht im Geschäftsbericht ausgewiesene Jahrgänge bleiben `None` (keine Schätzwerte).
Bei Instituten, die sowohl Netto- (freiwillige/natürliche Fluktuation exkl. Pensionierungen/interne Übertritte)
als auch Brutto-/Gesamtfluktuation ausweisen, ist `turnover_rate_pct` die primär berichtete Steuerungsgrösse
und `turnover_gross_pct` bzw. `turnover_net_pct` sind separat dokumentiert.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from shared.config import REPO_ROOT, VALID_BANKS, load_bank_config

# Struktur: bank_id -> {
#   "basis": Methodik / Definition der Hauptreihe,
#   "source": Primärquellen-Referenz,
#   "years": { year: {"rate": float, "net": float | None, "gross": float | None, "note": str} }
# }
TURNOVER_DATA: dict[str, dict[str, Any]] = {
    "bcv": {
        "basis": "Taux moyen de rotation (Stammhaus; ab 2021 explizit exkl. Pensionierungen / hors départs en retraite)",
        "source": "bcv/.md/bcv-geschaeftsbericht-2007..2025.md (Kapitel «La BCV et ses missions / Ressources humaines»)",
        "years": {
            2006: {"rate": 11.8, "net": None, "gross": 11.8, "note": "Taux moyen de rotation (Vorjahreswert aus GB 2007)"},
            2007: {"rate": 12.8, "net": None, "gross": 12.8, "note": "Taux moyen de rotation (inkl. Pensionierungen)"},
            2008: {"rate": 11.3, "net": None, "gross": 11.3, "note": "Taux moyen de rotation"},
            2009: {"rate": 9.3, "net": None, "gross": 9.3, "note": "Taux moyen de rotation"},
            2010: {"rate": 9.8, "net": None, "gross": 9.8, "note": "Taux moyen de rotation"},
            2011: {"rate": 10.4, "net": None, "gross": 10.4, "note": "Taux moyen de rotation"},
            2012: {"rate": 9.4, "net": None, "gross": 9.4, "note": "Taux moyen de rotation"},
            2013: {"rate": 8.7, "net": None, "gross": 8.7, "note": "Taux moyen de rotation"},
            2014: {"rate": 9.2, "net": None, "gross": 9.2, "note": "Taux moyen de rotation"},
            2015: {"rate": 8.4, "net": None, "gross": 8.4, "note": "Taux moyen de rotation"},
            2016: {"rate": 8.4, "net": None, "gross": 8.4, "note": "Taux moyen de rotation"},
            2017: {"rate": 10.5, "net": None, "gross": 10.5, "note": "Taux moyen de rotation"},
            2018: {"rate": 9.8, "net": None, "gross": 9.8, "note": "Taux moyen de rotation"},
            2019: {"rate": 8.5, "net": None, "gross": 8.5, "note": "Taux moyen de rotation"},
            2020: {"rate": 8.8, "net": None, "gross": 8.8, "note": "Taux moyen de rotation"},
            2021: {"rate": 8.0, "net": 8.0, "gross": None, "note": "Taux moyen de rotation hors départs en retraite"},
            2022: {"rate": 9.5, "net": 9.5, "gross": None, "note": "Taux moyen de rotation hors départs en retraite"},
            2023: {"rate": 8.6, "net": 8.6, "gross": None, "note": "Taux moyen de rotation hors départs en retraite"},
            2024: {"rate": 7.7, "net": 7.7, "gross": None, "note": "Taux moyen de rotation hors départs en retraite"},
            2025: {"rate": 6.9, "net": 6.9, "gross": None, "note": "Taux moyen de rotation hors départs en retraite"},
        },
    },
    "bekb": {
        "basis": "Fluktuationsrate netto (GRI G4-LA1 / GRI 401-1: fest angestellte Mitarbeitende ohne Lernende im Jahresdurchschnitt; ab NHB 2022 ganzzahlig gerundet)",
        "source": "BEKB Nachhaltigkeitsberichte 2015 (S. 36), 2020 (S. 26), 2022 (S. 60), 2024 (S. 78/80) & 2025 (S. 77/79) – GRI G4-LA1 / GRI 401-1",
        "years": {
            2011: {"rate": 6.7, "net": 6.7, "gross": None, "note": "Fluktuationsrate netto Festangestellte exkl. Lernende & Aushilfen (NHB 2015 S. 36)"},
            2012: {"rate": 5.4, "net": 5.4, "gross": None, "note": "Fluktuationsrate netto Festangestellte exkl. Lernende & Aushilfen (NHB 2015 S. 36)"},
            2013: {"rate": 7.3, "net": 7.3, "gross": None, "note": "Fluktuationsrate netto Festangestellte exkl. Lernende & Aushilfen (NHB 2015 S. 36)"},
            2014: {"rate": 8.8, "net": 8.8, "gross": None, "note": "Fluktuationsrate netto Festangestellte exkl. Lernende & Aushilfen (NHB 2015 S. 36)"},
            2015: {"rate": 7.9, "net": 7.9, "gross": None, "note": "Fluktuationsrate netto (Frauen: 7,8 %, Männer: 8,0 %; NHB 2015 S. 36)"},
            2016: {"rate": 8.6, "net": 8.6, "gross": None, "note": "Fluktuationsrate netto (100 Austritte netto; Frauen: 10,4 %, Männer: 7,2 %; NHB 2020 S. 26)"},
            2017: {"rate": 6.3, "net": 6.3, "gross": None, "note": "Fluktuationsrate netto (71 Austritte netto; Frauen: 8,5 %, Männer: 4,6 %; NHB 2020 S. 26)"},
            2018: {"rate": 10.1, "net": 10.1, "gross": None, "note": "Fluktuationsrate netto (113 Austritte netto; Frauen: 11,2 %, Männer: 9,2 %; NHB 2020 S. 26; im NHB 2022 gerundet 10 %)"},
            2019: {"rate": 8.0, "net": 8.0, "gross": None, "note": "Fluktuationsrate netto (90 Austritte netto; Frauen: 9,2 %, Männer: 7,1 %; NHB 2020 S. 26 / NHB 2022 S. 60)"},
            2020: {"rate": 5.9, "net": 5.9, "gross": None, "note": "Fluktuationsrate netto (65 Austritte netto; Frauen: 5,8 %, Männer: 6,0 %; NHB 2020 S. 26; im NHB 2022/2024 gerundet 6 %)"},
            2021: {"rate": 7.0, "net": 7.0, "gross": None, "note": "Fluktuationsrate netto (79 Austritte netto; Frauen: 7 %, Männer: 7 %; NHB 2025 S. 77)"},
            2022: {"rate": 9.0, "net": 9.0, "gross": None, "note": "Fluktuationsrate netto (94 Austritte netto; Frauen: 10 %, Männer: 8 %; NHB 2025 S. 77)"},
            2023: {"rate": 9.0, "net": 9.0, "gross": None, "note": "Fluktuationsrate netto BEKB (84 Austritte netto; Frauen: 10 %, Männer: 7 %); IT-Tochter aity AG: 7 % (17 Austritte; NHB 2025 S. 77/79)"},
            2024: {"rate": 6.0, "net": 6.0, "gross": None, "note": "Fluktuationsrate netto BEKB (67 Austritte netto; Frauen: 8 %, Männer: 5 %); IT-Tochter aity AG: 2 % (6 Austritte; NHB 2025 S. 77/79)"},
            2025: {"rate": 7.0, "net": 7.0, "gross": None, "note": "Fluktuationsrate netto BEKB (83 Austritte netto; Frauen: 8 %, Männer: 7 %); IT-Tochter aity AG: 2 % (6 Austritte; NHB 2025 S. 77/79)"},
        },
    },
    "blkb": {
        "basis": "Natürliche / Netto-Fluktuationsrate (GRI G4-LA1 / GRI 401-1: exkl. Arbeitgeberkündigung, Pensionierungen, Schwangerschaften & Todesfälle; 2013–2025) bzw. einfache Fluktuationsrate (GRI G3 LA2, 2006–2012)",
        "source": "blkb/.md/blkb-geschaeftsbericht-2007..2021.md & BLKB Nachhaltigkeitsberichte 2010, 2013, 2014, 2017, 2021, 2022, 2023, 2024 & 2025 (GRI 401-1)",
        "years": {
            2006: {"rate": 6.1, "net": None, "gross": 6.1, "note": "Einfache Fluktuationsrate (Vorjahreswert aus GB 2007)"},
            2007: {"rate": 7.8, "net": None, "gross": 7.8, "note": "Einfache Fluktuationsrate (GRI G3 LA2)"},
            2008: {"rate": 7.4, "net": None, "gross": 7.4, "note": "Einfache Fluktuationsrate (GRI G3 LA2)"},
            2009: {"rate": 4.8, "net": None, "gross": 4.8, "note": "Einfache Fluktuationsrate (GRI G3 LA2)"},
            2010: {"rate": 4.8, "net": None, "gross": 4.8, "note": "Fluktuationsrate (GRI-Berichterstattung 2010 S. 16, LA2)"},
            2012: {"rate": 3.6, "net": None, "gross": 3.6, "note": "Einfache Fluktuationsrate (GNB 2013 S. 73, GRI G3.1 LA2)"},
            2013: {"rate": 3.3, "net": 3.3, "gross": None, "note": "Netto-Fluktuationsrate ohne Pensionierungen, Schwangerschaften & Todesfälle (GNB 2013 S. 20/73 & GNB 2017 S. 24)"},
            2014: {"rate": 4.1, "net": 4.1, "gross": None, "note": "Fluktuationsrate ohne Pensionierungen, Schwangerschaften & Todesfälle (GNB 2014 S. 14 & GNB 2017 S. 24)"},
            2015: {"rate": 4.5, "net": 4.5, "gross": None, "note": "Fluktuation ohne Pensionierungen, Schwangerschaften & Todesfälle (GNB 2017 S. 24, GRI G4-LA1)"},
            2016: {"rate": 4.6, "net": 4.6, "gross": None, "note": "Fluktuation ohne Pensionierungen, Schwangerschaften & Todesfälle (GNB 2017 S. 24, GRI G4-LA1)"},
            2017: {"rate": 5.0, "net": 5.0, "gross": None, "note": "Natürliche Fluktuation Stammhaus (GNB 2017 S. 24 & NHB 2021 S. 71, GRI 401-1)"},
            2018: {"rate": 5.3, "net": 5.3, "gross": None, "note": "Natürliche Fluktuation Stammhaus (NHB 2021 S. 71 & NHB 2022 S. 56, GRI 401-1)"},
            2019: {"rate": 6.3, "net": 6.3, "gross": None, "note": "Natürliche Fluktuation Stammhaus (GB 2020/2021 & NHB 2022 S. 56, GRI 401-1)"},
            2020: {"rate": 5.3, "net": 5.3, "gross": None, "note": "Natürliche Fluktuation Stammhaus (GB 2020/2021 & NHB 2022 S. 56, GRI 401-1)"},
            2021: {"rate": 5.6, "net": 5.6, "gross": None, "note": "Natürliche Fluktuation Stammhaus (GB 2021 & NHB 2022 S. 56, GRI 401-1)"},
            2022: {"rate": 6.3, "net": 6.3, "gross": None, "note": "Natürliche Fluktuation Stammhaus (NHB 2022 S. 56 & NHB 2024 S. 12, GRI 401-1)"},
            2023: {"rate": 7.4, "net": 7.4, "gross": 10.7, "note": "Fluktuationsrate Konzern netto 7,4 % (im NHB 2023/2024: 7,5 %), brutto 10,7 % (NHB 2025 S. 35, GRI 401-1)"},
            2024: {"rate": 5.8, "net": 5.8, "gross": 10.4, "note": "Fluktuationsrate Konzern netto 5,8 % (im NHB 2024: 6,1 %), brutto 10,4 % (NHB 2025 S. 35, GRI 401-1)"},
            2025: {"rate": 7.8, "net": 7.8, "gross": 11.9, "note": "Fluktuationsrate Konzern netto 7,8 % (exkl. AG-Kündigung, Pensionierungen, Schwangerschaften, Todesfälle), brutto 11,9 % (NHB 2025 S. 35, GRI 401-1)"},
        },
    },
    "fkb": {
        "basis": "Fluktuationsrate netto insgesamt in % (GRI 401-1: Rotationsrate des Personals, Zielwert < 5 %)",
        "source": "FKB Nachhaltigkeitsberichte 2023 (S. 54), 2024 (S. 35/54, rdd-fkb-2024.pdf) & 2025 (esg.bcf.ch) – GRI 401-1",
        "years": {
            2019: {"rate": 3.82, "net": 3.82, "gross": None, "note": "Fluktuationsrate netto 3,82 % (18 Austritte netto; NHB 2023 S. 54)"},
            2020: {"rate": 1.91, "net": 1.91, "gross": None, "note": "Fluktuationsrate netto 1,91 % (9 Austritte netto; NHB 2023/2024 S. 54)"},
            2021: {"rate": 2.29, "net": 2.29, "gross": None, "note": "Fluktuationsrate netto 2,29 % (12 Austritte netto; NHB 2023/2024 S. 54)"},
            2022: {"rate": 4.02, "net": 4.02, "gross": None, "note": "Fluktuationsrate netto 4,02 % (18 Austritte netto; NHB 2023/2024 S. 54)"},
            2023: {"rate": 2.6, "net": 2.6, "gross": None, "note": "Fluktuationsrate netto 2,6 % (12 Austritte netto, 67 Neueinstellungen; NHB 2023/2024 S. 54)"},
            2024: {"rate": 3.1, "net": 3.1, "gross": None, "note": "Fluktuationsrate netto 3,1 % (17 Austritte netto, 62 Neueinstellungen; NHB 2024 S. 35/54)"},
            2025: {"rate": 4.6, "net": 4.6, "gross": None, "note": "Fluktuationsrate netto 4,6 % (bei 602 Mitarbeitenden; FKB Nachhaltigkeitsbericht 2025 / esg.bcf.ch)"},
        },
    },
    "gekb": {
        "basis": "Taux de rotation du personnel BCGE Maison-mère (GRI 401-1: nombre de départs / effectif moyen)",
        "source": "gekb/.md/gekb-geschaeftsbericht-2023.md & BCGE Rapports RSE 2024 (p. 52/61) & 2025 (p. 67/72) – GRI 401-1",
        "years": {
            2022: {
                "rate": 9.27,
                "net": None,
                "gross": 9.27,
                "note": "BCGE Maison-mère GRI 401-1: 9,27 % (Frauen 11,32 %, Männer 7,89 %; im Rapport RSE 2023 exkl. Lernende: 9,08 %; BCGE France: 14 %)",
            },
            2023: {
                "rate": 10.10,
                "net": None,
                "gross": 10.10,
                "note": "BCGE Maison-mère GRI 401-1: 10,10 % (Frauen 10,16 %, Männer 10,06 %; im Rapport RSE 2023 exkl. Lernende: 9,83 %; BCGE France: 23 %)",
            },
            2024: {
                "rate": 8.3,
                "net": None,
                "gross": 8.3,
                "note": "BCGE Maison-mère GRI 401-1: 8,3 % (Frauen 10,16 %, Männer 7,04 %; BCGE France: 13 %; Rapport RSE 2024 p. 52 / 2025 p. 67)",
            },
            2025: {
                "rate": 9.73,
                "net": None,
                "gross": 9.73,
                "note": "BCGE Maison-mère GRI 401-1: 9,73 % vs. Ziel ≤ 10 % (Frauen 9,78 %, Männer 9,70 %; BCGE France: 15 %; Rapport RSE 2025 p. 58/67)",
            },
        },
    },
    "lukb": {
        "basis": "Netto-Fluktuationsrate Konzern (freiwillige Fluktuation exkl. Pensionierungen, befristete Verträge, Lernende & familiäre Gründe, GRI 401-1)",
        "source": "lukb/.md/lukb-geschaeftsbericht-2017..2023.md & LUKB-Nachhaltigkeitsberichte 2024 (S. 57/69) & 2025 (S. 77/94) – GRI 401-1",
        "years": {
            2016: {"rate": 3.6, "net": 3.6, "gross": None, "note": "Netto-Fluktuationsrate (Vorjahreswert aus GB 2017)"},
            2017: {"rate": 3.3, "net": 3.3, "gross": None, "note": "Netto-Fluktuationsrate exkl. Pensionierungen & familiäre Gründe"},
            2018: {"rate": 4.1, "net": 4.1, "gross": None, "note": "Netto-Fluktuationsrate exkl. Pensionierungen & familiäre Gründe"},
            2019: {"rate": 4.8, "net": 4.8, "gross": None, "note": "Netto-Fluktuationsrate exkl. Pensionierungen & familiäre Gründe"},
            2020: {"rate": 4.1, "net": 4.1, "gross": None, "note": "Netto-Fluktuationsrate exkl. Pensionierungen & familiäre Gründe"},
            2021: {"rate": 3.7, "net": 3.7, "gross": None, "note": "Netto-Fluktuationsrate exkl. Pensionierungen & familiäre Gründe"},
            2022: {"rate": 5.5, "net": 5.5, "gross": 8.2, "note": "Netto-Fluktuationsrate 5,5 % (Frauen 6,3 %, Männer 4,3 %); Brutto-Fluktuationsrate 8,2 % (NHB 2024 S. 69)"},
            2023: {"rate": 4.5, "net": 4.5, "gross": 7.9, "note": "Netto-Fluktuationsrate 4,5 % (Frauen 4,8 %, Männer 4,3 %); Brutto-Fluktuationsrate 7,9 % (NHB 2025 S. 94)"},
            2024: {"rate": 3.2, "net": 3.2, "gross": 6.5, "note": "Netto-Fluktuationsrate 3,2 % (Frauen 5,5 %, Männer 4,4 %); Brutto-Fluktuationsrate 6,5 % (NHB 2024 S. 69 / NHB 2025 S. 94)"},
            2025: {"rate": 4.3, "net": 4.3, "gross": 7.8, "note": "Netto-Fluktuationsrate 4,3 % (Frauen 4,2 %, Männer 3,8 %); Brutto-Fluktuationsrate 7,8 % (NHB 2025 S. 77/94)"},
        },
    },
    "migrosbank": {
        "basis": "Bruttofluktuationsrate in % (natürliche Austritte ohne ordentliche Pensionierungen, befristete Verträge, Tod & interne Wechsel / Ø Monatslohn-Bestand Schweiz)",
        "source": "Migros Bank Nachhaltigkeitsberichte 2024 (S. 24) & 2025 (S. 23, Kapitel «Mitarbeitende – Fluktuationsrate»)",
        "years": {
            2024: {
                "rate": 13.5,
                "net": 13.5,
                "gross": 13.5,
                "note": "Fluktuationsrate 13,5 % (natürliche Austritte exkl. ordentliche Pensionierungen, befristete Verträge & Tod; Zielband 8–15 %; NHB 2024 S. 24 / NHB 2025 S. 23)",
            },
            2025: {
                "rate": 11.1,
                "net": 11.1,
                "gross": 11.1,
                "note": "Fluktuationsrate 11,1 % (natürliche Austritte exkl. ordentliche Pensionierungen, befristete Verträge & Tod; Zielband 8–15 %; NHB 2025 S. 23)",
            },
        },
    },
    "pictet": {
        "basis": "Global employee turnover rate in % (GRI 401-1: total leavers / average active headcount over 12 months)",
        "source": "Pictet Group Sustainability Reports 2023 (p. 45/70), 2024 (p. 32/119) & 2025 (p. 41/149) – GRI 401-1",
        "years": {
            2023: {
                "rate": 7.1,
                "net": None,
                "gross": 7.1,
                "note": "Global employee turnover 7,1 % (Frauen 7,7 %, Männer 6,7 %; <30 J.: 10,0 %, 30–50 J.: 6,1 %, 50+ J.: 8,4 %; GSR 2023 p. 45/70)",
            },
            2024: {
                "rate": 6.9,
                "net": None,
                "gross": 6.9,
                "note": "Global employee turnover 6,9 % (361 leavers permanent: 144 women, 217 men; GSR 2024 p. 32/119 & GSR 2025 p. 149)",
            },
            2025: {
                "rate": 8.2,
                "net": None,
                "gross": 8.2,
                "note": "Global employee turnover 8,2 % (total leavers / average headcount over 12 months; GSR 2025 p. 41/149)",
            },
        },
    },
    "raiffeisen": {
        "basis": "Nettofluktuationsrate (freiwillige Austritte exkl. Gruppenübertritte, ab 2022) bzw. Brutto-/Gesamtfluktuationsrate (2012–2025)",
        "source": "raiffeisen/.md/raiffeisen-geschaeftsbericht-2013..2025.md (Sozialbilanz / Kennzahlen Mitarbeitende / GRI 401-1)",
        "years": {
            2012: {"rate": 10.0, "net": None, "gross": 10.0, "note": "Bruttofluktuationsrate inkl. Mutationen innerhalb der Gruppe (aus GB 2013)"},
            2013: {"rate": 11.8, "net": None, "gross": 11.8, "note": "Bruttofluktuationsrate inkl. Mutationen (Schlüsselpersonen: 2,9 %)"},
            2014: {"rate": 12.3, "net": None, "gross": 12.3, "note": "Bruttofluktuationsrate inkl. Mutationen (Schlüsselpersonen: 3,4 %)"},
            2015: {"rate": 10.7, "net": None, "gross": 10.7, "note": "Bruttofluktuationsrate inkl. Mutationen (Schlüsselpersonen: 5,4 %)"},
            2016: {"rate": 11.2, "net": None, "gross": 11.2, "note": "Bruttofluktuationsrate inkl. Mutationen (Top-Management: 2,0 %)"},
            2017: {"rate": 12.5, "net": None, "gross": 12.5, "note": "Bruttofluktuationsrate inkl. Mutationen (Top-Management: 1,0 %)"},
            2018: {"rate": 12.1, "net": None, "gross": 12.1, "note": "Bruttofluktuationsrate inkl. Übertritte (Top-Management: 1,0 %)"},
            2019: {"rate": 14.3, "net": 2.1, "gross": 14.3, "note": "Bruttofluktuationsrate 14,3 % (inkl. Gruppengesellschaften); BSC-Zielgrösse Netto: 2,1 %"},
            2020: {"rate": 11.1, "net": None, "gross": 11.1, "note": "Bruttofluktuationsrate inkl. Übertritte innerhalb der Gruppe"},
            2021: {"rate": 10.4, "net": None, "gross": 10.4, "note": "Bruttofluktuationsrate inkl. Übertritte innerhalb der Gruppe"},
            2022: {"rate": 10.0, "net": 10.0, "gross": 12.3, "note": "Nettofluktuationsrate 10,0 % (Gesamtfluktuation exkl. Übertritte: 12,3 %; inkl. Übertritte: 12,2 %)"},
            2023: {"rate": 8.5, "net": 8.5, "gross": 12.1, "note": "Nettofluktuationsrate 8,5 % (freiwillige Austritte); Gesamtfluktuationsrate: 12,1 %"},
            2024: {"rate": 8.4, "net": 8.4, "gross": 10.2, "note": "Nettofluktuationsrate 8,4 % (freiwillige Austritte); Gesamtfluktuationsrate: 10,2 %"},
            2025: {"rate": 7.4, "net": 7.4, "gross": 9.7, "note": "Nettofluktuationsrate 7,4 % (freiwillige Austritte); Gesamtfluktuationsrate: 9,7 %"},
        },
    },
    "sgkb": {
        "basis": "Personalfluktuationsrate in % (freiwillige Fluktuation exkl. Pensionierungen und befristete Verträge, GRI 401-1)",
        "source": "sgkb/.md/sgkb-geschaeftsbericht-2018..2025.md (Personalkennzahlen & Nachhaltigkeitsbericht GRI 401-1)",
        "years": {
            2016: {"rate": 6.8, "net": 6.8, "gross": None, "note": "Fluktuation in % (Mehrjahrestabelle GB 2018)"},
            2017: {"rate": 6.9, "net": 6.9, "gross": None, "note": "Fluktuation in % (Mehrjahrestabelle GB 2018/2019)"},
            2018: {"rate": 5.6, "net": 5.6, "gross": None, "note": "Fluktuation in %"},
            2019: {"rate": 5.1, "net": 5.1, "gross": None, "note": "Fluktuation in %"},
            2020: {"rate": 6.6, "net": 6.6, "gross": None, "note": "Fluktuation in %"},
            2021: {"rate": 4.6, "net": 4.6, "gross": None, "note": "Fluktuation in %"},
            2022: {"rate": 8.9, "net": 8.9, "gross": None, "note": "Freiwillige Personalfluktuationsrate (143 Austritte gesamt)"},
            2023: {"rate": 7.3, "net": 7.3, "gross": None, "note": "Freiwillige Personalfluktuationsrate (144 Austritte gesamt)"},
            2024: {"rate": 6.8, "net": 6.8, "gross": None, "note": "Freiwillige Personalfluktuationsrate (135 Austritte gesamt)"},
            2025: {"rate": 7.74, "net": 7.74, "gross": None, "note": "Freiwillige Personalfluktuationsrate 7,74 % (gerundet 7,7 %; 148 Austritte gesamt)"},
        },
    },
    "ubs": {
        "basis": "Voluntary employee turnover rate in % (UBS Group; Gesamtfluktuation inkl. unfreiwilliger & neutraler Austritte in `gross`)",
        "source": "UBS Group Sustainability Report Supplement 2024 (p. 32) & 2025 (GRI 401-1: Voluntary and involuntary employee turnover)",
        "years": {
            2022: {
                "rate": 12.6,
                "net": 12.6,
                "gross": 15.9,
                "note": "Voluntary turnover 12,6 %; Involuntary turnover 2,5 %; Overall turnover 15,9 % (Frauen 15,4 %, Männer 16,2 %; Director+ 10,9 %)",
            },
            2023: {
                "rate": 12.4,
                "net": 12.4,
                "gross": 18.6,
                "note": "Voluntary turnover 12,4 %; Involuntary turnover 5,3 %; Overall turnover 18,6 % im Zuge der CS-Übernahme (Frauen 18,7 %, Männer 18,6 %)",
            },
            2024: {
                "rate": 7.9,
                "net": 7.9,
                "gross": 12.8,
                "note": "Voluntary turnover 7,9 %; Involuntary turnover 4,1 %; Overall turnover 12,8 % (Frauen 13,3 %, Männer 12,5 %; Director+ 12,3 %)",
            },
            2025: {
                "rate": 7.1,
                "net": 7.1,
                "gross": 12.6,
                "note": "Voluntary turnover 7,1 %; Involuntary turnover 4,9 %; Overall turnover 12,6 % (UBS Sustainability Report Supplement 2025)",
            },
        },
    },
    "valiant": {
        "basis": "Nettofluktuationsrate in % (alle durch Arbeitnehmende oder Arbeitgeber initiierten Austritte inkl. vorzeitiger Pensionierung auf eigenen Wunsch, GRI 401-1)",
        "source": "valiant/.md/valiant-geschaeftsbericht-2016..2023.md & Valiant Nachhaltigkeitsberichte 2023 (S. 66), 2024 (S. 76) & 2025 (S. 83)",
        "years": {
            2014: {"rate": 13.2, "net": 13.2, "gross": None, "note": "Fluktuationsrate (Mehrjahrestabelle GB 2016)"},
            2015: {"rate": 14.1, "net": 14.1, "gross": None, "note": "Fluktuationsrate (Mehrjahrestabelle GB 2016/2017)"},
            2016: {"rate": 11.9, "net": 11.9, "gross": None, "note": "Nettofluktuationsrate"},
            2017: {"rate": 11.7, "net": 11.7, "gross": None, "note": "Nettofluktuationsrate"},
            2018: {"rate": 13.2, "net": 13.2, "gross": None, "note": "Nettofluktuationsrate"},
            2019: {"rate": 12.5, "net": 12.5, "gross": None, "note": "Nettofluktuationsrate"},
            2020: {"rate": 11.0, "net": 11.0, "gross": None, "note": "Nettofluktuationsrate"},
            2021: {"rate": 10.5, "net": 10.5, "gross": None, "note": "Nettofluktuationsrate (172 Neueintritte; NHB 2023 S. 66)"},
            2022: {"rate": 11.9, "net": 11.9, "gross": None, "note": "Nettofluktuationsrate (113 Neueintritte; NHB 2024 S. 76)"},
            2023: {"rate": 12.0, "net": 12.0, "gross": None, "note": "Nettofluktuationsrate (162 Neueintritte; NHB 2025 S. 83)"},
            2024: {"rate": 13.1, "net": 13.1, "gross": None, "note": "Nettofluktuationsrate (160 Neueintritte; NHB 2024 S. 76 / NHB 2025 S. 83)"},
            2025: {"rate": 9.4, "net": 9.4, "gross": None, "note": "Nettofluktuationsrate (144 Neueintritte; NHB 2025 S. 83)"},
        },
    },
    "vontobel": {
        "basis": "Employee turnover rate in % (GRI 401-1: permanent employees leaving / average permanent headcount)",
        "source": "vontobel/.md/vontobel-geschaeftsbericht-2020..2025.md (Sustainability Report – Great workplace in figures, GRI 401-1)",
        "years": {
            2018: {"rate": 11.4, "net": None, "gross": 11.4, "note": "Employee turnover rate exkl. Notenstein La Roche (aus GB 2020)"},
            2019: {"rate": 14.2, "net": None, "gross": 14.2, "note": "Employee turnover rate (aus GB 2020)"},
            2020: {"rate": 11.1, "net": None, "gross": 11.1, "note": "Employee turnover rate (234 leavers: 89 women, 145 men)"},
            2022: {"rate": 9.8, "net": None, "gross": 9.8, "note": "Employee turnover rate (Women 10,5 %, Men 9,5 %; Schweiz 9,9 %)"},
            2023: {"rate": 11.6, "net": None, "gross": 11.6, "note": "Employee turnover rate (269 leavers: 100 women / 13,4 %, 169 men / 10,7 %)"},
            2024: {"rate": 11.4, "net": None, "gross": 11.4, "note": "Employee turnover rate (268 leavers: 110 women / 14,2 %, 158 men / 10,0 %)"},
            2025: {"rate": 10.8, "net": None, "gross": 10.8, "note": "Employee turnover rate (255 leavers: 96 women / 12,2 %, 159 men / 10,1 %)"},
        },
    },
    "vskb": {
        "basis": "Netto-Fluktuationsrate (exkl. Pensionierungen & Mutterschaft, 2016–2024) bzw. GRI 401-1 Taux de rotation du personnel (inkl. Brutto-Ausweis 2021–2025)",
        "source": "vskb/.md/vskb-geschaeftsbericht-2007..2024.md & BCVS Rapports RSE / CSR Reports 2023 (p. 63), 2024 (p. 38) & 2025 (p. 24) – GRI 401-1",
        "years": {
            2003: {"rate": 5.43, "net": None, "gross": 5.43, "note": "Personalwechselquote (Mehrjahresgrafik GB 2009)"},
            2004: {"rate": 4.44, "net": None, "gross": 4.44, "note": "Personalwechselquote (Mehrjahresgrafik GB 2009/2010)"},
            2005: {"rate": 4.89, "net": None, "gross": 4.89, "note": "Personalwechselquote (Mehrjahresgrafik GB 2009/2010)"},
            2006: {"rate": 3.79, "net": None, "gross": 3.79, "note": "Personalwechselquote (Mehrjahresgrafik GB 2009/2010)"},
            2007: {"rate": 4.04, "net": None, "gross": 4.04, "note": "Personalwechselquote 4,04 % in Mehrjahresgrafik (im Text GB 2007: 5,11 %)"},
            2008: {"rate": 3.29, "net": None, "gross": 3.29, "note": "Personalwechselquote (Mehrjahresgrafik GB 2009/2010)"},
            2009: {"rate": 5.59, "net": None, "gross": 5.59, "note": "Personalwechselquote 5,59 % (gerundet 5,6 %)"},
            2010: {"rate": 2.87, "net": None, "gross": 2.87, "note": "Personalwechselquote 2,87 % (gerundet 2,9 %)"},
            2014: {"rate": 6.8, "net": None, "gross": 6.8, "note": "Personalwechselrate (inkl. zahlreicher Pensionierungen)"},
            2015: {"rate": 5.5, "net": None, "gross": 5.5, "note": "Personalwechselquote (inkl. Pensionierungen)"},
            2016: {"rate": 3.1, "net": 3.1, "gross": 6.8, "note": "Netto 3,1 % (exkl. Pensionierungen & Mutterschaft); Brutto 6,8 %"},
            2017: {"rate": 2.3, "net": 2.3, "gross": 5.2, "note": "Netto 2,3 % (exkl. Pensionierungen & Mutterschaft); Brutto 5,2 %"},
            2018: {"rate": 3.9, "net": 3.9, "gross": 5.9, "note": "Netto 3,9 % (exkl. Pensionierungen & Mutterschaft); Brutto 5,9 %"},
            2021: {"rate": 6.46, "net": 6.46, "gross": 10.79, "note": "Netto-Fluktuationsrate 6,46 % (33 Austritte, GB 2021); GRI 401-1 Taux de rotation (inkl. Lernende): 10,79 % (Rapport RSE 2023/2024)"},
            2022: {"rate": 7.01, "net": 7.01, "gross": 11.31, "note": "Netto-Fluktuationsrate 7,01 % (GB 2022); GRI 401-1 Taux de rotation (inkl. Lernende): 11,31 % (Rapport RSE 2023–2025)"},
            2023: {"rate": 6.64, "net": 6.64, "gross": 11.53, "note": "Netto-Fluktuationsrate 6,64 % (GB 2023); GRI 401-1 Taux de rotation (inkl. Lernende): 11,53 % (Rapport RSE 2023–2025)"},
            2024: {"rate": 3.64, "net": 3.64, "gross": 8.05, "note": "Netto-Fluktuationsrate 3,64 % (GB 2024); GRI 401-1 Taux de rotation (inkl. Lernende): 8,05 % (Rapport RSE 2024/2025)"},
            2025: {"rate": 7.99, "net": None, "gross": 7.99, "note": "GRI 401-1 Staff turnover rate (inkl. Lernende): 7,99 % (65 Neueintritte; BCVS CSR Report 2025 p. 24)"},
        },
    },
    "zkb": {
        "basis": "Fluktuationsrate Stammhaus in % (Personalbericht / Kennzahlen Beschäftigung)",
        "source": "zkb/.md/zkb-geschaeftsbericht-2014..2025.md (Kapitel «Mitarbeitende / Unternehmensprofil»)",
        "years": {
            2010: {"rate": 6.4, "net": None, "gross": 6.4, "note": "Fluktuationsrate Stammhaus (Mehrjahrestabelle GB 2014)"},
            2011: {"rate": 6.5, "net": None, "gross": 6.5, "note": "Fluktuationsrate Stammhaus (Mehrjahrestabelle GB 2014/2015)"},
            2012: {"rate": 6.5, "net": None, "gross": 6.5, "note": "Fluktuationsrate Stammhaus (Mehrjahrestabelle GB 2014–2016)"},
            2013: {"rate": 7.7, "net": None, "gross": 7.7, "note": "Fluktuationsrate Stammhaus (Mehrjahrestabelle GB 2014–2017)"},
            2014: {"rate": 7.7, "net": None, "gross": 7.7, "note": "Fluktuationsrate Stammhaus"},
            2015: {"rate": 6.8, "net": None, "gross": 6.8, "note": "Fluktuationsrate Stammhaus"},
            2016: {"rate": 5.9, "net": None, "gross": 5.9, "note": "Fluktuationsrate Stammhaus"},
            2017: {"rate": 5.7, "net": None, "gross": 5.7, "note": "Fluktuationsrate Stammhaus"},
            2018: {"rate": 6.3, "net": None, "gross": 6.3, "note": "Fluktuationsrate Stammhaus"},
            2019: {"rate": 5.8, "net": None, "gross": 5.8, "note": "Fluktuationsrate Stammhaus"},
            2020: {"rate": 4.5, "net": None, "gross": 4.5, "note": "Fluktuationsrate Stammhaus"},
            2021: {"rate": 5.9, "net": None, "gross": 5.9, "note": "Fluktuationsrate Stammhaus"},
            2022: {"rate": 6.4, "net": None, "gross": 6.4, "note": "Fluktuationsrate Stammhaus"},
            2023: {"rate": 6.1, "net": None, "gross": 6.1, "note": "Fluktuationsrate Stammhaus"},
            2024: {"rate": 5.5, "net": None, "gross": 5.5, "note": "Fluktuationsrate Stammhaus"},
            2025: {"rate": 5.0, "net": None, "gross": 5.0, "note": "Fluktuationsrate Stammhaus"},
        },
    },
}


def get_bank_turnover_meta(bank_id: str) -> dict[str, Any]:
    return TURNOVER_DATA.get(bank_id, {"basis": "Nicht im Geschäftsbericht ausgewiesen", "source": "–", "years": {}})


def get_turnover_for_year(bank_id: str, year: int) -> dict[str, Any] | None:
    return TURNOVER_DATA.get(bank_id, {}).get("years", {}).get(int(year))


def get_latest_turnover(bank_id: str, max_year: int = 2025) -> tuple[int | None, dict[str, Any] | None]:
    yrs_dict = TURNOVER_DATA.get(bank_id, {}).get("years", {})
    valid_yrs = [y for y in yrs_dict if y <= max_year and yrs_dict[y].get("rate") is not None]
    if not valid_yrs:
        return None, None
    latest_y = max(valid_yrs)
    return latest_y, yrs_dict[latest_y]


def export_turnover_data() -> Path:
    comp_data = REPO_ROOT / "comparison" / "data"
    comp_data.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []

    for b in VALID_BANKS:
        cfg = load_bank_config(b)
        meta = get_bank_turnover_meta(b)
        yrs_map = meta.get("years", {})
        b_payload = {
            "bank_id": b,
            "short_name": cfg.short_name,
            "basis": meta["basis"],
            "source": meta["source"],
            "years": {str(k): v for k, v in sorted(yrs_map.items())},
        }
        b_data = REPO_ROOT / "banks" / b / "data"
        b_data.mkdir(parents=True, exist_ok=True)
        (b_data / f"{b}_fluktuation.json").write_text(
            json.dumps(b_payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        for yr in sorted(yrs_map.keys()):
            entry = yrs_map[yr]
            rows.append({
                "bank_id": b,
                "short_name": cfg.short_name,
                "peer_group": cfg.peer_group,
                "year": yr,
                "turnover_rate_pct": entry.get("rate"),
                "turnover_net_pct": entry.get("net"),
                "turnover_gross_pct": entry.get("gross"),
                "basis": meta["basis"],
                "note": entry.get("note", ""),
                "source": meta["source"],
            })

    csv_path = comp_data / "xkb_personalfluktuation.csv"
    cols = [
        "bank_id",
        "short_name",
        "peer_group",
        "year",
        "turnover_rate_pct",
        "turnover_net_pct",
        "turnover_gross_pct",
        "basis",
        "note",
        "source",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"[OK] Personalfluktuation: {len(rows)} Jahreswerte über {len(TURNOVER_DATA)} berichtende Institute nach {csv_path} exportiert.")
    return csv_path


if __name__ == "__main__":
    export_turnover_data()
