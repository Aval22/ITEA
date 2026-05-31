#!/usr/bin/env python3
"""
03_aggregate_to_occupation.py — Paso 7 del pipeline ITEA-EU.

Produce DOS perfiles de competencia por ocupación, ambos anclados a ISCO-08,
para que sean comparables en el paso 8 (prueba de invarianza de medición):

  A) PERFIL NATIVO ESCO (referencia): occupationSkillRelations -> iscoGroup.
     Es la "cuota oficial" de skills por ocupación según ESCO.

  B) PERFIL DERIVADO DE TAREAS (AXI): task_skill_map (mejor skill por tarea)
     -> SOC -> ISCO (crosswalk) -> agregado por (ISCO, skill).
     Ponderación: similitud del match × exposición del grado AXI.
     NOTA: los Task Ratings de O*NET NO se usan (el Task_ID del AXI es local
     por ocupación y no casa con O*NET; ver MAPPING_VERSIONS.md). La señal de
     tarea proviene de Auto_Grade/CI_Grade, base del AEI.

Pesos de grado (alineados con la fórmula AEI = %HIGH×1 + %TRANS×0.5 + %HIGH_ALGO×2):
  Auto_Grade: HIGH=1.0, TRANS=0.5, LOW=0.0
  CI_Grade:   HIGH_ALGO aporta +2.0 (codificación algorítmica de conocimiento)
  exposición_tarea = auto_w + 2.0×(CI_Grade==HIGH_ALGO)

Uso:
  python3 03_aggregate_to_occupation.py --base . --out-dir 08_outputs
"""
import argparse, os, json, hashlib, datetime
import pandas as pd

AUTO_W = {"HIGH": 1.0, "TRANS": 0.5, "LOW": 0.0}

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=".", help="raíz del repositorio ITEA-EU_Datos")
    ap.add_argument("--out-dir", default="08_outputs")
    a = ap.parse_args()
    B = a.base
    esco = f"{B}/01_ESCO_v1.2.1/ESCO dataset - v1.2.1 - classification - en - csv"

    # ---------- A) PERFIL NATIVO ESCO ----------
    osr = pd.read_csv(f"{esco}/occupationSkillRelations_en.csv")
    occ = pd.read_csv(f"{esco}/occupations_en.csv")[["conceptUri", "preferredLabel", "iscoGroup"]]
    occ = occ.drop_duplicates("conceptUri")   # 4 conceptUri duplicados en el dump; evita inflar el merge
    occ = occ.rename(columns={"conceptUri": "occupationUri", "preferredLabel": "occupationLabel"})
    nat = osr.merge(occ, on="occupationUri", how="left")
    nat = nat.rename(columns={"iscoGroup": "isco"})
    nat_out = f"{B}/{a.out_dir}/entornos/esco/esco_occ_skill.parquet"
    nat.to_parquet(nat_out, index=False)
    print(f"[A] esco_occ_skill.parquet: {len(nat)} relaciones | "
          f"ocupaciones={nat['occupationUri'].nunique()} | ISCO={nat['isco'].nunique()}")

    # ---------- B) PERFIL DERIVADO DE TAREAS (AXI) ----------
    m = pd.read_parquet(f"{B}/{a.out_dir}/entornos/hibrido/task_skill_map.parquet")
    inp = pd.read_parquet(f"{B}/{a.out_dir}/entornos/onet/axi_tasks_input.parquet")[["task_uid", "SOC_CODE"]]
    cw = pd.read_excel(f"{B}/04_crosswalk_salarios/Salarios_2024_ONET.xlsx", sheet_name="Hoja1")
    cw = cw[["SOC CODE", "ISCO-08 Code"]].dropna(subset=["ISCO-08 Code"])
    cw["isco"] = cw["ISCO-08 Code"].astype(int)
    cw = cw.rename(columns={"SOC CODE": "SOC_CODE"})[["SOC_CODE", "isco"]].drop_duplicates("SOC_CODE")

    best = m[m["rank"] == 1].copy()                       # mejor skill ESCO por tarea
    best = best.merge(inp, left_on="task_id", right_on="task_uid", how="left")
    best = best.merge(cw, on="SOC_CODE", how="left")
    cov = best["isco"].notna().mean() * 100
    print(f"[B] tareas con ISCO asignado (vía crosswalk): {cov:.1f}%")
    best = best.dropna(subset=["isco"]); best["isco"] = best["isco"].astype(int)

    best["auto_w"] = best["Auto_Grade"].map(AUTO_W).fillna(0.0)
    best["ci_high"] = (best["CI_Grade"] == "HIGH_ALGO").astype(int)
    best["exposure"] = best["auto_w"] + 2.0 * best["ci_high"]
    best["weighted"] = best["similarity"] * best["exposure"]

    prof = (best.groupby(["isco", "esco_uri", "esco_skill", "skillType", "reuseLevel", "k_weight"])
                 .agg(n_tasks=("task_id", "count"),
                      mean_similarity=("similarity", "mean"),
                      mean_exposure=("exposure", "mean"),
                      weighted_score=("weighted", "sum"),
                      n_high_algo=("ci_high", "sum"))
                 .reset_index())
    prof["mean_similarity"] = prof["mean_similarity"].round(4)
    prof["mean_exposure"] = prof["mean_exposure"].round(4)
    prof["weighted_score"] = prof["weighted_score"].round(4)
    prof = prof.sort_values(["isco", "weighted_score"], ascending=[True, False])
    prof_out = f"{B}/{a.out_dir}/entornos/hibrido/occ_skill_profile_AXI.parquet"
    prof.to_parquet(prof_out, index=False)
    print(f"[B] occ_skill_profile_AXI.parquet: {len(prof)} pares (ISCO×skill) | "
          f"ISCO={prof['isco'].nunique()} | skills={prof['esco_uri'].nunique()}")

    # ---------- Sidecar de procedencia ----------
    meta = {
        "step": "7 — agregación a ocupación (ISCO-08)",
        "generated_utc": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "esco_native": {"path": nat_out, "rows": int(len(nat)),
                        "occupations": int(nat["occupationUri"].nunique()),
                        "isco_groups": int(nat["isco"].nunique()), "sha256": sha(nat_out)},
        "axi_derived": {"path": prof_out, "rows": int(len(prof)),
                        "isco_groups": int(prof["isco"].nunique()),
                        "skills": int(prof["esco_uri"].nunique()),
                        "soc_to_isco_coverage_pct": round(cov, 1),
                        "weighting": "similarity × (auto_w + 2·[CI=HIGH_ALGO]); auto HIGH=1,TRANS=.5,LOW=0",
                        "task_ratings_used": False,
                        "sha256": sha(prof_out)},
    }
    with open(f"{B}/{a.out_dir}/entornos/hibrido/occ_aggregation.meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print("Procedencia guardada: occ_aggregation.meta.json")

if __name__ == "__main__":
    main()
