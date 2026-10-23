#!/usr/bin/env python3
"""
Grading layer 2 (issue #1): embed the 18,796 O*NET 30.2 tasks and the ESCO
v1.2.1 concepts, link them, and write K2/E2 per task. Runs locally (Apple MPS
GPU if available, else CPU); the model is downloaded once and then cached.

Usage:
    python scripts/grading/build_semantic.py --external data/external \
        --esco "ITEA-EU_Datos/01_ESCO_v1.2.1/ESCO dataset - v1.2.1 - classification - en - csv"
"""

import argparse
import datetime
import json
import os
import time

import numpy as np
import pandas as pd

from itea.grading.semantic import MODEL, PERCENTILE, TOP_K, embed, esco_concepts, grade, top_k


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--external", default="data/external")
    ap.add_argument("--esco", required=True)
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--out", default="v4.0/outputs/grading")
    ap.add_argument("--cache", default="data/external/embeddings")
    ap.add_argument("--keep", type=int, default=None,
                    help="variant B: keep this many nearest concepts per task, with no global threshold")
    ap.add_argument("--label", default="", help="suffix for the output files, e.g. _B")
    a = ap.parse_args()

    import torch
    from sentence_transformers import SentenceTransformer

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    t0 = time.time()
    model = SentenceTransformer(a.model, device=device)
    revision = getattr(getattr(model[0], "auto_model", None), "config", None)
    revision = getattr(revision, "_commit_hash", None)

    ts = pd.read_csv(os.path.join(a.external, "db_30_2_text", "Task Statements.txt"), sep="\t", dtype=str)
    tasks = ts.rename(columns={"O*NET-SOC Code": "SOC", "Task ID": "TaskID"})[["SOC", "TaskID", "Task"]]
    concepts = esco_concepts(a.esco)

    os.makedirs(a.cache, exist_ok=True)
    slug = a.model.replace("/", "__")  # the cache is valid only for the model that produced it
    cache_t = os.path.join(a.cache, f"onet302_tasks.{slug}.npy")
    cache_c = os.path.join(a.cache, f"esco121_concepts.{slug}.npy")
    tv = np.load(cache_t) if os.path.exists(cache_t) else embed(tasks["Task"], model)
    cv = np.load(cache_c) if os.path.exists(cache_c) else embed(concepts["text"], model)
    np.save(cache_t, tv)
    np.save(cache_c, cv)
    t_embed = time.time() - t0

    idx, sim = top_k(tv, cv, k=a.keep or TOP_K)
    grades, links, threshold = grade(tasks, concepts, idx, sim, percentile=0 if a.keep else PERCENTILE)

    os.makedirs(a.out, exist_ok=True)
    grades.round(4).to_csv(os.path.join(a.out, f"task_semantic{a.label}.csv"), index=False)
    links.to_csv(os.path.join(a.out, f"task_esco_links{a.label}.csv.gz"), index=False)
    meta = {
        "layer": 2, "built": datetime.date.today().isoformat(), "model": a.model, "model_revision": revision,
        "device": device, "top_k": a.keep or TOP_K, "percentile": 0 if a.keep else PERCENTILE, "similarity_threshold": round(threshold, 4),
        "n_tasks": int(len(tasks)), "n_concepts": int(len(concepts)),
        "n_tasks_without_links": int((grades["n_links"] == 0).sum()), "n_links": int(len(links)),
        "concept_flags": {k: int(concepts[k].sum()) for k in ("social", "manual", "informational")},
        "seconds_embedding": round(t_embed, 1),
    }
    json.dump(meta, open(os.path.join(a.out, f"task_semantic{a.label}.meta.json"), "w"), indent=2)
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
