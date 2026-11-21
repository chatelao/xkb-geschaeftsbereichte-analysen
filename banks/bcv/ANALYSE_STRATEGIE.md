# Daten- und Analysestrategie: Banque Cantonale Vaudoise (BCV, 2003–2026)

> **Zielsetzung:** Strukturierte Extraktion, Normalisierung und mehrjährige Längsschnittanalyse über alle Geschäfts-, Halbjahres- und Pilier-3-Berichte der **Banque Cantonale Vaudoise (BCV / Waadtländer Kantonalbank)** – umgesetzt über die gemeinsame `shared/`-Pipeline und optimiert für **Gemini Hydrogen**.
> **Master-Plan:** Siehe [`../PLAN.md`](../PLAN.md) (Phase 3).

---

## 1. Bankprofil & Domänen-Kontext

| Merkmal | Ausprägung BCV |
| :--- | :--- |
| **Offizieller Name** | Banque Cantonale Vaudoise (BCV) |
| **Rechtsform & Börse** | Öffentlich-rechtliche Aktiengesellschaft, **SIX Swiss Exchange (`BCVN`)** |
| **Aktionariat** | **~66,95 % Kanton Waadt** (`Etat de Vaud`), ~33,05 % Publikumsaktionariat |
| **Staatsgarantie** | **Keine** (Rating AA S&P / Aa2 Moody's aus eigener Bilanzkraft, ohne Staatsgarantie) |
| **FINMA-Aufsichtskategorie** | **Kategorie 3** |
| **Abschluss-Scope** | **Konzernrechnung (`Groupe BCV` / `Comptes consolidés`)** – inkl. Piguet Galland & Cie SA, Gérifonds SA |
| **Primärsprache** | **Französisch** & **Englisch** (sehr konsistente parallele PDF-Reihen) – **Ausgabeberichte einheitlich auf Deutsch** |
| **Berichtstypen** | *Rapport annuel* (`YYYY`), *Rapport semestriel / intermédiaire* (`H1-YYYY`), *Rapport Bâle III – Pilier 3* (`YYYY` & `06-YYYY`) |

### Offizielle Quellen für `bcv/download_reports.py`
1. **Primärarchiv BCV:**
   - FR: `https://www.bcv.ch/fr/home/la-bcv/relations-investisseurs/news-et-rapports.html`
   - EN: `https://www.bcv.ch/en/home/la-bcv/investor-relations/reports.html`
   - Direkte DAM-Pfade: `https://www.bcv.ch/content/dam/bcv/fichiers/publications/publications-institutionnelles/rapports/...`
2. **VSKB-Archiv:** `https://vskb.ch/publikationen/jahresberichte` (z. B. `BCV_2024.pdf`, `BCV_2025.pdf`)
3. **Historisches Archiv (2003–2017):** Wayback Machine CDX API (`web.archive.org/cdx/search/cdx?url=bcv.ch/*&filter=mimetype:application/pdf`)

---

## 2. Kritische Datenbrüche & Fallstricke (BCV-spezifisch)

1. **Konzern (`Groupe BCV`) vs. Stammhaus (`BCV maison-mère`):** Der *Rapport annuel* enthält beide Abschlüsse. Der Chunker muss zwingend die **konsolidierten Tabellen** (`Bilan consolidé`, `Compte de résultat consolidé` bzw. `Consolidated balance sheet`) selektieren (`reporting_scope: "consolidated"`).
2. **Historische BCV-Krise & Restrukturierung (`2002–2005`):**
   - Nach den massiven Wertberichtigungen und der kantonalen Rekapitalisierung `2002/2003` durchlief die BCV einen der bemerkenswertesten Turnarounds im Schweizer Banking (Abbau Risikopositionen, Fokussierung auf 4 Kernsegmente, Rückkehr zu hoher Ausschüttungskraft). Die Startjahre `2003–2005` zeigen deshalb Sonderbewegungen bei Eigenkapital, Rückstellungen und Steuern, die im Validation-Log und in Bericht 07 klar kontextualisiert werden müssen.
3. **1:10-Aktiensplit (`28. Mai 2020`) – Pflicht-Bereinigung in Python!**
   - Am 28. Mai 2020 führte die BCV einen **1:10-Aktiensplit** durch (Nennwert CHF 10 → CHF 1; Aktienzahl 8,606 Mio. → 86,062 Mio.).
   - **Verbindliche Regel:** Gemini Hydrogen extrahiert stets den im jeweiligen Bericht abgedruckten Rohwert. `shared/validator_kpi.py` wendet deterministisch `share_splits: [{date: "2020-05-28", ratio: 10}]` an, damit Aktienkurs und Dividende/Ausschüttung über `2003–2025` bruchfrei vergleichbar sind!
4. **Zusammensetzung der Ausschüttung (`Dividende ordinaire` + `Remboursement de capital`):**
   - Über viele Jahre (v. a. `2008–2018`) kombinierte die BCV die ordentliche Dividende mit steuerfreien **Kapitalrückzahlungen aus Reserven / Nennwertreduktionen** (hohe Ausschüttungsquote von ~80–85 % des Konzerngewinns!). In Bericht 05 zwingend **Gesamtausschüttung pro Aktie** (ordentlich + Kapitalrückzahlung) ausweisen.
5. **IRB-Ansatz bei Kreditrisiken & *Basel III final* (`ab 01.01.2025`):**
   - Als eine der wenigen Kantonalbanken verwendet die BCV den **internen Ratingansatz (F-IRB)** für einen Grossteil der Kreditrisiken (mit *IRB Shortfall* und 2020 eingeführten *Provisions pour risques de défaillance inhérents* gemäss Art. 25/28 RelV-FINMA, finanziert über CHF 35 Mio. aus Bankrisikoreserven).
   - Dadurch ist der Übergang auf **Basel III final (ab 2025, inkl. Output Floor)** bei der BCV analytisch hochrelevant für Bericht 03!
6. **FINMA-RVB / ARB Umstellung (`2015`):** Einführung von *Résultat opérationnel* (*Geschäftserfolg*) und Netto-Zinserfolg.

---

## 3. BCV-spezifische Ankerbegriffe & `bank_config.yaml`-Eckwerte

### Französische / Englische Ankerbegriffe (`chunker.py`)
- **Bilanz (Konzern):** `Bilan consolidé`, `Total de l'actif`, `Créances hypothécaires`, `Créances sur la clientèle`, `Engagements résultant des dépôts de la clientèle`, `Total des capitaux propres`, `Réserves pour risques bancaires généraux` *(EN: `Consolidated balance sheet`, `Mortgage loans`, `Customer deposits`)*
- **Erfolgsrechnung (Konzern):** `Compte de résultat consolidé`, `Résultat net des opérations d'intérêts`, `Résultat des opérations de commissions`, `Résultat des opérations de négoce`, `Total des revenus`, `Charges de personnel`, `Autres charges d'exploitation`, `Total des charges d'exploitation`, `Résultat opérationnel`, `Bénéfice net`
- **Aktie & Kanton Waadt:** `Action BCV`, `Cours de clôture`, `Dividende ordinaire`, `Remboursement de capital`, `Distribution totale par action`, `Canton de Vaud`, `Contributions aux collectivités publiques`
- **Offenlegung (Pilier 3):** `KM1`, `OV1`, `CC1`, `CET1`, `Fonds propres réglementaires`, `Ratio CET1`, `Ratio de levier`, `LCR`, `NSFR`, `F-IRB`
- **Vergütung (Gouvernance):** `Conseil d'administration` (VR), `Direction générale` (GL), `Président de la Direction générale` (CEO)

### Vorgabe für `bcv/bank_config.yaml`
- `bank_id: "bcv"`, `short_name: "BCV"`, `reporting_scope: "consolidated"`, `listed: true`, `ticker: "BCVN"`, `finma_category: 3`, `state_guarantee: false`
- `share_splits: [{date: "2020-05-28", ratio: 10}]`
- `report_05_mode: "listed_share"`
- `report_05_slug: "05_aktie_dividenden_und_wertschoepfung"`
- **Markenfarben (`palette`):** Primary `#007A33` (BCV-Grün), Secondary `#0F2942`, Accent `#00A651`, Muted `#64748B`
- **Epochen (Bericht 07):**
  1. `2003–2008`: *Post-Restrukturierung, Bilanzbereinigung & Neuausrichtung der 4 Geschäftsbereiche*
  2. `2009–2019`: *Stabiles Ertragsmodell, hohe Ausschüttungspolitik (Dividende + Kapitalrückzahlung) & Akquisition Piguet Galland (2011)*
  3. `2020–2026`: *1:10-Aktiensplit (2020), Zinswende-Spitzenergebnisse, digitale Transformation & Basel III final (IRB-Übergang)*

---

## 4. Katalog der 7 BCV-Mehrjahresberichte & 13 Grafiken

| Nr. | Bericht (`bcv/reports/`) | Fokus & Besonderheiten gegenüber BEKB |
| :---: | :--- | :--- |
| **01** | `01_zinszyklen_und_ertragsarchitektur.md` | Ausbalanciertes 4-Säulen-Modell (Retail, Corporate, Wealth Management / Piguet Galland, Trading) – deutlich höherer Kommissions- & Handelsanteil als BEKB/VSKB |
| **02** | `02_bilanzwachstum_hypotheken_und_refinanzierung.md` | Wachstum auf > 60 Mrd. CHF Bilanzsumme, Waadtländer Hypothekenmarkt, Trade Finance & verwaltete Vermögen (> 110 Mrd. CHF) |
| **03** | `03_aufsichtsrechtliche_resilienz_basel_iii.md` | Hohe CET1-Quote (~17 %+) **ohne Staatsgarantie** (praktisch reines CET1, kaum T2), F-IRB-Ansatz & Übergang zu *Bâle III final* (2025/06-2026) |
| **04** | `04_operative_effizienz_und_transformation.md` | CIR-Stabilität (~55–59 % bei breiterem Geschäftsmodell), FTE-Produktivität (~1'900–2'000 EPT) & Filialnetz im Kanton Waadt |
| **05** | `05_aktie_dividenden_und_wertschoepfung.md` | **Split-bereinigte** BCVN-Aktie (1:10-Split 2020), Gesamtausschüttung (Dividende + Kapitalrückzahlung), > 80 % Ausschüttungsquote & Milliarden-Rückflüsse an den Kanton Waadt (66,95 %) |
| **06** | `06_unterjaehrige_dynamik_semesterberichte.md` | H1/FY-Saisonalität der *Rapports semestriels*, Rückstellungs- & Reservensteuerung sowie Indikation H1-2026 |
| **07** | `07_strategische_epochen_und_governance.md` | Epochen-Scorecard (Turnaround → Ausschüttungsmaschine → Zinswende) + inflationsbereinigter Vergleich (real 2025 CHF, BFS LIK): Konzerngewinn vs. Personalaufwand vs. VR-, CEO- & GL-Vergütung |
