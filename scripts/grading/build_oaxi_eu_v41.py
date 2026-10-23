#!/usr/bin/env python3
"""
Rebuild OAXI-EU from the itea.grading task grades (v4.1) and compare it with
the v4.0 index built on the legacy AXI grades.

Today the only finished grading layer is the structural one (K1, E1), so the
default output is labelled "layer1": a preview, not the v4.1 index. When the
combined grades exist, run it again with --grades and --label v41.

Usage:
    python scripts/grading/build_oaxi_eu_v41.py --external data/external \
        [--grades v4.0/outputs/grading/task_prior_structural.csv --k K1 --e E1 --label layer1]
"""

import argparse
import datetime
import hashlib
import json
import os

import pandas as pd

import itea
from itea.crosswalk import build_crosswalk
from itea.fetch import SOURCES
from itea.grading.rebuild import compare, oaxi_eu_from_grades
from itea.oaxi_eu import KAPPA, convergence


def sha(path: str) -> str:
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--external", default="data/external")
    ap.add_argument("--grades", default="v4.0/outputs/grading/task_prior_structural.csv")
    ap.add_argument("--k", default="K1")
    ap.add_argument("--e", default="E1")
    ap.add_argument("--label", default="layer1")
    ap.add_argument("--legacy", default="v4.0/outputs/oaxi_eu.csv")
    ap.add_argument("--out", default="v4.0/outputs/grading")
    a = ap.parse_args()

    onet = os.path.join(a.external, "db_30_2_text")
    cw = build_crosswalk(os.path.join(a.external, SOURCES["isco_soc"]["file"]),
                         os.path.join(a.external, SOURCES["soc_2010_2018"]["file"]))
    grades = pd.read_csv(a.grades, dtype={"TaskID": str})
    idx, occ = oaxi_eu_from_grades(grades, onet, cw, k=a.k, e=a.e)
    legacy = pd.read_csv(a.legacy, dtype={"isco": str, "isco3": str})

    os.makedirs(a.out, exist_ok=True)
    base = os.path.join(a.out, f"oaxi_eu_{a.label}")
    idx.round(4).to_csv(base + ".csv", index=False)
    occ.round(4).to_csv(os.path.join(a.out, f"occupation_scores_{a.label}.csv"), index=False)

    meta = {
        "index": "OAXI-EU", "grades": a.label, "itea_version": itea.__version__,
        "built": datetime.date.today().isoformat(), "kappa": KAPPA,
        "grade_columns": {"K": a.k, "E": a.e}, "n_tasks": int(len(grades)),
        "n_onet_soc": int(len(occ)), "n_isco": int(len(idx)),
        "inputs_sha256": {"grades": sha(a.grades)},
        "convergence_jrc145832": convergence(idx, itea.jrc_benchmark()),
        "agreement_with_v40_axi": compare(idx, legacy),
        "note": ("JRC145832 is ability-based, like the structural layer: its convergence is reported "
                 "for information and is not an independent validation of K (decision D17)."),
    }
    json.dump(meta, open(base + ".meta.json", "w"), indent=2)
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
