"""
AXI task grades and their roll-up to activities and occupations.

The AXI dataset grades each of the 47,810 O*NET task statements on four
ordinal scales (Auto_Grade, CI_Grade, GenAI_Impact, Agentic_Impact). ITEA
v4.0 does not average these grades directly by occupation. It first rolls
them up to O*NET Detailed Work Activities (DWAs), so that the unit of
analysis is the activity rather than the job title, and then maps the
activity shares back onto every O*NET-SOC occupation through the official
Tasks-to-DWAs table. An occupation whose own AXI tasks do not match the
current O*NET release still receives shares through the activities it
performs.

Reference: ITEA v4.0 design specification (v4.0/docs/ITEA_v4_0_SPEC_DISENO.md).
"""

from __future__ import annotations

import os

import pandas as pd

from .rollup import to_activities, to_occupations

# The grade that counts as "high" on each AXI scale.
HIGH = {
    "Auto_Grade": "HIGH",
    "CI_Grade": "HIGH_ALGO",
    "GenAI_Impact": "High",
    "Agentic_Impact": "High",
}

# Output column for each scale: percentage of graded tasks at the high level.
SHARE_COLUMNS = {
    "Auto_Grade": "pct_Auto_HIGH",
    "CI_Grade": "pct_CI_HIGH_ALGO",
    "GenAI_Impact": "pct_GenAI_High",
    "Agentic_Impact": "pct_Agentic_High",
}


def normalise_text(s: pd.Series) -> pd.Series:
    """Lower-case, strip punctuation and collapse whitespace for exact matching."""
    s = s.astype(str).str.lower().str.replace(r"[^a-z0-9 ]", "", regex=True)
    return s.str.replace(r"\s+", " ", regex=True).str.strip()


def load_axi(path: str) -> pd.DataFrame:
    """
    Load the AXI task grades (CSV, optionally gzipped, or parquet).

    Required columns: SOC_CODE, Task_Description and the four grade columns.
    """
    df = pd.read_parquet(path) if path.endswith(".parquet") else pd.read_csv(path, dtype=str)
    missing = {"SOC_CODE", "Task_Description", *HIGH} - set(df.columns)
    if missing:
        raise ValueError(f"AXI file lacks columns: {sorted(missing)}")
    return df


def load_onet(onet_dir: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Read the two O*NET text-database tables the roll-up needs.

    Returns (task_statements, tasks_to_dwas) with columns renamed to
    SOC, TaskID, Task and SOC, TaskID, DWA_ID respectively.
    """
    ts = pd.read_csv(os.path.join(onet_dir, "Task Statements.txt"), sep="\t", dtype=str)
    ts = ts.rename(columns={"O*NET-SOC Code": "SOC", "Task ID": "TaskID"})[["SOC", "TaskID", "Task"]]
    t2d = pd.read_csv(os.path.join(onet_dir, "Tasks to DWAs.txt"), sep="\t", dtype=str)
    t2d = t2d.rename(columns={"O*NET-SOC Code": "SOC", "Task ID": "TaskID", "DWA ID": "DWA_ID"})
    return ts, t2d[["SOC", "TaskID", "DWA_ID"]]


def match_tasks(axi: pd.DataFrame, task_statements: pd.DataFrame) -> pd.DataFrame:
    """
    Attach the O*NET Task ID to each AXI task by exact normalised text within
    the same O*NET-SOC code. Unmatched tasks (release drift) are dropped.
    """
    key = task_statements["SOC"] + "||" + normalise_text(task_statements["Task"])
    # identical statements within one occupation keep the first Task ID
    key_to_id = task_statements.assign(k=key).drop_duplicates("k").set_index("k")["TaskID"].to_dict()
    out = axi.copy()
    out["TaskID"] = (out["SOC_CODE"].astype(str) + "||" + normalise_text(out["Task_Description"])).map(key_to_id)
    return out.dropna(subset=["TaskID"])


def activity_shares(matched: pd.DataFrame, tasks_to_dwas: pd.DataFrame) -> pd.DataFrame:
    """
    Percentage of high-graded AXI tasks per DWA, for each of the four scales.

    Each matched task contributes once to every DWA it is linked to.
    Shares are rounded to one decimal, as in the published v4.0 tables.
    """
    # a high grade becomes 100, any other grade 0, so the activity mean is a percentage
    flags = matched[["TaskID"]].copy()
    for col, high in HIGH.items():
        flags[SHARE_COLUMNS[col]] = (matched[col] == high) * 100.0
    out = to_activities(flags, tasks_to_dwas, SHARE_COLUMNS.values())
    out[list(SHARE_COLUMNS.values())] = out[list(SHARE_COLUMNS.values())].round(1)
    return out.rename(columns={"n_tasks": "n_axi_tasks"})


def occupation_shares(dwa_shares: pd.DataFrame, tasks_to_dwas: pd.DataFrame) -> pd.DataFrame:
    """
    Map activity shares back to O*NET-SOC occupations.

    An occupation's share is the mean over all its task-DWA links of the
    shares of the linked DWAs (DWAs without graded tasks are ignored).
    """
    return to_occupations(dwa_shares, tasks_to_dwas, SHARE_COLUMNS.values())


def axi_to_occupations(axi: pd.DataFrame, onet_dir: str) -> pd.DataFrame:
    """Full roll-up: AXI tasks -> O*NET tasks -> DWAs -> O*NET-SOC occupations."""
    ts, t2d = load_onet(onet_dir)
    matched = match_tasks(axi, ts)
    return occupation_shares(activity_shares(matched, t2d), t2d)
