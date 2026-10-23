"""
Datasets shipped inside the package, so that `pip install` is enough to use them.

    axi_path()        AXI task grades (CC BY 4.0; see data/README_AXI.md)
    jrc_benchmark()   JRC145832 Table M.1: AI exposure 2024 for 127 ISCO-3 groups

The JRC table is transcribed from Appendix M of Casas et al. (2026),
"Revisiting the occupational impact of AI in the generative AI era",
JRC Working Papers Series on Labour, Education and Technology 2026/02,
JRC145832, © European Union, 2026, reused under CC BY 4.0
(https://publications.jrc.ec.europa.eu/repository/handle/JRC145832).
"""

from __future__ import annotations

from importlib.resources import files

import pandas as pd

_DATA = files("itea") / "data"


def axi_path() -> str:
    """Path to the packaged AXI task grades (gzipped CSV)."""
    return str(_DATA / "axi_task_grades.csv.gz")


def jrc_benchmark() -> pd.DataFrame:
    """
    JRC145832 AI-exposure scores for 2024, one row per ISCO-08 3-digit group.

    Columns: isco3 (zero-padded string), occupation, score.
    Ready to pass as `criterion` to itea.oaxi_eu.convergence or kappa_grid.
    """
    df = pd.read_csv(_DATA / "jrc145832_isco3_ai_exposure_2024.csv", dtype={"isco3": str})
    return df.rename(columns={"ai_exposure_2024": "score"})
