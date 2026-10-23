"""
Generic roll-up of task-level scores: tasks -> activities -> occupations -> ISCO-08.

These functions do not depend on AXI. Any numeric score attached to O*NET
Task IDs (for instance the LLM-exposure ratings of Eloundou et al., 2024, or
a user's own coding) can be carried to O*NET Detailed Work Activities, back
to every O*NET-SOC occupation that performs them, and on to ISCO-08 through
a weighted crosswalk.
"""

from __future__ import annotations

import pandas as pd


def to_activities(tasks: pd.DataFrame, tasks_to_dwas: pd.DataFrame, cols, task_id: str = "TaskID") -> pd.DataFrame:
    """
    Mean of each score in `cols` over the tasks linked to each DWA.

    `tasks` has one row per scored task with column `task_id`; a task linked
    to several DWAs contributes to each of them. Returns DWA_ID, the means of
    `cols` and n_tasks (distinct scored tasks per DWA).
    """
    cols = list(cols)
    links = tasks_to_dwas[["TaskID", "DWA_ID"]].rename(columns={"TaskID": task_id})
    md = tasks[[task_id, *cols]].merge(links, on=task_id, how="inner")
    out = md.groupby("DWA_ID")[cols].mean()
    out["n_tasks"] = md.groupby("DWA_ID")[task_id].nunique()
    return out.reset_index()


def to_occupations(activities: pd.DataFrame, tasks_to_dwas: pd.DataFrame, cols) -> pd.DataFrame:
    """
    Score of each O*NET-SOC occupation: mean over all its task-DWA links of the
    linked activities' scores (activities without a score are ignored).
    Returns SOC, soc6 (6-digit SOC 2018 code) and `cols`.
    """
    cols = list(cols)
    occ = tasks_to_dwas[["SOC", "DWA_ID"]].merge(activities[["DWA_ID", *cols]], on="DWA_ID", how="left")
    occ = occ.groupby("SOC")[cols].mean().dropna(how="all").reset_index()
    occ["soc6"] = occ["SOC"].str[:7]
    return occ


def to_isco(occupations: pd.DataFrame, crosswalk: pd.DataFrame, cols) -> pd.DataFrame:
    """
    Crosswalk-weighted mean of `cols` for each ISCO-08 unit group.

    `occupations` needs SOC, soc6 and `cols`; `crosswalk` needs soc2018, isco, w.
    Returns isco, `cols` and n_soc (distinct O*NET-SOC occupations mapped).
    """
    cols = list(cols)
    d = occupations.merge(crosswalk, left_on="soc6", right_on="soc2018", how="inner")
    weighted = d[cols].mul(d["w"], axis=0).assign(isco=d["isco"], w=d["w"])
    g = weighted.groupby("isco").sum(min_count=1)
    out = g[cols].div(g["w"], axis=0)
    out["n_soc"] = d.groupby("isco")["SOC"].nunique()
    return out.reset_index()
