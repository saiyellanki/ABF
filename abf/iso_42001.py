"""ISO/IEC 42001:2023 Annex A — public control titles only.

ISO standards text is copyrighted. ABF ships titles that are widely published in
tables of contents and public commentaries, plus ABF-authored auditor notes.
Auditors must obtain ISO/IEC 42001:2023 for the authentic control wording.
"""

SOURCE = {
    "id": "ISO-IEC-42001-2023",
    "name": "ISO/IEC 42001:2023 — AI management system",
    "date": "2023",
    "url": "https://www.iso.org/standard/81230.html",
    "license_note": (
        "Control titles only. Official 'shall' statements are copyright ISO and are not reproduced. "
        "Use the purchased standard (and Annex B guidance) for implementation and certification."
    ),
}

# 38 Annex A controls. Titles follow the public ISO 42001 Annex A numbering.
ANNEX_A = [
    {"id": "A.2.2", "objective": "A.2 Policies related to AI", "title": "AI policy"},
    {"id": "A.2.3", "objective": "A.2 Policies related to AI", "title": "Alignment with other organisational policies"},
    {"id": "A.2.4", "objective": "A.2 Policies related to AI", "title": "Review of the AI policy"},
    {"id": "A.3.2", "objective": "A.3 Internal organisation", "title": "AI roles and responsibilities"},
    {"id": "A.3.3", "objective": "A.3 Internal organisation", "title": "Reporting of concerns"},
    {"id": "A.4.2", "objective": "A.4 Resources for AI systems", "title": "Resource documentation"},
    {"id": "A.4.3", "objective": "A.4 Resources for AI systems", "title": "Data resources"},
    {"id": "A.4.4", "objective": "A.4 Resources for AI systems", "title": "Tooling resources"},
    {"id": "A.4.5", "objective": "A.4 Resources for AI systems", "title": "System and computing resources"},
    {"id": "A.4.6", "objective": "A.4 Resources for AI systems", "title": "Human resources"},
    {"id": "A.5.2", "objective": "A.5 Assessing impacts of AI systems", "title": "AI system impact assessment process"},
    {"id": "A.5.3", "objective": "A.5 Assessing impacts of AI systems", "title": "Documentation of AI system impact assessments"},
    {"id": "A.5.4", "objective": "A.5 Assessing impacts of AI systems", "title": "Assessing AI system impact on individuals or groups of individuals"},
    {"id": "A.5.5", "objective": "A.5 Assessing impacts of AI systems", "title": "Assessing societal impacts of AI systems"},
    {"id": "A.6.1.2", "objective": "A.6 AI system life cycle", "title": "Objectives for responsible development of AI system"},
    {"id": "A.6.1.3", "objective": "A.6 AI system life cycle", "title": "Processes for responsible design and development of AI systems"},
    {"id": "A.6.2.2", "objective": "A.6 AI system life cycle", "title": "AI system requirements and specification"},
    {"id": "A.6.2.3", "objective": "A.6 AI system life cycle", "title": "Documentation of AI system design and development"},
    {"id": "A.6.2.4", "objective": "A.6 AI system life cycle", "title": "AI system verification and validation"},
    {"id": "A.6.2.5", "objective": "A.6 AI system life cycle", "title": "AI system deployment"},
    {"id": "A.6.2.6", "objective": "A.6 AI system life cycle", "title": "AI system operation and monitoring"},
    {"id": "A.6.2.7", "objective": "A.6 AI system life cycle", "title": "AI system technical documentation"},
    {"id": "A.6.2.8", "objective": "A.6 AI system life cycle", "title": "AI system recording of event logs"},
    {"id": "A.7.2", "objective": "A.7 Data for AI systems", "title": "Data for development and enhancement of AI system"},
    {"id": "A.7.3", "objective": "A.7 Data for AI systems", "title": "Acquisition of data"},
    {"id": "A.7.4", "objective": "A.7 Data for AI systems", "title": "Quality of data for AI systems"},
    {"id": "A.7.5", "objective": "A.7 Data for AI systems", "title": "Data provenance"},
    {"id": "A.7.6", "objective": "A.7 Data for AI systems", "title": "Data preparation"},
    {"id": "A.8.2", "objective": "A.8 Information for interested parties of AI systems", "title": "System documentation and information for users"},
    {"id": "A.8.3", "objective": "A.8 Information for interested parties of AI systems", "title": "External reporting"},
    {"id": "A.8.4", "objective": "A.8 Information for interested parties of AI systems", "title": "Communication of incidents"},
    {"id": "A.8.5", "objective": "A.8 Information for interested parties of AI systems", "title": "Information for interested parties"},
    {"id": "A.9.2", "objective": "A.9 Use of AI systems", "title": "Processes for responsible use of AI systems"},
    {"id": "A.9.3", "objective": "A.9 Use of AI systems", "title": "Objectives for responsible use of AI system"},
    {"id": "A.9.4", "objective": "A.9 Use of AI systems", "title": "Intended use of the AI system"},
    {"id": "A.10.2", "objective": "A.10 Third-party and customer relationships", "title": "Allocation of responsibilities"},
    {"id": "A.10.3", "objective": "A.10 Third-party and customer relationships", "title": "Suppliers"},
    {"id": "A.10.4", "objective": "A.10 Third-party and customer relationships", "title": "Customers"},
]


def as_obligations():
    items = []
    for row in ANNEX_A:
        tags = ["iso42001", "aims"]
        if row["id"].startswith("A.2") or row["id"].startswith("A.3"):
            tags.append("governance_baseline")
        if row["id"].startswith("A.10"):
            tags.append("third_party")
        if row["id"].startswith("A.7"):
            tags.append("personal_data")
        if row["id"] in {"A.6.2.4", "A.6.2.6"}:
            tags.append("tevv")
        if row["id"] in {"A.5.4", "A.5.5"}:
            tags.append("fairness")
        if row["id"] in {"A.9.2", "A.9.4"}:
            tags.append("human_oversight")
        items.append({
            "id": f"ISO-{row['id']}",
            "framework": "ISO/IEC 42001:2023",
            "citation": f"ISO/IEC 42001:2023 Annex A, {row['id']} {row['title']}",
            "source_url": SOURCE["url"],
            "kind": "control_title",
            "code": row["id"],
            "function": "AIMS",
            "category": row["objective"],
            "title": row["title"],
            "official_text": (
                f"Control title only: {row['id']} — {row['title']}. "
                "Obtain ISO/IEC 42001:2023 for the authentic control text and Annex B guidance."
            ),
            "tags": tags,
            "crosswalk": [],
        })
    return items
