#!/usr/bin/env python3
"""
H24 (layer F): across sectors, the alienable surface of each AI family goes with that family's
adoption by enterprises (Eurostat). Measure fixed in the annex of
docs/grading/LIBRO_CRITERIOS_capa_F_v0.1_ES.md before running (decision D30).

    .venv/bin/python scripts/grading/validate_h24.py --oes ITEA-EU_Datos/13_actividad/oes_national.parquet \
        --families v4.0/outputs/grading/task_families_v42.csv \
        --adoption v4.0/outputs/grading/eurostat_ai_families.csv \
        --concordance docs/grading/concordancia_NAICS_NACE_H24.csv --out v4.0/outputs/grading
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np
import pandas as pd

from itea.grading.families import FAM

SECTOR_LEVEL = {"22", "23", "48-49", "55", "72"}
TESTED = ("F1", "F2", "F5")


def oes_by_sector(oes: pd.DataFrame, conc: pd.DataFrame) -> pd.DataFrame:
    o = oes[(oes.O_GROUP == "detailed") & ~oes.I_GROUP.str.contains("ownership")].copy()
    o["n"] = o.NAICS.astype(str)
    rows = []
    for _, r in conc.iterrows():
        for code in r.naics.split(";"):
            if code in SECTOR_LEVEL:
                part = o[(o.I_GROUP == "sector") & (o.n == code)]
            else:
                part = o[(o.n == code.ljust(6, "0")) & o.I_GROUP.isin(["3-digit", "4-digit"])]
            sign = 1.0
            rows.append(part.assign(nace=r.nace_eurostat, sign=sign)[["nace", "OCC_CODE", "TOT_EMP", "sign"]])
    df = pd.concat(rows)
    # N77-N82 excludes 5615 (travel agencies, N79): subtract it
    travel = o[(o.n == "561500") & (o.I_GROUP == "4-digit")][["OCC_CODE", "TOT_EMP"]].assign(nace="N77-N82_X_N79", sign=-1.0)
    df = pd.concat([df, travel])
    df["emp"] = pd.to_numeric(df.TOT_EMP, errors="coerce") * df.sign
    return df.groupby(["nace", "OCC_CODE"], as_index=False).emp.sum().query("emp > 0")


def occupation_surface(fam: pd.DataFrame) -> pd.DataFrame:
    # task weights: importance within occupation, recomputed exactly as in build_families.py
    s = fam.assign(**{f: fam[f] * fam.in_play * fam.w for f in FAM})
    occ = s.groupby("SOC")[FAM].sum()
    occ["soc6"] = occ.index.str[:7]
    return occ.groupby("soc6")[FAM].mean()


def boot_spearman(x, y, rng, reps=2000):
    x, y = np.asarray(x), np.asarray(y)
    n = len(x)
    stats = []
    for _ in range(reps):
        i = rng.integers(0, n, n)
        if len(set(i)) > 2:
            stats.append(pd.Series(x[i]).corr(pd.Series(y[i]), method="spearman"))
    return np.nanpercentile(stats, [2.5, 97.5]).tolist()


def main():
    ap = argparse.ArgumentParser()
    for k in ("oes", "families", "adoption", "concordance", "out", "onet"):
        ap.add_argument(f"--{k}", required=k not in ("onet",))
    a = ap.parse_args()

    fam = pd.read_csv(a.families, dtype={"TaskID": str})
    if "w" not in fam:
        onet = a.onet or "ITEA-EU_Datos/02_ONET_30.2/db_30_2_text"
        tr = pd.read_csv(os.path.join(onet, "Task Ratings.txt"), sep="\t", dtype={"Task ID": str})
        im = tr[tr["Scale ID"] == "IM"].rename(columns={"O*NET-SOC Code": "SOC", "Task ID": "TaskID", "Data Value": "IM"})
        fam = fam.merge(im[["SOC", "TaskID", "IM"]], on=["SOC", "TaskID"], how="left")
        fam["w"] = fam.IM.fillna(fam.groupby("SOC").IM.transform("mean")).fillna(1.0)
        fam["w"] = fam.w / fam.groupby("SOC").w.transform("sum")
    occ = occupation_surface(fam)

    emp = oes_by_sector(pd.read_parquet(a.oes), pd.read_csv(a.concordance, dtype=str))
    emp = emp[emp.OCC_CODE.isin(occ.index)]
    j = emp.join(occ, on="OCC_CODE")
    surf = j.groupby("nace").apply(lambda d: pd.Series({f: np.average(d[f], weights=d.emp) for f in FAM}), include_groups=False)

    ad = pd.read_csv(a.adoption)
    rng = np.random.default_rng(20261026)
    res = {"n_sectors": int(len(surf)), "by_geo": {}}
    for geo in ("EU27_2020", "ES"):
        g = ad[ad.geo == geo].sort_values("time")
        latest = g.groupby(["nace_r2", "family"]).agg(value=("value", "last"), time=("time", "last")).reset_index()
        adop = latest.pivot(index="nace_r2", columns="family", values="value").reindex(surf.index)
        years = latest.pivot(index="nace_r2", columns="family", values="time").reindex(surf.index)
        out = {}
        for f in FAM:
            m = pd.concat([surf[f], adop.get(f)], axis=1, keys=["surface", "adoption"]).dropna()
            rho = float(m.surface.corr(m.adoption, method="spearman")) if len(m) > 2 else None
            ci = boot_spearman(m.surface, m.adoption, rng) if len(m) > 2 else None
            out[f] = {"n": int(len(m)), "rho": rho, "ci95": ci,
                      "years": sorted(set(years[f].dropna().astype(int))) if f in years else [],
                      "tested": f in TESTED,
                      "supported": (rho is not None and rho > 0.30 and len(m) >= 12) if f in TESTED else None}
        res["by_geo"][geo] = out
    os.makedirs(a.out, exist_ok=True)
    surf.round(5).to_csv(os.path.join(a.out, "surface_by_sector_family_v42.csv"))
    with open(os.path.join(a.out, "validation_h24.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
