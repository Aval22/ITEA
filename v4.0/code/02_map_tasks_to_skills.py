#!/usr/bin/env python3
"""
02_map_tasks_to_skills.py — Mapeo O*NET-task -> ESCO-skill (pasos 4-5 del pipeline ITEA-EU).

Toma el corpus ESCO (de 01_load_esco.py) y un fichero de tareas O*NET etiquetadas, y por
cada tarea devuelve las top-k competencias ESCO más similares, heredando reuseLevel (peso K).

Dos métodos seleccionables:
  --method tfidf       TF-IDF + coseno. Sin dependencias pesadas; válido para EN<->EN (1a pasada).
  --method embeddings  sentence-transformers multilingüe. Mejor calidad; requiere torch/GPU.
                       (No disponible en este entorno por espacio; usar en máquina local.)

Uso:
  python 02_map_tasks_to_skills.py \
      --skills ../outputs/esco_skills_corpus.parquet \
      --tasks  ../data/onet/onet_tasks_axi.csv \
      --task-text-col task_statement --task-id-col task_id \
      --topk 5 --method tfidf --out ../outputs/task_skill_map.parquet

Formato esperado de tareas O*NET (CSV o parquet):
  - una columna de id de tarea (p.ej. task_id), una de texto (task_statement),
  - opcionalmente Auto_Grade y CI_Grade (se arrastran a la salida).
"""
import argparse, os, sys
import pandas as pd
import numpy as np

# Interpretación del peso K (cristalización) según reuseLevel de ESCO.
K_INTERP = {
    "transversal":         "cristalización muy baja — competencia transversal, reutilizable en cualquier ocupación",
    "cross-sector":        "cristalización baja — competencia intersectorial",
    "sector-specific":     "cristalización media-alta — competencia específica de sector",
    "occupation-specific": "cristalización alta — competencia propia de la ocupación, muy codificable",
}

def similarity_quality(sim):
    if sim >= 0.30: return "fuerte"
    if sim >= 0.15: return "moderada"
    return "débil"

def build_explanation(task_text, rank, topk, sim, skill_label, skill_type, reuse, kw, grades):
    """Frase en lenguaje natural que explica un match tarea O*NET -> competencia ESCO."""
    cristal = K_INTERP.get(reuse, "reuseLevel no especificado")
    txt = (f"La tarea «{str(task_text)[:80].strip()}…» se asocia a la competencia ESCO "
           f"«{skill_label}» (puesto {rank} de {topk}; similitud {sim:.4f}, coincidencia {similarity_quality(sim)}). "
           f"Tipo: {skill_type}; reuseLevel «{reuse}» ⇒ peso K = {kw} ({cristal}).")
    if grades:
        txt += " Etiqueta AXI: " + ", ".join(f"{k}={v}" for k, v in grades.items()) + "."
    return txt

def load_tasks(path, text_col, id_col):
    df = pd.read_parquet(path) if path.endswith(".parquet") else pd.read_csv(path)
    if text_col not in df.columns:
        sys.exit(f"ERROR: no existe la columna de texto '{text_col}'. Columnas: {list(df.columns)}")
    if id_col not in df.columns:
        df = df.reset_index().rename(columns={"index": id_col})
    df[text_col] = df[text_col].astype(str)
    return df

def map_tfidf(tasks_text, skills_text, topk):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import linear_kernel
    vec = TfidfVectorizer(lowercase=True, stop_words="english", ngram_range=(1, 2),
                          min_df=2, max_features=60000)
    # ajustar sobre el conjunto unido para vocabulario común
    vec.fit(pd.concat([pd.Series(skills_text), pd.Series(tasks_text)], ignore_index=True))
    S = vec.transform(skills_text)          # (n_skills, V)
    T = vec.transform(tasks_text)           # (n_tasks, V)
    out_idx, out_sim = [], []
    B = 500
    for i in range(0, T.shape[0], B):
        sims = linear_kernel(T[i:i+B], S)   # coseno (vectores ya normalizados por TF-IDF)
        idx = np.argpartition(-sims, kth=min(topk, sims.shape[1]-1), axis=1)[:, :topk]
        for r in range(sims.shape[0]):
            order = idx[r][np.argsort(-sims[r, idx[r]])]
            out_idx.append(order); out_sim.append(sims[r, order])
    return np.array(out_idx), np.array(out_sim)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skills", required=True)
    ap.add_argument("--tasks", required=True)
    ap.add_argument("--task-text-col", default="task_statement")
    ap.add_argument("--task-id-col", default="task_id")
    ap.add_argument("--topk", type=int, default=5)
    ap.add_argument("--method", choices=["tfidf", "embeddings"], default="tfidf")
    ap.add_argument("--out", required=True)
    ap.add_argument("--map-version", default=None,
                    help="Etiqueta de versión del mapa (p.ej. 1.0-tfidf). Si se omite, se deriva del método.")
    ap.add_argument("--esco-version", default="v1.2.1", help="Versión del dump ESCO usado (procedencia).")
    a = ap.parse_args()
    map_version = a.map_version or f"1.0-{a.method}"

    skills = pd.read_parquet(a.skills)
    tasks = load_tasks(a.tasks, a.task_text_col, a.task_id_col)
    print(f"skills ESCO: {len(skills)} | tareas O*NET: {len(tasks)} | método: {a.method}")

    if a.method == "embeddings":
        sys.exit("Método 'embeddings' no disponible aquí (torch/espacio). Ejecutar en máquina local "
                 "con: pip install sentence-transformers; modelo 'paraphrase-multilingual-MiniLM-L12-v2'.")

    idx, sim = map_tfidf(tasks[a.task_text_col].tolist(), skills["corpus_text"].tolist(), a.topk)

    rows = []
    extra = [c for c in ("Auto_Grade", "CI_Grade") if c in tasks.columns]
    for ti, (ridx, rsim) in enumerate(zip(idx, sim)):
        trow = tasks.iloc[ti]
        for rank, (si, sc) in enumerate(zip(ridx, rsim), 1):
            srow = skills.iloc[si]
            grades = {c: trow[c] for c in extra}
            rec = {"task_id": trow[a.task_id_col], "task_text": trow[a.task_text_col][:120],
                   "rank": rank, "similarity": round(float(sc), 4),
                   "esco_skill": srow["preferredLabel"], "esco_uri": srow["conceptUri"],
                   "skillType": srow["skillType"], "reuseLevel": srow["reuseLevel"],
                   "k_weight": srow["k_weight_proposed"],
                   "explicacion": build_explanation(trow[a.task_text_col], rank, a.topk, float(sc),
                                                    srow["preferredLabel"], srow["skillType"],
                                                    srow["reuseLevel"], srow["k_weight_proposed"], grades),
                   "method": a.method, "map_version": map_version}
            for c in extra: rec[c] = trow[c]
            rows.append(rec)
    out = pd.DataFrame(rows)
    out.to_parquet(a.out, index=False)
    sim1 = float(out[out["rank"] == 1]["similarity"].mean())
    print(f"Mapeo guardado: {a.out} ({len(out)} filas = {len(tasks)} tareas x {a.topk} top-k)")
    print(f"Similitud media del top-1: {sim1:.3f}")

    # --- Sidecar de procedencia/versión: hace el artefacto auto-documentado y evolucionable ---
    import json, hashlib, datetime
    def _sha(p):
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
        return h.hexdigest()
    meta = {
        "map_version": map_version,
        "method": a.method,
        "generated_utc": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "esco_version": a.esco_version,
        "topk": a.topk,
        "n_tasks": int(len(tasks)),
        "n_skills": int(len(skills)),
        "n_rows": int(len(out)),
        "mean_similarity_top1": round(sim1, 4),
        "grade_cols_present": extra,
        "inputs": {
            "skills": {"path": a.skills, "sha256": _sha(a.skills)},
            "tasks":  {"path": a.tasks,  "sha256": _sha(a.tasks)},
        },
        "output": {"path": a.out, "sha256": _sha(a.out)},
        "columns": list(out.columns),
    }
    meta_path = os.path.splitext(a.out)[0] + ".meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"Procedencia guardada: {meta_path} (map_version={map_version})")

if __name__ == "__main__":
    main()
