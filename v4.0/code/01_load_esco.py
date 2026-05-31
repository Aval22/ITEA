#!/usr/bin/env python3
"""
01_load_esco.py — Carga y validación del dump ESCO v1.2.1 (clasificación, EN).
Paso 1 del pipeline ITEA-EU. Construye el corpus textual por competencia para los embeddings.

Uso:
    python 01_load_esco.py --dump ../data/01_esco/dump_v1.2.1_en --out ../outputs

Entradas (del dump oficial ESCO v1.2.1):
    skills_en.csv, occupations_en.csv, ISCOGroups_en.csv, occupationSkillRelations_en.csv
Salidas:
    esco_skills_corpus.parquet   (corpus textual por competencia, listo para embeddings)
    esco_occupations.parquet     (ocupaciones con ISCO-08 y NACE)
    esco_occ_skill.parquet       (relaciones ocupación-competencia essential/optional)
    validation_report.txt
"""
import argparse, os, hashlib
import pandas as pd

EXPECTED = {  # recuentos esperados v1.2.1 (para alerta, no para fallo)
    "occupations": 3043, "skills": 13960, "isco_groups": 619, "occ_skill_rel": 126051,
}

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def build_skill_corpus(sk: pd.DataFrame) -> pd.DataFrame:
    """Corpus textual por competencia: preferredLabel + altLabels + description.
    Es el texto sobre el que correrán los embeddings multilingües del mapeo task->skill."""
    def join_text(row):
        parts = []
        for col in ("preferredLabel", "altLabels", "description"):
            v = row.get(col)
            if isinstance(v, str) and v.strip():
                parts.append(v.replace("\n", " ").strip())
        return " | ".join(parts)
    out = sk.copy()
    out["corpus_text"] = out.apply(join_text, axis=1)
    # reuseLevel -> peso K propuesto (a calibrar): especificidad creciente
    k_weight = {"transversal": 0.25, "cross-sector": 0.50,
                "sector-specific": 0.75, "occupation-specific": 1.00}
    out["k_weight_proposed"] = out["reuseLevel"].map(k_weight)
    return out[["conceptUri", "skillType", "reuseLevel", "k_weight_proposed",
                "preferredLabel", "corpus_text", "status"]]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dump", required=True, help="carpeta con los CSV del dump ESCO")
    ap.add_argument("--out", required=True, help="carpeta de salida")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    sk = pd.read_csv(os.path.join(args.dump, "skills_en.csv"))
    occ = pd.read_csv(os.path.join(args.dump, "occupations_en.csv"))
    isco = pd.read_csv(os.path.join(args.dump, "ISCOGroups_en.csv"))
    osr = pd.read_csv(os.path.join(args.dump, "occupationSkillRelations_en.csv"))

    report = []
    def log(s): report.append(s); print(s)

    log("== VALIDACIÓN DUMP ESCO v1.2.1 ==")
    for name, df, key in [("occupations", occ, "occupations"), ("skills", sk, "skills"),
                          ("isco_groups", isco, "isco_groups"), ("occ_skill_rel", osr, "occ_skill_rel")]:
        flag = "OK" if len(df) == EXPECTED[key] else f"!! esperado {EXPECTED[key]}"
        log(f"  {name:16s}: {len(df):>7d}  {flag}")

    log("\n== INTEGRIDAD ==")
    log(f"  ocupaciones con ISCO-08 : {occ['iscoGroup'].notna().sum()}/{len(occ)}")
    log(f"  ocupaciones con NACE    : {occ['naceCode'].notna().sum()}/{len(occ)}")
    log(f"  skills released         : {(sk['status']=='released').sum()}/{len(sk)}")
    log(f"  reuseLevel nulos        : {sk['reuseLevel'].isna().sum()}")

    log("\n== reuseLevel (proxy de especificidad -> K) ==")
    for lvl, n in sk['reuseLevel'].value_counts(dropna=False).items():
        log(f"  {str(lvl):20s}: {n}")

    log("\n== relaciones ocupación-competencia ==")
    for rt, n in osr['relationType'].value_counts(dropna=False).items():
        log(f"  {str(rt):12s}: {n}")
    ess = osr[osr['relationType']=='essential'].groupby('occupationUri').size()
    log(f"  skills esenciales/ocup.: media={ess.mean():.1f} mediana={ess.median():.0f} max={ess.max()}")

    # --- construir y guardar artefactos del pipeline ---
    corpus = build_skill_corpus(sk)
    corpus.to_parquet(os.path.join(args.out, "esco_skills_corpus.parquet"), index=False)
    occ[["conceptUri","iscoGroup","naceCode","preferredLabel","description","code"]].to_parquet(
        os.path.join(args.out, "esco_occupations.parquet"), index=False)
    osr.to_parquet(os.path.join(args.out, "esco_occ_skill.parquet"), index=False)

    log("\n== SALIDAS ==")
    log(f"  esco_skills_corpus.parquet  ({len(corpus)} competencias con corpus_text + k_weight)")
    log(f"  esco_occupations.parquet    ({len(occ)} ocupaciones con ISCO-08 + NACE)")
    log(f"  esco_occ_skill.parquet      ({len(osr)} relaciones essential/optional)")

    with open(os.path.join(args.out, "validation_report.txt"), "w") as f:
        f.write("\n".join(report))

if __name__ == "__main__":
    main()
