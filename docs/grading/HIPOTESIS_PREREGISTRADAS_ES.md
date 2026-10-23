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

---

## Capa 2 (semántica ESCO): diseño e hipótesis H9–H13 (issue #1)

**Registradas el 23-10-2026, antes de calcular ningún *embedding*** con `scripts/grading/build_semantic.py`. El diseño queda fijado aquí; si cambia, se registra con fecha nueva.

### Diseño

1. **Textos.**
   - Cada tarea de O\*NET 30.2: el enunciado.
   - Cada concepto ESCO v1.2.1 (13.960): «preferredLabel. description».
2. **Modelo.** `sentence-transformers/all-mpnet-base-v2` (Apache-2.0), con la revisión fijada en los metadatos y vectores normalizados.
3. **Enlace.**
   - Para cada tarea se toman los **10 conceptos más similares** (coseno).
   - Se descartan los que quedan por debajo del **percentil 80** de todas esas similitudes, un umbral relativo como en Kogan et al.
   - Cada concepto pesa según su similitud.
4. **Grupos oficiales de ESCO** (pilar de competencias, nivel 1, más colecciones):
   - **social:** S1 (comunicación, colaboración y creatividad), S3 (asistencia y cuidados) y T4 (competencias sociales y de comunicación);
   - **manual:** S6 (manipular y mover), S7 (construir), S8 (manejar maquinaria y equipo especializado) y T5 (competencias físicas y manuales);
   - **informacional:** conocimientos (*skillType* = knowledge), S2 (competencias de información), S5 (trabajar con ordenadores), la colección digital de ESCO y T2 (competencias de pensamiento).
5. **Cálculo por tarea**, con proporciones ponderadas sobre los conceptos enlazados:
   - `K2 = (1 − proporción manual) × (1 − proporción social)`. Es el análogo semántico de la capa 1, que calcula `K = cognitivo × (1 − social)`.
   - `E2` = proporción informacional. Es el análogo de E1, que se basa en capacidades verbales, de razonamiento y cuantitativas.
   - Si una tarea no tiene ningún concepto por encima del umbral, K2 y E2 quedan vacíos y no se imputan.

### Hipótesis

| # | Hipótesis | Prueba | Umbral |
|---|---|---|---|
| H9 | E2 se correlaciona positivamente con la exposición humana de Eloundou | Spearman por tarea, IC por *bootstrap* de ocupaciones | ρ > 0 con IC que excluye el 0 |
| H10 | Combinar E1 y E2 (media de rangos) **mejora** la convergencia con Eloundou respecto a E1 solo | Igual | ρ > 0,43 (techo del IC de H1) |
| H11 | K2 **discrimina dentro de cada actividad** mucho más que K1 | Proporción de la varianza de K2 dentro de cada GWA | > 0,20 (K1: 0,053) |
| H12 | K2 se asocia al trabajo analítico no rutinario **dentro de cada Job Zone** | Spearman parcial por ocupación | ρ > 0 con IC que excluye el 0 |
| H13 | K2 predice la exposición humana descontando la cualificación | Spearman parcial por tarea | ρ > 0,10 con IC que excluye el 0 |

**Se informa además, sin hipótesis:** la correlación de K2 con el Job Zone y con K1, y la de E2 con E1.

**Interpretación prevista:**
- **Si H11 falla,** la capa semántica no aporta lo que justificaba hacerla, y habrá que revisar el enlace (k, umbral o modelo) con una hipótesis nueva y fechada.
- **Si H9 falla,** E2 no se usa en la combinación.

---

## Capa 2, variante B (cobertura completa): registro del 23-10-2026

**Registrada después de ver los resultados de la variante A** (`RESULTADOS_capa2_ES.md`) y **antes de ejecutar la B**. Es una respuesta declarada a un problema de cobertura (D18), no una búsqueda del mejor resultado. Si la B falla, se informa igual.

- **Cambio único:** para cada tarea se usan sus **5 conceptos más próximos**, sin umbral global, ponderados por similitud. Todo lo demás es igual que en la variante A: textos, modelo, grupos ESCO y fórmulas de K2 y E2.
- **Hipótesis:** las mismas H9–H13 con los mismos umbrales, ahora sobre todas las tareas (se llaman H9B–H13B).
- **Regla de uso:** la variante B sustituye a la A en la combinación solo si cumple **H11B, H12B y H13B**. E2 sigue fuera mientras H10B no se cumpla.

---

## Capa 3 (anclas *zero-shot* con NLI): diseño e hipótesis H14–H17 (issue #2)

**Registradas el 23-10-2026, antes de ejecutar** `scripts/grading/build_anchors.py`. Se conocen ya los resultados de las capas 1 y 2.

### Diseño

- **Modelo:** `MoritzLaurer/deberta-v3-large-zeroshot-v2.0-c` (MIT; la variante «-c» está entrenada solo con datos de uso comercial permitido), con la revisión fijada en los metadatos. Se ejecuta en local (MPS).
- **Cálculo:** la premisa es el enunciado de la tarea. Para cada grupo de anclas, la probabilidad de cada ancla es el *softmax* de los *logits* de implicación entre las anclas del grupo.
- **Anclas de exposición (E3).** Son paráfrasis de la rúbrica de Eloundou et al. (2024):
  - **e1:** «Using a large language model, this task could be done in half the time or less with the same quality.»
  - **e2:** «This task could be done much faster with a large language model only if it is combined with other software, such as tools to search documents, read images or run code.»
  - **e0:** «A large language model would not meaningfully reduce the time needed to do this task.»
  - **E3 = p(e1) + 0,5 · p(e2)**, análogo a la β de Eloundou.
- **Anclas de codificabilidad (K3).** Siguen la distinción entre información codificada y no codificada de Fernández-Macías y Bisello (2022):
  - **k1:** «The knowledge needed to decide how to do this task can be written down as explicit rules, procedures or data.»
  - **k0:** «Doing this task well depends on tacit experience, personal judgment or human interaction that cannot be written down as rules.»
  - **K3 = p(k1)**.

### Hipótesis

| # | Hipótesis | Prueba | Umbral |
|---|---|---|---|
| H14 | E3 se correlaciona con la exposición humana de Eloundou (+) | Spearman por tarea, IC por *bootstrap* de ocupaciones | ρ > 0 con IC que excluye el 0 |
| H15 | E1 + E2 + E3 (media de rangos) mejora la combinación E1 + E2 de la capa 2B | Igual | ρ > 0,476 (techo del IC de H10B) |
| H16 | K3 se asocia al trabajo analítico no rutinario dentro de cada Job Zone | Spearman parcial por ocupación | ρ > 0 con IC que excluye el 0 |
| H17 | K3 predice la exposición humana descontando la cualificación | Spearman parcial por tarea | ρ > 0,10 con IC que excluye el 0 |

**Se informa además:** la varianza de K3 dentro de cada GWA, y su correlación con K1, con K2 y con el Job Zone.

**Cautela declarada:** las anclas de E3 parafrasean la rúbrica que usaron los anotadores de Eloundou. Por eso H14 mide la fidelidad a esa rúbrica, no una validez independiente, y así se informará.

---

## Combinación (capa 5) y OAXI-EU v4.1: diseño e hipótesis H18–H20 (issue #4)

**Registradas el 23-10-2026, mientras se calcula la capa 3 y antes de conocer sus resultados.** Siguen las pautas del manual OCDE/JRC de indicadores compuestos.

### Qué componentes entran

Un componente entra solo si cumplió sus hipótesis de validación:

- **K1:** cumple H2, H6 y H8. Entra.
- **K2B:** cumple H11B, H12B y H13B. Entra.
- **K3:** entra si cumple H16 y H17.
- **E1:** cumple H1. Entra.
- **E2B:** cumple H9B y H10B. Entra.
- **E3:** entra si cumple H14 y H15.

### Cálculo central

1. Cada componente se normaliza a **rango percentil** sobre las 18.796 tareas.
2. **K y E** son la media, con pesos iguales, de los componentes que entran.
3. **OAXI-EU v4.1** se calcula con la cadena de la v4.0 (`itea.grading.rebuild`) y κ = 0,40 (D17).

### Incertidumbre (Monte Carlo, 1.000 réplicas, semilla 20261023)

En cada réplica se sortean cuatro decisiones del método:
- los pesos de los componentes, con una Dirichlet(1);
- la exclusión de un componente al azar, con probabilidad 0,5, siempre que quede al menos uno en K y otro en E;
- la normalización: rango o min-max;
- κ, uniforme entre 0,30 y 0,50.

**Se publican** la mediana y la banda del 5–95 % del índice y del rango de cada grupo ISCO, y la sensibilidad de primer orden a cada decisión (cociente de correlación η² sobre el rango).

### Hipótesis

| # | Hipótesis | Umbral |
|---|---|---|
| H18 | La E final converge con la exposición humana de Eloundou | ρ > 0,40, el valor de E1 sola |
| H19 | La K final se asocia al trabajo analítico no rutinario dentro de cada Job Zone | ρ parcial > 0, con IC que excluye el 0 |
| H20 | El orden de OAXI-EU v4.1 es robusto a las decisiones del método | La mediana de la amplitud de la banda 5–95 % del rango ISCO es menor de 100 puestos (de 428) |

**Se informa además, sin hipótesis:** la convergencia con el JRC (no es independiente, D17) y la comparación con OAXI-EU v4.0.
