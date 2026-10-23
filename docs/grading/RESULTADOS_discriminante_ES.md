# Resultados de la validación discriminante de K (issue #3)

**Ejecución:** 23-10-2026, `scripts/grading/validate_discriminant.py`, sobre O\*NET 30.2 y las etiquetas de Eloundou et al. (commit `0471612`).
**Hipótesis:** H6–H8, registradas antes de esta ejecución (`HIPOTESIS_PREREGISTRADAS_ES.md`).
**Salida:** `v4.0/outputs/grading/validation_discriminant.json`.
**Intervalos de confianza:** del 95 %, por *bootstrap* de ocupaciones (1.000 réplicas, semilla 20261023).

| # | Hipótesis | Resultado | n | Veredicto |
|---|---|---|---|---|
| H6 | K1 ↔ trabajo analítico no rutinario, neto del Job Zone | ρ parcial = **0,28** [0,22; 0,35] | 894 ocupaciones | **Se cumple** |
| H6 (por Job Zone) | ρ > 0 en cada Job Zone | JZ2 0,14 [0,03; 0,25] · JZ3 0,33 [0,19; 0,46] · JZ4 0,27 [0,14; 0,39] · JZ5 0,45 [0,30; 0,57] | 151–324 por Job Zone | **Se cumple** en los 4 Job Zones que existen (ver la desviación) |
| H7 | K1 ↔ rutina cognitiva en ocupaciones no manuales (+) | ρ = **−0,21** [−0,29; −0,13] | 518 ocupaciones | **No se cumple:** el signo es contrario |
| H8 | K1 ↔ exposición humana de Eloundou, neta del Job Zone | ρ parcial = **0,40** [0,38; 0,42] | 18.739 tareas | **Se cumple** |

**Fuera de las hipótesis (informativo):** E1 ↔ Eloundou, neta del Job Zone: ρ parcial = 0,29 [0,26; 0,31].

**Desviación del registro:** la hipótesis H6 pedía resultados en «4 de los 5 Job Zones», pero O\*NET 30.2 no asigna ninguna ocupación al Job Zone 1. El criterio se aplica, por tanto, a los 4 Job Zones existentes, y se cumple en todos. El error está en el registro, no en los datos, y se deja escrito.

## Lectura

1. **K no es la cualificación disfrazada (H6 y H8).** Al comparar ocupaciones del mismo nivel de cualificación, K1 sigue ordenándolas según su contenido analítico, y sigue prediciendo la exposición humana a la IA. La correlación de 0,70 con el Job Zone (H4) refleja, por tanto, que la cualificación y el conocimiento codificable van juntos, pero K aporta información propia. Así se reduce la amenaza principal que señalaba `RESULTADOS_capa1_ES.md`.

2. **La rutina cognitiva no es un criterio de validez para K (H7).** El signo negativo se mantiene incluso en el trabajo no manual. Las variables de Work Context que forman el índice (importancia de la repetición, de la exactitud y de no poder estructurar el propio trabajo) miden la **falta de autonomía**, no la explicitud del conocimiento. Una tarea puede ser repetitiva y depender de criterio, o variada y estar plenamente documentada. Como prevé el registro, se deja de usar este índice como referencia de K y se explica en la metodología. Es un resultado negativo y se publica.

3. **Lo que sigue:** las capas semánticas (2–3) se evaluarán también con H6 y H8, para comprobar que no aumentan la dependencia de la cualificación.
