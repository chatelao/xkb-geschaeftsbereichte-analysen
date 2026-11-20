# Roadmap: UBS Group AG Geschäftsberichte-Analyse

> **Bank:** UBS Group AG
> **Strategie-Dokument:** [`ANALYSE_STRATEGIE.md`](./ANALYSE_STRATEGIE.md)
> **Master-Plan:** [`../PLAN.md`](../PLAN.md)

---

## Status-Übersicht

| Phase | Beschreibung | Status | Details / Artefakte |
| :--- | :--- | :---: | :--- |
| **Phase 0a** | Analyse-Strategie & Plan | ✅ | [`ANALYSE_STRATEGIE.md`](./ANALYSE_STRATEGIE.md) |
| **Phase 0b** | PDF-Beschaffung (`pdf/`) | ✅ | **14 / 14 PDFs** in `ubs/pdf/` + [`pdf_manifest.json`](./pdf_manifest.json) |
| **Phase 0c** | PDF → Markdown (`.md/`) | ✅ | **14 / 14 Markdown-Dateien** in `ubs/.md/` (ohne Deko-PNGs) |
| **Phase 1** | `bank_config.yaml` & `overrides.json` | ⏳ | Offen für Gemini Hydrogen |
| **Phase 2** | Stufe 1 & 2 (Chunker & Extraktion) | ⏳ | `data/chunks/`, `data/extracted/` |
| **Phase 3** | Stufe 3 (Validierung, KPIs & BFS-Real) | ⏳ | `data/ubs_panel_*.csv`, `data/validation_report.md` |
| **Phase 4** | Stufe 4 (7 Berichte & 13 Charts) | ⏳ | `reports/01_*.md` .. `07_*.md`, `reports/charts/` |

---

## Beschaffte Primärquellen (`ubs/pdf/`)

- **Annual Reports (`annual`, 2020–2025):** **6 Jahrgänge** lückenlos (`ubs-geschaeftsbericht-2020.pdf` bis `2025.pdf`, EN, inkl. Vorjahresreihen 2018–2019 in 2020, Credit-Suisse-Übernahme 2023 & Integration 2024–2025).
- **Interim / Second Quarter Reports (`semester`, 2Q 2022–2025):** **4 Berichte** (`2022–2025`, EN).
- **Pillar 3 Disclosures (`offenlegung`):** **4 Berichte** (`06-2023`, `2023`, `2024`, `06-2025`; weitere G-SIB-Kapitalkennzahlen sind direkt in den Annual & 2Q Reports enthalten).
- **Download-Skript:** [`download_reports.py`](./download_reports.py) (Wayback- & Mirror-basiert wegen Akamai-WAF auf `ubs.com`; ältere JCR-Captures 2014–2019 sind in Wayback bei 5 MB gekappt und können bei Bedarf manuell aus dem Browser ergänzt werden).

---

## Nächste Schritte für Gemini Hydrogen

1. `ubs/bank_config.yaml` (`reporting_scope: consolidated`, `reporting_currency: USD`, `finma_category: 1`, `listed: true`, `ticker: UBSG`) und `ubs/overrides.json` anlegen.
2. Chunker & Extraktor auf `ubs/.md/` ausführen (IFRS-Englisch, USD-Mio., Reported vs. Underlying PBT, G-SIB Going-/Gone-Concern & TLAC).
3. Validierung, Panel-Generierung (`ubs_panel_2018_2025.csv`), USD→CHF-Umrechnung für `comparison/`, 13 Grafiken und 7 Analyseberichte auf **Deutsch** erstellen.
