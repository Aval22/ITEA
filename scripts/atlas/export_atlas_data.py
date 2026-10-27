#!/usr/bin/env python3
"""
Export the data behind the ITEA atlas of the alienable frontier (v1.0) as one JSON file for the web explorer
(docs/atlas/index.html). Every figure comes from outputs already committed (layer F, time annex) and from public
sources (O*NET 30.2, OEWS, BLS Employment Projections 2025–35, Anthropic Economic Index robot_exposure time shares).

    .venv/bin/python scripts/atlas/export_atlas_data.py --ext /path/to/Datos_externos_ITEA \
        --wages ITEA-EU_Datos/04_crosswalk_salarios/ONET_wages_2025.csv --bls /path/to/bls_projections_2025_35.csv
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np
import pandas as pd

from itea.grading.families import FAM, task_gwa_links, task_types_fmb

ONET = "ITEA-EU_Datos/02_ONET_30.2/db_30_2_text"
TH = {"strict": (0.7066, 0.7210), "central": (0.5124, 0.6198), "broad": (0.2868, 0.5395)}
RECURRENCE = {1: "periodic", 2: "periodic", 3: "periodic", 4: "weekly", 5: "daily", 6: "daily", 7: "daily"}
SOC2 = {"11": "Management", "13": "Business and financial operations", "15": "Computer and mathematical",
        "17": "Architecture and engineering", "19": "Life, physical and social science", "21": "Community and social service",
        "23": "Legal", "25": "Educational instruction and library", "27": "Arts, design, entertainment, sports and media",
        "29": "Healthcare practitioners and technical", "31": "Healthcare support", "33": "Protective service",
        "35": "Food preparation and serving", "37": "Building and grounds cleaning and maintenance",
        "39": "Personal care and service", "41": "Sales and related", "43": "Office and administrative support",
        "45": "Farming, fishing and forestry", "47": "Construction and extraction", "49": "Installation, maintenance and repair",
        "51": "Production", "53": "Transportation and material moving", "55": "Military specific"}
ISCO1 = {"0": "Armed forces", "1": "Managers", "2": "Professionals", "3": "Technicians and associate professionals",
         "4": "Clerical support workers", "5": "Service and sales workers", "6": "Skilled agricultural workers",
         "7": "Craft and related trades workers", "8": "Plant and machine operators", "9": "Elementary occupations"}


# detailed SOC codes that OEWS / BLS publish only within an aggregate code (same table as the PDF atlas script)
SOC_AGG = {"13-1021": "13-1020", "13-1022": "13-1020", "13-1023": "13-1020", "13-2022": "13-2020", "13-2023": "13-2020",
           "21-1011": "21-1018", "21-1014": "21-1018", "25-2055": "25-2052", "25-2056": "25-2052",
           "25-9042": "25-9045", "25-9043": "25-9045", "25-9044": "25-9045", "29-2011": "29-2010", "29-2012": "29-2010",
           "31-1121": "31-1120", "31-1122": "31-1120", "51-2022": "51-2028", "51-2023": "51-2028",
           "53-1042": "53-1047", "53-1043": "53-1047", "53-1044": "53-1047"}


def soc_link(soc6, table):
    """The SOC code under which `table` publishes this occupation: itself, its listed aggregate, or the broad code ending
    in 0. Returns soc6 when nothing is found."""
    for c in (soc6, SOC_AGG.get(soc6), soc6[:6] + "0"):
        if c and c in table and not (isinstance(table, pd.Series) and pd.isna(table.get(c))):
            return c
    return soc6


def r(x, n=1):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ext", required=True)
    ap.add_argument("--wages", required=True)
    ap.add_argument("--bls", required=True)
    ap.add_argument("--out", default="docs/atlas/atlas_data_v1.0.json")
    a = ap.parse_args()

    f = pd.read_csv("v4.0/outputs/grading/task_families_v42.csv", dtype={"TaskID": str})
    links = task_gwa_links(ONET)
    fmb = task_types_fmb(links).rename(columns={"O*NET-SOC Code": "SOC", "Task ID": "TaskID"})
    f = f.merge(fmb[["SOC", "TaskID", "fmb_primary"]], on=["SOC", "TaskID"], how="left")
    f["fam_primary"] = f[FAM].idxmax(axis=1)
    ts = pd.read_csv(os.path.join(ONET, "Task Statements.txt"), sep="\t", dtype=str) \
           .rename(columns={"O*NET-SOC Code": "SOC", "Task ID": "TaskID"})
    f = f.merge(ts[["SOC", "TaskID", "Task"]], on=["SOC", "TaskID"], how="left")
    tr = pd.read_csv(os.path.join(ONET, "Task Ratings.txt"), sep="\t", dtype={"Task ID": str}) \
           .rename(columns={"O*NET-SOC Code": "SOC", "Task ID": "TaskID"})
    im = tr[tr["Scale ID"] == "IM"][["SOC", "TaskID", "Data Value"]].rename(columns={"Data Value": "IM"})
    ft = tr[tr["Scale ID"] == "FT"].assign(cat=lambda x: pd.to_numeric(x.Category, errors="coerce"),
                                           p=lambda x: pd.to_numeric(x["Data Value"], errors="coerce"))
    modal = ft.sort_values(["p", "cat"], ascending=[False, False]).drop_duplicates(["SOC", "TaskID"])[["SOC", "TaskID", "cat"]]
    rob = pd.read_csv(os.path.join(a.ext, "aei_raw/robot_exposure/robot_exposure_tasks.csv"),
                      usecols=["onetsoc_code", "task_id", "time_share"], dtype={"task_id": str}) \
            .rename(columns={"onetsoc_code": "SOC", "task_id": "TaskID"})
    f = f.merge(im, on=["SOC", "TaskID"], how="left").merge(modal, on=["SOC", "TaskID"], how="left") \
         .merge(rob, on=["SOC", "TaskID"], how="left")
    f["im_missing"] = f.IM.isna()   # no importance rating in O*NET: occupation mean, or equal weights if none at all
    f["IM"] = f.IM.fillna(f.groupby("SOC").IM.transform("mean")).fillna(1.0)
    f["w_im"] = f.IM / f.groupby("SOC").IM.transform("sum")
    f["w_time"] = f.time_share.fillna(f.w_im)
    f["w_time"] = f.w_time / f.groupby("SOC").w_time.transform("sum")
    f["rec"] = f.cat.map(RECURRENCE)
    f["state"] = sum(((f.K >= k) & (f.E >= e)).astype(int) for k, e in TH.values())
    k0, e0 = TH["central"]
    f["ip"] = ((f.K >= k0) & (f.E >= e0)).astype(int)

    occ_title = pd.read_csv(os.path.join(ONET, "Occupation Data.txt"), sep="\t", dtype=str).set_index("O*NET-SOC Code").Title
    o = pd.read_parquet("ITEA-EU_Datos/13_actividad/oes_national.parquet")
    # detailed codes plus broad ones (the aggregates some occupations are published under; see soc_link)
    emp = pd.to_numeric(o[o.O_GROUP.isin(["detailed", "broad"]) & (o.I_GROUP == "cross-industry")]
                        .sort_values("O_GROUP", ascending=False).drop_duplicates("OCC_CODE")
                        .set_index("OCC_CODE").TOT_EMP, errors="coerce")
    wages = pd.read_csv(a.wages, dtype={"SOC Code": str}).set_index("SOC Code")
    bls = pd.read_csv(a.bls, dtype={"soc6": str}).fillna({"bls_ai_factor": ""}).set_index("soc6")
    cw = pd.read_csv("v4.0/outputs/crosswalk_soc2018_isco08.csv", dtype={"isco": str})
    tsk = pd.read_csv(os.path.join(ONET, "Technology Skills.txt"), sep="\t", dtype=str)

    # similarity: Jaccard on detailed work activities (official O*NET task -> DWA link)
    td = pd.read_csv(os.path.join(ONET, "Tasks to DWAs.txt"), sep="\t", dtype=str)
    dwa_sets = td.groupby("O*NET-SOC Code")["DWA ID"].apply(set).to_dict()
    codes = sorted(f.SOC.unique())
    soc_used = {c: soc_link(c[:7], emp) for c in codes}
    shared = pd.Series(soc_used).value_counts().to_dict()
    sims = {}
    for c in codes:
        A = dwa_sets.get(c, set())
        sc = [(d, len(A & B) / len(A | B)) for d, B in dwa_sets.items() if d != c and A and B]
        sims[c] = [[d, round(j, 3)] for d, j in sorted(sc, key=lambda t: -t[1])[:8] if j > 0]

    out = []
    for c in codes:
        d = f[f.SOC == c]
        st = float((d.w_time * d.ip).sum())
        ip_w = (d.w_im * d.ip)
        fam = (d[FAM].mul(ip_w, axis=0).sum() / ip_w.sum()) if ip_w.sum() > 0 else None
        rec = d[d.ip == 1].groupby("rec").w_time.sum()
        soc6 = c[:7]
        isco = cw[cw.soc2018 == soc6].assign(g=lambda x: x.isco.str[0]).groupby("g").w.sum()
        g = tsk[tsk["O*NET-SOC Code"] == c]
        hot = list(dict.fromkeys(g[g["Hot Technology"] == "Y"].assign(dem=lambda x: x["In Demand"].eq("Y"))
                                 .sort_values("dem", ascending=False, kind="stable").Example))   # same order as the PDF
        w = wages.loc[c] if c in wages.index else None
        su = soc_used[c]
        sb = soc_link(soc6, bls.index)
        b = bls.loc[sb] if sb in bls.index else None
        e = emp.get(su)
        out.append({
            "code": c, "title": occ_title.get(c, c), "soc2": c[:2],
            "emp": None if e is None or pd.isna(e) else int(e), "emp_shared": shared[su],
            "emp_soc": su if su != soc6 else None, "im_imputed": int(d.im_missing.sum()),
            "n": int(len(d)),
            "share": {s: r(100 * (d.w_im * ((d.K >= k) & (d.E >= e_))).sum()) for s, (k, e_) in TH.items()},
            "share_time": r(100 * st), "hours": r(8 * st, 2),
            "rec": {k: r(100 * rec.get(k, 0) / st) if st > 0 else None for k in ("periodic", "weekly", "daily")},
            "ai": None if fam is None else {k: r(100 * v) for k, v in fam.items()},
            "isco": {k: r(100 * v / isco.sum()) for k, v in isco.items()} if len(isco) else {},
            "wage": None if w is None else {k: r(w[k], 0) for k in ("p10", "p25", "p50", "p75", "p90")},
            "bls": None if b is None else {"chg": r(b.change_pct_2025_35), "open_k": r(b.openings_annual_k),
                                           "ai": b.bls_ai_factor or None},
            "tech": {"n": int(g.Example.nunique()), "classes": g["Commodity Title"].value_counts().index[:4].tolist(),
                     "hot": hot[:10]},
            "tasks": [[t.Task, t.fmb_primary, int(t.state), None if t.im_missing else r(t.IM, 2), t.fam_primary if t.ip else None]
                      for t in d.sort_values(["state", "IM"], ascending=[False, False]).itertuples()],
            "similar": sims[c],
        })
    meta = {"version": "1.0", "built": pd.Timestamp.today().strftime("%Y-%m-%d"),
            "itea_doi": "10.5281/zenodo.23604652", "families": SOC2, "isco1": ISCO1,
            "licence": "© 2026 Alberto García-Lluis Valencia · Epistémica · CC BY-NC 4.0 (non-commercial use only). "
                       "Third-party data keep their own terms (O*NET and Anthropic: CC BY 4.0; BLS: public domain).",
            "onet_attribution": "This product includes information from the O*NET 30.2 Database (https://www.onetcenter.org/database.html) by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license (https://creativecommons.org/licenses/by/4.0/). O*NET® is a trademark of USDOL/ETA. Alberto García-Lluis Valencia has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications. Changes: occupation titles, O*NET-SOC codes and task statements are reproduced unchanged; all other fields (K and E grades, in-play status, shares, hours, recurrence, task types, AI family, similarity) are derived by ITEA (github.com/Aval22/ITEA, scripts/atlas). Contact: aval@epistemica.eu."}
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w") as fh:
        json.dump({"meta": meta, "occupations": out}, fh, ensure_ascii=False, separators=(",", ":"))
    print(a.out, len(out), os.path.getsize(a.out) // 1024, "KB")


if __name__ == "__main__":
    main()
