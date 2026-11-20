# Daten- und Analysestrategie: UBS Group AG (2014–2026)

> **Zielsetzung:** Strukturierte Extraktion, Normalisierung und mehrjährige Längsschnittanalyse über alle Geschäfts-, Halbjahres- (Q2) und Pillar-3-Berichte der **UBS Group AG** – umgesetzt über die gemeinsame `shared/`-Pipeline und optimiert für **Gemini Hydrogen**.
> **Master-Plan:** Siehe [`../PLAN.md`](../PLAN.md).

---

## 1. Bankprofil & Domänen-Kontext

| Merkmal | Ausprägung UBS |
| :--- | :--- |
| **Offizieller Name** | UBS Group AG (Konzernmuttergesellschaft; bis 2014 UBS AG) |
| **Rechtsform & Eigentümer** | Publikums-Aktiengesellschaft (SIX: `UBSG`, NYSE: `UBS`; Streubesitz) |
| **Staatsgarantie** | **Keine** |
| **FINMA-Aufsichtskategorie** | **Kategorie 1 – Global systemrelevante Bank (G-SIB / TBTF)** |
| **Abschluss-Scope** | **Konzernrechnung UBS Group AG (consolidated, IFRS)** |
| **Berichtswährung** | **USD (Mio. USD)** *(Umstellung von CHF auf USD per Q4 2018!)* |
| **Primärsprache** | Englisch (`EN`, Teile der Geschäftsberichte auch auf Deutsch verfügbar) |
| **Berichtstypen** | Annual Report (`YYYY`), Second Quarter / Interim Report (`2QYYYY`), Pillar 3 Report (`2Q` & `4Q` / `FY`) |

### Offizielle Quellen für `ubs/download_reports.py`
1. **Primär- & Wayback-Archiv:** `https://www.ubs.com/global/en/investor-relations/financial-information/` (`annual-reporting.html`, `quarterly-reporting.html`, `pillar-3-disclosures.html`) sowie Wayback Machine (`web.archive.org`) für automatisierte Downloads ohne WAF-Blockade.

---

## 2. Kritische Datenbrüche & Fallstricke (UBS-spezifisch)

1. **Berichtswährung USD (und Währungswechsel CHF → USD per Q4 `2018`):**
   - Bis inkl. **2017** berichtete UBS in **CHF**; per **Q4 2018** stellte UBS Group AG auf **USD** als funktionale und Berichtswährung um (inkl. retrospektiver USD-Restatements ab 2016/2017).
   - Im Vergleichsmodul (`comparison/`) muss UBS über historische Jahresschluss-/Durchschnittskurse **USD/CHF** in Mio. CHF umgerechnet werden, während im `ubs/`-Panel die Originalwährung **USD** (mit CHF-Umrechnungsspalte) geführt wird!
2. **Credit-Suisse-Übernahme (`2023–2026`):**
   - Am **12. Juni 2023** erfolgte der rechtliche Abschluss der Übernahme der **Credit Suisse Group AG**:
     - Bilanzsprung auf > **1,5–1,7 Billionen USD** (`total_assets`)
     - Einmaliger **Negative-Goodwill-Ertrag (~27–29 Mrd. USD)** im GJ 2023!
     - Bereinigte vs. ausgewiesene Profitabilität (*Reported* vs. *Underlying PBT*) sowie Integrationskosten und *Non-core and Legacy (NCL)* müssen in Berichten 01, 02, 04 und 07 zwingend getrennt werden.
3. **G-SIB / TBTF-Kapitalregime (Kategorie 1):**
   - UBS unterliegt den höchsten Schweizer TBTF-Anforderungen (Going-Concern + Gone-Concern / TLAC + G-SIB-Zuschlag) sowie ab `01.01.2025` **Basel III final**.
4. **Aktienrückkäufe + Dividende in USD:**
   - Gesamtausschüttung an Aktionäre besteht aus ordentlicher **Dividende (USD/Aktie)** **plus** milliardenschweren **Aktienrückkäufen (Share Buybacks)**.

---

## 3. UBS-spezifische Ankerbegriffe & `bank_config.yaml`-Eckwerte

- **Bilanz (IFRS, in Mio. USD):** `Total assets`, `Loans and advances to customers`, `Customer deposits`, `Equity attributable to shareholders`
- **Erfolgsrechnung (IFRS, in Mio. USD):** `Total operating income`, `Net interest income`, `Net fee and commission income`, `Operating expenses`, `Operating profit / (loss) before tax`, `Net profit / (loss) attributable to shareholders`
- **Offenlegung (G-SIB Pillar 3):** `CET1 capital ratio`, `Going concern capital ratio`, `Total loss-absorbing capacity (TLAC)`, `Tier 1 leverage ratio`, `Liquidity coverage ratio (LCR)`, `Net stable funding ratio (NSFR)`, `Risk-weighted assets (RWA)`
- **Vorgabe für `ubs/bank_config.yaml`:**
  - `bank_id: "ubs"`, `reporting_scope: "consolidated"`, `reporting_currency: "USD"`, `listed: true`, `ticker: "UBSG"`, `finma_category: 1`, `state_guarantee: false`, `report_05_mode: "listed_share"`
  - **Palette:** Primary `#E60000` (UBS-Rot), Secondary `#111111`, Accent `#666666`, Muted `#94A3B8`
  - **Epochen (Bericht 07):**
    1. `2014–2018`: *Holding-Gründung (UBS Group AG), Kapitalaufbau & Wechsel zu USD*
    2. `2019–2022`: *Global Wealth Management-Skalierung, Digitalisierung & Aktienrückkäufe*
    3. `2023–2026`: *Übernahme & Integration der Credit Suisse, G-SIB-TBTF & Basel III final*
