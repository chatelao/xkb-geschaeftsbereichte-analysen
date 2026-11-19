# Roadmap: ZKB Geschäftsberichte-Analyse

> **Bank:** Zürcher Kantonalbank (ZKB)
> **Strategie-Dokument:** [`ANALYSE_STRATEGIE.md`](./ANALYSE_STRATEGIE.md)
> **Master-Plan:** [`../PLAN.md`](../PLAN.md)

---

## Status-Übersicht

| Phase | Beschreibung | Status | Details / Artefakte |
| :--- | :--- | :---: | :--- |
| **Phase 0a** | Analyse-Strategie & Plan | ✅ | [`ANALYSE_STRATEGIE.md`](./ANALYSE_STRATEGIE.md) |
| **Phase 0b** | PDF-Beschaffung (`pdf/`) | ✅ | **74 / 74 PDFs** in `zkb/pdf/` + [`pdf_manifest.json`](./pdf_manifest.json) |
| **Phase 0c** | PDF → Markdown (`.md/`) | ✅ | **74 / 74 Markdown-Dateien** in `zkb/.md/` (ohne Deko-PNGs) |
| **Phase 1** | `bank_config.yaml` & `overrides.json` | ⏳ | Offen für Gemini Hydrogen |
| **Phase 2** | Stufe 1 & 2 (Chunker & Extraktion) | ⏳ | `data/chunks/`, `data/extracted/` |
| **Phase 3** | Stufe 3 (Validierung, KPIs & BFS-Real) | ⏳ | `data/zkb_panel_*.csv`, `data/validation_report.md` |
| **Phase 4** | Stufe 4 (7 Berichte & 13 Charts) | ⏳ | `reports/01_*.md` .. `07_*.md`, `reports/charts/` |

---

## Beschaffte Primärquellen (`zkb/pdf/`)

- **Geschäftsberichte (`annual`, 2014–2025):** **12 Jahrgänge** lückenlos (`2014–2025`) inkl. aller **4 Teilberichte 2025** (`finanzbericht`, `lagebericht`, `corporate-governance`, `verguetungsbericht`) = **16 PDFs**.
- **Semesterberichte (`semester`, H1 2013–H1 2026):** **14 Berichte** lückenlos (`2013–2026`, inkl. `2013–2014` via Wayback Machine).
- **Offenlegungsberichte (`offenlegung`, 03-2014–06-2026):** **44 Berichte** (Quartals- und Halbjahres-/Jahresoffenlegungen inkl. D-SIB-Kennzahlen, TLAC/Going-Concern und Basel III final ab 2025).
- **Download-Skript:** [`download_reports.py`](./download_reports.py)

---

## Nächste Schritte für Gemini Hydrogen

1. `zkb/bank_config.yaml` (`report_05_mode: cantonal_endowment`, `finma_category: 2`, `is_dsib: true`) und `zkb/overrides.json` anlegen.
2. Chunker & Extraktor auf `zkb/.md/` ausführen (inkl. D-SIB Going-Concern/Gone-Concern-Quoten und Dotationskapital-Ausschüttung an Kanton & Gemeinden).
3. Validierung, Panel-Generierung (`zkb_panel_2013_2026.csv`), 13 Grafiken und 7 Analyseberichte erstellen.
