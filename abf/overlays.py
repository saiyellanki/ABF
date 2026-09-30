"""Additional authoritative overlays: SR 11-7, OWASP LLM Top 10 2025, NIST AI 600-1 GAI risks."""

SR117_SOURCE = {
    "id": "SR-11-7",
    "name": "SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management",
    "date": "April 4, 2011",
    "url": "https://www.occ.gov/news-issuances/bulletins/2011/bulletin-2011-12.html",
    "license_note": "U.S. federal supervisory guidance. Applies to banking organizations supervised by the OCC, Federal Reserve, and FDIC; not automatically to every AI system.",
}

SR117_ELEMENTS = [
    {
        "id": "SR117-DEV",
        "code": "SR 11-7 Development",
        "title": "Model development, implementation, and use",
        "official_text": (
            "Supervisory guidance expects sound development, implementation, and use of models: "
            "clear statement of purpose, conceptually sound design, appropriate data, testing before "
            "implementation, and use consistent with the model's design and documented limitations."
        ),
        "tags": ["sr117"],
    },
    {
        "id": "SR117-VAL",
        "code": "SR 11-7 Validation",
        "title": "Model validation (independent)",
        "official_text": (
            "Effective validation is performed by staff with appropriate incentives, competence, and "
            "influence, independent of model development and use. Core elements include evaluation of "
            "conceptual soundness (including developmental evidence), ongoing monitoring (including "
            "process verification and benchmarking), and outcomes analysis (including back-testing)."
        ),
        "tags": ["sr117", "tevv"],
    },
    {
        "id": "SR117-GOV",
        "code": "SR 11-7 Governance",
        "title": "Governance, policies, and controls",
        "official_text": (
            "Board and senior management are expected to establish a model risk management framework "
            "with policies, procedures, staff, and controls commensurate with the bank's risk exposures, "
            "including a comprehensive model inventory, documentation standards, and limits on use of "
            "models that are deficient or that have identified weaknesses."
        ),
        "tags": ["sr117", "governance_baseline", "inventory"],
    },
]

OWASP_SOURCE = {
    "id": "OWASP-LLM-2025",
    "name": "OWASP Top 10 for Large Language Model Applications 2025",
    "date": "2025",
    "url": "https://owasp.org/www-project-top-10-for-large-language-model-applications/",
    "license_note": "OWASP materials are typically CC BY-SA. Entries are threat categories, not regulatory controls.",
}

OWASP_LLM_2025 = [
    {"id": "LLM01", "title": "Prompt Injection", "official_text": "User or untrusted content alters the LLM's behaviour or instructions (direct or indirect)."},
    {"id": "LLM02", "title": "Sensitive Information Disclosure", "official_text": "The system reveals secrets, personal data, or proprietary content in outputs or side channels."},
    {"id": "LLM03", "title": "Supply Chain", "official_text": "Compromised models, datasets, plugins, or third-party components introduce risk into the LLM application."},
    {"id": "LLM04", "title": "Data and Model Poisoning", "official_text": "Training, fine-tuning, or embedding data is manipulated to degrade or steer model behaviour."},
    {"id": "LLM05", "title": "Improper Output Handling", "official_text": "Insufficient validation of model output leads to XSS, RCE, data exfiltration, or privilege issues downstream."},
    {"id": "LLM06", "title": "Excessive Agency", "official_text": "The LLM is granted too much autonomy, functionality, or permission to invoke tools and take actions."},
    {"id": "LLM07", "title": "System Prompt Leakage", "official_text": "Hidden developer instructions, secrets, or policy text in the system prompt are extracted."},
    {"id": "LLM08", "title": "Vector and Embedding Weaknesses", "official_text": "Retrieval/embedding pipelines allow data leakage, poisoning, or authorization bypass via the vector store."},
    {"id": "LLM09", "title": "Misinformation", "official_text": "The system produces false, unsupported, or hallucinated content that users may rely on."},
    {"id": "LLM10", "title": "Unbounded Consumption", "official_text": "Uncontrolled inference, tool calls, or context growth causes denial of service or cost/resource abuse."},
]

GAI_SOURCE = {
    "id": "NIST-AI-600-1",
    "name": "NIST AI 600-1 — Generative AI Profile",
    "date": "July 2024",
    "url": "https://doi.org/10.6028/NIST.AI.600-1",
    "license_note": "U.S. government work. Profile is voluntary. Lists 12 GAI risks and suggested actions mapped to AI RMF subcategories.",
}

GAI_RISKS = [
    {"id": "GAI-CBRN", "title": "CBRN information or capabilities", "official_text": "Generative systems may lower barriers to chemical, biological, radiological, or nuclear information or capabilities."},
    {"id": "GAI-CONFAB", "title": "Confabulation", "official_text": "The model produces plausible but incorrect or fabricated content (hallucination)."},
    {"id": "GAI-VIOLENT", "title": "Dangerous or violent recommendations", "official_text": "Outputs may recommend or enable dangerous or violent activity."},
    {"id": "GAI-PRIVACY", "title": "Data privacy", "official_text": "Training, prompts, retrieval, or outputs may expose or mishandle personal or sensitive data."},
    {"id": "GAI-ENV", "title": "Environmental", "official_text": "Training and operating generative models can have significant energy and environmental impact."},
    {"id": "GAI-BIAS", "title": "Harmful bias and homogenization", "official_text": "Generated content may encode harmful bias or collapse diverse outputs toward homogenized representations."},
    {"id": "GAI-CONFIG", "title": "Human-AI configuration", "official_text": "Risks arise from how humans and generative systems are configured to interact, oversee, and rely on each other."},
    {"id": "GAI-INTEGRITY", "title": "Information integrity", "official_text": "Generated or manipulated content can undermine authenticity, provenance, and public information integrity."},
    {"id": "GAI-SECURITY", "title": "Information security", "official_text": "Generative systems expand attack surface (prompt injection, data exfiltration, malware generation, credential leakage)."},
    {"id": "GAI-IP", "title": "Intellectual property", "official_text": "Training data and outputs may implicate copyright, trademark, trade secrets, or licensed content."},
    {"id": "GAI-ABUSIVE", "title": "Obscene, degrading, and/or abusive content", "official_text": "Systems may generate or fail to block obscene, degrading, or abusive material."},
    {"id": "GAI-VALUECHAIN", "title": "Value chain and component integration", "official_text": "Risk concentrates in third-party models, data, tools, plugins, and downstream integration."},
]


def as_obligations():
    items = []
    for row in SR117_ELEMENTS:
        items.append({
            "id": f"US-{row['id']}",
            "framework": "SR 11-7 / OCC 2011-12",
            "citation": f"Board/OCC/FDIC SR 11-7 (OCC Bulletin 2011-12), {row['title']}",
            "source_url": SR117_SOURCE["url"],
            "kind": "supervisory_expectation",
            "code": row["code"],
            "function": "MRM",
            "category": "Model risk management",
            "title": row["title"],
            "official_text": row["official_text"],
            "tags": row["tags"],
            "crosswalk": [],
        })
    for row in OWASP_LLM_2025:
        tags = ["owasp", "genai"]
        if row["id"] in {"LLM01", "LLM07"}:
            tags.append("security")
        if row["id"] in {"LLM06"}:
            tags.append("agentic")
        if row["id"] in {"LLM08"}:
            tags.append("rag")
        if row["id"] in {"LLM03"}:
            tags.append("third_party")
        if row["id"] in {"LLM02"}:
            tags.append("personal_data")
        items.append({
            "id": f"OWASP-{row['id']}",
            "framework": "OWASP LLM Top 10 2025",
            "citation": f"OWASP Top 10 for LLM Applications 2025, {row['id']}:{row['title']}",
            "source_url": OWASP_SOURCE["url"],
            "kind": "threat_category",
            "code": row["id"],
            "function": "AppSec",
            "category": "LLM application risks",
            "title": row["title"],
            "official_text": row["official_text"],
            "tags": tags,
            "crosswalk": [],
        })
    for row in GAI_RISKS:
        items.append({
            "id": f"NIST-{row['id']}",
            "framework": "NIST AI 600-1",
            "citation": f"NIST AI 600-1 (July 2024), GAI risk: {row['title']}",
            "source_url": GAI_SOURCE["url"],
            "kind": "risk_category",
            "code": row["id"],
            "function": "GAI Profile",
            "category": "Generative AI risks",
            "title": row["title"],
            "official_text": row["official_text"],
            "tags": ["gai_profile", "genai"],
            "crosswalk": [],
        })
    return items
