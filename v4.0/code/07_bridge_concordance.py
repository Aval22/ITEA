#!/usr/bin/env python3
"""
07_bridge_concordance.py — Paso 8 (evidencia empírica de invarianza de medición).

Pregunta: ¿el puente tarea-O*NET -> competencia-ESCO (occ_skill_profile_AXI)
reproduce las competencias que la PROPIA ESCO asigna a cada ocupación
(esco_occ_skill), y lo hace por encima del azar?

Si el solape con el perfil nativo de ESCO es muy superior al esperado al azar,
es la primera evidencia de que ambas estructuras (task-based y competence-based)
miden el mismo constructo ocupacional -> precursor de la invarianza formal.

Por cada grupo ISCO:
  A = skills derivadas de tareas (bridge)   B = skills nativas ESCO (todas)   B_ess = esenciales
  recall_ess = |A∩B_ess| / |B_ess|     precision = |A∩B| / |A|     jaccard = |A∩B|/|A∪B|
  lift = recall_ess / (|A|/N)          (N = universo de skills ESCO; baseline azar)
"""
import argparse, json, datetime
import pandas as pd, numpy as np

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--base", default="."); a = ap.parse_args()
    ENT = f"{a.base}/08_outputs/entornos"
    corpus = pd.read_parquet(f"{ENT}/esco/esco_skills_corpus.parquet")
    N = corpus["conceptUri"].nunique()                       # universo de skills ESCO

    prof = pd.read_parquet(f"{ENT}/hibrido/occ_skill_profile_AXI.parquet")
    nat = pd.read_parquet(f"{ENT}/esco/esco_occ_skill.parquet")

    A = prof.groupby("isco")["esco_uri"].apply(set)
    B = nat.groupby("isco")["skillUri"].apply(set)
    Bess = nat[nat["relationType"] == "essential"].groupby("isco")["skillUri"].apply(set)

    rows = []
    for isco in sorted(set(A.index) & set(B.index)):
        a_, b_ = A[isco], B[isco]
        be = Bess.get(isco, set())
        inter = a_ & b_; inter_e = a_ & be
        rec_all = len(inter) / len(b_) if b_ else np.nan
        rec_ess = len(inter_e) / len(be) if be else np.nan
        prec = len(inter) / len(a_) if a_ else np.nan
        jac = len(inter) / len(a_ | b_) if (a_ | b_) else np.nan
        exp_rand = len(a_) / N                                # P(una skill dada ∈ A) al azar
        lift = (rec_ess / exp_rand) if (exp_rand > 0 and be) else np.nan
        rows.append(dict(isco=isco, n_bridge=len(a_), n_esco=len(b_), n_esco_ess=len(be),
                         recall_ess=rec_ess, recall_all=rec_all, precision=prec, jaccard=jac, lift=lift))
    df = pd.DataFrame(rows)
    for c in ["recall_ess","recall_all","precision","jaccard","lift"]:
        df[c] = df[c].round(4)
    out = f"{ENT}/comparativo/bridge_concordance_by_isco.parquet"
    df.to_parquet(out, index=False)

    d = df.dropna(subset=["recall_ess","lift"])
    summ = dict(
        n_isco=int(len(df)),
        recall_ess_mean=round(float(d["recall_ess"].mean()),4),
        recall_ess_median=round(float(d["recall_ess"].median()),4),
        precision_mean=round(float(df["precision"].mean()),4),
        jaccard_mean=round(float(df["jaccard"].mean()),4),
        lift_mean=round(float(d["lift"].mean()),2),
        lift_median=round(float(d["lift"].median()),2),
        pct_lift_gt_1=round(float((d["lift"]>1).mean())*100,1),
        pct_lift_gt_2=round(float((d["lift"]>2).mean())*100,1),
        universo_skills_N=int(N),
    )
    print("=== Paso 8 — concordancia BRIDGE↔ESCO ===")
    for k,v in summ.items(): print(f"  {k}: {v}")
    meta = {"step":"8 — evidencia de invarianza (concordancia BRIDGE↔ESCO)",
            "generated_utc": datetime.datetime.utcnow().isoformat(timespec="seconds")+"Z",
            "interpretacion":"lift>1 = el puente recupera competencias esenciales de ESCO por encima del azar; "
                             "lift alto y recall_ess sustancial = evidencia de que task-based y competence-based "
                             "convergen en el mismo perfil ocupacional.",
            "resumen": summ}
    with open(f"{ENT}/comparativo/bridge_concordance.meta.json","w",encoding="utf-8") as f:
        json.dump(meta,f,ensure_ascii=False,indent=2)
    print("Guardado:", out)

if __name__ == "__main__":
    main()
