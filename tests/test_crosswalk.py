"""Tests for the BLS SOC 2018 -> ISCO-08 crosswalk builder (synthetic BLS-shaped files)."""
import pandas as pd
import pytest

from itea.crosswalk import build_crosswalk, read_soc2010_isco08, read_soc2010_soc2018, reweight

PREAMBLE = [["Bureau of Labor Statistics", None, None, None], [None] * 4, ["Questions: soc@bls.gov", None, None, None]]


def _write(path, header, rows, sheet="Sheet1", preamble=PREAMBLE):
    width = len(header)
    pre = [r[:width] + [None] * (width - len(r[:width])) for r in preamble]
    pd.DataFrame(pre + [header] + rows).to_excel(path, sheet_name=sheet, header=False, index=False)


@pytest.fixture
def bls_files(tmp_path):
    soc = tmp_path / "soc_2010_to_2018.xlsx"
    _write(soc, ["2010 SOC Code", "2010 SOC Title", "2018 SOC Code", "2018 SOC Title"], [
        ["13-1111", "Management Analysts", "13-1111", "Management Analysts"],
        ["15-1132", "Software Developers, Applications", "15-1252", "Software Developers"],
        ["15-1133", "Software Developers, Systems", "15-1252", "Software Developers"],
        ["99-9999", "Unmapped", "99-9999", "Unmapped"],
    ])
    isco = tmp_path / "isco_soc.xlsx"
    with pd.ExcelWriter(isco) as w:
        pd.DataFrame([["x"]]).to_excel(w, sheet_name="ISCO-08 to 2010 SOC", header=False, index=False)
    with pd.ExcelWriter(isco, mode="a") as w:
        rows = PREAMBLE + [["2010 SOC Code", "2010 SOC Title", "part", "ISCO-08 Code", "ISCO-08 Title EN"]] + [
            ["13-1111 ", "Management Analysts", None, "2421", "Management and organization analysts"],
            ["15-1132", "Software Developers, Applications", None, "2512", "Software developers"],
            ["15-1132", "Software Developers, Applications", "*", "2514", "Applications programmers"],
            ["15-1133", "Software Developers, Systems", None, "2512", "Software developers"],
            ["15-1133", "Software Developers, Systems", None, "25", "(not a unit group)"],
        ]
        pd.DataFrame([r + [None] * (5 - len(r)) for r in rows]).to_excel(
            w, sheet_name="2010 SOC to ISCO-08", header=False, index=False)
    return str(isco), str(soc)


def test_header_detection_and_whitespace(bls_files):
    isco, soc = bls_files
    x = read_soc2010_isco08(isco)
    assert "13-1111" in set(x["soc2010"])            # trailing space removed
    assert set(x["isco"]) == {"2421", "2512", "2514"}  # non-4-digit codes dropped
    assert len(read_soc2010_soc2018(soc)) == 4


def test_many_to_many_weights(bls_files):
    cw = build_crosswalk(*bls_files)
    sw = cw[cw["soc2018"] == "15-1252"]
    # two SOC 2010 parents collapse to two distinct ISCO groups
    assert sorted(sw["isco"]) == ["2512", "2514"]
    assert sw["w"].tolist() == [0.5, 0.5]
    assert cw.groupby("soc2018")["w"].sum().round(12).eq(1.0).all()


def test_unmapped_codes_are_dropped(bls_files):
    cw = build_crosswalk(*bls_files)
    assert "99-9999" not in set(cw["soc2018"])
    assert cw.loc[cw["soc2018"] == "13-1111", "isco"].tolist() == ["2421"]
