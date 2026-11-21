# Roadmap: Raiffeisen Gruppe Geschäftsberichte-Analyse

> **Bank:** Raiffeisen Gruppe Schweiz
> **Strategie-Dokument:** [`ANALYSE_STRATEGIE.md`](./ANALYSE_STRATEGIE.md)
> **Master-Plan:** [`../PLAN.md`](../PLAN.md)

---

## Status-Übersicht

| Phase | Beschreibung | Status | Details / Artefakte |
| :--- | :--- | :---: | :--- |
| **Phase 0a** | Analyse-Strategie & Plan | ✅ | [`ANALYSE_STRATEGIE.md`](./ANALYSE_STRATEGIE.md) |
| **Phase 0b** | PDF-Beschaffung (`pdf/`) | ✅ | **75 / 75 PDFs** in `raiffeisen/pdf/` + [`pdf_manifest.json`](./pdf_manifest.json) |
| **Phase 0c** | PDF → Markdown (`.md/`) | ✅ | **75 / 75 Markdown-Dateien** in `raiffeisen/.md/` (ohne Deko-PNGs) |
| **Phase 1** | `bank_config.yaml` & `overrides.json` | ⏳ | Offen für Gemini Hydrogen |
| **Phase 2** | Stufe 1 & 2 (Chunker & Extraktion) | ⏳ | `data/chunks/`, `data/extracted/` |
| **Phase 3** | Stufe 3 (Validierung, KPIs & BFS-Real) | ⏳ | `data/raiffeisen_panel_*.csv`, `data/validation_report.md` |
| **Phase 4** | Stufe 4 (7 Berichte & 13 Charts) | ⏳ | `reports/01_*.md` .. `07_*.md`, `reports/charts/` |

---

## Beschaffte Primärquellen (`raiffeisen/pdf/`)

- **Geschäftsberichte (`annual`, 2011–2025):** **15 Jahrgänge** lückenlos (`raiffeisen-geschaeftsbericht-2011.pdf` bis `2025.pdf`, Konzernrechnung Raiffeisen Gruppe, DE).
- **Semesterberichte / Zwischenabschlüsse (`semester`, H1 2012–H1 2026):** **15 Berichte** lückenlos (`2012–2026`, DE).
- **Offenlegungsberichte (`offenlegung`, 06-2015–06-2026):** **45 Berichte** lückenlos (Quartals-, Halbjahres- und Jahresberichte inkl. D-SIB-TBTF & Basel III final ab `2025`).
- **Download-Skript:** [`download_reports.py`](./download_reports.py)

---

## Nächste Schritte für Gemini Hydrogen

1. `raiffeisen/bank_config.yaml` (`reporting_scope: consolidated`, `finma_category: 2`, `report_05_mode: cooperative`) und `raiffeisen/overrides.json` anlegen.
2. Chunker & Extraktor auf `raiffeisen/.md/` ausführen (Genossenschaftskapital, Thesaurierungsquote, D-SIB Going-/Gone-Concern).
3. Validierung, Panel-Generierung (`raiffeisen_panel_2011_2026.csv`), 13 Grafiken und 7 Analyseberichte erstellen.
