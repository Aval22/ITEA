"""
Grading layer 2: link each O*NET task to ESCO v1.2.1 concepts by sentence
embeddings and derive K2 and E2 from the official ESCO groups of the linked
concepts. Design and hypotheses (H9–H13) are registered in
docs/grading/HIPOTESIS_PREREGISTRADAS_ES.md before any run.

    social        S1, S3, T4
    manual        S6, S7, S8, T5
    informational knowledge concepts, S2, S5, ESCO digital collection, T2

    K2 = (1 − manual share) · (1 − social share)
    E2 = informational share

Shares are similarity-weighted over the concepts kept for each task: its
top-k neighbours whose similarity exceeds a global percentile of all top-k
similarities. The embedding model is passed in, so tests use a stub.
"""

from __future__ import annotations

import os
from collections import defaultdict

import numpy as np
import pandas as pd

MODEL = "sentence-transformers/all-mpnet-base-v2"
TOP_K = 10
PERCENTILE = 80

SOCIAL = {"S1", "S3", "T4"}
MANUAL = {"S6", "S7", "S8", "T5"}
INFORMATIONAL_GROUPS = {"S2", "S5", "T2"}


def _level1_codes(esco_dir: str) -> dict[str, str]:
    """URI -> code (S1…S8, T1…T6) of the level-1 groups of the skills pillar."""
    h = pd.read_csv(os.path.join(esco_dir, "skillsHierarchy_en.csv"), dtype=str)
    h = h.dropna(subset=["Level 1 URI", "Level 1 code"])
    h = h[h["Level 1 code"].str.match(r"^[ST]\d$")]
    return dict(zip(h["Level 1 URI"], h["Level 1 code"]))


def esco_concepts(esco_dir: str) -> pd.DataFrame:
    """
    One row per ESCO skill/knowledge concept with its embedding text and flags:
    conceptUri, label, text, social, manual, informational (booleans), groups.
    """
    sk = pd.read_csv(os.path.join(esco_dir, "skills_en.csv"), dtype=str)
    sk = sk[sk["status"].fillna("released") == "released"] if "status" in sk else sk
    level1 = _level1_codes(esco_dir)

    br = pd.read_csv(os.path.join(esco_dir, "broaderRelationsSkillPillar_en.csv"), dtype=str)
    parents = defaultdict(set)
    for c, b in zip(br["conceptUri"], br["broaderUri"]):
        parents[c].add(b)

    memo: dict[str, frozenset] = {}

    def groups(uri: str, seen=frozenset()) -> frozenset:
        if uri in level1:
            return frozenset({level1[uri]})
        if uri in memo:
            return memo[uri]
        out = set()
        for p in parents.get(uri, ()):
            if p not in seen:
                out |= groups(p, seen | {uri})
        memo[uri] = frozenset(out)
        return memo[uri]

    digital = set(pd.read_csv(os.path.join(esco_dir, "digitalSkillsCollection_en.csv"), dtype=str)["conceptUri"])
    sk = sk.assign(groups=[groups(u) for u in sk["conceptUri"]])
    desc = sk["description"].fillna("").str.replace(r"\s+", " ", regex=True).str.strip()
    sk["text"] = (sk["preferredLabel"].fillna("") + ". " + desc).str.strip()
    sk["social"] = sk["groups"].map(lambda g: bool(g & SOCIAL))
    sk["manual"] = sk["groups"].map(lambda g: bool(g & MANUAL))
    sk["informational"] = ((sk["skillType"] == "knowledge") | sk["conceptUri"].isin(digital)
                           | sk["groups"].map(lambda g: bool(g & INFORMATIONAL_GROUPS)))
    sk["groups"] = sk["groups"].map(lambda g: ",".join(sorted(g)))
    return sk[["conceptUri", "preferredLabel", "skillType", "text", "groups",
               "social", "manual", "informational"]].reset_index(drop=True)


def top_k(task_emb: np.ndarray, concept_emb: np.ndarray, k: int = TOP_K,
          chunk: int = 2048) -> tuple[np.ndarray, np.ndarray]:
    """Indices and cosine similarities of the k nearest concepts for each task (rows normalised)."""
    idx = np.empty((len(task_emb), k), dtype=np.int64)
    sim = np.empty((len(task_emb), k), dtype=np.float32)
    for s in range(0, len(task_emb), chunk):
        m = task_emb[s:s + chunk] @ concept_emb.T
        part = np.argpartition(-m, kth=k - 1, axis=1)[:, :k]
        ps = np.take_along_axis(m, part, axis=1)
        order = np.argsort(-ps, axis=1)
        idx[s:s + chunk] = np.take_along_axis(part, order, axis=1)
        sim[s:s + chunk] = np.take_along_axis(ps, order, axis=1)
    return idx, sim


def grade(tasks: pd.DataFrame, concepts: pd.DataFrame, idx: np.ndarray, sim: np.ndarray,
          percentile: float = PERCENTILE) -> tuple[pd.DataFrame, pd.DataFrame, float]:
    """
    K2, E2 and the shares per task from the top-k links.

    Returns (grades, links, threshold): grades has SOC, TaskID, n_links,
    social_share, manual_share, informational_share, K2, E2; links has one
    row per kept task–concept pair.
    """
    threshold = float(np.percentile(sim, percentile))
    rows = np.repeat(np.arange(len(tasks)), idx.shape[1])
    links = pd.DataFrame({"row": rows, "concept": idx.ravel(), "sim": sim.ravel()})
    links = links[links["sim"] >= threshold]
    flags = concepts.loc[links["concept"], ["social", "manual", "informational"]].astype(float).to_numpy()
    w = links["sim"].to_numpy()[:, None]
    agg = pd.DataFrame(flags * w, columns=["social", "manual", "informational"]).assign(
        row=links["row"].to_numpy(), w=w[:, 0])
    g = agg.groupby("row").sum()
    shares = g[["social", "manual", "informational"]].div(g["w"], axis=0).add_suffix("_share")
    out = tasks[["SOC", "TaskID"]].copy()
    out = out.join(shares, how="left")
    out["n_links"] = links.groupby("row").size().reindex(range(len(tasks))).fillna(0).astype(int).to_numpy()
    out["K2"] = (1 - out["manual_share"]) * (1 - out["social_share"])
    out["E2"] = out["informational_share"]
    link_table = pd.DataFrame({
        "SOC": tasks["SOC"].to_numpy()[links["row"]], "TaskID": tasks["TaskID"].to_numpy()[links["row"]],
        "conceptUri": concepts["conceptUri"].to_numpy()[links["concept"]],
        "label": concepts["preferredLabel"].to_numpy()[links["concept"]],
        "similarity": links["sim"].round(4).to_numpy(),
    })
    return out, link_table, threshold


def embed(texts, model, batch_size: int = 64) -> np.ndarray:
    """Normalised embeddings from a sentence-transformers model (or any object with .encode)."""
    return np.asarray(model.encode(list(texts), batch_size=batch_size, normalize_embeddings=True,
                                   show_progress_bar=False, convert_to_numpy=True), dtype=np.float32)
