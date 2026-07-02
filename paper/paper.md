---
title: "ITEA Framework: A multidimensional system for measuring occupational exposure and algorithmic expropriability under the Agentic AI regime"
tags:
  - R
  - Python
  - labor economics
  - automation
  - artificial intelligence
  - O*NET
  - psychometric validation
authors:
  - name: Alberto García-Lluis Valencia
    orcid: 0009-0003-1438-1633
    affiliation: 1
    corresponding: true
affiliations:
  - name: Universidad Rey Juan Carlos, Madrid, Spain
    index: 1
    ror: 01v5cv687
date: 30 April 2026
bibliography: paper.bib
---

# Summary

The ITEA Framework is an open multidimensional system for measuring occupational
exposure and algorithmic expropriability under the Agentic AI regime, distinct from
but complementary to task-level automation indices in the Frey-Osborne tradition
[@frey2017future] or ability-based exposure measures such as the AI Occupational
Exposure index of @felten2021occupational. Version 3.0 covers all 1,016 SOC 6-digit
occupations of O\*NET 30.2, providing ten complementary indicators (eight original
plus two introduced in v3.0), four reference R/Python implementations, a
twelve-sheet validated dataset, and a Streamlit dashboard. External convergent
validation against the AIOE benchmark over 769 common SOC 6-digit occupations
yields *r* = 0.797.

# Statement of need

Existing occupational automation indices fall into two methodological families.
The first, exemplified by @frey2017future and @webb2020impact, scores tasks for
their direct technical automatability. The second, exemplified by
@felten2021occupational and @eloundou2024gpts, scores occupations for their
exposure to AI capabilities at the ability level. Both families measure exposure
under the *generative* AI regime — whether tasks or abilities are automatable
using current or near-term AI tools. Neither captures the distinct mechanism that
defines the *Agentic* AI regime: the rate at which a worker's intellectual capital
can be externalised, combined and internalised by autonomous AI systems into firm-
level proprietary assets that persist beyond individual worker tenure
[@nonaka1995knowledge].

The ITEA Framework was developed to fill this measurement gap. Its primary use
case is research on labour-contract redesign and monetary-policy transmission
under sustained AI exposure: the framework is the empirical instrument for a
trilogy of research papers (the "trilogy" referenced throughout the
documentation) that motivate v3.0's design choices and demonstrate the
framework's active use in research [@gll2026structural; @gll2026tokenised;
@gll2026qe].

The framework is intended for three audiences. First, labour and monetary
economists requiring an occupation-level exposure measure orthogonal to
qualification and complexity. Second, policy analysts at national statistical
agencies and labour ministries requiring a granular ranking of populations
likely to face IC-crystallisation pressure. Third, replication researchers
building on the trilogy or independent papers that cite ITEA as input variable.

# Indicators and methodology

ITEA v3.0 produces ten indicators per occupation. The four central composites
are:

- **ITEA** (Triple Index of Exposure to Automation) — z-score-normalised equal-
  weight aggregation of EAC, EIG and EIA components.
- **IRA** (Adaptive Resilience Index) — 0.6·CA + 0.4·IRO_residual where
  IRO_residual is the residual of OLS(IRO ~ GEE + ITEA + ICT), implementing
  triple residualisation against all structural moderators.
- **OAEI v3.0 multiplicative** — ITEA × GEE × ICT × (1 − IPI) min-max-projected
  to [1, 100], the canonical composite preserving compatibility with cited
  research.
- **OAEI v3.0+ additive** — 0.5·GEE + 0.3·ITEA + 0.2·ICT·(1 − IPI), an
  alternative for criterion-validity-priority applications.

The framework anchors in O\*NET 30.2 (1,016 SOC 6-digit occupations, 47,810 task
statements) and integrates BLS OEWS wage data. External convergent validation
against the AIOE benchmark of @felten2021occupational confirms that ITEA
captures a related-but-distinct construct: r(OAEI v3.0+, AIOE) = 0.797 over the
769 common occupations.

# State of the field and ITEA's contribution

The literature provides binary task-level indices [@frey2017future],
continuous ability-level indices [@felten2021occupational; @brynjolfsson2025generative],
sectoral panels [@acemoglu2018race], and aggregate macroeconomic models
[@acemoglu2025simple]. ITEA fills the granularity-and-mechanism gap by providing
occupation-level measurement under the Agentic regime, with explicit psychometric
validation including discriminant validity against qualification and technical
complexity.

The four-criterion validation matrix shows ITEA v3.0 improving on v2.1 across
six of eight psychometric criteria, with the dual OAEI architecture supporting
both internal-coherence-priority and external-convergence-priority applications.
The full validation table, eight criteria including convergent, discriminant,
criterion and stability validity, is reported in the Consolidated Methodology
[@itea_methodology_v3].

# Software design

The repository follows a layered structure: a primary Excel workbook
(`data/processed/ITEA_v3_0_Workbook.xlsx`, twelve sheets, 1,016 rows × 27
columns) is the canonical data artefact; reference R and Python implementations
(`code/v3/`) reproduce the workbook values to machine precision (`Δ < 10⁻¹⁴`);
a 14-test pytest suite verifies indicator properties, NaN handling, weight
preservation and end-to-end reconciliation; a SHA-256 manifest supports Zenodo
deposit verification.

The `v1.45-legacy` git tag preserves the previous release for replication of
v1.x results. The `docs/MIGRATION.md` provides step-by-step guidance for
researchers updating pipelines from v1.45.

# Project history and the v3.0 case study

The framework has evolved across nine documented versions since March 2024. The
v3.0 release unifies two parallel numbering lines — operational v1.x (data and
code) and methodological v2.x (academic papers) — onto a single version, with
deprecation declarations and trilogy case studies that document the principled
reasoning behind each major revision. The full evolution narrative, including
how each of the three central v3.0 changes was motivated by a specific empirical
finding from one of the trilogy papers, is documented in §2 and §4.4–§5.4–§6.5
of the Consolidated Methodology [@itea_methodology_v3].

# Acknowledgements

Parts of the v1.x operational releases were developed in the Universidad Rey
Juan Carlos doctoral research environment. The author thanks the participants
of related URJC research seminars for feedback on earlier versions, and
acknowledges the use of generative AI tools (Claude, Anthropic) for data
management, table organisation, and quantitative consistency checks during the
v3.0 revision; all theoretical frameworks, analytical decisions, and
interpretations remain the sole responsibility of the author.

# References
