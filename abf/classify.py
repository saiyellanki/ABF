"""Indicative screening engine.

This is not a legal determination. Each conclusion cites the rule applied.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


ANNEX_III_KEYS = [
    "annex_iii_1",
    "annex_iii_2",
    "annex_iii_3",
    "annex_iii_4",
    "annex_iii_5",
    "annex_iii_6",
    "annex_iii_7",
    "annex_iii_8",
]


@dataclass
class Finding:
    topic: str
    status: str
    summary: str
    rule: str
    citation: str
    source_url: str


@dataclass
class ScreeningResult:
    findings: list[Finding] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    applicable_ids: list[str] = field(default_factory=list)
    eu_high_risk: bool = False
    eu_possible_exception: bool = False
    eu_prohibited_indicative: bool = False
    gpai: bool = False
    gpai_systemic: bool = False
    sr117: bool = False
    art50: bool = False

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        return d


def _yes(answers: dict, key: str) -> bool:
    val = answers.get(key)
    if isinstance(val, list):
        return bool(val)
    return val in (True, "yes", "true", "YES")


def classify(answers: dict) -> ScreeningResult:
    """Return an indicative screening from scoping answers."""
    result = ScreeningResult()
    tags: set[str] = {"governance_baseline", "nist", "always_if_using_rmf", "system_specific"}

    role = answers.get("role") or "deployer"
    markets = set(answers.get("markets") or [])
    architecture = set(answers.get("architecture") or [])
    eu_market = "eu" in markets or _yes(answers, "output_used_in_eu")

    if role in ("provider", "both"):
        tags.add("eu_provider")
    if role in ("deployer", "both"):
        tags.add("eu_deployer")
    if role == "gpai_provider":
        tags.add("eu_gpai")
        result.gpai = True

    if architecture & {"llm_chat", "rag", "agentic"}:
        tags.update({"genai", "gai_profile", "owasp"})
    if "rag" in architecture:
        tags.add("rag")
    if "agentic" in architecture:
        tags.add("agentic")
    if "classic_ml" in architecture:
        tags.add("classic_ml")
    if "biometrics" in architecture:
        tags.add("biometrics")

    if _yes(answers, "third_party_model_or_api"):
        tags.add("third_party")
    if _yes(answers, "personal_data"):
        tags.add("personal_data")
    if _yes(answers, "automated_decision"):
        tags.add("human_oversight")

    # --- Article 5 ---
    prohibited_flags = answers.get("art5_practices") or []
    if prohibited_flags:
        result.eu_prohibited_indicative = True
        tags.add("eu_prohibited")
        result.findings.append(Finding(
            topic="EU AI Act — prohibited practices",
            status="Indicative: possible Article 5 issue",
            summary=(
                "One or more practices associated with Article 5 were indicated. "
                "Do not treat this as a legal finding. Counsel should compare the intended use "
                "to the authentic Article 5 list and its exceptions."
            ),
            rule="Art. 5 prohibits placing on the market, putting into service, or using listed practices.",
            citation="Regulation (EU) 2024/1689, Article 5",
            source_url="https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
        ))

    # --- Article 6 / Annex III ---
    annex = [k for k in ANNEX_III_KEYS if _yes(answers, k)]
    annex_i_product = _yes(answers, "annex_i_safety_component")
    profiles = _yes(answers, "profiles_natural_persons")
    exception_all = all(_yes(answers, k) for k in (
        "art63_narrow_procedural",
        "art63_improves_human",
        "art63_detects_patterns",
        "art63_preparatory",
    ))
    # Art 6(3) is OR of those four conditions, not AND. If ANY applies, exception MAY apply,
    # unless profiling. We ask the user which 6(3) conditions they believe apply.
    exception_any = any(_yes(answers, k) for k in (
        "art63_narrow_procedural",
        "art63_improves_human",
        "art63_detects_patterns",
        "art63_preparatory",
    ))

    if eu_market or annex or annex_i_product or _yes(answers, "eu_in_scope"):
        tags.add("eu")
        tags.add("eu_classification")

    if annex_i_product:
        result.eu_high_risk = True
        result.findings.append(Finding(
            topic="EU AI Act — high-risk (Article 6(1))",
            status="Indicative: high-risk if Annex I + third-party conformity assessment applies",
            summary=(
                "The engagement indicated the system is (or is a safety component of) a product "
                "covered by Annex I Union harmonisation legislation that requires third-party "
                "conformity assessment. Confirm both limbs of Article 6(1) against the product file."
            ),
            rule="Art. 6(1): safety component/product under Annex I AND third-party conformity assessment.",
            citation="Regulation (EU) 2024/1689, Article 6(1) and Annex I",
            source_url="https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
        ))

    if annex:
        labels = ", ".join(k.replace("annex_iii_", "Annex III(") + ")" for k in annex)
        if profiles:
            result.eu_high_risk = True
            result.findings.append(Finding(
                topic="EU AI Act — high-risk (Article 6(2) + profiling)",
                status="Indicative: high-risk (profiling removes the Art. 6(3) exception)",
                summary=(
                    f"Intended purpose appears to fall under {labels}. Article 6 provides that "
                    "Annex III systems that profile natural persons are always high-risk. "
                    "Handling personal data alone is not the test; the use-case list is."
                ),
                rule="Annex III systems that profile natural persons are high-risk; Art. 6(3) does not apply.",
                citation="Regulation (EU) 2024/1689, Article 6(2)–6(3) and Annex III",
                source_url="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3",
            ))
        elif exception_any:
            result.eu_possible_exception = True
            result.findings.append(Finding(
                topic="EU AI Act — possible Article 6(3) exception",
                status="Indicative: Annex III use case, but a 6(3) exception may apply",
                summary=(
                    f"Intended purpose appears to fall under {labels}, but one or more Art. 6(3) "
                    "conditions were indicated (narrow procedural task; improving a completed human "
                    "activity; detecting decision-making patterns without replacing human assessment; "
                    "or a purely preparatory task). The provider must document this assessment before "
                    "placing the system on the market or putting it into service. This tool does not "
                    "decide whether the exception is available."
                ),
                rule="Art. 6(3) exception is documented by the provider and is unavailable if the system profiles persons.",
                citation="Regulation (EU) 2024/1689, Article 6(3)",
                source_url="https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
            ))
        else:
            result.eu_high_risk = True
            result.findings.append(Finding(
                topic="EU AI Act — high-risk (Article 6(2))",
                status="Indicative: high-risk Annex III system",
                summary=(
                    f"Intended purpose appears to fall under {labels}. No Art. 6(3) exception was "
                    "indicated. Confirm the exact Annex III paragraph against the authentic text "
                    "and intended purpose documentation (Art. 11 / Annex IV)."
                ),
                rule="Art. 6(2): systems listed in Annex III are high-risk unless a documented 6(3) exception applies.",
                citation="Regulation (EU) 2024/1689, Article 6(2) and Annex III",
                source_url="https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3",
            ))
    elif eu_market and not annex_i_product:
        result.findings.append(Finding(
            topic="EU AI Act — not classified as Annex III high-risk on this intake",
            status="Indicative: no Annex III category selected",
            summary=(
                "No Annex III use case was selected. Personal data processing, use of a foundation "
                "model, or an agentic architecture does not by itself make a system high-risk. "
                "Revisit intended purpose with legal if the use case is close to Annex III "
                "(employment, credit, education, biometrics, essential services)."
            ),
            rule="High-risk classification is Art. 6 + Annex I or Annex III, not data sensitivity alone.",
            citation="Regulation (EU) 2024/1689, Article 6",
            source_url="https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
        ))

    if result.eu_high_risk:
        tags.update({"eu_high_risk", "human_oversight", "tevv", "security", "fairness"})
        if role in ("provider", "both"):
            tags.add("eu_provider")
        if role in ("deployer", "both"):
            tags.add("eu_deployer")
        if _yes(answers, "fria_role"):
            tags.add("fria")
        if any(k in annex for k in ("annex_iii_3", "annex_iii_4", "annex_iii_5")):
            tags.add("fairness")

    # Article 50
    if _yes(answers, "interacts_with_natural_persons") or _yes(answers, "synthetic_content") or _yes(answers, "deepfake"):
        result.art50 = True
        tags.add("eu_transparency")
        tags.add("genai")
        result.findings.append(Finding(
            topic="EU AI Act — transparency (Article 50)",
            status="Indicative: Article 50 transparency duties may apply",
            summary=(
                "The system interacts with natural persons and/or generates synthetic content. "
                "Article 50 requires informing persons they are interacting with AI (unless obvious) "
                "and machine-readable marking of certain synthetic content. Deep-fake and "
                "emotion-recognition/biometric-categorisation deployers have additional disclosure duties."
            ),
            rule="Art. 50 applies to certain systems regardless of high-risk classification.",
            citation="Regulation (EU) 2024/1689, Article 50",
            source_url="https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
        ))

    # GPAI
    if _yes(answers, "gpai_model_provider") or role == "gpai_provider":
        result.gpai = True
        tags.add("eu_gpai")
        result.findings.append(Finding(
            topic="EU AI Act — general-purpose AI model (Chapter V)",
            status="Indicative: GPAI provider obligations (Art. 53) may apply",
            summary=(
                "The engagement indicated the organization provides a general-purpose AI model. "
                "Art. 53 documentation, downstream information, copyright policy, and training-content "
                "summary duties should be scoped. Open-source GPAI models that are not systemic-risk "
                "models have a reduced set of duties."
            ),
            rule="Chapter V applies to GPAI model providers, distinct from high-risk AI system duties.",
            citation="Regulation (EU) 2024/1689, Articles 51–53",
            source_url="https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
        ))
    if _yes(answers, "gpai_systemic_flops"):
        result.gpai_systemic = True
        tags.add("eu_gpai_systemic")
        result.findings.append(Finding(
            topic="EU AI Act — GPAI with systemic risk",
            status="Indicative: Art. 51 presumption of systemic risk (10^25 FLOPs)",
            summary=(
                "Training compute above 10^25 FLOPs creates a presumption of high-impact capabilities. "
                "The provider must notify the Commission and, if classified as systemic-risk, meet Art. 55 "
                "evaluation, incident-reporting, and cybersecurity duties. The provider may argue the "
                "presumption should not apply."
            ),
            rule="Art. 51 presumption: cumulative training compute > 10^25 FLOPs.",
            citation="Regulation (EU) 2024/1689, Articles 51 and 55",
            source_url="https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
        ))

    # SR 11-7 — only if US banking organization + quantitative model used for material decisions
    us_bank = "us_banking" in markets or _yes(answers, "us_supervised_bank")
    material_model = _yes(answers, "material_business_decision_model")
    if us_bank and material_model:
        result.sr117 = True
        tags.add("sr117")
        result.findings.append(Finding(
            topic="US banking — model risk management",
            status="Indicative: SR 11-7 / OCC 2011-12 in scope",
            summary=(
                "The auditee is (or is part of) a US supervised banking organization and the system "
                "is used as a quantitative method for material business decisions. SR 11-7 expects "
                "development standards, independent validation, inventory, and governance. "
                "Not every LLM chatbot at a bank is automatically a 'model' — confirm against the "
                "institution's model-definition policy."
            ),
            rule="SR 11-7 applies to models at supervised banking organizations, not to AI in general.",
            citation="OCC Bulletin 2011-12 / SR 11-7",
            source_url="https://www.occ.gov/news-issuances/bulletins/2011/bulletin-2011-12.html",
        ))
    elif material_model and not us_bank:
        result.findings.append(Finding(
            topic="Model risk management",
            status="Not automatically SR 11-7",
            summary=(
                "The system influences material decisions, but the engagement did not identify a US "
                "supervised banking organization. Apply the institution's model-risk policy and, if "
                "relevant, sector guidance. Do not cite SR 11-7 as binding outside its supervisory scope."
            ),
            rule="SR 11-7 is federal banking supervisory guidance.",
            citation="OCC Bulletin 2011-12 / SR 11-7 (scope: banking organizations)",
            source_url="https://www.occ.gov/news-issuances/bulletins/2011/bulletin-2011-12.html",
        ))

    if _yes(answers, "iso42001_aims"):
        tags.add("iso42001")
        tags.add("aims")

    # Always include NIST RMF as the voluntary audit backbone unless opted out
    if not _yes(answers, "exclude_nist"):
        tags.add("nist")

    result.tags = sorted(tags)
    return result


def obligation_applies(item: dict, result: ScreeningResult) -> bool:
    """Decide whether a library item is in the scoped workpaper."""
    item_tags = set(item.get("tags") or [])
    selected = set(result.tags)

    kind = item.get("kind")
    code = item.get("id", "")

    # Always offer the NIST core when NIST is selected
    if item.get("framework") == "NIST AI RMF 1.0" and "nist" in selected:
        return True

    if item.get("framework") == "ISO/IEC 42001:2023":
        return "iso42001" in selected

    if item.get("framework") == "SR 11-7 / OCC 2011-12":
        return result.sr117

    if item.get("framework") == "OWASP LLM Top 10 2025":
        return "owasp" in selected

    if item.get("framework") == "NIST AI 600-1":
        return "gai_profile" in selected

    if item.get("framework") == "EU AI Act (Reg. 2024/1689)":
        if "eu" not in selected and not result.eu_high_risk and not result.art50 and not result.gpai:
            # Still show Art. 6 classification article whenever markets include EU
            return code in {"EU-ART-5", "EU-ART-6"} and "eu" in selected
        if code == "EU-ART-5":
            return True  # always screen prohibited practices for EU-touching engagements
        if code == "EU-ART-6":
            return True
        if "eu_annex_iii" in item_tags:
            return result.eu_high_risk or result.eu_possible_exception
        if "eu_high_risk" in item_tags:
            if "eu_provider" in item_tags and "eu_provider" not in selected and not result.eu_high_risk:
                return False
            if "eu_deployer" in item_tags and "eu_deployer" not in selected:
                return result.eu_high_risk and "eu_deployer" in selected
            return result.eu_high_risk
        if "eu_transparency" in item_tags:
            return result.art50
        if "eu_gpai_systemic" in item_tags:
            return result.gpai_systemic
        if "eu_gpai" in item_tags:
            return result.gpai
        if "eu_prohibited" in item_tags:
            return True
        if "eu_classification" in item_tags:
            return True
        return "eu" in selected

    return bool(item_tags & selected)
