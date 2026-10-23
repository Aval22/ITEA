"""
Rebuild OAXI-EU from the itea.grading task grades instead of the legacy AXI grades.

The pipeline is the v4.0 one with a different input:

    task grades (K, E per O*NET Task ID)
      -> activities (mean over the tasks linked to each DWA)
      -> O*NET-SOC occupations (mean over the activities they perform)
      -> ISCO-08 (official BLS crosswalk, itea.crosswalk)
      -> OAXI-EU = 1 + 99 · minmax(E^(1-κ) · K^κ)          (itea.oaxi_eu)

Differences from v4.0, by design:
- grades are continuous scores in [0, 1], not shares of tasks with a high grade;
- every O*NET 30.2 task is graded, so no task is lost to text matching;
- κ stays at the v4.0 value (0.40). It is not recalibrated against JRC145832,
  because the structural layer and the JRC index are both ability-based and
  the benchmark would no longer be independent (decision D17).
"""

from __future__ import annotations

import pandas as pd

from ..axi import load_onet
from ..oaxi_eu import KAPPA, oaxi_eu
from ..rollup import to_activities, to_occupations


def grades_to_occupations(grades: pd.DataFrame, onet_dir: str, k: str = "K1", e: str = "E1") -> pd.DataFrame:
    """Task grades (TaskID, `k`, `e`) -> one row per O*NET-SOC occupation with SOC, soc6, `e`, `k`."""
    _, t2d = load_onet(onet_dir)
    g = grades[["TaskID", k, e]].assign(TaskID=grades["TaskID"].astype(str))
    act = to_activities(g, t2d, [e, k])
    return to_occupations(act, t2d, [e, k])


def oaxi_eu_from_grades(grades: pd.DataFrame, onet_dir: str, crosswalk: pd.DataFrame,
                        k: str = "K1", e: str = "E1", kappa: float = KAPPA) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    OAXI-EU built from itea.grading task grades.

    Returns (index, occupations): the ISCO-08 table of itea.oaxi_eu and the
    O*NET-SOC occupation scores it was built from.
    """
    occ = grades_to_occupations(grades, onet_dir, k=k, e=e)
    return oaxi_eu(occ, crosswalk, kappa=kappa, exposure=e, codifiability=k), occ


def compare(new: pd.DataFrame, legacy: pd.DataFrame, top: int = 20) -> dict:
    """Agreement between two OAXI-EU tables at ISCO-4: Spearman, Pearson and top-`top` overlap."""
    m = new[["isco", "OAXI_EU"]].merge(legacy[["isco", "OAXI_EU"]], on="isco", suffixes=("_new", "_legacy"))
    top_new = set(new.nlargest(top, "OAXI_EU")["isco"])
    top_old = set(legacy.nlargest(top, "OAXI_EU")["isco"])
    return {"n_isco": int(len(m)),
            "spearman": float(m["OAXI_EU_new"].corr(m["OAXI_EU_legacy"], method="spearman")),
            "pearson": float(m["OAXI_EU_new"].corr(m["OAXI_EU_legacy"])),
            f"top{top}_overlap": len(top_new & top_old)}
