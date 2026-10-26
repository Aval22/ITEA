#!/usr/bin/env python3
"""
Layer F, time annex (D33): time share (a), recurrence (b), regulatory and market exposure (c), heterogeneity
across profiles (d), and hypotheses H29–H30. Measures fixed in the annex of LIBRO_CRITERIOS_capa_F_v0.1_ES.md
before running (commit 0e5d384).

    .venv/bin/python scripts/grading/validate_time.py --onet ITEA-EU_Datos/02_ONET_30.2/db_30_2_text \
        --robot /path/to/aei_raw/robot_exposure/robot_exposure_tasks.csv \
        --oes ITEA-EU_Datos/13_actividad/oes_national.parquet --out v4.0/outputs/grading
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np
import pandas as pd

FT_PER_YEAR = {1: 1, 2: 4, 3: 24, 4: 100, 5: 250, 6: 750, 7: 2000}   # category -> occurrences a year (approx.)
RECURRENCE = {1: "periodic", 2: "periodic", 3: "periodic", 4: "weekly", 5: "daily", 6: "daily", 7: "daily"}
REG = r"regulat|complian|legislat|\blaws?\b|legal"
MKT = r"\bmarket|\bprice|pricing|econom|competit"


def wavg(x, w):
    x, w = np.asarray(x, float), np.asarray(w, float)
    m = ~(np.isnan(x) | np.isnan(w))
    return float((x[m] * w[m]).sum() / w[m].sum())


def within_rank(s, g):
    r = s.groupby(g).rank()
    return r - r.groupby(g).transform("mean")


def main():
    ap = argparse.ArgumentParser()
    for k in ("onet", "robot", "oes", "out"):
        ap.add_argument(f"--{k}", required=True)
    ap.add_argument("--families", default="v4.0/outputs/grading/task_families_v42.csv")
    a = ap.parse_args()
    rng = np.random.default_rng(20261026)

    t = pd.read_csv(a.families, dtype={"TaskID": str})[["SOC", "TaskID", "K", "E", "in_play"]]
    tr = pd.read_csv(os.path.join(a.onet, "Task Ratings.txt"), sep="\t", dtype={"Task ID": str})
    tr = tr.rename(columns={"O*NET-SOC Code": "SOC", "Task ID": "TaskID"})
    im = tr[tr["Scale ID"] == "IM"][["SOC", "TaskID", "Data Value"]].rename(columns={"Data Value": "IM"})
    rt = tr[tr["Scale ID"] == "RT"][["SOC", "TaskID", "Data Value"]].rename(columns={"Data Value": "RT"})
    ft = tr[tr["Scale ID"] == "FT"].copy()
    ft["cat"] = pd.to_numeric(ft.Category, errors="coerce").astype(int)
    ft["p"] = pd.to_numeric(ft["Data Value"], errors="coerce") / 100
    freq = ft.assign(o=ft.cat.map(FT_PER_YEAR) * ft.p).groupby(["SOC", "TaskID"]).o.sum().rename("freq")
    modal = ft.sort_values(["p", "cat"], ascending=[False, False]).drop_duplicates(["SOC", "TaskID"]) \
              .set_index(["SOC", "TaskID"]).cat.rename("ft_modal")
    rob = pd.read_csv(a.robot, usecols=["onetsoc_code", "task_id", "time_share"], dtype={"task_id": str}) \
            .rename(columns={"onetsoc_code": "SOC", "task_id": "TaskID"})

    t = t.merge(im, on=["SOC", "TaskID"], how="left").merge(rt, on=["SOC", "TaskID"], how="left") \
         .merge(rob, on=["SOC", "TaskID"], how="left").join(freq, on=["SOC", "TaskID"]).join(modal, on=["SOC", "TaskID"])
    t["IM"] = t.IM.fillna(t.groupby("SOC").IM.transform("mean")).fillna(1.0)
    t["w_im"] = t.IM / t.groupby("SOC").IM.transform("sum")
    t["time_imputed"] = t.time_share.isna()
    t["w_time"] = t.time_share.fillna(t.w_im)
    t["w_time"] = t.w_time / t.groupby("SOC").w_time.transform("sum")
    t["recurrence"] = t.ft_modal.map(RECURRENCE)

    # (c) regulatory / market tasks via official DWA titles
    td = pd.read_csv(os.path.join(a.onet, "Tasks to DWAs.txt"), sep="\t", dtype=str)
    dr = pd.read_csv(os.path.join(a.onet, "DWA Reference.txt"), sep="\t", dtype=str)
    td = td.merge(dr[["DWA ID", "DWA Title"]], on="DWA ID")
    td["reg"] = td["DWA Title"].str.contains(REG, case=False, regex=True)
    td["mkt"] = td["DWA Title"].str.contains(MKT, case=False, regex=True)
    flags = td.groupby(["O*NET-SOC Code", "Task ID"])[["reg", "mkt"]].any().reset_index() \
              .rename(columns={"O*NET-SOC Code": "SOC", "Task ID": "TaskID"})
    t = t.merge(flags, on=["SOC", "TaskID"], how="left")
    t[["reg", "mkt"]] = t[["reg", "mkt"]].fillna(False)

    # employment weights
    o = pd.read_parquet(a.oes)
    emp = pd.to_numeric(o[(o.O_GROUP == "detailed") & (o.I_GROUP == "cross-industry")].drop_duplicates("OCC_CODE")
                        .set_index("OCC_CODE").TOT_EMP, errors="coerce")
    n_soc = t.groupby(t.SOC.str[:7]).SOC.transform("nunique")
    t["emp_occ"] = t.SOC.str[:7].map(emp) / t.SOC.str[:7].map(t.groupby(t.SOC.str[:7]).SOC.nunique())
    res = {"n_tasks": int(len(t)), "time_share_linked": int((~t.time_imputed).sum()),
           "ft_linked": int(t.freq.notna().sum()), "rt_linked": int(t.RT.notna().sum())}

    # ---- H29: within-occupation Spearman(time_share, freq)
    h = t.dropna(subset=["time_share", "freq"])
    x, y = within_rank(h.time_share, h.SOC), within_rank(h.freq, h.SOC)
    rho = float(np.corrcoef(x, y)[0, 1])
    occs = h.SOC.unique()
    bs = []
    for _ in range(1000):
        pick = rng.choice(occs, len(occs))
        idx = np.concatenate([np.flatnonzero(h.SOC.values == s) for s in pick[:300]])  # 300 occupations per draw
        bs.append(np.corrcoef(x.values[idx], y.values[idx])[0, 1])
    ci = [float(v) for v in np.percentile(bs, [2.5, 97.5])]
    rho_im = float(np.corrcoef(within_rank(h.time_share, h.SOC), within_rank(h.IM, h.SOC))[0, 1])
    res["H29"] = {"n_tasks": int(len(h)), "n_occ": int(len(occs)), "rho_within": round(rho, 3),
                  "ci95": [round(v, 3) for v in ci], "supported": rho > 0.30 and ci[0] > 0,
                  "reported_rho_within_time_vs_importance": round(rho_im, 3),
                  "note": "bootstrap resamples 300 occupations with replacement per draw (computational shortcut)"}

    # ---- occupation shares under both weights
    occ = t.groupby("SOC").apply(lambda d: pd.Series({
        "share_im": float((d.w_im * d.in_play).sum()), "share_time": float((d.w_time * d.in_play).sum()),
        "n_tasks": len(d), "emp": d.emp_occ.iloc[0]}), include_groups=False)
    occ["hours_in_play"] = 8 * occ.share_time
    rho30 = float(occ.share_im.corr(occ.share_time, method="spearman"))
    occ["diff_pp"] = 100 * (occ.share_time - occ.share_im)
    res["H30"] = {"n_occ": int(len(occ)), "rho": round(rho30, 3), "supported": rho30 >= 0.85,
                  "diff_pp_p10_p50_p90": [round(float(occ.diff_pp.quantile(q)), 1) for q in (0.1, 0.5, 0.9)],
                  "corr_ntasks_absdiff": round(float(occ.n_tasks.corr(occ.diff_pp.abs(), method="spearman")), 3)}

    # ---- (a) hours in play, by SOC major group (employment-weighted)
    occ["soc2"] = occ.index.str[:2]
    g = occ.dropna(subset=["emp"]).groupby("soc2").apply(lambda d: pd.Series({
        "emp_M": round(d.emp.sum() / 1e6, 2), "hours_in_play": round(wavg(d.hours_in_play, d.emp), 2),
        "share_time_pct": round(100 * wavg(d.share_time, d.emp), 1), "share_im_pct": round(100 * wavg(d.share_im, d.emp), 1)}),
        include_groups=False)
    res["a_hours_by_soc2"] = g.reset_index().to_dict(orient="records")
    m = occ.dropna(subset=["emp"])
    res["a_overall"] = {"hours_in_play_emp_weighted": round(wavg(m.hours_in_play, m.emp), 2),
                        "share_time_pct": round(100 * wavg(m.share_time, m.emp), 1),
                        "share_im_pct": round(100 * wavg(m.share_im, m.emp), 1)}

    # ---- pooled task-level shares (task time weight x occupation employment)
    tw = t.w_time * t.emp_occ.fillna(0)

    def pooled(mask):
        w = tw[mask]
        return {"share_of_all_work_pct": round(float(100 * w.sum() / tw.sum()), 1),
                "in_play_pct": round(float(100 * (w * t.in_play[mask]).sum() / w.sum()), 1)}
    res["b_recurrence"] = {c: pooled(t.recurrence == c) for c in ("periodic", "weekly", "daily")}
    res["b_recurrence"]["no_ft"] = pooled(t.recurrence.isna())
    res["c_regulatory"] = {"regulatory": pooled(t.reg), "not_regulatory": pooled(~t.reg)}
    res["c_market"] = {"market": pooled(t.mkt), "not_market": pooled(~t.mkt)}
    res["d_relevance"] = {"specialist_RT_lt_50": pooled(t.RT < 50), "common_RT_ge_50": pooled(t.RT >= 50),
                          "no_RT": pooled(t.RT.isna())}
    em = pd.read_csv(os.path.join(a.onet, "Emerging Tasks.txt"), sep="\t", dtype=str)
    res["c_emerging_tasks"] = {"n": int(len(em)), "by_category": em.Category.value_counts().to_dict(),
                               "by_soc2_top": em["O*NET-SOC Code"].str[:2].value_counts().head(8).to_dict()}

    os.makedirs(a.out, exist_ok=True)
    occ.round(4).to_csv(os.path.join(a.out, "time_weighted_occupations_v42.csv"))
    with open(os.path.join(a.out, "validation_time.json"), "w") as fh:
        json.dump(res, fh, indent=1, default=float)
    print(json.dumps(res, indent=1, default=float))


if __name__ == "__main__":
    main()
