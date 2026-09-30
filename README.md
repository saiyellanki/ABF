# ABF — Auditor’s Best Friend

Professional workbench for **AI audit scoping**, **control extraction**, **standard alignment**, **evidence**, and **engineer walkthroughs**.

v2 replaces a three-step demo that invented `ABF-CTL-01`…`05` and treated personal data or “agentic” architecture as EU high-risk. That was wrong. This edition only emits **official identifiers**, cites a source URL on every row, and labels screening conclusions as **indicative**.

## Who it is for

Second-line risk, internal audit (3LoD), and model-risk officers who need to:

1. Scope an AI system (purpose, actor role, markets, architecture).
2. See which **NIST AI RMF 1.0** outcomes, **EU AI Act** articles/annexes, **ISO/IEC 42001** Annex A titles, **SR 11-7**, **OWASP LLM Top 10 2025**, and **NIST AI 600-1** GAI risks apply.
3. Walk AI engineers and auditee teams through questions, live observation, and evidence.
4. Export a workpaper (JSON, CSV, Markdown, print/PDF) into the audit file.

## What “100% sourced” means here

| Source | What ABF stores | What ABF does not do |
| --- | --- | --- |
| [NIST AI 100-1](https://doi.org/10.6028/NIST.AI.100-1) | All **72** subcategory outcomes (GOVERN, MAP, MEASURE, MANAGE) | Treat the RMF as a mandatory law |
| [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | Article-level paraphrases + [Annex III](https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3) use cases | Issue a legal classification or CE opinion |
| [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html) | **Titles** of 38 Annex A controls | Quote copyrighted “shall” text |
| [OCC 2011-12 / SR 11-7](https://www.occ.gov/news-issuances/bulletins/2011/bulletin-2011-12.html) | Development, independent validation, governance | Apply SR 11-7 outside US banking supervision |
| [OWASP LLM Top 10 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | Ten threat categories | Treat them as regulations |
| [NIST AI 600-1](https://doi.org/10.6028/NIST.AI.600-1) | Twelve generative-AI risk categories | Substitute for the full action tables |

Walkthrough questions, evidence checklists, and test steps are **ABF-authored workpapers** mapped to those IDs. They are labelled as such.

### Classification rules (the ones the old app got wrong)

- EU **high-risk** follows **Article 6**: Annex I product-safety path **or** Annex III use case — not “handles PII”, not “is an agent”.
- Annex III + **profiling of natural persons** → Art. 6(3) exception is **unavailable**.
- Annex III + a 6(3) condition, without profiling → **possible exception**; the provider must document it.
- **Article 5** ticks are an indicative screen for counsel, not a finding that the system is prohibited.
- **Article 50** transparency can apply to a chatbot that is **not** high-risk.
- **SR 11-7** is included only for a **US supervised banking organization** using a **material decision model**.
- ISO **A.8.4** is **Communication of incidents**, not system protection.

## Live site

**GitHub Pages:** [https://saiyellanki.github.io/ABF/](https://saiyellanki.github.io/ABF/)

The repository is a static site. GitHub Pages publishes `main` from `/`. A `.nojekyll` file tells Pages not to run Jekyll, so `data/library.json` and `assets/` are served as-is.

## Run the website locally

Static site (Netlify-ready). From the repository root:

```bash
python3 tools/build_library.py          # regenerates data/library.json
python3 -m http.server 4173
```

Open `http://127.0.0.1:4173/`. Use **Scope an audit** → extract requirements → export CSV / Markdown / JSON.

`netlify.toml` publishes the repository root. No Node build.

## Python engine

```bash
python3 -m unittest tests.test_classify -v
python3 tools/abf_cli.py --answers path/to/answers.json --out workpaper.json
python3 walkthrough_generator.py --control EU-ART-14
```

## Repository layout

```
index.html              # workbench UI
assets/                 # CSS + screening engine + app
data/library.json       # generated sourced library
abf/                    # NIST, EU, ISO, overlays, procedures, classify
tools/build_library.py
tests/test_classify.py
```

## Disclaimer

ABF is not legal advice, a notified-body conformity assessment, or an ISO certification. Obtain the authentic Official Journal text, NIST publications, and purchased ISO/IEC 42001:2023 before relying on a conclusion in an audit opinion.
