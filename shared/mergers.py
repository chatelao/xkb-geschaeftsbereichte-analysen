"""Deterministische Fusions-, Übernahme- und Institutsgeschichtsdaten seit 1900 für alle 14 Banken."""

from __future__ import annotations

from typing import Any

MERGER_HISTORY: dict[str, dict[str, Any]] = {
    "bekb": {
        "founded": "1834 (Kantonalbank von Bern) / 1846 (Hypothekarkasse des Kantons Bern)",
        "lineage_summary": (
            "Die heutige Berner Kantonalbank AG (BEKB | BCBE) entstand 1991 aus dem Zusammenschluss der "
            "1834 gegründeten Kantonalbank von Bern (KBB) und der 1846 gegründeten Hypothekarkasse des Kantons Bern (HKB). "
            "Nach der Abspaltung von vier jurassischen Niederlassungen an die neue BCJ (1979) wurde die BEKB 1998 als "
            "erste Kantonalbank der Schweiz in eine privatrechtliche Aktiengesellschaft nach OR umgewandelt."
        ),
        "mermaid": """flowchart TD
    KBB["Kantonalbank von Bern (gegr. 1834, Stand 1900)"] -->|"1979: Abgabe 4 Filialen an BCJ"| KBB79["Kantonalbank von Bern (ab 1979)"]
    HKB["Hypothekarkasse des Kantons Bern (gegr. 1846, Stand 1900)"] --> MERGE1991["1991: Fusion KBB + HKB zur Berner Kantonalbank"]
    KBB79 --> MERGE1991
    MERGE1991 --> AG1998["1998: Umwandlung in privatrechtliche AG (OR)"]
    AG1998 --> SG2006["2006–2012: Schrittweiser Wegfall der Staatsgarantie"]
    SG2006 --> BEKB["Berner Kantonalbank AG (BEKB | BCBE, heute)"]""",
        "milestones": [
            ["1834 / 1900", "Kantonalbank von Bern (KBB) & Hypothekarkasse des Kantons Bern (HKB)", "Ausgangslage 1900", "Zwei eigenständige bernische Staatsinstitute (Universal- vs. Hypothekarbank)"],
            ["1979", "Gründung Kanton Jura / Banque Cantonale du Jura (BCJ)", "Abspaltung", "Übertragung von vier jurassischen Niederlassungen der KBB an die neu gegründete BCJ"],
            ["1991", "Fusion KBB + HKB → Berner Kantonalbank", "Fusion", "Grosser Rat beschliesst mit 136:0 Stimmen den Zusammenschluss beider Staatsbanken"],
            ["1998", "Umwandlung in BEKB AG", "Rechtsformwechsel", "Erste Kantonalbank der Schweiz als privatrechtliche AG (Art. 620 OR); Kanton reduziert Anteil auf 51,5 %"],
            ["2006–2012", "Aufhebung der Staatsgarantie", "Regulierung", "Schrittweiser Übergang zu voller Eigenmittel- und Marktdisziplin ohne kantonale Haftung"],
        ],
        "sources": "BEKB Firmengeschichte (bekb.ch); Kanton Bern Beteiligungsbericht",
    },
    "vskb": {
        "founded": "1917 (Walliser Kantonalbank / Banque Cantonale du Valais)",
        "lineage_summary": (
            "Die Walliser Kantonalbank (WKB | BCVs) wurde 1917 als öffentlich-rechtliche Staatsbank des Kantons Wallis "
            "gegründet (nachdem die frühere Banque Cantonale du Valais von 1858–1871 liquidiert worden war). "
            "Seit 1900 blieb das Institut nach seiner Neugründung 1917 frei von Grossfusionen und wurde 1993 in eine "
            "börsenkotierte spezialgesetzliche Aktiengesellschaft umgewandelt."
        ),
        "mermaid": """flowchart TD
    VORG["Kantonale Kreditversorgung Wallis (1900–1916)"] -->|"1917: Neugründung"| WKB1917["Walliser Kantonalbank (1917, öffentlich-rechtlich)"]
    WKB1917 --> AG1993["1993: Umwandlung in börsenkotierte AG"]
    AG1993 --> BCVS["Walliser Kantonalbank AG / BCVs (heute)"]""",
        "milestones": [
            ["1900–1916", "Übergangsphase nach Liquidation der ersten WKB (1871)", "Vorgeschichte", "Kantonale Kreditversorgung über Sparkassen und Hypothekarkasse vor Neugründung"],
            ["1917", "Gründung der Walliser Kantonalbank (WKB / BCVs)", "Gründung", "Öffentlich-rechtliche Anstalt mit voller Staatsgarantie des Kantons Wallis"],
            ["1993", "Umwandlung in eine Aktiengesellschaft (SIX-kotiert)", "Rechtsformwechsel", "Öffnung des Aktienkapitals für private und institutionelle Investoren"],
            ["2017–2026", "100-Jahr-Jubiläum & digitales Universalbank-Ausbau", "Organisches Wachstum", "22 Filialen in Ober-, Mittel- und Unterwallis; keine Grossfusionen"],
        ],
        "sources": "WKB / BCVs Geschäftsberichte; Historisches Lexikon der Schweiz",
    },
    "zkb": {
        "founded": "1870 (Zürcher Kantonalbank)",
        "lineage_summary": (
            "Die Zürcher Kantonalbank (ZKB) wurde 1870 gegründet und operiert seit 1900 ununterbrochen als "
            "selbstständige öffentlich-rechtliche Anstalt des Kantons Zürich. Der bedeutendste anorganische "
            "Wachstumsschritt seit 1900 war die Übernahme der Swisscanto Holding AG (2014/2015) von den übrigen Kantonalbanken."
        ),
        "mermaid": """flowchart TD
    ZKB1900["Zürcher Kantonalbank (gegr. 1870, Stand 1900)"] --> ZKB2014["Zürcher Kantonalbank (öffentlich-rechtliche Anstalt)"]
    SC1973["Swisscanto Anlagestiftung (1973) & Vorsorge AG (1983)"] --> SC1993["Swisscanto Holding AG (1993, Gemeinschaftswerk aller KB)"]
    SC1993 -->|"2014/2015: Übernahme durch ZKB"| ZKB2015["ZKB + Swisscanto (drittgrösster Fondsanbieter CH)"]
    ZKB2014 --> ZKB2015
    ZKB2015 --> ZKB["Zürcher Kantonalbank (heute)"]""",
        "milestones": [
            ["1870 / 1900", "Zürcher Kantonalbank", "Ausgangslage 1900", "Selbstständige öffentlich-rechtliche Anstalt mit unbeschränkter Staatsgarantie"],
            ["1973 / 1983 / 1993", "Gründung Swisscanto-Gruppe (Anlagestiftung, Vorsorge AG, Holding AG)", "Gemeinschaftsplattform", "Gemeinsame Fonds- und Vorsorgeplattform der Schweizer Kantonalbanken"],
            ["2014–2015", "Übernahme der Swisscanto Holding AG", "Akquisition", "Vollständige Integration von Swisscanto in die ZKB (rückwirkend per 01.07.2014)"],
            ["2022–2026", "Swisscanto-Markenvereinheitlichung & Asset Management", "Integration", "Ausbau zur Top-3-Fondsanbieterin der Schweiz (~500 Mrd. CHF AuM)"],
        ],
        "sources": "ZKB Geschäftsberichte; Swisscanto Chronik (swisscanto.com)",
    },
    "bcv": {
        "founded": "1845 (Banque Cantonale Vaudoise)",
        "lineage_summary": (
            "Die Banque Cantonale Vaudoise (BCV, gegr. 1845) konsolidierte in den 1990er-Jahren den Waadtländer "
            "Bankenmarkt durch die Übernahme der Banque Vaudoise de Crédit (1993) und die historische Fusion mit dem "
            "Crédit Foncier Vaudois (1995), der zuvor 1993 mit der Caisse d'Épargne et de Crédit fusioniert hatte."
        ),
        "mermaid": """flowchart TD
    BCV1900["Banque Cantonale Vaudoise (gegr. 1845, Stand 1900)"] --> BCV1993["1993: Übernahme Banque Vaudoise de Crédit"]
    BVC["Banque Vaudoise de Crédit (BVC)"] --> BCV1993
    CEC["Caisse d'Épargne et de Crédit (CEC)"] -->|"1993: Fusion"| CFV1993["Crédit Foncier Vaudois + CEC"]
    CFV["Crédit Foncier Vaudois (CFV)"] --> CFV1993
    BCV1993 --> FUS1995["1995: Historische Fusion BCV + CFV"]
    CFV1993 --> FUS1995
    FUS1995 --> REKAP["2001–2003: Rekapitalisierung durch Kanton Waadt (84 % -> 67 %)"]
    REKAP --> BCV["Banque Cantonale Vaudoise (BCV, heute)"]""",
        "milestones": [
            ["1845 / 1900", "Banque Cantonale Vaudoise (BCV)", "Ausgangslage 1900", "Gegründet 1845 per Dekret; 1903 Bezug des Hauptsitzes Place Saint-François 14"],
            ["1993", "Übernahme Banque Vaudoise de Crédit (BVC)", "Akquisition", "Integration der BVC in die BCV"],
            ["1993", "Fusion Crédit Foncier Vaudois (CFV) + Caisse d'Épargne et de Crédit (CEC)", "Vorfusion", "Konsolidierung der beiden Waadtländer Hypothekar- und Sparinstitute"],
            ["1995", "Fusion BCV + Crédit Foncier Vaudois (CFV)", "Fusion", "Zusammenschluss zur dominierenden Universalbank des Kantons Waadt"],
            ["2001–2003", "Rekapitalisierung & Bereinigung Handelsgeschäft", "Restrukturierung", "Kanton Waadt erhöht vorübergehend Beteiligung; Fokus auf Waadtländer Kernmarkt"],
        ],
        "sources": "BCV Histoire (bcv.ch); Archives cantonales vaudoises",
    },
    "gekb": {
        "founded": "1816 (Caisse d'Épargne) / 1869 (BHCG) → 1994 Fusion zur BCGE",
        "lineage_summary": (
            "Die Banque Cantonale de Genève (BCGE) entstand am 1. Januar 1994 aus der Fusion zweier historischer "
            "Genfer Institute: der 1816 gegründeten Caisse d'Épargne de la République et Canton de Genève (CEG) und "
            "der 1869 gegründeten Banque Hypothécaire du Canton de Genève (BHCG). Später folgten gezielte Boutique-Akquisitionen "
            "wie Dimension SA (2015) und Loyal Finance AG (2019)."
        ),
        "mermaid": """flowchart TD
    CEG["Caisse d'Épargne de Genève (CEG, gegr. 1816, Stand 1900)"] --> FUS1994["1994: Fusion CEG + BHCG → Banque Cantonale de Genève (BCGE)"]
    BHCG["Banque Hypothécaire du Canton de Genève (BHCG, gegr. 1869, Stand 1900)"] --> FUS1994
    FUS1994 --> RESTR2000["2000: Sanierung & Rekapitalisierung durch Kanton Genf"]
    RESTR2000 --> DIM2015["2015: Übernahme Dimension SA (M&A)"]
    RESTR2000 --> LF2019["2019: Übernahme Loyal Finance AG (Zürich)"]
    DIM2015 --> BCGE["Banque Cantonale de Genève (BCGE, heute)"]
    LF2019 --> BCGE""",
        "milestones": [
            ["1816 / 1900", "Caisse d'Épargne (CEG) & Banque Hypothécaire (BHCG)", "Ausgangslage 1900", "Zwei eigenständige Genfer Kantonal-/Sparkasseninstitute seit dem 19. Jh."],
            ["1994", "Fusion CEG + BHCG → Banque Cantonale de Genève (BCGE)", "Fusion", "Gründung der BCGE als öffentlich-rechtliche Aktiengesellschaft"],
            ["2000", "Kantonale Rekapitalisierung & Neuausrichtung", "Restrukturierung", "Bereinigung von Altlasten; Beginn der Ära Blaise Goetschin (2000–2024)"],
            ["2015 / 2019", "Übernahmen Dimension SA (Lausanne) & Loyal Finance AG (Zürich)", "Akquisitionen", "Ausbau von M&A-Beratung und institutionellem Obligationen-Asset-Management"],
        ],
        "sources": "BCGE Geschäftsberichte; Historisches Lexikon der Schweiz",
    },
    "raiffeisen": {
        "founded": "1899/1902 (Darlehenskasse Bichwil & Schweizerischer Raiffeisenverband)",
        "lineage_summary": (
            "Die Raiffeisen-Gruppe entstand 1899/1902 mit der ersten Darlehenskasse in Bichwil (SG) und dem "
            "Schweizerischen Raiffeisenverband (1902). Über das 20. Jahrhundert wuchs das Netz auf über 1'000 lokale "
            "Genossenschaften an, die durch laufende Regionalfusionen auf rund 218 Raiffeisenbanken konsolidiert wurden. "
            "2012 übernahm Raiffeisen Teile der Privatbank Wegelin & Co. (Notenstein, später Notenstein La Roche) und "
            "veräusserte Notenstein La Roche 2018 an Vontobel."
        ),
        "mermaid": """flowchart TD
    BICH["Darlehenskasse Bichwil (1899) & Verband (1902)"] --> NETZ["Ausbau auf >1'000 lokale Darlehenskassen (20. Jh.)"]
    NETZ -->|"Laufende Regionalfusionen"| GEN["Konsolidierung auf ~218 Raiffeisenbanken (heute)"]
    WEG["Privatbank Wegelin & Co. (gegr. 1741)"] -->|"2012: Übernahme Nicht-US-Geschäft"| NOTE["Notenstein Privatbank (2012) / Notenstein La Roche (2015)"]
    LARO["Bank La Roche & Co. (gegr. 1787)"] -->|"2015: Integration"| NOTE
    GEN -->|"2012–2018: Beteiligung/Tochter"| NOTE
    NOTE -->|"2018: Verkauf an Vontobel"| VONT["Bank Vontobel AG"]
    GEN --> RAIF["Raiffeisen Gruppe Schweiz (heute)"]""",
        "milestones": [
            ["1899 / 1902", "Darlehenskasse Bichwil & Schweizerischer Raiffeisenverband", "Gründung", "Start der schweizerischen Genossenschaftsbanken nach Friedrich Wilhelm Raiffeisen"],
            ["1902–2025", "Gründungswelle & spätere Regionalfusionen", "Konsolidierung", "Von über 1'200 lokalen Darlehenskassen zu rund 218 schlagkräftigen Raiffeisenbanken"],
            ["2012", "Übernahme Nicht-US-Geschäft von Wegelin & Co. (Notenstein)", "Akquisition", "Einstieg ins Private Banking über Tochtergesellschaft Notenstein Privatbank AG"],
            ["2015", "Übernahme Bank La Roche & Co. durch Notenstein", "Akquisition", "Fusion zu Notenstein La Roche Privatbank AG"],
            ["2018", "Verkauf von Notenstein La Roche an Vontobel", "Devestition", "Fokussierung auf das Schweizer Retail-, KMU- und Anlagegeschäft"],
        ],
        "sources": "Raiffeisen Schweiz Geschäftsberichte; Vontobel Chronik",
    },
    "postfinance": {
        "founded": "1906 (Postcheck- und Girodienst) / 2013 (PostFinance AG)",
        "lineage_summary": (
            "PostFinance geht auf den 1906 eingeführten schweizerischen Postcheck- und Girodienst zurück. "
            "1998 wurde der Zahlungsverkehrs- und Finanzdienstleistungsbereich der Schweizerischen Post unter der "
            "Marke PostFinance gebündelt und am 26. Juni 2013 als eigenständige Aktiengesellschaft (PostFinance AG) "
            "mit FINMA-Bankbewilligung aus der Post ausgegliedert."
        ),
        "mermaid": """flowchart TD
    PTT1906["Postcheck- und Girodienst (PTT, gegr. 1906)"] --> PTT90["Postfinance-Dienst der Schweizerischen Post (1990er)"]
    PTT90 -->|"1998: Verselbstständigung Post / Marke PostFinance"| PF98["PostFinance (Bereich Die Schweizerische Post, 1998)"]
    PF98 -->|"2013: Ausgliederung & FINMA-Banklizenz"| PF13["PostFinance AG (Tochter Die Schweizerische Post AG, 2013)"]
    PF13 --> PF["PostFinance AG (heute, systemrelevant)"]""",
        "milestones": [
            ["1906", "Einführung des Postcheck- und Girodienstes (PTT)", "Gründung", "Aufbau des schweizweiten bargeldlosen Zahlungsverkehrs"],
            ["1998", "Aufspaltung PTT → Die Schweizerische Post & Swisscom", "Reorganisation", "Etablierung der Marke PostFinance innerhalb der Schweizerischen Post"],
            ["2013", "Ausgliederung als PostFinance AG", "Spin-off & Lizenz", "Erteilung der FINMA-Bankbewilligung (26.06.2013); 100 % im Eigentum der Post"],
            ["2015–2026", "Einstufung als inlandrelevante systemrelevante Bank (D-SIB)", "Regulierung", "Kreditvergabeverbot bleibt bestehen; Ausbau von Anlage-, Vorsorge- und Digitalangeboten"],
        ],
        "sources": "PostFinance Geschäftsberichte; Bundesamt für Kommunikation / Post-Chronik",
    },
    "ubs": {
        "founded": "1862/1872 → 1998 (SBG + SBV = UBS AG) → 2023 (+ Credit Suisse)",
        "lineage_summary": (
            "Die heutige UBS Group AG vereint die gesamte moderne Schweizer Grossbankengeschichte seit 1900: "
            "1912 entstand die Schweizerische Bankgesellschaft (SBG) aus der Bank in Winterthur (1862) und der "
            "Toggenburger Bank (1863); 1897 hatte sich der Schweizerische Bankverein (SBV, aus Basler Bankverein 1872) "
            "formiert. 1998 fusionierten SBG und SBV zur modernen UBS AG. 2023 folgte die historische Übernahme der "
            "Credit Suisse Group AG (1856 als Schweizerische Kreditanstalt gegründet, inklusive Bank Leu 1990, "
            "Schweizerische Volksbank 1993 und Neue Aargauer Bank 1994)."
        ),
        "mermaid": """flowchart TD
    BIW["Bank in Winterthur (1862, Stand 1900)"] -->|"1912: Fusion"| SBG["Schweizerische Bankgesellschaft (SBG, 1912)"]
    TOG["Toggenburger Bank (1863, Stand 1900)"] -->|"1912: Fusion"| SBG
    EID["Eidgenössische Bank (1863)"] -->|"1945: Übernahme"| SBG
    ARKB["Appenzell-Ausserrhodische KB"] -->|"1996: Übernahme"| SBG
    BBV["Schweizerischer Bankverein (SBV, 1872/1897, Stand 1900)"] -->|"1995: Übernahme S.G. Warburg"| SBV95["SBV + Warburg / O'Connor / Brinson"]
    SBG -->|"1998: Fusion SBG + SBV"| UBS98["UBS AG (1998)"]
    SBV95 -->|"1998: Fusion SBG + SBV"| UBS98
    PW["PaineWebber (USA)"] -->|"2000: Übernahme"| UBS98
    UBS98 -->|"2014: Holding-Struktur"| UBS14["UBS Group AG (2014)"]
    SKA["Schweizerische Kreditanstalt / Credit Suisse (1856, Stand 1900)"] --> CS93["CS + Bank Leu (1990) + Volksbank (1993) + NAB (1994)"]
    CS93 --> CS00["Credit Suisse Group (inkl. First Boston / DLJ)"]
    UBS14 -->|"2023: Übernahme & Fusion"| UBS23["UBS Group AG (heute)"]
    CS00 -->|"2023: Übernahme & Fusion"| UBS23""",
        "milestones": [
            ["1900", "Basler/Schweizerischer Bankverein (1897), Bank in Winterthur (1862), Toggenburger Bank (1863), SKA (1856)", "Ausgangslage 1900", "Vorgängerinstitute der drei späteren Schweizer Grossbanken"],
            ["1912 / 1945", "Gründung Schweizerische Bankgesellschaft (SBG) & Übernahme Eidg. Bank", "Fusion & Übernahme", "Bank in Winterthur + Toggenburger Bank fusionieren 1912 zur SBG"],
            ["1990–1996", "Konsolidierung (Bank Leu 1990, Volksbank 1993, Warburg 1995, ARKB 1996)", "Akquisitionen", "Inland- und Investmentbank-Konsolidierung bei CS, SBV und SBG"],
            ["1998", "Fusion SBG + SBV → UBS AG", "Megafusion", "Entstehung der modernen UBS (Verkauf Solothurner Bank SoBa 2000 als WEKO-Auflage)"],
            ["2000 / 2014", "Übernahme PaineWebber (2000) & Gründung UBS Group AG (2014)", "Expansion & Holding", "Ausbau US Wealth Management; TBTF-Holdingstruktur"],
            ["2023–2026", "Übernahme & Fusion der Credit Suisse Group AG", "Historische Fusion", "Abschluss Übernahme 12.06.2023; rechtliche und IT-Integration bis Ende 2026"],
        ],
        "sources": "UBS Annual Reports; UBS & Credit Suisse Historische Archive",
    },
    "eks": {
        "founded": "1819 (Ersparniskasse Speicher)",
        "lineage_summary": (
            "Die Ersparniskasse Speicher (EKS) wurde 1819 im Kanton Appenzell Ausserrhoden gegründet und ist seit "
            "1900 als unabhängige Genossenschaftsbank ohne Fusionen oder Übernahmen organisch gewachsen. "
            "Sie gehört zu den ältesten und kleinsten eigenständigen Regionalbanken der Schweiz."
        ),
        "mermaid": """flowchart TD
    EKS1900["Ersparniskasse Speicher (gegr. 1819, Stand 1900)"] -->|"Organische Kontinuität (keine Fusionen)"| EKS["Ersparniskasse Speicher Genossenschaft (heute)"]""",
        "milestones": [
            ["1819 / 1900", "Ersparniskasse Speicher (Genossenschaft)", "Ausgangslage 1900", "Gemeinnützige Dorf- und Regionalsparkasse in Speicher (AR)"],
            ["1900–2026", "Eigenständiges Wachstum ohne Fusionen", "Kontinuität", "Bewusste Unabhängigkeit als Lokalbank mit ~4 FTE und >80 Mio. CHF Bilanzsumme"],
        ],
        "sources": "Ersparniskasse Speicher Geschäftsberichte (2007–2025)",
    },
    "slm": {
        "founded": "1869/1870 (Spar- und Leihkasse Münsingen → 2015 Bank SLM AG)",
        "lineage_summary": (
            "Die Bank SLM AG wurde im November 1869 gegründet und eröffnete am 1. April 1870 als Spar- und "
            "Leihkasse Münsingen ihren ersten Schalter. Seit 1900 entwickelte sich das Institut eigenständig ohne "
            "Grossfusionen im Aaretal (Einnehmereien ab 1915 in Kiesen, Wichtrach, Rubigen und Worb) und firmierte "
            "Anfang 2015 von Spar + Leihkasse Münsingen AG in Bank SLM AG um."
        ),
        "mermaid": """flowchart TD
    SLM1900["Spar- und Leihkasse Münsingen (gegr. 1869/1870, Stand 1900)"] -->|"1915–1925: Filialnetz Aaretal"| SLM_AG["Spar + Leihkasse Münsingen AG"]
    SLM_AG -->|"2015: Umfirmierung"| SLM["Bank SLM AG (heute)"]""",
        "milestones": [
            ["1869–1870 / 1900", "Spar- und Leihkasse Münsingen", "Ausgangslage 1900", "Gegründet von 17 Handwerkern, Gewerbetreibenden und Bauern im Aaretal"],
            ["1915–1925", "Eröffnung der Geschäftsstellen im Aaretal", "Expansion", "Einnehmereien in Kiesen, Wichtrach, Kirchdorf, Rubigen und Worb (1925)"],
            ["2015", "Umfirmierung in Bank SLM AG", "Rebranding", "Moderner Markenauftritt unter Beibehaltung der regionalen Eigenständigkeit"],
        ],
        "sources": "Bank SLM 150-Jahre-Chronik (bankslm.ch); Geschäftsberichte (2012–2025)",
    },
    "aek": {
        "founded": "1826 (Ersparniskasse des Amtes Thun / Amtsersparniskasse Thun → 2006 AEK BANK 1826)",
        "lineage_summary": (
            "Die AEK BANK 1826 wurde 1826 als «Ersparniskasse des Amtes Thun» (EKAT) gegründet und führte ab "
            "Ende des 19. Jahrhunderts den Namen «Amtsersparniskasse Thun». Seit 1900 wuchs die Genossenschaftsbank "
            "ohne Fusionen organisch im Raum Thun/Berner Oberland und heisst seit 2006 offiziell AEK BANK 1826."
        ),
        "mermaid": """flowchart TD
    EKAT1900["Amtsersparniskasse Thun / EKAT (gegr. 1826, Stand 1900)"] -->|"1951: Hauptsitz Lauitor"| AEK1951["Amtsersparniskasse Thun (Genossenschaft)"]
    AEK1951 -->|"2006: Umbenennung"| AEK["AEK BANK 1826 Genossenschaft (heute, 200 Jahre)"]""",
        "milestones": [
            ["1826 / 1900", "Amtsersparniskasse Thun (ehem. Ersparniskasse des Amtes Thun)", "Ausgangslage 1900", "Selbsttragende Genossenschaftsbank (Statuten 1889); 1908 unter Top-10-Banken im Kanton Bern"],
            ["1951", "Neubau Hauptsitz am Thuner Lauitor", "Infrastruktur", "Zentraler Standort für die Expansion im Berner Oberland"],
            ["2006–2026", "Umbenennung in AEK BANK 1826 & 200-Jahr-Jubiläum", "Rebranding", "Organisches Wachstum auf >5,7 Mrd. CHF Bilanzsumme und 14 Niederlassungen"],
        ],
        "sources": "AEK BANK 1826 Chronik (aekbank.ch/200/Geschichte); Geschäftsberichte (2016–2025)",
    },
    "migrosbank": {
        "founded": "1958 (Migros Bank AG, Tochter des Migros-Genossenschafts-Bundes)",
        "lineage_summary": (
            "Die Migros Bank AG wurde Ende 1957 ins Handelsregister eingetragen und nahm 1958 auf Initiative von "
            "Gottlieb Duttweiler (Migros-Genossenschafts-Bund, gegr. 1925) den Betrieb auf. Seit ihrer Gründung wuchs "
            "die Bank rein organisch innerhalb der Migros-Gruppe zu einer der grössten Schweizer Retail- und Hypothekarbanken."
        ),
        "mermaid": """flowchart TD
    MGB["Migros AG (1925) / Migros-Genossenschafts-Bund (1941)"] -->|"1957/1958: Neugründung"| MB58["Migros Bank AG (1958, 10 Mio. CHF Kapital)"]
    MB58 -->|"Organisches Wachstum (>70 Filialen)"| MB["Migros Bank AG (heute, >60 Mrd. CHF Bilanzsumme)"]""",
        "milestones": [
            ["1925 / 1941", "Gründung Migros AG & Umwandlung in MGB", "Mutterkonzern", "Genossenschaftlicher Hintergrund durch Gottlieb Duttweiler"],
            ["1957–1958", "Gründung der Migros Bank AG", "Neugründung", "Eintrag Ende 1957 mit 10 Mio. CHF Aktienkapital; Eröffnung 1958 für günstige Kredite & Sparzinsen"],
            ["1958–2026", "Organischer Filial- und Digitalausbau", "Kontinuität", "Ausbau auf >70 Filialen, Direct-Banking und >62 Mrd. CHF Bilanzsumme ohne Grossfusionen"],
        ],
        "sources": "Migros-Chronik (corporate.migros.ch); Migros Bank Geschäftsberichte (2010–2025)",
    },
    "vontobel": {
        "founded": "1924 (Börsenagentur Haeberli & Cie. → 1936 Bank J. Vontobel & Co.)",
        "lineage_summary": (
            "Vontobel entstand 1924 durch den Einstieg von Jakob Vontobel in die Zürcher Börsenagentur Haeberli & Cie. "
            "(1936 Umfirmierung in Bank J. Vontobel & Co., 1984 Holdinggründung, 1986 Börsengang). "
            "Wichtige Zukäufe seit 2000 waren TwentyFour Asset Management (2015), die Übernahme von Notenstein La Roche "
            "von Raiffeisen (2018) sowie das US-Private-Wealth-Portfolio von UBS Swiss Financial Advisers (2022)."
        ),
        "mermaid": """flowchart TD
    HAEB["Börsenagentur Haeberli & Cie. (1924)"] -->|"1936: Übernahme/Name"| JV["Bank J. Vontobel & Co. (1936)"]
    JV -->|"1984/1986: Holding & Börsengang"| VH["Vontobel Holding AG (1986)"]
    TF["TwentyFour Asset Management (UK)"] -->|"2015: Mehrheitsübernahme"| VH
    NOTE["Notenstein La Roche (ex Wegelin / La Roche)"] -->|"2018: Übernahme von Raiffeisen"| VH
    SFA["UBS Swiss Financial Advisers (US-Kunden CH)"] -->|"2022: Übernahme"| VH
    VH --> VONT["Vontobel Holding AG (heute)"]""",
        "milestones": [
            ["1924 / 1936", "Haeberli & Cie. → Bank J. Vontobel & Co.", "Gründung", "Jakob Vontobel übernimmt Börsenagentur und gründet 1936 das Bankhaus"],
            ["1984 / 1986", "Gründung Vontobel Holding AG & IPO", "Börsengang", "Familienmehrheit bleibt über Pool- und Stiftungsstruktur gesichert"],
            ["2015", "Mehrheitsübernahme TwentyFour Asset Management (London)", "Akquisition", "Ausbau des Fixed-Income- und institutionellen Asset Managements"],
            ["2018", "Übernahme Notenstein La Roche Privatbank AG (von Raiffeisen)", "Akquisition", "Stärkung des Schweizer Wealth Management um ~16 Mrd. CHF AuM"],
            ["2022", "Übernahme UBS Swiss Financial Advisers AG (SFA)", "Akquisition", "Ausbau des Geschäfts mit US-domizilierten Wealth-Management-Kunden in der Schweiz"],
        ],
        "sources": "Vontobel 100-Jahr-Chronik 1924–2024 (vontobel.com); Geschäftsberichte",
    },
    "pictet": {
        "founded": "1805 (De Candolle, Mallet & Cie → 1841 Pictet & Cie → 2014 Banque Pictet & Cie SA)",
        "lineage_summary": (
            "Die Pictet-Gruppe geht auf die 1805 in Genf gegründete Bank De Candolle, Mallet & Cie zurück "
            "(seit 1841 unter dem Namen Pictet & Cie). Seit 1900 wuchs die Privatbank nahezu vollständig organisch "
            "durch ihre Teilhaberstruktur; 2014 erfolgte die historische Umwandlung von einer unbeschränkt haftenden "
            "Personengesellschaft in eine Kapitalgesellschaft-Gruppe (Pictet & Cie Group SCA / Banque Pictet & Cie SA)."
        ),
        "mermaid": """flowchart TD
    PIC1900["Pictet & Cie (gegr. 1805 / Name 1841, Stand 1900)"] -->|"Organische Expansion Asset & Wealth Management"| PIC1990["Pictet & Cie (Personengesellschaft, 1990er–2013)"]
    PIC1990 -->|"2014: Rechtsformwandel"| PIC14["Pictet & Cie Group SCA / Banque Pictet & Cie SA (2014)"]
    PIC14 --> PIC["Pictet-Gruppe (heute, >700 Mrd. CHF AuM)"]""",
        "milestones": [
            ["1805 / 1841 / 1900", "De Candolle, Mallet & Cie → Pictet & Cie", "Ausgangslage 1900", "Genfer Privatbankier-Partnerschaft mit internationaler Vermögensverwaltung"],
            ["1974–2013", "Aufbau Asset Management & Institutional Custody", "Organisches Wachstum", "Globale Expansion nach London, Luxemburg, Tokio, Hongkong und Singapur ohne Grossfusionen"],
            ["2014", "Umwandlung in Pictet & Cie Group SCA & Banque Pictet & Cie SA", "Rechtsformwechsel", "Übergang von der Kommanditgesellschaft zur modernen Konzernstruktur mit Kommanditaktiengesellschaft"],
        ],
        "sources": "Pictet Annual Review (2018–2025); Pictet Group Corporate History",
    },
    "entris": {
        "founded": "1971 (Verband) → 1994 (RBA-Holding AG) → Entris Holding AG / Entris Banking AG",
        "lineage_summary": (
            "Die Entris Holding AG entstand am 1. September 1994 als RBA-Holding AG durch den Zusammenschluss "
            "von 94/98 unabhängigen Schweizer Regionalbanken und Sparkassen (infolge der Immobilienkrise der 1990er-Jahre, "
            "auf Basis des 1971 gegründeten Verbandes Schweizer Regionalbanken). 2003 bildete sich innerhalb der Gruppe "
            "die Clientis-Gruppe, 2007 folgte Entris Operations (2013 an Swisscom verkauft), und 2018 wurde die "
            "Interessenvertretung an den neu gegründeten Verband Schweizer Regionalbanken (VSRB) ausgelagert."
        ),
        "mermaid": """flowchart TD
    VRB1971["Verband Schweizer Regionalbanken (1971)"] -->|"1994: Gründung durch 94/98 Regionalbanken"| RBA94["RBA-Holding AG & RBA-Zentralbank (1994)"]
    RBA94 -->|"2003: Teilgruppe"| CLI03["Clientis-Gruppe (2003, 14 Regionalbanken)"]
    RBA94 -->|"2007: Joint Venture mit BEKB (50/50)"| EOP07["Entris Operations AG (2007)"]
    EOP07 -->|"2013: Verkauf"| SWC13["Swisscom IT Services"]
    RBA94 -->|"Umfirmierung"| ENTH["Entris Holding AG & Entris Banking AG (35 Aktionärsbanken)"]
    ENTH -->|"2018: Auslagerung Verbandsfunktion"| VSRB["Verband Schweizer Regionalbanken VSRB (2018)"]
    ENTH --> ENTRIS["Entris Holding AG (heute, B2B-Zentralbank)"]""",
        "milestones": [
            ["1971", "Gründung Verband Schweizer Regionalbanken", "Dachverband", "Gesamtschweizerische Organisation der regionalen Verbände"],
            ["1994 / 1996", "Gründung RBA-Holding AG durch 94/98 Regionalbanken", "Gründung & Übertragung", "Schaffung eines Sicherheits-, Liquiditäts- und Dienstleistungsnetzes; 1996 Übertragung Verbandsfunktion"],
            ["2003", "Gründung Clientis-Gruppe innerhalb der RBA-Gruppe", "Allianz", "14 selbstständige Regionalbanken bündeln Refinanzierung & Markenauftritt"],
            ["2007 / 2013", "Entris Operations AG (50 % BEKB) → Verkauf an Swisscom", "Joint Venture & Verkauf", "Bündelung und spätere Auslagerung des Kernbanken-IT-Betriebs an Swisscom"],
            ["2015–2018", "Entris Holding AG / Entris Banking AG & Gründung VSRB (2018)", "Reorganisation", "Öffnung für Drittbanken (2017) & Auslagerung Lobbying an VSRB (2018)"],
        ],
        "sources": "Entris Holding Geschäftsberichte (2021–2025); VSRB Chronik",
    },
    "valiant": {
        "founded": "1997 (Fusion Spar + Leihkasse in Bern, Gewerbekasse in Bern & BB Bank Belp; >40 Vorgängerbanken)",
        "lineage_summary": (
            "Valiant entstand Mitte 1997 durch den Zusammenschluss der drei bernischen Regionalbanken Spar + Leihkasse in Bern, "
            "Gewerbekasse in Bern und BB Bank Belp unter dem Dach der Valiant Holding AG. Insgesamt gingen über 40 Regionalbanken "
            "(mit Wurzeln bis ins frühe 19. Jh.) in Valiant auf – u. a. Sensebank, Luzerner Regiobank und IRB Interregio Bank (2002), "
            "Obersimmentalische Volksbank, Bank Jura Laufen, Spar + Leihkasse Steffisburg und Caisse d'épargne de Siviriez (2008–2011) "
            "sowie die Triba Partner Bank AG (2017–2018)."
        ),
        "mermaid": """flowchart TD
    SLB["Spar + Leihkasse in Bern (Stand 1900)"] --> VAL97["1997: Gründung Valiant Holding AG"]
    GEW["Gewerbekasse in Bern (gegr. 1905)"] --> VAL97
    BBB["BB Bank Belp (Stand 1900)"] --> VAL97
    VAL97 -->|"2002: Fusionen"| FUS02["+ KGS Sensebank, Luzerner Regiobank & IRB Interregio Bank"]
    FUS02 -->|"2008–2011: Fusionen"| FUS11["+ Obersimmental, Jura Laufen, Steffisburg, Siviriez & Investas"]
    FUS11 -->|"Ende 2011: Ein-Bank-Strategie"| VAG["Valiant Bank AG (Konsolidierung 4 Tochterbanken + Finnova)"]
    TRIBA["Triba Partner Bank AG (Luzern)"] -->|"2017–2018: Übernahme & Integration"| VAG
    VAG -->|"2020–2026: Expansion 15 Kantone"| VAL["Valiant Holding AG / Valiant Bank AG (heute)"]""",
        "milestones": [
            ["1900–1996", "Über 40 selbstständige Regional- & Ersparniskassen", "Ausgangslage", "Wurzeln in Bern, Luzern, Freiburg, Jura und der Westschweiz bis ins 19. Jh."],
            ["1997", "Gründung Valiant Holding AG", "Dreierfusion", "Zusammenschluss von Spar + Leihkasse in Bern, Gewerbekasse in Bern und BB Bank Belp"],
            ["2002", "Übernahme/Fusion KGS Sensebank, Luzerner Regiobank & IRB Interregio Bank", "Expansion", "Vorstoss in die Zentralschweiz und das Mittelland"],
            ["2008–2011", "Fusionen Obersimmentalische Volksbank, Bank Jura Laufen, SL Steffisburg, Siviriez", "Konsolidierung", "Ende 2011 Zusammenführung von 4 Tochterbanken unter dem Dach der Valiant Bank AG"],
            ["2017–2018", "Übernahme & Integration der Triba Partner Bank AG (Luzern)", "Akquisition", "Aufstockung auf 97,4 % (2017) und vollständige Fusion in die Valiant Bank AG (2018)"],
        ],
        "sources": "Valiant Geschäftsberichte (2016–2025); Valiant Chronik",
    },
}
