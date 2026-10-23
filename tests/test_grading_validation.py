"""Tests for itea.grading.validation (agreement statistics and reference loaders)."""
import os

import numpy as np
import pandas as pd
import pytest

from itea.grading.validation import (bootstrap_corr, eloundou_labels, task_content_indices,
                                     weighted_kappa)

EXTERNAL = os.environ.get("ITEA_EXTERNAL", os.path.join(os.path.dirname(__file__), "..", "data", "external"))
ONET = os.path.join(EXTERNAL, "db_30_2_text")
ELOUNDOU = os.path.join(EXTERNAL, "eloundou_full_labelset.tsv")
CATS = ["low", "medium", "high"]


def test_weighted_kappa_bounds():
    a = ["low", "medium", "high", "high"]
    assert weighted_kappa(a, a, CATS) == pytest.approx(1.0)
    # adjacent disagreements are penalised less than extreme ones
    near = weighted_kappa(["low", "low", "high", "high"], ["low", "medium", "high", "medium"], CATS)
    far = weighted_kappa(["low", "low", "high", "high"], ["low", "high", "high", "low"], CATS)
    assert far < near < 1


def test_bootstrap_corr_resamples_clusters():
    rng = np.random.default_rng(0)
    df = pd.DataFrame({"SOC": np.repeat([f"o{i}" for i in range(30)], 5)})
    df["x"] = rng.normal(size=len(df))
    df["y"] = df["x"] + rng.normal(scale=0.3, size=len(df))
    r = bootstrap_corr(df, "x", "y", n_boot=200)
    assert r["clusters"] == 30 and r["n"] == 150
    assert r["ci95"][0] < r["r"] < r["ci95"][1] and r["r"] > 0.8


def test_eloundou_loader(tmp_path):
    p = tmp_path / "labels.tsv"
    pd.DataFrame({"O*NET-SOC Code": ["11-1011.00", "11-1011.00"], "Task ID": [8823.0, 8831.0],
                  "human_exposure_agg": ["E1", "E2"]}).to_csv(p, sep="\t")
    d = eloundou_labels(str(p))
    assert d["TaskID"].tolist() == ["8823", "8831"]          # float IDs cast to strings of ints
    assert d["human_beta"].tolist() == [1.0, 0.5]


@pytest.mark.skipif(not os.path.isdir(ONET), reason="O*NET not fetched (run `itea fetch`)")
def test_task_content_indices_real():
    t = task_content_indices(ONET)
    assert {"routine_cognitive", "nonroutine_analytical", "job_zone"} <= set(t.columns)
    assert t["routine_cognitive"].notna().sum() > 800
    assert abs(t["routine_cognitive"].mean()) < 1e-9          # standardised components


@pytest.mark.skipif(not os.path.exists(ELOUNDOU), reason="Eloundou labels not fetched")
def test_eloundou_real_overlap():
    d = eloundou_labels(ELOUNDOU)
    assert len(d) > 19000 and set(d["human_label"]) == {"E0", "E1", "E2"}
