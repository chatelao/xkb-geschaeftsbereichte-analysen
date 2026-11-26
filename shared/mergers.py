"""Deterministische Fusions-, Übernahme- und Institutsgeschichtsdaten seit 1900 für alle 19 Banken."""

from __future__ import annotations

from typing import Any

MERGER_HISTORY: dict[str, dict[str, Any]] = {
    "bekb": {
        "founded": "1834 (Kantonalbank von Bern) / 1846 (Hypothekarkasse des Kantons Bern)",
        "lineage_summary": (
            "Die heutige Berner Kantonalbank AG (BEKB | BCBE) entstand 1991 aus dem Zusammenschluss der "
            "1834 gegründeten Kantonalbank von Bern (KBB) und der 1846 gegründeten Hypothekarkasse des Kantons Bern (HKB). "
            "Historisch prägend waren zwei bedeutende Abspaltungen: 1979 wurden vier jurassische Filialen zur Gründung der "
            "Banque Cantonale du Jura (BCJ) abgetrennt, und 1993 wurden infolge der Immobilienkrise notleidende Kredite im Umfang "
            "von CHF 6.5 Mrd. in die kantonale Auffanggesellschaft (Bad Bank) Dezennium-Finanz AG (DFAG) ausgegliedert. "
            "1998 wurde die BEKB als erste Kantonalbank der Schweiz in eine privatrechtliche Aktiengesellschaft nach OR umgewandelt."
        ),
        "mermaid": """flowchart TD
    KBB["Kantonalbank von Bern (gegr. 1834, Stand 1900)"] -->|"1979: Territoriale Abspaltung 4 Filialen"| BCJ["Banque Cantonale du Jura (BCJ, 1979)"]
    KBB -->|"Kerninstitut"| KBB79["Kantonalbank von Bern (nach 1979)"]
    HKB["Hypothekarkasse des Kantons Bern (gegr. 1846, Stand 1900)"] --> MERGE1991["1991: Fusion KBB + HKB zur Berner Kantonalbank"]
    KBB79 --> MERGE1991
    MERGE1991 -->|"1993: Ausgliederung Bad Bank"| DFAG["Dezennium-Finanz AG (DFAG, 1993)<br>CHF 6.5 Mrd. Problemkredite; liq. 2002/03"]
    MERGE1991 -->|"Bereinigtes Stammhaus"| BEKB93["Berner Kantonalbank (gesundes Stammhaus)"]
    BEKB93 --> AG1998["1998: Umwandlung in privatrechtliche AG (OR)"]
    AG1998 --> SG2006["2006–2012: Schrittweiser Wegfall der Staatsgarantie"]
    SG2006 --> BEKB["Berner Kantonalbank AG (BEKB | BCBE, heute)"]
    BEKB -.->|"2021: IT-Carve-out / 2026: Reintegration"| AITY["aity AG (IT-Dienstleister)"]""",
        "milestones": [
            ["1834 / 1900", "Kantonalbank von Bern (KBB) & Hypothekarkasse des Kantons Bern (HKB)", "Ausgangslage 1900", "Zwei eigenständige bernische Staatsinstitute (Universal- vs. Hypothekarbank)"],
            ["1979", "Gründung Kanton Jura / Banque Cantonale du Jura (BCJ)", "Territoriale Abspaltung", "Übertragung von vier jurassischen Niederlassungen der KBB (Delsberg, Pruntrut, Freiberge) an die neu gegründete BCJ"],
            ["1991", "Fusion KBB + HKB → Berner Kantonalbank", "Fusion", "Grosser Rat beschliesst mit 136:0 Stimmen den Zusammenschluss beider bernischer Staatsbanken"],
            ["1993", "Ausgliederung Bad Bank Dezennium-Finanz AG (DFAG)", "Bad Bank Carve-Out", "Übertragung von CHF 6.5 Mrd. notleidenden Krediten/Immobilien an DFAG; Kanton fängt CHF 1.5 Mrd. Verlust auf, liquidiert 2002/03"],
            ["1998", "Umwandlung in BEKB AG", "Rechtsformwechsel", "Erste Kantonalbank der Schweiz als privatrechtliche AG (Art. 620 OR); Kanton reduziert Anteil auf 51,5 %"],
            ["2006–2012", "Aufhebung der Staatsgarantie", "Regulierung", "Schrittweiser Übergang zu voller Eigenmittel- und Marktdisziplin ohne kantonale Haftung"],
            ["2021–2026", "IT-Carve-Out aity AG & Reintegration", "IT-Spin-off", "2021 Ausgliederung der IT in aity AG; 11/2026 Beschluss zur vollständigen Reintegration in die BEKB bis 2028"],
        ],
        "sources": "BEKB Firmengeschichte (bekb.ch); Kanton Bern Beteiligungsberichte & DFAG-Schlussbericht",
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
            "der 1869 gegründeten Banque Hypothécaire du Canton de Genève (BHCG). Im Jahr 2000 erfolgte nach massiven "
            "Immobilienverlusten die Ausgliederung einer staatlichen Bad Bank ('Fondation de valorisation des actifs de la BCGe', "
            ">CHF 5 Mrd. Problemaktiven mit kantonaler Garantie; liquidiert 2008). Später folgten gezielte Boutique-Akquisitionen "
            "wie Dimension SA (2015) und Loyal Finance AG (2019)."
        ),
        "mermaid": """flowchart TD
    CEG["Caisse d'Épargne de Genève (CEG, gegr. 1816, Stand 1900)"] --> FUS1994["1994: Fusion CEG + BHCG → Banque Cantonale de Genève (BCGE)"]
    BHCG["Banque Hypothécaire du Canton de Genève (BHCG, gegr. 1869, Stand 1900)"] --> FUS1994
    FUS1994 -->|"2000: Ausgliederung Bad Bank"| FOND["Fondation de valorisation des actifs de la BCGe<br>(>CHF 5 Mrd. Problemkredite; liq. 2008)"]
    FUS1994 -->|"Sanierte Kernbank"| RESTR2000["2000: Sanierung & Rekapitalisierung durch Kanton Genf"]
    RESTR2000 --> DIM2015["2015: Übernahme Dimension SA (M&A)"]
    RESTR2000 --> LF2019["2019: Übernahme Loyal Finance AG (Zürich)"]
    DIM2015 --> BCGE["Banque Cantonale de Genève (BCGE, heute)"]
    LF2019 --> BCGE""",
        "milestones": [
            ["1816 / 1900", "Caisse d'Épargne (CEG) & Banque Hypothécaire (BHCG)", "Ausgangslage 1900", "Zwei eigenständige Genfer Kantonal-/Sparkasseninstitute seit dem 19. Jh."],
            ["1994", "Fusion CEG + BHCG → Banque Cantonale de Genève (BCGE)", "Fusion", "Gründung der BCGE als öffentlich-rechtliche Aktiengesellschaft"],
            ["2000", "Bad Bank 'Fondation de valorisation' & Rekapitalisierung", "Bad Bank Carve-Out", "Ausgliederung von >5 Mrd. CHF notleidenden Aktiven in kantonale Stiftung (liq. 2008); Beginn Ära Blaise Goetschin"],
            ["2015 / 2019", "Übernahmen Dimension SA (Lausanne) & Loyal Finance AG (Zürich)", "Akquisitionen", "Ausbau von M&A-Beratung und institutionellem Obligationen-Asset-Management"],
        ],
        "sources": "BCGE Geschäftsberichte; Cour des comptes Genève; Historisches Lexikon der Schweiz",
    },
    "raiffeisen": {
        "founded": "1899/1902 (Darlehenskasse Bichwil & Schweizerischer Raiffeisenverband)",
        "lineage_summary": (
            "Die Raiffeisen-Gruppe entstand 1899/1902 mit der ersten Darlehenskasse in Bichwil (SG) und dem "
            "Schweizerischen Raiffeisenverband (1902). Über das 20. Jahrhundert wuchs das Netz auf über 1'000 lokale "
            "Genossenschaften an, die durch laufende Regionalfusionen auf rund 218 Raiffeisenbanken konsolidiert wurden. "
            "2012 übernahm Raiffeisen Teile der Privatbank Wegelin & Co. (Notenstein, später Notenstein La Roche) und "
            "veräusserte 2016 Vescore sowie 2018 Notenstein La Roche an Vontobel für CHF 700 Mio."
        ),
        "mermaid": """flowchart TD
    BICH["Darlehenskasse Bichwil (1899) & Verband (1902)"] --> NETZ["Ausbau auf >1'000 lokale Darlehenskassen (20. Jh.)"]
    NETZ -->|"Laufende Regionalfusionen"| GEN["Konsolidierung auf ~218 Raiffeisenbanken (heute)"]
    WEG["Privatbank Wegelin & Co. (gegr. 1741)"] -->|"2012: Übernahme Nicht-US-Geschäft"| NOTE["Notenstein Privatbank (2012) / Notenstein La Roche (2015)"]
    LARO["Bank La Roche & Co. (gegr. 1787)"] -->|"2015: Integration"| NOTE
    GEN -->|"2012–2018: Beteiligung/Tochter"| NOTE
    NOTE -->|"2018: Verkauf für CHF 700 Mio."| VONT["Bank Vontobel AG"]
    GEN -.->|"2016: Verkauf Asset Management"| VESC["Vescore AG (an Vontobel)"]
    GEN --> RAIF["Raiffeisen Gruppe Schweiz (heute)"]""",
        "milestones": [
            ["1899 / 1902", "Darlehenskasse Bichwil & Schweizerischer Raiffeisenverband", "Gründung", "Start der schweizerischen Genossenschaftsbanken nach Friedrich Wilhelm Raiffeisen"],
            ["1902–2025", "Gründungswelle & spätere Regionalfusionen", "Konsolidierung", "Von über 1'200 lokalen Darlehenskassen zu rund 218 schlagkräftigen Raiffeisenbanken"],
            ["2012", "Übernahme Nicht-US-Geschäft von Wegelin & Co. (Notenstein)", "Akquisition", "Einstieg ins Private Banking über Tochtergesellschaft Notenstein Privatbank AG"],
            ["2015", "Übernahme Bank La Roche & Co. durch Notenstein", "Akquisition", "Fusion zu Notenstein La Roche Privatbank AG"],
            ["2016 / 2018", "Verkäufe Vescore & Notenstein La Roche an Vontobel", "Devestition / Spin-off", "Verkauf des Asset Managers Vescore (2016) und von Notenstein La Roche (2018, CHF 700 Mio.) zur Fokussierung auf Retail"],
        ],
        "sources": "Raiffeisen Schweiz Geschäftsberichte; Vontobel Chronik",
    },
    "postfinance": {
        "founded": "1906 (Postcheck- und Girodienst) / 2013 (PostFinance AG)",
        "lineage_summary": (
            "PostFinance geht auf den 1906 eingeführten schweizerischen Postcheck- und Girodienst zurück. "
            "1998 wurde der Zahlungsverkehrs- und Finanzdienstleistungsbereich im Rahmen der PTT-Aufspaltung unter der "
            "Marke PostFinance gebündelt und am 26. Juni 2013 als eigenständige Aktiengesellschaft (PostFinance AG) "
            "mit FINMA-Bankbewilligung aus der Post ausgegliedert. 2025 erfolgte der Ausstieg aus dem Neobank-Joint-Venture Yuh (Verkauf 50 % an Swissquote)."
        ),
        "mermaid": """flowchart TD
    PTT1906["Postcheck- und Girodienst (PTT, gegr. 1906)"] --> PTT90["Postfinance-Dienst der Schweizerischen Post (1990er)"]
    PTT90 -->|"1998: Verselbstständigung Post / Marke PostFinance"| PF98["PostFinance (Bereich Die Schweizerische Post, 1998)"]
    PF98 -->|"2013: Ausgliederung & FINMA-Banklizenz"| PF13["PostFinance AG (Tochter Die Schweizerische Post AG, 2013)"]
    PF13 -.->|"2025: Verkauf 50%-Beteiligung"| YUH["Yuh SA (an Swissquote)"]
    PF13 --> PF["PostFinance AG (heute, systemrelevant)"]""",
        "milestones": [
            ["1906", "Einführung des Postcheck- und Girodienstes (PTT)", "Gründung", "Aufbau des schweizweiten bargeldlosen Zahlungsverkehrs"],
            ["1998", "Aufspaltung PTT → Die Schweizerische Post & Swisscom", "Reorganisation & Carve-Out", "Etablierung der Marke PostFinance innerhalb der Schweizerischen Post"],
            ["2013", "Ausgliederung als PostFinance AG", "Spin-off & Lizenz", "Erteilung der FINMA-Bankbewilligung (26.06.2013); 100 % im Eigentum der Post"],
            ["2015–2024", "Einstufung als inlandrelevante systemrelevante Bank (D-SIB)", "Regulierung", "Kreditvergabeverbot bleibt bestehen; Ausbau von Anlage-, Vorsorge- und Digitalangeboten"],
            ["2025", "Verkauf Yuh-Beteiligung & Swissquote-Aktienabbau", "Devestition", "Verkauf des 50%-Anteils an Neobank Yuh SA an Swissquote sowie Reduktion der Swissquote-Beteiligung"],
        ],
        "sources": "PostFinance Geschäftsberichte; Bundesamt für Kommunikation / Post-Chronik",
    },
    "ubs": {
        "founded": "1856 (SKA) / 1862 (Bank in Winterthur) / 1872 (Basler Bankverein) → 1998 (UBS) → 2023 (+ CS)",
        "lineage_summary": (
            "Die heutige UBS Group AG vereint die gesamte moderne Schweizer Grossbankengeschichte in drei historischen Hauptsträngen: "
            "(1) Die SBG-Linie, entstanden 1912 aus der Fusion der Bank in Winterthur (1862) und der Toggenburger Bank (1863), "
            "erweitert u. a. um die Eidgenössische Bank (1945), Interhandel (1967) und die kriselnde Appenzell-Ausserrhodische Kantonalbank (1996). "
            "(2) Die SBV-Linie (Schweizerischer Bankverein), gegründet 1872/1897 aus Basler und Zürcher Vorgängern, gewachsen durch die "
            "Basler Handelsbank (1945) sowie internationale Investmentbanken wie O'Connor (1992), Brinson (1994), S.G. Warburg (1995) und Dillon Read (1997). "
            "(3) Die Credit Suisse-Linie (1856 als Schweizerische Kreditanstalt SKA gegründet), die 1990 Bank Leu (gegr. 1755), 1993 die kriselnde "
            "Schweizerische Volksbank (SVB), 1994 die Neue Aargauer Bank (NAB, Wurzeln bis 1812), 1988/90 First Boston und 2000 DLJ integrierte. "
            "1998 fusionierten SBG und SBV zur UBS AG (unter WEKO-Auflage des Verkaufs der Solothurner Bank SoBa im Jahr 2000). "
            "2008 wurde die Bad Bank 'SNB StabFund' (USD 38.7 Mrd.) ausgegliedert. Am 19. März 2023 übernahm UBS in einer staatlich orchestrierten "
            "Rettung die Credit Suisse Group AG, gliederte deren toxische Investmentbank-Aktiven in die Bad-Bank-Einheit 'Non-Core and Legacy' (NCL) aus "
            "und fusionierte 2024 die operativen Stammhäuser und Schweizer Banktöchter."
        ),
        "mermaid": """flowchart TD
    subgraph SBG_Linie["1. SBG-Linie (Schweizerische Bankgesellschaft)"]
        BIW["Bank in Winterthur (gegr. 1862)"] -->|"1912: Fusion"| SBG["SBG (1912)"]
        TOG["Toggenburger Bank (gegr. 1863)"] -->|"1912: Fusion"| SBG
        EID["Eidgenössische Bank (1863)"] -->|"1945: Übernahme"| SBG
        INH["Interhandel (1967)"] -->|"1967: Fusion"| SBG
        ARKB["Appenzell-Ausserrh. KB"] -->|"1996: Notübernahme"| SBG
        SMH["Schroeder Münchmeyer Hengst"] -->|"1997: Kauf"| SBG
    end

    subgraph SBV_Linie["2. SBV-Linie (Schweizerischer Bankverein)"]
        BBV["Basler Bankverein (gegr. 1854/1872)"] -->|"1897: Konsolidierung"| SBV["SBV (1897)"]
        ZBV["Zürcher Bankverein + Basler Depositenbank"] -->|"1897"| SBV
        BHB["Basler Handelsbank (1862)"] -->|"1945: Übernahme"| SBV
        OCO["O'Connor & Associates (Chicago)"] -->|"1992: Derivate"| SBV
        BRI["Brinson Partners (Chicago)"] -->|"1994: Asset Mgmt"| SBV
        WAR["S.G. Warburg & Co. (London)"] -->|"1995: Investment Banking"| SBV
        DIL["Dillon, Read & Co. (Wall Street)"] -->|"1997: M&A"| SBV
    end

    subgraph CS_Linie["3. Credit Suisse-Linie (SKA / SVB / Leu / NAB — Rekursiver Baum)"]
        %% SKA Stammhaus & historische Übernahmen
        SKA1856["Schweizerische Kreditanstalt (SKA, gegr. 1856)<br>+ Allg. Deutsche Creditanstalt Leipzig (50 % Startkapital)"]
        BIZ1836["Bank in Zürich ('Meisenbank', gegr. 1836, älteste Aktienbank CH)<br>+ Oberrheinische Bank Basel + St. Galler Handelsbank + Bank in St. Gallen"] -->|"1905–1907: Fusion / Übernahmen"| SKA_EXP1["SKA Nationale Expansion (1905–1937)"]
        SKA1856 --> SKA_EXP1
        REG1911["1911: SLK Aussersihl-Wiedikon | 1912: Bank in Luzern, Bank in Glarus, Bank in Horgen<br>1916: Bank in Baden | 1920: Thurg. Handelsbank | 1921: Soc. Suisse Lausanne<br>1925: Centralschweiz. Hypothekenbank | 1930: Rhätische Bank Davos | 1937: Bank in Zug"] -->|"1911–1937: Übernahmen"| SKA_EXP1
        SBKA1896["Schweiz. Bodenkredit-Anstalt (SBKA, ex Hypothekarbank Zürich, 1896)<br>+ 1961: Banque Pop. Martigny + 1968: Obwaldner Gewerbebank + 1978: Bank Wädenswil"] -->|"1961–1978: Übernahmen"| SKA_KERN["SKA Stammhaus (Retail & Corporate)"]
        EKO["1986: Discont-Credit Zürich | 1992: EKO Hypothekar- & Handelsbank Olten<br>1993: Krefina-Bank St. Gallen & Swiss-Kuwaiti Bank Genf"] -->|"1986–1993: Übernahmen"| SKA_KERN
        SKA_EXP1 --> SKA_KERN
        SKA_KERN -->|"1982/1989: Holdingstruktur"| CSH1982["CS Holding (1982)"]

        %% Schweizerische Volksbank (SVB) & ihre eigenen Fusionen
        VB1869["Volksbank in Bern (gegr. 1869)"] -->|"1880/81: Statuten & Fusion lokale Volksbanken"| SVB1881["Schweizerische Volksbank (SVB / BPS)"]
        SVB_ACQ1["1889: Banque pop. de Tramelan | 1912: Caisse d'épargne de Moutier<br>1918: St. Moritzer Bank (ex R. Bavier) | 1924: Leihkasse Meilen-Herrliberg<br>+ Bank Gebr. Oechslin Schaffhausen + BICC Genf"] -->|"1889–1930: Übernahmen"| SVB1881
        SVB1881 -->|"1933/37: Bundessanierung (CHF 100 Mio.) / 1993: Notübernahme (CHF 1.1 Mrd.)"| CSH1982

        %% Clariden Leu & Privatbanken-Zweig
        LEU1755["Bank Leu AG (gegr. 1755, älteste Bank CH)"] -->|"1990: Übernahme durch CS Holding"| LEU_CS["Bank Leu"]
        LEU_SUB["1993: Bank Jenni & Cie. + Bank Heusser & Cie. (Basel)<br>1994/95: Bank Neumünster Zürich | 1997: Affida Bank Zürich"] -->|"1993–1997: Fusionen in Leu"| LEU_CS
        HOF1897["Bank Hofmann AG (1897, Kauf 1973) + Clariden Bank (ex White Weld 1962)<br>+ Finter Bank (1994) + BGP Lugano (1998) + CS Fides (ex KPMG Fides 1928)"] -->|"01.01.2007: 5er-Fusion"| CL2007["Clariden Leu AG (2007)"]
        LEU_CS -->|"2007: Fusion"| CL2007

        %% Neue Aargauer Bank (NAB) & Vorgänger
        AAEK1812["Allg. Aargauische Ersparniskasse (AAEK, 1812)<br>+ Ersparniskasse Laufenburg + SLK Zurzach"] -->|"1989: Fusion"| NAB1989["Neue Aargauer Bank (NAB, 1989)"]
        AHB1849["Aarg. Hypotheken- & Handelsbank (AHB, 1849)<br>+ Gewerbebank Baden"] -->|"1989: Fusion"| NAB1989
        FREI1883["1996: Aargauer SVB- & SKA-Filialen<br>1997: Freiämter Bank Wohlen (gegr. 1883)"] -->|"1996–1997: Integration"| NAB_CS["NAB (CS-Tochter ab 1994)"]
        NAB1989 -->|"1994/95: Mehrheitskauf CS"| NAB_CS

        %% Wall Street: First Boston, BZW, Garantia & DLJ
        FB1932["First Boston Corp. (1932/34) + White, Weld & Co. Eurobonds (1978)"] -->|"1978: JV / 1988–90: Übernahme"| CSFB["CS First Boston (CSFB)"]
        BZW["1997: BZW Equities/M&A | 1998: Banco Garantia (Brasilien)<br>2000: Donaldson, Lufkin & Jenrette (DLJ, USD 11.5 Mrd.)"] -->|"1997–2000: Zukäufe"| CSFB

        %% Zusammenführung in Credit Suisse Group
        CSH1982 -->|"1997: Rebranding"| CSG["Credit Suisse Group AG"]
        WIN1875["Winterthur Versicherungen (gegr. 1875)"] -->|"1997: Allfinanz-Kauf (CHF 14 Mrd.)"| CSG
        CSG -.->|"2006: Spin-off & Verkauf (CHF 12.3 Mrd.)"| WIN_AXA["Winterthur an AXA"]
        CSFB -->|"2006: 'One Bank' Integration"| CSG
        CL2007 -->|"2012: Vollintegration"| CSG
        NAB_CS -->|"2020: Vollabsorption in CS (Schweiz) AG"| CSG
    end

    SBG -->|"1998: Megafusion"| UBS98["UBS AG (1998)"]
    SBV -->|"1998: Megafusion"| UBS98
    UBS98 -.->|"2000: WEKO-Auflage Abspaltung"| SOBA["Solothurner Bank SoBa (an Baloise)"]
    PW["PaineWebber (USA)"] -->|"2000: Übernahme USD 10.8 Mrd."| UBS98
    UBS98 -.->|"2008: Bad Bank Carve-out"| STAB["SNB StabFund (USD 38.7 Mrd.; 2013 rückgekauft)"]
    UBS98 -->|"2014: TBTF-Holdingstruktur"| UBS14["UBS Group AG (2014)"]
    UBS14 -->|"19.03.2023: Notübernahme"| UBS23["UBS Group AG (vereinte Grossbank)"]
    CSG -->|"12.06.2023: Vollzug Übernahme"| UBS23
    UBS23 -.->|"2023–2026: Bad-Bank-Abbau"| NCL["Non-Core and Legacy (NCL) & SPG-Verkauf an Apollo"]
    UBS23 -->|"2024: Rechtliche Fusion Stammhäuser & Schweiz-Töchter"| UBS_HEUTE["UBS Group AG (globaler Wealth Manager >$5.5 Bio. AuM)"]""",
        "milestones": [
            ["1854–1872", "Gründungsära Basler Bankverein (1872), Bank in Winterthur (1862), Toggenburger Bank (1863), SKA (1856)", "Ausgangslage", "Pioniere der schweizerischen Industrie- und Eisenbahnfinanzierung"],
            ["1869", "Gründung Schweizerische Volksbank (SVB) in Bern", "Gründung", "Genossenschaftlicher Ursprung als 'Volksbank in Bern'"],
            ["1912", "Gründung Schweizerische Bankgesellschaft (SBG)", "Grossfusion", "Zusammenschluss der Bank in Winterthur und der Toggenburger Bank"],
            ["1945", "Kriegs-Bereinigung: Eidgenössische Bank (an SBG) & Basler Handelsbank (an SBV)", "Übernahmen", "Rettung zweier kriselnder Grossbanken durch SBG und SBV"],
            ["1988–1990", "CS Holding expandiert: First Boston & Bank Leu", "Akquisitionen", "Einstieg an der Wall Street und Übernahme der ältesten Bank der Schweiz (Leu, gegr. 1755)"],
            ["1993–1994", "Inland-Konsolidierung CS: Übernahme SVB & Neue Aargauer Bank (NAB)", "Notübernahme / Zukauf", "Rettung der viertgrössten Schweizer Bank (SVB) vor dem Kollaps; Kauf der führenden Regionalbank im Aargau"],
            ["1995–1997", "SBV formiert Investmentbank: O'Connor, Brinson, S.G. Warburg, Dillon Read", "Expansion", "Aufbau von SBC Warburg Dillon Read als global führendes Investmenthaus"],
            ["1996", "Notübernahme Appenzell-Ausserrhodische Kantonalbank (ARKB) durch SBG", "Notübernahme", "Rettung der nach Immobiliencrash illiquiden ARKB; Kanton übernimmt CHF 60 Mio. Verluste"],
            ["1997 / 2006", "CS kauft Winterthur Group & spaltet sie 2006 an AXA ab", "Allfinanz & Spin-off", "CHF 14 Mrd. Kauf zur Allfinanz; 2006 für CHF 12.3 Mrd. an AXA veräussert"],
            ["1998", "Megafusion SBG + SBV → UBS AG", "Grossfusion", "Zusammenschluss zur damals zweitgrössten Bank der Welt; WEKO verlangt Verkauf der Solothurner Bank SoBa (2000 an Baloise)"],
            ["2000", "Übernahmen PaineWebber (UBS) & Donaldson, Lufkin & Jenrette (DLJ, CS)", "Wall Street M&A", "UBS kauft PaineWebber für USD 10.8 Mrd.; CS kauft DLJ für USD 11.5 Mrd."],
            ["2007–2012", "Clariden Leu: Bündelung & Vollintegration in CS", "Konsolidierung", "Fusion von 5 Privatbanken (Leu, Hofmann, Clariden, BGP, Finter) 2007 zu Clariden Leu; 2012 Vollintegration"],
            ["2008", "Ausgliederung Bad Bank 'SNB StabFund' (UBS)", "Bad Bank Carve-Out", "Übertragung von USD 38.7 Mrd. toxischen Aktiven an Zweckgesellschaft der SNB; 2013 liquidiert/rückgekauft mit USD 3.8 Mrd. SNB-Gewinn"],
            ["2014", "Umstrukturierung in UBS Group AG (Holding) & Stammhaus-Ring-Fencing", "TBTF-Restrukturierung", "Schaffung von UBS Switzerland AG und separaten Ländergesellschaften unter einer Konzernholding"],
            ["2020", "Vollständige Integration der Neuen Aargauer Bank (NAB) in CS", "Markenbereinigung", "Aufgabe der Marke NAB und Schliessung redundanter Filialen im Aargau"],
            ["2023", "Historische Notübernahme der Credit Suisse Group AG durch UBS", "Megafusion & Notrettung", "19.03.2023 staatlich gestützte Vereinbarung; 12.06.2023 Vollzug; Ausgliederung NCL-Bad-Bank"],
            ["2024–2026", "Rechtliche Fusionen & Vollintegration", "Vollzug", "31.05.2024 Fusion UBS AG/CS AG; 01.07.2024 Fusion UBS Schweiz AG/CS Schweiz AG; IT-Migration bis 2026"],
        ],
        "sources": "UBS Annual Reports; Credit Suisse Historisches Archiv; SNB Berichte; FINMA Verfügungen",
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
    "sgkb": {
        "founded": "1868 (St.Gallische Kantonalbank) → 2001 (Umwandlung in Aktiengesellschaft & Börsengang SIX)",
        "lineage_summary": (
            "Die 1868 gegründete St.Galler Kantonalbank wurde 2001 in eine spezialgesetzliche/privatrechtliche "
            "Aktiengesellschaft umgewandelt und an der SIX Swiss Exchange kotiert (Kanton St. Gallen hält 51,0 %). "
            "In den 2000er-Jahren expandierte sie über Hyposwiss (Zürich/Genf) und gründete 2009 die SGKB Deutschland AG. "
            "2013–2014 fokussierte sie sich wieder auf das Kerngebiet (Verkauf Hyposwiss Genf und Übernahme/Integration "
            "der Vadian Bank AG St. Gallen) sowie 2017–2018 Übernahme von Teilen der M.M.Warburg Bank (Schweiz)."
        ),
        "mermaid": """flowchart TD
    SGKB1900["St.Gallische Kantonalbank (gegr. 1868, Stand 1900)"] -->|"2001: Umwandlung AG & IPO SIX"| SGKB01["St.Galler Kantonalbank AG (2001)"]
    SGKB01 -->|"2009: Gründung Tochter"| DE["SGKB Deutschland AG (München)"]
    HYPO["Hyposwiss Zürich / Genf"] -->|"2000er: Expansion / 2013–2014: Verkauf Genf & Integration Zürich"| SGKB01
    VAD["Vadian Bank AG (St. Gallen)"] -->|"2014: Kauf & Integration"| SGKB01
    WAR["M.M.Warburg Bank (Schweiz) PB-Geschäft"] -->|"2017–2018: Übernahme"| SGKB01
    SGKB01 --> SGKB["St.Galler Kantonalbank Gruppe (heute)"]
    DE --> SGKB""",
        "milestones": [
            ["1868 / 1900", "St.Gallische Kantonalbank", "Gründung & Ausgangslage", "Staatsbank des Kantons St. Gallen seit 1868"],
            ["2001", "Umwandlung in AG & Börsengang (SIX: SGKN)", "Rechtsformwechsel", "Teilprivatisierung unter Beibehaltung der kantonalen Mehrheit (51,0 %) und Staatsgarantie"],
            ["2009", "Gründung St.Galler Kantonalbank Deutschland AG", "Auslandstochter", "Aufbau des Private-Banking-Standorts München"],
            ["2013–2014", "Kauf Vadian Bank AG & Verkauf Hyposwiss Genf", "Fokussierung", "Stärkung im Heimmarkt St. Gallen und Rückzug aus nicht-strategischen Auslandsmärkten"],
            ["2017–2018", "Übernahme M.M.Warburg Bank (Schweiz) PB-Geschäft", "Akquisition", "Ausbau des Schweizer Private Bankings zum 150-Jahr-Jubiläum"],
        ],
        "sources": "SGKB Geschäftsberichte (2018–2025); SGKB Chronik",
    },
    "blkb": {
        "founded": "1864 (Basellandschaftliche Kantonalbank, Liestal)",
        "lineage_summary": (
            "Die Basellandschaftliche Kantonalbank wurde 1864 durch Volksabstimmung im Kanton Basel-Landschaft gegründet "
            "und wuchs seither ohne Grossfusionen organisch zur führenden Bank der Nordwestschweiz. "
            "2001 übernahm sie zur Auslandsexpansion die AAM Privatbank (2009 an die Basler Kantonalbank verkauft). "
            "2021–2025 lancierte sie die Digitalbank-Tochter radicant, deren Betrieb 2025 zugunsten der Fokussierung auf das Stammgeschäft eingestellt wurde."
        ),
        "mermaid": """flowchart TD
    BLKB1900["Basellandschaftliche Kantonalbank (gegr. 1864, Stand 1900)"] -->|"Organisches Wachstum Nordwestschweiz"| BLKB00["BLKB (Staatsanstalt mit KB-Zertifikaten)"]
    AAM["AAM Privatbank (Übernahme 2001)"] -->|"2009: Verkauf an BKB"| BLKB00
    BLKB00 -->|"2021–2025: Gründung & Ausstieg 2025"| RAD["radicant bank ag (eingestellt 2025)"]
    BLKB00 --> BLKB["Basellandschaftliche Kantonalbank (heute)"]""",
        "milestones": [
            ["1864 / 1900", "Basellandschaftliche Kantonalbank", "Gründung & Ausgangslage", "Volksbeschluss vom 10. Juli 1864; Staatsbank des Kantons Basel-Landschaft in Liestal"],
            ["2001–2009", "Übernahme & Verkauf AAM Privatbank", "Auslandsexpansion / Rückzug", "2001 Übernahme der AAM zur Auslandsexpansion, 2009 Verkauf an die Basler Kantonalbank"],
            ["2010", "Einführung Avaloq Banking System", "IT-Modernisierung", "Ablösung der Eigenentwicklung durch die Standardplattform Avaloq"],
            ["2021–2025", "Aufbau und Beendigung radicant bank ag", "Strategische Bereinigung", "Nachhaltigkeits-Digitalbank 2025 wertberichtigt (CHF 105,5 Mio.) und geordnet beendet"],
        ],
        "sources": "BLKB Geschäftsberichte (2007–2025); BLKB Chronik",
    },
    "lukb": {
        "founded": "1850 (Luzerner Kantonalbank) → 2001 (Umwandlung in privatrechtliche AG & Börsengang SIX)",
        "lineage_summary": (
            "Die 1850 gegründete Luzerner Kantonalbank wurde 2001 auf Basis des kantonalen Umwandlungsgesetzes in eine "
            "privatrechtliche Aktiengesellschaft umgewandelt und an der SIX Swiss Exchange kotiert (Kanton Luzern hält 61,5 %). "
            "2006 übernahm die Tochter Adler & Co. Privatbank den Basler Standort der swissfirst Bank AG und fusionierte 2010 "
            "mit dem Stammhaus LUKB; 2025 wurde zudem die Tochter Refinum AG ins Stammhaus integriert."
        ),
        "mermaid": """flowchart TD
    LUKB1900["Luzerner Kantonalbank (gegr. 1850, Stand 1900)"] -->|"2001: Umwandlungsgesetz & IPO SIX"| LUKB01["Luzerner Kantonalbank AG (2001)"]
    ADL["Adler & Co. Privatbank AG (inkl. swissfirst Basel 2006)"] -->|"2010: Fusion ins Stammhaus"| LUKB01
    REF["Refinum AG"] -->|"01/2025: Integration ins Stammhaus"| LUKB01
    LUKB01 --> LUKB["Luzerner Kantonalbank Konzern (heute)"]""",
        "milestones": [
            ["1850 / 1900", "Luzerner Kantonalbank", "Gründung & Ausgangslage", "Kantonalbank des Kantons Luzern seit 1850"],
            ["2001", "Umwandlung in AG & Börsengang (SIX: LUKN)", "Rechtsformwechsel", "Privatrechtliche AG mit Staatsgarantie und 61,5 % Kantonsbeteiligung"],
            ["2006–2010", "Adler & Co. Privatbank AG", "Akquisition & Fusion", "Übernahme Standort Basel (2006) und vollständige Fusion mit LUKB (2010)"],
            ["2025", "175-Jahr-Jubiläum & Integration Refinum AG", "Jubiläum & Konsolidierung", "Integration der Tochter Refinum AG per 31. Januar 2025 ins Stammhaus"],
        ],
        "sources": "LUKB Geschäftsberichte (2001–2025); LUKB Chronik",
    },
    "fkb": {
        "founded": "1892 (Freiburger Kantonalbank / Banque Cantonale de Fribourg, Gesetz vom 29. Dezember 1892)",
        "lineage_summary": (
            "Die Freiburger Kantonalbank (FKB) wurde durch Gesetz vom 29. Dezember 1892 als öffentlich-rechtliche "
            "Anstalt des Kantons Freiburg gegründet und nahm 1893 ihre Geschäftstätigkeit auf. Seit 1900 wuchs sie "
            "kontinuierlich organisch ohne Grossfusionen zur klaren Marktführerin im zweisprachigen Kanton Freiburg "
            "(heute 25–26 Niederlassungen) und übernahm während der Immobilienkrise der 1990er-Jahre eine stabilisierende "
            "Rolle im Kanton."
        ),
        "mermaid": """flowchart TD
    FKB1892["Freiburger Kantonalbank (gegr. 1892, Stand 1900)"] -->|"Organisches Wachstum im Kanton Freiburg"| FKB1990["FKB (1990er: Stabilität nach Konkurs Freiburger Hypothekarkasse)"]
    FKB1990 -->|"1993–2025: Kontinuierliche Expansion & Digitalisierung"| FKB["Freiburger Kantonalbank (heute, 100 % Kanton Freiburg)"]""",
        "milestones": [
            ["1892 / 1900", "Freiburger Kantonalbank (FKB / BCF)", "Gründung & Ausgangslage", "Gesetz vom 29. Dezember 1892; öffentlich-rechtliche Staatsbank mit Sitz in Freiburg"],
            ["1992", "100-Jahr-Jubiläum & Stiftung der FKB", "Meilenstein", "Gründung der 100-Jahre-Stiftung zugunsten von Kultur, Sozialem und Wirtschaft im Kanton Freiburg"],
            ["1993–2011", "Ära Albert Michel (CEO)", "Wachstum & Marktführerschaft", "Stabilisierung des Freiburger Bankenplatzes in den 1990er-Jahren und Ausbau des Filialnetzes"],
            ["2015–2025", "FINMA-RVB, Zinswende & Digitalisierung", "Modernisierung", "Bilanzwachstum von CHF 20,6 Mrd. (2015) auf CHF 29,5 Mrd. (2025) bei branchenführender CIR (~32–38 %)"],
        ],
        "sources": "FKB Geschäftsberichte (2015–2025); Gesetz über die Freiburger Kantonalbank",
    },
}
