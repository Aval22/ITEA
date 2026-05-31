#!/usr/bin/env python3
"""
04_build_environments.py — Arquitectura de 3 entornos ITEA-EU.

Organiza datos e indicadores en TRES entornos para análisis comparativo Y
unificado, sobre el eje común ISCO-08 (4 dígitos):

  ONET    — task-based, US, eje SOC. Indicadores ITEA v3.0 ya calculados.
  ESCO    — competence-based, EU, eje ISCO. Sin tareas (límite natural).
  HIBRIDO — puente O*NET-task -> ESCO-skill (crosswalk + mapeo textual).

Genera, dentro de 08_outputs/entornos/:
  onet/onet_occupations.parquet, onet/crosswalk_SOC_ISCO.parquet
  esco/esco_occupations.parquet, esco/esco_isco_profile.parquet
  hibrido/hibrido_isco_profile.parquet
  comparativo/itea_by_isco.parquet   (una fila por ISCO-4, los 3 entornos)

Lee artefactos canónicos de 08_outputs/ (antes de moverlos a entornos/).
"""
import argparse, os
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=".")
    a = ap.parse_args()
    B = a.base
    O = f"{B}/08_outputs"
    esco_dir = f"{B}/01_ESCO_v1.2.1/ESCO dataset - v1.2.1 - classification - en - csv"
    ENT = f"{O}/entornos"
    for d in ["onet", "esco", "hibrido", "comparativo"]:
        os.makedirs(f"{ENT}/{d}", exist_ok=True)

    # ---------- Crosswalk SOC -> ISCO ----------
    cw = pd.read_excel(f"{B}/04_crosswalk_salarios/Salarios_2024_ONET.xlsx", sheet_name="Hoja1")
    cw = cw[["SOC CODE", "ISCO-08 Code"]].dropna(subset=["ISCO-08 Code"]).rename(
        columns={"SOC CODE": "soc", "ISCO-08 Code": "isco"})
    cw["isco"] = cw["isco"].astype(int)
    cw = cw.drop_duplicates("soc")
    cw.to_parquet(f"{ENT}/onet/crosswalk_SOC_ISCO.parquet", index=False)

    # ---------- ENTORNO O*NET ----------
    wb = pd.read_excel(f"{B}/07_workbooks_ITEA/ITEA_v3.0_Workbook.xlsx",
                       sheet_name="ITEA_INDICATORS_v3.0", header=2)
    keep = {"SOC Code": "soc", "Job Title": "job_title", "SOC Major": "soc_major",
            "Job Zone": "job_zone", "AEI": "AEI", "ITEA v3.0": "ITEA_v3",
            "IRA v3.0": "IRA_v3", "OAEI v3.0": "OAEI_v3",
            "AIOE (Felten 2021)": "AIOE", "Wage Median ($)": "wage_median"}
    onet = wb[[c for c in keep if c in wb.columns]].rename(columns=keep)
    onet = onet.merge(cw, on="soc", how="left")
    onet.to_parquet(f"{ENT}/onet/onet_occupations.parquet", index=False)

    # ---------- ENTORNO ESCO ----------
    occ = pd.read_csv(f"{esco_dir}/occupations_en.csv").drop_duplicates("conceptUri")
    cols = [c for c in ["conceptUri", "preferredLabel", "iscoGroup", "code", "naceCode"] if c in occ.columns]
    esco_occ = occ[cols].rename(columns={"conceptUri": "occupationUri",
                                          "preferredLabel": "occupationLabel", "iscoGroup": "isco"})
    esco_occ.to_parquet(f"{ENT}/esco/esco_occupations.parquet", index=False)

    occ_skill = pd.read_parquet(f"{ENT}/esco/esco_occ_skill.parquet")
    corp = pd.read_parquet(f"{ENT}/esco/esco_skills_corpus.parquet")[["conceptUri", "k_weight_proposed"]]
    occ_skill = occ_skill.merge(corp, left_on="skillUri", right_on="conceptUri", how="left")
    esco_isco = (occ_skill.groupby("isco")
                 .agg(n_occupations=("occupationUri", "nunique"),
                      n_relations=("skillUri", "count"),
                      n_essential=("relationType", lambda s: (s == "essential").sum()),
                      n_optional=("relationType", lambda s: (s == "optional").sum()),
                      mean_k_weight=("k_weight_proposed", "mean"))
                 .reset_index())
    esco_isco["mean_k_weight"] = esco_isco["mean_k_weight"].round(4)
    esco_isco.to_parquet(f"{ENT}/esco/esco_isco_profile.parquet", index=False)

    # ---------- ENTORNO HIBRIDO ----------
    prof = pd.read_parquet(f"{ENT}/hibrido/occ_skill_profile_AXI.parquet")
    hib_isco = (prof.groupby("isco")
                .agg(n_skills=("esco_uri", "nunique"),
                     total_tasks=("n_tasks", "sum"),
                     mean_weighted_score=("weighted_score", "mean"),
                     mean_exposure=("mean_exposure", "mean"),
                     mean_k_weight=("k_weight", "mean"))
                .reset_index())
    for c in ["mean_weighted_score", "mean_exposure", "mean_k_weight"]:
        hib_isco[c] = hib_isco[c].round(4)
    hib_isco.to_parquet(f"{ENT}/hibrido/hibrido_isco_profile.parquet", index=False)

    # ---------- TABLA UNIFICADA POR ISCO ----------
    onet_isco = (onet.dropna(subset=["isco"]).assign(isco=lambda d: d["isco"].astype(int))
                 .groupby("isco").agg(onet_n_soc=("soc", "nunique"),
                                      onet_mean_AEI=("AEI", "mean"),
                                      onet_mean_OAEI_v3=("OAEI_v3", "mean"),
                                      onet_mean_ITEA_v3=("ITEA_v3", "mean"),
                                      onet_mean_AIOE=("AIOE", "mean"),
                                      onet_mean_wage=("wage_median", "mean")).reset_index())
    e = esco_isco.rename(columns={"n_occupations": "esco_n_occ", "n_relations": "esco_n_rel",
                                  "n_essential": "esco_n_essential", "n_optional": "esco_n_optional",
                                  "mean_k_weight": "esco_mean_k"})
    h = hib_isco.rename(columns={"n_skills": "hib_n_skills", "total_tasks": "hib_n_tasks",
                                 "mean_weighted_score": "hib_mean_score",
                                 "mean_exposure": "hib_mean_exposure", "mean_k_weight": "hib_mean_k"})
    uni = onet_isco.merge(e, on="isco", how="outer").merge(h, on="isco", how="outer")
    uni["in_onet"] = uni["onet_n_soc"].notna()
    uni["in_esco"] = uni["esco_n_occ"].notna()
    uni["in_hibrido"] = uni["hib_n_skills"].notna()
    uni["n_entornos"] = uni[["in_onet", "in_esco", "in_hibrido"]].sum(axis=1)
    num = uni.select_dtypes("float").columns
    uni[num] = uni[num].round(3)
    uni = uni.sort_values("isco")
    uni.to_parquet(f"{ENT}/comparativo/itea_by_isco.parquet", index=False)

    print(f"ONET ocupaciones: {len(onet)} (SOC) | con ISCO: {onet['isco'].notna().sum()}")
    print(f"ESCO ISCO-profile: {len(esco_isco)} grupos ISCO | ocupaciones ESCO: {len(esco_occ)}")
    print(f"HIBRIDO ISCO-profile: {len(hib_isco)} grupos ISCO")
    print(f"UNIFICADA itea_by_isco: {len(uni)} grupos ISCO | "
          f"en los 3 entornos: {(uni['n_entornos']==3).sum()} | "
          f"solo 1: {(uni['n_entornos']==1).sum()}")

if __name__ == "__main__":
    main()
