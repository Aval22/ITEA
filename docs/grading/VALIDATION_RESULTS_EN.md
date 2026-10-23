# Validation of `itea.grading`: hypotheses and results

English summary of `HIPOTESIS_PREREGISTRADAS_ES.md`, `RESULTADOS_capa1_ES.md`, `RESULTADOS_discriminante_ES.md` and `RESULTADOS_capaU_ES.md`. The Spanish files are the record of reference, because they were written and dated before each run.

**Data:**
- O\*NET 30.2;
- Eloundou et al. (2024) human labels, commit `0471612`.

**Confidence intervals:** 95 %, from a bootstrap that resamples occupations (1,000 draws, seed 20261023).

## Registration

| Run | Hypotheses | Registered | Script |
|---|---|---|---|
| Structural layer | H1–H5 | 23-10-2026, before the first run | `scripts/grading/validate_structural.py` |
| Discriminant validity | H6–H8 | 23-10-2026, after seeing H1–H5 and before running H6–H8 | `scripts/grading/validate_discriminant.py` |

H6–H8 were written in response to H3 and H4. They are confirmatory only for the new comparisons they test, and they are declared as such.

## Results

| # | Hypothesis | Result | n | Verdict |
|---|---|---|---|---|
| H1 | E1 correlates positively with Eloundou human exposure (β = E1 + 0.5·E2) | ρ = 0.40 [0.38, 0.43] | 18,739 tasks | Supported |
| H2 | K1 correlates positively with non-routine analytical work (Acemoglu & Autor, 2011) | ρ = 0.67 [0.64, 0.71] | 894 occupations | Supported |
| H3 | K1 correlates positively, but less than in H2, with routine cognitive work | ρ = −0.21 [−0.27, −0.15] | 894 occupations | **Not supported** (opposite sign) |
| H4 | \|K1 vs Job Zone\| < 0.70 | ρ = 0.70 [0.66, 0.73] | 923 occupations | Borderline |
| H5 | Within-GWA share of K1 variance < 0.20 (diagnostic) | 0.053 | 18,796 tasks | As expected: layer 1 does not discriminate within activities |
| H6 | K1 vs non-routine analytical, net of Job Zone; positive within each Job Zone | partial ρ = 0.28 [0.22, 0.35]; JZ2 0.14, JZ3 0.33, JZ4 0.27, JZ5 0.45 | 894 occupations | Supported |
| H7 | K1 vs routine cognitive is positive in non-manual occupations (SOC 11–29, 41–43) | ρ = −0.21 [−0.29, −0.13] | 518 occupations | **Not supported** |
| H8 | K1 predicts Eloundou human exposure net of Job Zone (partial ρ > 0.10) | partial ρ = 0.40 [0.38, 0.42] | 18,739 tasks | Supported |

**Deviation from registration.** H6 asked for a positive correlation in "at least 4 of the 5 Job Zones". O\*NET 30.2 assigns no occupation to Job Zone 1, so the criterion was applied to the 4 Job Zones that exist, and it holds in all of them.

## Reading

1. **K is not skill level in disguise (H6, H8).** Among occupations at the same skill level, K1 still orders them by analytical content and still predicts human-rated AI exposure. The 0.70 correlation with Job Zone reflects co-movement, not identity.

2. **Routine cognitive content is not a validity criterion for K (H3, H7).** The Work Context items behind the index capture the importance of repetition, of exactness and of not structuring one's own work: lack of autonomy, not explicitness of knowledge. The index is dropped as a reference (decision D15), and both failures are reported.

3. **Layers 2–3 are still needed (H5).** The structural prior has too little variance within activities to grade individual tasks.

## Layer U (adoption by sector and country)

- **Source and coverage:** Eurostat ICT survey, enterprises with 10+ employees, latest year per cell (2023–2025); 35 territories and 13 NACE sectors. The financial sector (NACE K) is not covered.
- **Outputs:** `v4.0/outputs/grading/utilisation_by_sector.csv`, with U = adoption × depth for depth 0.10, 0.27 and 0.35.
- **Spain against the EU-27:** Spain is above the EU-27 average in ERP adoption in every sector covered, but not in AI adoption, except in real estate and transport.
