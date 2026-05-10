# ITEA Framework — Triple Index of Exposure to Automation

🌐 **English** · [Español](README_ES.md) · [Português](README_PT.md) · [中文](README_ZH.md)

[![DOI](https://zenodo.org/badge/1210690701.svg)](https://doi.org/10.5281/zenodo.19578915)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![O*NET](https://img.shields.io/badge/O*NET-30.2-green)]()
[![Version](https://img.shields.io/badge/Version-3.0-blue)]()
[![JOSS](https://img.shields.io/badge/JOSS-submission%20mid--2026-orange)]()

> **A multidimensional framework for measuring occupational exposure to algorithmic expropriation under the Agentic AI regime.**

---

## What is ITEA v3.0?

The ITEA Framework provides ten complementary indicators covering 1,016 SOC 6-digit occupations from O\*NET 30.2, designed to measure occupational exposure to algorithmic expropriation in the Agentic AI regime — distinct from but complementary to task-level automation indices in the Frey-Osborne (2017) tradition or ability-based exposure measures such as the AIOE benchmark of Felten, Raj and Seamans (2021).

External convergent validation against the AIOE benchmark over 738 common SOC 6-digit occupations: **r(OAEI v3.0+, AIOE) = 0.797**.

| Indicator | Full Name | Dimension | Type | Status |
|-----------|-----------|-----------|------|--------|
| **ITEA** | Triple Index of Exposure to Automation | Exposure | Formative (z-score aggregation) | **Revised in v3.0** |
| **IRA** | Adaptive Resilience Index | Resilience | Reflective (triple residualisation) | **Revised in v3.0** |
| **ICT** | Technical Complexity Index | Complexity | Formative | Stable since v2.0 |
| **IFS** | Social Friction Index | Social interaction | Reflective | Stable since v2.0 |
| **IPI** | Interpersonal Presence Index | Presentiality | Formative | Stable since v1.3 |
| **IEF** | Functional Specificity Index | Specificity | Reflective | Stable since v2.0 |
| **GEE** | Education-Experience Gradient | Qualification | Calibrated (OLS+ordinal) | Stable since v1.45 |
| **IMO** | Occupational Mutation Index | Mutation | Hurdle model | Stable since v1.2 |
| **OAEI** | Occupational Algorithmic Expropriation Index | Composite operational | Multiplicative (canonical) + additive (alternative) | **Revised in v3.0 — dual variant** |
| **AEI** | Algorithmic Expropriation Index | Internal benchmark | Auxiliary | Stable since v2.0 |

---

## Why version 3.0? Evidence of a living research project

This repository advances from **v1.45 (October 2025)** to **v3.0 (April 2026)**, archiving the previous release as the [`v1.45-legacy`](https://github.com/Aval22/ITEA/releases/tag/v1.45-legacy) tag. The transition is not cosmetic. It reflects a major methodological revision motivated by a documented case study — three research papers (the trilogy 8A/8B/8C) that put the framework into active empirical use and, in doing so, exposed three specific limitations of v2.1 (the methodological line that paralleled v1.45). Documenting this evolution explicitly is part of the framework's preparation for submission to the [Journal of Open Source Software](https://joss.theoj.org/) (target window: mid-2026), which values evidence of community use and principled software evolution.

### The trilogy as case study

Three research papers in active circulation as of April 2026 motivated each of the three central revisions in v3.0:

- **Paper 8A — *"The Structural Flaw: Industrial Labour Contract Inadequacy under Agentic AI"*** (García-Lluis Valencia, 2026a). Targeted journals: Journal of Institutional Economics, Industrial and Corporate Change. → motivated the **z-score ITEA aggregation**.
- **Paper 8B — *"Beyond the Pigouvian Trap: Tokenised Intellectual Capital..."*** (García-Lluis Valencia, 2026b). Theoretical paper formalising the Lindbeck–Snower protective condition dissolution. → motivated the **dual-variant OAEI** (multiplicative for theoretical alignment + additive for criterion validity).
- **Paper 8C — *"QE and Senior Workforce Restructuring: A Labour Liability Transmission Channel"*** (García-Lluis Valencia, 2026c). Targeted journal: *Labour Economics*. Empirical paper on a novel monetary-policy transmission channel. → motivated the **triple-residualised IRA**.

| v3.0 change | Empirical motivation from trilogy | Validation gain |
|-------------|-----------------------------------|-----------------|
| ITEA: z-score normalisation before equal-weight averaging | Paper 8A's top-20 narrative diverged from v2.1's algorithmic ranking; component variance asymmetry was diluting the EIA Agentic-regime signal | r(ITEA, AEI): 0.71 → 0.89; r(ITEA, AIOE): 0.36 → 0.43 |
| IRA: triple residualisation against (GEE, ITEA, ICT) | Paper 8C's GEE × IRA quadrant analysis showed inflated Q1-Q4 separation due to residual IRA-ITEA correlation under v2.1's univariate residualisation | r(IRA, ITEA): 0.28 → 0.14; r(IRA, ICT): 0.10 → 0.06; 84% variance preserved |
| OAEI: dual-variant architecture (multiplicative canonical + additive alternative) | Paper 8B's tokenisation-rate calibration required higher r(OAEI, Wage) than the multiplicative form delivers, but trilogy backward compatibility required preserving multiplicativity | Additive variant: r(OAEI, Wage) 0.58 → 0.66; AIOE convergence preserved at 0.80 |

The full case-study reasoning, including how each paper's specific empirical finding pushed the methodological decision, is documented in §4.4, §5.4 and §6.5 of the [Consolidated Methodology document](docs/ITEA_v3_0_Consolidated_Methodology.pdf).

---

## Why this matters (and what changed since v1.45)

The v1.x line (March 2024 – October 2025) was the operational release cycle: data workbooks, R/Python implementation code, Streamlit dashboard. The v2.x line (April 2026) was the methodological documentation cycle: academic papers anchoring the framework's psychometric foundations. Until this release, the two lines progressed asynchronously — a researcher citing "ITEA v1.45" referred to the same conceptual framework as one citing "ITEA v2.1", but the precise indicator formulas, source data versions, and validation tables were not trivially comparable.

**v3.0 unifies both numbering lines onto a single version.** The operational repository advances to v3.0 with the v1.45 release archived as a permanent legacy tag for replication of any results published using the v1.x specification. The methodological documentation advances to a single Consolidated Edition that supersedes both v2.0 and v2.1.

| Aspect | v1.45 (legacy) | v3.0 (this release) |
|--------|----------------|----------------------|
| Indicators | 8 (ITEA, IRO, ICT, IFS, IPI, IEF, GEE, IMO) | 10 (adds IRA derived from CA + IRO_residual; introduces OAEI as composite) |
| Source data | O\*NET 29.1 | O\*NET 30.2 |
| ITEA aggregation | Equal-weight arithmetic mean in [0,1] | **z-score normalisation → equal-weight average → min-max projection** |
| Resilience indicator | IRO (with 4→2 item revision in v1.45) | **IRA = 0.6·CA + 0.4·IRO_residual_v3.0**, where IRO_residual is residualised against (GEE, ITEA, ICT) |
| Composite metric | None — indicators reported separately | **OAEI multiplicative (canonical) and OAEI v3.0+ additive (alternative)** |
| External convergent validation against AIOE | Not reported | r(OAEI v3.0+, AIOE) = 0.797 |
| Effective N for full validation | — | 738 occupations |
| Trilogy backward compatibility | n/a | OAEI multiplicative preserves trilogy citation |

**Migration from v1.45 is documented step-by-step in [`docs/MIGRATION.md`](docs/MIGRATION.md).** Researchers who wish to reproduce results using the v1.x specification can check out the `v1.45-legacy` tag and follow the version-specific README preserved in that snapshot.

---

## Quick Start

### R

```r
source("code/v3/itea_functions_v3.R")

# Load processed data
library(readxl)
df <- read_excel("data/processed/ITEA_v3_0_Workbook.xlsx",
                 sheet = "ITEA_INDICATORS_v3.0", skip = 2)

# Compute ITEA v3.0 (z-score aggregation)
df$ITEA_v30_check <- itea_v3(df$EAC, df$EIG, df$EIA)

# Compute IRA v3.0 (triple residualisation)
df$IRA_v30_check <- ira_v3(df$CA, df$`IRO v1.45 (legacy)`,
                            df$`GEE v2.1`, df$ITEA_v30_check, df$ICT)

# Compute OAEI v3.0 multiplicative (canonical)
df$OAEI_v30_check <- oaei_v3_mult(df$ITEA_v30_check, df$`GEE v2.1`,
                                    df$ICT, df$IPI)

# Compute OAEI v3.0+ additive (alternative)
df$OAEI_v30_plus_check <- oaei_v3_add(df$ITEA_v30_check, df$`GEE v2.1`,
                                       df$ICT, df$IPI)
```

### Python

```python
from code.v3.itea_functions_v3 import itea_v3, ira_v3, oaei_v3_mult, oaei_v3_add
import pandas as pd

df = pd.read_excel("data/processed/ITEA_v3_0_Workbook.xlsx",
                   sheet_name="ITEA_INDICATORS_v3.0", skiprows=2)

df['ITEA_v30_check'] = itea_v3(df['EAC'], df['EIG'], df['EIA'])
df['IRA_v30_check'] = ira_v3(df['CA'], df['IRO v1.45 (legacy)'],
                              df['GEE v2.1'], df['ITEA_v30_check'], df['ICT'])
df['OAEI_v30_check'] = oaei_v3_mult(df['ITEA_v30_check'], df['GEE v2.1'],
                                     df['ICT'], df['IPI'])
df['OAEI_v30_plus_check'] = oaei_v3_add(df['ITEA_v30_check'], df['GEE v2.1'],
                                         df['ICT'], df['IPI'])
```

Both implementations are designed to reproduce the values stored in `OAEI v3.0` and `OAEI v3.0+ additive` columns of the data workbook (Δ < 1e-6 over the 1,016 occupations).

---

## Repository structure

```
ITEA-Framework/
├── README.md                          # This file
├── README_ES.md · README_PT.md · README_ZH.md   # Multilingual versions
├── LICENSE                            # MIT
├── CITATION.cff                       # GitHub-native citation metadata
├── CHANGELOG.md                       # Full v1.0 → v3.0 change history
├── MANIFEST.json                      # SHA-256 checksums for Zenodo deposit
├── .gitignore
│
├── data/
│   ├── processed/
│   │   └── ITEA_v3_0_Workbook.xlsx          # Primary v3.0 dataset (12 sheets)
│   └── legacy/
│       └── Research_Data_Workbook_ITEA_v1.45.xlsx   # Preserved for v1.x replication
│
├── code/
│   ├── v3/
│   │   ├── itea_functions_v3.R              # R reference implementation
│   │   ├── itea_functions_v3.py             # Python reference implementation
│   │   └── tests/                           # Unit tests reproducing the workbook values
│   └── legacy/
│       ├── itea_functions_v1.45.R           # Preserved v1.x implementation
│       └── itea_functions_v1_45.py
│
├── docs/
│   ├── ITEA_v3_0_Consolidated_Methodology.pdf   # Single authoritative methodology document
│   ├── MIGRATION.md                              # v1.45 → v3.0 step-by-step migration
│   └── papers/
│       ├── README.md                             # Pointers to trilogy papers (Zenodo DOIs)
│       └── trilogy_case_study.md                 # Standalone case study
│
└── paper/                                        # JOSS submission
    ├── paper.md                                  # 1,000-word JOSS paper
    ├── paper.bib                                 # Bibliography
    └── figures/                                  # JOSS figures
```

---

## Version history

| Version | Date | Key Changes | Impact |
|---------|------|-------------|--------|
| v1.0 | 2024-03 | Initial release: 8 indicators, O\*NET 28.x | Baseline |
| v1.1 | 2024-09 | IRO institutional security; ITEA additive form | Medium |
| v1.2 | 2025-03 | GEE OLS calibration (ρ 0.259 → 0.927); IMO Hurdle+cap | High |
| v1.3 | 2025-04 | IPI new indicator; IFS CI extraction | Medium |
| v1.45 | 2025-10 | IRO 4→2 items; GEE dual OLS+ordinal | Medium — last v1.x release; archived as `v1.45-legacy` tag |
| v2.0 | 2026-04 | Methodology paper: formative/reflective typology, conceptual foundations | High — first methodological document |
| v2.1 | 2026-04 | Memorandum: data refresh to O\*NET 30.2 | Medium |
| **v3.0** | **2026-04** | **z-score ITEA · triple-residualised IRA · dual-variant OAEI · trilogy case study · JOSS preparation** | **Critical — single authoritative version** |

The full change-log is in [CHANGELOG.md](CHANGELOG.md).

---

## Related research papers

The trilogy that motivated v3.0 (citable by name in any work using ITEA):

1. García-Lluis Valencia, A. (2026a). **The Structural Flaw: Industrial Labour Contract Inadequacy under Agentic AI**. Universidad Rey Juan Carlos. Zenodo: [10.5281/zenodo.19592542](https://doi.org/10.5281/zenodo.19592542).
2. García-Lluis Valencia, A. (2026b). **Beyond the Pigouvian Trap: Tokenised Intellectual Capital as a Pareto-Dominant Mechanism for the Agentic AI Layoff Externality**. Universidad Rey Juan Carlos.
3. García-Lluis Valencia, A. (2026c). **QE and Senior Workforce Restructuring: A Labour Liability Transmission Channel**. Universidad Rey Juan Carlos. Zenodo: [10.5281/zenodo.19592184](https://doi.org/10.5281/zenodo.19592184).

---

## Data sources

- **O\*NET 30.2** (February 2026): 1,016 occupations, 47,810 task statements. U.S. Department of Labor. Public domain.
- **BLS OEWS** (May 2024): Occupational wage data by percentile, used for the criterion validity test r(OAEI, Wage).
- **AIOE** (Felten, Raj & Seamans, 2021): External convergent benchmark over 769 common SOC 6-digit occupations.
- **Eurostat ESJS2** (referenced for future European replication, §11 of methodology).
- **U.S. Census Bureau IDB**: Demographic context only (not used in indicator construction).

---

## Citation

```bibtex
@software{garcia-lluis2026itea,
  title     = {ITEA Framework: A Multidimensional System for Measuring Occupational
               Exposure to Algorithmic Expropriation under the Agentic AI Regime},
  author    = {García-Lluis Valencia, Alberto},
  year      = {2026},
  version   = {3.0},
  doi       = {10.5281/zenodo.20083102},
  url       = {https://github.com/Aval22/ITEA},
  note      = {Consolidated Methodological Edition. Supersedes v2.0 and v2.1.}
}
```

GitHub-native citation metadata is available in [CITATION.cff](CITATION.cff).

---

## License

Released under the [MIT License](LICENSE).

- **Academic use**: Free with citation.
- **Commercial use**: Contact the author.
- **Data**: O\*NET data follows U.S. DOL public domain terms; BLS OES public domain; AIOE used under Felten et al. 2021 terms.

---

## Contact

**Alberto García-Lluis Valencia**
Universidad Rey Juan Carlos, Madrid
Doctoral Programme in Economics and Business
ORCID: [0009-0003-1438-1633](https://orcid.org/0009-0003-1438-1633)
Email: alb.valencia@gmail.com
Institutional: a.garciaval.2025@alumnos.urjc.es

---

*ITEA Framework v3.0 — Making algorithmic expropriation measurable, multidimensional, and actionable.*
