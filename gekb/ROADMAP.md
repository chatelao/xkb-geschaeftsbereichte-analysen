# Roadmap: GEKB / BCGE Geschäftsberichte-Analyse

> **Bank:** Banque Cantonale de Genève (GEKB / BCGE)
> **Strategie-Dokument:** [`ANALYSE_STRATEGIE.md`](./ANALYSE_STRATEGIE.md)
> **Master-Plan:** [`../PLAN.md`](../PLAN.md)

---

## Status-Übersicht

| Phase | Beschreibung | Status | Details / Artefakte |
| :--- | :--- | :---: | :--- |
| **Phase 0a** | Analyse-Strategie & Plan | ✅ | [`ANALYSE_STRATEGIE.md`](./ANALYSE_STRATEGIE.md) |
| **Phase 0b** | PDF-Beschaffung (`pdf/`) | ✅ | **65 / 65 PDFs** in `gekb/pdf/` + [`pdf_manifest.json`](./pdf_manifest.json) |
| **Phase 0c** | PDF → Markdown (`.md/`) | ✅ | **65 / 65 Markdown-Dateien** in `gekb/.md/` (ohne Deko-PNGs) |
| **Phase 1** | `bank_config.yaml` & `overrides.json` | ⏳ | Offen für Gemini Hydrogen |
| **Phase 2** | Stufe 1 & 2 (Chunker & Extraktion) | ⏳ | `data/chunks/`, `data/extracted/` |
| **Phase 3** | Stufe 3 (Validierung, KPIs & BFS-Real) | ⏳ | `data/gekb_panel_*.csv`, `data/validation_report.md` |
| **Phase 4** | Stufe 4 (7 Berichte & 13 Charts) | ⏳ | `reports/01_*.md` .. `07_*.md`, `reports/charts/` |

---

## Beschaffte Primärquellen (`gekb/pdf/`)

- **Geschäftsberichte (`annual`, 2003–2025):** **23 Jahrgänge** lückenlos (`gekb-geschaeftsbericht-2003.pdf` bis `2025.pdf`, FR).
- **Semesterberichte (`semester`, H1 2008–H1 2026):** **18 Berichte** (`2008–2015`, `2017–2026`; Hinweis: H1 2016 fehlt im öffentlichen Archiv von `bcge.ch`).
- **Offenlegungsberichte / Pilier III (`offenlegung`, 2010–06-2026):** **24 Berichte** (Jahresendberichte `2010–2025` lückenlos + Halbjahresberichte `06-2019` bis `06-2026`).
- **Download-Skript:** [`download_reports.py`](./download_reports.py)

---

## Nächste Schritte für Gemini Hydrogen

1. `gekb/bank_config.yaml` und `gekb/overrides.json` gemäss [`PLAN.md`](../PLAN.md) Abschnitt 5.1 anlegen.
2. Chunker (`shared/chunker.py`) und Extraktor (`shared/extractor.py`) mit französischen Bilanz-/ER-Begriffen (`Total du bilan`, `Résultat net des opérations d'intérêts`, `Fonds propres de base CET1`, `Bénéfice net`) auf `gekb/.md/` ausführen.
3. Validierung, Panel-Generierung (`gekb_panel_2003_2026.csv`), 13 Grafiken und 7 Analyseberichte auf **Deutsch** erstellen.
