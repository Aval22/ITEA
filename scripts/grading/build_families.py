#!/usr/bin/env python3
"""
Build layer F (ITEA 4.2): AI-family and task-type vectors for every O*NET 30.2 task,
Eurostat adoption by AI family, and the alienable surface by family (H22, descriptive).

Run only after the criteria book and hypotheses H21–H25 are committed (decision D29):

    .venv/bin/python scripts/grading/build_families.py --external data/external \
        --grades v4.0/outputs/grading/task_grades_v41.csv --out v4.0/outputs/grading

Outputs: task_families_v42.csv, eurostat_ai_families.csv, surface_by_family_v42.json.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os

import numpy as np
import pandas as pd

from itea.grading.families import (FAM, TYPES, adoption_by_family, attach, perturb_rules,
                                   surface_by_family, task_gwa_links, task_vectors)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--external", required=True)
    ap.add_argument("--grades", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tau-k", type=float, default=None, help="K threshold (default: median of K)")
    ap.add_argument("--tau-e", type=float, default=None, help="E threshold (default: central, 0.6198)")
    ap.add_argument("--draws", type=int, default=1000)
    ap.add_argument("--no-eurostat", action="store_true")
    a = ap.parse_args()

    onet = os.path.join(a.external, "db_30_2_text")
    links = task_gwa_links(onet)
    vec = task_vectors(links)
    grades = pd.read_csv(a.grades, dtype={"TaskID": str})
    t = attach(grades, vec)

    # task importance (IM), normalised within occupation; no employment weights here
    tr = pd.read_csv(os.path.join(onet, "Task Ratings.txt"), sep="\t", dtype={"Task ID": str})
    im = tr[tr["Scale ID"] == "IM"].rename(columns={"O*NET-SOC Code": "SOC", "Task ID": "TaskID", "Data Value": "IM"})
    t = t.merge(im[["SOC", "TaskID", "IM"]], on=["SOC", "TaskID"], how="left")
    t["w"] = t.IM.fillna(t.groupby("SOC").IM.transform("mean")).fillna(1.0)
    t["w"] = t.w / t.groupby("SOC").w.transform("sum")

    tau_k = a.tau_k if a.tau_k is not None else float(t.K.quantile(0.5))
    tau_e = a.tau_e if a.tau_e is not None else 0.6198
    t["in_play"] = ((t.K >= tau_k) & (t.E >= tau_e)).astype(int)

    os.makedirs(a.out, exist_ok=True)
    t[["SOC", "TaskID", "K", "E", "in_play", "imputed", "n_dwa", *FAM, *TYPES]].to_csv(
        os.path.join(a.out, "task_families_v42.csv"), index=False)

    central = surface_by_family(t, t.in_play, t.w)
    rng = np.random.default_rng(42)
    draws = []
    for _ in range(a.draws):
        v = task_vectors(links, perturb_rules(rng))
        tt = attach(grades, v).merge(t[["SOC", "TaskID", "w", "in_play"]], on=["SOC", "TaskID"])
        draws.append(surface_by_family(tt, tt.in_play, tt.w))
    band = pd.DataFrame(draws).quantile([0.05, 0.95])

    res = {"built": datetime.date.today().isoformat(), "tau_k": tau_k, "tau_e": tau_e,
           "n_tasks": int(len(t)), "n_imputed": int(t.imputed.sum()), "n_in_play": int(t.in_play.sum()),
           "weights": "task importance within occupation (occupations equally weighted)",
           "surface_by_family": central.round(4).to_dict(),
           "band_5_95": {f: [round(band.loc[0.05, f], 4), round(band.loc[0.95, f], 4)] for f in FAM},
           "H22_F1_plus_F2": round(float(central["F1"] + central["F2"]), 4)}
    if not a.no_eurostat:
        ad = adoption_by_family()
        ad.to_csv(os.path.join(a.out, "eurostat_ai_families.csv"), index=False)
        res["eurostat_rows"] = int(len(ad))
    with open(os.path.join(a.out, "surface_by_family_v42.json"), "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
