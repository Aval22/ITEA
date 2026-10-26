"""Tests for layer F (AI families and task types)."""
import os

import numpy as np
import pandas as pd
import pytest

from itea.grading.families import (FAM, GWA_FAMILY, TYPES, adoption_by_family, attach, gwa_matrix,
                                   perturb_rules, surface_by_family, task_gwa_links, task_type_of,
                                   task_vectors)

EXTERNAL = os.environ.get("ITEA_EXTERNAL", os.path.join(os.path.dirname(__file__), "..", "data", "external"))
ONET = os.path.join(EXTERNAL, "db_30_2_text")


def test_rules_sum_to_one_and_use_known_families():
    gm = gwa_matrix()
    assert np.allclose(gm.sum(axis=1), 1.0)
    assert len(gm) == 41
    assert all(set(w) <= set(FAM) for w in GWA_FAMILY.values())


def test_every_gwa_has_a_task_type():
    assert all(task_type_of(g) in TYPES for g in GWA_FAMILY)
    assert task_type_of("4.A.4.a.7") == "T_C" and task_type_of("4.A.3.a.4") == "T_E"


def test_task_vectors_average_over_dwas():
    links = pd.DataFrame({"O*NET-SOC Code": ["X", "X", "Y"], "Task ID": ["1", "1", "2"],
                          "GWA": ["4.A.2.b.5", "4.A.3.a.4", "4.A.2.b.2"]})   # scheduling + driving; creative
    v = task_vectors(links).set_index("Task ID")
    assert v.loc["1", "F6"] == pytest.approx(0.5) and v.loc["1", "F7"] == pytest.approx(0.5)
    assert v.loc["1", "T_B"] == pytest.approx(0.5) and v.loc["1", "T_E"] == pytest.approx(0.5)
    assert v.loc["2", "F2"] == pytest.approx(1.0) and v.loc["1", "n_dwa"] == 2
    assert np.allclose(v[FAM].sum(axis=1), 1.0) and np.allclose(v[TYPES].sum(axis=1), 1.0)


def test_unknown_gwa_raises():
    links = pd.DataFrame({"O*NET-SOC Code": ["X"], "Task ID": ["1"], "GWA": ["4.A.9.z.9"]})
    with pytest.raises(ValueError):
        task_vectors(links)


def test_attach_imputes_from_occupation_and_flags():
    links = pd.DataFrame({"O*NET-SOC Code": ["X"], "Task ID": ["1"], "GWA": ["4.A.2.b.2"]})
    grades = pd.DataFrame({"SOC": ["X", "X"], "TaskID": ["1", "2"], "K": [.5, .5], "E": [.5, .5]})
    g = attach(grades, task_vectors(links)).set_index("TaskID")
    assert not g.loc["1", "imputed"] and g.loc["2", "imputed"]
    assert g.loc["2", "F2"] == pytest.approx(1.0)


def test_surface_by_family_weights_only_tasks_in_play():
    t = pd.DataFrame({"F1": [1.0, 0.0], "F2": [0.0, 0.0], "F3": 0.0, "F4": 0.0, "F5": [0.0, 1.0],
                      "F6": 0.0, "F7": 0.0})
    s = surface_by_family(t, in_play=pd.Series([1, 0]), weight=pd.Series([2.0, 5.0]))
    assert s["F1"] == pytest.approx(1.0) and s["F5"] == pytest.approx(0.0)


def test_perturbed_rules_stay_normalised():
    p = perturb_rules(np.random.default_rng(0))
    assert all(abs(sum(w.values()) - 1) < 1e-9 for w in p.values())
    assert set(p) == set(GWA_FAMILY)


def test_adoption_by_family_maps_indicators():
    def fake_fetch(code, **f):
        return pd.DataFrame({"dataset": code, "geo": "ES", "nace_r2": "C", "indic_is": ["E_AI_TNLG", "E_AI_TANY"],
                             "time": "2025", "value": [8.9, 20.3], "retrieved": "2026-10-26"})
    a = adoption_by_family(fetch=fake_fetch)
    assert a.family.tolist() == ["F2"]


@pytest.mark.skipif(not os.path.isdir(ONET), reason="O*NET not fetched (run `itea fetch`)")
def test_rules_cover_all_onet_gwas():
    links = task_gwa_links(ONET)
    v = task_vectors(links)                       # raises if a GWA has no rule
    assert np.allclose(v[FAM].sum(axis=1), 1.0)
