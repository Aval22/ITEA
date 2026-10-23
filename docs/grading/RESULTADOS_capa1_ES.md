# Resultados de la capa 1 (prior estructural) frente a las hipótesis registradas

**Ejecución:** 23-10-2026, `scripts/grading/validate_structural.py`, con O\*NET 30.2 y las etiquetas de Eloundou et al. (commit `0471612`).
**Salidas:** `v4.0/outputs/grading/` (`gwa_scores.csv`, `task_prior_structural.csv`, `validation_structural.json`).
**Intervalos de confianza:** del 95 %, por *bootstrap* de ocupaciones (1.000 réplicas, semilla 20261023).

| # | Hipótesis | Resultado | n | Veredicto |
|---|---|---|---|---|
| H1 | E1 ↔ exposición humana de Eloundou (+) | ρ = **0,40** [0,38; 0,43] | 18.739 tareas, 923 ocupaciones | **Se cumple** |
| H2 | K1 ↔ trabajo analítico no rutinario (+) | ρ = **0,67** [0,64; 0,71] | 894 ocupaciones | **Se cumple** |
| H3 | K1 ↔ rutina cognitiva (+, más débil que H2) | ρ = **−0,21** [−0,27; −0,15] | 894 ocupaciones | **No se cumple:** el signo es contrario |
| H4 | \|K1 ↔ Job Zone\| < 0,70 | ρ = **0,70** [0,66; 0,73] | 923 ocupaciones | **Al límite:** el valor puntual está justo por debajo, pero el IC incluye 0,70 |
| H5 | Varianza de K1 dentro de cada GWA < 0,20 (diagnóstico) | **0,053** | 18.796 tareas | **Como se esperaba**: la capa 1 no discrimina dentro de cada actividad |

**Fuera de las hipótesis (informativo):**
- K1 ↔ exposición humana de Eloundou: ρ = 0,49 [0,47; 0,51];
- E1 ↔ trabajo analítico no rutinario: ρ = 0,64 [0,60; 0,67];
- K1 toma 355 valores distintos.

## Lectura

1. **Validez convergente de E (H1).** Un prior construido solo con las tablas oficiales de O\*NET, sin leer los enunciados, ya converge de forma moderada con un juicio humano independiente. Es una base razonable, que las capas semánticas tendrán que mejorar.

2. **K capta el conocimiento analítico aprendible a partir de registros (H2).** Era la predicción teórica distintiva, y se sostiene: K no es una medida de rutina.

3. **La rutina cognitiva va en sentido contrario (H3).** El índice de Acemoglu y Autor combina la repetición, la exactitud y la poca libertad para fijar tareas. Esas propiedades también son altas en ocupaciones de producción y de operación de máquinas, donde K es bajo por su componente físico. **K y la rutina cognitiva son constructos distintos**, que es lo que queríamos demostrar en H2, pero la hipótesis H3 tal como se escribió no se cumple, y se informa como tal. Para la próxima versión, la comparación adecuada es con la rutina cognitiva **dentro de las ocupaciones no manuales**. Esa nueva hipótesis se registrará con su propia fecha.

4. **El riesgo de confundir K con la cualificación (H4) es real.** La correlación con el Job Zone (0,70) está en el umbral. Las capas 2–4 (ESCO y anclas) y los análisis de K dentro de cada Job Zone deberán demostrar que K aporta algo más que el nivel de cualificación. Es la amenaza principal a la validez discriminante.

5. **Hacen falta las capas siguientes (H5).** Solo el 5,3 % de la varianza de K1 está dentro de cada actividad general. Sin las capas semánticas, la medida repetiría el problema de AXI: pocos valores y poca discriminación entre tareas parecidas.

## Implicaciones para el diseño
- La fórmula estructural se mantiene como prior; no se ajusta a la vista de estos resultados.
- Se añaden dos análisis obligatorios: K dentro de cada Job Zone (discriminante) y la rutina cognitiva solo en ocupaciones no manuales (hipótesis nueva, fechada).
- Las capas 2 y 3 se evaluarán por su aumento de la varianza dentro de cada actividad y por la mejora sobre H1.
