"""
External validation of itea.grading against independent, public references.

None of these references is used to build the grades (decision D7 in
docs/grading/DECISIONES_ES.md):

    E  ↔  human exposure labels of Eloundou et al. (2024), per O*NET Task ID
    K  ↔  routine-cognitive index of Acemoglu & Autor (2011), from Work Context
    K  ↔  non-routine cognitive analytical index (Acemoglu & Autor, 2011)
    K, E ↔ Job Zone (discriminant check: the grades should not be qualification in disguise)

Agreement is reported with chance-corrected statistics and bootstrap
confidence intervals that resample occupations, not tasks, because tasks of
the same occupation are not independent.
"""

from __future__ import annotations

import os

import numpy as np
import pandas as pd

# Eloundou et al. rubric: E1 = direct exposure, E2 = exposure with complementary
# tools, E0 = none. beta = E1 + 0.5·E2 is their headline measure.
ELOUNDOU_BETA = {"E0": 0.0, "E2": 0.5, "E1": 1.0}

# Acemoglu & Autor (2011) O*NET elements (as reproduced by Webb 2020, App. D.2)
ROUTINE_COGNITIVE = {"4.C.3.b.7": 1, "4.C.3.b.4": 1, "4.C.3.b.8": -1}  # 4.C.3.b.8 reversed
NONROUTINE_ANALYTICAL = ("4.A.2.a.4", "4.A.2.b.2", "4.A.4.a.1")


def eloundou_labels(path: str) -> pd.DataFrame:
    """Human exposure labels per O*NET task: SOC, TaskID, human_label, human_beta."""
    d = pd.read_csv(path, sep="\t")
    d = d.dropna(subset=["Task ID", "human_exposure_agg"])
    out = pd.DataFrame({
        "SOC": d["O*NET-SOC Code"].astype(str),
        "TaskID": d["Task ID"].astype(int).astype(str),   # stored as float in the source
        "human_label": d["human_exposure_agg"],
    })
    out["human_beta"] = out["human_label"].map(ELOUNDOU_BETA)
    return out.drop_duplicates(["SOC", "TaskID"])


def _standardise(s: pd.Series) -> pd.Series:
    return (s - s.mean()) / s.std(ddof=0)


def task_content_indices(onet_dir: str) -> pd.DataFrame:
    """
    Occupation-level routine-cognitive and non-routine-analytical indices
    (Acemoglu & Autor, 2011) and Job Zone, from O*NET 30.2.

    Each element is standardised across occupations; an index is the mean of
    its (signed) standardised elements.
    """
    wc = pd.read_csv(os.path.join(onet_dir, "Work Context.txt"), sep="\t", dtype=str)
    wc = wc[(wc["Scale ID"] == "CX") & wc["Element ID"].isin(ROUTINE_COGNITIVE)]
    wc = wc.assign(v=pd.to_numeric(wc["Data Value"])).pivot_table(
        index="O*NET-SOC Code", columns="Element ID", values="v")
    rc = sum(sign * _standardise(wc[e]) for e, sign in ROUTINE_COGNITIVE.items()) / len(ROUTINE_COGNITIVE)

    wa = pd.read_csv(os.path.join(onet_dir, "Work Activities.txt"), sep="\t", dtype=str)
    wa = wa[(wa["Scale ID"] == "IM") & wa["Element ID"].isin(NONROUTINE_ANALYTICAL)]
    wa = wa.assign(v=pd.to_numeric(wa["Data Value"])).pivot_table(
        index="O*NET-SOC Code", columns="Element ID", values="v")
    nra = sum(_standardise(wa[e]) for e in NONROUTINE_ANALYTICAL) / len(NONROUTINE_ANALYTICAL)

    jz = pd.read_csv(os.path.join(onet_dir, "Job Zones.txt"), sep="\t", dtype=str)
    jz = jz.set_index("O*NET-SOC Code")["Job Zone"].astype(float)

    out = pd.DataFrame({"routine_cognitive": rc, "nonroutine_analytical": nra}).join(jz.rename("job_zone"), how="outer")
    return out.rename_axis("SOC").reset_index()


def weighted_kappa(a, b, categories) -> float:
    """Cohen's kappa with linear weights for two ordinal ratings over `categories` (in order)."""
    idx = {c: i for i, c in enumerate(categories)}
    x = np.array([idx[v] for v in a])
    y = np.array([idx[v] for v in b])
    k = len(categories)
    obs = np.zeros((k, k))
    np.add.at(obs, (x, y), 1)
    obs /= obs.sum()
    exp = np.outer(obs.sum(1), obs.sum(0))
    w = 1 - np.abs(np.subtract.outer(np.arange(k), np.arange(k))) / (k - 1)
    return float(1 - (1 - (w * obs).sum()) / (1 - (w * exp).sum()))


def bootstrap_corr(df: pd.DataFrame, x: str, y: str, cluster: str = "SOC",
                   method: str = "spearman", n_boot: int = 1000, seed: int = 20261023) -> dict:
    """Correlation of x and y with a percentile CI that resamples whole clusters (occupations)."""
    d = df[[x, y, cluster]].dropna()
    point = float(d[x].corr(d[y], method=method))
    groups = d.groupby(cluster).indices
    keys = np.array(list(groups))
    rng = np.random.default_rng(seed)
    draws = []
    for _ in range(n_boot):
        pick = rng.choice(len(keys), len(keys), replace=True)
        rows = np.concatenate([groups[keys[i]] for i in pick])
        s = d.iloc[rows]
        draws.append(s[x].corr(s[y], method=method))
    lo, hi = np.nanpercentile(draws, [2.5, 97.5])
    return {"r": point, "ci95": (float(lo), float(hi)), "n": int(len(d)), "clusters": int(len(keys))}


def _within_ranks(d: pd.DataFrame, col: str, by: str) -> pd.Series:
    """Ranks of `col` centred within each `by` group (removes the group effect)."""
    r = d[col].rank()
    return r - r.groupby(d[by]).transform("mean")


def bootstrap_partial_corr(df: pd.DataFrame, x: str, y: str, by: str, cluster: str = "SOC",
                           n_boot: int = 1000, seed: int = 20261023) -> dict:
    """
    Spearman correlation of x and y net of the categorical control `by`
    (ranks centred within each `by` group), with a CI that resamples clusters.
    """
    d = df[[x, y, by, cluster]].dropna().reset_index(drop=True)

    def stat(s: pd.DataFrame) -> float:
        return float(_within_ranks(s, x, by).corr(_within_ranks(s, y, by)))

    point = stat(d)
    groups = d.groupby(cluster).indices
    keys = np.array(list(groups))
    rng = np.random.default_rng(seed)
    draws = []
    for _ in range(n_boot):
        pick = rng.choice(len(keys), len(keys), replace=True)
        draws.append(stat(d.iloc[np.concatenate([groups[keys[i]] for i in pick])].reset_index(drop=True)))
    lo, hi = np.nanpercentile(draws, [2.5, 97.5])
    return {"r": point, "ci95": (float(lo), float(hi)), "n": int(len(d)), "clusters": int(len(keys))}
