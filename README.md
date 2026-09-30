ABF
ABF - Auditor's Best Friend: The Enterprise Scoping, Technical Assurance &amp; Control Extraction Workbench for AI Risk &amp; IT Audit

ABF (Auditor's Best Friend) is an interactive, professional-grade web application engineered to bridge the gap between static GRC compliance checklists and live technical telemetry. Designed specifically for 2LoD Risk, 3LoD IT Audit, and Model Risk Officers, ABF guides auditors through an adaptive scoping wizard, dynamically generates authoritative control frameworks, provides step-by-step technical walkthrough scripts for engineering teams, and exports audit evidence directly into enterprise GRC platforms like Workiva IRM and ServiceNow.

Application Workflow & Data Architecture
┌───────────────────────────┐      ┌───────────────────────────┐      ┌───────────────────────────┐
│  1. Interactive Scoping   │ ───► │  2. Control & Evidence    │ ───► │  3. Engineer Interrogation│
│     Questionnaire Wizard  │      │     Extraction Engine     │      │     & Walkthrough Guide   │
└───────────────────────────┘      └───────────────────────────┘      └─────────────┬─────────────┘
                                                                                    │
                                                                                    ▼
┌───────────────────────────┐      ┌───────────────────────────┐      ┌───────────────────────────┐
│  5. Integrated Telemetry  │ ◄─── │  4. Enterprise GRC &      │ ◄─── │  3. Model Risk & Safety   │
│     & Evidence Collector  │      │     Audit Export Center   │      │     Testing Sandbox       │
└───────────────────────────┘      └───────────────────────────┘      └───────────────────────────┘

Core Feature Modules
1. Adaptive Scoping Questionnaire WizardAn intake wizard that profiles the target AI system, classifies regulatory exposure, and establishes the audit boundary before controls are mapped.
2. System Taxonomy & Deployment Architecture:Categorizes the system: Autonomous agentic framework (LangGraph, CrewAI, MCP), RAG-backed LLM, or classic ML decision model.
3. Evaluates deployment model: Third-party SaaS, fine-tuned open-weight model, or proprietary internal API.
4. Regulatory & Risk Classification Engine:EU AI Act Classification: Automatically categorizes the system as Prohibited, High-Risk (Annex III critical infrastructure/employment/banking), or General Purpose AI (GPAI).
5. SR 11-7 / Model Risk Management (MRM): Determines whether the application triggers quantitative validation mandates under SR 11-7.
6. Technical Boundary Evaluation (4-Gate Intake):Model Training & Data Privacy: Are prompt payloads opt-out verified or used for vendor retraining?
7. Tenant Isolation Architecture: Multi-tenant shared vector DB vs. KMS-encrypted single-tenant instance.
8. Context-Aware Access Control (RBAC): How user privileges and entitlement tokens pass to downstream agentic tools.
9. Session Revocation: Support for Continuous Architecture Event Protocol (CAEP) and token lifecycle termination.

Standard-Mapped Control & Evidence Extraction Engine
Once the audit profile is established, ABF queries its authoritative Knowledge Graph to generate a unified Common Control Framework (CCF) grounded in ISO/IEC 42001, NIST AI RMF 1.0 / NIST AI 600-1, EU AI Act, OWASP LLM Top 10, and SR 11-7.


                                  ┌───────────────────────────────┐
                                  │      NIST AI RMF 1.0 &        │
                                  │       NIST AI 600-1           │
                                  └───────────────┬───────────────┘
                                                  │
┌───────────────────────────────┐                 ▼                 ┌───────────────────────────────┐
│        EU AI Act              │ ──────►  [  ABF CONTROL  ] ◄───── │       ISO/IEC 42001           │
│   (Art. 10, 14, 15, etc.)     │          [  KNOWLEDGE    ]        │   (AIMS Controls A.8/A.9)     │
└───────────────────────────────┘          [    GRAPH      ]        └───────────────────────────────┘
                                                  ▲
                                                  │
                                  ┌───────────────┴───────────────┐
                                  │    OWASP LLM Top 10 &         │
                                  │    SR 11-7 Model Risk         │
                                  └───────────────────────────────┘


Engineering Walkthrough & Interview Script Generator
To assist auditors during technical walkthroughs with AI/ML engineers and quantitative model developers, ABF converts complex AI safety concepts into clear, structured interview scripts.

Walkthrough Guide: Indirect Prompt Injection in RAG OrchestrationTarget Role: Lead AI/ML Data Engineer
1. Architectural Inquiry:"How does the RAG ingestion pipeline separate untrusted retrieval context from system instructions before passing vectors into the prompt context window?"   
2. Technical Verification Step: Have the engineer demonstrate live context construction. Inspect whether retrieved vector metadata undergoes strict output encoding or prompt isolation (e.g., using XML tags or boundary markers) prior to model inference.
3. Evidence Request: Request sanitized execution traces showing how the RAG pipeline handles a retrieved document containing text like "[SYSTEM OVERRIDE: Ignore prior instructions]".

Enterprise GRC & Evidence Export CenterABF enables auditors to export scoped control frameworks and evidence manifests directly into enterprise formats:
GRC System Integrations: Native export schemas ready for direct ingestion into Workiva IRM, ServiceNow GRC, and Archer.   
Signed Telemetry Reports: Export cryptographically signed JSON (audit_telemetry.json) or Markdown/PDF executive summaries for audit committees.   
Audit Workpapers: Pre-formatted Excel/CSV workpapers complete with Control ID, Description, Mapped Standards, Mandatory Evidence Checklist, and Test Procedure.  

Technical Stack & Architecture
Frontend UI: Next.js (TypeScript), Tailwind CSS, Shadcn UI, React Flow (for visualizing agentic workflow & RAG data-flow diagrams).
Backend API: FastAPI (Python 3.11+), Pydantic v2 (for strict schema validation across standard mappings).
Database & Knowledge Graph: PostgreSQL (storing standard control mappings across ISO 42001, NIST, EU AI Act) with SQLite support for offline local auditor desktop use.   
Evidence Validation Utilities: Integrated SHA-256 model weight checksum calculator, API prompt canary inspector, and Workiva/ServiceNow-compatible payload generators.   

Why ABF is an "Auditor's Best Friend"
Telemetry Over Checklists: Focuses on verifying code-level evidence (SHA-256 checksums, CAEP logs, canary hashes) rather than relying solely on policy documents.   
Eliminates Duplicate Audit Effort: Uses a Common Control Framework (CCF) approach, satisfying multiple frameworks (NIST, ISO, EU AI Act) from a single evidence set.   
Translator for Auditors & Engineers: Translates complex ML concepts (Disparate Impact Ratio, RAG vector isolation, context retention limits) into structured, defensible audit procedures.   
100% Authoritative Sourcing: Every control and evidence requirement is explicitly mapped to published standards without subjective or ungrounded metrics.  
