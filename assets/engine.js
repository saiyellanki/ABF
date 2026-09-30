/**
 * Indicative screening — keep in lockstep with abf/classify.py
 * (Python tests are canonical).
 */
(function (global) {
  const ANNEX_III_KEYS = [
    "annex_iii_1", "annex_iii_2", "annex_iii_3", "annex_iii_4",
    "annex_iii_5", "annex_iii_6", "annex_iii_7", "annex_iii_8",
  ];

  function yes(answers, key) {
    const val = answers[key];
    if (Array.isArray(val)) return val.length > 0;
    return val === true || val === "yes" || val === "true" || val === "YES";
  }

  function classify(answers) {
    const findings = [];
    const tags = new Set(["governance_baseline", "nist", "always_if_using_rmf", "system_specific"]);
    let euHighRisk = false;
    let euPossibleException = false;
    let euProhibitedIndicative = false;
    let gpai = false;
    let gpaiSystemic = false;
    let sr117 = false;
    let art50 = false;

    const role = answers.role || "deployer";
    const markets = new Set(answers.markets || []);
    const architecture = new Set(answers.architecture || []);
    const euMarket = markets.has("eu") || yes(answers, "output_used_in_eu");

    if (role === "provider" || role === "both") tags.add("eu_provider");
    if (role === "deployer" || role === "both") tags.add("eu_deployer");
    if (role === "gpai_provider") {
      tags.add("eu_gpai");
      gpai = true;
    }

    if (["llm_chat", "rag", "agentic"].some((x) => architecture.has(x))) {
      tags.add("genai"); tags.add("gai_profile"); tags.add("owasp");
    }
    if (architecture.has("rag")) tags.add("rag");
    if (architecture.has("agentic")) tags.add("agentic");
    if (architecture.has("classic_ml")) tags.add("classic_ml");
    if (architecture.has("biometrics")) tags.add("biometrics");
    if (yes(answers, "third_party_model_or_api")) tags.add("third_party");
    if (yes(answers, "personal_data")) tags.add("personal_data");
    if (yes(answers, "automated_decision")) tags.add("human_oversight");

    const prohibited = answers.art5_practices || [];
    if (prohibited.length) {
      euProhibitedIndicative = true;
      tags.add("eu_prohibited");
      findings.push({
        topic: "EU AI Act — prohibited practices",
        status: "Indicative: possible Article 5 issue",
        tone: "high",
        summary:
          "One or more practices associated with Article 5 were indicated. Do not treat this as a legal finding. Counsel should compare the intended use to the authentic Article 5 list and its exceptions.",
        rule: "Art. 5 prohibits placing on the market, putting into service, or using listed practices.",
        citation: "Regulation (EU) 2024/1689, Article 5",
        source_url: "https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
      });
    }

    const annex = ANNEX_III_KEYS.filter((k) => yes(answers, k));
    const annexI = yes(answers, "annex_i_safety_component");
    const profiles = yes(answers, "profiles_natural_persons");
    const exceptionAny = [
      "art63_narrow_procedural",
      "art63_improves_human",
      "art63_detects_patterns",
      "art63_preparatory",
    ].some((k) => yes(answers, k));

    if (euMarket || annex.length || annexI || yes(answers, "eu_in_scope")) {
      tags.add("eu");
      tags.add("eu_classification");
    }

    if (annexI) {
      euHighRisk = true;
      findings.push({
        topic: "EU AI Act — high-risk (Article 6(1))",
        status: "Indicative: high-risk if Annex I + third-party conformity assessment applies",
        tone: "high",
        summary:
          "The engagement indicated the system is (or is a safety component of) a product covered by Annex I Union harmonisation legislation that requires third-party conformity assessment. Confirm both limbs of Article 6(1) against the product file.",
        rule: "Art. 6(1): safety component/product under Annex I AND third-party conformity assessment.",
        citation: "Regulation (EU) 2024/1689, Article 6(1) and Annex I",
        source_url: "https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
      });
    }

    if (annex.length) {
      const labels = annex.map((k) => k.replace("annex_iii_", "Annex III(") + ")").join(", ");
      if (profiles) {
        euHighRisk = true;
        findings.push({
          topic: "EU AI Act — high-risk (Article 6(2) + profiling)",
          status: "Indicative: high-risk (profiling removes the Art. 6(3) exception)",
          tone: "high",
          summary: `Intended purpose appears to fall under ${labels}. Article 6 provides that Annex III systems that profile natural persons are always high-risk. Handling personal data alone is not the test; the use-case list is.`,
          rule: "Annex III systems that profile natural persons are high-risk; Art. 6(3) does not apply.",
          citation: "Regulation (EU) 2024/1689, Article 6(2)–6(3) and Annex III",
          source_url: "https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3",
        });
      } else if (exceptionAny) {
        euPossibleException = true;
        findings.push({
          topic: "EU AI Act — possible Article 6(3) exception",
          status: "Indicative: Annex III use case, but a 6(3) exception may apply",
          tone: "warn",
          summary: `Intended purpose appears to fall under ${labels}, but one or more Art. 6(3) conditions were indicated. The provider must document this assessment before placing the system on the market or putting it into service. This tool does not decide whether the exception is available.`,
          rule: "Art. 6(3) exception is documented by the provider and is unavailable if the system profiles persons.",
          citation: "Regulation (EU) 2024/1689, Article 6(3)",
          source_url: "https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
        });
      } else {
        euHighRisk = true;
        findings.push({
          topic: "EU AI Act — high-risk (Article 6(2))",
          status: "Indicative: high-risk Annex III system",
          tone: "high",
          summary: `Intended purpose appears to fall under ${labels}. No Art. 6(3) exception was indicated. Confirm the exact Annex III paragraph against the authentic text and intended purpose documentation (Art. 11 / Annex IV).`,
          rule: "Art. 6(2): systems listed in Annex III are high-risk unless a documented 6(3) exception applies.",
          citation: "Regulation (EU) 2024/1689, Article 6(2) and Annex III",
          source_url: "https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3",
        });
      }
    } else if (euMarket && !annexI) {
      findings.push({
        topic: "EU AI Act — not classified as Annex III high-risk on this intake",
        status: "Indicative: no Annex III category selected",
        tone: "ok",
        summary:
          "No Annex III use case was selected. Personal data processing, use of a foundation model, or an agentic architecture does not by itself make a system high-risk. Revisit intended purpose with legal if the use case is close to Annex III.",
        rule: "High-risk classification is Art. 6 + Annex I or Annex III, not data sensitivity alone.",
        citation: "Regulation (EU) 2024/1689, Article 6",
        source_url: "https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
      });
    }

    if (euHighRisk) {
      ["eu_high_risk", "human_oversight", "tevv", "security", "fairness"].forEach((t) => tags.add(t));
      if (role === "provider" || role === "both") tags.add("eu_provider");
      if (role === "deployer" || role === "both") tags.add("eu_deployer");
      if (yes(answers, "fria_role")) tags.add("fria");
    }

    if (yes(answers, "interacts_with_natural_persons") || yes(answers, "synthetic_content") || yes(answers, "deepfake")) {
      art50 = true;
      tags.add("eu_transparency");
      tags.add("genai");
      findings.push({
        topic: "EU AI Act — transparency (Article 50)",
        status: "Indicative: Article 50 transparency duties may apply",
        tone: "info",
        summary:
          "The system interacts with natural persons and/or generates synthetic content. Article 50 requires informing persons they are interacting with AI (unless obvious) and machine-readable marking of certain synthetic content.",
        rule: "Art. 50 applies to certain systems regardless of high-risk classification.",
        citation: "Regulation (EU) 2024/1689, Article 50",
        source_url: "https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
      });
    }

    if (yes(answers, "gpai_model_provider") || role === "gpai_provider") {
      gpai = true;
      tags.add("eu_gpai");
      findings.push({
        topic: "EU AI Act — general-purpose AI model (Chapter V)",
        status: "Indicative: GPAI provider obligations (Art. 53) may apply",
        tone: "info",
        summary:
          "The engagement indicated the organization provides a general-purpose AI model. Art. 53 documentation, downstream information, copyright policy, and training-content summary duties should be scoped.",
        rule: "Chapter V applies to GPAI model providers, distinct from high-risk AI system duties.",
        citation: "Regulation (EU) 2024/1689, Articles 51–53",
        source_url: "https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
      });
    }
    if (yes(answers, "gpai_systemic_flops")) {
      gpaiSystemic = true;
      tags.add("eu_gpai_systemic");
      findings.push({
        topic: "EU AI Act — GPAI with systemic risk",
        status: "Indicative: Art. 51 presumption of systemic risk (10^25 FLOPs)",
        tone: "high",
        summary:
          "Training compute above 10^25 FLOPs creates a presumption of high-impact capabilities. The provider must notify the Commission and, if classified as systemic-risk, meet Art. 55 duties.",
        rule: "Art. 51 presumption: cumulative training compute > 10^25 FLOPs.",
        citation: "Regulation (EU) 2024/1689, Articles 51 and 55",
        source_url: "https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
      });
    }

    const usBank = markets.has("us_banking") || yes(answers, "us_supervised_bank");
    const materialModel = yes(answers, "material_business_decision_model");
    if (usBank && materialModel) {
      sr117 = true;
      tags.add("sr117");
      findings.push({
        topic: "US banking — model risk management",
        status: "Indicative: SR 11-7 / OCC 2011-12 in scope",
        tone: "high",
        summary:
          "The auditee is (or is part of) a US supervised banking organization and the system is used as a quantitative method for material business decisions. SR 11-7 expects development standards, independent validation, inventory, and governance. Not every LLM chatbot at a bank is automatically a 'model' — confirm against the institution's model-definition policy.",
        rule: "SR 11-7 applies to models at supervised banking organizations, not to AI in general.",
        citation: "OCC Bulletin 2011-12 / SR 11-7",
        source_url: "https://www.occ.gov/news-issuances/bulletins/2011/bulletin-2011-12.html",
      });
    } else if (materialModel && !usBank) {
      findings.push({
        topic: "Model risk management",
        status: "Not automatically SR 11-7",
        tone: "warn",
        summary:
          "The system influences material decisions, but the engagement did not identify a US supervised banking organization. Do not cite SR 11-7 as binding outside its supervisory scope.",
        rule: "SR 11-7 is federal banking supervisory guidance.",
        citation: "OCC Bulletin 2011-12 / SR 11-7 (scope: banking organizations)",
        source_url: "https://www.occ.gov/news-issuances/bulletins/2011/bulletin-2011-12.html",
      });
    }

    if (yes(answers, "iso42001_aims")) {
      tags.add("iso42001");
      tags.add("aims");
    }
    if (!yes(answers, "exclude_nist")) tags.add("nist");

    return {
      findings,
      tags: Array.from(tags).sort(),
      eu_high_risk: euHighRisk,
      eu_possible_exception: euPossibleException,
      eu_prohibited_indicative: euProhibitedIndicative,
      gpai,
      gpai_systemic: gpaiSystemic,
      sr117,
      art50,
    };
  }

  function obligationApplies(item, result) {
    const itemTags = new Set(item.tags || []);
    const selected = new Set(result.tags || []);
    const code = item.id || "";

    if (item.framework === "NIST AI RMF 1.0" && selected.has("nist")) return true;
    if (item.framework === "ISO/IEC 42001:2023") return selected.has("iso42001");
    if (item.framework === "SR 11-7 / OCC 2011-12") return !!result.sr117;
    if (item.framework === "OWASP LLM Top 10 2025") return selected.has("owasp");
    if (item.framework === "NIST AI 600-1") return selected.has("gai_profile");

    if (item.framework === "EU AI Act (Reg. 2024/1689)") {
      if (!selected.has("eu") && !result.eu_high_risk && !result.art50 && !result.gpai) {
        return false;
      }
      if (code === "EU-ART-5" || code === "EU-ART-6") return true;
      if (itemTags.has("eu_annex_iii")) return result.eu_high_risk || result.eu_possible_exception;
      if (itemTags.has("eu_high_risk")) return !!result.eu_high_risk;
      if (itemTags.has("eu_transparency")) return !!result.art50;
      if (itemTags.has("eu_gpai_systemic")) return !!result.gpai_systemic;
      if (itemTags.has("eu_gpai")) return !!result.gpai;
      if (itemTags.has("eu_prohibited") || itemTags.has("eu_classification")) return true;
      return selected.has("eu");
    }
    return item.tags.some((t) => selected.has(t));
  }

  global.ABFEngine = { classify, obligationApplies };
})(window);
