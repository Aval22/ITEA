"""Grading layer 2 (itea.grading.semantic) on synthetic ESCO tables and a stub embedder."""
import numpy as np
import pandas as pd

from itea.grading.semantic import embed, esco_concepts, grade, top_k


def _esco(tmp_path):
    L1 = "http://g/"
    pd.DataFrame({"Level 1 URI": [L1 + "S1", L1 + "S6", L1 + "S2", L1 + "T5"],
                  "Level 1 code": ["S1", "S6", "S2", "T5"]}).to_csv(tmp_path / "skillsHierarchy_en.csv", index=False)
    pd.DataFrame({"conceptUri": ["k:talk", "k:lift", "k:data", "k:law", "g:S6sub"],
                  "broaderUri": [L1 + "S1", "g:S6sub", L1 + "S2", "x:isced", L1 + "S6"]}).to_csv(
        tmp_path / "broaderRelationsSkillPillar_en.csv", index=False)
    pd.DataFrame({"conceptUri": ["k:talk", "k:lift", "k:data", "k:law"],
                  "preferredLabel": ["talk to clients", "lift loads", "analyse data", "tax law"],
                  "description": ["", "move heavy items", "", "rules of taxation"],
                  "skillType": ["skill/competence", "skill/competence", "skill/competence", "knowledge"],
                  "status": ["released"] * 4}).to_csv(tmp_path / "skills_en.csv", index=False)
    pd.DataFrame({"conceptUri": ["k:data"]}).to_csv(tmp_path / "digitalSkillsCollection_en.csv", index=False)
    return str(tmp_path)


def test_concept_groups_and_flags(tmp_path):
    c = esco_concepts(_esco(tmp_path)).set_index("conceptUri")
    assert c.loc["k:talk", "social"] and not c.loc["k:talk", "manual"]
    assert c.loc["k:lift", "manual"] and c.loc["k:lift", "groups"] == "S6"   # reached through a sub-group
    assert c.loc["k:data", "informational"] and c.loc["k:law", "informational"]  # S2/digital, knowledge
    assert c.loc["k:lift", "text"] == "lift loads. move heavy items"


def test_top_k_and_grades(tmp_path):
    concepts = esco_concepts(_esco(tmp_path))
    cvec = np.eye(4, dtype=np.float32)                     # talk, lift, data, law
    tvec = np.array([[0.9, 0, 0.1, 0], [0, 1, 0, 0], [0, 0, 0.7, 0.7]], dtype=np.float32)
    tvec /= np.linalg.norm(tvec, axis=1, keepdims=True)
    idx, sim = top_k(tvec, cvec, k=2)
    assert idx[1, 0] == 1 and sim[0, 0] >= sim[0, 1]
    tasks = pd.DataFrame({"SOC": ["a", "b", "c"], "TaskID": ["1", "2", "3"]})
    g, links, thr = grade(tasks, concepts, idx, sim, percentile=40)
    g = g.set_index("TaskID")
    assert g.loc["2", "manual_share"] == 1.0 and g.loc["2", "K2"] == 0.0
    assert g.loc["3", "E2"] == 1.0 and g.loc["3", "K2"] == 1.0
    assert (links["similarity"] >= round(thr, 4) - 1e-4).all()


def test_embed_uses_encode():
    class Stub:
        def encode(self, texts, **kw):
            assert kw["normalize_embeddings"]
            return np.ones((len(texts), 3))
    assert embed(["a", "b"], Stub()).shape == (2, 3)
