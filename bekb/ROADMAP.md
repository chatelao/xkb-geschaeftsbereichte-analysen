# Roadmap: Schrittweise Konvertierung der BEKB PDF-Berichte in Markdown

Diese Roadmap beschreibt den strukturierten Plan zur schrittweisen Konvertierung aller PDF-Dokumente im Ordner `pdf/` in strukturierte Markdown-Dateien im Ordner `.md/`, inklusive der Extraktion von Bildelementen und Tabellen.

---

## 1. Übersicht & Zielsetzung

- **Ziel:** Konvertierung aller 57 PDF-Dateien (Geschäftsberichte 2003–2025, Semesterberichte 2013–2026 sowie Jahres- und Halbjahres-Offenlegungsberichte 2015–2026) in sauberes, lesbares Markdown mit referenzierten Bildern.
- **Zielordner:** `.md/` für Markdown-Dateien und `.md/images/` für extrahierte Grafiken/Bilder.
- **Werkzeuge:** Python, `pymupdf4llm` (PyMuPDF) für qualitativ hochwertige Layout- und Tabellenerfassung.

---

## 2. Bestandsaufnahme

### PDF-Dateien in `pdf/`
- **Geschäftsberichte (23 Dateien):**
  - `bekb-geschaeftsbericht-2003.pdf` bis `bekb-geschaeftsbericht-2025.pdf`
- **Semesterberichte (14 Dateien):**
  - `bekb-semesterbericht-2013.pdf` bis `bekb-semesterbericht-2026.pdf`
- **Offenlegungsberichte (20 Dateien):**
  - Jahresberichte: `bekb-offenlegungsbericht-2015.pdf` bis `bekb-offenlegungsbericht-2025.pdf` (11 Dateien)
  - Halbjahresberichte: `bekb-offenlegungsbericht-06-2018.pdf` bis `bekb-offenlegungsbericht-06-2026.pdf` (9 Dateien)

### Aktueller Fortschritt
- [x] Semesterberichte 2013–2026 konvertiert (`.md/bekb-semesterbericht-2013.md` bis `2026.md`)
- [x] Geschäftsberichte 2003–2025 konvertiert (`.md/bekb-geschaeftsbericht-2003.md` bis `2025.md`)
- [x] Offenlegungsberichte 2015–2025 & 06-2018–06-2026 konvertiert (`.md/bekb-offenlegungsbericht-*.md`)

---

## 3. Phaseneinteilung

### Phase 1: Vorbereitung & Skripterstellung
- [x] Download-Skript für fehlende Berichte erstellen (`download_reports.py`)
- [x] Erstellung eines Konvertierungsskripts (`convert_pdf_to_md.py`):
  - Automatisches Einlesen aller PDF-Dateien aus `pdf/`
  - Konvertierung mittels `pymupdf4llm.to_markdown()`
  - Bildextraktion nach `.md/images/<pdf-name>/`
  - Speichern der `.md`-Dateien in `.md/`
- [x] Abhängigkeiten verifizieren (`pymupdf4llm`, `PyMuPDF`)

### Phase 2: Konvertierung der Semesterberichte (2013–2026)
- [x] Semesterberichte 2013–2015
- [x] Batch 1: Semesterberichte 2016–2019
- [x] Batch 2: Semesterberichte 2020–2023
- [x] Batch 3: Semesterberichte 2024–2026
- [x] Sichtprüfung und Qualitätskontrolle der erzeugten `.md`-Dateien

### Phase 3: Konvertierung der Geschäftsberichte (2003–2025) & Offenlegungsberichte
- [x] Batch 1: Geschäftsberichte 2003–2009 (Ältere Berichte, einfache/klassische Layouts)
- [x] Batch 2: Geschäftsberichte 2010–2016 (Mittlere Dekade, komplexere Tabellen, inkl. Reparatur abgeschnittener PDFs)
- [x] Batch 3: Geschäftsberichte 2017–2025 (Neueste Berichte, umfangreiche Finanztabellen)
- [x] Batch 4: Offenlegungsberichte 2015–2025 sowie 06-2018–06-2026
- [x] Überprüfung der Bild- und Tabellenintegrität

### Phase 4: Qualitätskontrolle & Nachbearbeitung
- [x] Automatische Validierung:
  - Vollständigkeit prüfen (1:1 Abgleich PDF zu MD: 57/57)
  - Prüfung abgebrochener/fehlender Bildreferenzen (0 fehlend)
- [x] Stichprobenartige manuelle Nachbearbeitung von Tabellenformatierungen
- [x] Dokumentation & Bereinigung von temporären Dateien

---

## 4. Richtlinien & Konventionen

- **Dateibenennung:**
  - PDF: `bekb-geschaeftsbericht-YYYY.pdf` / `bekb-semesterbericht-YYYY.pdf` / `bekb-offenlegungsbericht-[06-]YYYY.pdf`
  - MD: `.md/bekb-geschaeftsbericht-YYYY.md` / `.md/bekb-semesterbericht-YYYY.md` / `.md/bekb-offenlegungsbericht-[06-]YYYY.md`
  - Bilder: `.md/images/<pdf-filename>/...`
- **Formatierung:**
  - Standard-Markdown-Header (`#`, `##`, `###`) für Überschriften.
  - Tabellen im Markdown-Format.
  - Bildlinks in relativer Pfadangabe (`![Alt-Text](images/...)`).

---

## 5. Meilensteine & Nachverfolgung

| Meilenstein | Beschreibung | Status |
| :--- | :--- | :--- |
| **M1** | Infrastruktur & Konvertierungsskript eingerichtet | Abgeschlossen |
| **M2** | Alle Semesterberichte (2013–2026) konvertiert | Abgeschlossen |
| **M3** | Geschäftsberichte 2003–2009 konvertiert | Abgeschlossen |
| **M4** | Geschäftsberichte 2010–2025 & Offenlegungsberichte konvertiert | Abgeschlossen |
| **M5** | Finaler Review & Abschlussdokumentation (57/57 Berichte) | Abgeschlossen |
