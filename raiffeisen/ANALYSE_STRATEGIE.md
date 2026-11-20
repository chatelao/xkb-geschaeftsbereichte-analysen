# Daten- und Analysestrategie: Raiffeisen Gruppe Schweiz (2011–2026)

> **Zielsetzung:** Strukturierte Extraktion, Normalisierung und mehrjährige Längsschnittanalyse über alle Geschäfts-, Zwischen- und Offenlegungsberichte der **Raiffeisen Gruppe Schweiz** – umgesetzt über die gemeinsame `shared/`-Pipeline und optimiert für **Gemini Hydrogen**.
> **Master-Plan:** Siehe [`../PLAN.md`](../PLAN.md).

---

## 1. Bankprofil & Domänen-Kontext

| Merkmal | Ausprägung Raiffeisen |
| :--- | :--- |
| **Offizieller Name** | Raiffeisen Gruppe Schweiz (Verbund aus 218 Genossenschaftsbanken + Raiffeisen Schweiz Genossenschaft) |
| **Rechtsform & Eigentümer** | **Genossenschaftsverbund** (über 2 Mio. Genossenschafter mit Anteilscheinen, **nicht börsenkotiert**) |
| **Staatsgarantie** | **Keine** (Solidarhaftung innerhalb der Raiffeisen Gruppe über Haftungsverbund) |
| **FINMA-Aufsichtskategorie** | **Kategorie 2 – Inländisch systemrelevante Bank (D-SIB / TBTF)** (seit 2014) |
| **Abschluss-Scope** | **Konzernrechnung Raiffeisen Gruppe** (`reporting_scope: "consolidated"`, nicht Raiffeisen Schweiz Einzelinstitut) |
| **Primärsprache** | Deutsch (Parallel-Ausgaben auf Französisch & Italienisch) |
| **Berichtstypen** | Geschäftsbericht (`YYYY`), Zwischenabschluss (`H1-YYYY`), Aufsichtsrechtliche Offenlegung (`06-2015–06-2026`, quartalsweise/halbjährlich) |

### Offizielle Quellen für `raiffeisen/download_reports.py`
1. **Geschäfts- & Zwischenberichte:** `https://www.raiffeisen.ch/rch/de/ueber-uns/raiffeisen-gruppe/finanzinformationen/geschaeftsberichte.html` & `.../dokumente/archiv.html`
2. **Offenlegung (D-SIB / Basel III):** `https://www.raiffeisen.ch/rch/de/ueber-uns/raiffeisen-gruppe/finanzinformationen/offenlegung.html`

---

## 2. Kritische Datenbrüche & Fallstricke (Raiffeisen-spezifisch)

1. **Raiffeisen Gruppe vs. Raiffeisen Schweiz:** Auf der Website liegen jeweils zwei Geschäftsberichte pro Jahr vor (`*-raiffeisen-gruppe.pdf` und `*-raiffeisen-schweiz.pdf`). Für den Bankenvergleich wird zwingend die **Konzernrechnung der Raiffeisen Gruppe** verwendet!
2. **Genossenschaftsmodell & Anteilschein-Verzinsung (statt Dividende):**
   - Statt Aktienkapital und Dividende pro Aktie besitzt die Raiffeisen Gruppe **Genossenschaftskapital** (Anteilscheine) und hohe **Gewinnreserven / Thesaurierung** (typisch > 85–90 % Gewinnthesaurierung!).
   - Bericht 05 verwendet `report_05_mode: "cooperative"` (`05_genossenschaftskapital_thesaurierung_und_ausschuettung.md`).
3. **D-SIB / TBTF-Kapitalregime (seit `2014`):**
   - Als Kat.-2-Bank (D-SIB) weist Raiffeisen **Going-Concern-** und **Gone-Concern- (TLAC / Bail-in-Bonds)**-Quoten sowie die TBTF-Leverage Ratio aus. Besonderheit: Hoher Anteil an **hartem Kernkapital (CET1)** durch Gewinnthesaurierung und Anteilscheine.
4. **FINMA-RVB / ARB Umstellung (`2015`) & Basel III final (`2025`):**
   - Bruch 2014→2015 (Einführung *Geschäftserfolg*).
   - Einführung **Basel III final** ab `01.01.2025` (RWA-Dichte auf Hypothekarportfolio!).
5. **Hypothekar-Marktführerschaft:** Mit > 200 Mrd. CHF Hypothekarforderungen ist Raiffeisen der grösste Hypothekargeber der Schweiz (~18 % Marktanteil).

---

## 3. Raiffeisen-spezifische Ankerbegriffe & `bank_config.yaml`-Eckwerte

- **Bilanz (Gruppe):** `Konzernbilanz`, `Total Aktiven`, `Hypothekarforderungen`, `Verpflichtungen aus Kundeneinlagen`, `Genossenschaftskapital`, `Reserven für allgemeine Bankrisiken`
- **Erfolgsrechnung (Gruppe):** `Konzernerfolgsrechnung`, `Netto-Erfolg aus dem Zinsengeschäft`, `Geschäftsertrag`, `Geschäftserfolg`, `Gruppengewinn`
- **Vorgabe für `raiffeisen/bank_config.yaml`:**
  - `bank_id: "raiffeisen"`, `reporting_scope: "consolidated"`, `listed: false`, `finma_category: 2`, `state_guarantee: false`, `report_05_mode: "cooperative"`
  - **Palette:** Primary `#E2001A` (Raiffeisen-Rot), Secondary `#1E1E1E`, Accent `#F59E0B`, Muted `#64748B`
  - **Epochen (Bericht 07):**
    1. `2011–2014`: *Genossenschaftliches Wachstum & Weg zur Systemrelevanz (D-SIB)*
    2. `2015–2019`: *Negativzins-Ära, Governance-Reform & TBTF-Aufbau*
    3. `2020–2026`: *Hypothekar-Marktführerschaft, Zinswende & Basel III final*
