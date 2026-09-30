"""ABF-authored audit procedures mapped to official requirement IDs.

These are workpaper procedures, not the standards themselves.
"""

# Each procedure attaches to one primary official ID.
PROCEDURES = [
    {
        "id": "PROC-GOVERN-1.1",
        "primary": "NIST-GOVERN-1.1",
        "title": "Legal and regulatory inventory for the in-scope AI system",
        "target_roles": ["AI governance lead", "Legal / compliance", "CISO"],
        "inquiry": (
            "Walk me through the inventory of laws, regulations, and internal policies you have "
            "mapped to this system, including who owns updates when the intended purpose changes."
        ),
        "observe": (
            "Inspect the mapping register (or equivalent) for this system. Confirm it names concrete "
            "instruments (e.g., EU AI Act articles, SR 11-7 if a bank model, privacy law) rather than "
            "a generic 'AI policy' bullet. Check last-review date against a material change (new use case, "
            "new model provider, new geography)."
        ),
        "evidence": [
            "AI system legal/regulatory mapping register with owners and review dates",
            "Intended-purpose statement used as the mapping input",
            "Change-management ticket showing the mapping was revisited after a material change",
        ],
        "test": (
            "Select the in-scope system. Agree intended purpose with the owner. Independently list "
            "candidate instruments from the ABF screening. Compare to the auditee's register and "
            "document gaps. Do not treat an uncited 'AI ethics policy' as coverage of a named article."
        ),
    },
    {
        "id": "PROC-GOVERN-1.6",
        "primary": "NIST-GOVERN-1.6",
        "title": "AI system inventory completeness",
        "target_roles": ["AI inventory owner", "Enterprise architecture", "Model risk (if bank)"],
        "inquiry": "How do new LLM apps, copilots, and vendor embeddings enter the AI inventory, and what is excluded by policy?",
        "observe": (
            "Compare the official inventory to shadow sources: SaaS spend, API keys, vector databases, "
            "and MLflow/model-registry entries. Look for unregistered RAG or agent prototypes in production paths."
        ),
        "evidence": [
            "Current AI / model inventory extract with owner, intended purpose, and risk tier",
            "Procedure for adding, changing, and decommissioning inventory records",
            "Reconciliation sample against cloud billing or API-key inventory",
        ],
        "test": "Sample five production AI uses from a non-inventory source; trace each to an inventory record or document an exception.",
    },
    {
        "id": "PROC-GOVERN-3.2",
        "primary": "NIST-GOVERN-3.2",
        "title": "Human-AI configuration and oversight roles",
        "target_roles": ["Product owner", "Operations lead", "Model owner"],
        "inquiry": "Who is allowed to accept, override, or halt this system's output, and what competence is required of that person?",
        "observe": (
            "Review RACI / job descriptions for oversight. In a live walkthrough, ask the operator to "
            "show the override or stop path. If none exists, document residual automation-bias risk."
        ),
        "evidence": [
            "Documented human-oversight procedure (roles, training, escalation)",
            "Screenshot or demo of override / stop control in the production UI or API",
            "Training or competency records for persons assigned oversight",
        ],
        "test": "Trace one production decision path from model output to human action. Confirm the assigned person can interrupt the system.",
    },
    {
        "id": "PROC-GOVERN-6.1",
        "primary": "NIST-GOVERN-6.1",
        "title": "Third-party model, data, and tool due diligence",
        "target_roles": ["Procurement / vendor risk", "Security architecture", "Legal"],
        "inquiry": "What residual rights does the vendor have over prompts, embeddings, and logs, and how was that verified in the contract and DPA?",
        "observe": (
            "Read the enterprise agreement and data-processing terms for training-use, sub-processors, "
            "residency, and audit rights. Confirm the running environment matches the contracted tier "
            "(e.g., enterprise vs consumer API)."
        ),
        "evidence": [
            "Executed enterprise agreement / DPA with model or vector-DB vendor",
            "Vendor due-diligence file (SOC 2, ISO 27001, model card, data-use representations)",
            "Configuration evidence that production traffic uses the contracted endpoint/tier",
        ],
        "test": "For the production endpoint, compare contract, key/tenant configuration, and a sample request log.",
    },
    {
        "id": "PROC-MAP-1.1",
        "primary": "NIST-MAP-1.1",
        "title": "Intended purpose and deployment context",
        "target_roles": ["Product owner", "AI engineer", "Risk"],
        "inquiry": "State the intended purpose in one sentence, the users, the forbidden uses, and the jurisdictions of deployment.",
        "observe": "Compare marketing copy, system prompts, and production routing rules to the documented intended purpose. Flag scope creep.",
        "evidence": [
            "Intended-purpose / use-case document (feeds EU Annex IV if high-risk)",
            "User personas and out-of-scope uses",
            "Deployment topology (regions, tenants, connected tools)",
        ],
        "test": "Reconcile intended purpose to actual prompts, tools, and data sources in a live architecture walkthrough.",
    },
    {
        "id": "PROC-MAP-2.1",
        "primary": "NIST-MAP-2.1",
        "title": "Task and method characterization",
        "target_roles": ["Lead AI/ML engineer"],
        "inquiry": "Which tasks are classification, generation, retrieval, ranking, or tool-calling, and which model or component performs each?",
        "observe": "Walk the runtime graph (orchestrator, retriever, tools). Identify where untrusted content enters the prompt.",
        "evidence": [
            "Architecture diagram of the production path",
            "Model and component inventory (base model, fine-tunes, retrievers, tools)",
            "Description of human vs automated task split",
        ],
        "test": "From a production trace, label each hop as retrieve / generate / tool / human. Confirm it matches documentation.",
    },
    {
        "id": "PROC-MAP-3.5",
        "primary": "NIST-MAP-3.5",
        "title": "Documented human-oversight process",
        "target_roles": ["Operations", "AI product owner"],
        "inquiry": "In what cases must a human review output before it takes effect, and how is that enforced technically rather than by policy alone?",
        "observe": "Attempt (or review a recorded test of) a path that should require approval. Confirm the tool cannot complete without the approval token.",
        "evidence": [
            "Oversight design (human-in-the-loop vs human-on-the-loop vs human-in-command)",
            "Enforcement mechanism (workflow, allowlist, dual control)",
            "Exception log for skipped reviews",
        ],
        "test": "Select one high-impact action. Verify a control prevents unattended execution.",
    },
    {
        "id": "PROC-MEASURE-2.5",
        "primary": "NIST-MEASURE-2.5",
        "title": "Validity, reliability, and documented limits",
        "target_roles": ["Model developer", "Independent validator / QA"],
        "inquiry": "What held-out or production-like evaluation shows the system is valid for the stated purpose, and where do you tell operators it does not generalize?",
        "observe": "Review eval sets for leakage from training. For generative systems, inspect groundedness / hallucination metrics against the retrieval corpus, not only chatbot preference scores.",
        "evidence": [
            "Evaluation report with datasets, metrics, dates, and owners",
            "Documented known failure modes and operating limits",
            "Sign-off that residual error is within risk tolerance",
        ],
        "test": "Re-perform or inspect a sample of evaluation cases. Confirm metrics match the intended purpose (e.g., credit default vs BLEU).",
    },
    {
        "id": "PROC-MEASURE-2.7",
        "primary": "NIST-MEASURE-2.7",
        "title": "Security and resilience evaluation",
        "target_roles": ["Application security", "AI engineer"],
        "inquiry": "Which adversarial tests (prompt injection, data exfiltration, tool abuse) were run against this build, and who triaged the results?",
        "observe": "Review red-team or eval-harness output. Confirm findings were closed or risk-accepted with an owner.",
        "evidence": [
            "Security test plan and results for the current production version",
            "Guardrail / filter configuration (input and output)",
            "Incident or bug tickets from failed adversarial tests",
        ],
        "test": "Map tests to OWASP LLM Top 10 2025 entries that apply to this architecture. Identify untested categories.",
    },
    {
        "id": "PROC-MEASURE-2.10",
        "primary": "NIST-MEASURE-2.10",
        "title": "Privacy risk of prompts, logs, and retrieval",
        "target_roles": ["Privacy engineer", "Data protection officer", "Platform engineer"],
        "inquiry": "Where do prompts, completions, embeddings, and evaluator traces live, for how long, and who can replay them?",
        "observe": "Inspect log stores, vendor training-use settings, and retention jobs. Confirm production is not on a consumer endpoint that reserves training rights.",
        "evidence": [
            "Data-flow diagram for prompts, embeddings, logs, and fine-tune sets",
            "Retention / TTL configuration and access-control lists",
            "Vendor data-use setting evidence (enterprise opt-out / no-training)",
        ],
        "test": "Trace one customer utterance from UI to storage. Confirm deletion/TTL and access on a sample record.",
    },
    {
        "id": "PROC-MEASURE-2.11",
        "primary": "NIST-MEASURE-2.11",
        "title": "Fairness and bias evaluation",
        "target_roles": ["Model risk / data science", "Legal (discrimination)", "Product"],
        "inquiry": "For this intended purpose, which groups did you test, which metrics, and what threshold would block release?",
        "observe": "Do not accept a generic 'we use a fair model' statement. Require slice metrics or a documented reason that quantitative fairness measurement is not applicable, per MEASURE 1.1 (unmeasured characteristics must be documented).",
        "evidence": [
            "Bias / fairness test report tied to the intended purpose",
            "Definition of protected or sensitive attributes used (or legal basis for not processing them)",
            "Mitigations and residual-risk acceptance",
        ],
        "test": "If Annex III employment, credit, or education applies, treat this as a key control. Sample whether production monitoring continues slice metrics.",
    },
    {
        "id": "PROC-MANAGE-2.4",
        "primary": "NIST-MANAGE-2.4",
        "title": "Disengage, override, and deactivation",
        "target_roles": ["SRE / platform", "Security operations", "Product owner"],
        "inquiry": "Show me how you disable this system or a single tenant within an agreed time, including revoke of model API keys and agent tool credentials.",
        "observe": "Table-top or live kill-switch. Confirm it covers orchestrator, tools, and scheduled jobs, not only the chat UI.",
        "evidence": [
            "Documented deactivation / rollback procedure with RTO",
            "Evidence of a tested disable (ticket, game-day, or change record)",
            "Key and credential revocation path (IdP, API gateway)",
        ],
        "test": "Inspect last test of deactivation. If never tested, raise as a design gap against MANAGE 2.4 and, if high-risk, EU Art. 14 stop-button language.",
    },
    {
        "id": "PROC-MANAGE-3.2",
        "primary": "NIST-MANAGE-3.2",
        "title": "Monitoring of pre-trained and vendor models",
        "target_roles": ["MLOps", "Vendor manager"],
        "inquiry": "How do you learn that the vendor changed the model, the system prompt, or the safety layer under your deployment?",
        "observe": "Check for pinned model versions vs floating 'latest'. Review changelog subscription and regression evals on vendor updates.",
        "evidence": [
            "Pinned model version IDs in production config",
            "Vendor change-notification process",
            "Regression evaluation after the last vendor update",
        ],
        "test": "Compare production model identifier to the last approved version in change control.",
    },
    {
        "id": "PROC-MANAGE-4.1",
        "primary": "NIST-MANAGE-4.1",
        "title": "Post-deployment monitoring, appeals, and incidents",
        "target_roles": ["Operations", "Risk", "Customer support"],
        "inquiry": "Where do users contest an output, and how does that feed evaluation and incident response?",
        "observe": "Follow one complaint or override into the monitoring backlog. Confirm drift, toxicity, and tool-error metrics exist for genAI, not only classic ML PSI.",
        "evidence": [
            "Post-deployment monitoring plan and dashboards",
            "User appeal / feedback channel",
            "Incident response playbook covering AI-specific events",
        ],
        "test": "Sample two production incidents or complaints and trace to a logged event and a documented response.",
    },
    {
        "id": "PROC-EU-ART-9",
        "primary": "EU-ART-9",
        "title": "High-risk risk-management system (Art. 9)",
        "target_roles": ["Provider quality / risk", "AI product owner"],
        "inquiry": "Show the living Art. 9 file for this system: foreseeable misuse, residual risk, and measures tied to post-market data.",
        "observe": "The file should be iterative (versions), not a one-time DPIA copy-paste. Check reasonably foreseeable misuse (jailbreak, over-reliance, wrong population).",
        "evidence": [
            "Risk-management system documentation for the system lifecycle",
            "Register of known and reasonably foreseeable risks",
            "Link from post-market monitoring data into risk updates",
        ],
        "test": "Pick one residual risk. Trace identification → measure → owner → residual rating → monitoring metric.",
    },
    {
        "id": "PROC-EU-ART-10",
        "primary": "EU-ART-10",
        "title": "Training, validation, and test data governance (Art. 10)",
        "target_roles": ["Data science lead", "Data protection"],
        "inquiry": "For each training/validation/test set: origin, representativeness versus intended purpose, known gaps, and bias examination.",
        "observe": "If the team only uses a third-party foundation model, Art. 10 still matters for fine-tunes, RAG corpora, and evaluator sets the provider controls.",
        "evidence": [
            "Dataset inventory with intended-purpose alignment notes",
            "Bias/quality examination records",
            "Data-protection measures for personal data in those sets",
        ],
        "test": "Sample one dataset. Confirm documented provenance and a quality/bias check dated before the last training or index build.",
    },
    {
        "id": "PROC-EU-ART-11",
        "primary": "EU-ART-11",
        "title": "Annex IV technical documentation",
        "target_roles": ["Provider compliance", "Engineering documentation owner"],
        "inquiry": "Walk through the Annex IV pack: intended purpose, design specifications, data, TEVV, cybersecurity, and human oversight.",
        "observe": "Confirm the pack matches the running system version (commit, model ID, prompt version).",
        "evidence": [
            "Technical documentation mapped to Annex IV headings",
            "Version identifier that matches production",
            "Instructions for use provided to deployers (Art. 13)",
        ],
        "test": "Tick Annex IV headings against the file. Record missing headings as exceptions. Do not invent content.",
    },
    {
        "id": "PROC-EU-ART-14",
        "primary": "EU-ART-14",
        "title": "Human oversight operability (Art. 14)",
        "target_roles": ["Deployer operations", "Provider UX/safety"],
        "inquiry": "How does an overseer interpret output, ignore it, and interrupt the system? How do you reduce automation bias?",
        "observe": "Live demo of stop/override. Check whether the UI discloses confidence/limits or presents output as authoritative fact.",
        "evidence": [
            "Oversight design in technical documentation",
            "Deployer instructions describing oversight measures",
            "Training material on automation bias for overseers",
        ],
        "test": "Execute (or review recording of) interrupt and override. Confirm logs capture the human action (Art. 12).",
    },
    {
        "id": "PROC-EU-ART-15",
        "primary": "EU-ART-15",
        "title": "Accuracy, robustness, and cybersecurity (Art. 15)",
        "target_roles": ["ML engineer", "Security"],
        "inquiry": "Which accuracy metrics are declared to deployers, and which robustness tests cover data poisoning and adversarial inputs?",
        "observe": "Instructions for use should declare metrics (Art. 15). Compare declared metrics to actual eval reports.",
        "evidence": [
            "Declared accuracy metrics in instructions for use",
            "Robustness / adversarial evaluation results",
            "Cybersecurity measures for the AI pipeline (incl. poisoning and adversarial examples)",
        ],
        "test": "Match declared metrics to the latest evaluation. Inspect one adversarial test case and its disposition.",
    },
    {
        "id": "PROC-EU-ART-26",
        "primary": "EU-ART-26",
        "title": "Deployer obligations walkthrough (Art. 26)",
        "target_roles": ["Deployer management", "IT operations", "HR (if workplace use)"],
        "inquiry": "Who is assigned oversight, how do you monitor operation against the instructions for use, and where are logs retained (at least six months if under your control)?",
        "observe": "For workplace systems, check worker information. For credit/insurance/public bodies, check FRIA (Art. 27) separately.",
        "evidence": [
            "Record of assigned overseers and their competence",
            "Operating procedure aligned to provider instructions for use",
            "Log-retention configuration (≥ 6 months where Art. 26 applies and logs are under deployer control)",
            "Worker notification evidence if used in the workplace",
        ],
        "test": "Sample log retention and one monitoring exception. Confirm reporting path to the provider for serious incidents.",
    },
    {
        "id": "PROC-EU-ART-27",
        "primary": "EU-ART-27",
        "title": "Fundamental rights impact assessment (Art. 27)",
        "target_roles": ["Deployer public-sector / essential-services owner", "Legal"],
        "inquiry": "Was an Art. 27 FRIA required, who performed it, and how did it change deployment conditions?",
        "observe": "Confirm whether the deployer is a public body, a private provider of public services, or a deployer of Annex III 5(b)/(c). Critical infrastructure (Annex III(2)) is excluded from this FRIA duty.",
        "evidence": [
            "FRIA document (or documented determination that Art. 27 does not apply)",
            "Notification to the market surveillance authority where required",
            "Mitigations feeding the deployer operating procedure",
        ],
        "test": "Check actor type and Annex III paragraph against Art. 27 scope. Do not demand a FRIA from in-scope-excluded deployers.",
    },
    {
        "id": "PROC-EU-ART-50",
        "primary": "EU-ART-50",
        "title": "User-facing AI and synthetic-content disclosure",
        "target_roles": ["Product", "Communications", "Engineering"],
        "inquiry": "How is a person told they are interacting with AI, and how is synthetic media marked in a machine-readable way?",
        "observe": "Chat UI, email agents, and generated PDFs. Check watermarking/manifests for media, not only a footer disclaimer.",
        "evidence": [
            "UI/UX evidence of AI interaction notice",
            "Technical marking of synthetic content (where Art. 50(2) applies)",
            "Deep-fake or emotion-recognition disclosure procedure if those systems are in use",
        ],
        "test": "Use the system as a new user. Record whether the AI nature is disclosed before reliance on output.",
    },
    {
        "id": "PROC-EU-ART-53",
        "primary": "EU-ART-53",
        "title": "GPAI provider documentation and training-content summary",
        "target_roles": ["Foundation-model provider compliance", "Research engineering"],
        "inquiry": "Show the Art. 53 technical documentation, downstream-provider information, copyright policy, and public training-content summary.",
        "observe": "If claiming open-source reduced duties, test whether weights, architecture, and usage information are actually public and whether the model is systemic-risk.",
        "evidence": [
            "GPAI technical documentation",
            "Downstream information pack",
            "Copyright-compliance policy",
            "Published training-content summary",
        ],
        "test": "Tick Art. 53 items. If systemic-risk indicators exist, continue to Art. 55 procedures.",
    },
    {
        "id": "PROC-SR117-VAL",
        "primary": "US-SR117-VAL",
        "title": "Independent model validation (SR 11-7)",
        "target_roles": ["Independent model validation", "Model owner", "Internal audit"],
        "inquiry": "Who validated this model, how are they independent, and which of conceptual soundness, ongoing monitoring, and outcomes analysis are complete?",
        "observe": "Validator reporting line, last validation memo, limitations, and restrictions on use. Chatbots used as decision models still need a documented model definition.",
        "evidence": [
            "Independent validation report",
            "Model inventory record and risk tier",
            "Ongoing monitoring / back-testing evidence",
            "Limitations and restrictions communicated to users",
        ],
        "test": "Confirm independence (no developer self-validation as the sole line). Tick the three validation elements from SR 11-7.",
    },
    {
        "id": "PROC-OWASP-LLM01",
        "primary": "OWASP-LLM01",
        "title": "Prompt injection (direct and indirect)",
        "target_roles": ["Lead LLM engineer", "AppSec"],
        "inquiry": "How do you separate untrusted retrieved or tool content from developer instructions, and what tests prove the boundary holds?",
        "observe": "Live prompt construction. Look for delimiters, privilege reduction, and tool-call confirmation. For RAG, inspect a document containing instruction-like text.",
        "evidence": [
            "Prompt-template and orchestration code showing instruction/data separation",
            "Adversarial test results for direct and indirect injection",
            "Tool-gateway policy that does not blindly execute model-proposed actions",
        ],
        "test": "Review one indirect-injection test using retrieved content. Confirm the tool layer does not treat model text as authorization.",
    },
    {
        "id": "PROC-OWASP-LLM06",
        "primary": "OWASP-LLM06",
        "title": "Excessive agency / tool authorization",
        "target_roles": ["Agent platform architect", "IAM"],
        "inquiry": "Which tools can the agent invoke, under whose identity, and what actions require step-up approval?",
        "observe": "Tool manifest (MCP or equivalent). Attempt a write action under a read-only user. Confirm identity propagation vs a shared superuser token.",
        "evidence": [
            "Tool allowlist / schema with least privilege",
            "End-user identity propagation design",
            "Logs of blocked tool calls",
        ],
        "test": "Map each production tool to a business-justified permission. Fail if a general-purpose code-exec or payment tool is enabled without dual control.",
    },
    {
        "id": "PROC-OWASP-LLM08",
        "primary": "OWASP-LLM08",
        "title": "Vector store authorization and poisoning",
        "target_roles": ["RAG / search engineer", "Data owner"],
        "inquiry": "Does retrieval enforce the requesting user's entitlements, and how is corpus integrity controlled?",
        "observe": "Query the index as a low-privilege user. Inspect ingestion pipeline for access control on source documents and for poisoning tests.",
        "evidence": [
            "Document-level ACL enforcement at retrieval time (not only at UI)",
            "Ingestion provenance and change control for the corpus",
            "Tests for embedding inversion / cross-tenant retrieval if multi-tenant",
        ],
        "test": "Two-user retrieval test: user A must not receive user B documents. Record queries and hits.",
    },
    {
        "id": "PROC-ISO-A.7.5",
        "primary": "ISO-A.7.5",
        "title": "Data provenance (ISO/IEC 42001 A.7.5) — title-level procedure",
        "target_roles": ["Data engineering", "AIMS owner"],
        "inquiry": "How do you reconstruct where training, RAG, and evaluation data came from and how they were transformed?",
        "observe": "Lineage store or equivalent. This procedure tests the public control title; confirm authentic ISO text in the purchased standard.",
        "evidence": [
            "Dataset lineage records (source, transformations, versions)",
            "Link from model version to dataset version",
        ],
        "test": "Pick the production model or index. Reconstruct upstream data versions from records alone.",
    },
]


def for_primary(primary_id: str) -> dict | None:
    for p in PROCEDURES:
        if p["primary"] == primary_id:
            return p
    return None
