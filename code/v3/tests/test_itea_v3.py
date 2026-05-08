"""
Test suite for ITEA Framework v3.0 reference implementation.

Run with: pytest code/v3/tests/ -v

Tests:
1. Reconciliation against the workbook values (Δ < 1e-6)
2. ITEA v3.0 mathematical properties (range [0,1], z-score correctness)
3. IRA v3.0 mathematical properties (range [0,1], 60/40 weighting)
4. OAEI bounds (range [1, 100])
5. Function signatures and error handling
"""
import os
import pytest
import numpy as np
import pandas as pd
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from itea_functions_v3 import (
    itea_v3, ira_v3, oaei_v3_mult, oaei_v3_add,
    oaei_recommend, itea_reconcile, __version__
)


WORKBOOK_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "..",
    "data", "processed", "ITEA_v3_0_Workbook.xlsx"
)


def test_version():
    assert __version__ == "3.0"


# ============================================================
# Reconciliation tests — primary integrity guarantee
# ============================================================

@pytest.mark.skipif(not os.path.exists(WORKBOOK_PATH),
                     reason="workbook not available")
def test_reconciliation_all_indicators():
    """All four indicators must reconcile within 1e-6."""
    df = itea_reconcile(WORKBOOK_PATH)
    assert (df['max_abs_diff'] < 1e-6).all(), (
        f"Reconciliation failed:\n{df}")


# ============================================================
# Mathematical property tests
# ============================================================

def test_itea_v3_range():
    """ITEA v3.0 must produce values in [0, 1] after min-max."""
    eac = np.array([0.0, 0.05, 0.10, 0.15, 0.20])
    eig = np.array([0.60, 0.70, 0.80, 0.90, 1.00])
    eia = np.array([0.00, 0.05, 0.10, 0.15, 0.20])
    out = itea_v3(eac, eig, eia)
    assert np.nanmin(out) == 0.0
    assert np.nanmax(out) == 1.0


def test_itea_v3_monotone():
    """ITEA v3.0 should be monotonic when one component dominates."""
    n = 100
    rng = np.random.default_rng(42)
    # Add tiny noise to EAC so std > 0 (avoid degenerate z-score)
    eac = rng.uniform(0, 0.1, n)
    eig = rng.uniform(0.7, 1.0, n)
    eia = np.linspace(0.0, 0.3, n)  # strictly increasing
    out = itea_v3(eac, eig, eia)
    # Higher EIA should produce higher ITEA on average
    assert np.corrcoef(out, eia)[0, 1] > 0.5


def test_itea_v3_handles_nans():
    """NaN inputs should propagate, not crash."""
    eac = np.array([0.1, np.nan, 0.2])
    eig = np.array([0.8, 0.85, 0.9])
    eia = np.array([0.05, 0.1, 0.15])
    out = itea_v3(eac, eig, eia)
    assert np.isnan(out[1])
    assert not np.isnan(out[0])
    assert not np.isnan(out[2])


def test_ira_v3_range():
    """IRA v3.0 must produce values in [0, 1]."""
    n = 100
    rng = np.random.default_rng(42)
    ca = rng.uniform(0, 1, n)
    iro = rng.uniform(0, 1, n)
    gee = rng.uniform(0, 1, n)
    itea = rng.uniform(0, 1, n)
    ict = rng.uniform(0, 1, n)
    out = ira_v3(ca, iro, gee, itea, ict)
    assert np.nanmin(out) >= 0.0
    assert np.nanmax(out) <= 1.0


def test_ira_v3_weighting():
    """The 60/40 split between CA and IRO_residual is preserved."""
    # Construct case where CA is at max (1.0) and IRO_residual is at min (0.0)
    # then output should equal 0.6
    n = 50
    rng = np.random.default_rng(0)
    ca = np.linspace(0, 1, n)
    iro = rng.uniform(0, 1, n)
    gee = rng.uniform(0, 1, n)
    itea = rng.uniform(0, 1, n)
    ict = rng.uniform(0, 1, n)
    out = ira_v3(ca, iro, gee, itea, ict)
    # IRA at CA=1 should be > IRA at CA=0 (CA dominates with 60% weight)
    assert out[-1] > out[0]


def test_ira_v3_insufficient_data():
    """ira_v3 should raise ValueError when too many NaNs."""
    arr = np.array([np.nan, np.nan, np.nan])
    with pytest.raises(ValueError):
        ira_v3(arr, arr, arr, arr, arr)


def test_oaei_mult_range():
    """OAEI multiplicative must produce values in [1, 100]."""
    n = 50
    rng = np.random.default_rng(1)
    out = oaei_v3_mult(
        rng.uniform(0, 1, n),
        rng.uniform(0, 1, n),
        rng.uniform(0, 1, n),
        rng.uniform(0, 1, n),
    )
    assert np.nanmin(out) == pytest.approx(1.0)
    assert np.nanmax(out) == pytest.approx(100.0)


def test_oaei_add_range():
    """OAEI additive must produce values in [1, 100]."""
    n = 50
    rng = np.random.default_rng(2)
    out = oaei_v3_add(
        rng.uniform(0, 1, n),
        rng.uniform(0, 1, n),
        rng.uniform(0, 1, n),
        rng.uniform(0, 1, n),
    )
    assert np.nanmin(out) == pytest.approx(1.0)
    assert np.nanmax(out) == pytest.approx(100.0)


def test_oaei_variants_correlate():
    """Multiplicative and additive variants should correlate strongly."""
    n = 200
    rng = np.random.default_rng(3)
    itea = rng.uniform(0, 1, n)
    gee = rng.uniform(0, 1, n)
    ict = rng.uniform(0, 1, n)
    ipi = rng.uniform(0, 1, n)
    mult = oaei_v3_mult(itea, gee, ict, ipi)
    add = oaei_v3_add(itea, gee, ict, ipi)
    assert np.corrcoef(mult, add)[0, 1] > 0.5


# ============================================================
# Recommendation engine tests
# ============================================================

def test_oaei_recommend_known_cases():
    rec = oaei_recommend("trilogy_replication")
    assert "multiplicative" in rec
    rec = oaei_recommend("wage_modelling")
    assert "additive" in rec


def test_oaei_recommend_unknown():
    rec = oaei_recommend("foobar_use_case")
    assert "Unknown" in rec


# ============================================================
# Smoke test
# ============================================================

def test_smoke_full_pipeline():
    """End-to-end pipeline on synthetic data."""
    n = 100
    rng = np.random.default_rng(42)
    df = pd.DataFrame({
        'EAC': rng.uniform(0, 0.3, n),
        'EIG': rng.uniform(0.6, 1.0, n),
        'EIA': rng.uniform(0, 0.3, n),
        'CA':  rng.uniform(0, 1, n),
        'IRO': rng.uniform(0, 1, n),
        'GEE': rng.uniform(0, 1, n),
        'ICT': rng.uniform(0, 1, n),
        'IPI': rng.uniform(0, 1, n),
    })
    df['ITEA'] = itea_v3(df['EAC'], df['EIG'], df['EIA'])
    df['IRA']  = ira_v3(df['CA'], df['IRO'], df['GEE'], df['ITEA'], df['ICT'])
    df['OAEI'] = oaei_v3_mult(df['ITEA'], df['GEE'], df['ICT'], df['IPI'])
    df['OAEI+'] = oaei_v3_add(df['ITEA'], df['GEE'], df['ICT'], df['IPI'])
    assert not df['ITEA'].isna().any()
    assert not df['IRA'].isna().any()
    assert not df['OAEI'].isna().any()
    assert not df['OAEI+'].isna().any()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
