# Verbesserungsplan für Gemini Hydrogen: Datenqualität, Branchenvergleiche (Investoren & Mitarbeitende) & Vorsorgeeinrichtungen

> **Auftrag:** Dieses Dokument ist das verbindliche Abarbeitungs-Runbook für **Gemini Hydrogen** zur qualitativen und inhaltlichen Aufwertung aller 8 Einzelbank-Auswertungen (`bekb`, `vskb`, `zkb`, `bcv`, `gekb`, `raiffeisen`, `postfinance`, `ubs`) sowie der institutsübergreifenden Auswertung (`comparison/`).
> **Ausgangslage (Audit-Stand nach Commit `996bf1d`):** Technisch sind alle 56 Einzelbank-Berichte, 104 Einzelbank-Grafiken, 5 Cross-Bank-Berichte und 9 Vergleichsgrafiken vorhanden und `mkdocs build --strict` läuft grün. Das inhaltlich-qualitative Audit hat jedoch **gravierende Datenlücken, einzelne Skalierungs-/Zuordnungsfehler sowie fehlende Analysetiefe** identifiziert, die zwingend vor neuen Auswertungen behoben werden müssen.

---

## Teil A: Befunde des Qualitäts-Audits (Ist-Zustand)

### 1. Kritische Zahlen- & Skalierungsfehler (Blocker — Prio 1)

| Institut | Befund im aktuellen Bestand | Ursache | Erwarteter Zielwert (Grössenordnung) |
| :--- | :--- | :--- | :--- |
| **UBS** | `total_operating_income_mio = 43,7`, `net_profit_mio = 6,8`, `roe_pct = 0,01 %` (2025) | **1'000×-Skalierungsfehler:** `normalize_to_mio()` dividierte `USD million`-Werte bei `unit=None` durch `1'000`; die Disambiguierung skalierte nur Felder mit identischer `unit` wie `total_assets`. | Ertrag ~`43'700 Mio. CHF`, Gewinn ~`6'800 Mio. CHF`, ROE ~`8–9 %` |
| **UBS** | `leverage_ratio_pct = 1'658'089,00 %` (Offenlegung H1-2025) | Zeile `Leverage ratio denominator` (in Mio. USD) wurde als `leverage_ratio_pct` gematcht. | ~`4,5–5,0 %` |
| **BCGE (GEKB)** | `net_profit_mio = 9,0`, `roe_pct = 0,36 %` (2025) | Falsche Tabellenzeile in `gekb-geschaeftsbericht-2025.md` getroffen. | Reingewinn ~`190–220 Mio. CHF`, ROE ~`8–10 %` |
| **BCV** | `dividend_per_share = 4'403,00 CHF` (2025) | Falsche Zeile/Einheit (z. B. Gesamtausschüttung / TCHF oder fehlendes Komma). | ~`4,40 CHF` je Aktie |
| **ZKB** | `shareholders_equity_mio = 2'425,0`, `roe_pct = 51,18 %` (2025) | Dotationskapital statt **Total Eigenkapital** (inkl. Reserven für allg. Bankrisiken / Gewinnreserven) extrahiert. | Eigenkapital ~`14'500–16'000 Mio. CHF`, ROE ~`8–9 %` |
| **BEKB** | `fte_count = 1'273,0` (2025) → verzerrt `Ertrag/FTE` (`429,9` statt `517,3 TCHF`) und `Lohn/FTE real` (`120,9` statt `145,4 TCHF`) | **Personen (Headcount)** statt **Vollzeitstellen (FTE = `1'058`)** gematcht. | `1'058,0 FTE` (analog Referenz-Repo) |

### 2. Systematische Datenlücken in Kernspalten (Prio 1)

Obwohl `--strict-audit` grün war (es prüfte bisher nur `total_assets_mio`, `total_operating_income_mio`, `net_profit_mio`), sind zentrale Spalten grossflächig leer:

- **Eigenkapital & ROE (`shareholders_equity_mio`, `roe_pct`):** 100 % leer bei `bekb` (`23/23`), `vskb` (`15/15`), `postfinance` (`13/13`); teilweise leer bei `zkb` (`5/12`) und `bcv` (`5/19`).
- **Ertragsstruktur (`net_interest_income_mio`, `commission_income_mio`, `trading_income_mio`):** Fast leer bei `bekb` (`21/23`), `zkb` (`12/12`), `postfinance` (`11/13`), `ubs` (`6/6`) → `comparison/reports/01_*.md` zeigt bei 5 von 8 Banken `– %`.
- **Personalbestand (`fte_count`):** 100 % leer bei `bcv` (`19/19`), `gekb` (`23/23`), `raiffeisen` (`15/15`), `ubs` (`6/6`); `14/15` leer bei `vskb`, `11/13` leer bei `postfinance`.
- **Aktie, Dividende & Öffentliche Hand (`share_price_eoy`, `dividend_per_share`, `contribution_public_mio`, `branch_count`):** Nahezu durchgehend leer.
- **Offenlegung (`cet1_ratio_pct`, `total_capital_ratio_pct`, `leverage_ratio_pct`, `lcr_pct`, `nsfr_pct`):** Am jüngsten Stichtag (`H1-2026` bzw. `H1-2025`) ist `cet1_ratio_pct` bei **allen 8 Banken leer (`– %`)**! Über alle Stichtage: `vskb` `0/13`, `zkb` `1/44`, `bcv` `1/35`, `gekb` `1/24`, `ubs` `0/4`; `lcr_pct` bei 6 Banken `0`.
- **Vergütung (`vr_total_tchf`, `ceo_total_tchf`, `gl_total_tchf`):** Bei **allen 8 Banken `0`** (100 % leer).
- **Semesterberichte (`net_profit_mio`):** `vskb` `0/12`, `gekb` `3/18`.

### 3. Inhaltliche & redaktionelle Schwächen (Prio 2)

- **Widerspruch zwischen Text und Tabelle:** In `comparison/reports/03_*.md` behauptet das Management Summary *"Sämtliche 8 Institute übertreffen ihre jeweiligen FINMA-Zielgrössen komfortabel"*, während die Tabelle darunter **achtmal `– %`** bei CET1-Ist ausweist.
- **Oberflächliche Textbausteine:** Die aktuellen Berichte (`22–45` Zeilen) erreichen nicht die analytische Tiefe der BEKB-Referenzberichte (konkrete Wendepunkt-Datierung, Treiber-Zerlegung, Epochen-Einordnung, saubere Kennzahlen-Verknüpfung).

---

## Teil B: Priorisierter Verbesserungsplan für Gemini Hydrogen (Phasen V1–V5)

> **Ausführungsregel:** Arbeite `V1 → V2 → V3 → V4 → V5` strikt sequenziell ab. Starte keine neue Phase, bevor das zugehörige **Qualitäts-Gate** mit Exit-Code `0` bestanden ist.

---

### Phase V1: Extraktor-Härtung & verschärfte Plausibilitäts-Gates (`shared/`)

**Ziel:** Alle Skalierungs-, Zeilen- und KM1-Tabellenfehler an der Wurzel beheben und `--strict-audit` so verschärfen, dass kein fehlerhafter Wert mehr unbemerkt durchläuft.

#### Atomare Aufgaben
1. **`shared/extractor.py` härten:**
   - **Prozent-Guard verschärfen:** Für `leverage_ratio_pct` explizit `denominator` / `gesamtengagement` / `exposition` ausschliessen; für `cet1_ratio_pct` / `total_capital_ratio_pct` / `lcr_pct` / `nsfr_pct` Werte ausserhalb plausibler Prozentbereiche (`0 < x < 1000` bzw. `< 100` bei Kapital-/Leverage-Quoten) ablehnen.
   - **KM1-Spezialparser für Offenlegungsberichte:** FINMA-KM1-Tabellen erkennen Zeilennummern (`1`, `2`, `3`, `4`, `5`, `6`, `7`, `13`, `14`, `15`, `17`, `20`, `22`) sowie Spaltenköpfe `a | b | c | d | e` (mit Stichtag in Zeile 2) in DE/FR/EN, damit `cet1_capital`, `rwa_total`, `cet1_ratio_pct`, `total_capital_ratio_pct`, `leverage_ratio_pct`, `lcr_pct`, `nsfr_pct` zuverlässig extrahiert werden.
   - **Eigenkapital & Ertragskomponenten:** `shareholders_equity` explizit von `Dotationskapital` / `Aktienkapital` abgrenzen (muss `Total Eigenkapital` / `Total des capitaux propres` / `Total equity` sein); `fte_count` strikt von `Headcount` / `Personen` / `Mitarbeitende (Köpfe)` trennen (`Vollzeitstellen`, `FTE`, `EPT`, `teilzeitbereinigt`).
   - **Währungs-/Einheiten-Vererbung pro Tabelle:** Für jede Tabelle `default_unit` aus `bank_config.yaml` (z. B. `Mio. USD` bei UBS, `Mio. CHF` bei ZKB/Raiffeisen/PostFinance/BCV/GEKB, `TCHF` bei BEKB) als Fallback hinterlegen, falls kein Header über dem Tabellenfragment steht — statt blind durch `1'000` zu dividieren.
   - **Dividende vs. Gesamtausschüttung:** `dividend_per_share` nur matchen, wenn `je Aktie` / `par action` / `per share` vorliegt und Wert `< 500` (bzw. vor Split `< 2'000`).
2. **`shared/validator_kpi.py` — Verschärftes `--strict-audit`:**
   - **Einheiten-Disambiguierung auf alle monetären Zeilen** anwenden (nicht nur Zeilen mit gleicher `unit` wie `total_assets`), oder separate Plausibilitätskorridore für Bilanz, Ertrag und Gewinn prüfen.
   - **Harte Bereichs-Assertions im `--strict-audit`:**
     - `0 < roe_pct < 35` (Ausnahme: `extraordinary_flag`, z. B. UBS 2023 CS-Goodwill)
     - `25 < cir_pct < 110`
     - `2.0 < leverage_ratio_pct < 20.0`
     - `8.0 < cet1_ratio_pct < 40.0`
     - `80.0 < lcr_pct < 600.0`
     - `60.0 < avg_per_fte_tchf_real2025 < 450.0`
     - `0 < dividend_per_share < 250.0` (split-bereinigt)
   - **Vollständigkeits-Gate (für das jüngste Geschäftsjahr 2025 & H1-2026):** `0` fehlende Werte bei `total_assets_mio`, `shareholders_equity_mio`, `net_interest_income_mio`, `commission_income_mio`, `total_operating_income_mio`, `total_operating_expenses_mio`, `net_profit_mio`, `cir_pct`, `roe_pct`, `fte_count` sowie `cet1_ratio_pct`, `leverage_ratio_pct`, `lcr_pct` am jüngsten Offenlegungsstichtag.
3. **Bank-spezifische `overrides.json` & Vergütungsdaten (`vr`, `gl`, `ceo`):**
   - Für `bekb` die geprüften Daten aus dem BEKB-Referenz-Repo (insbesondere `bekb_verguetung_real_2003_2025.csv`, FTE `1'058`, Eigenkapital, Dividenden, öffentliche Hand) sauber in `bekb/overrides.json` / Parser übernehmen.
   - Für alle weiteren 7 Banken die Vergütungsberichte (`verguetung`-Chunks, inkl. `zkb-geschaeftsbericht-2025-verguetungsbericht.md`, UBS Compensation Report, BCV/GEKB/VSKB/Raiffeisen/PostFinance Corporate-Governance-Abschnitte) mindestens für die Jahre **`2020–2025`** (ideal ab `2015`) vollständig auslesen (`vr_total_tchf`, `gl_total_tchf`, `ceo_total_tchf`, `vr_seats`, `gl_fte`).

#### Qualitäts-Gate V1
- `pytest tests/` inkl. neuer Plausibilitäts- & KM1-Parser-Tests grün.
- `validator_kpi --bank <b > --strict-audit` besteht für **alle 8 Banken** unter den verschärften Bereichs- und Vollständigkeits-Gates (0 `–` in den 2025-Kernspalten, 0 unplausible Quoten wie UBS `1'658'089 %` oder ZKB `51,18 %` ROE).

---

### Phase V2: Datenerhebung der zugehörigen Vorsorgeeinrichtungen (Pensionskassen)

**Ziel:** Aufbau eines einheitlichen, belegbaren **Pensionskassen-Datensatzes** (`<bank>/data/<bank>_vorsorge.json` + konsolidiert `comparison/data/xkb_vorsorgeeinrichtungen.csv`) als integraler Bestandteil des Mitarbeiter-Branchenvergleichs und der Governance-Analyse.

#### Bereits identifizierte Vorsorgeeinrichtungen & Primärquellen im Repo

| Institut | Zugehörige Vorsorgeeinrichtung | Primärquelle im Repo (`.md/`) | Ergänzende externe Quelle (falls im Bank-GB nicht vollständig) |
| :--- | :--- | :--- | :--- |
| **BEKB** | **Pensionskasse der Berner Kantonalbank AG** | Anhang Vorsorgeverpflichtungen (`bekb-geschaeftsbericht-2024.md:4451`: Deckungsgrad `126,0 %` 2024 / `120,2 %` 2023; PK-Einlage 2015 `83,8 Mio.`) | Geschäftsbericht PK BEKB (`pk-bekb.ch`) |
| **VSKB (WKB)** | **Pensions- und Vorsorgekasse für das Personal der Walliser Kantonalbank** | Anhang Ziff. 8.13 / 10.3 (`vskb-geschaeftsbericht-2021.md`: Einlage `29,0 Mio. CHF` 2020; Stiftungsrat in `vskb-geschaeftsbericht-2024.md:2655`) | Geschäftsbericht PK WKB (`bcvs.ch`) |
| **ZKB** | **Pensionskasse der Zürcher Kantonalbank** | Anhang Vorsorgeverpflichtungen & Lagebericht (`zkb-geschaeftsbericht-2024.md:2847`: `6'039` aktive Versicherte, `2'282` Rentner) | Geschäftsbericht PK ZKB (`pkzkb.ch`) |
| **BCV** | **Caisse de pensions de la Banque Cantonale Vaudoise** *(umhüllend)* | Nachhaltigkeits-/Sozialbericht & Anhang (`bcv-geschaeftsbericht-2024.md:732–734`: `2'210` Aktive, `1'479` Rentner) | Rapport annuel Caisse de pensions BCV (`cpbcv.ch`) |
| **GEKB (BCGE)** | **Fondation de prévoyance professionnelle de la BCGE** | Anhang Konzernrechnung (`gekb-geschaeftsbericht-2024.md:3507`, `4917`) | Rapport annuel Fondation de prévoyance BCGE |
| **Raiffeisen** | **Raiffeisen Pensionskasse** (& *Raiffeisen Arbeitgeberstiftung*, St. Gallen) | Anhang Vorsorgeverpflichtungen (`raiffeisen-geschaeftsbericht-2024.md:3309`) | Geschäftsbericht Raiffeisen Pensionskasse (`raiffeisen-pensionskasse.ch`) |
| **PostFinance** | **Pensionskasse Post** | Anhang Ziff. 15 *Verpflichtungen gegenüber eigenen Vorsorgeeinrichtungen*, Swiss GAAP FER 16/26 (`postfinance-geschaeftsbericht-2024.md:2191`, `2803`) | Geschäftsbericht Pensionskasse Post (`pkpost.ch`) |
| **UBS** | **Pensionskasse der UBS (Pension Fund of UBS)** *(inkl. Integration CS-PK Schweiz)* | IAS 19 *Note 26 Post-employment benefit plans* (`ubs-geschaeftsbericht-2024.md:2390–2406`) | Geschäftsbericht PK UBS (`pensionskasse-ubs.ch` — für BVG-Deckungsgrad gemäss Art. 44 BVV 2, da IFRS/IAS 19 abweicht!) |

#### Kanonisches Erhebungsschema pro Vorsorgeeinrichtung (Jahre `2020–2025`, mind. `2024/2025`)
Für jedes der 8 Institute erhebt Gemini Hydrogen deterministisch (zuerst aus den vorhandenen `.md`-Dateien via neuem Chunk `vorsorge` in `shared/chunker.py`, fehlende BVG-Kennzahlen sauber gekennzeichnet aus den offiziellen PK-Geschäftsberichten):
1. `pk_name` & `pk_plan_type` (`Beitragsprimat` / `Leistungsprimat` / `Duoprimat`, `umhüllend` vs. `gesplittet`)
2. `active_insured_count` & `pensioners_count` (Verhältnis Aktive zu Rentnern → demografische Resilienz!)
3. `coverage_ratio_bvg_pct` (Deckungsgrad nach Art. 44 BVV 2 in %) & `technical_interest_rate_pct` (Technischer Zinssatz)
4. `interest_crediting_pct` (Effektive Verzinsung der Altersguthaben `2021–2025` vs. BVG-Mindestzinssatz)
5. `conversion_rate_65_pct` (Umwandlungssatz im ordentlichen Rentenalter 65)
6. `employer_contribution_mio` & `employer_share_pct` (Arbeitgeberbeitrag in Mio. CHF bzw. Arbeitgeberanteil in % der Gesamtbeiträge, z. B. 60/40 oder 65/35)
7. `employer_contribution_reserve_mio` (Arbeitgeberbeitragsreserve / AGBR) & `extraordinary_contributions_mio` (Sanierungs-/Sondereinlagen, z. B. BEKB 2015, VSKB 2020)
8. `source_url_or_file` & `accounting_basis` (`Swiss GAAP FER 16/26` vs. `IAS 19` — explizite Warnung bei UBS-Vergleich!).

#### Qualitäts-Gate V2
- `comparison/data/xkb_vorsorgeeinrichtungen.csv` existiert und enthält alle 8 Institute mit belegten Quellenangaben (`source_url_or_file`), ohne erfundene Werte (nicht verfügbare Felder explizit `null` / `n. a.`).

---

### Phase V3: Ausbau der Einzelbank-Berichte & Investoren-/Mitarbeiter-Perspektive

**Ziel:** Jede der 8 Banken erhält qualitativ tiefgehende, widerspruchsfreie Berichte (ohne generische Platzhalter-Sätze) und wird um die Perspektiven **Investoren** und **Mitarbeitende (inkl. Vorsorge)** erweitert.

#### Atomare Aufgaben
1. **Qualitäts-Upgrade der Berichte 01–07 in `shared/report_builder.py`:**
   - **Keine ungedeckten Aussagen:** Jeder Satz im Management Summary darf nur Kennzahlen interpretieren, die im zugehörigen Datenpanel tatsächlich vorhanden (`not None`) sind (automatischer Guard im Template).
   - **Konkrete Trend- & Wendepunkt-Synthese:** Automatische Berechnung und textliche Einbindung von Minimum/Maximum-Jahren, Vor-/Nach-Zinswende-Delta (`2021` vs. `2023/2024` vs. `2025`), 5-Jahres- und Gesamt-CAGR sowie Epochen-Durchschnitten.
   - **Bank-spezifische Einordnung:** Strukturbrüche aus `bank_config.yaml` (z. B. UBS CS-Übernahme, PostFinance Kreditverbot, BCV 1:10-Split & IRB, ZKB Custody-Umklassierung & OECD-Steuer, BEKB PK-Einlage 2015) werden quantitativ in den betroffenen Berichten eingeordnet.
   - **Optionaler Hydrogen-Reduce-Pass (`--backend gemini`):** Strukturierte Prompt-Vorlagen für narrative Abschnitte mit strikter Zahlen-Verifikation (Post-Check: jede Zahl im generierten Text muss in der Eingabetabelle vorkommen).
2. **Ergänzung in Bericht 05 & Bericht 07 (pro Bank):**
   - **Bericht 05 (Investoren-/Eigentümer-Sicht):** Ergänzung um **Total Shareholder Return (TSR)** (Kursentwicklung + kumulierte Dividenden bei kotierten Banken), **Ausschüttungsquote (Payout Ratio)**, **Kurs-Buchwert-Verhältnis (P/B)**, **KGV (P/E)** bzw. bei nicht-kotierten Instituten **Rendite auf Dotations-/Genossenschafts-/Eigenkapital** & Ausschüttungsstabilität.
   - **Bericht 07 (Mitarbeiter- & Vorsorge-Sicht):** Ergänzung um einen dedizierten Abschnitt **«Arbeitgeber-Attraktivität & Pensionskasse»** mit realer Personalaufwandsentwicklung pro FTE (`real 2025 CHF`), **CEO-zu-Mitarbeitenden-Vergütungs-Ratio**, und den wichtigsten Kennzahlen der hauseigenen **Vorsorgeeinrichtung** (Deckungsgrad, Verzinsung, Arbeitgeberanteil).

---

### Phase V4: Zwei neue Branchenvergleichs-Berichte (Investoren & Mitarbeitende) in `comparison/`

**Ziel:** Erweiterung von `shared/compare_banks.py` um **zwei dedizierte, tiefgehende Branchenvergleiche** über alle 8 Institute (inkl. Peer-Gruppen-Einordnung `Kantonalbanken`, `Inland-D-SIBs`, `G-SIB`) sowie zugehörige 300-DPI-Grafiken.

#### 1. Neuer Bericht `comparison/reports/06_investoren_branchenvergleich.md`
**Fragestellung:** *Welches Institut bietet Investoren bzw. öffentlichen Eigentümern das attraktivste Risiko-Rendite- und Ausschüttungsprofil?*
- **Segment A — Kotierte Institute (`BEKB`, `VSKB`, `BCV`, `GEKB`, `UBS`):**
  - Bewertungskennzahlen (`2025` & 5-Jahres-Ø): **P/E (KGV)**, **P/B (Kurs-Buchwert)**, **Dividendenrendite (%)**, **Payout Ratio (%)**, **Aktienrückkäufe** (UBS), **5-Jahres-TSR (Total Shareholder Return 2020–2025)** (split-bereinigt!).
  - Risiko-Adjustierung: **ROE vs. CET1-Quote** (Kapitalrendite unter Berücksichtigung der Kapitalstärke) und **Ertragsstabilität** (Volatilität von Geschäftsertrag & Reingewinn `2015–2025`).
- **Segment B — Nicht-kotierte / Öffentliche & Genossenschafts-Eigentümer (`ZKB`, `Raiffeisen`, `PostFinance` + Kantonsanteile der 5 KB):**
  - Gesamtablieferung an die öffentliche Hand / Eigentümer (Dividende + Steuern + Staatsgarantie-Abgeltung) in Mio. CHF und in % des Eigenkapitals.
  - Vergleich **Staatsgarantie-Prämie vs. Kapitalkosten** (`ZKB/VSKB` mit Staatsgarantie vs. `BEKB/BCV/GEKB` ohne).
- **Neue Investoren-Grafiken (`comparison/reports/charts/`):**
  - `10_investoren_bewertung_pb_vs_roe_2025.png` (P/B vs. ROE-Regressionslinie der 5 kotierten Banken + Dividendenrendite)
  - `11_investoren_tsr_und_ausschuettung_2020_2025.png` (5J-TSR & Ausschüttungsquote im Branchenvergleich)

#### 2. Neuer Bericht `comparison/reports/07_mitarbeiter_und_vorsorge_branchenvergleich.md`
**Fragestellung:** *Wie schneiden die 8 Institute aus Sicht der Mitarbeitenden ab (Entlöhnung, Produktivität, Vergütungsspreizung, Arbeitsplatzstabilität und Pensionskasse)?*
- **Vergütung & Kaufkraft (`real 2025 CHF`):**
  - Personalaufwand pro FTE nominal & real (`2020–2025`), reale Lohnkosten-Entwicklung (Kaufkraftgewinn/-verlust seit 2015/2020).
  - **Vergütungsspreizung (Pay Ratio):** `CEO-Gesamtvergütung / Ø Personalaufwand pro FTE` sowie `GL-Durchschnitt / Ø Personalaufwand pro FTE` über alle 8 Institute.
- **Produktivität & Arbeitsplatz-Dynamik:**
  - `Geschäftsertrag / FTE` und `Geschäftserfolg / FTE` vs. `Personalaufwand / FTE` (Personal-Wertschöpfungsquote).
  - FTE-Aufbau vs. -Abbau (`2015–2025` & `2020–2025`) und Filialnetz-Transformation.
- **Vorsorgeeinrichtungen (Pensionskassen-Benchmark der 8 Institute):**
  - Tabellarischer Gesamtvergleich aller 8 Pensionskassen: **Deckungsgrad (BVG %)**, **Verzinsung Altersguthaben (5-Jahres-Ø vs. BVG-Minimum)**, **Umwandlungssatz Alter 65**, **Arbeitgeber-Beitragsanteil (%)**, **Verhältnis Aktive / Rentner**, **Sondereinlagen / AGBR**.
  - Methodischer Hinweis auf `Swiss GAAP FER 16/26` (CH-Banken) vs. `IAS 19` (UBS Konzernrechnung) und Abgleich über den BVG-Deckungsgrad der *Pensionskasse der UBS*.
- **Neue Mitarbeiter- & Vorsorge-Grafiken (`comparison/reports/charts/`):**
  - `12_mitarbeiter_lohn_produktivitaet_pay_ratio_2025.png` (Personalaufwand/FTE real vs. Ertrag/FTE & CEO-Pay-Ratio)
  - `13_vorsorgeeinrichtungen_deckungsgrad_verzinsung.png` (Deckungsgrad BVG % & Verzinsung der 8 Pensionskassen im Branchenvergleich)

---

### Phase V5: Portal-Integration, Tests & Endabnahme

1. **`mkdocs.yml` & `shared/prepare_docs.py` aktualisieren:**
   - Neue Navigationspunkte unter `Bankenvergleich (8 Institute)` für Bericht `06 · Investoren-Branchenvergleich` und `07 · Mitarbeiter- & Vorsorge-Branchenvergleich` einbinden.
2. **Test-Suite (`tests/`) erweitern:**
   - `tests/test_plausibility_and_quality.py`: Prüft für **alle 8 Banken** automatisch die Plausibilitätsgrenzen (ROE, CIR, CET1, Leverage, Dividende, FTE, Lohn/FTE) und dass keine Tabelle in `comparison/reports/01..07` mehr als definierte Toleranz an `–`-Lücken enthält.
   - `tests/test_vorsorge.py`: Prüft Schema, Quellenbelege und Wertebereiche (`50 < coverage_ratio_bvg_pct < 200`) von `comparison/data/xkb_vorsorgeeinrichtungen.csv`.
3. **Endabnahme-Kommandos (müssen alle mit Exit-Code `0` bestehen):**
   ```bash
   uv run --with pytest --with pyyaml --with matplotlib pytest -v tests/
   for b in bekb vskb zkb bcv gekb raiffeisen postfinance ubs; do
     uv run --with pyyaml python3 -m shared.validator_kpi --bank "$b" --strict-audit
     uv run --with pyyaml python3 -m shared.report_builder --bank "$b" --backend local
     uv run --with matplotlib --with pyyaml python3 -m shared.chart_engine --bank "$b"
   done
   uv run --with matplotlib --with pyyaml python3 -m shared.compare_banks --backend local
   uv run --with pyyaml python3 -m shared.prepare_docs
   uvx --with mkdocs-material --with pymdown-extensions mkdocs build --strict
   ```
4. **Commit & Push auf `main`** nach jeder abgeschlossenen Verbesserungsphase (`V1` bis `V5`).
