"""
Grading layer 5: composite K and E per task and their uncertainty, following
the OECD/JRC handbook on composite indicators. Design and hypotheses
(H18–H20) are registered in docs/grading/HIPOTESIS_PREREGISTRADAS_ES.md.

Central grades: equal-weight mean of the percentile ranks of the components
that passed their validation hypotheses. Monte Carlo: random component
weights (Dirichlet), random exclusion of one component, rank or min–max
normalisation and κ in [0.30, 0.50]; the index is rebuilt in every draw.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ..oaxi_eu import minmax


def normalise(df: pd.DataFrame, cols, how: str = "rank") -> pd.DataFrame:
    """Percentile ranks (default) or min–max scaling of each column."""
    if how == "rank":
        return df[list(cols)].rank(pct=True)
    return df[list(cols)].apply(minmax)


def composite(df: pd.DataFrame, cols, weights=None, how: str = "rank") -> pd.Series:
    """Weighted mean of the normalised components (weights default to equal)."""
    n = normalise(df, cols, how)
    w = np.ones(len(cols)) if weights is None else np.asarray(weights, dtype=float)
    return (n * w).sum(axis=1) / w.sum()


def draw_spec(rng: np.random.Generator, k_cols, e_cols) -> dict:
    """One Monte Carlo specification of the method choices."""
    def pick(cols):
        cols = list(cols)
        if len(cols) > 1 and rng.random() < 0.5:
            cols.pop(rng.integers(len(cols)))
        return cols, rng.dirichlet(np.ones(len(cols)))
    kc, kw = pick(k_cols)
    ec, ew = pick(e_cols)
    return {"k_cols": kc, "k_w": kw, "e_cols": ec, "e_w": ew,
            "how": "rank" if rng.random() < 0.5 else "minmax", "kappa": float(rng.uniform(0.30, 0.50))}


def eta_squared(factor: pd.Series, outcome: pd.Series, bins: int = 10) -> float:
    """First-order sensitivity: share of the outcome variance explained by a (binned) factor."""
    f = pd.qcut(factor, bins, duplicates="drop") if pd.api.types.is_float_dtype(factor) else factor
    groups = outcome.groupby(f, observed=True)
    between = (groups.size() * (groups.mean() - outcome.mean()) ** 2).sum()
    total = ((outcome - outcome.mean()) ** 2).sum()
    return float(between / total) if total > 0 else 0.0
