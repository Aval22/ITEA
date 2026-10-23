"""Tests for the AXI task -> activity -> occupation roll-up (synthetic O*NET tables)."""
import pandas as pd
import pytest

from itea.axi import activity_shares, load_axi, match_tasks, normalise_text, occupation_shares


@pytest.fixture
def onet():
    ts = pd.DataFrame({
        "SOC": ["11-1011.00", "11-1011.00", "13-1111.00", "15-1252.00"],
        "TaskID": ["1", "2", "3", "4"],
        "Task": ["Direct the budget.", "Negotiate contracts!", "Analyse data", "Write code"],
    })
    t2d = pd.DataFrame({
        "SOC": ["11-1011.00", "11-1011.00", "13-1111.00", "15-1252.00", "15-1252.00"],
        "TaskID": ["1", "2", "3", "4", "4"],
        "DWA_ID": ["D1", "D2", "D1", "D3", "D1"],
    })
    return ts, t2d


@pytest.fixture
def axi():
    return pd.DataFrame({
        "SOC_CODE": ["11-1011.00", "11-1011.00", "13-1111.00", "99-0000.00"],
        "Task_Description": ["direct the  budget", "Negotiate contracts", "Analyse data", "No match"],
        "Auto_Grade": ["TRANS", "HIGH", "TRANS", "LOW"],
        "CI_Grade": ["HIGH_ALGO", "MEDIUM_SC", "HIGH_ALGO", "LOW_TRANS"],
        "GenAI_Impact": ["High", "Low", "Medium", "High"],
        "Agentic_Impact": ["Medium", "High", "High", "Low"],
    })


def test_normalise_text():
    assert normalise_text(pd.Series(["  Direct, the   BUDGET. "]))[0] == "direct the budget"


def test_match_tasks_is_exact_within_occupation(axi, onet):
    m = match_tasks(axi, onet[0])
    assert m["TaskID"].tolist() == ["1", "2", "3"]   # unmatched task dropped


def test_activity_shares(axi, onet):
    ts, t2d = onet
    a = activity_shares(match_tasks(axi, ts), t2d).set_index("DWA_ID")
    # D1 holds tasks 1 (GenAI High) and 3 (Medium); D2 holds task 2 (Low)
    assert a.loc["D1", "pct_GenAI_High"] == 50.0
    assert a.loc["D1", "pct_CI_HIGH_ALGO"] == 100.0
    assert a.loc["D2", "pct_GenAI_High"] == 0.0
    assert "D3" not in a.index                        # no graded task links to D3


def test_occupation_inherits_shares_through_activities(axi, onet):
    ts, t2d = onet
    occ = occupation_shares(activity_shares(match_tasks(axi, ts), t2d), t2d).set_index("SOC")
    # 15-1252 has no graded task of its own but performs D1
    assert occ.loc["15-1252.00", "pct_GenAI_High"] == 50.0
    assert occ.loc["11-1011.00", "pct_GenAI_High"] == 25.0  # mean of D1 (50) and D2 (0)
    assert occ.loc["15-1252.00", "soc6"] == "15-1252"


def test_load_axi_rejects_missing_columns(tmp_path):
    p = tmp_path / "axi.csv"
    pd.DataFrame({"SOC_CODE": ["1"], "Task_Description": ["x"]}).to_csv(p, index=False)
    with pytest.raises(ValueError, match="lacks columns"):
        load_axi(str(p))
