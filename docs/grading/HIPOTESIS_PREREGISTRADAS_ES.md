# Hipótesis de validación escritas antes de ver los resultados

**Registradas el 23-10-2026, antes de ejecutar `scripts/grading/validate_structural.py` por primera vez.** No se modifican después; si se añaden hipótesis nuevas, se fechan aparte.

**Capa evaluada:** el prior estructural (capa 1) de `itea.grading`. K1 y E1 se calculan por tarea con las tablas oficiales de enlace de O\*NET 30.2.

| # | Hipótesis | Nivel | Prueba | Umbral de apoyo |
|---|---|---|---|---|
| H1 | E1 se correlaciona **positivamente** con la exposición humana de Eloundou et al. (β = E1 + 0,5·E2) | Tarea (Task ID común) | Spearman con IC del 95 % por *bootstrap* de ocupaciones | ρ > 0 y el IC excluye el 0 |
| H2 | K1 (media por ocupación) se correlaciona **positivamente con el trabajo analítico no rutinario** (Acemoglu y Autor, 2011), porque K incluye el conocimiento aprendible a partir de registros | Ocupación | Spearman con IC | ρ > 0 y el IC excluye el 0 |
| H3 | K1 se correlaciona **positivamente, pero menos que en H2**, con la rutina cognitiva (Acemoglu y Autor, 2011) | Ocupación | Spearman con IC | ρ > 0 |
| H4 | K1 **no equivale a la cualificación**: su correlación con el Job Zone no es casi perfecta | Ocupación | Spearman | \|ρ\| < 0,70 |
| H5 | El prior estructural **discrimina poco dentro de cada actividad general (GWA)**. Es el diagnóstico que justifica las capas 2–4 | Tarea | Proporción de la varianza de K1 dentro de cada GWA | Se espera < 0,20 (es un diagnóstico, no un éxito) |

**Interpretación prevista:**
- **Si H1 o H2 fallan:** la fórmula estructural se revisa (pesos y subgrupos de capacidades) y se documenta como resultado negativo.
- **Si H4 falla:** K1 estaría captando cualificación y no codificabilidad, lo que obliga a reformular.

---

## Hipótesis añadidas: validación discriminante de K (issue #3)

**Registradas el 23-10-2026, después de ver los resultados de H1–H5 y antes de ejecutar `scripts/grading/validate_discriminant.py` por primera vez.** Responden a dos lecturas de `RESULTADOS_capa1_ES.md`: el riesgo de que K sea la cualificación (H4) y el signo de la rutina cognitiva (H3). Como se escriben conociendo esos resultados, son confirmatorias solo respecto a los datos nuevos que usan; se declara así.

| # | Hipótesis | Nivel | Prueba | Umbral de apoyo |
|---|---|---|---|---|
| H6 | K1 se correlaciona con el trabajo analítico no rutinario **dentro de cada Job Zone**, es decir, no solo a través de la cualificación | Ocupación | Spearman parcial: los rangos se centran dentro de cada Job Zone; IC por *bootstrap* de ocupaciones. También ρ por Job Zone | ρ parcial > 0 con IC que excluye el 0, y ρ > 0 en al menos 4 de los 5 Job Zones |
| H7 | En las ocupaciones **no manuales** (grupos mayores SOC 11–29 y 41–43), K1 se correlaciona **positivamente** con la rutina cognitiva | Ocupación | Spearman con IC | ρ > 0 con IC que excluye el 0 |
| H8 | K1 tiene **validez incremental** sobre la cualificación: predice la exposición humana de Eloundou una vez controlado el Job Zone | Tarea | Spearman parcial dentro de cada Job Zone, IC por *bootstrap* de ocupaciones | ρ parcial > 0,10 con IC que excluye el 0 |

**Interpretación prevista:**
- **Si H6 falla:** K1 es en lo esencial la cualificación. Las capas 2–3 tendrán que aportar la discriminación, y el prior se documenta como insuficiente.
- **Si H7 falla:** la rutina cognitiva de Acemoglu y Autor no es un criterio de validez para K, ni siquiera en el trabajo de oficina. Se deja de usar como referencia y se explica por qué.
- **Si H8 falla:** el poder de K1 frente a Eloundou en H1 se debe al nivel de cualificación.
