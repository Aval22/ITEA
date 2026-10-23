# Provenance and limitations of the legacy AXI grades

**Date:** 23 October 2026.
**Scope:** `src/itea/data/axi_task_grades.csv.gz`, with 47,810 O\*NET 29.1 task statements across 923 occupations. It is the input of OAXI-EU in ITEA v4.0.
**Spanish version:** `PROCEDENCIA_AXI_ES.md`.

## 1. How they were produced (as reported by the author)

- **Task-by-task analysis in the professional context:** how existing technology performs each task. Examples are a CRM that builds the sales pipeline from data entered by sales staff, or risk and pricing engines fed with market data.
- **Source:** the public technical specifications of business software and hardware vendors.
- **Typology:** new tasks, modernised and hybrid tasks, and tasks that a new tool does better and that force processes to be reorganised.
- **Second phase:** how far generative and agentic AI, embedded in those tools, extend that support.
- **The cost of the technology was analysed but not included in the grades.**
- **Application by pattern:** the judgements were applied to tasks **by technology pattern**. Each pattern carries fixed grades and texts, with an associated catalogue of 244 technologies (vendor and version).
- **What was not recorded:** how patterns were assigned to the 47,810 tasks (by hand, by script, or with help from a language model). **That assignment cannot be reproduced.**

## 2. What the data show (forensic checks)

| Check | Result |
|---|---|
| The same statement in different occupations (6,451 repeated texts) | Identical grades on all four scales, with no inconsistencies |
| Diversity of the descriptive texts | 5 justifications, 16 generative-AI and 18 agentic-AI descriptions, each tied to a single grade |
| Predictive power of the leading verb | The verb's modal grade is correct for 95.5 % of automation and 95.4 % of codifiability grades |
| Linked scales | `Auto_Grade = LOW` coincides exactly with `CI_Grade = LOW_TRANS` (2,784 tasks) |
| Concentration | 90.6 % of tasks share the same codifiability grade (`MEDIUM_SC`) |
| Unit | O\*NET statements are split into sub-statements (01a, 01b…); only 23,890 match O\*NET 30.2 |

## 3. Measured reliability and validity

**Independent automated coders (June 2026).** On 500 stratified tasks, with models from four providers (DeepSeek, OpenAI, Perplexity and Google):

| Scale | Krippendorff's α | Reading |
|---|---|---|
| Codifiability (`CI_Grade`) | 0.50 | Moderate |
| Automation (`Auto_Grade`) | 0.35 | Insufficient |

- **Deterministic codebook:** a codebook based on the leading verb reproduces the grades with weighted κ = 0.74 (CI) and 0.70 (Auto), out of sample. The grades follow regular patterns but distinguish little between similar tasks.

**Human panel and documented agents (July 2026).**
- **The study:** 20 raters gave 580 ratings of 295 tasks on a 0–3 codifiability scale. The same tasks were also graded by AI agents that documented their sources.
- **Panel reliability:** single-rater reliability is low (α ≈ 0.14), as is usual for undocumented judgements.
- **The panel and the agents agree with each other** (ρ = 0.39).
- **Crossed with `CI_Grade`** on the same tasks, **agreement is close to zero:** ρ = 0.08 with the panel mean and −0.01 to 0.04 with the agents. The human mean barely changes across grades: 1.31 for LOW, 1.64 for MEDIUM and 1.58 for HIGH.

**Reading:** the aggregate OAXI-EU v4.0 result converges with an independent European index (JRC145832: Pearson 0.736, Spearman 0.819). However, **AXI's task-level codifiability is not validated**: independent references on the same construct do not reproduce it.

## 4. Corrections to earlier ITEA documentation

Some earlier ITEA texts described the AXI grades as a task-by-task classification with individual justifications and a higher reliability than was measured. They include the first version of the dataset note and the first draft of the JOSS paper. **The only valid reliability figures are those in §3.**

## 5. What is done with them

- **v4.0:** they are kept as "legacy grades", with this note, so that published results can be reproduced.
- **v4.1:** they are replaced by the automated, documented grading of `itea.grading`, which **is never trained on them** and is validated against independent references under registered hypotheses (`VALIDATION_RESULTS_EN.md`). OAXI-EU v4.1 keeps the overall ordering of the v4.0 index (Spearman 0.80).
