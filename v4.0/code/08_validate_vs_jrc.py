#!/usr/bin/env python3
"""
08_validate_vs_jrc.py — Pasos 8/9: construye los DOS índices EU y los valida
contra el benchmark JRC (JRC145832, 127 ISCO-3).

Implementa la decisión del autor (dos índices, ver 00_DOCS/DECISION_dos_indices.md):
  - IEA-EU  (exposición)  = aditivo  0,5·GEE + 0,3·exp(Auto_Grade) + 0,2·ICT·(1−IPI)
  - OAXI-EU (expropiación) = exposición(Auto_Grade) × codificabilidad(CI_Grade HIGH_ALGO)
La codificabilidad procede del CI_Grade del AXI (NO del reuseLevel, jubilado tras
el diagnóstico: reuseLevel correlaciona NEGATIVO con la exposición JRC).

Requiere (en el repo): 08_outputs/entornos/onet/axi_tasks_input.parquet,
onet/crosswalk_SOC_ISCO.parquet, hibrido/occ_oaxi_eu.parquet (GEE/ICT/IPI),
comparativo/jrc145832_isco3_scores.parquet (dato de contraste, no público).
"""
import argparse, json, datetime
import pandas as pd

def mm(s): s = pd.to_numeric(s, errors="coerce"); return (s - s.min()) / (s.max() - s.min())

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--base", default="."); a = ap.parse_args()
    ENT = f"{a.base}/08_outputs/entornos"

    ax = pd.read_parquet(f"{ENT}/onet/axi_tasks_input.parquet")[["Auto_Grade", "CI_Grade", "SOC_CODE"]]
    cw = pd.read_parquet(f"{ENT}/onet/crosswalk_SOC_ISCO.parquet")
    ax = ax.merge(cw, left_on="SOC_CODE", right_on="soc", how="left").dropna(subset=["isco"])
    ax["isco"] = ax["isco"].astype(int)
    ax["auto_w"] = ax["Auto_Grade"].map({"HIGH": 1.0, "TRANS": 0.5, "LOW": 0.0}).fillna(0)
    ax["ci_high"] = (ax["CI_Grade"] == "HIGH_ALGO").astype(int)
    axg = ax.groupby("isco").agg(exp_axi=("auto_w", "mean"), codif_axi=("ci_high", "mean"),
                                 n_tasks=("auto_w", "size")).reset_index()

    oc = pd.read_parquet(f"{ENT}/hibrido/occ_oaxi_eu.parquet")[["isco", "GEE", "ICT", "IPI"]]
    df = axg.merge(oc, on="isco", how="inner").dropna(subset=["GEE", "ICT", "IPI"])

    df["IEA_EU"] = 1 + 99 * mm(0.5 * mm(df["GEE"]) + 0.3 * mm(df["exp_axi"]) + 0.2 * mm(df["ICT"] * (1 - df["IPI"])))
    df["OAXI_EU"] = 1 + 99 * mm(mm(df["exp_axi"]) * mm(df["codif_axi"]))
    df.to_parquet(f"{ENT}/hibrido/occ_indices_EU_v1.parquet", index=False)

    # validación vs JRC (ISCO-3)
    jrc = pd.read_parquet(f"{ENT}/comparativo/jrc145832_isco3_scores.parquet")
    df["isco3"] = df["isco"].astype(str).str[:3].astype(int)
    g = df.groupby("isco3").agg(IEA_EU=("IEA_EU", "mean"), OAXI_EU=("OAXI_EU", "mean"),
                                exp_axi=("exp_axi", "mean"), codif_axi=("codif_axi", "mean"),
                                GEE=("GEE", "mean")).reset_index()
    m = g.merge(jrc, on="isco3", how="inner")
    def c(col):
        d = m.dropna(subset=[col, "jrc_score"])
        return round(d[col].corr(d["jrc_score"]), 3), round(d[col].corr(d["jrc_score"], method="spearman"), 3)
    res = {k: c(k) for k in ["exp_axi", "codif_axi", "GEE", "IEA_EU", "OAXI_EU"]}
    print(f"n ISCO-3 comunes: {len(m)}")
    for k, v in res.items(): print(f"  {k:10} Pearson/Spearman = {v}")
    meta = {"step": "8-9 validación", "generated_utc": datetime.datetime.utcnow().isoformat(timespec="seconds")+"Z",
            "n_isco3": int(len(m)), "umbral": 0.70, "vs_JRC": {k: list(v) for k, v in res.items()},
            "nota": "IEA-EU (exposición) valida >=0.70; OAXI-EU (expropiación) diverge por diseño; "
                    "reuseLevel jubilado (corr negativa con exposición); codificabilidad desde CI_Grade."}
    with open(f"{ENT}/comparativo/validation_jrc.meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print("Guardado: occ_indices_EU_v1.parquet + validation_jrc.meta.json")

if __name__ == "__main__":
    main()
