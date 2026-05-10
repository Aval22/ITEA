# JOSS Submission Checklist — ITEA Framework v3.0

This document maps the current state of the repository against the submission
and review criteria of the [Journal of Open Source Software](https://joss.theoj.org/).
Use it as a pre-submission self-audit and, after submission, as a quick reply
template for reviewer questions.

References:

- JOSS submission requirements: <https://joss.readthedocs.io/en/latest/submitting.html>
- JOSS review checklist (what reviewers will tick): <https://joss.readthedocs.io/en/latest/review_checklist.html>
- JOSS paper structure: <https://joss.readthedocs.io/en/latest/paper.html>

---

## 1. Repository-level requirements

| # | Requirement | Status | Evidence in this repo |
|---|-------------|:------:|------------------------|
| 1.1 | Software is open source under an OSI-approved license | ✅ | `LICENSE` (MIT) |
| 1.2 | Public, version-controlled repository | ⚠️ | URL declared in metadata: `https://github.com/Aval22/ITEA`. **Confirm the GitHub repo is public and the contents match this folder before submitting.** |
| 1.3 | The submitting author is a substantial contributor | ✅ | Sole-author project (CITATION.cff, paper.md, ORCID 0009-0003-1438-1633) |
| 1.4 | The software has an obvious research application | ✅ | `paper.md` §"Statement of need"; trilogy 8A/8B/8C cited as active use |
| 1.5 | Substantial scholarly effort (≥ 3 person-months equivalent or non-trivial contribution) | ✅ | `CHANGELOG.md` documents 9 versions across March 2024 → April 2026 with three major methodological revisions in v3.0 |
| 1.6 | First-time submission OR substantial change since last review | ✅ | First-time submission |

## 2. Software paper (`paper/paper.md`)

| # | Requirement | Status | Notes |
|---|-------------|:------:|-------|
| 2.1 | Length 250–1,000 words (excluding refs and code) | ✅ | ~960 words |
| 2.2 | YAML front-matter with title, authors, ORCID, affiliations, date, bibliography | ✅ | All present; ROR for URJC included |
| 2.3 | "Summary" section accessible to a non-specialist | ✅ | Lines 24–35 |
| 2.4 | "Statement of need" section explicitly named | ✅ | Lines 37–64 |
| 2.5 | Reference to "State of the field" (compares to other tools) | ✅ | Lines 88–96 |
| 2.6 | Bibliography file referenced (`paper.bib`) | ✅ | 12 BibTeX entries; includes Frey-Osborne, Felten-Raj-Seamans, Brynjolfsson 2025, Acemoglu, Eloundou, Nonaka, the trilogy |
| 2.7 | All in-text citations resolve in `paper.bib` | 🔍 | Recommend a final `pandoc-citeproc --strict` pass before submission |
| 2.8 | Acknowledges generative-AI assistance per JOSS policy | ✅ | Lines 130–138 |
| 2.9 | Figures (optional) — if added, ≤ 6 and Figure N captions | n/a | None used |

## 3. Documentation

| # | Requirement | Status | Where |
|---|-------------|:------:|-------|
| 3.1 | Statement of need in README | ✅ | `README.md` "What is ITEA v3.0?" |
| 3.2 | Installation instructions | ⚠️ | README mentions reference implementations under `code/v3/` but does not yet provide a one-line install (no `pyproject.toml` / `setup.py` / `requirements.txt`). Reviewers usually accept "pip install -e ." or a `requirements.txt`. **Recommended addition: minimal `requirements.txt`** (numpy, pandas, openpyxl, pytest) **and a 5-line install/usage block.** |
| 3.3 | Example usage (command or notebook) | ⚠️ | Tests and `code/v3/itea_functions_v3.py` docstrings serve as examples; consider adding a `examples/quickstart.py` calling `itea_v3()`, `ira_v3()`, `oaei_v3_mult()` over a 10-row sample. |
| 3.4 | API / function docs | ✅ | Docstrings in `itea_functions_v3.py` and `.R`; reconciliation example in `MIGRATION.md` |
| 3.5 | Multilingual READMEs | ✅ | EN, ES, PT, ZH |
| 3.6 | Migration / upgrade guide | ✅ | `docs/MIGRATION.md` (v1.45 → v3.0) |

## 4. Software quality

| # | Requirement | Status | Where |
|---|-------------|:------:|-------|
| 4.1 | Automated tests | ✅ | `code/v3/tests/test_itea_v3.py` — 14 pytest tests, all passing per CHANGELOG |
| 4.2 | CI configured (recommended, not strictly required) | ⚠️ | No `.github/workflows/` yet. **Suggest adding** a 30-line GitHub Actions workflow running `pytest -v` on Python 3.10/3.11/3.12; reviewers regularly request this. |
| 4.3 | Reconciliation against authoritative artefact | ✅ | Tests reconcile R/Python output against the workbook within Δ < 1e-6 |
| 4.4 | Continuous numerical-precision check | ✅ | `itea_reconcile()` exposed as importable function |
| 4.5 | Functionality is non-trivial (not a script wrapper) | ✅ | Implements z-score aggregation, triple residualisation, and dual-variant OAEI — non-trivial transformations |

## 5. Community standards

| # | Requirement | Status | Notes |
|---|-------------|:------:|-------|
| 5.1 | `LICENSE` file at repository root | ✅ | MIT |
| 5.2 | `CONTRIBUTING.md` | ⚠️ | Not present. **Recommended addition** before submission. A 30-line template suffices: how to file issues, how to propose a methodological change, how to validate against the workbook. |
| 5.3 | `CODE_OF_CONDUCT.md` | ⚠️ | Not present. JOSS strongly encourages adopting the [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). |
| 5.4 | Issue / PR templates | ⚠️ | Optional. JOSS reviewers seldom block on this. |
| 5.5 | Citation file (`CITATION.cff`) | ✅ | Present, valid CFF 1.2.0, with ORCID, concept DOI, references to the trilogy |

## 6. Citation and DOI

| # | Requirement | Status | Notes |
|---|-------------|:------:|-------|
| 6.1 | Repository has a Zenodo DOI | ✅ | `CITATION.cff` declares concept DOI `10.5281/zenodo.19578915` (resolves to all versions), version DOI v3.0 `10.5281/zenodo.20083102`, and version DOI v1.45 `10.5281/zenodo.19578916`. All three resolve in Zenodo. |
| 6.2 | The DOI in CITATION.cff is the *concept* DOI (resolves to "all versions") | ✅ | Concept DOI `10.5281/zenodo.19578915` recorded in `CITATION.cff` and badges; version DOI for v3.0 (`10.5281/zenodo.20083102`) recorded in `MANIFEST.json` and BibTeX entries. Both will be supplied to the JOSS submission form. |
| 6.3 | Dataset has a DOI (if separate from software) | n/a | Dataset is bundled in `data/processed/ITEA_v3_0_Workbook.xlsx` and covered by the software DOI |

## 7. Pre-submission action list

In priority order — *only items 1–3 are blockers, the rest are reviewer-friendly polish*:

1. **Make the GitHub repo public** at the URL declared in `CITATION.cff` and `paper.md`, and confirm contents match this folder.
2. **Mint or confirm the Zenodo DOI** (see `docs/ZENODO_DEPOSIT_GUIDE.md`) and update `CITATION.cff`, `paper.md`, `README*.md` and `MANIFEST.json` with the *real* concept and version DOIs.
3. **Add `requirements.txt`** (or `pyproject.toml`) and a 5-line install/usage block to the README. Reviewers will block on a missing install path.
4. Add a `CONTRIBUTING.md` (Contributor Covenant template).
5. Add a `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1).
6. Add a GitHub Actions workflow `.github/workflows/test.yml` running `pytest -v` on Python 3.10/3.11/3.12.
7. Run `pandoc paper.md -o paper.pdf --filter pandoc-citeproc --bibliography paper/paper.bib` locally and visually inspect: this is exactly what JOSS's `Whedon`/`editorialbot` will do.
8. Replace the typo in `CHANGELOG.md` line 40: it says "ITEA_v3_0_Consolidated_Methodology.pdf" but the file in `docs/` has the `.docx` extension — either convert to PDF (recommended for JOSS reviewers) or fix the changelog reference.
9. Open the JOSS [pre-submission issue](https://github.com/openjournals/joss-reviews/issues/new?template=pre_submission.md) if you want a sanity-check before formal submission.

## 8. Submission step (when items 1–3 are done)

1. Visit <https://joss.theoj.org/papers/new>.
2. Provide the GitHub URL (`https://github.com/Aval22/ITEA`), the version tag (`v3.0`), and the path to the paper (`paper/paper.md`).
3. Editor-bot ("editorialbot") will validate the YAML, build `paper.pdf` from `paper.md`, run a citation check, and verify the license. Fix anything it flags before a human editor is assigned.
4. After acceptance, JOSS asks for the **Zenodo archive DOI of the exact reviewed commit** — this is why minting the Zenodo deposit is a prerequisite, not an afterthought.

---

*Generated 2026-05-07 alongside `DEPLOYMENT_REPORT_2026-05-07.md` and
`ZENODO_DEPOSIT_GUIDE.md`. Update this file whenever any of the action items
above are completed.*
