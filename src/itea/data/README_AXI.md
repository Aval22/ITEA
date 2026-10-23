# AXI task grades (v1.0)

`axi_task_grades.csv.gz` — 47,810 O\*NET task statements (923 O\*NET-SOC
occupations, O\*NET 29.1 task text) graded on four ordinal scales. This is
the task-level input of OAXI-EU (`itea build-eu`).

| Column | Values | Meaning |
|---|---|---|
| `SOC_CODE` | e.g. `13-1111.00` | O\*NET-SOC 2019 occupation code |
| `Task_ID` | e.g. `01a` | Task identifier **local to the occupation** (not the O\*NET Task ID; 100 pairs repeat within an occupation) |
| `Task_Description` | text | O\*NET task statement |
| `Auto_Grade` | `HIGH` / `TRANS` / `LOW` | Potential automation of the task by pre-GenAI technology (≥80 % / 30–79 % with supervision / <30 %) |
| `CI_Grade` | `HIGH_ALGO` / `MEDIUM_SC` / `LOW_TRANS` | Codifiability of the knowledge the task uses: algorithmic codification into firm assets / partial codification of contextual know-how / knowledge stays with the worker |
| `GenAI_Impact` | `High` / `Medium` / `Low` | Expected impact of generative AI on the task |
| `Agentic_Impact` | `High` / `Medium` / `Low` | Expected impact of agentic AI on the task |

Distribution: Auto_Grade HIGH 875 · TRANS 44,151 · LOW 2,784; CI_Grade HIGH_ALGO 1,709 ·
MEDIUM_SC 43,317 · LOW_TRANS 2,784; GenAI_Impact High 9,730 · Medium 31,477 · Low 6,603;
Agentic_Impact High 7,704 · Medium 35,019 · Low 5,087.

**Linked scales.** `Auto_Grade = LOW` and `CI_Grade = LOW_TRANS` occur on
exactly the same 2,784 tasks: the methodology treats a task with minimal
automation potential as one whose knowledge stays with the worker. The two
scales vary independently only among the remaining 45,026 tasks. OAXI-EU uses
`CI_Grade = HIGH_ALGO`, which is not affected by this link.

## How the grades were produced (legacy grades; to be replaced)

**Status.** These are the *legacy* AXI grades. They are kept so that published
v4.0 results can be reproduced. They will be replaced in v4.1 by a documented,
fully automated grading pipeline (`itea.grading`; see `docs/grading/`).

**Procedure, as far as it is documented.**
- The grades come from the author's analysis of how existing technology
  performs each task in its professional context. The author reviewed the
  public technical specifications of business software and hardware vendors
  (for example, a CRM building a sales pipeline from the data entered by sales
  staff, or risk and pricing engines).
- The analysis then assessed how far generative and agentic AI, embedded in
  those tools, extend that support.
- The resulting judgements were applied to tasks **by technology pattern**.
  Each pattern carries fixed grades and fixed descriptive text, which is why
  the descriptive texts take only 5 distinct values.
- **The procedure that applied the patterns to the 47,810 task statements was
  not recorded.** It cannot be re-run.
- The grades classify **potential** impact. They do not measure deployed
  automation or realised transfers of knowledge.

**Forensic properties of the data:**
- identical task statements always receive identical grades on all four scales
  (6,451 repeated statements, no inconsistencies);
- the task's leading verb predicts the modal grade for about 95 % of tasks on
  `Auto_Grade` and `CI_Grade`.

**Reliability.** On a stratified 500-task sample, language models from four
providers, used as independent coders, agree with these grades as follows:
- `CI_Grade`: Krippendorff's α = 0.50 (moderate);
- `Auto_Grade`: α = 0.35 (insufficient).

A deterministic codebook based on the leading verb reproduces them with
weighted κ = 0.74 (CI) and 0.70 (Auto), out of sample in 5-fold
cross-validation. A July 2026 human panel (20 raters, 295 tasks, 0–3 codifiability scale) and
documented AI agents agree with each other (ρ = 0.39) but not with `CI_Grade`
(ρ = 0.08 and −0.01 to 0.04): task-level codifiability is not validated. Full
note: `docs/grading/AXI_PROVENANCE_EN.md`.
Treat the grades as a coarse ordinal signal for aggregation, not as
task-by-task truth.

Matching to O\*NET 30.2. The roll-up matches tasks to the current O\*NET
release by exact normalised text within each occupation; 23,890 of 47,810
tasks match (task statements were rewritten between releases). Every
O\*NET 30.2 occupation still receives shares through the Detailed Work
Activities it performs (see `src/itea/axi.py`).

## Licence and attribution

Released under **CC BY 4.0**. The task statements are from the O\*NET
database by the U.S. Department of Labor, Employment and Training
Administration (USDOL/ETA), used under CC BY 4.0 and modified here (grades
added). O\*NET® is a trademark of USDOL/ETA, which has not approved,
endorsed or tested these modifications.

SHA-256: `6b761d8fdcf654a2d724de217e0f9f5b149cf89e67830247608c86655176a5ed`
