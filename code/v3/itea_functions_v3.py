"""
ITEA Framework v3.0 — Python reference implementation
======================================================

Author:   Alberto García-Lluis Valencia
License:  MIT
Version:  3.0 (April 2026)
Repo:     https://github.com/AVAL22/ITEA-Framework
DOI:      10.5281/zenodo.19578916

This implementation reproduces the values stored in
data/processed/ITEA_v3_0_Workbook.xlsx within numerical
precision (Δ < 1e-6 over the 1,016 occupations).

THREE KEY FUNCTIONS:
    itea_v3()        — z-score equal-weight aggregation
    ira_v3()         — triple residualisation
    oaei_v3_mult()   — multiplicative canonical OAEI
    oaei_v3_add()    — additive alternative OAEI v3.0+

The reasoning behind each v3.0 design decision is documented
in the ITEA v3.0 Consolidated Methodology (docs/), with case
studies referencing Papers 8A, 8B and 8C of the trilogy.
"""

from __future__ import annotations
import numpy as np
import pandas as pd

__version__ = "3.0"


def itea_v3(eac, eig, eia):
    """
    ITEA v3.0 — Triple Index of Exposure to Automation.

    Aggregates the three components (EAC, EIG, EIA) using z-score
    normalisation followed by equal-weight averaging and final
    min-max projection to [0, 1]. This corrects the variance
    asymmetry pathology of the v2.1 equal-weight-in-[0,1] approach
    that was diluting the EIA Agentic-regime signal.

    Reference: ITEA v3.0 Consolidated Methodology, §4.
    Motivation: Paper 8A "The Structural Flaw" (García-Lluis
    Valencia, 2026a). See §4.4 for the case-study reasoning.

    Parameters
    ----------
    eac, eig, eia : array-like
        Vectors of EAC, EIG and EIA component values.

    Returns
    -------
    np.ndarray
        ITEA v3.0 values in [0, 1].

    Examples
    --------
    >>> df = pd.read_excel("ITEA_v3_0_Workbook.xlsx",
    ...                    sheet_name="ITEA_INDICATORS_v3.0", skiprows=2)
    >>> df['ITEA_v3'] = itea_v3(df['EAC'], df['EIG'], df['EIA'])
    """
    eac = np.asarray(eac, dtype=float)
    eig = np.asarray(eig, dtype=float)
    eia = np.asarray(eia, dtype=float)

    def _z(x):
        out = np.full_like(x, np.nan, dtype=float)
        valid = ~np.isnan(x)
        if valid.sum() < 2:
            return out
        sd = x[valid].std(ddof=0)
        if sd == 0:
            # Degenerate case: constant component → contribute zero
            out[valid] = 0.0
            return out
        out[valid] = (x[valid] - x[valid].mean()) / sd
        return out

    raw = (_z(eac) + _z(eig) + _z(eia)) / 3.0
    rmin, rmax = np.nanmin(raw), np.nanmax(raw)
    return (raw - rmin) / (rmax - rmin)


def ira_v3(ca, iro_v145, gee, itea_v3_vals, ict):
    """
    IRA v3.0 — Adaptive Resilience Index with triple residualisation.

    Combines CA (raw, weight 0.60) with IRO_residual (weight 0.40),
    where IRO_residual is the residual of OLS(IRO_v1.45 ~ GEE +
    ITEA_v3.0 + ICT) min-max-normalised to [0, 1]. The triple
    residualisation against all structural moderators ensures
    clean discriminant validity while preserving 84% of the
    original IRO variance.

    Reference: ITEA v3.0 Consolidated Methodology, §5.
    Motivation: Paper 8C "QE and Senior Workforce Restructuring"
    (García-Lluis Valencia, 2026c). See §5.4 for the case-study
    reasoning.

    DEPENDENCY: ITEA v3.0 must be computed first.

    Parameters
    ----------
    ca, iro_v145, gee, itea_v3_vals, ict : array-like
        Vectors of inputs. Must all be the same length.

    Returns
    -------
    np.ndarray
        IRA v3.0 values in [0, 1].
    """
    ca = np.asarray(ca, dtype=float)
    iro_v145 = np.asarray(iro_v145, dtype=float)
    gee = np.asarray(gee, dtype=float)
    itea = np.asarray(itea_v3_vals, dtype=float)
    ict = np.asarray(ict, dtype=float)

    valid = (~np.isnan(ca) & ~np.isnan(iro_v145) & ~np.isnan(gee) &
             ~np.isnan(itea) & ~np.isnan(ict))

    if valid.sum() < 4:
        raise ValueError("Insufficient non-missing observations for "
                         "triple residualisation (need ≥ 4)")

    # OLS: IRO_v1.45 ~ const + GEE + ITEA_v3 + ICT, on complete cases
    X = np.column_stack([np.ones(valid.sum()),
                         gee[valid], itea[valid], ict[valid]])
    y = iro_v145[valid]
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)

    # Residuals
    iro_residual = np.full_like(iro_v145, np.nan)
    iro_residual[valid] = y - X @ beta

    # Min-max
    rmin, rmax = np.nanmin(iro_residual), np.nanmax(iro_residual)
    iro_residual_n = (iro_residual - rmin) / (rmax - rmin)

    ca_min, ca_max = np.nanmin(ca), np.nanmax(ca)
    ca_n = (ca - ca_min) / (ca_max - ca_min)

    return 0.60 * ca_n + 0.40 * iro_residual_n


def oaei_v3_mult(itea_v3_vals, gee, ict, ipi):
    """
    OAEI v3.0 multiplicative — canonical Occupational Algorithmic
    Expropriation Index.

    The canonical multiplicative OAEI preserves the structural form
    of v2.1 with the upgraded ITEA v3.0 input. Used for backward
    compatibility with the trilogy of papers (8A, 8B, 8C).

    OAEI_raw = ITEA × GEE × ICT × (1 − IPI)
    OAEI = 1 + 99 × (OAEI_raw − min) / (max − min)   ∈ [1, 100]

    Reference: ITEA v3.0 Consolidated Methodology, §6.1.

    Parameters
    ----------
    itea_v3_vals, gee, ict, ipi : array-like

    Returns
    -------
    np.ndarray
        OAEI v3.0 values in [1, 100].
    """
    itea = np.asarray(itea_v3_vals, dtype=float)
    gee = np.asarray(gee, dtype=float)
    ict = np.asarray(ict, dtype=float)
    ipi = np.asarray(ipi, dtype=float)

    raw = itea * gee * ict * (1 - ipi)
    rmin, rmax = np.nanmin(raw), np.nanmax(raw)
    return 1 + 99 * (raw - rmin) / (rmax - rmin)


def oaei_v3_add(itea_v3_vals, gee, ict, ipi):
    """
    OAEI v3.0+ additive — alternative for criterion-validity-priority
    applications.

    The additive variant improves r(OAEI, Wage) from 0.58 (multiplicative)
    to 0.66, while preserving external convergent validation against
    AIOE at 0.80.

    OAEI+_raw = 0.5·GEE + 0.3·ITEA + 0.2·ICT·(1 − IPI)
    OAEI+ = 1 + 99 × (OAEI+_raw − min) / (max − min)   ∈ [1, 100]

    Reference: ITEA v3.0 Consolidated Methodology, §6.2.
    Motivation: Paper 8B "Beyond the Pigouvian Trap" (García-Lluis
    Valencia, 2026b). See §6.5 for the case-study reasoning.

    Parameters
    ----------
    itea_v3_vals, gee, ict, ipi : array-like

    Returns
    -------
    np.ndarray
        OAEI v3.0+ values in [1, 100].
    """
    itea = np.asarray(itea_v3_vals, dtype=float)
    gee = np.asarray(gee, dtype=float)
    ict = np.asarray(ict, dtype=float)
    ipi = np.asarray(ipi, dtype=float)

    raw = 0.5 * gee + 0.3 * itea + 0.2 * ict * (1 - ipi)
    rmin, rmax = np.nanmin(raw), np.nanmax(raw)
    return 1 + 99 * (raw - rmin) / (rmax - rmin)


def oaei_recommend(use_case: str) -> str:
    """
    Use-case selector — guidance for choosing OAEI variant.

    Reference: ITEA v3.0 Consolidated Methodology, §6.4 Table 6.2.

    Parameters
    ----------
    use_case : str
        One of: 'trilogy_replication', 'aioe_meta_analysis',
        'wage_modelling', 'sectoral_aggregation',
        'theoretical_exposition', 'new_research'.

    Returns
    -------
    str
    """
    recs = {
        "trilogy_replication":     "OAEI v3.0 multiplicative — for backward compatibility with cited formula",
        "aioe_meta_analysis":      "OAEI v3.0+ additive — for maximum AIOE convergence",
        "wage_modelling":          "OAEI v3.0+ additive — criterion validity = 0.66",
        "sectoral_aggregation":    "Either variant — both produce similar SOC Major rankings",
        "theoretical_exposition":  "OAEI v3.0 multiplicative — conceptual alignment with SECI",
        "new_research":            "OAEI v3.0+ additive as primary, multiplicative as robustness check",
    }
    return recs.get(use_case,
                    "Unknown use case. Choose one of: " + ", ".join(recs.keys()))


def itea_reconcile(workbook_path="data/processed/ITEA_v3_0_Workbook.xlsx"):
    """
    Reconciliation check — confirm that the functions reproduce
    the stored workbook values within numerical precision.

    Returns a DataFrame with one row per indicator showing the
    maximum absolute difference between recomputed and stored
    values. All differences should be near machine epsilon.

    Parameters
    ----------
    workbook_path : str
        Path to ITEA_v3_0_Workbook.xlsx.

    Returns
    -------
    pd.DataFrame
        Columns: indicator, max_abs_diff.
    """
    df = pd.read_excel(workbook_path,
                       sheet_name="ITEA_INDICATORS_v3.0", skiprows=2)

    itea_check = itea_v3(df['EAC'], df['EIG'], df['EIA'])
    ira_check = ira_v3(df['CA'], df['IRO v1.45 (legacy)'],
                       df['GEE v2.1'], itea_check, df['ICT'])
    oaei_check = oaei_v3_mult(itea_check, df['GEE v2.1'],
                              df['ICT'], df['IPI'])
    oaei_plus_check = oaei_v3_add(itea_check, df['GEE v2.1'],
                                  df['ICT'], df['IPI'])

    return pd.DataFrame({
        'indicator': ['ITEA v3.0', 'IRA v3.0',
                      'OAEI v3.0', 'OAEI v3.0+ additive'],
        'max_abs_diff': [
            float(np.nanmax(np.abs(itea_check - df['ITEA v3.0']))),
            float(np.nanmax(np.abs(ira_check - df['IRA v3.0']))),
            float(np.nanmax(np.abs(oaei_check - df['OAEI v3.0']))),
            float(np.nanmax(np.abs(oaei_plus_check - df['OAEI v3.0+ additive']))),
        ]
    })


__all__ = [
    'itea_v3', 'ira_v3', 'oaei_v3_mult', 'oaei_v3_add',
    'oaei_recommend', 'itea_reconcile',
]
