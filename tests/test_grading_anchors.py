"""Grading layer 3 (itea.grading.anchors): probabilities and scores from entailment logits."""
import numpy as np
import pandas as pd

from itea.grading.anchors import ANCHORS, grade


def test_grade_softmax_within_groups():
    logits = pd.DataFrame([[5, 0, 0, 0, 0], [0, 0, 5, -3, 3]], columns=list(ANCHORS))
    g = grade(logits)
    assert np.allclose(g[["p_e1", "p_e2", "p_e0"]].sum(axis=1), 1)
    assert np.allclose(g[["p_k1", "p_k0"]].sum(axis=1), 1)
    assert g.loc[0, "E3"] > 0.95 and g.loc[1, "E3"] < 0.05     # e1 wins / e0 wins
    assert g.loc[0, "K3"] == 0.5 and g.loc[1, "K3"] < 0.01      # tie / k0 wins
