"""Tests for OAXI-EU: properties, aggregation and reproduction of the published table."""
import os

import numpy as np
import pandas as pd
import pytest

from itea.oaxi_eu import KAPPA, convergence, kappa_grid, minmax, oaxi_eu

ROOT = os.path.join(os.path.dirname(__file__), "..")
EXTERNAL = os.environ.get("ITEA_EXTERNAL", os.path.join(ROOT, "data", "external"))
PUBLISHED = os.path.join(ROOT, "v4.0", "outputs", "oaxi_eu.csv")


@pytest.fixture
def occ():
    return pd.DataFrame({
        "SOC": ["A-1.00", "A-1.01", "B-2.00", "C-3.00", "D-4.00"],
        "soc6": ["A-1", "A-1", "B-2", "C-3", "D-4"],
        "pct_GenAI_High": [10.0, 30.0, 60.0, 90.0, 50.0],
        "pct_CI_HIGH_ALGO": [2.0, 4.0, 10.0, 6.0, 8.0],
    })


@pytest.fixture
def cw():
    return pd.DataFrame({"soc2018": ["A-1", "B-2", "B-2", "C-3", "D-4"],
                         "isco": ["1111", "2421", "2422", "2421", "3333"],
                         "w": [1.0, 0.5, 0.5, 1.0, 1.0]})


def test_minmax():
    assert minmax([2, 4, 6]).tolist() == [0.0, 0.5, 1.0]
    assert minmax([3, 3]).tolist() == [0.0, 0.0]


def test_scale_and_columns(occ, cw):
    idx = oaxi_eu(occ, cw)
    assert idx["OAXI_EU"].min() == pytest.approx(1.0)
    assert idx["OAXI_EU"].max() == pytest.approx(100.0)
    assert list(idx.columns) == ["isco", "isco3", "E", "K", "n_soc", "core", "OAXI_EU"]
    assert idx["OAXI_EU"].is_monotonic_decreasing


def test_weighted_aggregation(occ, cw):
    idx = oaxi_eu(occ, cw).set_index("isco")
    # SOC-level minmax: E(B-2) = 50/80, E(C-3) = 1; ISCO 2421 = (0.5·E_B + 1·E_C) / 1.5
    assert idx.loc["2421", "E"] == pytest.approx((0.5 * 50 / 80 + 1.0) / 1.5)
    assert idx.loc["2421", "n_soc"] == 2
    assert idx.loc["1111", "n_soc"] == 2               # A-1.00 and A-1.01 share soc6


def test_kappa_extremes(occ, cw):
    e_only, k_only = oaxi_eu(occ, cw, kappa=0.0), oaxi_eu(occ, cw, kappa=1.0)
    assert e_only.sort_values("E")["isco"].tolist() == e_only.sort_values("OAXI_EU")["isco"].tolist()
    assert k_only.sort_values("K")["isco"].tolist() == k_only.sort_values("OAXI_EU")["isco"].tolist()
    with pytest.raises(ValueError):
        oaxi_eu(occ, cw, kappa=1.5)


def test_convergence_and_grid(occ, cw):
    crit = pd.DataFrame({"isco3": [111, 242, 333], "score": [0.1, 0.9, 0.5]})
    c = convergence(oaxi_eu(occ, cw), crit)
    assert c["n_isco3"] == 3 and -1 <= c["pearson"] <= 1
    grid = kappa_grid(occ, cw, crit, kappas=[0.0, KAPPA, 1.0])
    assert grid["kappa"].tolist() == [0.0, KAPPA, 1.0]


def test_published_table_is_well_formed():
    idx = pd.read_csv(PUBLISHED, dtype={"isco": str, "isco3": str})
    assert idx["isco"].str.fullmatch(r"\d{4}").all() and idx["isco"].is_unique
    assert idx["OAXI_EU"].between(1, 100).all()
    # consulting and finance unit groups are covered (they were missing before v4.0)
    assert {"2411", "2412", "2413", "2421", "2512"} <= set(idx["isco"])


@pytest.mark.skipif(not os.path.isdir(os.path.join(EXTERNAL, "db_30_2_text")),
                    reason="external inputs not fetched (run `itea fetch`)")
def test_reproduces_published_table(tmp_path):
    from itea.cli import main
    main(["build-eu", "--external", EXTERNAL, "--out", str(tmp_path)])   # packaged AXI grades
    new = pd.read_csv(tmp_path / "oaxi_eu.csv", dtype={"isco": str}).set_index("isco")
    old = pd.read_csv(PUBLISHED, dtype={"isco": str}).set_index("isco")
    assert new.index.equals(old.index)
    assert np.allclose(new["OAXI_EU"], old["OAXI_EU"], atol=1e-4)


# --- validation against the public JRC145832 benchmark (no download needed) ---

def _published_inputs():
    out = os.path.join(ROOT, "v4.0", "outputs")
    occ = pd.read_csv(os.path.join(out, "occupation_shares.csv"))
    cw = pd.read_csv(os.path.join(out, "crosswalk_soc2018_isco08.csv"), dtype={"isco": str})
    return occ, cw


def test_published_convergence_with_jrc():
    from itea.datasets import jrc_benchmark
    idx = pd.read_csv(PUBLISHED, dtype={"isco": str, "isco3": str})
    c = convergence(idx, jrc_benchmark())
    assert c["n_isco3"] == 127
    assert round(c["pearson"], 3) == 0.736 and round(c["spearman"], 3) == 0.819


def test_kappa_optimum_is_flat_around_published_value():
    from itea.datasets import jrc_benchmark
    occ, cw = _published_inputs()
    grid = kappa_grid(occ, cw, jrc_benchmark()).set_index("kappa")
    best = grid["pearson"].idxmax()
    assert 0.3 <= best <= 0.4
    assert grid.loc[KAPPA, "pearson"] >= grid["pearson"].max() - 0.001
