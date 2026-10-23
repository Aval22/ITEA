import numpy as np
import pandas as pd

from itea.grading.validation import bootstrap_partial_corr


def test_partial_corr_removes_group_effect():
    # x and y both depend only on the group: their partial correlation is ~0
    rng = np.random.default_rng(0)
    g = np.repeat([1, 2, 3, 4], 100)
    d = pd.DataFrame({"g": g, "x": g + rng.normal(0, 0.1, 400), "y": g + rng.normal(0, 0.1, 400),
                      "c": np.arange(400)})
    assert abs(d["x"].corr(d["y"], method="spearman")) > 0.9
    r = bootstrap_partial_corr(d, "x", "y", by="g", cluster="c", n_boot=50)
    assert abs(r["r"]) < 0.2


def test_partial_corr_keeps_within_group_signal():
    rng = np.random.default_rng(1)
    g = np.repeat([1, 2], 200)
    x = rng.normal(size=400)
    d = pd.DataFrame({"g": g, "x": x + 5 * g, "y": x + rng.normal(0, 0.3, 400), "c": np.arange(400)})
    r = bootstrap_partial_corr(d, "x", "y", by="g", cluster="c", n_boot=50)
    assert r["r"] > 0.8 and r["ci95"][0] > 0.7
