#!/usr/bin/env python3
"""
First validation of the structural layer of itea.grading against the
pre-registered hypotheses in docs/grading/HIPOTESIS_PREREGISTRADAS_ES.md.

Usage:
    python scripts/grading/validate_structural.py --external data/external --out v4.0/outputs/grading
"""

import argparse
import json
import os

import pandas as pd

from itea.grading.structural import gwa_scores, task_links, task_prior, within_share
from itea.grading.validation import bootstrap_corr, eloundou_labels, task_content_indices


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--external", default="data/external")
    ap.add_argument("--out", default="v4.0/outputs/grading")
    a = ap.parse_args()
    onet = os.path.join(a.external, "db_30_2_text")
    os.makedirs(a.out, exist_ok=True)

    g = gwa_scores(onet)
    t = task_prior(onet)
    g.round(4).to_csv(os.path.join(a.out, "gwa_scores.csv"), index=False)
    t.round(4).to_csv(os.path.join(a.out, "task_prior_structural.csv"), index=False)

    # H1: task level, E1 vs Eloundou human labels
    el = eloundou_labels(os.path.join(a.external, "eloundou_full_labelset.tsv"))
    te = t.merge(el, on=["SOC", "TaskID"], how="inner")
    h1 = bootstrap_corr(te, "E1", "human_beta")
    h1_k = bootstrap_corr(te, "K1", "human_beta")   # reported, not a hypothesis

    # H2–H4: occupation level
    occ = t.groupby("SOC")[["K1", "E1"]].mean().reset_index()
    oi = occ.merge(task_content_indices(onet), on="SOC", how="inner")
    oi["one"] = oi["SOC"]  # each occupation is its own cluster
    h2 = bootstrap_corr(oi, "K1", "nonroutine_analytical", cluster="one")
    h3 = bootstrap_corr(oi, "K1", "routine_cognitive", cluster="one")
    h4 = bootstrap_corr(oi, "K1", "job_zone", cluster="one")
    e_nra = bootstrap_corr(oi, "E1", "nonroutine_analytical", cluster="one")

    # H5: share of K1 variance within GWA (tasks assigned to their first GWA)
    first_gwa = task_links(onet).dropna(subset=["gwa"]).sort_values("gwa").drop_duplicates(["SOC", "TaskID"])
    tg = t.merge(first_gwa[["SOC", "TaskID", "gwa"]], on=["SOC", "TaskID"])
    h5 = within_share(tg["K1"], tg["gwa"])

    res = {
        "H1_E1_vs_eloundou_human_beta": h1, "K1_vs_eloundou_human_beta": h1_k,
        "H2_K1_vs_nonroutine_analytical": h2, "H3_K1_vs_routine_cognitive": h3,
        "H4_K1_vs_job_zone": h4, "E1_vs_nonroutine_analytical": e_nra,
        "H5_K1_within_gwa_variance_share": h5,
        "n_tasks": int(t["TaskID"].nunique()), "n_tasks_with_eloundou": int(len(te)),
        "n_occupations": int(len(oi)), "distinct_K1_values": int(t["K1"].round(6).nunique()),
    }
    with open(os.path.join(a.out, "validation_structural.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    for k, v in res.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
