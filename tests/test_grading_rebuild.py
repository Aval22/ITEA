"""OAXI-EU rebuilt from itea.grading task grades (itea.grading.rebuild)."""
import pandas as pd

from itea.grading.rebuild import compare, grades_to_occupations, oaxi_eu_from_grades


def _onet(tmp_path):
    pd.DataFrame({"O*NET-SOC Code": ["11-1011.00", "15-1252.00", "47-2061.00"],
                  "Task ID": ["1", "2", "3"], "Task": ["a", "b", "c"]}).to_csv(
        tmp_path / "Task Statements.txt", sep="\t", index=False)
    pd.DataFrame({"O*NET-SOC Code": ["11-1011.00", "15-1252.00", "15-1252.00", "47-2061.00"],
                  "Task ID": ["1", "2", "2", "3"], "DWA ID": ["D1", "D1", "D2", "D3"]}).to_csv(
        tmp_path / "Tasks to DWAs.txt", sep="\t", index=False)
    return str(tmp_path)


def test_grades_roll_up_through_activities(tmp_path):
    grades = pd.DataFrame({"TaskID": ["1", "2", "3"], "K1": [0.2, 0.8, 0.0], "E1": [0.4, 1.0, 0.1]})
    occ = grades_to_occupations(grades, _onet(tmp_path)).set_index("SOC")
    # D1 = mean(task 1, task 2) = 0.5; D2 = task 2 = 0.8; 15-1252 = mean(D1, D2) = 0.65
    assert abs(occ.loc["11-1011.00", "K1"] - 0.5) < 1e-12
    assert abs(occ.loc["15-1252.00", "K1"] - 0.65) < 1e-12
    assert abs(occ.loc["47-2061.00", "K1"] - 0.0) < 1e-12


def test_index_and_comparison(tmp_path):
    grades = pd.DataFrame({"TaskID": ["1", "2", "3"], "K1": [0.2, 0.8, 0.0], "E1": [0.4, 1.0, 0.1]})
    cw = pd.DataFrame({"soc2018": ["11-1011", "15-1252", "47-2061"], "isco": ["1120", "2512", "7112"], "w": [1.0, 1.0, 1.0]})
    idx, occ = oaxi_eu_from_grades(grades, _onet(tmp_path), cw)
    assert set(idx["isco"]) == {"1120", "2512", "7112"}
    assert idx.iloc[0]["isco"] == "2512" and idx["OAXI_EU"].between(1, 100).all()
    c = compare(idx, idx, top=2)
    assert c["spearman"] == 1.0 and c["top2_overlap"] == 2
