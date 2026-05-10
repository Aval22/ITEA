# Migration Guide — v1.45 → v3.0

This document provides a step-by-step migration path from the legacy v1.45 release
(October 2025) to the unified v3.0 (April 2026). It is intended for researchers
who have existing pipelines built on v1.45 and need to transition to the new
specification.

---

## TL;DR

If you only need v1.45 backward compatibility, **check out the `v1.45-legacy` tag**:

```bash
git checkout v1.45-legacy
```

This snapshot preserves the v1.45 indicator specifications, data workbook,
implementation code, and README exactly as released.

If you are **starting new research**, use v3.0 directly. The Consolidated
Methodology (`docs/ITEA_v3_0_Consolidated_Methodology.pdf`) is the authoritative
reference.

---

## What changed

| Aspect | v1.45 | v3.0 |
|--------|-------|------|
| Number of indicators | 8 | 10 (introduces IRA composite + OAEI) |
| Source O\*NET version | 29.1 | 30.2 |
| ITEA aggregation | Equal-weight arithmetic mean of EAC, EIG, EIA in [0,1] | **z-score** normalisation → equal-weight average → min-max projection |
| Resilience | IRO (4-item then 2-item version) | **IRA** = 0.6·CA + 0.4·IRO_residual_v3.0 |
| IRO residualisation | None / partial against GEE | Full triple residualisation against (GEE, ITEA, ICT) |
| Composite measure | None — indicators reported separately | **OAEI** with two variants: multiplicative (canonical) and additive (alternative) |
| External AIOE convergence | Not reported | r(OAEI v3.0+, AIOE) = 0.797 |

---

## Migration steps

### Step 1 — Update data file references

Old (v1.45):
```r
df <- readxl::read_excel("Research_Data_Workbook_ITEA_v1.35.xlsx",
                         sheet = "ITEA_8_INDICADORES_v1.3")
```

New (v3.0):
```r
df <- readxl::read_excel("data/processed/ITEA_v3_0_Workbook.xlsx",
                         sheet = "ITEA_INDICATORS_v3.0", skip = 2)
```

The new workbook has 27 columns including all v2.1 and v3.0 indicators side-by-side
to support migration.

### Step 2 — Update ITEA computation

Old (v1.45):
```r
df$ITEA_v145 <- (df$EAC + df$EIG + df$EIA) / 3
```

New (v3.0):
```r
source("code/v3/itea_functions_v3.R")
df$ITEA_v3 <- itea_v3(df$EAC, df$EIG, df$EIA)
```

The new function applies z-score normalisation before averaging. The values are
**not directly comparable** to v1.45 ITEA; expect r(ITEA_v145, ITEA_v3) ≈ 0.83.

### Step 3 — Update resilience computation

Old (v1.45): used IRO directly.

New (v3.0): use IRA, which combines CA (60%) and IRO_residual (40%) where
IRO_residual is residualised against the full set of structural moderators.

```r
df$IRA_v3 <- ira_v3(df$CA, df$`IRO v1.45 (legacy)`,
                    df$`GEE v2.1`, df$ITEA_v3, df$ICT)
```

Cross-version stability r(IRO_v145, IRA_v3) ≈ 0.999 because most of the variance
in IRA derives from CA.

### Step 4 — Compute OAEI (new in v3.0)

v1.45 did not provide a composite. In v3.0 you have two choices:

**For backward compatibility with the trilogy or theoretical alignment with SECI:**
```r
df$OAEI_v3_mult <- oaei_v3_mult(df$ITEA_v3, df$`GEE v2.1`, df$ICT, df$IPI)
```

**For criterion validity (wage modelling, employment outcomes):**
```r
df$OAEI_v3_plus <- oaei_v3_add(df$ITEA_v3, df$`GEE v2.1`, df$ICT, df$IPI)
```

See §6.4 of the Consolidated Methodology and `oaei_recommend()` for the
selection guidance.

### Step 5 — Update validation reporting

If your downstream pipeline reports validation correlations, recompute on v3.0.
The new criteria (v) and (vi) discriminant validity should be reported in any
methodological appendix using v3.0 data.

### Step 6 — Update top-N references

If your code references the top 20 OAEI occupations:
- v2.1 ranking (used in research drafts citing v1.45 / v2.1) is preserved in
  the workbook column `OAEI v2.1`.
- v3.0 ranking is in `OAEI v3.0` and the dedicated `TOP20_OAEI_v3.0` sheet.
- 11 of 20 occupations are common; 9 are new entries. The new ranking is led
  by Pathologists, Market Research Analysts, Business Intelligence Analysts.

### Step 7 — Update policy population numbers

The policy population for the top-20 quantification was reported as 2.97 million
US workers in v2.1 trilogy drafts. The v3.0 figure based on BLS OEWS 2024
disaggregation is **1.22 million workers (0.74% of the US workforce)**. See §8.4
of the Consolidated Methodology.

---

## Reconciliation check

Run the reconciliation utility to confirm your installation reproduces the
workbook values:

```python
from code.v3.itea_functions_v3 import itea_reconcile
print(itea_reconcile("data/processed/ITEA_v3_0_Workbook.xlsx"))
```

All four indicators should show `max_abs_diff < 1e-6`.

---

## When NOT to migrate

Stay on v1.45 if you are:

- Reproducing results from a paper that explicitly cites the v1.45 specification.
- Running a validation comparison between v1.x and v3.x (in which case use both).
- Working with downstream code that depends on the 8-indicator architecture
  exactly as released in v1.45 and you do not have time for the migration in
  this cycle.

For all new research and publications targeting any submission window beyond
April 2026, use v3.0.

---

## Questions?

Open an issue at https://github.com/Aval22/ITEA/issues or contact
Alberto García-Lluis Valencia at alb.valencia@gmail.com.
