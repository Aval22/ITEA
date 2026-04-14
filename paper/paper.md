---
title: 'ITEA: A Multidimensional Framework for Measuring Occupational Exposure to Automation'
tags:
  - R
  - Python
  - automation
  - labor economics
  - occupational analysis
  - artificial intelligence
  - O*NET
authors:
  - name: Alberto García-Lluis Valencia
    orcid: 0009-0003-1438-1633
    affiliation: 1
affiliations:
  - name: Universidad Rey Juan Carlos, Madrid, Spain
    index: 1
date: 14 April 2026
bibliography: paper.bib
---

# Summary

The Triple Exposure to Automation Index (ITEA) is an open-source framework, implemented in both R and Python, that provides eight complementary indicators for measuring occupational exposure to automation and artificial intelligence. Unlike binary classification approaches that label occupations as simply "automatable" or "not automatable" [@frey2017future], ITEA offers a multidimensional, continuous, and granular assessment across 1,016 occupations using data from O\*NET 2024 (v29.1).

The eight indicators capture distinct dimensions of the automation landscape: exposure to cognitive, general, and AI-specific automation (ITEA); occupational resilience through adaptability and institutional protection (IRO); technical complexity requiring non-routine judgment (ICT); social friction from human interaction demands (IFS); physical presence requirements (IPI); functional specificity of knowledge (IEF); education and experience requirements (GEE); and occupational mutation tracking task evolution over time (IMO). Each indicator is validated through appropriate statistical methods: Cronbach's alpha for reflective constructs (IRO α=0.842, IFS α=0.749, IEF α=0.919), variance inflation factors for formative indices (ITEA VIF=1.21, ICT VIF=1.15), OLS calibration against Job Zone benchmarks (GEE ρ=0.927), and Hurdle models for zero-inflated distributions (IMO, 76.9% zeros).

The software includes functions for computing all indicators, validation utilities following the `performance` package standards [@ludecke2021performance], cross-language consistency tests, and an interactive Streamlit dashboard for exploration of results (https://itea-framework.streamlit.app).

# Statement of Need

The accelerating deployment of artificial intelligence in workplaces demands tools that can assess automation risk at the occupational level with sufficient granularity for policy analysis, workforce planning, and academic research. Existing approaches present three fundamental limitations.

First, the influential Frey and Osborne framework [@frey2017future] provides only a binary classification of occupations, losing information about the degree, type, and trajectory of automation exposure. Second, most indices are unidimensional, reducing a complex, multifaceted phenomenon to a single score and thereby conflating distinct mechanisms such as cognitive automation, physical robotization, and AI-driven task substitution. Third, existing tools are predominantly static, offering a snapshot of current automation probability without capturing occupational evolution.

ITEA addresses these gaps by providing researchers and policymakers with a validated, multidimensional toolkit. The target users include labor economists studying automation impacts, human resource professionals assessing workforce vulnerability, policymakers designing reskilling programs, and doctoral researchers requiring granular occupational data for panel econometrics. The framework has been applied in ongoing doctoral research at Universidad Rey Juan Carlos to study the interaction between quantitative easing policies and senior workforce displacement [@garcia2026qe], and to analyze the Spanish labor market using Infoempleo-Adecco survey data.

# State of the Field

Several tools exist for measuring automation exposure. The seminal work by @frey2017future estimated automation probabilities for 702 occupations using expert elicitation, producing a widely cited but binary and static index. @autor2015why provided a task-based framework distinguishing routine from non-routine tasks, but without a computational implementation. @acemoglu2018race formalized the race between automation and new task creation, offering theoretical insights but no occupational-level software tool.

The O\*NET database itself [@onet2024] provides the underlying task and skill data but requires substantial processing to derive automation indicators. @ludecke2021performance established validation standards for psychological and social science instruments that ITEA follows.

ITEA differentiates itself in four ways: (1) it provides eight distinct indicators rather than a single score, enabling researchers to decompose automation risk into its constituent dimensions; (2) it covers 1,016 occupations with continuous scores rather than binary classifications; (3) it includes an occupational mutation index (IMO) that tracks how occupations evolve over time; and (4) it offers dual R/Python implementations with automated cross-language validation, ensuring reproducibility across research environments.

# Software Design

The ITEA framework is organized around three design principles: transparency (all formulas are explicit and documented), reproducibility (dual-language implementation with cross-validation), and multidimensionality (eight indicators capturing distinct constructs).

**Indicator taxonomy.** The framework distinguishes between formative indicators (ITEA, ICT, IPI), where components cause the construct and validation relies on VIF analysis; reflective indicators (IRO, IFS, IEF), where the construct causes the observed items and validation uses Cronbach's alpha; and hybrid indicators (GEE via OLS calibration, IMO via Hurdle model).

**Architecture.** Each indicator is implemented as a standalone function accepting O\*NET-derived inputs and returning a normalized [0,1] score. The R implementation (`code/R/itea_functions_v1.45.R`) and Python implementation (`code/Python/itea_functions_v1_45.py`) are structurally parallel, with automated tests verifying cross-language consistency to six decimal places.

**Data pipeline.** The processed dataset (`data/processed/Research_Data_Workbook_ITEA_v1.35.xlsx`) contains 1,016 occupations with all indicator values, component scores, and metadata. An interactive Streamlit dashboard provides five exploration views: sortable table with progress bars, configurable scatter plot, individual occupation radar profile, sector-level analysis with box plots, and multi-occupation comparison.

**Versioning.** The framework follows semantic versioning with documented changes from v1.0 through v1.45. Key improvements include the OLS calibration of GEE (v1.2, raising ρ from 0.259 to 0.927), the extraction of physical presence into a dedicated IPI indicator (v1.3), and the reduction of cognitive complexity items in IRO to decrease construct overlap (v1.45).

# Research Impact Statement

The ITEA framework is currently deployed in three active research streams within a doctoral program at Universidad Rey Juan Carlos:

1. **Quantitative easing and senior employment restructuring** [@garcia2026qe]: ITEA indicators (particularly the wage-weighted ITEA and IEF) are used to quantify heterogeneous automation incentives across 923 occupations in a panel of 82 publicly listed firms from the Euro Stoxx 50, FTSE 100, S&P 500, and Nikkei 225.

2. **Spanish labor market validation**: ITEA indicators are cross-referenced with Infoempleo-Adecco 2023-2024 survey data (n>3,000 firms) to validate automation adoption patterns, training gaps, and sectoral wage structures against framework predictions.

3. **Algorithmic expropriation and contractual models**: The AEI (Algorithmic Expropriation Index), derived from ITEA, serves as the dependent variable in a three-pillar contractual model targeting publication in *Industrial and Corporate Change*.

The interactive dashboard (https://itea-framework.streamlit.app) provides public access to all indicator values, enabling independent researchers to explore and build upon the framework.

# AI Usage Disclosure

Generative AI tools (Claude, Anthropic) were used to assist with code generation, documentation drafting, and data visualization during the development of this software. All AI-generated content was reviewed, validated, and modified by the author. The core methodological decisions, indicator design, validation strategy, and research applications were conceived and directed by the author. The statistical formulas, weight calibrations, and empirical validations were executed on real O\*NET data with results independently verified.

# Acknowledgements

The author acknowledges the U.S. Department of Labor and the National Center for O\*NET Development for making occupational data publicly available. This work is part of a doctoral research program at Universidad Rey Juan Carlos, Madrid.

# References
