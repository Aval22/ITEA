# Resultados: capa 2 (variante B), capa 3 y OAXI-EU v4.1

**Ejecución:** 23-10-2026, en local, en un Mac con GPU Apple (MPS). Las hipótesis se registraron antes de cada ejecución (`HIPOTESIS_PREREGISTRADAS_ES.md`).

## Capa 2, variante B (cobertura completa)

Se usan los 5 conceptos ESCO más próximos de cada tarea, sin umbral global. La variante se registró tras ver que la A dejaba el 46 % de las tareas sin enlazar.

| # | Resultado | Veredicto |
|---|---|---|
| H9B: E2 ↔ Eloundou | ρ = 0,28 [0,26; 0,30] | Se cumple |
| H10B: E1+E2 > 0,43 | ρ = 0,45 [0,43; 0,48] | Se cumple |
| H11B: varianza de K2 dentro de cada GWA > 0,20 | 0,68 (K1: 0,05) | Se cumple |
| H12B: K2 ↔ trabajo analítico, neto del Job Zone | 0,20 [0,13; 0,27] | Se cumple |
| H13B: K2 ↔ Eloundou, neto del Job Zone (> 0,10) | 0,24 [0,22; 0,26] | Se cumple |

**Informativo:**
- Cobertura: 18.796 tareas (100 %).
- K2 ↔ Job Zone: 0,49 (K1: 0,70).
- K2 ↔ K1: 0,47.
- E2 ↔ E1: 0,11.

**Consecuencia:** según la regla registrada, la variante B sustituye a la A, y E2 entra en la combinación.

## Capa 3 (anclas *zero-shot* con NLI)

**Modelo:** `MoritzLaurer/deberta-v3-large-zeroshot-v2.0-c`, revisión `b2730f16`. Tardó 51 minutos para las 18.796 tareas.

| # | Resultado | Veredicto |
|---|---|---|
| H14: E3 ↔ Eloundou (+) | ρ = **−0,07** [−0,09; −0,05] | **No se cumple** |
| H15: E1+E2+E3 > 0,476 | 0,36 | **No se cumple** (empeora) |
| H16: K3 ↔ trabajo analítico, neto del Job Zone | 0,05 [−0,02; 0,11] | **No se cumple** |
| H17: K3 ↔ Eloundou, neto del Job Zone (> 0,10) | 0,096 [0,08; 0,11] | **No se cumple** |

**Lectura:**
- **No es un fallo de programación.** La etiqueta de implicación es la correcta, y K3 ordena con sentido los casos claros: preparar presupuestos, 0,86; reunirse con el consejo, 0,23.
- **E3 apenas varía** (desviación típica 0,05). Las anclas de exposición son largas y una va en negativo, algo que los modelos NLI resuelven mal.
- **K3 discrimina dentro de cada actividad** (82 % de su varianza), pero no converge con las referencias.
- **Según la regla registrada, ni K3 ni E3 entran en el índice** (D20). Rediseñar las anclas sería una hipótesis nueva, con su propio registro.

## OAXI-EU v4.1

**Componentes:** K = K1 + K2 y E = E1 + E2, en rangos percentiles con pesos iguales; κ = 0,40 (D17).
**Monte Carlo:** 1.000 réplicas, semilla 20261023.
**Salidas:** `oaxi_eu_v41.csv`, con la mediana y la banda 5–95 % del índice y del puesto; `oaxi_eu_v41.meta.json`; `task_grades_v41.csv`.

| # | Hipótesis | Resultado | Veredicto |
|---|---|---|---|
| H18 | La E final ↔ Eloundou, por encima de 0,40 | ρ = 0,454 [0,431; 0,476] | Se cumple |
| H19 | La K final ↔ trabajo analítico, neta del Job Zone | 0,26 [0,19; 0,33] | Se cumple |
| H20 | Mediana de la banda 5–95 % del puesto ISCO < 100 | 66 puestos | Se cumple |

**Informativo:**
- **Convergencia con el JRC:** Pearson 0,81 y Spearman 0,82. No es una validación independiente (D17).
- **Respecto a OAXI-EU v4.0 (AXI):** Spearman 0,80; comparten 12 de los 20 primeros grupos.
- **Sensibilidad del puesto a cada decisión** (η² medio):

  | Decisión | η² |
  |---|---|
  | Qué componentes de E entran | 0,57 |
  | Peso de E1 | 0,16 |
  | Qué componentes de K entran | 0,12 |
  | Normalización | 0,03 |
  | Peso de K1 | 0,03 |
  | κ | 0,02 |

  Con 1.000 réplicas, el sesgo al alza de η² por tramos es menor de 0,01.

**Lectura:**
1. **La mayor fuente de incertidumbre es la exposición.** E1 (capacidades) y E2 (ESCO) casi no se parecen (ρ = 0,11), y el puesto de un grupo depende mucho de si entra una u otra. Es el punto más débil de la v4.1, y se declara así.
2. **El índice se reordena de forma creíble.** Arriba quedan bases de datos, estadística, software, análisis financiero y nóminas; abajo, la construcción y la limpieza.
3. **Una limitación del crosswalk:** algunos grupos ISCO reciben exactamente la misma puntuación porque proceden de la misma ocupación estadounidense. Es el caso de los tenderos (5221) y los gerentes de comercio (1420), que además tienen una banda de incertidumbre muy amplia (puestos 3–205). El remedio son los pesos de empleo por país.
