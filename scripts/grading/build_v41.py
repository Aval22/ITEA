#!/usr/bin/env python3
"""
ITEA v4.1: composite task grades (layer 5), OAXI-EU v4.1 and its Monte Carlo
uncertainty, with the hypotheses H18–H20 registered in
docs/grading/HIPOTESIS_PREREGISTRADAS_ES.md.

Components enter only if they passed their registered hypotheses; the rule is
applied here from the validation files, not chosen by hand.

Usage:
    python scripts/grading/build_v41.py --external data/external --out v4.0/outputs/grading [--draws 1000]
"""

import argparse
import datetime
import json
import os

import numpy as np
import pandas as pd

import itea
from itea.axi import load_onet
from itea.crosswalk import build_crosswalk
from itea.fetch import SOURCES
from itea.grading.combine import composite, draw_spec, eta_squared, normalise
from itea.grading.rebuild import compare
from itea.grading.validation import bootstrap_corr, bootstrap_partial_corr, eloundou_labels, task_content_indices
from itea.oaxi_eu import KAPPA, convergence, oaxi_eu
from itea.rollup import to_activities, to_occupations

SEED = 20261023


def passed(v: dict, floor: float = 0.0) -> bool:
    return v["r"] > floor and v["ci95"][0] > 0


def components(out: str) -> tuple[list, list, dict]:
    """K and E components that passed their registered hypotheses."""
    k, e, why = ["K1", "K2"], ["E1", "E2"], {"K1": "H2,H6,H8", "K2": "H11B,H12B,H13B", "E1": "H1", "E2": "H9B,H10B"}
    path = os.path.join(out, "validation_anchors.json")
    if os.path.exists(path):
        v = json.load(open(path))
        if passed(v["H16_K3_vs_nonroutine_analytical_net_of_job_zone"]) and passed(v["H17_K3_vs_eloundou_net_of_job_zone"], 0.10):
            k.append("K3"); why["K3"] = "H16,H17"
        if passed(v["H14_E3_vs_eloundou"]) and v["H15_E123_vs_eloundou"]["r"] > 0.476:
            e.append("E3"); why["E3"] = "H14,H15"
    return k, e, why


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--external", default="data/external")
    ap.add_argument("--out", default="v4.0/outputs/grading")
    ap.add_argument("--legacy", default="v4.0/outputs/oaxi_eu.csv")
    ap.add_argument("--draws", type=int, default=1000)
    a = ap.parse_args()
    onet = os.path.join(a.external, "db_30_2_text")
    key = ["SOC", "TaskID"]

    t = (pd.read_csv(os.path.join(a.out, "task_prior_structural.csv"), dtype={"TaskID": str})
         .merge(pd.read_csv(os.path.join(a.out, "task_semantic_B.csv"), dtype={"TaskID": str})[key + ["K2", "E2"]], on=key))
    anchors = os.path.join(a.out, "task_anchors.csv")
    if os.path.exists(anchors):
        t = t.merge(pd.read_csv(anchors, dtype={"TaskID": str})[key + ["K3", "E3"]], on=key)
    k_cols, e_cols, why = components(a.out)

    # central task grades
    t["K"] = composite(t, k_cols)
    t["E"] = composite(t, e_cols)
    t[key + ["K", "E"] + k_cols + e_cols].round(4).to_csv(os.path.join(a.out, "task_grades_v41.csv"), index=False)

    # occupation-level means of every normalised component (the roll-up is linear,
    # so a weighted composite of these means equals the roll-up of the composite)
    _, t2d = load_onet(onet)
    occ_means = {}
    for how in ("rank", "minmax"):
        n = pd.concat([t[key], normalise(t, k_cols + e_cols, how)], axis=1)
        occ_means[how] = to_occupations(to_activities(n, t2d, k_cols + e_cols), t2d, k_cols + e_cols)
    cw = build_crosswalk(os.path.join(a.external, SOURCES["isco_soc"]["file"]),
                         os.path.join(a.external, SOURCES["soc_2010_2018"]["file"]))

    def index(spec) -> pd.DataFrame:
        o = occ_means[spec["how"]]
        occ = o[["SOC", "soc6"]].assign(
            K=(o[spec["k_cols"]] * spec["k_w"]).sum(axis=1) / sum(spec["k_w"]),
            E=(o[spec["e_cols"]] * spec["e_w"]).sum(axis=1) / sum(spec["e_w"]))
        return oaxi_eu(occ, cw, kappa=spec["kappa"], exposure="E", codifiability="K")

    central = {"k_cols": k_cols, "k_w": np.ones(len(k_cols)), "e_cols": e_cols, "e_w": np.ones(len(e_cols)),
               "how": "rank", "kappa": KAPPA}
    idx = index(central)

    rng = np.random.default_rng(SEED)
    draws, specs = [], []
    for i in range(a.draws):
        s = draw_spec(rng, k_cols, e_cols)
        d = index(s)[["isco", "OAXI_EU"]]
        d["rank"] = d["OAXI_EU"].rank(ascending=False)
        draws.append(d.assign(draw=i))
        specs.append({"draw": i, "how": s["how"], "kappa": s["kappa"],
                      "k_set": "+".join(s["k_cols"]), "e_set": "+".join(s["e_cols"]),
                      "k_w_first": float(s["k_w"][0]), "e_w_first": float(s["e_w"][0])})
    mc = pd.concat(draws)
    q = mc.groupby("isco").agg(OAXI_p5=("OAXI_EU", lambda x: x.quantile(.05)), OAXI_median=("OAXI_EU", "median"),
                               OAXI_p95=("OAXI_EU", lambda x: x.quantile(.95)),
                               rank_p5=("rank", lambda x: x.quantile(.05)), rank_median=("rank", "median"),
                               rank_p95=("rank", lambda x: x.quantile(.95)))
    idx = idx.merge(q.reset_index(), on="isco", how="left")
    idx["rank"] = idx["OAXI_EU"].rank(ascending=False)
    idx.round(4).to_csv(os.path.join(a.out, "oaxi_eu_v41.csv"), index=False)

    # sensitivity of each ISCO group's rank to each method choice (first order), averaged
    sp = pd.DataFrame(specs)
    m = mc.merge(sp, on="draw")
    sens = {}
    for f in ["how", "kappa", "k_set", "e_set", "k_w_first", "e_w_first"]:
        sens[f] = float(np.nanmean([eta_squared(g[f], g["rank"]) for _, g in m.groupby("isco") if g["rank"].std() > 0]))

    # registered hypotheses H18–H20
    ci = task_content_indices(onet)
    el = eloundou_labels(os.path.join(a.external, "eloundou_full_labelset.tsv"))
    te = t.merge(el, on=key)
    occ = t.groupby("SOC")[["K"]].mean().reset_index().merge(ci, on="SOC")
    occ["one"] = occ["SOC"]
    h18 = bootstrap_corr(te, "E", "human_beta")
    h19 = bootstrap_partial_corr(occ, "K", "nonroutine_analytical", by="job_zone", cluster="one")
    band = (idx["rank_p95"] - idx["rank_p5"]).median()
    legacy = pd.read_csv(a.legacy, dtype={"isco": str, "isco3": str})

    meta = {
        "index": "OAXI-EU", "version": "4.1 (built from itea.grading)", "built": datetime.date.today().isoformat(),
        "components": {"K": k_cols, "E": e_cols, "entered_because": why}, "kappa": KAPPA,
        "n_tasks": int(len(t)), "n_isco": int(len(idx)), "monte_carlo": {"draws": a.draws, "seed": SEED},
        "H18_E_vs_eloundou": h18, "H18_supported": h18["r"] > 0.40,
        "H19_K_vs_nonroutine_analytical_net_of_job_zone": h19, "H19_supported": passed(h19),
        "H20_median_rank_band_5_95": float(band), "H20_supported": bool(band < 100),
        "sensitivity_eta2_rank": sens,
        "convergence_jrc145832_not_independent": convergence(idx, itea.jrc_benchmark()),
        "agreement_with_v40_axi": compare(idx, legacy),
    }
    json.dump(meta, open(os.path.join(a.out, "oaxi_eu_v41.meta.json"), "w"), indent=2)
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
