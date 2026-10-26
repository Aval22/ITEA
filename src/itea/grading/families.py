"""
Layer F (ITEA 4.2): which family of AI would perform each task, and in which mode.

Two outputs per O*NET 30.2 task, both summing to 1:
  - a family vector F1–F7, anchored in Eurostat's AI technology types (isoc_eb_ai);
  - a task-type vector T_A–T_E (direct people, decide, relate, analyse, physical).

The family vector is *conditional on exposure*: it says which family would do the
automatable part of a task, not how much of it is automatable (that is E, and K for
alienability). Rules are fixed in docs/grading/LIBRO_CRITERIOS_capa_F_v0.1_ES.md
(26-10-2026) and must not be tuned to results; validation (H21–H25) is registered in
docs/grading/HIPOTESIS_PREREGISTRADAS_ES.md.
"""

from __future__ import annotations

import os

import numpy as np
import pandas as pd

FAMILIES = {
    "F1": ("Text analysis", "E_AI_TTM"),
    "F2": ("Language or code generation", "E_AI_TNLG"),
    "F3": ("Speech", "E_AI_TSR"),
    "F4": ("Vision", "E_AI_TIR"),
    "F5": ("Machine learning for data analysis", "E_AI_TML"),
    "F6": ("Workflow automation and decision support", "E_AI_TPA"),
    "F7": ("Robotics and autonomous movement", "E_AI_TAR"),
}
FAM = list(FAMILIES)

# GWA -> family weights (criteria book v0.1, section 3). Each row sums to 1.
GWA_FAMILY = {
    "4.A.1.a.1": {"F1": .7, "F2": .3},
    "4.A.1.a.2": {"F4": .5, "F5": .5},
    "4.A.1.b.1": {"F4": .7, "F5": .3},
    "4.A.1.b.2": {"F4": .8, "F7": .2},
    "4.A.1.b.3": {"F4": .3, "F5": .7},
    "4.A.2.a.1": {"F1": .3, "F4": .3, "F5": .4},
    "4.A.2.a.2": {"F1": .5, "F6": .5},
    "4.A.2.a.3": {"F1": .5, "F6": .5},
    "4.A.2.a.4": {"F1": .3, "F5": .7},
    "4.A.2.b.1": {"F2": .2, "F5": .3, "F6": .5},
    "4.A.2.b.2": {"F2": 1.0},
    "4.A.2.b.3": {"F1": .6, "F2": .4},
    "4.A.2.b.4": {"F2": .5, "F5": .25, "F6": .25},
    "4.A.2.b.5": {"F6": 1.0},
    "4.A.2.b.6": {"F2": .3, "F6": .7},
    "4.A.3.a.1": {"F7": 1.0},
    "4.A.3.a.2": {"F7": 1.0},
    "4.A.3.a.3": {"F6": .4, "F7": .6},
    "4.A.3.a.4": {"F7": 1.0},
    "4.A.3.b.1": {"F2": .5, "F6": .5},
    "4.A.3.b.2": {"F2": .5, "F4": .5},
    "4.A.3.b.4": {"F5": .3, "F7": .7},
    "4.A.3.b.5": {"F5": .4, "F7": .6},
    "4.A.3.b.6": {"F1": .3, "F2": .4, "F3": .3},
    "4.A.4.a.1": {"F1": .3, "F2": .7},
    "4.A.4.a.2": {"F2": .7, "F3": .3},
    "4.A.4.a.3": {"F2": .6, "F3": .4},
    "4.A.4.a.4": {"F2": .5, "F3": .5},
    "4.A.4.a.5": {"F2": .25, "F3": .25, "F7": .5},
    "4.A.4.a.6": {"F2": .6, "F5": .4},
    "4.A.4.a.7": {"F2": 1.0},
    "4.A.4.a.8": {"F2": .5, "F3": .5},
    "4.A.4.b.1": {"F2": .3, "F6": .7},
    "4.A.4.b.2": {"F2": .5, "F5": .5},
    "4.A.4.b.3": {"F2": .7, "F3": .3},
    "4.A.4.b.4": {"F2": .5, "F6": .5},
    "4.A.4.b.5": {"F2": .7, "F5": .3},
    "4.A.4.b.6": {"F1": .3, "F2": .7},
    "4.A.4.c.1": {"F1": .3, "F6": .7},
    "4.A.4.c.2": {"F5": .5, "F6": .5},
    "4.A.4.c.3": {"F5": .5, "F6": .5},
}

TASK_TYPES = {
    "A": ("Direct and supervise people", ["4.A.4.b.1", "4.A.4.b.2", "4.A.4.b.4", "4.A.4.b.5", "4.A.4.c.2", "4.A.4.c.3"]),
    "B": ("Decide, plan and create", ["4.A.2.b.1", "4.A.2.b.2", "4.A.2.b.4", "4.A.2.b.5", "4.A.2.b.6"]),
    "C": ("Advise, teach and relate", ["4.A.4.a.", "4.A.4.b.3", "4.A.4.b.6"]),
    "D": ("Analyse and process information", ["4.A.1.a.1", "4.A.1.b.3", "4.A.2.a.", "4.A.2.b.3", "4.A.3.b.1", "4.A.3.b.6", "4.A.4.c.1"]),
    "E": ("Physical and technical work", ["4.A.1.a.2", "4.A.1.b.1", "4.A.1.b.2", "4.A.3.a.", "4.A.3.b.2", "4.A.3.b.4", "4.A.3.b.5"]),
}
TYPES = [f"T_{k}" for k in TASK_TYPES]   # prefixed: "E" would clash with exposure


def gwa_matrix(rules: dict = GWA_FAMILY) -> pd.DataFrame:
    """GWA × F1–F7 weight matrix; rows are renormalised to sum to 1."""
    m = pd.DataFrame(rules).T.reindex(columns=FAM).fillna(0.0)
    return m.div(m.sum(axis=1), axis=0)


def task_type_of(gwa: str) -> str | None:
    for code, (_, prefixes) in TASK_TYPES.items():
        if any(gwa.startswith(p) for p in prefixes):
            return f"T_{code}"
    return None


def task_gwa_links(onet_dir: str) -> pd.DataFrame:
    """(O*NET-SOC Code, Task ID, GWA) for every task–DWA link in O*NET."""
    td = pd.read_csv(os.path.join(onet_dir, "Tasks to DWAs.txt"), sep="\t", dtype=str)
    dr = pd.read_csv(os.path.join(onet_dir, "DWA Reference.txt"), sep="\t", dtype=str)
    out = td.merge(dr[["DWA ID", "Element ID"]], on="DWA ID", how="left")
    return out.rename(columns={"Element ID": "GWA"})[["O*NET-SOC Code", "Task ID", "GWA"]]


def task_vectors(links: pd.DataFrame, rules: dict = GWA_FAMILY) -> pd.DataFrame:
    """Per task: family shares F1–F7 and task-type shares A–E (means over its DWAs).

    `links` has columns O*NET-SOC Code, Task ID, GWA. Unknown GWAs raise, so a change
    in O*NET cannot be silently absorbed."""
    gm = gwa_matrix(rules)
    unknown = set(links.GWA.dropna()) - set(gm.index)
    if unknown:
        raise ValueError(f"GWA without a family rule: {sorted(unknown)}")
    fam = gm.reindex(links.GWA).set_index(links.index)
    typ = pd.get_dummies(links.GWA.map(task_type_of)).reindex(columns=TYPES, fill_value=0).astype(float)
    df = pd.concat([links[["O*NET-SOC Code", "Task ID"]], fam, typ], axis=1)
    out = df.groupby(["O*NET-SOC Code", "Task ID"])[FAM + TYPES].mean().reset_index()
    out["n_dwa"] = df.groupby(["O*NET-SOC Code", "Task ID"]).size().values
    return out


def attach(grades: pd.DataFrame, vectors: pd.DataFrame) -> pd.DataFrame:
    """Join task grades (SOC, TaskID, K, E, …) with layer-F vectors. Tasks without any DWA
    get the mean vector of their occupation and are flagged (imputed=True)."""
    v = vectors.rename(columns={"O*NET-SOC Code": "SOC", "Task ID": "TaskID"})
    g = grades.merge(v, on=["SOC", "TaskID"], how="left")
    g["imputed"] = g[FAM[0]].isna()
    cols = FAM + TYPES
    g[cols] = g[cols].fillna(g.groupby("SOC")[cols].transform("mean"))
    return g


def surface_by_family(tasks: pd.DataFrame, in_play: pd.Series, weight: pd.Series) -> pd.Series:
    """Share of the alienable surface (tasks in play) carried by each family:
    Σ weight·in_play·F_f / Σ weight·in_play."""
    w = (weight * in_play).astype(float)
    return tasks[FAM].mul(w, axis=0).sum() / w.sum()


def perturb_rules(rng: np.random.Generator, rules: dict = GWA_FAMILY, scale: float = 0.2) -> dict:
    """Random perturbation of the rule weights (±scale, uniform, on non-zero cells),
    renormalised; used for the sensitivity band (criteria book, section 6.3)."""
    out = {}
    for gwa, w in rules.items():
        p = {f: max(v * (1 + rng.uniform(-scale, scale)), 0.0) for f, v in w.items()}
        s = sum(p.values())
        out[gwa] = {f: v / s for f, v in p.items()}
    return out


def adoption_by_family(fetch=None, geos=("EU27_2020", "ES"), years=("2024", "2025"),
                       dataset: str = "isoc_eb_ain2") -> pd.DataFrame:
    """Enterprise adoption of each AI family (% of enterprises with 10+ employees) by country
    and NACE sector, from Eurostat. Returns geo, nace_r2, family, time, value."""
    if fetch is None:
        from .eurostat import fetch_dataset as fetch
    codes = {v[1]: k for k, v in FAMILIES.items()}
    df = fetch(dataset, geo=list(geos), time=list(years), indic_is=list(codes),
               size_emp="GE10", unit="PC_ENT")
    df = df[df.indic_is.isin(codes)].copy()
    df["family"] = df.indic_is.map(codes)
    keep = [c for c in ("dataset", "geo", "nace_r2", "family", "indic_is", "time", "value", "retrieved") if c in df]
    return df[keep].reset_index(drop=True)
