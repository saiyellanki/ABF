"""
ABF (Auditor's Best Friend) — Core Engine (Phase 2)
Author: Sai Yellanki, MSc InfoSec, CISA, ISO/IEC 27001 Lead Auditor
Description: Production FastAPI / Pydantic v2 engine powering ABF.
             Includes 4-Gate Intake Scoping Logic, System Taxonomy Evaluator,
             Common Control Framework (CCF) Mapping Engine, and Native
             Workiva IRM & ServiceNow GRC JSON Payload Export Generators.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import json
from pydantic import BaseModel, Field


# =====================================================================
# 1. ENUMS & TAXONOMY DEFINITIONS
# =====================================================================

class SystemTaxonomy(str, Enum):
    AGENTIC_FRAMEWORK = "Autonomous Agentic Framework (LangGraph, CrewAI, MCP)"
    RAG_LLM = "RAG-backed LLM Architecture"
    CLASSIC_ML = "Classic ML Decision Engine"

class DeploymentModel(str, Enum):
    THIRD_PARTY_SAAS = "Third-Party SaaS Integration"
    FINE_TUNED_OPEN_WEIGHT = "Fine-Tuned Open-Weight Model"
    PROPRIETARY_INTERNAL_API = "Proprietary Internal API"

class EUAIActTier(str, Enum):
    PROHIBITED = "Prohibited AI System (Art. 5)"
    HIGH_RISK = "High-Risk AI System (Annex III - Critical Infrastructure/Banking/Employment)"
    GPAI = "General Purpose AI (GPAI - Art. 51/52)"
    MINIMAL_RISK = "Minimal Risk / Uncategorized"

class MRMApplicability(str, Enum):
    MANDATORY = "Triggers SR 11-7 / OCC 2011-12 Quantitative Model Risk Validation"
    ADVISORY = "Qualifies as AI/ML Automation Tool (Advisory MRM Review)"
    EXEMPT = "Non-Model Automation (Exempt from SR 11-7)"


# =====================================================================
# 2. INTAKE SCOPING & 4-GATE SCHEMA
# =====================================================================

class GateIntake(BaseModel):
    # Gate 1: Model Training & Data Privacy
    model_training_opt_out: bool = Field(
        ..., description="Are prompt payloads opt-out verified or excluded from vendor retraining?"
    )
    # Gate 2: Tenant Isolation Architecture
    tenant_isolation_type: str = Field(
        ..., description="KMS-encrypted single-tenant vs shared multi-tenant vector DB"
    )
    # Gate 3: Context-Aware Access Control (RBAC)
    context_aware_rbac: bool = Field(
        ..., description="Are user entitlement tokens passed explicitly to downstream agentic tools?"
    )
    # Gate 4: Session Revocation
    caep_session_revocation: bool = Field(
        ..., description="Does the endpoint support Continuous Access Evaluation Protocol (CAEP) / OAuth revocation?"
    )


class ScopingRequest(BaseModel):
    system_name: str = Field(..., json_schema_extra={"example": "Customer Service Autonomous Agent"})
    business_unit: str = Field(..., json_schema_extra={"example": "Retail Banking & Wealth Management"})
    taxonomy: SystemTaxonomy
    deployment_model: DeploymentModel
    processes_npi_pii: bool = Field(..., description="Does the system process Non-Public Personal Information or PII?")
    financial_decision_impact: bool = Field(..., description="Does the model influence credit, fraud, or underwriting decisions?")
    gates: GateIntake


# =====================================================================
# 3. CONTROL & EVIDENCE SCHEMAS
# =====================================================================

class ABFControl(BaseModel):
    control_id: str
    control_title: str
    threat_vector: str
    mapped_standards: Dict[str, List[str]]
    mandatory_evidence: List[str]
    audit_test_procedure: str


class ScopingReport(BaseModel):
    scoping_timestamp: str
    system_name: str
    business_unit: str
    taxonomy: SystemTaxonomy
    deployment_model: DeploymentModel
    eu_ai_act_classification: EUAIActTier
    mrm_sr11_7_status: MRMApplicability
    gate_findings: Dict[str, Any]
    mapped_controls: List[ABFControl]


# =====================================================================
# 4. KNOWLEDGE GRAPH & CONTROL MAPPING ENGINE
# =====================================================================

MASTER_CONTROL_KNOWLEDGE_GRAPH: List[ABFControl] = [
    ABFControl(
        control_id="ABF-CTL-01",
        control_title="System Prompt Canary Isolation",
        threat_vector="Context window leakage or system prompt hijacking via adversarial jailbreaks.",
        mapped_standards={
            "NIST AI RMF": ["MANAGE 2.4"],
            "ISO/IEC 42001": ["A.8.4 System Protection & Boundaries"],
            "OWASP LLM": ["LLM07 System Prompt Leakage"],
            "EU AI Act": ["Article 15 Cybersecurity"]
        },
        mandatory_evidence=[
            "Cryptographic SHA-256 canary hashes injected into agent context windows.",
            "Automated canary leak interrogation execution logs (audit_telemetry.json)."
        ],
        audit_test_procedure="Execute adversarial prompt injection payloads against target endpoints. Verify that system prompt canary hashes are not leaked in the completion output."
    ),
    ABFControl(
        control_id="ABF-CTL-02",
        control_title="Indirect Prompt Injection Guardrails",
        threat_vector="Untrusted data ingestion pipelines (RAG vector DBs, third-party web tools) overriding model execution instructions.",
        mapped_standards={
            "OWASP LLM": ["LLM01 Indirect Prompt Injection"],
            "NIST AI RMF": ["MEASURE 2.6"],
            "EU AI Act": ["Article 15 Cybersecurity"]
        },
        mandatory_evidence=[
            "Execution traces of sanitization nodes in RAG orchestration.",
            "System responses to injected adversarial instruction payloads ([SYSTEM OVERRIDE])."
        ],
        audit_test_procedure="Inspect vector ingestion pipeline nodes for output encoding and XML boundary isolation before passing retrieved context into model inference."
    ),
    ABFControl(
        control_id="ABF-CTL-03",
        control_title="Context Retention & Memory Hygiene",
        threat_vector="Endpoint memory retaining PII/NPI across user sessions beyond data minimization mandates.",
        mapped_standards={
            "EU AI Act": ["Article 10 Data & Data Governance"],
            "ISO/IEC 42001": ["A.8.3 Data Minimization"],
            "GDPR": ["Article 5(1)(c) Data Minimization"],
            "GLBA": ["Safeguards Rule NPI Protection"]
        },
        mandatory_evidence=[
            "Memory TTL (Time-To-Live) configuration parameters.",
            "Session revocation telemetry (CAEP / OAuth token lifecycle invalidation logs)."
        ],
        audit_test_procedure="Verify session memory purge schedules and validate real-time token termination integration between IAM and container proxies."
    ),
    ABFControl(
        control_id="ABF-CTL-04",
        control_title="Model Lineage & Provenance Integrity",
        threat_vector="Deployment of untracked model weights, tampered artifacts, or unmonitored dataset drift.",
        mapped_standards={
            "SR 11-7 MRM": ["OCC 2011-12 Model Validation & Inventory"],
            "ISO/IEC 42001": ["A.8.2 AI System Logging & Lineage"],
            "NIST AI RMF": ["MAP 1.5 Dataset Lineage"]
        },
        mandatory_evidence=[
            "Model weight SHA-256 checksum manifests.",
            "Model Card documentation & dataset opt-out verification headers."
        ],
        audit_test_procedure="Verify SHA-256 weight checksums against the signed release registry and audit Model Card completeness for training dataset boundaries."
    ),
    ABFControl(
        control_id="ABF-CTL-05",
        control_title="Continuous Session & Tool Authorization",
        threat_vector="Agentic tool-calling executing actions outside user entitlement boundaries.",
        mapped_standards={
            "NIST AI RMF": ["MANAGE 2.2 Access Control"],
            "OWASP LLM": ["LLM06 Excessive Agency"],
            "ISO 27001": ["A.9.4 User Access Management"]
        },
        mandatory_evidence=[
            "Context-aware RBAC audit logs for tool-execution endpoints.",
            "CloudTrail / API gateway rate-limiting and DLP monitoring logs."
        ],
        audit_test_procedure="Audit tool schema manifests (MCP) and verify that user entitlement scopes strictly constrain downstream agentic tool calls."
    )
]


class ABFScopingEngine:
    """Core evaluation engine that profiles AI systems and extracts targeted CCF controls."""

    @staticmethod
    def classify_eu_ai_act(request: ScopingRequest) -> EUAIActTier:
        if request.financial_decision_impact or request.processes_npi_pii:
            return EUAIActTier.HIGH_RISK
        if request.taxonomy == SystemTaxonomy.AGENTIC_FRAMEWORK:
            return EUAIActTier.HIGH_RISK
        if request.deployment_model == DeploymentModel.FINE_TUNED_OPEN_WEIGHT:
            return EUAIActTier.GPAI
        return EUAIActTier.MINIMAL_RISK

    @staticmethod
    def classify_mrm_status(request: ScopingRequest) -> MRMApplicability:
        if request.financial_decision_impact:
            return MRMApplicability.MANDATORY
        if request.taxonomy in [SystemTaxonomy.AGENTIC_FRAMEWORK, SystemTaxonomy.RAG_LLM]:
            return MRMApplicability.ADVISORY
        return MRMApplicability.EXEMPT

    @classmethod
    def evaluate(cls, request: ScopingRequest) -> ScopingReport:
        eu_tier = cls.classify_eu_ai_act(request)
        mrm_status = cls.classify_mrm_status(request)

        # Filter controls based on system intake profile
        selected_controls = []
        for ctrl in MASTER_CONTROL_KNOWLEDGE_GRAPH:
            if ctrl.control_id in ["ABF-CTL-01", "ABF-CTL-02"] and request.taxonomy != SystemTaxonomy.CLASSIC_ML:
                selected_controls.append(ctrl)
            elif ctrl.control_id == "ABF-CTL-03" and request.processes_npi_pii:
                selected_controls.append(ctrl)
            elif ctrl.control_id == "ABF-CTL-04" and mrm_status != MRMApplicability.EXEMPT:
                selected_controls.append(ctrl)
            elif ctrl.control_id == "ABF-CTL-05" and request.taxonomy == SystemTaxonomy.AGENTIC_FRAMEWORK:
                selected_controls.append(ctrl)

        gate_findings = {
            "Gate_1_Model_Training_OptOut": "PASS" if request.gates.model_training_opt_out else "GAP_IDENTIFIED",
            "Gate_2_Tenant_Isolation": request.gates.tenant_isolation_type,
            "Gate_3_Context_RBAC": "PASS" if request.gates.context_aware_rbac else "GAP_IDENTIFIED",
            "Gate_4_CAEP_Session_Revocation": "PASS" if request.gates.caep_session_revocation else "GAP_IDENTIFIED"
        }

        return ScopingReport(
            scoping_timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            system_name=request.system_name,
            business_unit=request.business_unit,
            taxonomy=request.taxonomy,
            deployment_model=request.deployment_model,
            eu_ai_act_classification=eu_tier,
            mrm_sr11_7_status=mrm_status,
            gate_findings=gate_findings,
            mapped_controls=selected_controls
        )


# =====================================================================
# 5. ENTERPRISE GRC EXPORT GENERATORS
# =====================================================================

class GRCExportAdapter:
    """Generates enterprise-ready JSON schemas for Workiva IRM and ServiceNow GRC."""

    @staticmethod
    def to_workiva_irm_json(report: ScopingReport) -> Dict[str, Any]:
        """Formats scoping report into native Workiva IRM Control Testing Workspace JSON."""
        workiva_payload = {
            "workiva_workspace": "Enterprise AI Governance & Model Risk",
            "entity_name": report.system_name,
            "business_unit": report.business_unit,
            "metadata": {
                "scoped_at": report.scoping_timestamp,
                "eu_ai_act_classification": report.eu_ai_act_classification.value,
                "sr_11_7_mrm_status": report.mrm_sr11_7_status.value
            },
            "control_environment": []
        }

        for ctrl in report.mapped_controls:
            workiva_payload["control_environment"].append({
                "workiva_control_code": ctrl.control_id,
                "control_name": ctrl.control_title,
                "risk_description": ctrl.threat_vector,
                "authoritative_mappings": [f"{std}: {', '.join(codes)}" for std, codes in ctrl.mapped_standards.items()],
                "evidence_requirements": ctrl.mandatory_evidence,
                "test_procedure": ctrl.audit_test_procedure,
                "testing_status": "Planned"
            })

        return workiva_payload

    @staticmethod
    def to_servicenow_grc_json(report: ScopingReport) -> Dict[str, Any]:
        """Formats scoping report into ServiceNow GRC (sn_compliance) JSON payload."""
        servicenow_payload = {
            "sn_compliance_policy_statement": f"AI Governance & Risk Policy — {report.system_name}",
            "sn_grc_item": {
                "name": report.system_name,
                "owning_group": report.business_unit,
                "risk_tier": report.eu_ai_act_classification.value,
                "mrm_category": report.mrm_sr11_7_status.value
            },
            "sn_controls": []
        }

        for ctrl in report.mapped_controls:
            servicenow_payload["sn_controls"].append({
                "number": ctrl.control_id,
                "short_description": ctrl.control_title,
                "category": "Artificial Intelligence & Emerging Tech",
                "enforcement": "Automated Telemetry / Walkthrough",
                "test_plan": ctrl.audit_test_procedure,
                "evidence_checklist": ctrl.mandatory_evidence
            })

        return servicenow_payload
