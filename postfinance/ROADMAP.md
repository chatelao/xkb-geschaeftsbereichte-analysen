# Roadmap: PostFinance AG Geschäftsberichte-Analyse

> **Bank:** PostFinance AG
> **Strategie-Dokument:** [`ANALYSE_STRATEGIE.md`](./ANALYSE_STRATEGIE.md)
> **Master-Plan:** [`../PLAN.md`](../PLAN.md)

---

## Status-Übersicht

| Phase | Beschreibung | Status | Details / Artefakte |
| :--- | :--- | :---: | :--- |
| **Phase 0a** | Analyse-Strategie & Plan | ✅ | [`ANALYSE_STRATEGIE.md`](./ANALYSE_STRATEGIE.md) |
| **Phase 0b** | PDF-Beschaffung (`pdf/`) | ✅ | **60 / 60 PDFs** in `postfinance/pdf/` + [`pdf_manifest.json`](./pdf_manifest.json) |
| **Phase 0c** | PDF → Markdown (`.md/`) | ✅ | **60 / 60 Markdown-Dateien** in `postfinance/.md/` (ohne Deko-PNGs) |
| **Phase 1** | `bank_config.yaml` & `overrides.json` | ⏳ | Offen für Gemini Hydrogen |
| **Phase 2** | Stufe 1 & 2 (Chunker & Extraktion) | ⏳ | `data/chunks/`, `data/extracted/` |
| **Phase 3** | Stufe 3 (Validierung, KPIs & BFS-Real) | ⏳ | `data/postfinance_panel_*.csv`, `data/validation_report.md` |
| **Phase 4** | Stufe 4 (7 Berichte & 13 Charts) | ⏳ | `reports/01_*.md` .. `07_*.md`, `reports/charts/` |

---

## Beschaffte Primärquellen (`postfinance/pdf/`)

- **Geschäftsberichte (`annual`, 2013–2025):** **13 Jahrgänge** lückenlos seit Gründung der PostFinance AG 2013 (`postfinance-geschaeftsbericht-2013.pdf` bis `2025.pdf`, DE).
- **Halbjahresberichte (`semester`):** **2 Einzelberichte** (`2022`, `2026`; ergänzend Halbjahres-Eigenmitteloffenlegung `06-2014–06-2026`).
- **Offenlegungsberichte (`offenlegung`, 2013–06-2026):** **45 Berichte** lückenlos (Quartals-, Halbjahres- und Jahresoffenlegungen inkl. D-SIB-TBTF & Basel III final ab `2025`).
- **Download-Skript:** [`download_reports.py`](./download_reports.py)

---

## Nächste Schritte für Gemini Hydrogen

1. `postfinance/bank_config.yaml` (`reporting_scope: standalone`, `finma_category: 2`, `report_05_mode: parent_company`) und `postfinance/overrides.json` anlegen.
2. Chunker & Extraktor auf `postfinance/.md/` ausführen (Finanzanlagen-Fokus statt Hypothekenbuch, Negativzins- vs. Zinswende-Effekt, D-SIB-Kapitalisierung).
3. Validierung, Panel-Generierung (`postfinance_panel_2013_2026.csv`), 13 Grafiken und 7 Analyseberichte erstellen.
