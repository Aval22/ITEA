"""Tests for the generic roll-up, crosswalk reweighting and the packaged datasets."""
import pandas as pd
import pytest

from itea.crosswalk import reweight
from itea.datasets import axi_path, jrc_benchmark
from itea.axi import load_axi
from itea.rollup import to_activities, to_isco, to_occupations


@pytest.fixture
def links():
    return pd.DataFrame({"SOC": ["A.00", "A.00", "B.00", "C.00"],
                         "TaskID": ["t1", "t2", "t3", "t4"],
                         "DWA_ID": ["D1", "D2", "D1", "D3"]})


def test_generic_rollup_with_continuous_scores(links):
    # e.g. an LLM-exposure rating per O*NET task
    scores = pd.DataFrame({"TaskID": ["t1", "t2", "t3"], "beta": [1.0, 0.0, 0.5]})
    act = to_activities(scores, links, ["beta"]).set_index("DWA_ID")
    assert act.loc["D1", "beta"] == 0.75 and act.loc["D1", "n_tasks"] == 2
    occ = to_occupations(act.reset_index(), links, ["beta"]).set_index("SOC")
    assert occ.loc["A.00", "beta"] == pytest.approx((0.75 + 0.0) / 2)
    assert occ.loc["B.00", "beta"] == 0.75
    assert "C.00" not in occ.index               # its only activity has no score


def test_to_isco_weighted_mean():
    occ = pd.DataFrame({"SOC": ["X.00", "Y.00"], "soc6": ["X", "Y"], "v": [0.0, 1.0]})
    cw = pd.DataFrame({"soc2018": ["X", "Y", "Y"], "isco": ["1111", "1111", "2222"], "w": [1.0, 0.25, 0.75]})
    g = to_isco(occ, cw, ["v"]).set_index("isco")
    assert g.loc["1111", "v"] == pytest.approx(0.25 / 1.25)
    assert g.loc["2222", "v"] == 1.0 and g.loc["1111", "n_soc"] == 2


def test_reweight_by_employment():
    cw = pd.DataFrame({"soc2018": ["S", "S", "T", "T"], "isco": ["1111", "2222", "3333", "4444"]})
    eq = reweight(cw)
    assert eq["w"].tolist() == [0.5, 0.5, 0.5, 0.5]
    emp = pd.Series({"1111": 300.0, "2222": 100.0})          # T's groups are absent
    w = reweight(cw, emp).set_index("isco")["w"]
    assert w["1111"] == 0.75 and w["2222"] == 0.25
    assert w["3333"] == 0.5 and w["4444"] == 0.5             # falls back to equal split


def test_packaged_axi_grades():
    axi = load_axi(axi_path())
    assert len(axi) == 47810 and axi["SOC_CODE"].nunique() == 923
    # LOW automation and LOW_TRANS codifiability are linked by design (README_AXI.md)
    assert ((axi["Auto_Grade"] == "LOW") == (axi["CI_Grade"] == "LOW_TRANS")).all()


def test_packaged_jrc_benchmark():
    j = jrc_benchmark()
    assert len(j) == 127 and j["isco3"].is_unique
    assert j["isco3"].str.fullmatch(r"\d{3}").all()
    assert j["score"].between(0, 1).all() and j["score"].max() == 1.0
