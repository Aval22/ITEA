# ITEA Framework — Index of Transformation and Algorithmic Expropriability

🌐 **English** · [Español](README_ES.md) · [Português](README_PT.md) · [中文](README_ZH.md)

[![DOI](https://zenodo.org/badge/1210690701.svg)](https://doi.org/10.5281/zenodo.19578915)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![O*NET](https://img.shields.io/badge/O*NET-30.2-green)]()
[![Version](https://img.shields.io/badge/Version-4.0.0-blue)]()
[![tests](https://github.com/Aval22/ITEA/actions/workflows/tests.yml/badge.svg)](https://github.com/Aval22/ITEA/actions/workflows/tests.yml)

> **A multidimensional framework for measuring occupational algorithmic expropriability under the Agentic AI regime.**

---

## What is ITEA?

ITEA measures **algorithmic expropriability** — the surface of human knowledge that AI can codify and capture from work. Its distinctive move is to separate what can be *measured* (a potential: **expropriability** = exposure × codifiability) from the *normative event* it enables — the transfer of the worker's **sovereignty** over the exploitation of that knowledge — and from its two consequences: the firm's **appropriation** of value and the **dilution** of market exclusivity. This layered view — a worker still *possesses* what she knows (non-rival), but may lose the *right to decide* how it is exploited — is what distinguishes ITEA from a single exposure score.

> **Understand the reasoning:** [The research narrative and the *why* of each decision](docs/ITEA_Relato_y_Decisiones.html) · [Data guide and glossary](docs/ITEA_Guia_Datos_y_Glosario.html)

ITEA has two layers, both in this repository:

- **v4.0 — OAXI-EU on the ISCO-08 / ESCO axis.** 47,810 O\*NET tasks graded for generative-AI exposure and codifiability (the legacy AXI grades, to be replaced in v4.1) are rolled up to O\*NET work activities, mapped back to all 923 O\*NET-SOC occupations, and carried to **428 ISCO-08 unit groups** through the official BLS crosswalks. Convergence with the JRC145832 exposure benchmark at ISCO-3: **Pearson 0.736, Spearman 0.819** (127 groups). Built end to end from public inputs with `itea build-eu`.
- **v3.0 — ten indicators on O\*NET 30.2** (1,016 SOC occupations), distinct from but complementary to task-level automation indices in the Frey-Osborne (2017) tradition or ability-based exposure measures such as the AIOE benchmark of Felten, Raj and Seamans (2021). Convergence with AIOE over 769 common occupations: **r(OAEI v3.0+, AIOE) = 0.798**.

Both measure a **potential** — which occupations' knowledge is most open to codification — not realised automation or realised transfers of value.

### In development: v4.1 task grading (`itea.grading`)

v4.1 replaces the legacy AXI grades with a documented, fully automated grading of the 18,796 O\*NET 30.2 tasks, built only from official taxonomies (O\*NET linkage tables, ESCO) and validated against independent public references that are never used for construction. Hypotheses are registered before each run.

- **Layer 1 (structural, done):** codifiability K and generative-AI exposure E from the O\*NET Abilities/Skills-to-Work-Activities tables. E converges with the Eloundou et al. (2024) human labels (ρ = 0.40); K converges with non-routine analytical work (ρ = 0.67, and 0.28 within Job Zone) and predicts the human labels net of skill level (partial ρ = 0.40). Two hypotheses failed and are reported.
- **Layer 2 (semantic, done):** each task linked to its five nearest ESCO v1.2.1 concepts with sentence embeddings (all-mpnet-base-v2, run locally). K now discriminates within activities (68 % of its variance, vs 5 % for layer 1) and is less tied to skill level.
- **Layer 3 (NLI anchors):** failed its registered tests; published as a negative result and not used.
- **OAXI-EU v4.1 (built):** K = layers 1+2, E = layers 1+2, with a 1,000-draw Monte Carlo giving a 5–95 % band for every ISCO group. Final E vs human labels ρ = 0.45; Spearman 0.80 with the v4.0 index. Table: [`v4.0/outputs/grading/oaxi_eu_v41.csv`](v4.0/outputs/grading/oaxi_eu_v41.csv).
- **Technology, utilisation and competence layers (T, U, S):** occupation × product inventory from O\*NET Technology Skills; enterprise adoption of ERP, CRM and AI by country and NACE sector from Eurostat.

Documentation: [methodology](docs/grading/METHODOLOGY_v0.2_EN.md) · [hypotheses and results](docs/grading/VALIDATION_RESULTS_EN.md) · [Spanish originals and decision log](docs/grading/README.md).

## Installation and testing

```bash
pip install git+https://github.com/Aval22/ITEA.git        # AXI grades and JRC benchmark are packaged
itea fetch --dest data/external                            # O*NET 30.2 + BLS crosswalks, SHA-256 verified
itea build-eu --external data/external --out outputs       # writes outputs/oaxi_eu.csv
itea validate --index outputs/oaxi_eu.csv                  # convergence with JRC145832 at ISCO-3
```

From a clone, `pip install -e ".[test]"` and `pytest` run the unit tests, the end-to-end rebuild of [`v4.0/outputs/oaxi_eu.csv`](v4.0/outputs/oaxi_eu.csv) and the benchmark reproduction. Python 3.10+; dependencies: numpy, pandas, scipy, openpyxl, xlrd. R ≥ 4.0 is optional (the CI checks the Python port against the R reference implementation).

Using the library directly, including with your own task-level scores:

```python
import itea
from itea.axi import load_onet
from itea.crosswalk import build_crosswalk

tasks, links = load_onet("data/external/db_30_2_text")
cw = build_crosswalk("data/external/ISCO_SOC_Crosswalk.xls",
                     "data/external/soc_2010_to_2018_crosswalk.xlsx")

# OAXI-EU from the packaged AXI grades
occ = itea.axi_to_occupations(itea.load_axi(itea.axi_path()), "data/external/db_30_2_text")
idx = itea.oaxi_eu(occ, cw)                          # isco, E, K, n_soc, core, OAXI_EU (1–100)
itea.convergence(idx, itea.jrc_benchmark())          # {'n_isco3': 127, 'pearson': 0.736, ...}
itea.kappa_grid(occ, cw, itea.jrc_benchmark())       # calibration table for κ

# any numeric score keyed by O*NET Task ID, e.g. an LLM-exposure rating
my_scores = tasks[["TaskID"]].assign(score=0.5)      # replace with your own column
act = itea.to_activities(my_scores, links, ["score"])
on_isco = itea.to_isco(itea.to_occupations(act, links, ["score"]), cw, ["score"])
```

The AXI task grades ship inside the package and are documented in [`src/itea/data/README_AXI.md`](src/itea/data/README_AXI.md), including how they were produced and their reliability.

> **Coverage note.** OAEI is available for **878 of the 1,016** occupations (86.5%). The 138 without OAEI lack the GEE/wage inputs it composes; among them, the **19 military occupations (SOC 55)** are a structural O\*NET exclusion (no Job Zone/wage). Details in the [dataset review](docs/ITEA_Revision_Dataset.md).

| Indicator | Full Name | Dimension | Type | Status |
|-----------|-----------|-----------|------|--------|
| **ITEA** | Index of Transformation and Algorithmic Expropriability | Exposure | Formative (z-score aggregation) | **Revised in v3.0** |
| **IRA** | Adaptive Resilience Index | Resilience | Reflective (triple residualisation) | **Revised in v3.0** |
| **ICT** | Technical Complexity Index | Complexity | Formative | Stable since v2.0 |
| **IFS** | Social Friction Index | Social interaction | Reflective | Stable since v2.0 |
| **IPI** | Interpersonal Presence Index | Presentiality | Formative | Stable since v1.3 |
| **IEF** | Functional Specificity Index | Specificity | Reflective | Stable since v2.0 |
| **GEE** | Education-Experience Gradient | Qualification | Calibrated (OLS+ordinal) | Stable since v1.45 |
| **IMO** | Occupational Mutation Index | Mutation | Hurdle model | Stable since v1.2 |
| **OAEI** | Occupational Algorithmic Expropriability Index | Composite operational | Multiplicative (canonical) + additive (alternative) | **Revised in v3.0 — dual variant** |
| **AEI** | Algorithmic Expropriability Index | Internal benchmark | Auxiliary | Stable since v2.0 |

---

## Why version 3.0? Evidence of a living research project

This repository advances from **v1.45 (October 2025)** to **v3.0 (April 2026)**, archiving the previous release as the [`v1.45`](https://github.com/Aval22/ITEA/releases/tag/v1.45) tag. The transition is not cosmetic. It reflects a major methodological revision motivated by a documented case study — three research papers (the trilogy 8A/8B/8C) that put the framework into active empirical use and, in doing so, exposed three specific limitations of v2.1 (the methodological line that paralleled v1.45). Documenting this evolution explicitly is part of the framework's preparation for submission to the [Journal of Open Source Software](https://joss.theoj.org/), which values evidence of community use and principled software evolution.

### The trilogy as case study

Three research papers in active circulation as of April 2026 motivated each of the three central revisions in v3.0:

- **Paper 8A — *"Mapping algorithmic expropriation: occupational exposure to Agentic AI under the multidimensional ITEA framework"*** (García-Lluis Valencia, 2026a). → motivated the **z-score ITEA aggregation**.
- **Paper 8B — *"Beyond the Pigouvian Trap: Tokenised Intellectual Capital..."*** (García-Lluis Valencia, 2026b). Theoretical paper formalising the Lindbeck–Snower protective condition dissolution. → motivated the **dual-variant OAEI** (multiplicative for theoretical alignment + additive for criterion validity).
- **Paper 8C — *"The MBB Triad as Limit Case of Algorithmic Expropriation"*** (García-Lluis Valencia, 2026c). Limit-case analysis of consulting up-or-out contracts under proprietary Agentic AI. → motivated the **triple-residualised IRA**.

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
| External convergent validation against AIOE | Not reported | r(OAEI v3.0+, AIOE) = 0.798 |
| Effective N for full validation | — | 769 occupations |
| Trilogy backward compatibility | n/a | OAEI multiplicative preserves trilogy citation |

**Migration from v1.45 is documented step-by-step in [`docs/MIGRATION.md`](docs/MIGRATION.md).** Researchers who wish to reproduce results using the v1.x specification can check out the `v1.45` tag and follow the version-specific README preserved in that snapshot.

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
from itea.v3 import itea_v3, ira_v3, oaei_v3_mult, oaei_v3_add
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
ITEA/
├── README.md · README_ES.md · README_PT.md · README_ZH.md
├── LICENSE (MIT) · NOTICE.md (data licences) · CITATION.cff · CHANGELOG.md · CONTRIBUTING.md
├── pyproject.toml                     # package `itea-framework`, CLI `itea`
├── src/itea/                          # installable package
│   ├── v3.py                          # v3.0 indicators (ITEA, IRA, OAEI)
│   ├── axi.py                         # task → activity → occupation roll-up
│   ├── crosswalk.py                   # official BLS SOC 2018 → ISCO-08 chain
│   ├── oaxi_eu.py                     # OAXI-EU, benchmark convergence, κ grid
│   ├── fetch.py · cli.py              # input download (SHA-256) and command line
│   ├── data/                          # AXI grades (CC BY 4.0) and JRC145832 benchmark
│   └── grading/                       # v4.1 task grading (structural, validation, technology, eurostat)
├── tests/                             # pytest suite (incl. R ↔ Python parity)
├── scripts/grading/                   # validation and layer-building scripts
├── data/processed/                    # ITEA_v3_0_Workbook.xlsx (v3.0) · ITEA_v4_0_Workbook.xlsx (v4.0)
├── code/v3/                           # R implementation, Python shim, v3.0 tests
├── v4.0/
│   ├── outputs/                       # oaxi_eu.csv, occupation_shares.csv, crosswalk, meta; grading/
│   ├── code/                          # research scripts for the ESCO profiles (need local ESCO dump)
│   └── docs/                          # v4.0 design and decisions
├── docs/                              # methodology (v3.0, v4.0), grading/, migration guide
└── paper/                             # JOSS paper (paper.md, paper.bib)
```

---

## Version history

| Version | Date | Key Changes | Impact |
|---------|------|-------------|--------|
| v1.0 | 2024-03 | Initial release: 8 indicators, O\*NET 28.x | Baseline |
| v1.1 | 2024-09 | IRO institutional security; ITEA additive form | Medium |
| v1.2 | 2025-03 | GEE OLS calibration (ρ 0.259 → 0.927); IMO Hurdle+cap | High |
| v1.3 | 2025-04 | IPI new indicator; IFS CI extraction | Medium |
| v1.45 | 2025-10 | IRO 4→2 items; GEE dual OLS+ordinal | Medium — last v1.x release; archived as the `v1.45` tag |
| v2.0 | 2026-04 | Methodology paper: formative/reflective typology, conceptual foundations | High — first methodological document |
| v2.1 | 2026-04 | Memorandum: data refresh to O\*NET 30.2 | Medium |
| v3.0 | 2026-04 | z-score ITEA · triple-residualised IRA · dual-variant OAEI · trilogy case study | Critical |
| **v4.0.0** | **2026-10** | **OAXI-EU on ISCO-08 · official BLS crosswalk · AXI grades released · Python package, CLI, tests, CI** | **High — European layer, reproducible from public inputs** |

The full change-log is in [CHANGELOG.md](CHANGELOG.md).

---

## Related research papers

The trilogy that motivated v3.0 (working papers, Zenodo):

1. García-Lluis Valencia, A. (2026a). **Mapping algorithmic expropriation: occupational exposure to Agentic AI under the multidimensional ITEA framework** [Paper 8A]. [10.5281/zenodo.20081628](https://doi.org/10.5281/zenodo.20081628).
2. García-Lluis Valencia, A. (2026b). **Beyond the Pigouvian Trap** [Paper 8B]. Concept DOI [10.5281/zenodo.20081794](https://doi.org/10.5281/zenodo.20081794).
3. García-Lluis Valencia, A. (2026c). **The MBB Triad as Limit Case of Algorithmic Expropriation** [Paper 8C]. [10.5281/zenodo.20082588](https://doi.org/10.5281/zenodo.20082588).

Related: *The Structural Flaw* ([10.5281/zenodo.19693452](https://doi.org/10.5281/zenodo.19693452)); *QE and Senior Workforce Restructuring* ([10.5281/zenodo.19592184](https://doi.org/10.5281/zenodo.19592184)).

---

## Data sources

- **O\*NET 30.2** (February 2026): 1,016 occupations; task statements and Tasks-to-DWAs links. U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license; O\*NET® is a trademark of USDOL/ETA. See full attribution below.
- **AXI task grades** (this repository, CC BY 4.0): 47,810 O\*NET 29.1 task statements graded for automation, codifiability, generative-AI and agentic-AI impact. See [`src/itea/data/README_AXI.md`](src/itea/data/README_AXI.md).
- **BLS crosswalks** (public domain): ISCO-08 ↔ SOC 2010 and SOC 2010 ↔ SOC 2018, downloaded by `itea fetch`.
- **ESCO v1.2.1** (CC BY 4.0, © European Union): ISCO-08 skill profiles in the v4.0 research scripts.
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
  version   = {4.0.0},
  doi       = {10.5281/zenodo.19578915},
  url       = {https://github.com/Aval22/ITEA},
  note      = {Concept DOI; cite the version DOI of the release you used}
}
```

GitHub-native citation metadata is available in [CITATION.cff](CITATION.cff).

---

## License

Code released under the [MIT License](LICENSE). Data licences and attributions are listed in [NOTICE.md](NOTICE.md): O\*NET data under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (attribution below, **not** public domain); AXI grades CC BY 4.0; BLS data public domain; AIOE used under Felten et al. 2021 terms. Please cite ITEA when you use it (see [Citation](#citation)).

Questions, bug reports and contributions: see [CONTRIBUTING.md](CONTRIBUTING.md).

### O\*NET attribution

This product includes information from the [O\*NET 30.2 Database](https://www.onetcenter.org/database.html) by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license. O\*NET® is a trademark of USDOL/ETA. Alberto García-Lluis Valencia has modified all or some of this information (the ITEA indicators are derived, not original O\*NET fields). USDOL/ETA has not approved, endorsed, or tested these modifications.

---

## Contact

**Alberto García-Lluis Valencia**
Universidad Rey Juan Carlos, Madrid
Doctoral Programme in Economics and Business
ORCID: [0009-0003-1438-1633](https://orcid.org/0009-0003-1438-1633)
Email: aval@epistemica.eu

---

*ITEA Framework v4.0 — Making algorithmic expropriability measurable, multidimensional, and actionable.*
