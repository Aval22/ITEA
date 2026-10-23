"""
OAXI-EU — occupational algorithmic-expropriability index on the ISCO-08 axis.

    E   = share of an occupation's activities with high generative-AI impact
    K   = share with algorithmically codifiable knowledge (CI_Grade = HIGH_ALGO)
    core = norm(E)^(1-κ) · norm(K)^κ          (geometric conjunction)
    OAXI-EU = 1 + 99 · minmax(core)            (scale 1..100, as OAEI v3.0)

Expropriability requires both exposure and codifiability, hence the
geometric rather than additive combination. κ = 0.40 maximises convergence
with an independent ISCO-3 exposure benchmark (JRC145832); the optimum is
flat between 0.3 and 0.4, so results are not sensitive to the exact value.

OAXI-EU measures a potential (which occupations' knowledge is most open to
codification by generative AI), not a realised transfer of value.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .rollup import to_isco

KAPPA = 0.40


def minmax(s) -> pd.Series:
    """Min-max scaling to [0, 1]; a constant series maps to 0."""
    s = pd.to_numeric(pd.Series(s), errors="coerce")
    lo, hi = s.min(), s.max()
    return (s - lo) / (hi - lo) if hi > lo else s * 0.0


def oaxi_eu(occ: pd.DataFrame, crosswalk: pd.DataFrame, kappa: float = KAPPA,
            exposure: str = "pct_GenAI_High", codifiability: str = "pct_CI_HIGH_ALGO") -> pd.DataFrame:
    """
    Compute OAXI-EU for every ISCO-08 unit group reached by the crosswalk.

    Parameters
    ----------
    occ : DataFrame
        One row per O*NET-SOC occupation with columns SOC, soc6 and the
        exposure and codifiability shares (output of itea.axi.axi_to_occupations).
    crosswalk : DataFrame
        Columns soc2018, isco, w (output of itea.crosswalk.build_crosswalk).
    kappa : float
        Weight of codifiability in the geometric core, in [0, 1].

    Returns
    -------
    DataFrame with columns isco, isco3, E, K, n_soc, core, OAXI_EU,
    sorted by OAXI_EU descending.
    """
    if not 0.0 <= kappa <= 1.0:
        raise ValueError("kappa must lie in [0, 1]")
    d = occ.dropna(subset=[exposure, codifiability]).copy()
    d["E"], d["K"] = minmax(d[exposure]).values, minmax(d[codifiability]).values
    # weighted mean over the SOC occupations that map to each ISCO group
    g = to_isco(d, crosswalk, ["E", "K"])

    gE, gK = minmax(g["E"]).clip(lower=1e-6), minmax(g["K"]).clip(lower=1e-6)
    g["core"] = gE ** (1 - kappa) * gK ** kappa
    g["OAXI_EU"] = 1 + 99 * minmax(g["core"])
    g["isco3"] = g["isco"].str[:3]
    cols = ["isco", "isco3", "E", "K", "n_soc", "core", "OAXI_EU"]
    return g[cols].sort_values("OAXI_EU", ascending=False).reset_index(drop=True)


def convergence(index: pd.DataFrame, criterion: pd.DataFrame, value: str = "OAXI_EU",
                criterion_col: str = "score") -> dict:
    """
    Pearson and Spearman correlation with an external benchmark at ISCO-3.

    `criterion` needs columns isco3 and `criterion_col`. The index is first
    averaged over the ISCO-4 groups within each ISCO-3 group.
    """
    crit = criterion.assign(isco3=criterion["isco3"].astype(str).str.zfill(3))
    g3 = index.groupby("isco3")[value].mean().reset_index().merge(crit, on="isco3", how="inner")
    return {"n_isco3": int(len(g3)),
            "pearson": float(g3[value].corr(g3[criterion_col])),
            "spearman": float(g3[value].corr(g3[criterion_col], method="spearman"))}


def kappa_grid(occ: pd.DataFrame, crosswalk: pd.DataFrame, criterion: pd.DataFrame,
               kappas=np.round(np.arange(0.0, 1.01, 0.1), 2), criterion_col: str = "score") -> pd.DataFrame:
    """Convergence with the benchmark for each κ in `kappas` (calibration table)."""
    rows = [{"kappa": float(k), **convergence(oaxi_eu(occ, crosswalk, k), criterion,
                                              criterion_col=criterion_col)} for k in kappas]
    return pd.DataFrame(rows)
