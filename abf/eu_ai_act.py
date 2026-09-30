"""EU Artificial Intelligence Act — Regulation (EU) 2024/1689.

Official text: https://eur-lex.europa.eu/eli/reg/2024/1689/oj
Commission service desk (Annex III): https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3

Summaries below are auditor-oriented paraphrases of public law, cited to article/annex.
They are not a substitute for the authentic Official Journal text.
"""

SOURCE = {
    "id": "EU-AI-ACT-2024-1689",
    "name": "Regulation (EU) 2024/1689 (Artificial Intelligence Act)",
    "date": "2024",
    "url": "https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
    "annex_iii_url": "https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3",
    "license_note": "EU legislative text is public. Application dates are staggered (Art. 113).",
}

# Annex III high-risk areas — paraphrased from the Commission AI Act Service Desk.
ANNEX_III = [
    {
        "id": "ANNEX-III-1",
        "code": "Annex III(1)",
        "title": "Biometrics (where permitted)",
        "official_text": (
            "Remote biometric identification (excluding verification whose sole purpose is to confirm "
            "a person is who they claim to be); biometric categorisation according to sensitive or "
            "protected attributes; emotion recognition."
        ),
        "tags": ["eu_annex_iii", "biometrics"],
    },
    {
        "id": "ANNEX-III-2",
        "code": "Annex III(2)",
        "title": "Critical infrastructure",
        "official_text": (
            "AI systems intended to be used as safety components in the management and operation of "
            "critical digital infrastructure, road traffic, or the supply of water, gas, heating or electricity."
        ),
        "tags": ["eu_annex_iii", "critical_infrastructure"],
    },
    {
        "id": "ANNEX-III-3",
        "code": "Annex III(3)",
        "title": "Education and vocational training",
        "official_text": (
            "Access/admission/assignment to education; evaluation of learning outcomes; assessing the "
            "appropriate level of education; monitoring/detecting prohibited student behaviour during tests."
        ),
        "tags": ["eu_annex_iii", "education", "fairness"],
    },
    {
        "id": "ANNEX-III-4",
        "code": "Annex III(4)",
        "title": "Employment, workers' management and access to self-employment",
        "official_text": (
            "Recruitment or selection (targeted job ads, analysing/filtering applications, evaluating candidates); "
            "decisions affecting terms of work, promotion or termination; allocating tasks based on behaviour "
            "or personal traits; monitoring and evaluating performance."
        ),
        "tags": ["eu_annex_iii", "employment", "fairness"],
    },
    {
        "id": "ANNEX-III-5",
        "code": "Annex III(5)",
        "title": "Essential private and public services and benefits",
        "official_text": (
            "Public-authority evaluation of eligibility for essential public assistance benefits and services "
            "(including healthcare); creditworthiness/credit scoring of natural persons except fraud detection; "
            "life and health insurance risk assessment and pricing; emergency-call classification, dispatch "
            "priority, and emergency patient triage."
        ),
        "tags": ["eu_annex_iii", "credit", "insurance", "public_benefits", "fairness"],
    },
    {
        "id": "ANNEX-III-6",
        "code": "Annex III(6)",
        "title": "Law enforcement (where permitted)",
        "official_text": (
            "Assessing risk of becoming a crime victim; polygraphs; evaluating reliability of evidence; "
            "assessing risk of offending or re-offending (not solely on profiling as defined in Directive "
            "(EU) 2016/680); profiling in detection, investigation or prosecution of criminal offences."
        ),
        "tags": ["eu_annex_iii", "law_enforcement"],
    },
    {
        "id": "ANNEX-III-7",
        "code": "Annex III(7)",
        "title": "Migration, asylum and border control management (where permitted)",
        "official_text": (
            "Polygraphs; assessing security, irregular-migration, or health risk of a person entering a "
            "Member State; assisting examination of asylum, visa or residence applications; detecting, "
            "recognising or identifying persons except verification of travel documents."
        ),
        "tags": ["eu_annex_iii", "migration"],
    },
    {
        "id": "ANNEX-III-8",
        "code": "Annex III(8)",
        "title": "Administration of justice and democratic processes",
        "official_text": (
            "Assisting a judicial authority in researching/interpreting facts and the law and applying the "
            "law to facts, or similar use in alternative dispute resolution; influencing the outcome of an "
            "election or referendum or voting behaviour (excluding administrative/logistical campaign tools "
            "to which persons are not directly exposed)."
        ),
        "tags": ["eu_annex_iii", "justice"],
    },
]

ARTICLES = [
    {
        "id": "ART-5",
        "code": "Article 5",
        "title": "Prohibited AI practices",
        "official_text": (
            "Places on the Union market, puts into service, or uses of listed practices are prohibited. "
            "The list includes (among others) subliminal/manipulative techniques causing or reasonably "
            "likely to cause significant harm; exploiting vulnerabilities of age, disability or socio-economic "
            "circumstances; social scoring causing detrimental treatment; untargeted scraping of facial images "
            "to build/expand facial-recognition databases; emotion recognition in the workplace or educational "
            "institutions (with limited medical/safety exceptions); biometric categorisation inferring certain "
            "sensitive attributes; assessing criminality solely on profiling or personality traits; and "
            "real-time remote biometric identification in publicly accessible spaces for law enforcement "
            "except narrowly defined cases. Consult the authentic Article 5 text for exceptions and conditions."
        ),
        "tags": ["eu_prohibited"],
    },
    {
        "id": "ART-6",
        "code": "Article 6",
        "title": "Classification rules for high-risk AI systems",
        "official_text": (
            "An AI system is high-risk if (Art. 6(1)) it is a safety component of a product, or is itself a "
            "product, covered by Union harmonisation legislation in Annex I and is required to undergo a "
            "third-party conformity assessment under that legislation; or (Art. 6(2)) it is listed in Annex III. "
            "Art. 6(3) provides that Annex III systems are not high-risk if they do not pose a significant risk "
            "of harm to health, safety or fundamental rights, including by not materially influencing the "
            "outcome of decision making. The exception does not apply if the system profiles natural persons. "
            "Providers that conclude an Annex III system is not high-risk must document that assessment before "
            "placing the system on the market or putting it into service."
        ),
        "tags": ["eu_classification"],
    },
    {
        "id": "ART-9",
        "code": "Article 9",
        "title": "Risk management system",
        "official_text": (
            "A continuous, iterative risk-management system shall be established, implemented, documented and "
            "maintained throughout the lifecycle of a high-risk AI system: identification and analysis of known "
            "and reasonably foreseeable risks; estimation and evaluation of risks arising from intended purpose "
            "and reasonably foreseeable misuse; evaluation of risks from post-market monitoring data; and "
            "adoption of appropriate and targeted risk-management measures."
        ),
        "tags": ["eu_high_risk", "eu_provider"],
    },
    {
        "id": "ART-10",
        "code": "Article 10",
        "title": "Data and data governance",
        "official_text": (
            "Training, validation and testing data sets shall be subject to appropriate data-governance and "
            "management practices. Data sets shall be relevant, sufficiently representative, and to the best "
            "extent possible, free of errors and complete in view of the intended purpose. Appropriate "
            "statistical properties, examination of possible biases, and relevant data-protection measures "
            "shall be considered."
        ),
        "tags": ["eu_high_risk", "eu_provider", "personal_data", "fairness"],
    },
    {
        "id": "ART-11",
        "code": "Article 11",
        "title": "Technical documentation",
        "official_text": (
            "Technical documentation shall be drawn up before the high-risk AI system is placed on the market "
            "or put into service and shall be kept up to date. It shall demonstrate compliance with Section 2 "
            "and provide national competent authorities and notified bodies with the information necessary to "
            "assess that compliance. Minimum content is set out in Annex IV."
        ),
        "tags": ["eu_high_risk", "eu_provider"],
    },
    {
        "id": "ART-12",
        "code": "Article 12",
        "title": "Record-keeping",
        "official_text": (
            "High-risk AI systems shall technically allow for the automatic recording of events (logs) over "
            "the lifetime of the system. Logging shall enable identification of situations that may result in "
            "the system presenting a risk or in a substantial modification, and shall facilitate post-market "
            "monitoring and operation monitoring."
        ),
        "tags": ["eu_high_risk", "eu_provider"],
    },
    {
        "id": "ART-13",
        "code": "Article 13",
        "title": "Transparency and provision of information to deployers",
        "official_text": (
            "High-risk AI systems shall be designed so that their operation is sufficiently transparent to "
            "enable deployers to interpret a system's output and use it appropriately. Instructions for use "
            "shall include identity and contact of the provider, characteristics, capabilities and limitations "
            "of performance, human-oversight measures, and the computational and hardware resources needed."
        ),
        "tags": ["eu_high_risk", "eu_provider"],
    },
    {
        "id": "ART-14",
        "code": "Article 14",
        "title": "Human oversight",
        "official_text": (
            "High-risk AI systems shall be designed and developed so that they can be effectively overseen by "
            "natural persons during the period in which they are in use. Oversight measures shall enable the "
            "persons to whom human oversight is assigned to understand the capacities and limitations, remain "
            "aware of automation bias, correctly interpret output, decide not to use or to disregard/override "
            "the output, and intervene or interrupt the system through a stop button or similar procedure."
        ),
        "tags": ["eu_high_risk", "eu_provider", "human_oversight"],
    },
    {
        "id": "ART-15",
        "code": "Article 15",
        "title": "Accuracy, robustness and cybersecurity",
        "official_text": (
            "High-risk AI systems shall be designed and developed so that they achieve an appropriate level of "
            "accuracy, robustness, and cybersecurity, and perform consistently in those respects throughout "
            "their lifecycle. Accuracy metrics shall be declared in the instructions for use. Resilience shall "
            "address errors, faults, inconsistencies, and attempts by unauthorised third parties to alter use "
            "or performance (including data poisoning and adversarial examples)."
        ),
        "tags": ["eu_high_risk", "eu_provider", "security", "tevv"],
    },
    {
        "id": "ART-16",
        "code": "Article 16",
        "title": "Obligations of providers of high-risk AI systems",
        "official_text": (
            "Providers shall ensure conformity with Section 2 requirements; indicate name/trademark and contact; "
            "have a quality management system (Art. 17); keep documentation (Art. 18); keep logs when under "
            "their control (Art. 19); take corrective actions (Art. 20); cooperate with competent authorities; "
            "demonstrate conformity on request; ensure accessibility requirements; and fulfil registration "
            "obligations (Art. 49)."
        ),
        "tags": ["eu_high_risk", "eu_provider"],
    },
    {
        "id": "ART-17",
        "code": "Article 17",
        "title": "Quality management system",
        "official_text": (
            "Providers shall put a quality management system in place that documents strategy for regulatory "
            "compliance, design/examination/verification/validation procedures, data-management procedures, "
            "the risk-management system, post-market monitoring, serious-incident reporting, communication "
            "with authorities, and resource/accountability arrangements."
        ),
        "tags": ["eu_high_risk", "eu_provider"],
    },
    {
        "id": "ART-26",
        "code": "Article 26",
        "title": "Obligations of deployers of high-risk AI systems",
        "official_text": (
            "Deployers shall take appropriate technical and organisational measures to use the system in "
            "accordance with the instructions for use; assign human oversight to persons with necessary "
            "competence, training and authority; ensure input data is relevant and sufficiently representative "
            "where they exercise control; monitor operation and report risks/serious incidents to the provider "
            "and authorities as required; keep logs under their control for a period of at least six months "
            "(subject to Union or national law); inform workers' representatives and affected workers; "
            "register use where they are public authorities or Union institutions; and inform natural persons "
            "subject to the use of certain Annex III systems that they are subject to that use (Art. 26(11))."
        ),
        "tags": ["eu_high_risk", "eu_deployer"],
    },
    {
        "id": "ART-27",
        "code": "Article 27",
        "title": "Fundamental rights impact assessment",
        "official_text": (
            "Before deploying a high-risk system referred to in Art. 6(2), deployers that are bodies governed "
            "by public law, or private entities providing public services, shall perform an assessment of the "
            "impact on fundamental rights. The same duty applies to deployers of Annex III point 5(b) and 5(c) "
            "systems (creditworthiness of natural persons, and life/health insurance risk assessment and pricing). "
            "Annex III point 2 (critical infrastructure) is excluded from this FRIA duty."
        ),
        "tags": ["eu_high_risk", "eu_deployer", "fria"],
    },
    {
        "id": "ART-50",
        "code": "Article 50",
        "title": "Transparency obligations for certain AI systems",
        "official_text": (
            "Providers shall ensure that AI systems intended to interact directly with natural persons are "
            "designed so that the persons concerned are informed that they are interacting with an AI system "
            "(unless this is obvious from the point of view of a reasonably well-informed, observant and "
            "circumspect person). Providers of AI systems generating synthetic audio, image, video or text "
            "content shall ensure the outputs are marked in a machine-readable format and detectable as "
            "artificially generated or manipulated. Deployers of emotion-recognition or biometric-categorisation "
            "systems shall inform natural persons exposed thereto. Deployers of systems that generate or "
            "manipulate image, audio or video content constituting a deep fake shall disclose that the content "
            "has been artificially generated or manipulated."
        ),
        "tags": ["eu_transparency", "genai"],
    },
    {
        "id": "ART-51",
        "code": "Article 51",
        "title": "Classification of GPAI models with systemic risk",
        "official_text": (
            "A general-purpose AI model is classified as a GPAI model with systemic risk if it has high-impact "
            "capabilities evaluated on the basis of appropriate technical tools and methodologies, including "
            "indicators and benchmarks. A model is presumed to have high-impact capabilities when the "
            "cumulative amount of computation used for its training is greater than 10^25 FLOPs. Providers "
            "shall notify the Commission without delay and in any event within two weeks if the threshold is met."
        ),
        "tags": ["eu_gpai"],
    },
    {
        "id": "ART-53",
        "code": "Article 53",
        "title": "Obligations for providers of GPAI models",
        "official_text": (
            "Providers of general-purpose AI models shall draw up and keep up-to-date technical documentation, "
            "including the training and testing process and the results of its evaluation; draw up and keep "
            "up-to-date information and documentation for downstream providers; put in place a policy to comply "
            "with Union copyright law; and publish a sufficiently detailed summary about the content used for "
            "training. Certain free and open-source GPAI models that are not systemic-risk models have a "
            "reduced set of these obligations."
        ),
        "tags": ["eu_gpai"],
    },
    {
        "id": "ART-55",
        "code": "Article 55",
        "title": "Obligations of providers of GPAI models with systemic risk",
        "official_text": (
            "In addition to Art. 53, providers of GPAI models with systemic risk shall perform model evaluation "
            "in accordance with standardised protocols and tools reflecting the state of the art, including "
            "conducting and documenting adversarial testing; assess and mitigate possible systemic risks; "
            "track, document and report serious incidents and possible corrective measures to the AI Office "
            "and national competent authorities without undue delay; and ensure an adequate level of "
            "cybersecurity protection for the model and its physical infrastructure."
        ),
        "tags": ["eu_gpai_systemic"],
    },
    {
        "id": "ANNEX-IV",
        "code": "Annex IV",
        "title": "Technical documentation referred to in Article 11(1)",
        "official_text": (
            "Annex IV specifies the minimum technical-documentation content for high-risk AI systems, including "
            "a general description of the system and intended purpose; a detailed description of the elements "
            "and development process (design specifications, design choices, data requirements, training/"
            "testing/validation procedures, cybersecurity measures); monitoring, functioning and control; "
            "the risk-management system; changes over the lifecycle; a list of harmonised standards applied; "
            "the EU declaration of conformity; and a description of the system in operation."
        ),
        "tags": ["eu_high_risk", "eu_provider"],
    },
]


def as_obligations():
    items = []
    for row in ARTICLES + ANNEX_III:
        items.append({
            "id": f"EU-{row['id']}",
            "framework": "EU AI Act (Reg. 2024/1689)",
            "citation": f"Regulation (EU) 2024/1689, {row['code']}",
            "source_url": SOURCE["url"] if not row["id"].startswith("ANNEX-III") else SOURCE["annex_iii_url"],
            "kind": "legal_obligation",
            "code": row["code"],
            "function": "EU AI Act",
            "category": row["code"],
            "title": row["title"],
            "official_text": row["official_text"],
            "tags": row["tags"] + ["eu"],
            "crosswalk": [],
        })
    return items
