#!/usr/bin/env python3
"""Strukturierte IT-Strategie-, Kernbankensystem- und Digitalisierungsdaten für alle 19 Institute."""

from __future__ import annotations

IT_STRATEGY_DATA: dict[str, dict] = {
    "bekb": {
        "core_banking": "IBIS4D (Eigenentwicklung / ehemaliger RTC- & DXC-Verbund)",
        "operating_model": "Eigene IT-Tochter aity (Reintegration ins Mutterhaus per 01.01.2028 beschlossen)",
        "cloud_ai_data": [
            "Umbau von IBIS4D in Richtung Microservices und vollständiger Mainframe-Verzicht.",
            "Fokus auf Open Banking / Embedded Finance sowie enge Verzahnung von Fachverantwortung und IT-Umsetzung durch die Integration von Aity.",
        ],
        "digital_channels": "BEKB E-Banking, BEKB-App, Nachhaltigkeitsportal «Hüt für morn»",
        "cyber_resilience": "Gezielte Investitionen in Systemmodernisierung, Cyberresilienz und operative Stabilität (FINMA-Kat. 3).",
        "sources": "bekb/.md/bekb-geschaeftsbericht-2025.md; Netzwoche / MoneyToday (Nov. 2026 zur Aity-Integration)",
    },
    "vskb": {
        "core_banking": "Finnova (seit 2007)",
        "operating_model": "Zentralisiertes IT-Outsourcing & Infrastrukturbetrieb über Swisscom",
        "cloud_ai_data": [
            "Migration auf eine souveräne Swisscom-Cloud-Lösung sowie cloudbasierte Arbeitsplätze (Swisscom Enterprise Workplace / Microsoft 365, Intune, Teams).",
            "Reduktion historisch fragmentierter Rechenzentren zugunsten einer einheitlichen Plattform.",
        ],
        "digital_channels": "WKB Online-Banking, Mobile-Banking, digitale Hypothekar- und Anlageservices",
        "cyber_resilience": "Konsequente Zero-Trust-Sicherheitsarchitektur (DLP, Verschlüsselung, lückenlose Zugriffskontrolle) in Partnerschaft mit Swisscom.",
        "sources": "vskb/.md/vskb-geschaeftsbericht-2025.md; Swisscom Success Story BCVS / WKB",
    },
    "zkb": {
        "core_banking": "Avaloq Banking Suite (seit 2009)",
        "operating_model": "Hybrides Betriebsmodell: On-Premises-Core kombiniert mit SaaS-/Cloud-Modulen",
        "cloud_ai_data": [
            "Einsatz der cloudbasierten Avaloq Digital Asset Platform (mit Fireblocks, seit 2024) für digitale Vermögenswerte.",
            "Gemeinsame Mobile-Banking-Plattform auf Avaloq-Basis mit weiteren Kantonalbanken; Fokus auf sichere Softwareentwicklung und Automatisierung.",
        ],
        "digital_channels": "ZKB eBanking, ZKB Mobile Banking, ZKB TWINT, digitale Anlage- & ETF-Plattformen",
        "cyber_resilience": "D-SIB-konforme IT-Risiko-Governance, Fokus auf sichere Softwareentwicklung und hohe Systemverfügbarkeit.",
        "sources": "zkb/.md/zkb-geschaeftsbericht-2025.md; Swisscom Core Banking Radar; Avaloq / IT-Finanzmagazin",
    },
    "bcv": {
        "core_banking": "Osiris (Eigenentwicklung auf IBM Host)",
        "operating_model": "In-House-Weiterentwicklung in strategischer Infrastruktur-Partnerschaft mit IBM",
        "cloud_ai_data": [
            "Bewusste Unabhängigkeit von Standard-Kernbankenpaketen (weder Finnova noch Avaloq), kontinuierliche Modernisierung der eigenen Osiris-Plattform.",
            "Strategieplan vista mit Fokus auf digitale Kundenschnittstellen bei stabiler Eigenarchitektur.",
        ],
        "digital_channels": "BCV-net, BCV Mobile, BCV TWINT, digitale Vorsorge- und Vermögensverwaltungs-Tools",
        "cyber_resilience": "Hohe Eigenkontrolle über Kernprozesse und Host-Stabilität; kontinuierliches Cyber- und OpRisk-Monitoring.",
        "sources": "bcv/.md/bcv-geschaeftsbericht-2025.md; Swisscom Core Banking Radar; Inside IT",
    },
    "gekb": {
        "core_banking": "Finnova (inkl. Verwaltungsrats-Einsitz bei Finnova AG, Lenzburg)",
        "operating_model": "Standard-Kernbankensystem mit eigener Weiterentwicklung und API-Anbindung",
        "cloud_ai_data": [
            "Aktive Mitgestaltung der Finnova-Roadmap über den Verwaltungsrat der Finnova AG.",
            "Digitalisierung der Handelsfinanzierungs-, Anlage- und KMU-Prozesse entlang der genferischen und internationalen Standorte.",
        ],
        "digital_channels": "BCGE Netbanking, BCGE Mobile Netbanking, BCGE TWINT, 1816 Online-Trading",
        "cyber_resilience": "Strenge Zugriffs- und Berechtigungskontrollen (u. a. privilegierte Systemmodule), jährliche Sicherheitsaudits.",
        "sources": "gekb/.md/gekb-geschaeftsbericht-2025.md (Corporate Governance / Finnova)",
    },
    "raiffeisen": {
        "core_banking": "Avaloq (Livegang 2019 über 900 Standorte, Weiterentwicklung via ehemaliges Arizon-Know-how)",
        "operating_model": "Gruppenweite Einheitsplattform durch Raiffeisen Schweiz (D-SIB) für alle Raiffeisenbanken",
        "cloud_ai_data": [
            "Hohe Dynamik rund um Datenmanagement und Künstliche Intelligenz (KI) unter strengen regulatorischen Auflagen für kritische Daten.",
            "Positionierung als «Smart Follower»: Überprüfung und Fokussierung laufender Technologieprojekte aus «Raiffeisen 2025» auf Vorsorge, Anlegen und Effizienz.",
        ],
        "digital_channels": "Raiffeisen E-Banking, Raiffeisen TWINT, Rio Anlage-App, Kundenportal",
        "cyber_resilience": "Zentrale D-SIB-Sicherheitsarchitektur, strenge Data-Governance und Notfall-/Resilienzplanung über die gesamte Gruppe.",
        "sources": "raiffeisen/.md/raiffeisen-geschaeftsbericht-2025.md (Technologie & KI); Raiffeisen / Netzwoche",
    },
    "postfinance": {
        "core_banking": "TCS BaNCS (Tata Consultancy Services, seit 2018)",
        "operating_model": "Skalierbare Hochleistungs-Plattform (>1 Mrd. Transaktionen/Jahr, ~60 % des CH-Zahlungsverkehrs)",
        "cloud_ai_data": [
            "Modernisierung des Zahlungsverkehrs- und Kontokerns auf Basis von TCS BaNCS zur Vermeidung von Legacy-Fragmentierung.",
            "Ausbau digitaler Anlage-, Krypto- und Open-Banking-Services innerhalb des gesetzlichen Kreditverbots.",
        ],
        "digital_channels": "PostFinance E-Finance, PostFinance App, PostFinance TWINT, Yuh (Joint Venture)",
        "cyber_resilience": "Dedizierter VR-Ausschuss «Informationstechnologie & Digitalisierung»; D-SIB-Anforderungen an Zahlungsverkehrs-Verfügbarkeit.",
        "sources": "postfinance/.md/postfinance-geschaeftsbericht-2025.md; TCS BaNCS Press Release / Inside IT",
    },
    "ubs": {
        "core_banking": "Eigenentwickelte globale Plattformen (inkl. Dekommissionierung der Credit-Suisse-IT bis Ende 2026)",
        "operating_model": "Globale Multi-Cloud- & In-House-Engineering-Organisation (strategischer Cloud-/AI-Partner: Microsoft Azure)",
        "cloud_ai_data": [
            "Über 380 Live-AI-Use-Cases Ende 2025 (u. a. «Red»-Assistenten auf Azure OpenAI, STAAT Insights, RiskLab) und 9 grosse Transformationsinitiativen.",
            "Rund 18'000 Entwickler (Q2-2026, nach 3'000 im Okt. 2025) nutzen AI-Coding-Tools; breite AI-Upskilling-Programme für Mitarbeitende.",
        ],
        "digital_channels": "UBS e-banking, UBS Mobile Banking (inkl. AI-Chatbots für 1,2 Mio. Mobile-Kunden), UBS TWINT, UBS Key4",
        "cyber_resilience": "Formelles AI-Governance-Framework mit Risk-Appetite-Metriken, G-SIB-Cyberabwehr und geordneter CS-Systemabschaltung.",
        "sources": "ubs/.md/ubs-geschaeftsbericht-2025.md (AI Strategy); BankingNewsAI / Fintechnews.ch",
    },
    "eks": {
        "core_banking": "Finstar (SaaS-Kernbankensystem der Hypothekarbank Lenzburg)",
        "operating_model": "Vollständiges Software-as-a-Service (SaaS) Modell für schlanke 4-Personen-Bank",
        "cloud_ai_data": [
            "Nutzung der modularen Finstar-Plattform inkl. Open Banking API zur Vermeidung eigener Gross-IT-Infrastruktur.",
            "Konservative Bilanzierung von Software/IT-Anlagen (Abschreibung max. 3 Jahre).",
        ],
        "digital_channels": "E-Banking / Mobile Banking auf Finstar-Basis",
        "cyber_resilience": "Auslagerung des technischen Betriebs an regulierten Schweizer Banken-IT-Provider (Hypothekarbank Lenzburg / Finstar) unter Stiftungsrats-Aufsicht.",
        "sources": "eks/.md/eks-geschaeftsbericht-2025.md; MoneyToday (Finstar-Kundenliste)",
    },
    "slm": {
        "core_banking": "Entris Banking Plattform (selbständige Regionalbank in der Entris-Holding)",
        "operating_model": "Gemeinschaftlicher Regionalbanken-IT- & Processing-Verbund über Entris Banking AG",
        "cloud_ai_data": [
            "Einführung einer eigenen TWINT-App mit direkter Kontoanbindung (Herbst 2025) sowie Zentralisierung der Bargeldtransaktionen.",
            "Intensive Entwicklung und Einführung einer neuen eBanking-Lösung (Produktivstart Frühling 2026).",
        ],
        "digital_channels": "SLM eBanking (neu 2026), SLM TWINT-App, ISO-20022-Unternehmensanbindung",
        "cyber_resilience": "Interne Fachspezialisierung für Informatik & Kreditrisikomanagement kombiniert mit dem Verbund-Betrieb von Entris.",
        "sources": "slm/.md/slm-geschaeftsbericht-2025.md (Lagebericht); Entris Banking",
    },
    "aek": {
        "core_banking": "Finnova",
        "operating_model": "Betrieb und Infrastruktur über den Regionalbanken-Verbund ESPRIT Netzwerk AG",
        "cloud_ai_data": [
            "Nutzung standardisierter Open-Banking-CH-Schnittstellen und Anbindung an moderne Buchhaltungs- und KMU-Ökosysteme.",
            "Interne Projektarbeit zur «Arbeitswelt 2030» zur Abstimmung von Technologie, Filialnetz und Beratung.",
        ],
        "digital_channels": "AEK E-Banking, AEK BANK 1826 App, AEK TWINT",
        "cyber_resilience": "Standardisierte Finnova-/ESPRIT-Betriebssicherheit bei tiefer Cost-Income-Ratio (37,3 %).",
        "sources": "aek/.md/aek-geschaeftsbericht-2025.md; ESPRIT Netzwerk AG; Abacus EGI",
    },
    "migrosbank": {
        "core_banking": "Finnova (seit 2009, inkl. eigenentwickelter FDK-Module)",
        "operating_model": "Langjährige strategische IT-Betriebspartnerschaft mit Inventx (Finnova, Umsysteme, Infrastruktur)",
        "cloud_ai_data": [
            "Aktiver Einsatz von generativer KI (GenAI) zur Prozess- und Beratungsunterstützung.",
            "Cloud-Projekte in Zusammenarbeit mit Inventx sowie eigenes Release- und Testmanagement für Finnova Development Kit (FDK) Module.",
        ],
        "digital_channels": "Migros Bank E-Banking, Migros Bank App, TWINT, Videoberatung",
        "cyber_resilience": "Umfassendes Informationssicherheits- und Outsourcing-Risikomanagement (Vertraulichkeit, Integrität, Verfügbarkeit im Finnova/Inventx-Setup).",
        "sources": "migrosbank/.md/migrosbank-geschaeftsbericht-2025.md; Inventx; Computerworld; Netzwoche (Juli 2025)",
    },
    "vontobel": {
        "core_banking": "Avaloq (Core Banking & Avaloq Cloud / BPO-Komponenten)",
        "operating_model": "Modulare Enterprise IT Architecture mit Data-Mesh-Prinzipien, Low-Code (Appian) und Cloud",
        "cloud_ai_data": [
            "Aufbau einer modernen Data Platform (Data Products / Data Marketplace) als Fundament für Analytics und Agentic/Generative AI.",
            "Kooperation mit Microsoft (Azure OpenAI Service) zur Produktivitätssteigerung sowie Verknüpfung von deritrade® mit der Avaloq-Wealth-Plattform.",
        ],
        "digital_channels": "Vontobel Wealth / Mobile, deritrade® (strukturierte Produkte), Vontobel Volt®",
        "cyber_resilience": "Risk Indicator Framework für IT-, Daten- und Cybersicherheit gemäss FINMA-Anforderungen; reibungslose IHAG-Systemintegration 2025.",
        "sources": "vontobel/.md/vontobel-geschaeftsbericht-2025.md; Vontobel Enterprise IT Architecture; Microsoft / Avaloq",
    },
    "pictet": {
        "core_banking": "Eigenentwickelte / modulare Privatbanken-Plattformen mit In-House-Recheninfrastruktur",
        "operating_model": "Hohe technologische Souveränität (eigene Hochleistungs-Server für AI & Datenkontrolle)",
        "cloud_ai_data": [
            "Entwicklung von «One.chat» (mit Zürcher Startup Unique) für interne Produktivität, Voice-to-Text-Call-Reports und automatisierte KYC-Prüfung.",
            "Eigene Server-Cluster (statt voller Abhängigkeit von externen Cloud-Preisen) für quantitative AI-Enhanced ETFs und Quest AI (>USD 1 Mrd. AuM).",
        ],
        "digital_channels": "Pictet Connect, Pictet Wealth Mobile, modulare digitale Kundenschnittstellen",
        "cyber_resilience": "Striktes Vertraulichkeits- und Bankgeheimnis-Design: interne AI-Produktivitäts-Tools ohne Preisgabe von Kundendaten an Dritte; formelles AI- & Cyber-OpRisk-Framework.",
        "sources": "pictet/.md/pictet-geschaeftsbericht-2025.md (Operational & AI Risks); Pictet / PwC Interview; Hubbis; Colombus Consulting",
    },
    "entris": {
        "core_banking": "Zentrale B2B-Giro-, Zahlungsverkehrs- & Global-Custody-Plattform (u. a. EntriX Payment Services; ehem. Entris Operations 2013 an Swisscom veräussert)",
        "operating_model": "Shared-Services- & Zentralbank-Plattform für 35 Regionalbanken und Drittbanken (Eingliederung des IT-Betriebsteams Giro-Management 2025)",
        "cloud_ai_data": [
            "Aufbau und Produktivsetzung von EntriX Payment Services sowie Erneuerung der Zahlungsverkehrs- und Karteninfrastruktur (>400'000 Debitkarten).",
            "Skalierung der Global-Custody- und Wertschriftenabwicklungsplattform auf CHF 35 Mrd. Assets under Custody sowie zentrales Bancomaten-Management.",
        ],
        "digital_channels": "B2B-Bankenplattformen (Giroorganisation, Trading & Treasury, Bancomaten-Service, Vorsorgestiftungen)",
        "cyber_resilience": "FINMA-konformes OpRisk- & IKT-Kontrollsystem für systemkritische B2B-Zahlungsverkehrs-, Custody- und Liquiditätsprozesse der Regionalbanken.",
        "sources": "entris/.md/entris-geschaeftsbericht-2025.md; entris.ch/insights (2025–2026)",
    },
    "valiant": {
        "core_banking": "Finnova (Gesamtbankenlösung, Migration 2011; konsolidiert für Ein-Bank-Plattform)",
        "operating_model": "Standardisierte Finnova-Architektur mit hybrider Geschäftsstellen- und Digitalberatung («einfach banken»)",
        "cloud_ai_data": [
            "Durchgängige End-to-End-Digitalisierung im Hypothekar- und KMU-Kreditprozess sowie Ausbau der Valiant-App und Online-Beratung.",
            "Effizienzprogramm im Rahmen der Strategie «Valiant 2029» zur Prozessautomatisierung und Filialnetz-Optimierung über 15 Kantone.",
        ],
        "digital_channels": "Valiant App, Valiant eBanking, Online-Hypotheken & Video-/Hybridberatung",
        "cyber_resilience": "FINMA-konformes OpRisk- und IKT-Sicherheits-Framework für überregionale Retail- & KMU-Plattform.",
        "sources": "valiant/.md/valiant-geschaeftsbericht-2025.md & valiant-geschaeftsbericht-2024.md",
    },
    "sgkb": {
        "core_banking": "Avaloq Banking System (Stammhaus Schweiz, eingeführt 2008); Atruvia AG (SGKB Deutschland AG)",
        "operating_model": "Multi-Provider-Outsourcing des IT-Betriebs an Swisscom (Schweiz) AG und Inventx AG; Atruvia für Deutschland",
        "cloud_ai_data": [
            "Aktives Technologie-Scouting und schrittweise Umsetzung bei Reife in den Bereichen Künstliche Intelligenz, Blockchain und Quantum Computing.",
            "Ausbau der digitalen Kundenkanäle, Mobile-ID-Authentifizierung (mit Swisscom) und Valorendaten-BPO.",
        ],
        "digital_channels": "SGKB E-Banking, SGKB Mobile Banking, SGKB TWINT, digitale Kontoeröffnung & Beratung",
        "cyber_resilience": "FINMA-konformes OpRisk- & IKT-Kontrollsystem; regelmässige Überprüfung der Outsourcing-Partner Swisscom, Inventx und Atruvia.",
        "sources": "sgkb/.md/sgkb-geschaeftsbericht-2025.md (Kernbankensystem & F&E); sgkb-geschaeftsbericht-2018.md",
    },
    "blkb": {
        "core_banking": "Avaloq Banking System (eingeführt 2010 als erste grössere Standardplattform-Migration)",
        "operating_model": "Modulare Avaloq-Plattform im Stammhaus; geordnete Beendigung der separaten Cloud-Tochterplattform radicant (2025)",
        "cloud_ai_data": [
            "Erweiterung der Datenstrategie 2025 um Künstliche Intelligenz (KI) inklusive bankweiter Schulung der Mitarbeitenden in KI-Governance.",
            "Fokussierung der IT-Investitionen auf das Kerngeschäft Nordwestschweiz, Prozessautomatisierung und digitale Beratungsprozesse nach dem radicant-Ausstieg.",
        ],
        "digital_channels": "BLKB E-Banking, BLKB Mobile Banking, BLKB TWINT, digitale Vorsorge- und Finanzierungsstrecken",
        "cyber_resilience": "FINMA-konformes IKT- & OpRisk-Framework; aktive Sensibilisierung von Kundschaft und Öffentlichkeit zu Cybersicherheit.",
        "sources": "blkb/.md/blkb-geschaeftsbericht-2025.md (Datenstrategie, KI-Governance & radicant); Inside IT (Avaloq 2008/2010)",
    },
    "lukb": {
        "core_banking": "Avaloq Banking System (Evaluationsentscheid 2013 gegen Finnova / Ablösung der AGI-Plattform)",
        "operating_model": "Eigenes Geschäftsleitungs-Departement Technology & Services (geleitet von Dr. Simon Kauth) auf Avaloq-Basis",
        "cloud_ai_data": [
            "Aufbau einer modernen Digital- und Krypto-Infrastruktur (einfacher Handel und Verwahrung von Kryptowährungen seit März 2024).",
            "Durchgängige Digitalisierung der Kundenprozesse (LUKB E-Banking, LUKB TWINT seit 2022) und schalterlose Filialkonzepte (2023).",
        ],
        "digital_channels": "LUKB E-Banking, LUKB Mobile Banking, LUKB TWINT, Krypto-Plattform & digitale Vermögensverwaltung",
        "cyber_resilience": "FINMA-konformes OpRisk- & IKT-Kontrollsystem; hohe Investitionen in IT-Sicherheit und Stabilität der Avaloq-Plattform.",
        "sources": "lukb/.md/lukb-geschaeftsbericht-2025.md (Departement Technology & Services, Lagebericht); Finews / Netzwoche",
    },
    "fkb": {
        "core_banking": "Finnova Banking Software & CreditMaster (IT-Outsourcing über Swisscom (Schweiz) AG)",
        "operating_model": "Vollständiges IT-Betriebsoutsourcing an Swisscom (Schweiz) AG; Rating-/Pricing-Modelle via RSN, Immobilienbewertung via Wüest Partner, Digitalisierung via SPS",
        "cloud_ai_data": [
            "Einsatz von Generativer KI auf der Swisscom Swiss AI Platform (u. a. als interner Kreditvergabe-Assistent mit Quellenangabe sowie für die Support-Ticket-Triage).",
            "Lancierung der neuen App «FKB Banking» und von «FKB Multibanking» für Firmenkunden im Jahr 2025; eigene Division «Technologien und Lösungen».",
        ],
        "digital_channels": "FKB e-banking, FKB Banking App (2025), FKB TWINT (57'046 Nutzende), FKB Multibanking",
        "cyber_resilience": "FINMA-konformes OpRisk- & IKT-Kontrollsystem; dedizierte Cybersecurity-Kompetenz im Verwaltungsrat (Paul Such) sowie Prüfung der Systeme Finnova & CreditMaster.",
        "sources": "fkb/.md/fkb-geschaeftsbericht-2025.md (Outsourcing, Revisionsbericht & Digitalisierung); Swisscom B2B Mag (2025)",
    },
}
