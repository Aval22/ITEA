#!/usr/bin/env python3
"""
Stratified sample of O*NET 30.2 tasks for the human reference coding of K and E.

Implements section 6 of docs/grading/LIBRO_CRITERIOS_v0.1_ES.md:
    - 400 tasks, stratified by the provisional GWA prior class (high/medium/low
      codifiability, equal allocation) and, within class, by SOC major group
      (proportional, largest remainder);
    - a hidden subset of 100 tasks (stratified by class) for the intra-coder
      re-coding at least three weeks later.

The coding form shows only the task statement and the occupation title, so
the coder stays blind to the GWA, the prior class and any model score. The
key (GWA, class, stratum, re-code flag) is written to a separate file that
the coder should not open.

Usage:
    python scripts/grading/make_human_sample.py --onet <db_30_2_text dir> \
        --form docs/grading/codificacion_humana/ITEA_codificacion_K_E_400.xlsx \
        --key <private dir>/muestra_400_clave.csv
"""

from __future__ import annotations

import argparse
import os

import numpy as np
import pandas as pd

SEED = 20261023
N_SAMPLE = 400
N_RECODE = 100

# Provisional prior codifiability class of each O*NET Generalized Work
# Activity (LIBRO_CRITERIOS v0.1, section 3). Used only to balance the sample.
GWA_CLASS = {
    "high": ["4.A.1.a.1", "4.A.2.a.2", "4.A.2.a.4", "4.A.2.a.3", "4.A.1.b.3",
             "4.A.3.b.6", "4.A.3.b.1", "4.A.2.b.5", "4.A.4.c.1"],
    "medium": ["4.A.2.b.1", "4.A.2.b.2", "4.A.2.b.3", "4.A.2.b.4", "4.A.2.b.6",
               "4.A.2.a.1", "4.A.4.a.1", "4.A.4.b.6", "4.A.4.c.3", "4.A.4.a.2",
               "4.A.4.a.3", "4.A.4.b.3", "4.A.4.c.2", "4.A.4.a.6"],
    "low": ["4.A.3.a.1", "4.A.3.a.2", "4.A.3.a.3", "4.A.3.a.4", "4.A.3.b.4",
            "4.A.1.b.2", "4.A.1.b.1", "4.A.1.a.2", "4.A.4.a.5", "4.A.4.a.4",
            "4.A.4.a.7", "4.A.4.a.8", "4.A.4.b.4", "4.A.4.b.5"],
}
SCORE = {"high": 1.0, "medium": 0.5, "low": 0.0}


def prior_class(onet_dir: str) -> pd.DataFrame:
    """One row per O*NET task: SOC, title, statement, GWAs and prior class."""
    ts = pd.read_csv(os.path.join(onet_dir, "Task Statements.txt"), sep="\t", dtype=str)
    t2d = pd.read_csv(os.path.join(onet_dir, "Tasks to DWAs.txt"), sep="\t", dtype=str)
    dwa = pd.read_csv(os.path.join(onet_dir, "DWA Reference.txt"), sep="\t", dtype=str)
    occ = pd.read_csv(os.path.join(onet_dir, "Occupation Data.txt"), sep="\t", dtype=str)

    gwa_score = {g: SCORE[c] for c, gs in GWA_CLASS.items() for g in gs}
    links = t2d.merge(dwa[["DWA ID", "Element ID"]], on="DWA ID")
    links["score"] = links["Element ID"].map(gwa_score)
    by_task = links.groupby("Task ID").agg(
        gwa=("Element ID", lambda s: ";".join(sorted(set(s)))),
        prior=("score", "mean")).reset_index()
    # mean of the task's GWA classes, cut back into three classes
    by_task["prior_class"] = pd.cut(by_task["prior"], [-0.01, 0.25, 0.75, 1.01],
                                    labels=["low", "medium", "high"]).astype(str)

    t = ts.merge(by_task, on="Task ID", how="inner").merge(
        occ[["O*NET-SOC Code", "Title"]], on="O*NET-SOC Code", how="left")
    t["soc_major"] = t["O*NET-SOC Code"].str[:2]
    return t


def allocate(weights: pd.Series, total: int, cap: pd.Series | None = None) -> pd.Series:
    """Largest-remainder allocation of `total` in proportion to `weights`, optionally capped."""
    raw = weights / weights.sum() * total
    n = np.floor(raw).astype(int)
    for k in (raw - n).sort_values(ascending=False).index[: total - n.sum()]:
        n[k] += 1
    return n if cap is None else n.clip(upper=cap)


def draw(t: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    # equal allocation across the three prior classes
    per_class = allocate(pd.Series(1.0, index=["high", "medium", "low"]), N_SAMPLE)
    parts = []
    for cls, n_cls in per_class.items():
        pool = t[t["prior_class"] == cls]
        sizes = pool.groupby("soc_major").size()
        quota = allocate(sizes, n_cls, cap=sizes)
        for major, n in quota.items():
            if n:
                parts.append(pool[pool["soc_major"] == major].sample(
                    n=int(n), random_state=int(rng.integers(1 << 31))))
    s = pd.concat(parts).sample(frac=1, random_state=int(rng.integers(1 << 31)))  # coding order
    s["item"] = np.arange(1, len(s) + 1)

    recode = []
    for cls, n in allocate(s.groupby("prior_class").size(), N_RECODE).items():
        recode += s[s["prior_class"] == cls].sample(
            n=int(n), random_state=int(rng.integers(1 << 31)))["Task ID"].tolist()
    s["recode"] = s["Task ID"].isin(recode)
    return s


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--onet", required=True)
    ap.add_argument("--form", required=True)
    ap.add_argument("--key", required=True)
    a = ap.parse_args()

    t = prior_class(a.onet)
    s = draw(t, np.random.default_rng(SEED))

    os.makedirs(os.path.dirname(a.key), exist_ok=True)
    s[["item", "Task ID", "O*NET-SOC Code", "Title", "Task Type", "soc_major",
       "gwa", "prior", "prior_class", "recode"]].to_csv(a.key, index=False)

    from form import write_form  # local module next to this script
    write_form(s, a.form)
    print(f"{len(s)} tasks ({s['prior_class'].value_counts().to_dict()}), "
          f"{int(s['recode'].sum())} flagged for re-coding -> {a.form}")


if __name__ == "__main__":
    main()
