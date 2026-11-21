# Daten- und Analysestrategie: Banque Cantonale de Genève (GEKB / BCGE, 2003–2026)

> **Zielsetzung:** Strukturierte Extraktion, Normalisierung und mehrjährige Längsschnittanalyse über alle Geschäfts-, Halbjahres- und Offenlegungsberichte der **Banque Cantonale de Genève (BCGE / Genfer Kantonalbank, Ordner `gekb/`)** – umgesetzt über die gemeinsame `shared/`-Pipeline und optimiert für **Gemini Hydrogen**.
> **Master-Plan:** Siehe [`../PLAN.md`](../PLAN.md) (Phase 4).

---

## 1. Bankprofil & Domänen-Kontext

| Merkmal | Ausprägung GEKB (BCGE) |
| :--- | :--- |
| **Offizieller Name** | Banque Cantonale de Genève SA (BCGE) |
| **Rechtsform & Börse** | Öffentlich-rechtliche Aktiengesellschaft, **SIX Swiss Exchange (`BCGE`)** |
| **Aktionariat (öffentliche Hand)** | **~72,6 % öffentliche Hand** über Aktionärsbindungsvertrag: Kanton Genf (~44,3 %), Stadt Genf (~20,9 %), Genfer Gemeinden (~7,4 %); Streubesitz ~27,4 % (> 15'000 Aktionäre) |
| **Staatsgarantie** | **Keine** (unbeschränkte Staatsgarantie abgeschafft; ordentliche Einlagensicherung esisuisse bis CHF 100'000) |
| **FINMA-Aufsichtskategorie** | **Kategorie 3** |
| **Abschluss-Scope** | **Konzernrechnung (`Groupe BCGE` / `Comptes consolidés`)** – inkl. BCGE France, Capital Transmission, Dimension, Loyal Finance |
| **Primärsprache** | **Französisch** (einzelne Pressemitteilungen/Kurzberichte auf DE/EN) – **Ausgabeberichte einheitlich auf Deutsch** |
| **Berichtstypen** | *Rapport de gestion / Rapport annuel* (`YYYY`), *Rapport semestriel* (`H1-YYYY`), *Publication du Pilier III / Exigences de publication* (`YYYY` & `06-YYYY`) |

### Offizielle Quellen für `gekb/download_reports.py`
1. **Primärarchiv BCGE:** `https://www.bcge.ch/fr/rapports-financiers` (direkte PDF-Links unter `https://www.bcge.ch/documents/395713/...`)
2. **VSKB-Archiv:** `https://vskb.ch/publikationen/jahresberichte` (z. B. `BCGE_2024.pdf`, `BCGE_2025.pdf`)
3. **Historisches Archiv (2003–2017):** Wayback Machine CDX API (`web.archive.org/cdx/search/cdx?url=bcge.ch/*&filter=mimetype:application/pdf`)

---

## 2. Kritische Datenbrüche & Fallstricke (GEKB / BCGE-spezifisch)

1. **Konzern (`Groupe BCGE`) vs. Stammhaus (`Maison-mère`):** Der *Rapport de gestion* enthält beide Abschlüsse. Der Chunker muss zwingend die **konsolidierten Tabellen** (*Bilan consolidé*, *Compte de résultat consolidé*) selektieren (`reporting_scope: "consolidated"`).
2. **Nachgang der Genfer Bankensanierung / *Fondation de valorisation* (`2000–2008`):**
   - In den frühen 2000er-Jahren erfolgten noch Nachwirkungen aus der Auslagerung notleidender Immobilienkredite in die *Fondation de valorisation* (abgeschlossen 2008) sowie eine schrittweise Stärkung der Eigenmittel ohne Staatsgarantie. Historische Einmaleffekte und Rückstellungen in diesem Zeitraum im Validation-Log und in Bericht 07 sauber isolieren.
3. **FINMA-RVB / ARB Umstellung (`2015`):** Einführung des *Résultat opérationnel* (*Geschäftserfolg*) und neue Darstellung der Wertberichtigungen im Zinsengeschäft (*Résultat net des opérations d'intérêts*).
4. **Globales Geschäftsmodell (*Global Commodity Finance* & *BCGE France*):**
   - Im Unterschied zu rein regionalen Kantonalbanken finanziert die BCGE signifikante Rohstoffhandels- und Unternehmenskredite (Genfer Handelsplatz) sowie Aktivitäten in Frankreich. Dadurch ist das Verhältnis von *Créances sur la clientèle* zu *Créances hypothécaires* höher als bei BEKB/VSKB – das muss in Bericht 02 (Bilanz- & Kreditstruktur) und Bericht 01 (Handels- & Kommissionsertrag) herausgearbeitet werden.
5. **Aktiensplit / Nennwertänderung prüfen (`2025/2026`):**
   - Aktuelle BCGE-Mitteilungen zu 2025/2026 prüfen, ob ein **Aktiensplit** (z. B. 1:10 zur Erhöhung der Liquidität der Aktie, Hinweis: intrinsischer Wert ~CHF 34.71 vs. früher ~CHF 300+) durchgeführt wurde! Falls ja, das exakte Split-Datum und Verhältnis (`ratio`) in `gekb/bank_config.yaml` (`share_splits`) eintragen, damit `shared/validator_kpi.py` die historische Kurs- und Dividendenreihe deterministisch glättet.
6. **Basel III final (`ab 01.01.2025`):** Auswirkung auf RWA (insbesondere Corporate / Commodity Finance & Hypotheken) und Gesamtkapitalquote (*Ratio global de fonds propres*) per `2025` und `06-2026`.
7. **Französisches Zahlen- & Einheitenformat:** Tabellen oft in `en milliers de CHF` (`TCHF`) oder `en millions de CHF` (`Mio. CHF`), Leerzeichen als Tausendertrennzeichen (`32 145`) und Komma oder Punkt als Dezimaltrennzeichen. Alle Sonderfälle über `tests/test_number_parser.py` absichern.

---

## 3. GEKB-spezifische Ankerbegriffe & `bank_config.yaml`-Eckwerte

### Französische Ankerbegriffe (`chunker.py`)
- **Bilanz (Konzern):** `Bilan consolidé`, `Total de l'actif`, `Créances hypothécaires`, `Créances sur la clientèle`, `Engagements résultant des dépôts de la clientèle`, `Total des capitaux propres`, `Réserves pour risques bancaires généraux`
- **Erfolgsrechnung (Konzern):** `Compte de résultat consolidé`, `Résultat net des opérations d'intérêts`, `Résultat des opérations de commissions`, `Résultat des opérations de négoce`, `Total des produits d'exploitation`, `Charges de personnel`, `Autres charges d'exploitation`, `Total des charges d'exploitation`, `Résultat opérationnel`, `Bénéfice net`
- **Aktie & Öffentliche Hand:** `Cours de l'action`, `Dividende par action`, `Actionnariat`, `Etat de Genève`, `Ville de Genève`, `Communes genevoises`, `Contribution aux collectivités publiques`
- **Offenlegung (Pilier III):** `KM1`, `OV1`, `CC1`, `Fonds propres de base durs (CET1)`, `Ratio CET1`, `Ratio de levier`, `LCR`, `NSFR`
- **Vergütung (Gouvernance):** `Conseil d'administration` (VR), `Direction générale` (GL), `Président de la Direction générale` / `CEO`

### Vorgabe für `gekb/bank_config.yaml`
- `bank_id: "gekb"`, `short_name: "BCGE (GEKB)"`, `reporting_scope: "consolidated"`, `listed: true`, `ticker: "BCGE"`, `finma_category: 3`, `state_guarantee: false`
- `report_05_mode: "listed_share"`
- `report_05_slug: "05_aktie_dividenden_und_wertschoepfung"`
- **Markenfarben (`palette`):** Primary `#005A4B` (BCGE-Dunkelgrün), Secondary `#1B365D`, Accent `#D4A017`, Muted `#64748B`
- **Epochen (Bericht 07):**
  1. `2003–2009`: *Nach-Sanierungs-Konsolidierung & Abschluss Fondation de valorisation*
  2. `2010–2019`: *Organisches Wachstum, Diversifikation (BCGE France / Asset Management) & Eigenmittelaufbau ohne Staatsgarantie*
  3. `2020–2026`: *Rekordprofitabilität in der Zinswende, Kapitalstärkung, Digitalisierung & Basel III final*

---

## 4. Katalog der 7 GEKB-Mehrjahresberichte & 13 Grafiken

| Nr. | Bericht (`gekb/reports/`) | Fokus & Besonderheiten gegenüber BEKB |
| :---: | :--- | :--- |
| **01** | `01_zinszyklen_und_ertragsarchitektur.md` | Zins- vs. Kommissions- & Handelserträge am Finanzplatz Genf (Private Banking, Asset Management, Commodity Finance) |
| **02** | `02_bilanzwachstum_hypotheken_und_refinanzierung.md` | Duale Kreditstruktur (Hypotheken + Firmen-/Handelsfinanzierungen), Kundengelder-Deckungsgrad & AuM-Wachstum |
| **03** | `03_aufsichtsrechtliche_resilienz_basel_iii.md` | Eigenmittelstärke **ohne Staatsgarantie**, CET1-/Gesamtkapital-Puffer gegenüber FINMA-Kat.-3-Zielen & Basel-III-final-Effekt |
| **04** | `04_operative_effizienz_und_transformation.md` | CIR-Entwicklung, Produktivität je EPT (FTE), Filialnetz Genf + Tochtergesellschaften |
| **05** | `05_aktie_dividenden_und_wertschoepfung.md` | **Split-bereinigte** BCGE-Aktie (`BCGE`), Dividendenreihe, Kurs-Buchwert-Verhältnis & kumulierte Rückflüsse an **Kanton Genf, Stadt Genf und Gemeinden (~72,6 %)** + Steuern |
| **06** | `06_unterjaehrige_dynamik_semesterberichte.md` | H1/FY-Saisonalität der *Rapports semestriels* & Indikation H1-2026 |
| **07** | `07_strategische_epochen_und_governance.md` | Epochen-Scorecard + inflationsbereinigter Vergleich (real 2025 CHF, BFS LIK): Konzerngewinn vs. Personalaufwand vs. VR-, CEO- & GL-Vergütung |
