# ITEA v4.1 task-grading methodology, version 0.2

**23 October 2026.** English version of `METODOLOGIA_v0.2_ES.md`, which remains the reference text. Decisions are logged in `DECISIONES_ES.md`; validation results are summarised in `VALIDATION_RESULTS_EN.md`.

## 1. What is measured

ITEA measures **algorithmic expropriability**: the potential for the knowledge a worker uses to become embedded in the firm's systems. It is decomposed into six components, each with its own source.

| Component | Question | Level | Status |
|---|---|---|---|
| **K** (codifiability) | Can the knowledge the task uses be expressed as rules or learned from records? | Task | Layer 1 done; layers 2–3 pending |
| **E** (exposure to generative AI) | Can generative AI produce the task's main output, or cut its time substantially? | Task | Layer 1 done; layers 2–3 pending |
| **T** (technology mediation) | Is there technology, documented by its vendor, that supports or automates the task in this occupation? | Task × technology | Inventory done; corpus pending |
| **U** (effective utilisation) | How much of that technology is adopted and actually used? | Sector × country | Adoption (Eurostat) by sector and country done; depth is a declared assumption (0.10–0.35) |
| **S** (certifiable technical competence) | Is there a certification that attests the competence the task requires? | Task × technology | Pending |
| **C** (economic feasibility) | Does it pay off, and how much reorganisation does it require? | Occupation × country | Pending (later layer) |

**Components are not mixed.** K and E are properties of the task, T and S of its technological environment, and U and C of its realisation. Potential expropriability is K × E. The realisable part adds T × U, and the competence gap is T × (1 − S).

## 2. Unit and sources

- **Unit:** the 18,796 tasks of O\*NET 30.2, identified by their official Task ID.
- **Construction sources, all public:**
  - O\*NET 30.2: tasks, links to DWA, IWA and GWA, the Abilities and Skills to Work Activities linkage tables, Technology Skills and Tools Used;
  - ESCO v1.2.1 (skills, skill types, groups, transversal skills, DigComp);
  - public vendor documentation (for T);
  - public certification programmes (for S);
  - Eurostat (for U).
- **Validation sources, never used for construction:**
  - the human exposure labels of Eloundou et al. (2024; MIT licence; 18,739 overlapping tasks);
  - the Anthropic Economic Index;
  - the task-content indices of Acemoglu and Autor (2011);
  - the O\*NET Job Zone;
  - JRC145832 (for OAXI-EU only, not for K).

## 3. Construction layers for K and E

| Layer | Method | Status |
|---|---|---|
| **1. Structural** | `K_GWA = cognitive share × (1 − social share)` and `E_GWA = share of verbal, reasoning and quantitative abilities`, both from the official O\*NET linkage tables, propagated to each task as the mean over its DWAs (`itea.grading.structural`) | **Done and validated** (§5) |
| **2. ESCO semantic layer** | Sentence embeddings (Sentence-BERT). For each task, the k nearest ESCO skills above a relative threshold (p80/p95), re-ranked with NLI. Features: knowledge share, social-skill share and digital-competence share | Pending: requires `sentence-transformers` |
| **3. Anchors** | Zero-shot classification against anchors taken from published definitions: K from the codified/uncodified information distinction of Fernández-Macías and Bisello (2022); E from the Eloundou et al. rubric | Pending |
| **4. LLM (optional)** | Open-weights model run locally at temperature 0, anchored by retrieval of similar cases as in ILO (2025), with full logging | Pending; optional |
| **5. Combination** | JRC-COIN composite-indicator practice: normalisation, coherence checks and aggregation, with Monte Carlo over method choices and per-task uncertainty | Pending |

## 4. Layers T, U and S

**T (technology mediation)**
- **Occupation inventory** (`itea.grading.technology`): 8,785 software products and 18,105 tools.
- **Vendor presence:** Microsoft in 894 occupations, SAP in 303, IBM in 241, Oracle in 240 and Cisco in 43.
- **Finance and consulting pilot:** 967 products (116 Hot Technologies); SAP appears in 18 of 27 occupations.
- **Corpus of vendor-declared capabilities**, in two phases (business software, then embedded AI), each statement with its URL and an archived copy.
- **Task-by-task matching** within each occupation.

**U (effective utilisation) = adoption × depth**
- **Adoption:** Eurostat ICT survey (`itea.grading.eurostat`): by size class (`isoc_eb_iip`, `isoc_eb_ics`, `isoc_eb_ai`), and by NACE sector and country (`isoc_eb_iipn2`, `isoc_eb_ain2`, `isoc_eb_icsn2`). For enterprises with 10+ employees, Spain has ERP in 60.4 % of enterprises (EU-27: 46.4 %) and AI in 20.3 % (EU-27: 20.0 %). **Caveat:** these tables exclude the financial sector (NACE K).
- **Depth:** a declared assumption of 0.10–0.35 (central 0.27), supported by McGrenere and Moore (2000), Aberdeen Group (2006–2007) and Pendo (2019). The whole range is propagated in the Monte Carlo.
- **Central hypothesis:** AI raises usage depth because it lowers the expertise barrier.

**S (certifiable technical competence)**
- Corpus of public certification exam objectives (Microsoft, SAP, Oracle, IBM, Cisco, AWS) and European frameworks (e-CF EN 16234-1, DigComp, ESCO).
- **Gap = T × (1 − S).**

## 5. Validation

Hypotheses are registered before each run (`HIPOTESIS_PREREGISTRADAS_ES.md`; English summary in `VALIDATION_RESULTS_EN.md`).

- **Layer 1:**
  - E1 converges with the Eloundou human exposure labels (ρ = 0.40);
  - K1 converges with non-routine analytical work (ρ = 0.67);
  - K1 runs against routine cognitive content (ρ = −0.21; the hypothesis failed);
  - the risk that K proxies skill level was borderline (ρ = 0.70 with Job Zone);
  - only 5.3 % of the variance of K1 lies within each generalised work activity, so layers 2–4 are needed.
- **Discriminant validation:**
  - K1 stays associated with non-routine analytical work within Job Zone (partial ρ = 0.28);
  - K1 predicts the Eloundou labels net of Job Zone (partial ρ = 0.40);
  - the routine-cognitive index stays negative in non-manual occupations (ρ = −0.21) and is dropped as a validity reference for K (decision D15).
- **Next required tests:**
  - improvement of layers 2–3 over H1, H6, H8 and the within-activity variance;
  - a multitrait-multimethod matrix;
  - a JRC-COIN Monte Carlo.

## 6. Reproducibility

- **Code** in `src/itea/grading/`, with tests in `tests/test_grading_*.py`.
- **Scripts** in `scripts/grading/`.
- **Outputs** in `v4.0/outputs/grading/`.
- **External inputs** are downloaded with `itea fetch` and verified by SHA-256; the Eloundou labels are pinned to commit `0471612`.
- **Policy:** no grade is trained on the legacy AXI grades, and no commit is backdated.
