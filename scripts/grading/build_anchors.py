#!/usr/bin/env python3
"""
Grading layer 3 (issue #2): anchored zero-shot NLI scores E3 and K3 for the
18,796 O*NET 30.2 tasks. Runs locally (Apple MPS GPU if available). Work is
saved in chunks, so an interrupted run resumes where it stopped.

Usage:
    caffeinate -i python scripts/grading/build_anchors.py --external data/external [--limit 64]
"""

import argparse
import datetime
import json
import os
import time

import pandas as pd

from itea.grading.anchors import ANCHORS, MODEL, entailment_logits, grade


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--external", default="data/external")
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--out", default="v4.0/outputs/grading")
    ap.add_argument("--cache", default="data/external/nli")
    ap.add_argument("--chunk", type=int, default=500)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--limit", type=int, default=None, help="score only the first N tasks (timing test)")
    a = ap.parse_args()

    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    tok = AutoTokenizer.from_pretrained(a.model)
    model = AutoModelForSequenceClassification.from_pretrained(a.model).to(device)
    revision = getattr(model.config, "_commit_hash", None)

    ts = pd.read_csv(os.path.join(a.external, "db_30_2_text", "Task Statements.txt"), sep="\t", dtype=str)
    tasks = ts.rename(columns={"O*NET-SOC Code": "SOC", "Task ID": "TaskID"})[["SOC", "TaskID", "Task"]]
    if a.limit:
        tasks = tasks.head(a.limit)

    slug = a.model.replace("/", "__")
    cdir = os.path.join(a.cache, slug)
    os.makedirs(cdir, exist_ok=True)
    t0, parts = time.time(), []
    for s in range(0, len(tasks), a.chunk):
        path = os.path.join(cdir, f"logits_{s:05d}_{len(tasks)}.csv")
        if os.path.exists(path):
            parts.append(pd.read_csv(path))
            continue
        lg = entailment_logits(tasks["Task"].iloc[s:s + a.chunk], model, tok, device=device, batch_size=a.batch)
        lg.to_csv(path, index=False)
        parts.append(lg)
        done = min(s + a.chunk, len(tasks))
        rate = done / (time.time() - t0)
        print(f"{done}/{len(tasks)} tasks · {rate:.1f} tasks/s · ~{(len(tasks) - done) / rate / 60:.0f} min left", flush=True)

    logits = pd.concat(parts, ignore_index=True)
    g = pd.concat([tasks[["SOC", "TaskID"]].reset_index(drop=True), grade(logits)], axis=1)
    suffix = f"_limit{a.limit}" if a.limit else ""
    os.makedirs(a.out, exist_ok=True)
    g.round(4).to_csv(os.path.join(a.out, f"task_anchors{suffix}.csv"), index=False)
    meta = {"layer": 3, "built": datetime.date.today().isoformat(), "model": a.model, "model_revision": revision,
            "device": device, "anchors": ANCHORS, "n_tasks": int(len(tasks)),
            "seconds": round(time.time() - t0, 1)}
    json.dump(meta, open(os.path.join(a.out, f"task_anchors{suffix}.meta.json"), "w"), indent=2)
    print(json.dumps({k: v for k, v in meta.items() if k != "anchors"}, indent=2))


if __name__ == "__main__":
    main()
