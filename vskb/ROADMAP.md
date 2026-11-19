# Roadmap: VSKB / WKB Geschäftsberichte-Analyse

> **Bank:** Walliser Kantonalbank (VSKB / WKB / BCVs)
> **Strategie-Dokument:** [`ANALYSE_STRATEGIE.md`](./ANALYSE_STRATEGIE.md)
> **Master-Plan:** [`../PLAN.md`](../PLAN.md)

---

## Status-Übersicht

| Phase | Beschreibung | Status | Details / Artefakte |
| :--- | :--- | :---: | :--- |
| **Phase 0a** | Analyse-Strategie & Plan | ✅ | [`ANALYSE_STRATEGIE.md`](./ANALYSE_STRATEGIE.md) |
| **Phase 0b** | PDF-Beschaffung (`pdf/`) | ✅ | **40 / 40 PDFs** in `vskb/pdf/` + [`pdf_manifest.json`](./pdf_manifest.json) |
| **Phase 0c** | PDF → Markdown (`.md/`) | ✅ | **40 / 40 Markdown-Dateien** in `vskb/.md/` (ohne Deko-PNGs) |
| **Phase 1** | `bank_config.yaml` & `overrides.json` | ⏳ | Offen für Gemini Hydrogen |
| **Phase 2** | Stufe 1 & 2 (Chunker & Extraktion) | ⏳ | `data/chunks/`, `data/extracted/` |
| **Phase 3** | Stufe 3 (Validierung, KPIs & BFS-Real) | ⏳ | `data/vskb_panel_*.csv`, `data/validation_report.md` |
| **Phase 4** | Stufe 4 (7 Berichte & 13 Charts) | ⏳ | `reports/01_*.md` .. `07_*.md`, `reports/charts/` |

---

## Beschaffte Primärquellen (`vskb/pdf/`)

- **Geschäftsberichte (`annual`, 2007, 2009–2010, 2014–2025):** **15 Jahrgänge** (`vskb-geschaeftsbericht-{2007,2009,2010,2014..2025}.pdf`, DE). Hinweis: Jahrgänge 2003–2006, 2008 und 2011–2013 sind im öffentlichen `bcvs.ch`-Archiv nicht mehr verlinkt (Vorjahreswerte in 2014/2010/2009 decken 2006, 2008 und 2013 mit ab).
- **Semesterberichte (`semester`, H1 2015–H1 2026):** **12 Berichte** lückenlos (`vskb-semesterbericht-2015.pdf` bis `2026.pdf`, DE).
- **Offenlegungsberichte (`offenlegung`, 06-2020–06-2026):** **13 Berichte** lückenlos (`06-2020` bis `06-2026`, halbjährlich).
- **Download-Skript:** [`download_reports.py`](./download_reports.py)

---

## Nächste Schritte für Gemini Hydrogen

1. `vskb/bank_config.yaml` (`scope: standalone`, `cantonal_ownership_pct: 70.0`) und `vskb/overrides.json` gemäss [`PLAN.md`](../PLAN.md) anlegen.
2. Chunker & Extraktor auf `vskb/.md/` ausführen; dabei Einzelabschluss-Besonderheiten (Reserven für allgemeine Bankrisiken, Voll-Staatsgarantie) berücksichtigen.
3. Validierung, Panel-Generierung (`vskb_panel_2007_2026.csv`), 13 Grafiken und 7 Analyseberichte auf **Deutsch** erstellen.
