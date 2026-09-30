"""Assemble the sourced library and attach ABF procedures + crosswalks."""

from __future__ import annotations

from abf.eu_ai_act import SOURCE as EU_SOURCE
from abf.eu_ai_act import as_obligations as eu_obligations
from abf.iso_42001 import SOURCE as ISO_SOURCE
from abf.iso_42001 import as_obligations as iso_obligations
from abf.nist_rmf import SOURCE as NIST_SOURCE
from abf.nist_rmf import as_obligations as nist_obligations
from abf.overlays import GAI_SOURCE, OWASP_SOURCE, SR117_SOURCE
from abf.overlays import as_obligations as overlay_obligations
from abf.procedures import PROCEDURES, for_primary

CROSSWALK = {
    "NIST-GOVERN-1.1": ["EU-ART-6", "EU-ART-16", "ISO-A.2.2"],
    "NIST-GOVERN-1.6": ["ISO-A.4.2", "US-SR117-GOV"],
    "NIST-GOVERN-2.1": ["ISO-A.3.2", "EU-ART-26"],
    "NIST-GOVERN-3.2": ["EU-ART-14", "ISO-A.9.2"],
    "NIST-GOVERN-6.1": ["ISO-A.10.3", "EU-ART-25", "OWASP-LLM03"],
    "NIST-GOVERN-6.2": ["ISO-A.10.2", "NIST-MANAGE-3.1"],
    "NIST-MAP-1.1": ["EU-ART-11", "EU-ANNEX-IV", "ISO-A.9.4"],
    "NIST-MAP-2.1": ["ISO-A.6.2.2"],
    "NIST-MAP-2.2": ["EU-ART-13", "EU-ART-14"],
    "NIST-MAP-3.5": ["EU-ART-14", "ISO-A.9.2"],
    "NIST-MAP-4.1": ["ISO-A.10.3", "NIST-GOVERN-6.1"],
    "NIST-MEASURE-2.5": ["EU-ART-15", "ISO-A.6.2.4", "US-SR117-VAL"],
    "NIST-MEASURE-2.6": ["EU-ART-15", "ISO-A.6.2.4"],
    "NIST-MEASURE-2.7": ["EU-ART-15", "OWASP-LLM01", "NIST-GAI-SECURITY"],
    "NIST-MEASURE-2.8": ["EU-ART-13", "EU-ART-50"],
    "NIST-MEASURE-2.9": ["EU-ART-13", "US-SR117-VAL"],
    "NIST-MEASURE-2.10": ["EU-ART-10", "ISO-A.7.2", "NIST-GAI-PRIVACY"],
    "NIST-MEASURE-2.11": ["EU-ART-10", "ISO-A.5.4"],
    "NIST-MANAGE-2.4": ["EU-ART-14", "ISO-A.9.2"],
    "NIST-MANAGE-3.1": ["ISO-A.10.3", "NIST-GOVERN-6.1"],
    "NIST-MANAGE-3.2": ["OWASP-LLM03", "NIST-GAI-VALUECHAIN"],
    "NIST-MANAGE-4.1": ["EU-ART-12", "EU-ART-26", "ISO-A.6.2.6"],
    "NIST-MANAGE-4.3": ["ISO-A.8.4", "EU-ART-73"],
    "EU-ART-9": ["NIST-MANAGE-1.2", "ISO-A.5.2"],
    "EU-ART-10": ["NIST-MEASURE-2.10", "NIST-MEASURE-2.11", "ISO-A.7.4"],
    "EU-ART-11": ["ISO-A.6.2.7", "NIST-MAP-1.1"],
    "EU-ART-12": ["ISO-A.6.2.8", "NIST-MEASURE-2.4"],
    "EU-ART-14": ["NIST-GOVERN-3.2", "NIST-MAP-3.5", "NIST-MANAGE-2.4"],
    "EU-ART-15": ["NIST-MEASURE-2.5", "NIST-MEASURE-2.7", "OWASP-LLM01"],
    "EU-ART-26": ["NIST-MANAGE-4.1", "ISO-A.9.2"],
    "OWASP-LLM01": ["NIST-MEASURE-2.7", "EU-ART-15"],
    "OWASP-LLM06": ["NIST-GOVERN-3.2", "EU-ART-14"],
    "OWASP-LLM08": ["NIST-MEASURE-2.7", "NIST-MEASURE-2.10"],
}


def build_library() -> dict:
    obligations = []
    obligations.extend(nist_obligations())
    obligations.extend(eu_obligations())
    obligations.extend(iso_obligations())
    obligations.extend(overlay_obligations())

    by_id = {o["id"]: o for o in obligations}
    for oid, others in CROSSWALK.items():
        if oid in by_id:
            by_id[oid]["crosswalk"] = [c for c in others if c in by_id]

    for proc in PROCEDURES:
        target = by_id.get(proc["primary"])
        if target is not None:
            target["procedure"] = {
                "id": proc["id"],
                "title": proc["title"],
                "target_roles": proc["target_roles"],
                "inquiry": proc["inquiry"],
                "observe": proc["observe"],
                "evidence": proc["evidence"],
                "test": proc["test"],
                "authored_by": "ABF workpaper procedure (not the source standard)",
            }

    sources = [
        NIST_SOURCE,
        EU_SOURCE,
        ISO_SOURCE,
        SR117_SOURCE,
        OWASP_SOURCE,
        GAI_SOURCE,
    ]
    return {
        "version": "2.0.0",
        "disclaimer": (
            "ABF is an audit workbench. Screening conclusions are indicative and cite the rule applied. "
            "They are not legal advice, a conformity assessment, or a certification decision. "
            "ISO/IEC 42001 control bodies are titles only; obtain the standard for authentic text. "
            "Where ABF authors a procedure or evidence list, it is labeled as such."
        ),
        "sources": sources,
        "obligations": obligations,
        "procedure_count": sum(1 for o in obligations if o.get("procedure")),
    }
