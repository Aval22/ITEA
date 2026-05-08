---
title: 'ITEA: A Multidimensional Framework for Measuring Occupational Exposure to Automation under Agentic AI'
tags:
  - R
  - Python
  - automation
  - labor economics
  - occupational analysis
  - agentic AI
  - O*NET
authors:
  - name: Alberto García-Lluis Valencia
    orcid: 0009-0003-1438-1633
    affiliation: 1
affiliations:
  - name: Universidad Rey Juan Carlos, Madrid, Spain
    index: 1
date: 31 October 2026
bibliography: paper.bib
---

# Summary

The Triple Exposure to Automation Index (ITEA) is an open-source framework, implemented in both R and Python, that provides eight complementary indicators for measuring occupational exposure to automation and artificial intelligence under the new regime of *agentic AI*. Unlike binary classification approaches that label occupations as simply "automatable" or "not automatable" [@frey2017future], ITEA delivers a multidimensional, continuous, and granular assessment across 1,016 published O\*NET occupations (846 with complete data across the four sources used by the framework), based on O\*NET database release 30.2 [@onet2026database].

The eight indicators capture distinct dimensions of the automation landscape: triple exposure to cognitive, general, and AI-specific automation (ITEA); adaptive resilience independent of formal qualification (IRA v2.0, replacing the IRO of v1.45); technical complexity requiring non-routine judgment (ICT); social friction from human interaction demands (IFS); face-to-face physical presence requirements (IPI); functional specificity of task knowledge (IEF); education and experience requirements calibrated against Job Zones (GEE); and occupational mutation tracking task evolution over time (IMO). Two auxiliary constructs complete the framework: the Algorithmic Expropriation Index (AEI), built from a granular task-level classification of 47,810 O\*NET task statements along *automation grade* and *capital-intelligence transfer grade* axes, and the Operational Algorithmic Expropriation Index (OAEI v2.0), a multiplicative composite rescaled to [1, 100] that operationalises the severity of contractual displacement under agentic AI.

Each indicator is validated through statistical methods appropriate to its measurement-theoretic type [@diamantopoulos2001index]: Cronbach's alpha for reflective constructs (IFS α=0.749, IEF α=0.919); variance inflation factors for formative indices (ITEA VIF=1.21, ICT VIF=1.15); OLS calibration against Job Zone benchmarks (GEE ρ=0.927); a Hurdle model for zero-inflated distributions (IMO, 76.9% zeros); and convergent-validity correlation against the AEI for the central exposure indicator (r(ITEA, AEI)=0.72; r(EIA, AEI)=0.94). The IRA v2.0, a residualised construct by design, is validated through discriminant correlation against GEE (r=0.43, down from r=0.904 of the IRO v1.45 it replaces) and through a quadrant analysis on GEE × IRA that identifies the "high human capital × high adaptive capacity" cell as the locus of maximum operational expropriation under agentic regimes (mean OAEI=61.5).

The software is distributed as parallel R and Python implementations with cross-language consistency tests, an interactive Streamlit dashboard for occupational exploration ([itea-framework.streamlit.app](https://itea-framework.streamlit.app)), reproducible ingestion pipelines from raw O\*NET text files, and a Zenodo-archived release for citation [@iteazenodo2026]. The framework follows validation standards established by the `performance` R package [@ludecke2021performance].

# Statement of Need

The accelerating deployment of artificial intelligence in workplaces — and in particular the diffusion of *agentic AI* during 2025–2026 [@bain2025; @mckinsey2025; @ibm2025; @microsoft2025] — demands occupational-level tools that can assess exposure with sufficient granularity for policy analysis, workforce planning, and academic research. Existing approaches present three fundamental limitations.

First, the influential Frey-Osborne framework [@frey2017future] provides only a binary classification of occupations, losing information about the degree, type, and trajectory of automation exposure. Second, most indices are unidimensional, reducing a multifaceted phenomenon to a single score and conflating distinct mechanisms — cognitive automation, physical robotisation, AI task substitution, and contractual expropriation. Third, existing tools are predominantly static, capturing a snapshot of current automation probability without incorporating occupational mutation or the institutional moderators that determine downstream labour-market outcomes.

ITEA addresses these gaps by providing researchers and policymakers with a validated multidimensional toolkit. The target users include labour economists studying automation and inequality [@autor2015why; @acemoglu2018race; @acemoglu2025tasks], human-resource professionals assessing workforce vulnerability, policymakers designing reskilling programs, and doctoral researchers requiring granular occupational data for panel econometrics. The framework has been applied in ongoing doctoral research at Universidad Rey Juan Carlos to study the interaction between quantitative-easing policies and senior-workforce displacement, and to analyse the Spanish labour market against Infoempleo-Adecco 2023–2024 survey data.

# State of the Field

Several tools exist for measuring automation exposure. @frey2017future estimated automation probabilities for 702 occupations using expert elicitation, producing a widely cited but binary index. @autor2015why provided a task-based framework distinguishing routine from non-routine tasks, but without a computational implementation. @acemoglu2018race and @acemoglu2025tasks formalise the race between automation and new task creation, offering theoretical insight without occupation-level software. @eloundou2024gpts and @brynjolfsson2025genai provide task-exposure estimates for generative AI but do not articulate adaptive resilience, mutation, or the contractual mechanism of expropriation that agentic systems make salient.

The O\*NET database itself [@onet2026database] supplies the underlying task and skill data but requires substantial processing to derive automation indicators. @ludecke2021performance establishes validation standards for psychological and social-science instruments that ITEA follows.

ITEA differentiates itself in five ways. (i) It provides eight complementary indicators rather than a single score, decomposing automation risk into its constituent dimensions. (ii) It introduces the AEI as an explicit task-level convergent criterion, validating the central ITEA construct against an independent classification of 47,810 task statements. (iii) The IRA v2.0 separates *adaptive resilience* (non-reducible to formal qualification) from human capital, an analytical move impossible under prior collinear formulations of resilience. (iv) The OAEI v2.0 introduces a multiplicative composite that operationalises *contractual* expropriation severity, linking the framework to the policy-design side of the labour-market debate. (v) Dual R and Python implementations with automated cross-language validation ensure reproducibility across research environments and computational platforms.

# Software Design

The ITEA framework is organised around three design principles: transparency (formulas and weights are explicit and documented), reproducibility (dual-language implementation with cross-validation, ingestion from raw O\*NET text files), and multidimensionality (eight indicators capturing distinct constructs).

**Indicator taxonomy.** The framework distinguishes formative indicators (ITEA, ICT, IPI), where the components cause the construct and validation relies on VIF analysis [@diamantopoulos2001index]; reflective indicators (IFS, IEF), where the construct causes the observed items and validation uses Cronbach's alpha; and hybrid constructs: GEE (OLS calibration against Job Zones), IMO (Hurdle model with capped log transformation), and IRA v2.0 (residualised composite of adaptive capacity and IRO-residualised-against-GEE).

**Architecture.** Each indicator is implemented as a standalone function accepting O\*NET-derived inputs and returning a normalised score. The R implementation (`code/R/itea_v2.R`) and Python implementation (`code/python/itea/__init__.py`, distributed as the `iteapy` package) are structurally parallel. Automated tests verify cross-language consistency to six decimal places (`tests/test_consistency.{R,py}`), and unit tests cover indicator formulas under boundary conditions, including the IRA residualisation and the AEI weighted sum.

**Data pipeline.** The repository includes the raw O\*NET 30.2 text files in `data/raw/onet_30_2/` together with their official Read Me, the ingestion script `code/ingest/build_workbook.py` that produces `data/processed/Research_Data_Workbook_ITEA_v2.xlsx` from the raw data, and the AEI source `data/processed/AEI_Unified_Analysis_v3_8.xlsx` with task-level classifications for 47,810 O\*NET tasks across 924 occupations.

**Dashboard.** A Streamlit application (`streamlit_app/app.py`, deployed at [itea-framework.streamlit.app](https://itea-framework.streamlit.app)) provides five exploration views: a sortable occupation table with progress bars; a configurable scatter plot for any indicator pair; an individual occupation radar profile; sector-level analysis with box plots; and multi-occupation comparison up to four roles.

**Versioning and provenance.** The framework follows semantic versioning. v1.0 (March 2024) was the initial release; v1.2 (March 2025) introduced the OLS calibration of GEE, raising ρ from 0.259 to 0.927; v1.3 (April 2026) extracted physical presence into the dedicated IPI indicator; v1.45 (April 2026, archived at Zenodo DOI 10.5281/zenodo.19578916) reduced the cognitive-complexity items in the IRO from four to two and is the version of the prior JOSS submission. **v2.0 (May 2026)** introduced three structural changes: (a) replacement of the IRO by the IRA after diagnosing collinearity with GEE that compromised discriminant validity; (b) explicit articulation of the AEI within the framework, with a documented derivation from the 47,810-task corpus; (c) recalibration of the OAEI to a [1, 100] interpretable scale. Subsequent minor releases between June and October 2026 added empirical validation of the IRA (v2.1), international crosswalks and Spanish-market validation (v2.2), the migration from O\*NET 29.1 to 30.2 with a reproducible ingestion pipeline (v2.3), installable R and Python packages (v2.4), and three vignettes plus a coverage report > 80 % (v2.5, the version of the present paper). The migration to O\*NET 30.2 was assessed for backward compatibility: inter-version Spearman rank correlations across the eight indicators ranged from 0.984 to 0.998, justifying retention of the v2.x line; a v3.0 breaking-change tag remains reserved for future O\*NET releases that fall below the 0.98 threshold.

# Quality Control

The validation metrics for the v2.0 release are summarised in Table 1. The N for psychometric validation differs by indicator: 1,016 occupations for indicators based solely on Skills, Knowledge, Abilities and Work Styles; 879 for criterion validity against wages; 923 for convergent validity against the AEI; and 846 for the OAEI composite (the intersection of the four sources).

| Indicator | Type | Metric | Value | Standard |
|-----------|------|--------|-------|----------|
| ITEA | Formative | VIF max | 1.21 | < 5 |
| IRA v2.0 | Residualised | r(IRA, GEE) | 0.43 | < 0.50 (discriminant) |
| ICT | Formative | VIF max | 1.15 | < 5 |
| IFS | Reflective | α Cronbach | 0.749 | > 0.70 |
| IPI | Formative | r(IPI, IFS) | −0.16 | < \|0.20\| (discriminant) |
| IEF | Reflective | α Cronbach | 0.919 | > 0.70 |
| GEE | OLS-calibrated | ρ Spearman vs Job Zone | 0.927 | > 0.50 |
| IMO | Hurdle | max ≤ 1.0 | 1.00 | ≤ 1.0 |
| ITEA | Convergent | r(ITEA, AEI) | 0.72 | > 0.50 |
| EIA | Convergent | r(EIA, AEI) | 0.94 | > 0.50 |

**Cronbach's α for the IRA.** The IRA v2.0 is by construction a residualised composite (60% normalised adaptive capacity + 40% min-max-normalised residual of IRO regressed on GEE) and the conventional α statistic is not directly applicable; discriminant validity against GEE is reported instead. The methodological document (`docs/methodology/ITEA_Metodologia_v2.docx`) details the derivation, the choice of weights, the bootstrap stability of the 60/40 weighting, and the limitations of the construct.

**Cross-language consistency.** Continuous integration (`.github/workflows/`) verifies that the R and Python implementations produce indicator values that agree to six decimal places on the 1,016-occupation reference dataset, that all psychometric statistics fall within their declared bounds, and that the Streamlit application boots and serves the index page in under five seconds in a clean environment.

# Research Impact Statement

The ITEA framework is currently deployed in three research streams in the doctoral programme at Universidad Rey Juan Carlos.

1. **Quantitative easing and senior employment restructuring** [@garcia2026qe]: ITEA indicators (in particular the wage-weighted ITEA and the IEF) are used to quantify heterogeneous automation incentives across 923 occupations within a panel of 82 publicly listed firms drawn from the Euro Stoxx 50, FTSE 100, S&P 500, and Nikkei 225.

2. **Spanish labour-market validation**: ITEA indicators are cross-referenced with the Infoempleo-Adecco 2023–2024 survey data (n > 3,000 firms) to test predicted automation-adoption patterns, training gaps and sectoral wage structures.

3. **Algorithmic expropriation under agentic AI** [@garcia2026paper8a; @garcia2026paper8b]: the OAEI v2.0 is the operational instrument for the trilogy on algorithmic expropriation, including the contractual model targeting *Industrial and Corporate Change* and the empirical limit-case study on the MBB triad over 2018–2026.

The interactive dashboard at [itea-framework.streamlit.app](https://itea-framework.streamlit.app) provides public access to all indicator values, enabling independent researchers to explore and build upon the framework. SOC↔CNO-11 and SOC↔ISCO-08 crosswalks are included in `data/crosswalks/` for application beyond the U.S. labour market.

# Maturity Statement

This v2.5.0 release is the consolidated successor of the v1.45 release submitted to JOSS in April 2026 and set aside for lack of demonstrable development history. The v2.0 cycle implemented a six-month public roadmap (May–October 2026) that delivered: structural reform of the framework (IRO→IRA, AEI articulation, OAEI rescaling) at v2.0.0; empirical validation of the IRA at v2.1.0; SOC↔CNO-11 and SOC↔ISCO-08 crosswalks at v2.2.0; migration to O\*NET 30.2 with reproducible ingestion pipeline at v2.3.0; installable R (`iteaR`) and Python (`iteapy`) packages at v2.4.0; three vignettes and test coverage > 80 % at v2.5.0. The roadmap, the changelog, and the migration notes from v1.45 to v2.0 are tracked in the repository (`docs/development/roadmap.md`, `CHANGELOG.md`, `docs/methodology/migration_v145_to_v2.md`). A complementary metapaper describing the methodology and data is currently under review at the *Journal of Open Research Software* (JORS); the present paper focuses on the software artifact.

# AI Usage Disclosure

Generative AI tools (Claude, Anthropic) were used to assist with code generation, documentation drafting, and data visualisation during the development of this software. All AI-generated content was reviewed, validated, and modified by the author. The core methodological decisions — the eight-indicator architecture, the IRO→IRA reconceptualisation, the AEI weighting scheme, the OAEI multiplicative form, the validation strategy, and the research applications — were conceived and directed by the author. All statistical formulas, weight calibrations, and empirical validations were executed on real O\*NET data and independently verified against the workbook computations.

# Acknowledgements

The author acknowledges the U.S. Department of Labor and the National Center for O\*NET Development for making occupational data publicly available, and the maintainers of the `tidyverse`, `psych`, `performance`, `numpy`, `pandas`, `scipy`, `plotly`, and `streamlit` projects for the open-source infrastructure on which ITEA depends. This work is part of a doctoral research programme at Universidad Rey Juan Carlos, Madrid.

# References
