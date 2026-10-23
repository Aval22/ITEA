"""The Python port (itea.v3) reproduces the R reference implementation (code/v3/itea_functions_v3.R)."""
import os
import shutil
import subprocess

import numpy as np
import pandas as pd
import pytest

from itea.v3 import ira_v3, itea_v3, oaei_v3_add, oaei_v3_mult

ROOT = os.path.join(os.path.dirname(__file__), "..")


@pytest.mark.skipif(shutil.which("Rscript") is None, reason="R not installed")
def test_python_matches_r_reference(tmp_path):
    out = tmp_path / "r.csv"
    subprocess.run(["Rscript", os.path.join(ROOT, "tests", "r", "v3_parity.R"), ROOT, str(out)], check=True)
    r = pd.read_csv(out)
    itea = itea_v3(r["eac"].values, r["eig"].values, r["eia"].values)
    py = {
        "itea": itea,
        "ira": ira_v3(r["ca"].values, r["iro"].values, r["gee"].values, itea, r["ict"].values),
        "oaei_mult": oaei_v3_mult(itea, r["gee"].values, r["ict"].values, r["ipi"].values),
        "oaei_add": oaei_v3_add(itea, r["gee"].values, r["ict"].values, r["ipi"].values),
    }
    for col, values in py.items():
        np.testing.assert_allclose(np.asarray(values, dtype=float), r[col].values, atol=1e-9, equal_nan=True, err_msg=col)
