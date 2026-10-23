"""Grading layer 5 (itea.grading.combine)."""
import numpy as np
import pandas as pd

from itea.grading.combine import composite, draw_spec, eta_squared


def test_composite_equal_and_weighted():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]})
    assert np.allclose(composite(df, ["a", "b"]), 2 / 3)               # opposite ranks cancel
    assert composite(df, ["a", "b"], weights=[1, 0]).tolist() == df["a"].rank(pct=True).tolist()
    assert composite(df, ["a"], how="minmax").tolist() == [0.0, 0.5, 1.0]


def test_draw_spec_keeps_one_component():
    rng = np.random.default_rng(0)
    for _ in range(200):
        s = draw_spec(rng, ["K1", "K2"], ["E1"])
        assert 1 <= len(s["k_cols"]) <= 2 and s["e_cols"] == ["E1"]
        assert abs(s["k_w"].sum() - 1) < 1e-9 and 0.30 <= s["kappa"] <= 0.50


def test_eta_squared():
    f = pd.Series(["x"] * 50 + ["y"] * 50)
    assert eta_squared(f, pd.Series([0.0] * 50 + [1.0] * 50)) == 1.0
    assert eta_squared(f, pd.Series([0.0, 1.0] * 50)) == 0.0
