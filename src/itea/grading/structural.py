"""
Layer 1 of itea.grading: structural priors from the official O*NET content model.

O*NET publishes, for each of its 41 Generalized Work Activities (GWAs), the
abilities and skills an analyst panel linked to it ("Abilities to Work
Activities", "Skills to Work Activities"). From those links, without any
judgement on individual tasks:

    cognitive share  = linked abilities in 1.A.1 (cognitive) / all linked abilities
    social share     = linked skills in 2.B.1 (social skills) / all linked skills
    K_GWA            = cognitive share × (1 − social share)
    E_GWA            = linked abilities in 1.A.1.a–c (verbal, reasoning,
                       quantitative) / all linked abilities

K_GWA is high for symbolic, non-relational activities (Analyzing Data) and
low for embodied (Handling Objects) or relational ones (Establishing
Relationships). E_GWA is a deliberately weak prior for generative-AI
exposure. Each task then takes the mean over its Detailed Work Activities
of the scores of their GWA.

See docs/grading/METODOLOGIA_v0.2_ES.md, decision D6.
"""

from __future__ import annotations

import os

import numpy as np
import pandas as pd

COGNITIVE = "1.A.1"
SYMBOLIC = ("1.A.1.a", "1.A.1.b", "1.A.1.c")  # verbal, idea generation & reasoning, quantitative
SOCIAL_SKILLS = "2.B.1"


def _read(onet_dir: str, name: str) -> pd.DataFrame:
    return pd.read_csv(os.path.join(onet_dir, f"{name}.txt"), sep="\t", dtype=str)


def gwa_scores(onet_dir: str, social_weight: float = 1.0) -> pd.DataFrame:
    """
    One row per GWA: shares from the official linkage tables, K_GWA and E_GWA.

    `social_weight` scales the social penalty (1 = the canonical formula,
    0 = cognitive share only); it exists for the robustness analysis.
    """
    ab = _read(onet_dir, "Abilities to Work Activities")
    ab.columns = ["ability", "ability_name", "gwa", "gwa_name"]
    sk = _read(onet_dir, "Skills to Work Activities")
    sk.columns = ["skill", "skill_name", "gwa", "gwa_name"]

    a = ab.groupby("gwa").agg(
        gwa_name=("gwa_name", "first"),
        n_abilities=("ability", "size"),
        cognitive_share=("ability", lambda s: s.str.startswith(COGNITIVE).mean()),
        symbolic_share=("ability", lambda s: s.str.startswith(SYMBOLIC).mean()))
    s = sk.groupby("gwa").agg(
        n_skills=("skill", "size"),
        social_share=("skill", lambda x: x.str.startswith(SOCIAL_SKILLS).mean()))
    g = a.join(s, how="left")
    # two physical GWAs have no linked skills: no social component
    g["n_skills"] = g["n_skills"].fillna(0).astype(int)
    g["social_share"] = g["social_share"].fillna(0.0)
    g["K_GWA"] = g["cognitive_share"] * (1 - social_weight * g["social_share"])
    g["E_GWA"] = g["symbolic_share"]
    return g.reset_index().sort_values("K_GWA", ascending=False, ignore_index=True)


def task_links(onet_dir: str) -> pd.DataFrame:
    """Task–DWA–GWA links for every O*NET task (SOC, TaskID, DWA_ID, gwa)."""
    t2d = _read(onet_dir, "Tasks to DWAs").rename(
        columns={"O*NET-SOC Code": "SOC", "Task ID": "TaskID", "DWA ID": "DWA_ID"})
    dwa = _read(onet_dir, "DWA Reference").rename(columns={"DWA ID": "DWA_ID", "Element ID": "gwa"})
    return t2d[["SOC", "TaskID", "DWA_ID"]].merge(dwa[["DWA_ID", "gwa"]], on="DWA_ID", how="left")


def task_prior(onet_dir: str, scores: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Structural priors K1 and E1 for each O*NET task: the mean, over the task's
    DWAs, of the K_GWA and E_GWA of each DWA's GWA (equal weights, because
    O*NET does not rate the importance of a DWA within a task).
    """
    scores = gwa_scores(onet_dir) if scores is None else scores
    links = task_links(onet_dir).merge(scores[["gwa", "K_GWA", "E_GWA"]], on="gwa", how="left")
    out = links.groupby(["SOC", "TaskID"]).agg(
        n_dwa=("DWA_ID", "nunique"), n_gwa=("gwa", "nunique"),
        K1=("K_GWA", "mean"), E1=("E_GWA", "mean")).reset_index()
    out["soc6"] = out["SOC"].str[:7]
    return out


def within_share(values: pd.Series, groups: pd.Series) -> float:
    """
    Share of the variance of `values` that lies within `groups`
    (1 − between/total). Used to check that later layers add discrimination
    inside each GWA, which the structural prior alone cannot provide.
    """
    v = pd.to_numeric(values, errors="coerce")
    total = float(np.nanvar(v))
    if total == 0:
        return 0.0
    between = float(np.nanvar(v.groupby(groups).transform("mean")))
    return 1 - between / total
