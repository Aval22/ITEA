#!/usr/bin/env python3
"""
06_build_oaxi_eu.py — OAXI-EU preliminar (núcleo de ITEA BRIDGE US–UE).

Compone el índice ocupacional de expropiación europeo sobre el eje ISCO-08,
siguiendo las decisiones de v4.0:
  - Vía HÍBRIDA (D2): núcleo de expropiación nativo-EU; modificadores carry-over.
  - GEE en DOS TIEMPOS (D3): esta versión usa GEE-O*NET por carry-over (preliminar).
  - Núcleo AXI/K/GEE/OAXI (D4).

Estructura (análoga al OAEI v3.0 = ITEA×GEE×ICT×(1−IPI), pero con núcleo EU):
  núcleo EU de expropiación = norm(exposición_BRIDGE) × norm(K_ESCO)
      · exposición_BRIDGE = hib_mean_exposure (señal AXI: Auto_Grade/CI_Grade por tarea→skill)
      · K_ESCO            = esco_mean_k (codificabilidad nativa de ESCO, reuseLevel)
  modificadores estructurales (carry-over O*NET→ISCO): GEE v2.1, ICT, (1−IPI)
  OAXI-EU_raw = núcleo × GEE × ICT × (1−IPI)
  OAXI-EU     = 1 + 99 · minmax(OAXI-EU_raw)        [escala 1..100, como OAEI]

PRELIMINAR: GEE por carry-over (no EQF); pesos K sin calibrar; mapa v1.0-tfidf.
"""
import argparse, json, hashlib, datetime
import pandas as pd, numpy as np

def mm(s):  # min-max a [0,1]
    s = pd.to_numeric(s, errors="coerce")
    lo, hi = s.min(), s.max()
    return (s - lo) / (hi - lo) if hi > lo else s * 0

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--base", default="."); a = ap.parse_args()
    B = a.base; ENT = f"{B}/08_outputs/entornos"

    # --- O*NET: GEE/ICT/IPI/ITEA/OAEI por SOC -> ISCO (carry-over) ---
    wb = pd.read_excel(f"{B}/07_workbooks_ITEA/ITEA_v3.0_Workbook.xlsx",
                       sheet_name="ITEA_INDICATORS_v3.0", header=2)
    wb = wb.rename(columns={"SOC Code": "soc", "GEE v2.1": "GEE", "ITEA v3.0": "ITEA",
                            "OAEI v3.0": "OAEI_onet"})
    for c in ["GEE", "ICT", "IPI", "ITEA", "OAEI_onet"]:
        wb[c] = pd.to_numeric(wb[c], errors="coerce")
    cw = pd.read_parquet(f"{ENT}/onet/crosswalk_SOC_ISCO.parquet")
    wb = wb.merge(cw, on="soc", how="left").dropna(subset=["isco"])
    wb["isco"] = wb["isco"].astype(int)
    onet_isco = wb.groupby("isco")[["GEE", "ICT", "IPI", "ITEA", "OAEI_onet"]].mean().reset_index()

    # --- EU: exposición BRIDGE + K ESCO por ISCO ---
    hib = pd.read_parquet(f"{ENT}/hibrido/hibrido_isco_profile.parquet")[["isco", "mean_exposure"]]
    esco = pd.read_parquet(f"{ENT}/esco/esco_isco_profile.parquet")[["isco", "mean_k_weight"]]

    df = onet_isco.merge(hib, on="isco", how="inner").merge(esco, on="isco", how="inner")
    df = df.dropna(subset=["GEE", "ICT", "IPI", "mean_exposure", "mean_k_weight"])

    # --- composición ---
    df["exp_norm"] = mm(df["mean_exposure"])
    df["k_norm"] = mm(df["mean_k_weight"])
    df["nucleo_EU"] = df["exp_norm"] * df["k_norm"]                  # expropiación = exposición × codificabilidad
    df["raw"] = df["nucleo_EU"] * df["GEE"] * df["ICT"] * (1 - df["IPI"])
    df["OAXI_EU"] = 1 + 99 * mm(df["raw"])
    # variante solo-exposición (sin K) para contraste
    df["raw_exp"] = df["exp_norm"] * df["GEE"] * df["ICT"] * (1 - df["IPI"])
    df["OAXI_EU_exp_only"] = 1 + 99 * mm(df["raw_exp"])

    for c in ["exp_norm", "k_norm", "nucleo_EU", "raw", "OAXI_EU", "raw_exp", "OAXI_EU_exp_only", "OAEI_onet"]:
        df[c] = df[c].round(4)
    out = f"{ENT}/hibrido/occ_oaxi_eu.parquet"
    df.sort_values("OAXI_EU", ascending=False).to_parquet(out, index=False)

    # --- chequeo: ¿cuánto se parece/diverge del OAEI carry-over? ---
    v = df.dropna(subset=["OAEI_onet"])
    r_p = v["OAXI_EU"].corr(v["OAEI_onet"])
    r_s = v["OAXI_EU"].corr(v["OAEI_onet"], method="spearman")
    r_var = df["OAXI_EU"].corr(df["OAXI_EU_exp_only"])
    print(f"OAXI-EU preliminar: {len(df)} grupos ISCO con todos los componentes.")
    print(f"Correlación OAXI-EU vs OAEI-O*NET (carry-over): Pearson={r_p:.3f}  Spearman={r_s:.3f}")
    print(f"  (positiva pero <1 = la aportación EU/codificabilidad desplaza el ranking; sanity OK)")
    print(f"Correlación variante con-K vs solo-exposición: {r_var:.3f}")

    meta = {
        "indice": "OAXI-EU (preliminar)", "version": "v0-carryover",
        "generated_utc": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "formula": "OAXI-EU = 1 + 99·minmax( [norm(exp_BRIDGE)·norm(K_ESCO)] · GEE · ICT · (1−IPI) )",
        "decisiones": {"portabilidad": "hibrida (D2)", "GEE": "carry-over O*NET (D3 fase 1)",
                       "nucleo": "AXI/K/GEE/OAXI (D4)"},
        "n_isco": int(len(df)),
        "corr_vs_OAEI_onet_pearson": round(float(r_p), 4),
        "corr_vs_OAEI_onet_spearman": round(float(r_s), 4),
        "pendiente": ["GEE-EU nativo (EQF)", "calibrar pesos K", "mapa v2.0-embeddings",
                      "invarianza (paso 8)", "validación JRC (paso 9)"],
        "output_sha256": sha(out),
    }
    with open(f"{ENT}/hibrido/occ_oaxi_eu.meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"Guardado: {out} (+ .meta.json)")

if __name__ == "__main__":
    main()
