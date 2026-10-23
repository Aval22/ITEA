---
title: "ITEA Framework — Methodology v4.0"
subtitle: "OAXI-EU on the ISCO-08 axis and v4.1 task grading (in development)"
author: "Alberto García-Lluis Valencia"
date: "23 October 2026"
lang: en
---

# 1. Scope of this document

This is the **methodological reference for ITEA version 4.0**. It extends, and does not replace, the *Consolidated Methodology v3.0* (`docs/ITEA_v3_0_Consolidated_Methodology.docx`).

- **Unchanged:** the ten v3.0 indicators on O\*NET 30.2 (ITEA, IRA, ICT, IFS, IPI, IEF, GEE, IMO, OAEI and AEI) and their formulas. They are cited here only where they bear on v4.0.
- **Added:**
  - the European index **OAXI-EU** on the ISCO-08 axis (§3);
  - the reproducible software architecture (§4);
  - the **v4.1 task-grading** programme (§5), which will replace the index's input.

Everything described here is reproduced from public inputs with the `itea-framework` package (repository `Aval22/ITEA`).

# 2. What ITEA measures

ITEA measures **algorithmic expropriability**: the potential for the knowledge a worker uses to become embedded in the firm's systems. The framework separates three planes:

- **Exposure:** how much of the work AI can reach.
- **Expropriability:** the potential for capture, which requires both exposure and codifiable knowledge.
- **Expropriation:** the normative event, the worker's loss of sovereignty over how that knowledge is exploited. It is not measured directly.

All ITEA indices measure a **potential**: which occupations' knowledge is most open to codification. They do **not** measure realised automation or realised transfers of value.

# 3. OAXI-EU: the European expropriability index

## 3.1 Inputs

- **Task grades (AXI, legacy).** 47,810 O\*NET 29.1 task statements graded on four ordinal scales: automation, codifiability (`CI_Grade`), generative-AI impact and agentic-AI impact. They come from an analysis of the technical specifications of business software and hardware vendors, applied by technology pattern. They are documented in `src/itea/data/README_AXI.md`. Their agreement with independent coders is moderate for codifiability (α = 0.50) and insufficient for automation (α = 0.35). They are replaced in v4.1 (§5).
- **O\*NET 30.2:** tasks and task-to-Detailed-Work-Activity (DWA) links.
- **Official BLS crosswalks:** SOC 2018 → SOC 2010 and SOC 2010 → ISCO-08.

## 3.2 Aggregation

1. **Task to activity.** Each AXI statement is matched to its O\*NET 30.2 task by normalised text within the occupation. 23,890 of the 47,810 tasks match, because O\*NET rewrote many statements between releases. Each DWA receives the share of its tasks with a high grade.
2. **Activity to occupation.** Each of the 923 O\*NET-SOC occupations receives the mean over the activities it performs, so occupations without matched tasks are still covered.
3. **Occupation to ISCO-08.** The official SOC 2018 → SOC 2010 → ISCO-08 chain is many-to-many. It is split with equal weights, with employment weights as an option. Result: **428 ISCO-08 unit groups**.

## 3.3 Index

For each ISCO group:

- **E** is the share of activities with high generative-AI impact.
- **K** is the share of activities with algorithmically codifiable knowledge (`CI_Grade = HIGH_ALGO`).
- Both are min–max normalised.

$$\text{core} = E^{\,1-\kappa}\cdot K^{\,\kappa}, \qquad \text{OAXI-EU} = 1 + 99\cdot \text{minmax}(\text{core})$$

**Why a geometric form:** expropriability requires both exposure and codifiability, so an occupation lacking either cannot score high.

**Choice of κ:** **0.40**, the value that maximises convergence with an independent external index. The optimum is flat between 0.3 and 0.4, and the calibration table is reproduced by `itea.kappa_grid`.

## 3.4 Validation

- **Convergence with the JRC AI-exposure index** (JRC145832; Casas et al., 2026, Table M.1, CC BY 4.0) at ISCO 3-digit level: **Pearson 0.736, Spearman 0.819** over 127 groups. It is reproduced by `itea validate` and by the tests.
- **Caveat:** the JRC index is ability-based. It is independent of the AXI grades, but not of the v4.1 structural layer, which also uses abilities (§5). It is therefore not used to validate K in v4.1.

## 3.5 Changes from the beta

- **Crosswalk.** The one-to-one mapping typed into a wage spreadsheet misassigned some occupations and left 48 professional ISCO groups without data. It is replaced by the official BLS tables.
- **Coverage.** The beta restricted the index to the 784 occupations with employment data. All 923 occupations are now used, reaching 428 ISCO groups (previously 237).

# 4. Software and reproducibility

| Component | Role |
|---|---|
| `itea fetch` | Downloads O\*NET 30.2 and the BLS crosswalks and verifies their SHA-256 |
| `itea build-eu` | Builds OAXI-EU and records input and output hashes (`oaxi_eu.meta.json`) |
| `itea validate` | Computes convergence with the packaged JRC index |
| `itea.rollup` | Carries any task-level score, keyed by O\*NET Task ID, to activities, occupations and ISCO-08 |
| `itea.v3` | v3.0 indicators. CI checks that they reproduce the R reference implementation |
| `itea.grading` | v4.1 task grading (§5) |

- **Testing:** continuous integration runs the tests on Python 3.10, 3.12 and 3.13, installs the package cleanly from its wheel, and checks R–Python parity.
- **Reference outputs:** the CSV files in `v4.0/outputs/`.
- **Excel workbook:** `data/processed/ITEA_v4_0_Workbook.xlsx` is a reading copy of those outputs, generated by `scripts/build_workbook_v4.py`.

# 5. v4.1 task grading (in development)

## 5.1 Why the grading is rebuilt

The AXI grades lack a reproducible task-by-task procedure, take few distinct values and have low reliability on automation. v4.1 replaces them with an automated, documented grading of the **18,796 O\*NET 30.2 tasks**, on these principles:

- **Construction uses official sources only:** the O\*NET linkage tables and ESCO.
- **Validation uses independent references** that are never used for construction.
- **Hypotheses are registered before each run.**
- **No grade is trained on AXI.**

## 5.2 Six components

| Component | Question | Level |
|---|---|---|
| **K** (codifiability) | Can the task's knowledge be expressed as rules or learned from records? | Task |
| **E** (generative-AI exposure) | Can generative AI produce the main output or cut its time substantially? | Task |
| **T** (technology mediation) | Is there vendor-documented technology that supports or automates the task? | Task × technology |
| **U** (effective utilisation) | How much of that technology is adopted and used? | Sector × country |
| **S** (certifiable competence) | Is there a certification that attests the competence? | Task × technology |
| **C** (economic feasibility) | Does it pay off? | Occupation × country |

## 5.3 Status and results

- **Layer 1 (structural), done.**
  - Construction: `K_GWA = cognitive share × (1 − social share)` and `E_GWA` = share of verbal, reasoning and quantitative abilities, both from the O\*NET Abilities and Skills to Work Activities tables, and propagated to each task through its DWAs.
  - Validation: E converges with the Eloundou et al. (2024) human labels (ρ = 0.40), and K with non-routine analytical work (ρ = 0.67, and 0.28 within Job Zone).
  - K predicts human-rated exposure net of skill level (partial ρ = 0.40).
  - Hypotheses that failed: routine cognitive content runs the other way, also in non-manual occupations, and is dropped as a reference; the correlation with Job Zone (0.70) was borderline.
- **Layer U, done:** adoption of ERP, CRM, business intelligence and AI by country and NACE sector (Eurostat; 35 territories × 13 sectors). Usage depth is a declared assumption: 0.10, 0.27 or 0.35. These tables do not cover the financial sector.
- **Layer T, inventory done:** 8,785 software products by occupation (O\*NET Technology Skills). The pilot will be in finance and consulting.
- **Layer 2 (semantic), done:** each task is linked to its 5 nearest ESCO concepts with sentence embeddings (all-mpnet-base-v2, run locally). 68 % of the variance of K2 lies within activities (5 % for K1), and K2 is less tied to skill level (ρ = 0.49 with Job Zone).
- **Layer 3 (NLI anchors), negative result:** it fails its four hypotheses and is not used.
- **OAXI-EU v4.1, built:**
  - components: K = K1 + K2 and E = E1 + E2;
  - uncertainty: a 1,000-draw Monte Carlo with a 5–95 % band per group (median: 66 of 428 places);
  - validation: final E vs Eloundou ρ = 0.45, and final K vs analytical work within Job Zone 0.26;
  - against the v4.0 index: Spearman 0.80. The largest uncertainty comes from E, whose two sources agree weakly.
- **Pending:** layers T, S and C.

**Full detail:** `docs/grading/` (methodology, decision log, hypotheses and results).

# 6. Limitations

1. **OAXI-EU v4.0 inherits the limitations of the AXI grades** (§3.1). Its results should be read as provisional until the v4.1 rebuild.
2. **Task loss across releases.** Only half of the AXI statements match O\*NET 30.2. Aggregation through activities covers every occupation, but with fewer tasks of its own.
3. **Equal crosswalk weights.** Employment weights are available as an option.
4. **The JRC index is not an independent criterion for K** in v4.1 (§3.4).
5. **All indices measure a potential,** not realised outcomes.

# References

- Acemoglu, D., & Autor, D. (2011). Skills, tasks and technologies: Implications for employment and earnings. *Handbook of Labor Economics*, 4B, 1043–1171.
- Casas, P., Fernández-Macías, E., Martínez-Plumed, F., Gómez, E., González-Vázquez, I., & Salotti, S. (2026). *Revisiting the occupational impact of AI in the generative AI era*. JRC145832, European Commission.
- Eloundou, T., Manning, S., Mishkin, P., & Rock, D. (2024). GPTs are GPTs: Labor market impact potential of LLMs. *Science*, 384(6702), 1306–1308.
- Fernández-Macías, E., & Bisello, M. (2022). A comprehensive taxonomy of tasks for assessing the impact of new technologies on work. *Social Indicators Research*, 159, 821–841.
- National Center for O\*NET Development (2026). *O\*NET 30.2 Database*. USDOL/ETA, CC BY 4.0.
- OECD & JRC (2008). *Handbook on Constructing Composite Indicators: Methodology and User Guide*. OECD.
