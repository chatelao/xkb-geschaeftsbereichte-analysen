# Daten- und Analysestrategie: Zürcher Kantonalbank (ZKB, 2003–2026)

> **Zielsetzung:** Strukturierte Extraktion, Normalisierung und mehrjährige Längsschnittanalyse über alle Geschäfts-, Halbjahres- und Offenlegungsberichte der **Zürcher Kantonalbank (ZKB)** – umgesetzt über die gemeinsame `shared/`-Pipeline und optimiert für **Gemini Hydrogen**.
> **Master-Plan:** Siehe [`../PLAN.md`](../PLAN.md) (Phase 2).

---

## 1. Bankprofil & Domänen-Kontext

| Merkmal | Ausprägung ZKB |
| :--- | :--- |
| **Offizieller Name** | Zürcher Kantonalbank (ZKB) |
| **Rechtsform & Eigentümer** | Öffentlich-rechtliche Anstalt des Kantons Zürich (**100 % Kanton Zürich**, Dotationskapital, **nicht börsenkotiert**) |
| **Staatsgarantie** | **Voll** (unbeschränkt für nicht nachrangige Verbindlichkeiten, gegen jährliche Abgeltung an den Kanton) |
| **FINMA-Aufsichtskategorie** | **Kategorie 2 – Inländisch systemrelevante Bank (D-SIB / TBTF)** |
| **Abschluss-Scope** | **Konzernrechnung (Group)** – verbindlich für alle Zeitreihen (inkl. Swisscanto ab 2015, ZKB Österreich AG) |
| **Primärsprache** | Deutsch (Parallel-Ausgaben auf Englisch) |
| **Berichtstypen** | Geschäftsbericht (`YYYY`), Halbjahresbericht (`H1-YYYY`), Offenlegungsbericht (`YYYY` & `06-YYYY`, zusätzl. Q1/Q3 verfügbar) |

### Offizielle Quellen für `zkb/download_reports.py`
1. **Primärarchiv ZKB:** `https://www.zkb.ch/de/lps/corporate/berichterstattung/downloads.html` und `https://www.zkb.ch/de/lps/corporate/berichterstattung/offenlegung.html`
2. **VSKB-Archiv:** `https://vskb.ch/publikationen/jahresberichte` (z. B. `ZKB_2024.pdf`, `ZKB_2025.pdf`)
3. **Kantonsrat Zürich (Geschäftsdatenbank):** `https://www.kantonsrat.zh.ch` (jährliche Vorlage *Rechnung, Geschäftsbericht und Nachhaltigkeitsbericht der ZKB*)
4. **Historisches Archiv (2003–2016):** Wayback Machine CDX API (`web.archive.org/cdx/search/cdx?url=zkb.ch/*&filter=mimetype:application/pdf`)

> **Wichtiger Sourcing-Hinweis für Gemini Hydrogen:** Die ZKB splittet neuere Jahrgänge teilweise in *Geschäftsbericht (Gesamt)*, *Finanzbericht*, *Lagebericht* und *Corporate Governance*. Vorrangig das **Gesamtdokument (Geschäftsbericht)** herunterladen; falls getrennt, Finanzbericht + Corporate Governance / Vergütungsbericht zusammenführen oder klar referenzieren.

---

## 2. Kritische Datenbrüche & Fallstricke (ZKB-spezifisch)

1. **Konzern vs. Stammhaus:** Der ZKB-Geschäftsbericht enthält sowohl die **Konzernrechnung** (vorne) als auch die **Jahresrechnung Stammhaus** (hinten). Der Chunker muss zwingend nur **Konzernbilanz / Konzernerfolgsrechnung** selektieren (`reporting_scope: "consolidated"`).
2. **FINMA-RVB / ARB Umstellung (`2015`) & Swisscanto-Übernahme (`2015`):**
   - Gleichzeitige Einführung der neuen Bankenrechnungslegung (*Geschäftserfolg* ab 2015) **und** Vollkonsolidierung der **Swisscanto-Gruppe** (massiver Sprung bei Kommissions-/Dienstleistungserfolg, verwalteten Vermögen AuM und FTE!). Beide Effekte müssen in Berichten 01, 04 und 07 explizit getrennt erläutert werden.
3. **Systemrelevanz / TBTF-Regime (seit `2013`, schrittweise verschärft bis `2026`):**
   - Im Gegensatz zu Kat.-3-Banken (BEKB, BCV, GEKB, VSKB) unterliegt die ZKB den **Going-Concern-** und **Gone-Concern- (TLAC / Bail-in-Bonds)**-Anforderungen gemäss ERV für systemrelevante Banken.
   - `capital_targets_pct` und Chart 03 müssen TBTF-Zielgrössen (Going-Concern-Quote, TLAC-Quote, TBTF-Leverage-Ratio) statt Standard-Kat.-3-ERV-Werten abbilden.
4. **OECD-Mindestbesteuerung (`ab 2024`):**
   - Traditionell war die ZKB als kantonale Anstalt weitgehend steuerbefreit und leistete stattdessen hohe Gewinnausschüttungen an Kanton und Gemeinden. Ab Geschäftsjahr **2024** greift die **OECD-Mindeststeuer (Pillar 2, ~156–169 Mio. CHF)**, wodurch der Steueraufwand sprunghaft ansteigt und der Konzerngewinn *nach* Steuern strukturell tiefer liegt als bei direktem Vergleich mit Vorjahren! In Bericht 01 und Bericht 05 zwingend *Gewinn vor Steuern* und *Gesamtpartizipation Kanton/Gemeinden (inkl. OECD-Mindeststeuer)* darstellen.
5. **Umklassierung verwaltete Vermögen vs. Custody Services (`2024`, angepasst per 31.12.2023):**
   - 2024 präzisierte die ZKB die Abgrenzung zwischen *Verwalteten Vermögen (AuM)* und *Custody Services* (**–55,0 Mrd. CHF** Umklassierung per 31.12.2023, NNM –9,35 Mrd. CHF). Im Validation-Log und in Bericht 02 dokumentieren.
6. **Basel III final (`ab 01.01.2025`):** Auswirkung auf RWA-Dichte, CET1-Quote und TLAC per `2025` und `06-2026` quantifizieren.
7. **Einheiten:** ZKB weist Konzerntabellen teils in **Mio. CHF** (statt TCHF wie bei kleineren Kantonalbanken) aus! Der Extractor muss die Tabellen-Kopfzeile (`in Mio. CHF` vs. `in CHF 1'000`) strikt lesen; `validator_kpi.py` prüft zusätzlich einen Plausibilitätskorridor (`total_assets` > 80'000 Mio. CHF).

---

## 3. ZKB-spezifische Ankerbegriffe & `bank_config.yaml`-Eckwerte

### Zusätzliche/angepasste Ankerbegriffe (`chunker.py`)
- **Bilanz (Konzern):** `Konzernbilanz`, `Total Aktiven`, `Hypothekarforderungen`, `Verpflichtungen aus Kundeneinlagen`, `Dotationskapital`
- **Erfolgsrechnung (Konzern):** `Konzernerfolgsrechnung`, `Netto-Erfolg aus dem Zinsengeschäft`, `Erfolg aus dem Kommissions- und Dienstleistungsgeschäft`, `Erfolg aus dem Handelsgeschäft`, `Geschäftsertrag`, `Geschäftserfolg`, `Konzerngewinn`
- **Ausschüttung & Kanton (statt Aktie):** `Gewinnausschüttung`, `Ausschüttung an Kanton und Gemeinden`, `Abgeltung der Staatsgarantie`, `OECD-Mindeststeuer`, `Dotationskapital`
- **Offenlegung (D-SIB):** `KM1`, `KM2` (TLAC / Verlustabsorptionsfähigkeit), `OV1`, `Going-Concern`, `Gone-Concern`, `Leverage Ratio (TBTF)`
- **Vergütung (Corporate Governance):** `Bankrat`, `Bankpräsidium`, `Geschäftsleitung`, `Vorsitzender der Geschäftsleitung` (CEO)

### Vorgabe für `zkb/bank_config.yaml`
- `bank_id: "zkb"`, `reporting_scope: "consolidated"`, `listed: false`, `finma_category: 2`, `state_guarantee: true`
- `report_05_mode: "cantonal_endowment"`
- `report_05_slug: "05_dotationskapital_ausschuettung_und_kanton_zuerich"`
- **Markenfarben (`palette`):** Primary `#0050A0` (ZKB-Blau), Secondary `#0B1F3A`, Accent `#0095D9`, Muted `#64748B`
- **Epochen (Bericht 07):**
  1. `2003–2012`: *Universalbank-Ausbau & Bewährung in der Finanzkrise*
  2. `2013–2019`: *Systemrelevanz (D-SIB), Swisscanto-Integration (2015) & Negativzins-Ära*
  3. `2020–2026`: *Skalierung als grösste Kantonalbank, Zinswende, OECD-Mindeststeuer & Basel III final*

---

## 4. Katalog der 7 ZKB-Mehrjahresberichte & 13 Grafiken

| Nr. | Bericht (`zkb/reports/`) | Fokus & Besonderheiten gegenüber BEKB |
| :---: | :--- | :--- |
| **01** | `01_zinszyklen_und_ertragsarchitektur.md` | Drei-Säulen-Ertragsmodell (Zins ~50–55 %, Kommission/Swisscanto ~30 %, Handel ~12–15 %) + Effekt der OECD-Mindeststeuer 2024/2025 |
| **02** | `02_bilanzwachstum_hypotheken_und_refinanzierung.md` | Bilanzwachstum auf > 200 Mrd. CHF, Hypotheken vs. übrige Ausleihungen, AuM-Sprung 2015 (Swisscanto) & Custody-Umklassierung 2024 |
| **03** | `03_aufsichtsrechtliche_resilienz_basel_iii.md` | **D-SIB / TBTF-Fokus:** Going-Concern-Kapital, Gone-Concern / TLAC (Bail-in-Bonds), TBTF-Leverage Ratio, LCR, NSFR & Basel III final |
| **04** | `04_operative_effizienz_und_transformation.md` | Skaleneffekte bei > 5'000 FTE, CIR-Entwicklung, IT-/Digitalisierungs-Investitionen & Standortnetz (~50 Filialen) |
| **05** | `05_dotationskapital_ausschuettung_und_kanton_zuerich.md` | **Kein Aktienbericht:** Rendite auf Dotationskapital, kumulierte Gewinnausschüttungen an Kanton & Gemeinden (z. B. 562 Mio. in 2024, 581 Mio. in 2025), Abgeltung Staatsgarantie & OECD-Mindeststeuer |
| **06** | `06_unterjaehrige_dynamik_semesterberichte.md` | H1/FY-Saisonalität (Handels- vs. Zinsergebnis im 1. Semester), Reservensteuerung & Indikation H1-2026 |
| **07** | `07_strategische_epochen_und_governance.md` | Epochen-Scorecard + inflationsbereinigter Vergleich (real 2025 CHF, BFS LIK): Konzerngewinn vs. Personalaufwand vs. Bankrat-, CEO- & GL-Vergütung |
