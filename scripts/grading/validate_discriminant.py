#!/usr/bin/env python3
"""
Discriminant validation of the structural layer (issue #3) against the
hypotheses H6–H8 pre-registered in docs/grading/HIPOTESIS_PREREGISTRADAS_ES.md.

Usage:
    python scripts/grading/validate_discriminant.py --external data/external --out v4.0/outputs/grading
"""

import argparse
import json
import os

from itea.grading.structural import task_prior
from itea.grading.validation import (bootstrap_corr, bootstrap_partial_corr,
                                     eloundou_labels, task_content_indices)

NON_MANUAL = {f"{m:02d}" for m in list(range(11, 30)) + [41, 43]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--external", default="data/external")
    ap.add_argument("--out", default="v4.0/outputs/grading")
    a = ap.parse_args()
    onet = os.path.join(a.external, "db_30_2_text")
    os.makedirs(a.out, exist_ok=True)

    t = task_prior(onet)
    ci = task_content_indices(onet)
    occ = t.groupby("SOC")[["K1", "E1"]].mean().reset_index().merge(ci, on="SOC", how="inner")
    occ["one"] = occ["SOC"]

    # H6: K1 vs non-routine analytical, net of Job Zone and within each Job Zone
    h6 = bootstrap_partial_corr(occ, "K1", "nonroutine_analytical", by="job_zone", cluster="one")
    h6_by = {int(z): bootstrap_corr(g, "K1", "nonroutine_analytical", cluster="one")
             for z, g in occ.dropna(subset=["job_zone"]).groupby("job_zone")}

    # H7: K1 vs routine cognitive in non-manual occupations
    nm = occ[occ["SOC"].str[:2].isin(NON_MANUAL)]
    h7 = bootstrap_corr(nm, "K1", "routine_cognitive", cluster="one")

    # H8: incremental validity of K1 for Eloundou human exposure, net of Job Zone
    el = eloundou_labels(os.path.join(a.external, "eloundou_full_labelset.tsv"))
    te = t.merge(el, on=["SOC", "TaskID"]).merge(ci[["SOC", "job_zone"]], on="SOC")
    h8 = bootstrap_partial_corr(te, "K1", "human_beta", by="job_zone")
    e_h8 = bootstrap_partial_corr(te, "E1", "human_beta", by="job_zone")  # reported, not a hypothesis

    res = {
        "H6_K1_vs_nonroutine_analytical_net_of_job_zone": h6,
        "H6_by_job_zone": h6_by,
        "H6_positive_job_zones": int(sum(v["r"] > 0 for v in h6_by.values())),
        "H7_K1_vs_routine_cognitive_non_manual": h7,
        "H8_K1_vs_eloundou_net_of_job_zone": h8,
        "E1_vs_eloundou_net_of_job_zone": e_h8,
    }
    with open(os.path.join(a.out, "validation_discriminant.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
