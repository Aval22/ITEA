# Changelog

All notable changes to the ITEA Framework are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

External convergent validation: **r(OAEI v3.0+, AIOE) = 0.797** over 738 common
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
