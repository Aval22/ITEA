"""
Grading layer 3: anchored zero-shot scoring with a natural-language-inference
model. Design and hypotheses (H14–H17) are registered in
docs/grading/HIPOTESIS_PREREGISTRADAS_ES.md before any run.

For each task (premise) and each group of anchors (hypotheses), the anchor
probabilities are the softmax of the entailment logits within the group.

    E3 = p(e1) + 0.5 · p(e2)       anchors paraphrasing Eloundou et al. (2024)
    K3 = p(k1)                     codified vs uncodified (Fernández-Macías & Bisello, 2022)
"""

from __future__ import annotations

import numpy as np
import pandas as pd

MODEL = "MoritzLaurer/deberta-v3-large-zeroshot-v2.0-c"

ANCHORS = {
    "e1": "Using a large language model, this task could be done in half the time or less with the same quality.",
    "e2": ("This task could be done much faster with a large language model only if it is combined with "
           "other software, such as tools to search documents, read images or run code."),
    "e0": "A large language model would not meaningfully reduce the time needed to do this task.",
    "k1": "The knowledge needed to decide how to do this task can be written down as explicit rules, procedures or data.",
    "k0": ("Doing this task well depends on tacit experience, personal judgment or human interaction "
           "that cannot be written down as rules."),
}
GROUPS = {"E": ("e1", "e2", "e0"), "K": ("k1", "k0")}


def entailment_logits(premises, model, tokenizer, device: str = "cpu", batch_size: int = 32,
                      anchors: dict = ANCHORS) -> pd.DataFrame:
    """Entailment logit of every (premise, anchor) pair: one row per premise, one column per anchor."""
    import torch

    ent = {v.lower(): k for k, v in model.config.id2label.items()}["entailment"]
    keys = list(anchors)
    premises = list(premises)
    out = np.empty((len(premises), len(keys)), dtype=np.float32)
    pairs = [(i, j) for i in range(len(premises)) for j in range(len(keys))]
    model.eval()
    with torch.no_grad():
        for s in range(0, len(pairs), batch_size):
            chunk = pairs[s:s + batch_size]
            enc = tokenizer([premises[i] for i, _ in chunk], [anchors[keys[j]] for _, j in chunk],
                            truncation=True, padding=True, return_tensors="pt").to(device)
            logits = model(**enc).logits[:, ent].float().cpu().numpy()
            for (i, j), v in zip(chunk, logits):
                out[i, j] = v
    return pd.DataFrame(out, columns=keys)


def grade(logits: pd.DataFrame) -> pd.DataFrame:
    """Anchor probabilities within each group, E3 and K3."""
    out = pd.DataFrame(index=logits.index)
    for cols in GROUPS.values():
        z = logits[list(cols)].to_numpy()
        p = np.exp(z - z.max(axis=1, keepdims=True))
        p /= p.sum(axis=1, keepdims=True)
        for c, col in zip(cols, p.T):
            out[f"p_{c}"] = col
    out["E3"] = out["p_e1"] + 0.5 * out["p_e2"]
    out["K3"] = out["p_k1"]
    return out
