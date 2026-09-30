"""Tests for conservative, cited classification — the previous app failed these."""

import unittest

from abf.classify import classify, obligation_applies
from abf.iso_42001 import ANNEX_A
from abf.library import build_library
from abf.nist_rmf import NIST_SUBCATEGORIES


class LibraryIntegrityTests(unittest.TestCase):
    def test_nist_has_72_subcategories(self):
        self.assertEqual(len(NIST_SUBCATEGORIES), 72)

    def test_iso_a84_is_incident_communication_not_system_protection(self):
        a84 = next(c for c in ANNEX_A if c["id"] == "A.8.4")
        self.assertEqual(a84["title"], "Communication of incidents")
        self.assertIn("interested parties", a84["objective"].lower())

    def test_library_contains_official_ids_not_invented_abf_ctl(self):
        lib = build_library()
        ids = {o["id"] for o in lib["obligations"]}
        self.assertIn("NIST-GOVERN-1.1", ids)
        self.assertIn("EU-ART-14", ids)
        self.assertIn("ISO-A.8.4", ids)
        self.assertTrue(all(not i.startswith("ABF-CTL") for i in ids))

    def test_every_item_has_source_url(self):
        lib = build_library()
        missing = [o["id"] for o in lib["obligations"] if not o.get("source_url")]
        self.assertEqual(missing, [])


class ClassificationTests(unittest.TestCase):
    def test_personal_data_alone_is_not_eu_high_risk(self):
        result = classify({
            "markets": ["eu"],
            "personal_data": True,
            "architecture": ["llm_chat"],
            "role": "deployer",
        })
        self.assertFalse(result.eu_high_risk)
        self.assertFalse(result.eu_prohibited_indicative)

    def test_agentic_architecture_alone_is_not_eu_high_risk(self):
        result = classify({
            "markets": ["eu"],
            "architecture": ["agentic"],
            "role": "provider",
        })
        self.assertFalse(result.eu_high_risk)

    def test_annex_iii_employment_plus_profiling_is_high_risk(self):
        result = classify({
            "markets": ["eu"],
            "annex_iii_4": True,
            "profiles_natural_persons": True,
            "role": "provider",
        })
        self.assertTrue(result.eu_high_risk)
        self.assertFalse(result.eu_possible_exception)
        joined = " ".join(f.citation for f in result.findings)
        self.assertIn("Article 6", joined)

    def test_annex_iii_with_6_3_condition_without_profiling_is_possible_exception(self):
        result = classify({
            "markets": ["eu"],
            "annex_iii_4": True,
            "profiles_natural_persons": False,
            "art63_narrow_procedural": True,
            "role": "provider",
        })
        self.assertFalse(result.eu_high_risk)
        self.assertTrue(result.eu_possible_exception)

    def test_sr117_requires_supervised_bank_and_material_model(self):
        bank = classify({
            "markets": ["us_banking"],
            "material_business_decision_model": True,
        })
        self.assertTrue(bank.sr117)
        not_bank = classify({
            "markets": ["eu"],
            "material_business_decision_model": True,
        })
        self.assertFalse(not_bank.sr117)

    def test_chat_interaction_triggers_art_50_not_high_risk(self):
        result = classify({
            "markets": ["eu"],
            "interacts_with_natural_persons": True,
            "architecture": ["llm_chat"],
            "role": "deployer",
        })
        self.assertTrue(result.art50)
        self.assertFalse(result.eu_high_risk)

    def test_art5_flag_is_indicative_not_a_conviction(self):
        result = classify({
            "markets": ["eu"],
            "art5_practices": ["social_scoring"],
        })
        self.assertTrue(result.eu_prohibited_indicative)
        self.assertTrue(any("not a legal finding" in f.summary.lower() or "indicative" in f.status.lower()
                            for f in result.findings))

    def test_high_risk_includes_provider_articles(self):
        lib = build_library()
        by_id = {o["id"]: o for o in lib["obligations"]}
        result = classify({
            "markets": ["eu"],
            "annex_iii_5": True,
            "role": "provider",
        })
        self.assertTrue(result.eu_high_risk)
        self.assertTrue(obligation_applies(by_id["EU-ART-9"], result))
        self.assertTrue(obligation_applies(by_id["EU-ART-14"], result))
        self.assertTrue(obligation_applies(by_id["NIST-MEASURE-2.11"], result))

    def test_owasp_only_when_genai_architecture(self):
        lib = build_library()
        llm01 = next(o for o in lib["obligations"] if o["id"] == "OWASP-LLM01")
        classic = classify({"markets": ["eu"], "architecture": ["classic_ml"]})
        gen = classify({"markets": ["eu"], "architecture": ["rag"]})
        self.assertFalse(obligation_applies(llm01, classic))
        self.assertTrue(obligation_applies(llm01, gen))


if __name__ == "__main__":
    unittest.main()
