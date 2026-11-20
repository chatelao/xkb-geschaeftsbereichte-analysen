# Daten- und Analysestrategie: PostFinance AG (2013–2026)

> **Zielsetzung:** Strukturierte Extraktion, Normalisierung und mehrjährige Längsschnittanalyse über alle Geschäfts-, Halbjahres- und Offenlegungsberichte der **PostFinance AG** – umgesetzt über die gemeinsame `shared/`-Pipeline und optimiert für **Gemini Hydrogen**.
> **Master-Plan:** Siehe [`../PLAN.md`](../PLAN.md).

---

## 1. Bankprofil & Domänen-Kontext

| Merkmal | Ausprägung PostFinance |
| :--- | :--- |
| **Offizieller Name** | PostFinance AG (100 % Tochtergesellschaft der Schweizerischen Post AG) |
| **Rechtsform & Eigentümer** | Aktiengesellschaft (**100 % Die Schweizerische Post AG**, mittelbar Bund; **nicht börsenkotiert**) |
| **Staatsgarantie** | **Keine** (explizite Staatsgarantie per Verselbständigung Juni 2013 aufgehoben) |
| **FINMA-Aufsichtskategorie** | **Kategorie 2 – Inländisch systemrelevante Bank (D-SIB / TBTF)** (seit 2015) |
| **Abschluss-Scope** | **Einzelabschluss / Geschäftsbericht PostFinance AG** (`reporting_scope: "standalone"`) |
| **Primärsprache** | Deutsch (Parallel-Ausgaben auf FR, IT, EN) |
| **Berichtstypen** | Geschäftsbericht (`2013–2025`, seit Gründung 2013), Halbjahresbericht (verfügbare Einzelberichte), Offenlegungsbericht (`2013–06-2026`, quartalsweise/halbjährlich) |

### Offizielle Quellen für `postfinance/download_reports.py`
1. **Geschäfts- & Halbjahresberichte:** `https://www.postfinance.ch/de/ueber-uns/medien/berichterstattung/geschaeftsbericht.html` & `halbjahresbericht.html`
2. **Offenlegung (D-SIB / Eigenmittel):** `https://www.postfinance.ch/de/ueber-uns/medien/berichterstattung/offenlegungen.html`

---

## 2. Kritische Datenbrüche & Fallstricke (PostFinance-spezifisch)

1. **Gründung per 26. Juni 2013 & Kreditvergabeverbot (Art. 3 Abs. 3 POG):**
   - PostFinance AG existiert als regulierte Bank erst seit **2013**.
   - Aufgrund des gesetzlichen **Kredit- und Hypothekarvergabeverbots** (Postorganisationsgesetz) hält PostFinance praktisch **keine klassischen Hypothekarforderungen** auf eigener Bilanz, sondern investiert die Kundeneinlagen (~90–100 Mrd. CHF) primär in **Finanzanlagen (Anleihen)**, **Forderungen gegenüber Banken** und **SNB-Sichtguthaben**!
   - Deshalb sind `hypothekarforderungen` ≈ 0 bzw. `n/a`, während `finanzanlagen` und *Netto-Zinsmarge* extrem stark an das SNB-Leitzinsniveau gekoppelt sind.
2. **Negativzins-Sonderdynamik (`2015–2022`) & Zinswende (`2022–2025`):**
   - In der Negativzinsphase erodierte der Zinserfolg massiv (mangels Kreditbuch zur Fristentransformation); 2023–2024 folgte ein starker Rebound bei Zinswende und anschliessende Normalisierung 2025.
3. **D-SIB / TBTF-Kapitalregime (seit `2015`):**
   - Trotz fehlendem Kreditbuch ist PostFinance aufgrund des systemkritischen Zahlungsverkehrs und Einlagenvolumens als **Kat. 2 (D-SIB)** eingestuft (Going-Concern- & Gone-Concern-Anforderungen, inkl. Kapitalzuschüssen / Nachrangdarlehen der Schweizerischen Post AG).
4. **Ausschüttung an Die Schweizerische Post (`report_05_mode: "parent_company"`):**
   - Dividenden und Kapitaltransaktionen fliessen direkt an die Muttergesellschaft **Die Schweizerische Post AG**.
5. **Rechnungslegung:** Geschäftsbericht nach **IFRS** (und statutarisch nach Schweizer Bankenrechnungslegung / ARB). Konsequent **IFRS-Konzern-/Berichtszahlen** (bzw. klar getrennte ARB-Kennzahlen für Offenlegung) dokumentieren!

---

## 3. PostFinance-spezifische Ankerbegriffe & `bank_config.yaml`-Eckwerte

- **Bilanz:** `Bilanzsumme`, `Total Aktiven`, `Finanzanlagen`, `Flüssige Mittel`, `Kundeneinlagen` / `Verpflichtungen aus Kundeneinlagen`, `Eigenkapital`
- **Erfolgsrechnung:** `Betriebsertrag`, `Zinserfolg` / `Nettozinsertrag`, `Kommissions- und Dienstleistungserfolg`, `Betriebsaufwand`, `Unternehmensgewinn` / `Jahresgewinn`
- **Vorgabe für `postfinance/bank_config.yaml`:**
  - `bank_id: "postfinance"`, `reporting_scope: "standalone"`, `listed: false`, `finma_category: 2`, `state_guarantee: false`, `report_05_mode: "parent_company"`
  - **Palette:** Primary `#FFCC00` (Post-Gelb), Secondary `#1A1A1A`, Accent `#006699`, Muted `#64748B`
  - **Epochen (Bericht 07):**
    1. `2013–2015`: *Verselbständigung als Bank-AG & Beginn der Negativzinsen*
    2. `2016–2021`: *Zinserosion unter Negativzinsen, Gebührenmodell & D-SIB-Aufbau*
    3. `2022–2026`: *Zinswende-Rebound, Digitalbanking & Basel III final*
