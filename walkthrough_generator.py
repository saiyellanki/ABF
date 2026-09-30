"""
ABF (Auditor's Best Friend) — Walkthrough Script Generator (Phase 4)
Author: Sai Yellanki, MSc InfoSec, CISA, ISO/IEC 27001 Lead Auditor
Description: Command-line utility that generates role-specific, structured technical
             interview guides and verification steps for AI/ML Data Engineers,
             Model Risk Developers, and Security Architecture Teams.
"""

import json
import argparse
from typing import Dict, List, Any


WALKTHROUGH_SCRIPTS_DATABASE: Dict[str, Dict[str, Any]] = {
    "ABF-CTL-01": {
        "control_id": "ABF-CTL-01",
        "title": "System Prompt Canary Isolation",
        "target_role": "Lead LLM Application Developer / Prompt Engineer",
        "threat_vector": "Context window leakage or system prompt hijacking via adversarial jailbreaks.",
        "mapped_standards": ["NIST AI RMF MANAGE 2.4", "ISO/IEC 42001 A.8.4", "OWASP LLM07"],
        "interview_script": {
            "architectural_inquiry": (
                "How does the model orchestration layer isolate underlying system prompts, "
                "developer instructions, and internal canary tokens from user-supplied completion payloads?"
            ),
            "technical_verification_step": (
                "Request a live demonstration of prompt template construction. Verify whether "
                "system prompts are enforced via API-level system-role parameters rather than prepended "
                "user-string concatenation. Check if canary hashes are dynamically injected and monitored."
            ),
            "evidence_request_checklist": [
                "API system-role configuration code snippets from the model wrapper.",
                "Automated canary leak interrogation execution logs (e.g., audit_telemetry.json).",
                "CI/CD pipeline test runs evaluating system prompt isolation under adversarial jailbreaks."
            ]
        }
    },
    "ABF-CTL-02": {
        "control_id": "ABF-CTL-02",
        "title": "Indirect Prompt Injection Guardrails",
        "target_role": "Lead AI/ML Data Engineer / RAG Architect",
        "threat_vector": "Untrusted data ingestion pipelines (RAG vector DBs, third-party web tools) overriding model execution instructions.",
        "mapped_standards": ["OWASP LLM01", "NIST AI RMF MEASURE 2.6", "EU AI Act Art. 15"],
        "interview_script": {
            "architectural_inquiry": (
                "How does the RAG ingestion pipeline separate untrusted retrieval context from system "
                "instructions before passing retrieved vectors into the LLM prompt context window?"
            ),
            "technical_verification_step": (
                "Have the engineer demonstrate live context construction inside the RAG pipeline. "
                "Inspect whether retrieved vector metadata undergoes strict output encoding, XML boundary "
                "delimitation (<context>...</context>), or sanitization node filtering prior to model inference."
            ),
            "evidence_request_checklist": [
                "Sanitization node source code in the vector retrieval pipeline.",
                "Execution traces showing RAG pipeline handling documents containing adversarial text like '[SYSTEM OVERRIDE: Ignore prior instructions]'.",
                "Input/Output guardrail configuration files (e.g., NeMo Guardrails, Llama Guard)."
            ]
        }
    },
    "ABF-CTL-03": {
        "control_id": "ABF-CTL-03",
        "title": "Context Retention & Memory Hygiene",
        "target_role": "Principal Data Privacy Engineer / Backend Security Lead",
        "threat_vector": "Endpoint memory retaining PII/NPI across user sessions beyond data minimization mandates.",
        "mapped_standards": ["EU AI Act Art. 10", "ISO/IEC 42001 A.8.3", "GDPR Art. 5(1)(c)", "GLBA Safeguards"],
        "interview_script": {
            "architectural_inquiry": (
                "What is the exact data lifecycle and Time-To-Live (TTL) configuration for conversation memory, "
                "session state vector caches, and intermediate prompt logs containing Non-Public Personal Information (NPI)?"
            ),
            "technical_verification_step": (
                "Inspect Redis/vector DB TTL configurations and verify automated cache purge jobs. "
                "Validate that user session termination triggers real-time token invalidation and cache wipes via CAEP/OAuth hooks."
            ),
            "evidence_request_checklist": [
                "Vector store and Redis cache TTL policy configuration code.",
                "CAEP / OAuth token lifecycle event integration logs showing immediate session termination.",
                "DLP scan reports confirming zero residual PII/NPI in long-term model memory logs."
            ]
        }
    },
    "ABF-CTL-04": {
        "control_id": "ABF-CTL-04",
        "title": "Model Lineage & Provenance Integrity",
        "target_role": "Quantitative Model Developer / MLOps Lead",
        "threat_vector": "Deployment of untracked model weights, tampered artifacts, or unmonitored dataset drift.",
        "mapped_standards": ["SR 11-7 Model Risk Management", "ISO/IEC 42001 A.8.2", "NIST AI RMF MAP 1.5"],
        "interview_script": {
            "architectural_inquiry": (
                "How are model weight artifacts cryptographically verified prior to container deployment, "
                "and how is dataset provenance documented for SR 11-7 model risk inventory reviews?"
            ),
            "technical_verification_step": (
                "Request live SHA-256 checksum validation of staging vs production model weights. "
                "Review Model Card documentation for training dataset opt-out verification and challenger model baselines."
            ),
            "evidence_request_checklist": [
                "Cryptographic SHA-256 weight checksum manifests from the model registry.",
                "Completed Model Card including dataset opt-out headers and licensing boundaries.",
                "SR 11-7 Model Risk Management independent validation approval documentation."
            ]
        }
    },
    "ABF-CTL-05": {
        "control_id": "ABF-CTL-05",
        "title": "Continuous Session & Tool Authorization",
        "target_role": "Agentic Platform Architect / IAM Solutions Lead",
        "threat_vector": "Agentic tool-calling executing actions outside end-user entitlement boundaries.",
        "mapped_standards": ["NIST AI RMF MANAGE 2.2", "OWASP LLM06", "ISO 27001 A.9.4"],
        "interview_script": {
            "architectural_inquiry": (
                "How are end-user entitlement tokens passed to downstream agentic tool invocations (MCP/REST), "
                "and how do you prevent agents from executing actions under over-provisioned service account scopes?"
            ),
            "technical_verification_step": (
                "Audit Model Context Protocol (MCP) tool schema manifests. Observe a live agent execution "
                "attempting an unauthorized tool call (e.g., database write when given read-only role) and verify real-time interception."
            ),
            "evidence_request_checklist": [
                "MCP tool schema manifests defining explicit tool-calling boundaries.",
                "Context-aware RBAC enforcement logs showing end-user token propagation to tools.",
                "API Gateway / CloudTrail logs demonstrating rate-limiting and unauthorized action blocks."
            ]
        }
    }
}


def generate_walkthrough_guide(control_ids: List[str] = None) -> str:
    """Generates formatted Markdown walkthrough scripts for specified controls."""
    if not control_ids:
        control_ids = list(WALKTHROUGH_SCRIPTS_DATABASE.keys())

    output_lines = [
        "# ABF Technical Walkthrough & Interview Script Guide",
        "**Target Audience:** 2LoD Risk, 3LoD IT Audit, and Model Risk Officers conducting technical interviews with AI/ML Engineers.",
        "---"
    ]

    for cid in control_ids:
        data = WALKTHROUGH_SCRIPTS_DATABASE.get(cid)
        if not data:
            continue

        output_lines.extend([
            f"## 📋 {data['control_id']}: {data['title']}",
            f"**Target Auditee Role:** `{data['target_role']}`",
            f"**Threat Vector:** {data['threat_vector']}",
            f"**Mapped Standards:** {', '.join(data['mapped_standards'])}",
            "",
            "### 1. 💬 Architectural Inquiry (What to Ask):",
            f"> *\"{data['interview_script']['architectural_inquiry']}\"*",
            "",
            "### 2. 🔍 Technical Verification Step (What to Observe Live):",
            f"{data['interview_script']['technical_verification_step']}",
            "",
            "### 3. 📄 Evidence Request Checklist (What to Request):",
            "\n".join([f"- [ ] {item}" for item in data['interview_script']['evidence_request_checklist']]),
            "",
            "---"
        ])

    return "\n".join(output_lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ABF Walkthrough Script Generator")
    parser.add_argument("--control", type=str, help="Filter by specific control ID (e.g. ABF-CTL-02)")
    parser.add_argument("--export-json", action="store_true", help="Output raw JSON format")
    args = parser.parse_args()

    selected_ids = [args.control] if args.control else list(WALKTHROUGH_SCRIPTS_DATABASE.keys())

    if args.export_json:
        filtered = {k: v for k, v in WALKTHROUGH_SCRIPTS_DATABASE.items() if k in selected_ids}
        print(json.dumps(filtered, indent=2))
    else:
        print(generate_walkthrough_guide(selected_ids))
