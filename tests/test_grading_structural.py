"""Tests for itea.grading.structural on a synthetic O*NET content-model extract."""
import os

import pandas as pd
import pytest

from itea.grading.structural import gwa_scores, task_prior, within_share

EXTERNAL = os.environ.get("ITEA_EXTERNAL", os.path.join(os.path.dirname(__file__), "..", "data", "external"))
ONET = os.path.join(EXTERNAL, "db_30_2_text")


def _tsv(path, cols, rows):
    pd.DataFrame(rows, columns=cols).to_csv(path, sep="\t", index=False)


@pytest.fixture
def onet(tmp_path):
    ab = ["Abilities Element ID", "Abilities Element Name", "Work Activities Element ID", "Work Activities Element Name"]
    _tsv(tmp_path / "Abilities to Work Activities.txt", ab, [
        ["1.A.1.a.1", "Oral Comprehension", "G1", "Analyzing"],
        ["1.A.1.c.1", "Mathematical Reasoning", "G1", "Analyzing"],
        ["1.A.1.a.1", "Oral Comprehension", "G2", "Caring"],
        ["1.A.4.a.1", "Near Vision", "G2", "Caring"],
        ["1.A.3.a.1", "Static Strength", "G3", "Lifting"],
    ])
    sk = ["Skills Element ID", "Skills Element Name", "Work Activities Element ID", "Work Activities Element Name"]
    _tsv(tmp_path / "Skills to Work Activities.txt", sk, [
        ["2.A.1.a", "Reading Comprehension", "G1", "Analyzing"],
        ["2.B.1.a", "Social Perceptiveness", "G2", "Caring"],
        ["2.A.1.b", "Active Listening", "G2", "Caring"],
    ])
    _tsv(tmp_path / "DWA Reference.txt", ["Element ID", "IWA ID", "DWA ID", "DWA Title"], [
        ["G1", "I1", "D1", "Analyze data"], ["G2", "I2", "D2", "Care for patients"],
        ["G3", "I3", "D3", "Lift objects"]])
    _tsv(tmp_path / "Tasks to DWAs.txt", ["O*NET-SOC Code", "Task ID", "DWA ID", "DWA Title", "Date", "Domain Source"], [
        ["11-0000.00", "1", "D1", "", "", ""], ["11-0000.00", "2", "D1", "", "", ""],
        ["11-0000.00", "2", "D3", "", "", ""], ["29-0000.00", "3", "D2", "", "", ""]])
    return str(tmp_path)


def test_gwa_scores_formula(onet):
    g = gwa_scores(onet).set_index("gwa")
    assert g.loc["G1", "K_GWA"] == 1.0                         # all cognitive, no social skill
    assert g.loc["G2", "K_GWA"] == pytest.approx(0.5 * 0.5)    # half cognitive, half social
    assert g.loc["G3", "K_GWA"] == 0.0 and g.loc["G3", "n_skills"] == 0
    assert g.loc["G1", "E_GWA"] == 1.0 and g.loc["G2", "E_GWA"] == 0.5


def test_social_weight_zero_gives_cognitive_share(onet):
    g = gwa_scores(onet, social_weight=0.0).set_index("gwa")
    assert g.loc["G2", "K_GWA"] == g.loc["G2", "cognitive_share"]


def test_task_prior_averages_over_dwas(onet):
    t = task_prior(onet).set_index("TaskID")
    assert t.loc["1", "K1"] == 1.0
    assert t.loc["2", "K1"] == 0.5 and t.loc["2", "n_gwa"] == 2   # analyzing + lifting
    assert t.loc["3", "soc6"] == "29-0000"


def test_within_share():
    v = pd.Series([0.0, 1.0, 5.0, 5.0])
    g = pd.Series(["a", "a", "b", "b"])
    assert 0 < within_share(v, g) < 0.1
    assert within_share(pd.Series([1.0, 1.0]), pd.Series(["a", "b"])) == 0.0


@pytest.mark.skipif(not os.path.isdir(ONET), reason="O*NET not fetched (run `itea fetch`)")
def test_real_onet_extremes():
    g = gwa_scores(ONET).set_index("gwa")
    assert len(g) == 41
    assert g.loc["4.A.2.a.4", "K_GWA"] == 1.0          # Analyzing Data or Information
    assert g.loc["4.A.3.a.2", "K_GWA"] == 0.0          # Handling and Moving Objects
    t = task_prior(ONET)
    assert t["TaskID"].nunique() == 18796 and t["K1"].between(0, 1).all()
