# Roadmap: BCV Geschäftsberichte-Analyse

> **Bank:** Banque Cantonale Vaudoise (BCV)
> **Strategie-Dokument:** [`ANALYSE_STRATEGIE.md`](./ANALYSE_STRATEGIE.md)
> **Master-Plan:** [`../PLAN.md`](../PLAN.md)

---

## Status-Übersicht

| Phase | Beschreibung | Status | Details / Artefakte |
| :--- | :--- | :---: | :--- |
| **Phase 0a** | Analyse-Strategie & Plan | ✅ | [`ANALYSE_STRATEGIE.md`](./ANALYSE_STRATEGIE.md) |
| **Phase 0b** | PDF-Beschaffung (`pdf/`) | ✅ | **73 / 73 PDFs** in `bcv/pdf/` + [`pdf_manifest.json`](./pdf_manifest.json) |
| **Phase 0c** | PDF → Markdown (`.md/`) | ✅ | **73 / 73 Markdown-Dateien** in `bcv/.md/` (ohne Deko-PNGs) |
| **Phase 1** | `bank_config.yaml` & `overrides.json` | ⏳ | Offen für Gemini Hydrogen |
| **Phase 2** | Stufe 1 & 2 (Chunker & Extraktion) | ⏳ | `data/chunks/`, `data/extracted/` |
| **Phase 3** | Stufe 3 (Validierung, KPIs & BFS-Real) | ⏳ | `data/bcv_panel_*.csv`, `data/validation_report.md` |
| **Phase 4** | Stufe 4 (7 Berichte & 13 Charts) | ⏳ | `reports/01_*.md` .. `07_*.md`, `reports/charts/` |

---

## Beschaffte Primärquellen (`bcv/pdf/`)

- **Geschäftsberichte (`annual`, 2007–2025):** **19 Jahrgänge** lückenlos (`bcv-geschaeftsbericht-2007.pdf` bis `2025.pdf`, FR).
- **Semesterberichte (`semester`, H1 2008–H1 2026):** **19 Berichte** lückenlos (`2008–2026`, FR; H1 2021 inkl. Wayback-Fallback).
- **Offenlegungsberichte / Bâle III Pilier 3 (`offenlegung`, 06-2009–06-2026):** **35 Berichte** lückenlos halbjährlich (`06-2009` bis `06-2026`, inkl. Basel III final ab `06-2025`).
- **Download-Skript:** [`download_reports.py`](./download_reports.py)

---

## Nächste Schritte für Gemini Hydrogen

1. `bcv/bank_config.yaml` (`share_split: {date: "2020-05-28", factor: 10}`, `irb_approach: "F-IRB"`, `state_guarantee: false`) und `bcv/overrides.json` anlegen.
2. Chunker & Extraktor auf `bcv/.md/` ausführen (FR-Finanzterminologie, 1:10-Aktiensplit-Bereinigung für Kurse/Dividenden vor Mai 2020).
3. Validierung, Panel-Generierung (`bcv_panel_2007_2026.csv`), 13 Grafiken und 7 Analyseberichte auf **Deutsch** erstellen.
