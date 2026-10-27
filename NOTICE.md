# Notices: data licences and attribution

The **code** in this repository is released under the MIT License (`LICENSE`).
The **data** it ships or downloads carry their own terms:

| Data | Where | Licence | Notes |
|---|---|---|---|
| ITEA indicators (v3.0 workbook, v4.0 outputs) | `data/processed/`, `v4.0/outputs/` | MIT | Derived from O\*NET; O\*NET attribution below applies |
| AXI task grades | `src/itea/data/` | CC BY 4.0 | O\*NET task statements with added grades |
| JRC145832 Table M.1 (AI exposure 2024, ISCO-3) | `src/itea/data/` | CC BY 4.0, © European Union 2026 | Casas et al. (2026), transcribed from Appendix M |
| O\*NET 30.2 database | downloaded by `itea fetch` | CC BY 4.0 | Not redistributed here |
| BLS SOC↔ISCO-08 and SOC 2010↔2018 crosswalks | downloaded by `itea fetch` | U.S. public domain | Not redistributed; derived crosswalk in `v4.0/outputs/` |
| BLS OEWS wages | `data/processed/` (v3.0 workbook) | U.S. public domain | |
| AIOE (Felten, Raj & Seamans, 2021) | `data/processed/` (v3.0 workbook) | Authors' academic terms | Used for convergent validation only |
| ESCO v1.2.1 | research scripts in `v4.0/code/` | CC BY 4.0 | © European Union; not redistributed |
| Atlas of the alienable frontier (explorer and data) | `docs/atlas/` | CC BY-NC 4.0, © 2026 A. García-Lluis Valencia, Epistémica | Exception to MIT; see `docs/atlas/README.md` |

**Recommended citation** of work using ITEA data: the Zenodo deposit
(v4.1.0: version DOI 10.5281/zenodo.23604653, concept DOI of the v4.x line 10.5281/zenodo.23604652;
releases v1.45-v3.0: concept DOI 10.5281/zenodo.19578915) and the specific release used; see `CITATION.cff`.

## O\*NET attribution

This product includes information from the O\*NET Database
(https://www.onetcenter.org/database.html) by the U.S. Department of Labor,
Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0
license. O\*NET® is a trademark of USDOL/ETA. Alberto García-Lluis Valencia has
modified all or some of this information. USDOL/ETA has not approved, endorsed,
or tested these modifications.

## ESCO attribution

© European Union, 2025. European Skills, Competences, Qualifications and
Occupations (ESCO), European Commission (DG EMPL), CC BY 4.0,
https://esco.ec.europa.eu. Modified for ITEA.
