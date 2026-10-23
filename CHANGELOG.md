# Changelog

All notable changes to the ITEA Framework are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased] — 4.0.0 release candidate (JOSS submission)

First stable release of the European layer. OAXI-EU becomes reproducible
end to end from public inputs, and its values change (see *Changed*).

**Development note.** The public history has no commits between 2 July and
October 2026. During that period:
- **June – early July:** v4.0 work continued locally: the reliability study
  of the AXI grades (multi-provider coding and deterministic codebook,
  24–25 June) and the ESCO/ISCO bridge. It also continued in the working
  papers that use ITEA.
- **August – September:** no development.
- **October:** the package, tests and documentation in this release were
  written and are published with their actual dates. No commit has been
  backdated.

### Added

- Installable Python package `itea-framework` (`src/itea/`, `pyproject.toml`)
  with a command-line tool: `itea fetch` downloads O\*NET 30.2 and the two
  BLS crosswalks and verifies their SHA-256; `itea build-eu` builds OAXI-EU.
- Modules `itea.axi` (task → activity → occupation roll-up), `itea.crosswalk`
  (official BLS SOC 2018 → ISCO-08 chain) and `itea.oaxi_eu` (index,
  benchmark convergence, κ calibration grid).
- **AXI task grades released** under CC BY 4.0, shipped inside the package
  (`src/itea/data/axi_task_grades.csv.gz`, 47,810 tasks, four ordinal scales)
  with provenance and reliability notes.
- **JRC145832 benchmark shipped** (`src/itea/data/`, CC BY 4.0): Table M.1 of
  Casas et al. (2026), so that `itea validate` and the tests reproduce the
  convergence figures.
- Canonical outputs in `v4.0/outputs/`: `oaxi_eu.csv`, `occupation_shares.csv`,
  `crosswalk_soc2018_isco08.csv`, `oaxi_eu.meta.json` (input and output hashes).
- Generic roll-up `itea.rollup` (`to_activities`, `to_occupations`, `to_isco`):
  any numeric task-level score can be carried to ISCO-08, not only AXI.
- **`itea.grading` (in development for v4.1)**, the documented replacement for the
  legacy AXI grades, which it never trains on:
  - `structural`: K and E priors from the official O\*NET linkage tables
    (Abilities/Skills to Work Activities) for all 18,796 O\*NET 30.2 tasks;
  - `validation`: external references (Eloundou et al. human labels, pinned
    commit; Acemoglu–Autor task indices; Job Zone), linear-weighted κ and
    occupation-clustered bootstrap CIs;
  - `technology`: occupation × product inventory from O\*NET Technology Skills
    and Tools Used;
  - `eurostat`: enterprise adoption of ERP, CRM and AI (Eurostat ICT survey).
- First structural validation against pre-registered hypotheses
  (`docs/grading/HIPOTESIS_PREREGISTRADAS_ES.md`): E1 vs the Eloundou human
  labels ρ = 0.40; K1 vs the non-routine analytical index ρ = 0.67. One
  hypothesis failed (K1 vs routine cognitive, ρ = −0.21) and one is borderline
  (K1 vs Job Zone, ρ = 0.70); both are reported in
  `docs/grading/RESULTADOS_capa1_ES.md`.
- `docs/grading/`: methodology v0.2, decision log, pre-registered
  hypotheses and validation results.
- Discriminant validation (issue #3, hypotheses H6–H8 registered before the run):
  K1 keeps its association with non-routine analytical work net of Job Zone
  (partial ρ = 0.28) and predicts the Eloundou human labels net of Job Zone
  (partial ρ = 0.40); K1 vs routine cognitive stays negative in non-manual
  occupations (ρ = −0.21), so that index is dropped as a reference for K
  (`docs/grading/RESULTADOS_discriminante_ES.md`).
- Layer U by sector and country (issue #7): `itea.grading.eurostat.adoption_by_sector`,
  `latest` and `utilisation` (Eurostat `isoc_eb_iipn2`, `isoc_eb_ain2`, `isoc_eb_icsn2`;
  35 territories × 13 NACE sectors; U = adoption × depth at 0.10 / 0.27 / 0.35).
  The financial sector (NACE K) is not covered by these tables.
- English documentation of the grading pipeline (issue #9):
  `docs/grading/METHODOLOGY_v0.2_EN.md` and `VALIDATION_RESULTS_EN.md`.
- R reference implementation checked in CI (issue #11): `tests/test_v3_r_parity.py`
  runs `code/v3/itea_functions_v3.R` and compares it with `itea.v3`.
- Optional dependency group `semantic` for grading layers 2–3.
- **Methodology v4.0** (`docs/methodology/ITEA_v4_0_Metodologia_ES.docx` and
  `ITEA_v4_0_Methodology_EN.docx`, with Markdown sources): OAXI-EU, software
  and the v4.1 grading programme; extends the v3.0 Consolidated Methodology.
- **Data workbook v4.0** (`data/processed/ITEA_v4_0_Workbook.xlsx`), generated
  from the canonical CSV outputs by `scripts/build_workbook_v4.py`: OAXI-EU
  with ISCO-08 titles, JRC validation, crosswalk, task grades, hypotheses H1–H8,
  layer U and vendor presence.
- README (EN, ES, PT, ZH) and project web page updated for v4.0 and the v4.1
  work in progress.
- `itea.grading.rebuild` and `scripts/grading/build_oaxi_eu_v41.py`: OAXI-EU
  built from itea.grading task grades instead of AXI (same roll-up and
  crosswalk, κ kept at 0.40, decision D17). Preview with the structural layer:
  Spearman 0.75 with the v4.0 index, 3 of the top 20 shared
  (`docs/grading/RESULTADOS_oaxi_eu_v41_ES.md`). The data workbook adds this
  table as a separate sheet when it exists.
- Grading layer 2 (issue #1): `itea.grading.semantic` and
  `scripts/grading/build_semantic.py` / `validate_semantic.py` link each O*NET
  task to ESCO v1.2.1 concepts with sentence embeddings (all-mpnet-base-v2,
  pinned revision, run locally) and derive K2 and E2 from official ESCO
  groups. Against hypotheses registered beforehand: K2 discriminates within
  activities (within-GWA variance 0.75 vs 0.07) and is less tied to skill level
  (ρ 0.41 vs 0.70 with Job Zone); E2 adds little to E1 (H10 failed). The
  registered global threshold leaves 46 % of tasks unlinked, so the layer is
  not yet used in the index (decisions D18, D19;
  `docs/grading/RESULTADOS_capa2_ES.md`).
- Layer 2, variant B (registered after variant A's coverage problem): the 5
  nearest ESCO concepts per task, full coverage; passes H9B–H13B, and E1+E2
  improves convergence with the Eloundou labels (ρ 0.454).
- Grading layer 3 (issue #2): `itea.grading.anchors` and
  `scripts/grading/build_anchors.py` / `validate_anchors.py`, anchored
  zero-shot NLI (deberta-v3-large-zeroshot-v2.0-c, MIT, run locally). It fails
  its registered hypotheses H14–H17 and is reported as a negative result; it
  does not enter the index (decision D20).
- Composite and **OAXI-EU v4.1** (issue #4): `itea.grading.combine` and
  `scripts/grading/build_v41.py`. K = K1+K2, E = E1+E2 (percentile ranks, equal
  weights), κ 0.40, with a 1,000-draw Monte Carlo over method choices that
  reports a 5–95 % band for every ISCO index value and rank. H18–H20 hold:
  final E vs Eloundou ρ 0.454, final K vs non-routine analytical net of Job
  Zone 0.26, median rank band 66 of 428 places. Spearman 0.80 with the v4.0
  index (`docs/grading/RESULTADOS_capa3_y_v41_ES.md`).
- The data workbook now carries OAXI-EU v4.1 with its uncertainty, the v4.1
  task grades and hypotheses H1–H20.
- **Full provenance note for the legacy AXI grades**
  (`docs/grading/AXI_PROVENANCE_EN.md`, `PROCEDENCIA_AXI_ES.md`): the step that
  assigned technology patterns to tasks was not recorded and cannot be re-run;
  forensic properties of the data; reliability against automated coders
  (α 0.50 / 0.35); and a July 2026 human panel and documented AI agents that
  agree with each other (ρ 0.39) but not with the AXI codifiability grade
  (ρ 0.08), so AXI's task-level codifiability is not validated. The dataset
  note (`src/itea/data/README_AXI.md`) states this in full, and earlier ITEA
  descriptions of the grades are corrected.
- The research report behind the grading design
  (`docs/grading/INFORME_investigacion_2026-10-23.md`) and the English summary
  of hypotheses H9–H20 (`VALIDATION_RESULTS_EN.md`).
- Optional employment weights for the crosswalk (`build_crosswalk(..., isco_weights=)`,
  `reweight`); equal split remains the default.
- `itea validate` and `itea.datasets` (`axi_path`, `jrc_benchmark`).
- Test suite in `tests/` (crosswalk, roll-up, weights, packaged data, index
  properties, end-to-end reproduction of the published table, benchmark
  convergence and κ calibration) and GitHub Actions CI on Python 3.10, 3.12
  and 3.13, plus a job that installs the wheel outside the source tree.
- `CONTRIBUTING.md`, `NOTICE.md`.

### Changed

- CI actions moved to versions that run on Node 24 (checkout v5, setup-python v6).
- Corrected four Eurostat figures that had been misrounded (e.g. EU-27 ERP
  adoption 46.45 % is 46.5 %, not 46.4 %).
- The embedding cache is keyed by model name, so a different model never
  reuses another model's vectors.

- `scipy` is now a declared dependency (pandas needs it for Spearman
  correlations in `itea.oaxi_eu` and `itea.grading.validation`); its absence
  made the first CI run fail on a clean install.

- **`itea.v3.itea_v3` now uses the sample standard deviation**, as `sd()` in the
  R reference implementation. The previous population SD gave results that
  differ by up to 7·10⁻⁵ when components have different missing values; with
  complete data the two are identical (the min–max step cancels the factor).
  Found by the new R ↔ Python parity test.

- **SOC → ISCO-08 crosswalk.** The beta used a one-to-one mapping typed into a
  wage spreadsheet, which misassigned some occupations (e.g. Management
  Analysts 13-1111 → 2423 instead of 2421) and left 48 managerial and
  professional ISCO groups without O\*NET data (2412, 2413, 2421, 2514…). It is replaced by the official BLS tables, chained many-to-many
  with equal weights.
- **Coverage.** The beta restricted the index to the 784 occupations with
  realised-employment data, a filter of one validation analysis. OAXI-EU now
  uses all 923 O\*NET-SOC occupations reached by the activity roll-up:
  **428 ISCO-08 unit groups** (was 237).
- **Convergence with JRC145832** (ISCO-3): Pearson 0.703 → **0.736**,
  Spearman 0.782 → **0.819**, groups matched 103 → **127**, now reproducible
  from the public JRC table. The κ = 0.40
  weight is kept: the calibration optimum is flat between 0.3 and 0.4.
- The v3.0 Python implementation moves to `itea.v3`;
  `code/v3/itea_functions_v3.py` remains as a compatibility shim.
- `LICENSE` is now the plain MIT text (data notices moved to `NOTICE.md`).
- Contact address: aval@epistemica.eu.
- Minimum Python version 3.10 (3.9 reached end of life in October 2025).

### Fixed

- README: AIOE overlap is 769 occupations (pairwise); paper titles and DOIs
  of 8A/8B/8C aligned with Zenodo; the DOI 10.5281/zenodo.19592542 cited for
  *The Structural Flaw* does not exist (correct: 10.5281/zenodo.19693452).

---

## [v4.0] — 2026-06-18 (documentación pública teórica de la actualización v4.0)

Documentación **teórica y conceptual** de la actualización v4.0, en
[`v4.0/`](v4.0/) ([EN](v4.0/RELEASE_v4.0.md) · [ES](v4.0/RELEASE_v4.0_ES.md) · [PT](v4.0/RELEASE_v4.0_PT.md) · [中文](v4.0/RELEASE_v4.0_ZH.md)):
novedades y principales hallazgos de los tres entornos —**ITEA US** (≈ v3.0, mejoras
puntuales), **ITEA ESCO (Europa) v1.2** y **ITEA Bridge (US–UE) v1.2**— sin tablas ni
datos operativos. Acceso a datos, índices a nivel tarea/ocupación e información operativa
**bajo solicitud** (anti-scooping): **alb.valencia@gmail.com**. La GitHub Page se actualizará
por separado.

---

## [v4.0-beta] — 2026-05-31 (Work In Progress, línea europea)

Línea de desarrollo **ITEA-EU** (integración ESCO/ISCO) publicada como **beta**
en la carpeta [`v4.0/`](v4.0/). Resultados preliminares, no revisados por pares;
la release estable del marco sigue siendo v3.0. Trazabilidad detallada de
versiones del marco y de cada componente en [`v4.0/CHANGELOG.md`](v4.0/CHANGELOG.md).

### Added

- Arquitectura de 3 entornos (ITEA-US / ITEA-UE / ITEA BRIDGE US–UE) sobre eje ISCO-08.
- Índice europeo **OAXI-EU** preliminar (v0-carryover) y mapeo tarea→competencia (v1.0-tfidf).
- Pipeline reproducible, documentos de diseño y dashboard interactivo (en `v4.0/`).
- Atribución de fuentes (ESCO v1.2.1 y O*NET, ambas CC BY 4.0) verificada en origen.

---

## [Unreleased] — 2026-05-07 (repository housekeeping, no methodological change)

### Added

- `versions/v2.0/` — archival of the original v2.0 deliverables (Methodology
  EN/ES, Research Data Workbook v2.0) for replication of pre-v3.0 results.
- `versions/v2.1/` — archival of the v2.1 update memorandum and Research
  Data Workbook v2.1.
- `versions/v3.0_originals/` — pre-consolidation v3.0 source documents
  (byte-identical to the active v3.0 release; preserved for upload provenance).
- `versions/README.md` — index of the archival folder with file-by-file SHA-256
  matches against the active release.
- `docs/legacy/working/` — pre-publication internal working documents
  (`Diagnostico_Framework_ITEA_2026-04-29.docx`, `ITEA_Development_Roadmap_v2.md`,
  `paper.md` working draft) moved out of the repository root to keep the
  published surface clean.
- `docs/DEPLOYMENT_REPORT_2026-05-07.md` — operational record of the
  v3.0 repository deployment, with SHA-256 verification of all 14 files in
  `MANIFEST.json`.
- `docs/JOSS_SUBMISSION_CHECKLIST.md` — review-readiness matrix against the
  Journal of Open Source Software submission requirements.
- `docs/ZENODO_DEPOSIT_GUIDE.md` and `docs/zenodo_metadata.json` — operational
  guide and machine-readable metadata for the Zenodo deposit workflow.

### Verified

- All 14 files declared in `MANIFEST.json` re-hashed (SHA-256) after deployment;
  every digest matched the manifest.

### Notes

- This entry documents *structural* repository changes only. No methodological,
  data, code, or numerical change relative to the v3.0 release of 2026-04-30.

---

## [3.0] — 2026-04-30

### What changed and why

Major methodological revision motivated by a documented case study of three research
papers (the trilogy 8A/8B/8C) that put the framework into active empirical use.
This release also unifies the operational v1.x and methodological v2.x numbering
lines onto a single version, archiving v1.45 as the `v1.45-legacy` tag for replication.

### Added

- **z-score ITEA aggregation**: components (EAC, EIG, EIA) are normalised to z-scores
  before equal-weight averaging, with a final min-max projection to [0, 1]. This
  corrects the variance asymmetry pathology of the v2.1 equal-weight-in-[0,1]
  approach. Validation gain: r(ITEA, AEI) 0.71 → 0.89; r(ITEA, AIOE) 0.36 → 0.43.
  Motivated by Paper 8A "The Structural Flaw" (García-Lluis Valencia, 2026a) — see
  §4.4 of the Consolidated Methodology for the case-study reasoning.
- **IRA with triple residualisation**: the IRO_v1.45 component is now residualised
  against the full set of structural moderators (GEE, ITEA, ICT) rather than against
  GEE alone. This achieves clean discriminant validity while preserving 84% of the
  original IRA variance. Validation gain: r(IRA, ITEA) 0.28 → 0.14; r(IRA, ICT) 0.10
  → 0.06. Motivated by Paper 8C "QE and Senior Workforce Restructuring" — see §5.4
  of the Consolidated Methodology.
- **OAEI dual-variant architecture**:
  - **OAEI v3.0 multiplicative (canonical)** preserves the multiplicative structure
    of v2.1 with the upgraded ITEA input. Used for backward compatibility with the
    trilogy papers.
  - **OAEI v3.0+ additive (alternative)**: weights 0.5·GEE + 0.3·ITEA + 0.2·ICT·(1−IPI),
    used for criterion-validity-priority applications (improves r(OAEI, Wage) from
    0.58 to 0.66, preserves AIOE convergence at 0.80). Motivated by Paper 8B "Beyond
    the Pigouvian Trap" — see §6.5 of the Consolidated Methodology.
- **`docs/ITEA_v3_0_Consolidated_Methodology.pdf`**: single authoritative methodology
  document superseding v2.0 and v2.1; introduces formal deprecation declaration,
  trilogy case study, and unified numbering narrative.
- **`code/v3/itea_functions_v3.R`** and **`code/v3/itea_functions_v3.py`**: reference
  implementations reproducing the workbook values within machine precision.
- **`code/v3/tests/test_itea_v3.py`**: pytest test suite (14 tests, all passing).
- **`paper/paper.md`**: JOSS submission draft (1,000 words).
- **CITATION.cff** for GitHub-native citation metadata.
- **MANIFEST.json** with SHA-256 checksums for Zenodo deposit verification.
- **README.md, README_ES.md, README_PT.md, README_ZH.md** rewritten for v3.0 with
  trilogy case study front and centre.

### Deprecated

- ITEA Methodology v2.0 (April 2026) — superseded by Consolidated Methodology §3.
- ITEA Memorandum v2.1 (April 2026) — superseded by Consolidated Methodology §3.3 and §9.
- ITEA Methodology v3.0 (original release, April 2026) — content fully integrated
  into the Consolidated Edition.
- `Research_Data_Workbook_ITEA_v1.x` series — preserved in `data/legacy/` for
  replication of v1.x results.
- `itea_functions_v1.45.{R, py}` — preserved in `code/legacy/`.

### Validation summary

External convergent validation: **r(OAEI v3.0+, AIOE) = 0.797** over 769 common
SOC 6-digit occupations. Six of eight psychometric criteria show net improvement
under v3.0; two are stable; two show small decreases under the multiplicative
variant only (recovered by the additive variant). Full validation table in §7 of
the Consolidated Methodology.

---

## [2.1] — 2026-04 (DEPRECATED)

### Changed

- Data refresh from O\*NET 29.1 to **O\*NET 30.2** (February 2026 release).
- All indicators recomputed on 30.2 data; cross-version stability r(v2.0, v2.1) ≈ 0.99.

### Deprecated by

- v3.0 Consolidated Methodology, §3.3 (data sources) and §9 (migration guide).

---

## [2.0] — 2026-04 (DEPRECATED)

### Added

- First formal methodology paper consolidating the eight-indicator architecture.
- Formative/reflective indicator typology (Bollen & Lennox, 1991).
- Six-criterion psychometric validation matrix.

### Deprecated by

- v3.0 Consolidated Methodology, §3 (conceptual foundations preserved with minimal
  change) and §4–§6 (revised aggregation methods).

---

## [1.45] — 2025-10 (LEGACY)

### Changed

- IRO indicator revised from 4 to 2 items (institutional security simplification).
- GEE recalibrated with **dual OLS+ordinal** approach (last v1.x methodological
  refinement before the v2.x methodological line opened).

### Status

**ARCHIVED as `v1.45-legacy` tag.** Researchers reproducing results published using
v1.x specifications should check out this tag. Located in `data/legacy/` and
`code/legacy/`.

---

## [1.3] — 2025-04

### Added

- **IPI (Interpersonal Presence Index)** as a new formative indicator capturing
  the physical-presence barrier to algorithmic crystallisation.
- IFS extracted to its own confidence-interval framework.

---

## [1.2] — 2025-03

### Changed

- **GEE OLS calibration** applied: validation correlation jumped from ρ = 0.259 to
  ρ = 0.927 against U.S. Census ACS educational attainment microdata.
- IMO redesigned as a **Hurdle model with cap**, addressing the zero-inflation
  characteristic of occupational mutation events.

### Notable

This release marked the transition from "experimental" to "calibrated" framework.

---

## [1.1] — 2024-09

### Changed

- IRO indicator now incorporates institutional security as a sub-component.
- ITEA temporarily moved to additive form (later reverted in v1.2).

---

## [1.0] — 2024-03

### Added

- Initial release: 8 indicators (ITEA, IRO, ICT, IFS, IPI, IEF, GEE, IMO).
- Source data: O\*NET 28.x.
- 1,016 SOC 6-digit occupations.

---

[3.0]: https://github.com/Aval22/ITEA/releases/tag/v3.0
[2.1]: https://github.com/Aval22/ITEA/releases/tag/v2.1
[2.0]: https://github.com/Aval22/ITEA/releases/tag/v2.0
[1.45]: https://github.com/Aval22/ITEA/releases/tag/v1.45-legacy
[1.3]: https://github.com/Aval22/ITEA/releases/tag/v1.3
[1.2]: https://github.com/Aval22/ITEA/releases/tag/v1.2
[1.1]: https://github.com/Aval22/ITEA/releases/tag/v1.1
[1.0]: https://github.com/Aval22/ITEA/releases/tag/v1.0
