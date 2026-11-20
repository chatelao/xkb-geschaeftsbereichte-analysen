# XKB Geschäftsberichte Analysen (ZKB, GEKB, VSKB, BCV, Raiffeisen, PostFinance, UBS)

> **Status:** Architektur & Umsetzungsplan vollständig definiert; Phase 0 (PDF-Download & Markdown-Konvertierung) umgesetzt – bereit zur Implementierung von Phase 1–6 durch **Gemini Hydrogen**.
> **Referenz-Architektur:** Analog [`chatelao/bekb-geschaeftsbereichte-analysen`](https://github.com/chatelao/bekb-geschaeftsbereichte-analysen)

Strukturierte, vollständig reproduzierbare Längsschnitt-, Bilanz-, Risiko-, Effizienz- und Governance-Analysen für **sieben Schweizer Banken** (vier Kantonalbanken + Raiffeisen, PostFinance und UBS) über eine gemeinsame, unit-getestete **«Hydrogen-First» Map-Validate-Reduce-Pipeline (`shared/`)** sowie ein bankübergreifendes **Cross-Bank-Benchmarking (`comparison/`)** und ein gemeinsames **MkDocs-/Read-the-Docs- & GitHub-Pages-Portal**.

---

## Master-Plan & Bank-Strategien

- **[`PLAN.md`](./PLAN.md)** – Verbindliches Schritt-für-Schritt-Runbook für Gemini Hydrogen (Phasen `P0` bis `P5`, Ziel-Ordnerstruktur, `bank_config.yaml`-Schema, kanonisches Datenmodell, Verifikations-Gates & Fallstrick-Matrix).

| Unterverzeichnis | Bank | Kanton / Sitz | Rechtsform / Ticker | Staatsgarantie | FINMA-Kat. | Abschluss-Scope | Detail-Strategie | Phase |
| :--- | :--- | :---: | :--- | :---: | :---: | :---: | :--- | :---: |
| [`vskb/`](./vskb/ANALYSE_STRATEGIE.md) | **Walliser Kantonalbank (WKB / BCVs)** | VS | AG (SIX: `WKB`, 70 % Kt.) | Voll | Kat. 3 | Einzelabschluss | [`vskb/ANALYSE_STRATEGIE.md`](./vskb/ANALYSE_STRATEGIE.md) | **P1 (Pilot)** |
| [`zkb/`](./zkb/ANALYSE_STRATEGIE.md) | **Zürcher Kantonalbank (ZKB)** | ZH | Anstalt (100 % Kt., nicht kotiert) | Voll | **Kat. 2 (D-SIB)** | Konzern | [`zkb/ANALYSE_STRATEGIE.md`](./zkb/ANALYSE_STRATEGIE.md) | **P2** |
| [`bcv/`](./bcv/ANALYSE_STRATEGIE.md) | **Banque Cantonale Vaudoise (BCV)** | VD | AG (SIX: `BCVN`, ~67 % Kt.) | Keine | Kat. 3 | Konzern | [`bcv/ANALYSE_STRATEGIE.md`](./bcv/ANALYSE_STRATEGIE.md) | **P3** |
| [`gekb/`](./gekb/ANALYSE_STRATEGIE.md) | **Banque Cantonale de Genève (BCGE)** | GE | AG (SIX: `BCGE`, ~73 % öff.) | Keine | Kat. 3 | Konzern | [`gekb/ANALYSE_STRATEGIE.md`](./gekb/ANALYSE_STRATEGIE.md) | **P4** |
| [`raiffeisen/`](./raiffeisen/ANALYSE_STRATEGIE.md) | **Raiffeisen Gruppe Schweiz** | SG | Genossenschaftsverbund (nicht kotiert) | Keine | **Kat. 2 (D-SIB)** | Konzern | [`raiffeisen/ANALYSE_STRATEGIE.md`](./raiffeisen/ANALYSE_STRATEGIE.md) | **P5** |
| [`postfinance/`](./postfinance/ANALYSE_STRATEGIE.md) | **PostFinance AG** | BE | AG (100 % Schweizerische Post) | Keine | **Kat. 2 (D-SIB)** | Einzelabschluss | [`postfinance/ANALYSE_STRATEGIE.md`](./postfinance/ANALYSE_STRATEGIE.md) | **P6** |
| [`ubs/`](./ubs/ANALYSE_STRATEGIE.md) | **UBS Group AG** | ZH | AG (SIX: `UBSG`, NYSE: `UBS`) | Keine | **Kat. 1 (G-SIB)** | Konzern (USD) | [`ubs/ANALYSE_STRATEGIE.md`](./ubs/ANALYSE_STRATEGIE.md) | **P7** |

---

## Geplanter Gesamtumfang (nach Abschluss aller Phasen)

- **Gemeinsame Kernbibliothek (`shared/` + `tests/`):** Konfigurierbarer DE/FR/EN-Chunker, Hydrogen-Map/Reduce-Extractor (`--backend local|gemini`), `t+1`-Selbstheilung, Aktiensplit- & Währungsbereinigung (USD→CHF für UBS), BFS-LIK-Inflationsbereinigung (`real 2025 CHF`) und 300-DPI-Chart-Engine.
- **Pro Bank (7×):** 7 Mehrjahresberichte + 13 hochauflösende Grafiken + validierte CSV/JSON-Panels + `validation_report.md` (= **49 Bankberichte & 91 Bankgrafiken**).
- **Cross-Bank-Benchmarking (`comparison/`):** 4 bankübergreifende Vergleichsberichte + 6–8 Vergleichsgrafiken über alle 7 Schweizer Banken.
- **Publikation:** Automatisiertes CI/CD-Portal auf **GitHub Pages** und **Read the Docs** (`mkdocs build --strict`).
