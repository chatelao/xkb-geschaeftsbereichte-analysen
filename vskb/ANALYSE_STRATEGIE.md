# Daten- und Analysestrategie: Walliser Kantonalbank (VSKB / WKB / BCVs, 2003–2026)

> **Zielsetzung:** Strukturierte Extraktion, Normalisierung und mehrjährige Längsschnittanalyse über alle Geschäfts-, Halbjahres- und Offenlegungsberichte der **Walliser Kantonalbank (WKB / BCVs, Ordner `vskb/`)** – Pilotbank zur End-to-End-Validierung der gemeinsamen `shared/`-Pipeline durch **Gemini Hydrogen**.
> **Master-Plan:** Siehe [`../PLAN.md`](../PLAN.md) (Phase 1 – Pilotbank).

---

## 1. Bankprofil & Domänen-Kontext

| Merkmal | Ausprägung VSKB (WKB / BCVs) |
| :--- | :--- |
| **Offizieller Name** | Walliser Kantonalbank (WKB) / Banque Cantonale du Valais (BCVs) |
| **Rechtsform & Börse** | Öffentlich-rechtliche Aktiengesellschaft, **SIX Swiss Exchange (`WKB`)** |
| **Aktionariat** | **70,0 % Kanton Wallis**, 30,0 % Publikumsaktionariat (~13'700 Aktionäre; Aktienkapital 158 Mio. CHF) |
| **Staatsgarantie** | **Voll** (gemäss Art. 5 WKB-Gesetz haftet der Staat Wallis für alle Verbindlichkeiten der Bank) |
| **FINMA-Aufsichtskategorie** | **Kategorie 3** |
| **Abschluss-Scope** | **Einzelabschluss (`standalone`)** – analog BEKB, keine konsolidierungspflichtigen Tochtergesellschaften |
| **Primärsprache** | **Deutsch** (vollständige deutsche Ausgaben parallel zu Französisch verfügbar!) |
| **Berichtstypen** | Geschäftsbericht (`YYYY`), Halbjahresbericht / Zwischenabschluss (`H1-YYYY`), Offenlegungsbericht Basel III (`YYYY` & `06-YYYY`) |

### Offizielle Quellen für `vskb/download_reports.py`
1. **Primärarchiv WKB/BCVs:** `https://www.bcvs.ch/de/die-wkb/publikationen-medien/publikationen/alle-publikationen` (direkte PDFs unter `https://www.bcvs.ch/fileadmin/user_upload/site/publications/...`)
2. **VSKB-Archiv (Verband):** `https://vskb.ch/publikationen/jahresberichte` (z. B. `WKB_2024.pdf`, `WKB_2025.pdf` – **Achtung:** Nicht verwechseln mit Verbands-Jahresberichten!)
3. **Historisches Archiv (2003–2017):** Wayback Machine CDX API (`web.archive.org/cdx/search/cdx?url=bcvs.ch/*&filter=mimetype:application/pdf` sowie `wkb.ch/*`)

---

## 2. Warum VSKB (WKB) die ideale Pilotbank (Phase 1) ist

Die strukturelle Nähe zur BEKB-Referenz reduziert den Validierungsaufwand für die neu erstellte `shared/`-Bibliothek drastisch:
- **Identischer Abschluss-Scope:** Einzelabschluss (`standalone`), keine Konzern/Stammhaus-Verwechslungsgefahr.
- **Identische FINMA-Kategorie:** Kategorie 3 (Standard-ERV-Anhang-8-Zielgrössen).
- **Deutsch als Originalsprache:** Vollständige deutsche Geschäftsberichte minimieren Sprach-Edge-Cases im ersten Durchlauf (FR-Unterstützung wird anschliessend in Phase 3/4 mit BCV & GEKB gezielt belastet).
- **Börsenkotiert (`WKB`):** Testet direkt `report_05_mode: "listed_share"` inkl. Dividendenpolitik (Ziel-Payout-Ratio 40–60 % des bereinigten Ergebnisses) und Abgeltung der Staatsgarantie an den Kanton Wallis.

---

## 3. Kritische Datenbrüche & Fallstricke (VSKB / WKB-spezifisch)

1. **Zweisprachige Dateinamen & URLs:** Ältere Archiv-PDFs auf `bcvs.ch` tragen teils französische Pfade (`rapport-gestion`, `rapport-semestriel`), während die deutsche Version `WKB_Geschaeftsbericht_YYYY.pdf` heisst. Im `download_reports.py` systematisch DE bevorzugen und FR als dokumentierten Fallback zulassen.
2. **FINMA-RVB / ARB Umstellung (`2015`):** Umstellung von *Bruttogewinn* auf *Geschäftserfolg*, Umgliederung der Reserven für allgemeine Bankrisiken ins Eigenkapital.
3. **Jubiläumsjahr `2017` (100 Jahre WKB):** Mögliche Sonderdividende / Jubiläumsbeiträge (Stiftung 100 Jahre WKB) in Bericht 05 & 07 separat kennzeichnen.
4. **Starke Zinsabhängigkeit & Tourismus-/Immobilienregion Wallis:** Überdurchschnittlich tiefe Cost-Income-Ratio (historisch häufig < 45–50 % – eine der effizientesten Kantonalbanken der Schweiz!) bei hohem Hypothekar- und KMU-/Tourismus-Fokus.
5. **Aktiensplit / Kapitalerhöhungen prüfen:** Historische Aktienanzahl (15,8 Mio. Namenaktien à CHF 10 Nennwert) über den Zeitraum `2003–2025` auf allfällige Splits oder Nennwertänderungen prüfen und ggf. in `vskb/bank_config.yaml` (`share_splits`) hinterlegen.
6. **Basel III final (`ab 01.01.2025`):** Auswirkung auf RWA-Dichte und CET1-/Gesamtkapitalquote per `2025` und `06-2026`.

---

## 4. VSKB-spezifische Ankerbegriffe & `bank_config.yaml`-Eckwerte

### Ankerbegriffe (`chunker.py`, DE mit FR-Fallback)
- **Bilanz:** `Bilanz`, `Total Aktiven`, `Hypothekarforderungen`, `Forderungen gegenüber Kunden`, `Verpflichtungen aus Kundeneinlagen`, `Reserven für allgemeine Bankrisiken`, `Total Eigenkapital`
- **Erfolgsrechnung:** `Erfolgsrechnung`, `Netto-Erfolg aus dem Zinsengeschäft`, `Erfolg aus dem Kommissions- und Dienstleistungsgeschäft`, `Erfolg aus dem Handelsgeschäft`, `Geschäftsertrag`, `Personalaufwand`, `Sachaufwand`, `Geschäftsaufwand`, `Geschäftserfolg`, `Jahresgewinn`
- **Aktie & Kanton Wallis:** `WKB-Aktie`, `Börsenkurs`, `Dividende pro Aktie`, `Abgeltung der Staatsgarantie`, `Kanton Wallis`, `Leistungen an die öffentliche Hand`
- **Offenlegung:** `KM1`, `OV1`, `CC1`, `CET1`, `Gesamtkapitalquote`, `Leverage Ratio`, `LCR`, `NSFR`
- **Vergütung:** `Verwaltungsrat`, `Generaldirektion` (GL), `Präsident der Generaldirektion` (CEO)

### Vorgabe für `vskb/bank_config.yaml`
- `bank_id: "vskb"`, `short_name: "WKB (VSKB)"`, `reporting_scope: "standalone"`, `listed: true`, `ticker: "WKB"`, `finma_category: 3`, `state_guarantee: true`
- `report_05_mode: "listed_share"`
- `report_05_slug: "05_aktie_dividenden_und_wertschoepfung"`
- **Markenfarben (`palette`):** Primary `#C8102E` (Walliser Rot), Secondary `#1E293B`, Accent `#0F766E`, Muted `#64748B`
- **Epochen (Bericht 07):**
  1. `2003–2012`: *Konsolidierung, Wachstum im Heimmarkt Wallis & starke Effizienzbasis*
  2. `2013–2019`: *100-Jahr-Jubiläum (2017), Negativzins-Phase & Stärkung des Anlagegeschäfts*
  3. `2020–2026`: *Zinswende-Rekordergebnisse, Digitalisierung, CSR/Klima-Reporting & Basel III final*

---

## 5. Katalog der 7 VSKB-Mehrjahresberichte & 13 Grafiken

| Nr. | Bericht (`vskb/reports/`) | Fokus & Besonderheiten gegenüber BEKB |
| :---: | :--- | :--- |
| **01** | `01_zinszyklen_und_ertragsarchitektur.md` | Zinserfolg als Hauptertragspfeiler, Margenentwicklung über SNB-Zinszyklen & Ausbau Kommissionsgeschäft |
| **02** | `02_bilanzwachstum_hypotheken_und_refinanzierung.md` | Bilanzwachstum auf > 22 Mrd. CHF, Hypothekar-Dominanz im Kanton Wallis, Kundeneinlagen- & Pfandbrief-Refinanzierung |
| **03** | `03_aufsichtsrechtliche_resilienz_basel_iii.md` | Eigenmittelquoten (CET1, Gesamtkapital, Leverage Ratio) vs. FINMA-Kat.-3-Ziele, LCR/NSFR & Basel III final |
| **04** | `04_operative_effizienz_und_transformation.md` | Spitzen-CIR im Kantonalbankenvergleich (< 50 %), Produktivität je FTE, Filialnetz-Modernisierung |
| **05** | `05_aktie_dividenden_und_wertschoepfung.md` | WKB-Aktie (`WKB`), Ausschüttungspolitik (40–60 % Payout), Dividende (z. B. CHF 4.00 in 2025), Rückflüsse an Kanton Wallis (70 % + Staatsgarantie-Abgeltung + Steuern) |
| **06** | `06_unterjaehrige_dynamik_semesterberichte.md` | H1/FY-Saisonalität, antizyklische Dotierung der Bankrisikoreserven im 2. Semester & Indikation H1-2026 |
| **07** | `07_strategische_epochen_und_governance.md` | Epochen-Scorecard + inflationsbereinigter Vergleich (real 2025 CHF, BFS LIK): Gewinn vs. Personalaufwand vs. VR-, CEO- & Generaldirektions-Vergütung |
