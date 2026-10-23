# Resultados de la capa 2 (semántica ESCO) frente a las hipótesis H9–H13

**Ejecución:** 23-10-2026, en local, en un Mac con GPU Apple (MPS):
- `scripts/grading/build_semantic.py`: 210 s de cálculo de *embeddings*;
- `scripts/grading/validate_semantic.py`.

**Modelo:** `sentence-transformers/all-mpnet-base-v2`, revisión `e8c3b32edf5434bc2275fc9bab85f82640a19130`.

**Diseño:** el registrado antes de la ejecución:
- los 10 conceptos ESCO más próximos a cada tarea;
- un umbral global en el percentil 80 de esas similitudes (coseno ≥ 0,697).

**Salidas** en `v4.0/outputs/grading/`:
- `task_semantic.csv`, `task_esco_links.csv.gz` y `task_semantic.meta.json`;
- `validation_semantic.json`.

## Cobertura

Con el umbral registrado, **10.220 de las 18.796 tareas (54 %) tienen al menos un concepto ESCO enlazado.** Las demás quedan sin K2 ni E2. La cobertura no es homogénea: es más baja en derecho (SOC 23: 28 %) e informática (SOC 15: 39 %), y más alta en servicios personales y sanidad (en torno al 62–69 %). Todos los resultados de abajo se refieren a las tareas enlazadas.

## Resultados

| # | Hipótesis | Resultado | n | Veredicto |
|---|---|---|---|---|
| H9 | E2 ↔ exposición humana de Eloundou (+) | ρ = **0,19** [0,17; 0,22] | 10.195 tareas | **Se cumple** |
| H10 | E1 + E2 mejora la convergencia de E1: ρ > 0,43 | ρ = **0,40** [0,38; 0,43] | 10.195 | **No se cumple** |
| H11 | Varianza de K2 dentro de cada GWA > 0,20 | **0,75** (K1, mismas tareas: 0,07) | 10.220 | **Se cumple** |
| H12 | K2 ↔ trabajo analítico no rutinario, neto del Job Zone (+) | ρ parcial = **0,19** [0,12; 0,25] | 890 ocupaciones | **Se cumple** |
| H13 | K2 ↔ exposición humana, neta del Job Zone (> 0,10) | ρ parcial = **0,18** [0,16; 0,20] | 10.195 | **Se cumple** |

**Fuera de las hipótesis (informativo):**
- **Correlaciones de la capa 2:** K2 ↔ Job Zone: ρ = 0,41, frente a 0,70 de K1. K2 ↔ K1, por tarea: 0,37. E2 ↔ E1, por tarea: 0,04.
- **E1 en las mismas tareas enlazadas:** ρ = 0,39. La combinación mejora solo 0,016.

## Lectura

1. **La capa 2 hace lo que se buscaba en K.** Discrimina entre tareas de una misma actividad: el 75 % de su varianza está dentro de cada GWA, frente al 7 % de K1. Está mucho menos ligada a la cualificación (0,41 frente a 0,70), y aun así conserva la relación con el trabajo analítico y con la exposición humana descontando la cualificación.
2. **Para E, la capa 2 aporta poco.** E2 converge con el juicio humano (0,19), pero menos que E1, y casi no se parece a E1 (0,04). Combinadas no superan el umbral registrado. Según lo previsto, E2 no entra en la combinación como estaba planteada. La exposición queda pendiente de la capa 3, con anclas tomadas de la rúbrica de Eloundou.
3. **La cobertura es el problema principal.** Con un umbral global, el 46 % de las tareas queda sin enlazar, y precisamente en ocupaciones de conocimiento como el derecho o la informática. Aunque las hipótesis se cumplan, la capa 2 no puede usarse para el índice tal cual. Cualquier cambio del umbral es un **diseño nuevo** y se registra con fecha antes de ejecutarlo (decisión D18).
