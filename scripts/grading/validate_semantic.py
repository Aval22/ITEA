#!/usr/bin/env python3
"""
Validation of grading layer 2 against hypotheses H9–H13, registered in
docs/grading/HIPOTESIS_PREREGISTRADAS_ES.md before the layer was computed.

Usage:
    python scripts/grading/validate_semantic.py --external data/external --out v4.0/outputs/grading
"""

import argparse
import json
import os

import pandas as pd

from itea.grading.structural import task_links, within_share
from itea.grading.validation import (bootstrap_corr, bootstrap_partial_corr,
                                     eloundou_labels, task_content_indices)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--external", default="data/external")
    ap.add_argument("--out", default="v4.0/outputs/grading")
    ap.add_argument("--label", default="", help="variant suffix, e.g. _B")
    a = ap.parse_args()
    onet = os.path.join(a.external, "db_30_2_text")

    sem = pd.read_csv(os.path.join(a.out, f"task_semantic{a.label}.csv"), dtype={"TaskID": str})
    prior = pd.read_csv(os.path.join(a.out, "task_prior_structural.csv"), dtype={"TaskID": str})
    t = prior.merge(sem[["SOC", "TaskID", "K2", "E2", "n_links"]], on=["SOC", "TaskID"], how="left")
    t["E12"] = (t["E1"].rank(pct=True) + t["E2"].rank(pct=True)) / 2

    ci = task_content_indices(onet)
    el = eloundou_labels(os.path.join(a.external, "eloundou_full_labelset.tsv"))
    te = t.merge(el, on=["SOC", "TaskID"]).merge(ci[["SOC", "job_zone"]], on="SOC")

    first_gwa = task_links(onet).dropna(subset=["gwa"]).sort_values("gwa").drop_duplicates(["SOC", "TaskID"])
    tg = t.merge(first_gwa[["SOC", "TaskID", "gwa"]], on=["SOC", "TaskID"]).dropna(subset=["K2"])

    occ = t.groupby("SOC")[["K1", "K2", "E1", "E2"]].mean().reset_index().merge(ci, on="SOC")
    occ["one"] = occ["SOC"]

    res = {
        "H9_E2_vs_eloundou": bootstrap_corr(te, "E2", "human_beta"),
        "H10_E12_vs_eloundou": bootstrap_corr(te, "E12", "human_beta"),
        "H11_K2_within_gwa_variance_share": within_share(tg["K2"], tg["gwa"]),
        "H12_K2_vs_nonroutine_analytical_net_of_job_zone": bootstrap_partial_corr(
            occ, "K2", "nonroutine_analytical", by="job_zone", cluster="one"),
        "H13_K2_vs_eloundou_net_of_job_zone": bootstrap_partial_corr(te, "K2", "human_beta", by="job_zone"),
        # reported without a hypothesis
        "K2_vs_job_zone": bootstrap_corr(occ, "K2", "job_zone", cluster="one"),
        "K2_vs_K1_task": float(t["K2"].corr(t["K1"], method="spearman")),
        "E2_vs_E1_task": float(t["E2"].corr(t["E1"], method="spearman")),
        "K1_within_gwa_variance_share": within_share(tg["K1"], tg["gwa"]),
        "n_tasks_graded": int(t["K2"].notna().sum()), "n_tasks_with_eloundou": int(te["E2"].notna().sum()),
    }
    with open(os.path.join(a.out, f"validation_semantic{a.label}.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
