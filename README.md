# XKB Geschäftsberichte Analysen (BEKB, ZKB, GEKB, VSKB, BCV, Raiffeisen, PostFinance, UBS)

> **Status:** Rohdaten aller **8 Schweizer Banken** (**458 PDFs** & **458 Markdown-Dateien**) vollständig im Repository vorhanden; Master-Umsetzungsplan ([`PLAN.md`](./PLAN.md)) für **Gemini Hydrogen** (Schritt 1: Einzelbank-Ausweitung P0–P7; Schritt 2: Institutsübergreifende Auswertung & Portal P8–P9) bereit zur Umsetzung.
> **Referenz-Architektur:** Analog [`chatelao/bekb-geschaeftsbereichte-analysen`](https://github.com/chatelao/bekb-geschaeftsbereichte-analysen)

Strukturierte, vollständig reproduzierbare Längsschnitt-, Bilanz-, Risiko-, Effizienz- und Governance-Analysen für **acht Schweizer Banken** (5 Kantonalbanken + Raiffeisen, PostFinance und UBS) über eine gemeinsame, unit-getestete **«Hydrogen-First» Map-Validate-Reduce-Pipeline (`shared/`)** sowie ein institutsübergreifendes **Cross-Bank-Benchmarking (`comparison/`)** und ein gemeinsames **MkDocs-/Read-the-Docs- & GitHub-Pages-Portal**.

---

## Master-Plan & Bank-Übersicht

- **[`PLAN.md`](./PLAN.md)** – Verbindliches 2-stufiges Schritt-für-Schritt-Runbook für **Gemini Hydrogen** (Schritt 1: `P0–P7` Einzelbank-Ausweitung mit BEKB-Regressionstest; Schritt 2: `P8–P9` Cross-Bank-Harmonisierung, Vergleichsberichte & Portal).

| Unterverzeichnis | Bank | Sitz | Rechtsform / Ticker | Staatsgarantie | FINMA-Kat. | Scope / Standard | Rohdaten (PDF / MD) | Phase |
| :--- | :--- | :---: | :--- | :---: | :---: | :--- | :---: | :---: |
| [`bekb/`](./bekb/) | **Berner Kantonalbank (BEKB)** | BE | AG (SIX: `BEKN`) | Keine | Kat. 3 | Einzelabschluss / ARB | 57 / 57 | **P0 (Baseline)** |
| [`vskb/`](./vskb/ANALYSE_STRATEGIE.md) | **Walliser Kantonalbank (WKB / BCVs)** | VS | AG (SIX: `WKB`) | Voll | Kat. 3 | Einzelabschluss / ARB | 40 / 40 | **P1 (Pilot)** |
| [`zkb/`](./zkb/ANALYSE_STRATEGIE.md) | **Zürcher Kantonalbank (ZKB)** | ZH | Anstalt (100 % Kt., nicht kotiert) | Voll | **Kat. 2 (D-SIB)** | Konzern / ARB | 74 / 74 | **P2** |
| [`bcv/`](./bcv/ANALYSE_STRATEGIE.md) | **Banque Cantonale Vaudoise (BCV)** | VD | AG (SIX: `BCVN`) | Keine | Kat. 3 | Konzern / ARB | 73 / 73 | **P3** |
| [`gekb/`](./gekb/ANALYSE_STRATEGIE.md) | **Banque Cantonale de Genève (BCGE)** | GE | AG (SIX: `BCGE`) | Keine | Kat. 3 | Konzern / ARB | 65 / 65 | **P4** |
| [`raiffeisen/`](./raiffeisen/ANALYSE_STRATEGIE.md) | **Raiffeisen Gruppe Schweiz** | SG | Genossenschaftsverbund | Keine | **Kat. 2 (D-SIB)** | Konzern / ARB | 75 / 75 | **P5** |
| [`postfinance/`](./postfinance/ANALYSE_STRATEGIE.md) | **PostFinance AG** | BE | AG (100 % Post) | Keine | **Kat. 2 (D-SIB)** | Einzelabschluss / ARB | 60 / 60 | **P6** |
| [`ubs/`](./ubs/ANALYSE_STRATEGIE.md) | **UBS Group AG** | ZH | AG (SIX: `UBSG`, NYSE: `UBS`) | Keine | **Kat. 1 (G-SIB)** | Konzern / IFRS (USD) | 14 / 14 | **P7** |

---

## Geplanter Gesamtumfang (nach Abschluss von Schritt 1 & Schritt 2)

- **Gemeinsame Kernbibliothek (`shared/` + `tests/`):** Konfigurierbarer DE/FR/EN-Chunker, Hydrogen-Map/Reduce-Extractor (`--backend local|gemini`), `t+1`-Selbstheilung, Aktiensplit- & FX-Umrechnung (`USD → CHF` für UBS via `shared/fx_rates.py`), BFS-LIK-Inflationsbereinigung (`real 2025 CHF`), BEKB-Regressionstest und 300-DPI-Chart-Engine.
- **Schritt 1 — Pro Institut (8×):** 7 Mehrjahresberichte + 13 hochauflösende Grafiken + validierte CSV/JSON-Panels + `validation_report.md` (= **56 Bankberichte & 104 Bankgrafiken**).
- **Schritt 2 — Institutsübergreifend (`comparison/`):** Harmonisiertes 8-Banken-Panel (inkl. Peer-Gruppen & Vergleichbarkeits-Flags) + **5 Vergleichsberichte** + **9 Vergleichsgrafiken**.
- **Publikation:** Automatisiertes CI/CD-Portal auf **GitHub Pages** und **Read the Docs** (`mkdocs build --strict`).
