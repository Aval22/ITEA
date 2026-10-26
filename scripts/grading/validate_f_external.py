#!/usr/bin/env python3
"""
Layer F: H23 (AEI June 2026, API vs claude.ai), H21b (Webb 2020 patent scores) and H28
(Microsoft vs Anthropic usage by GWA). Measures fixed in the second annex of
docs/grading/LIBRO_CRITERIOS_capa_F_v0.1_ES.md before running (commit b8f5c37, decision D31).

    .venv/bin/python scripts/grading/validate_f_external.py --ext /path/to/Datos_externos_ITEA \
        --onet ITEA-EU_Datos/02_ONET_30.2/db_30_2_text --out v4.0/outputs/grading
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np
import pandas as pd

from itea.grading.families import FAM, task_gwa_links

AI_GROUP = ["F1", "F2", "F3", "F4", "F5"]


def weights(fam: pd.DataFrame, onet: str) -> pd.DataFrame:
    tr = pd.read_csv(os.path.join(onet, "Task Ratings.txt"), sep="\t", dtype={"Task ID": str})
    im = tr[tr["Scale ID"] == "IM"].rename(columns={"O*NET-SOC Code": "SOC", "Task ID": "TaskID", "Data Value": "IM"})
    f = fam.merge(im[["SOC", "TaskID", "IM"]], on=["SOC", "TaskID"], how="left")
    f["w"] = f.IM.fillna(f.groupby("SOC").IM.transform("mean")).fillna(1.0)
    f["w"] = f.w / f.groupby("SOC").w.transform("sum")
    return f


def aei_task_pct(path: str, month: str) -> pd.Series:
    cols = ["date_start", "geo_level", "category_name", "hierarchy_level", "metric_id", "value", "node_external_id"]
    parts = []
    for c in pd.read_csv(path, usecols=cols, dtype=str, chunksize=2_000_000):
        parts.append(c[(c.geo_level == "global") & (c.category_name == "onet") & (c.hierarchy_level == "0")
                       & (c.metric_id == "pct") & (c.date_start == month)])
    d = pd.concat(parts)
    return d.assign(v=d.value.astype(float)).groupby("node_external_id").v.sum()


def boot(x, y, rng, reps=2000):
    x, y = np.asarray(x, float), np.asarray(y, float)
    n, out = len(x), []
    for _ in range(reps):
        i = rng.integers(0, n, n)
        out.append(pd.Series(x[i]).corr(pd.Series(y[i]), method="spearman"))
    return [float(v) for v in np.nanpercentile(out, [2.5, 97.5])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ext", required=True)
    ap.add_argument("--onet", required=True)
    ap.add_argument("--families", default="v4.0/outputs/grading/task_families_v42.csv")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rng = np.random.default_rng(20261026)
    fam = weights(pd.read_csv(a.families, dtype={"TaskID": str}), a.onet)
    res = {}

    # ---- H23
    rel = os.path.join(a.ext, "aei_raw", "release_2026_06_26")
    play = fam.groupby("TaskID").in_play.max()
    h23 = {}
    for month in ("2026-05-01", "2026-04-01"):
        row = {}
        for plat, fn in (("claude_ai", "aei_claude_ai_2026-06-26.csv"), ("1p_api", "aei_1p_api_2026-06-26.csv")):
            p = aei_task_pct(os.path.join(rel, fn), month)
            linked = p[p.index.isin(play.index)]
            row[plat] = {"n_tasks_with_pct": int(len(p)), "n_linked": int(len(linked)),
                         "pct_linked_of_total": round(float(linked.sum() / p.sum() * 100), 2),
                         "share_in_play_pct": round(float(linked[play.reindex(linked.index) == 1].sum() / linked.sum() * 100), 2)}
        row["diff_api_minus_claude_pp"] = round(row["1p_api"]["share_in_play_pct"] - row["claude_ai"]["share_in_play_pct"], 2)
        row["supported"] = row["diff_api_minus_claude_pp"] > 10 if month == "2026-05-01" else None
        h23[month] = row
    res["H23"] = h23

    # ---- H21b
    webb = pd.read_stata(os.path.join(a.ext, "living_job_polarization_2026-10-14", "webb", "webb_final_df_out.dta"))
    comp = fam.assign(AI=fam[AI_GROUP].sum(axis=1) * fam.w, SW=fam.F6 * fam.w, ROB=fam.F7 * fam.w) \
              .groupby("SOC")[["AI", "SW", "ROB"]].sum()
    m = comp.join(webb.set_index("onetsoccode")[["ai_score", "software_score", "robot_score"]], how="inner").dropna()
    h21b = {"n_occupations": int(len(m))}
    for g, s in (("AI", "ai_score"), ("SW", "software_score"), ("ROB", "robot_score")):
        rho = float(m[g].corr(m[s], method="spearman"))
        ci = boot(m[g], m[s], rng)
        h21b[f"{g}_vs_{s}"] = {"rho": round(rho, 3), "ci95": [round(v, 3) for v in ci], "pass": rho > 0.20 and ci[0] > 0}
    h21b["supported"] = all(v["pass"] for k, v in h21b.items() if isinstance(v, dict))
    h21b["cross_matrix"] = {g: {s: round(float(m[g].corr(m[s], method="spearman")), 3)
                                for s in ("ai_score", "software_score", "robot_score")} for g in ("AI", "SW", "ROB")}
    res["H21b"] = h21b

    # ---- H28  (IWA -> GWA: the GWA is the IWA code without its ".Ixx" suffix; the annex said
    #           "seven first characters", a typo: GWA codes have nine, e.g. 4.A.1.a.1)
    iwa = pd.read_csv(os.path.join(a.ext, "microsoft_working_with_ai", "iwa_metrics.csv"))
    iwa["GWA"] = iwa.IWA.str.split(".I").str[0]
    ms = iwa.groupby("GWA")[["share_user", "share_ai"]].sum()
    links = task_gwa_links(a.onet)
    links["k"] = 1.0 / links.groupby("Task ID")["GWA"].transform("size")
    cl = aei_task_pct(os.path.join(rel, "aei_claude_ai_2026-06-26.csv"), "2026-05-01")
    lk = links.drop_duplicates(["Task ID", "GWA", "k"]) if False else links
    lk = lk.assign(pct=lk["Task ID"].map(cl).fillna(0.0))
    # one statement per Task ID: links repeat a Task ID only within its own occupation
    an = (lk.pct * lk.k).groupby(lk.GWA).sum().rename("anthropic")
    j = ms.join(an, how="inner")
    jj = j[(j.share_user > 0) & (j.anthropic > 0)]
    rho = float(jj.share_user.corr(jj.anthropic, method="spearman"))
    ci = boot(jj.share_user, jj.anthropic, rng)
    res["H28"] = {"n_gwa": int(len(jj)), "rho_user": round(rho, 3), "ci95": [round(v, 3) for v in ci],
                  "supported": rho > 0.50 and ci[0] > 0,
                  "rho_ai_side_reported": round(float(jj.share_ai.corr(jj.anthropic, method="spearman")), 3),
                  "note": "IWA->GWA by removing the .Ixx suffix (the annex's 'seven characters' was a typo)"}

    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "validation_f_external.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    j.to_csv(os.path.join(a.out, "usage_by_gwa_microsoft_anthropic.csv"))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
