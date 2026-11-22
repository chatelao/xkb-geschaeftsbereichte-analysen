# XKB Geschäftsberichte Analysen (19 Schweizer Banken)

> **Status:** Vollständig umgesetzt und verifiziert — **19 Schweizer Finanzinstitute** unter [`banks/`](./banks/) (**190 Einzelbank-Berichte & 247 Grafiken**, **7 Cross-Bank-Vergleichsberichte & 13 Benchmark-Grafiken**, **19 Vorsorgeeinrichtungen**, **260 harmonisierte Geschäftsjahre**).
> **Live-Portal:** [GitHub Pages](https://chatelao.github.io/xkb-geschaeftsbereichte-analysen/) · **Repository:** [`chatelao/xkb-geschaeftsbereichte-analysen`](https://github.com/chatelao/xkb-geschaeftsbereichte-analysen)

Strukturierte, vollständig reproduzierbare Längsschnitt-, Bilanz-, Risiko-, Effizienz-, Leadership-, IT-Strategie-, Fusionsbaum- (seit 1900) und Mitarbeiter-/Vorsorge-Analysen über eine gemeinsame, unit-getestete **«Hydrogen-First» Map-Validate-Reduce-Pipeline ([`shared/`](./shared/))**.

![Bilanzsumme und CAGR über 19 Schweizer Banken](./comparison/reports/charts/01_bilanzsumme_und_cagr_8_banken.png)

---

## Executive Scorecard 2025 (19 Institute)

### Kantonalbanken
| Institut | Peer Group | Bilanzsumme 2025 (Mio. CHF) | Reingewinn 2025 (Mio. CHF) | CIR % | ROE % | FTE 2025 | Berichte |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Zürcher Kantonalbank (ZKB)** | KB / D-SIB | 206'177,0 | 1'241,0 | 55,71 % | 7,89 % | 5'809 | [`banks/zkb/reports/`](./banks/zkb/reports/README.md) |
| **Luzerner Kantonalbank (LUKB)** | Kantonalbank | 62'249,1 | 295,5 | 47,23 % | 6,99 % | 1'206 | [`banks/lukb/reports/`](./banks/lukb/reports/README.md) |
| **BCV (Waadt)** | Kantonalbank | 61'620,0 | 430,0 | 48,66 % | 11,00 % | 2'083 | [`banks/bcv/reports/`](./banks/bcv/reports/README.md) |
| **St.Galler Kantonalbank (SGKB)** | Kantonalbank | 48'136,6 | 227,0 | 53,15 % | 7,28 % | 1'219 | [`banks/sgkb/reports/`](./banks/sgkb/reports/README.md) |
| **BEKB \| BCBE** | Kantonalbank | 42'977,0 | 175,4 | 51,26 % | 5,88 % | 1'058 | [`banks/bekb/reports/`](./banks/bekb/reports/README.md) |
| **Basellandschaftliche KB (BLKB)** | Kantonalbank | 37'614,0 | 154,0 | 53,21 % | 5,11 % | 926 | [`banks/blkb/reports/`](./banks/blkb/reports/README.md) |
| **BCGE (GEKB)** | Kantonalbank | 34'905,0 | 221,0 | 53,79 % | 8,84 % | 958 | [`banks/gekb/reports/`](./banks/gekb/reports/README.md) |
| **Walliser Kantonalbank (VSKB)** | Kantonalbank | 22'042,2 | 85,9 | 45,69 % | 5,07 % | 494 | [`banks/vskb/reports/`](./banks/vskb/reports/README.md) |

### Gross- & Privatbanken
| Institut | Peer Group | Bilanzsumme 2025 (Mio. CHF) | Reingewinn 2025 (Mio. CHF) | CIR % | ROE % | FTE 2025 | Berichte |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **UBS Group AG** | G-SIB (IFRS)* | 1'426'570,6 | 6'842,7 | 81,09 % | 8,60 % | 103'177 | [`banks/ubs/reports/`](./banks/ubs/reports/README.md) |
| **Pictet-Gruppe** | Privatbank | 42'928,1 | 667,2 | 71,99 % | 20,32 % | 5'507 | [`banks/pictet/reports/`](./banks/pictet/reports/README.md) |
| **Vontobel Holding AG** | Wealth & AM | 34'737,0 | 262,0 | 74,63 % | 10,57 % | 2'310 | [`banks/vontobel/reports/`](./banks/vontobel/reports/README.md) |

### Genossenschaften & Post
| Institut | Peer Group | Bilanzsumme 2025 (Mio. CHF) | Reingewinn 2025 (Mio. CHF) | CIR % | ROE % | FTE 2025 | Berichte |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Raiffeisen Gruppe** | Inland-D-SIB | 305'611,0 | 1'208,0 | 56,72 % | 5,08 % | 10'972 | [`banks/raiffeisen/reports/`](./banks/raiffeisen/reports/README.md) |
| **PostFinance AG** | Inland-D-SIB | 104'836,0 | 120,0 | 84,08 % | 1,82 % | 3'527 | [`banks/postfinance/reports/`](./banks/postfinance/reports/README.md) |
| **Migros Bank AG** | Retailbank | 62'327,6 | 276,2 | 54,22 % | 5,07 % | 1'749 | [`banks/migrosbank/reports/`](./banks/migrosbank/reports/README.md) |

### Regionalbanken & Verbund
| Institut | Peer Group | Bilanzsumme 2025 (Mio. CHF) | Reingewinn 2025 (Mio. CHF) | CIR % | ROE % | FTE 2025 | Berichte |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Valiant Holding AG** | Regionalbank | 37'874,1 | 154,7 | 54,84 % | 5,60 % | 1'052 | [`banks/valiant/reports/`](./banks/valiant/reports/README.md) |
| **Entris / RBA-Holding** | Verbund / B2B | 11'247,9 | 13,8 | 77,22 % | 4,66 % | 67 | [`banks/entris/reports/`](./banks/entris/reports/README.md) |
| **AEK BANK 1826** | Regionalbank | 5'744,1 | 10,3 | 37,34 % | 1,70 % | 166 | [`banks/aek/reports/`](./banks/aek/reports/README.md) |
| **Bank SLM AG** | Regionalbank | 1'913,9 | 3,5 | 45,72 % | 1,83 % | 66 | [`banks/slm/reports/`](./banks/slm/reports/README.md) |
| **Ersparniskasse Speicher (EKS)** | Regionalbank | 80,7 | 0,2 | 72,84 % | 2,11 % | 4 | [`banks/eks/reports/`](./banks/eks/reports/README.md) |

*\*UBS-Beträge via SNB-Referenzkursen deterministisch von USD in CHF umgerechnet.*

---

## Institutsübergreifende Auswertung (`comparison/`)

- **[01 · Grösse, Wachstum & Geschäftsmodell](./comparison/reports/01_groesse_wachstum_und_geschaeftsmodell.md)**
- **[02 · Profitabilität, Effizienz & Produktivität](./comparison/reports/02_profitabilitaet_effizienz_und_produktivitaet.md)**
- **[03 · Kapitalisierung, Regulierung & Staatsgarantie](./comparison/reports/03_kapitalisierung_regulierung_und_staatsgarantie.md)**
- **[04 · Ausschüttung, Eigentümer & reale Vergütung](./comparison/reports/04_ausschuettung_eigentuemer_und_verguetung_real.md)**
- **[05 · Zinswenden, Saisonalität & Resilienz](./comparison/reports/05_zinswenden_saisonalitaet_und_resilienz.md)**
- **[06 · Investoren-Branchenvergleich](./comparison/reports/06_investoren_branchenvergleich.md)**
- **[07 · Mitarbeiter- & Vorsorge-Branchenvergleich (inkl. Pensionskassen)](./comparison/reports/07_mitarbeiter_und_vorsorge_branchenvergleich.md)**

---

## Berichte pro Institut (`banks/<bank>/reports/`)
Jedes der 19 Institute verfügt über 10 standardisierte Berichte inklusive 13 hochauflösenden Grafiken:
1. **01 · Zinszyklen & Ertragsarchitektur**
2. **02 · Bilanzwachstum, Hypotheken & Refinanzierung**
3. **03 · Aufsichtsrechtliche Resilienz & Basel III**
4. **04 · Operative Effizienz & Transformation**
5. **05 · Eigentümer, Aktie / Dotationskapital & Wertschöpfung**
6. **06 · Unterjährige Dynamik (Semesterberichte)**
7. **07 · Strategische Epochen, Governance & reale Vergütung**
8. **08 · CEO & Chairman of the Board Achievement Report** *(inkl. historischer Führungs-Chronik)*
9. **09 · IT-Strategie, Kernbankensysteme & Digitalisierung**
10. **10 · Fusionsbaum & Institutsgeschichte seit 1900** *(Mermaid-Diagramm & Meilensteine)*

---

## Pläne & Dokumentation

- **[`PLAN.md`](./PLAN.md)** – Master-Umsetzungsplan (Phasen P0–P9)
- **[`VERBESSERUNGSPLAN.md`](./VERBESSERUNGSPLAN.md)** – Qualitäts-Audit, Vorsorge-Erhebung & Branchenvergleiche (Phasen V1–V5)
