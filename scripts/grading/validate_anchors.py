#!/usr/bin/env python3
"""
Validation of grading layer 3 against hypotheses H14–H17, registered in
docs/grading/HIPOTESIS_PREREGISTRADAS_ES.md before the layer was computed.

Usage:
    python scripts/grading/validate_anchors.py --external data/external --out v4.0/outputs/grading
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
    a = ap.parse_args()
    onet = os.path.join(a.external, "db_30_2_text")
    key = ["SOC", "TaskID"]

    t = (pd.read_csv(os.path.join(a.out, "task_prior_structural.csv"), dtype={"TaskID": str})
         .merge(pd.read_csv(os.path.join(a.out, "task_semantic_B.csv"), dtype={"TaskID": str})[key + ["K2", "E2"]], on=key)
         .merge(pd.read_csv(os.path.join(a.out, "task_anchors.csv"), dtype={"TaskID": str})[key + ["K3", "E3"]], on=key))
    t["E123"] = t[["E1", "E2", "E3"]].rank(pct=True).mean(axis=1)

    ci = task_content_indices(onet)
    el = eloundou_labels(os.path.join(a.external, "eloundou_full_labelset.tsv"))
    te = t.merge(el, on=key).merge(ci[["SOC", "job_zone"]], on="SOC")
    first_gwa = task_links(onet).dropna(subset=["gwa"]).sort_values("gwa").drop_duplicates(key)
    tg = t.merge(first_gwa[key + ["gwa"]], on=key)
    occ = t.groupby("SOC")[["K1", "K2", "K3"]].mean().reset_index().merge(ci, on="SOC")
    occ["one"] = occ["SOC"]

    res = {
        "H14_E3_vs_eloundou": bootstrap_corr(te, "E3", "human_beta"),
        "H15_E123_vs_eloundou": bootstrap_corr(te, "E123", "human_beta"),
        "H16_K3_vs_nonroutine_analytical_net_of_job_zone": bootstrap_partial_corr(
            occ, "K3", "nonroutine_analytical", by="job_zone", cluster="one"),
        "H17_K3_vs_eloundou_net_of_job_zone": bootstrap_partial_corr(te, "K3", "human_beta", by="job_zone"),
        # reported without a hypothesis
        "K3_within_gwa_variance_share": within_share(tg["K3"], tg["gwa"]),
        "K3_vs_job_zone": bootstrap_corr(occ, "K3", "job_zone", cluster="one"),
        "K3_vs_K1_task": float(t["K3"].corr(t["K1"], method="spearman")),
        "K3_vs_K2_task": float(t["K3"].corr(t["K2"], method="spearman")),
        "E3_vs_E1_task": float(t["E3"].corr(t["E1"], method="spearman")),
        "E3_sd": float(t["E3"].std()), "K3_sd": float(t["K3"].std()),
        "n_tasks": int(len(t)), "n_tasks_with_eloundou": int(len(te)),
    }
    with open(os.path.join(a.out, "validation_anchors.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
