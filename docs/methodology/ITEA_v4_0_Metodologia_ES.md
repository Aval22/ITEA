---
title: "Marco ITEA — Metodología v4.0"
subtitle: "OAXI-EU sobre el eje ISCO-08 y graduación de tareas v4.1 (en desarrollo)"
author: "Alberto García-Lluis Valencia"
date: "23 de octubre de 2026"
lang: es
---

# 1. Alcance de este documento

Este documento es la **referencia metodológica de la versión 4.0** de ITEA. No sustituye a la *Metodología consolidada v3.0* (`docs/ITEA_v3_0_Consolidated_Methodology.docx`), sino que la amplía:

- **Se mantiene sin cambios:** los diez indicadores de la v3.0 sobre O\*NET 30.2 (ITEA, IRA, ICT, IFS, IPI, IEF, GEE, IMO, OAEI y AEI) y sus fórmulas. Se citan aquí solo en lo que afecta a la v4.0.
- **Se añade:**
  - el índice europeo **OAXI-EU** sobre el eje ISCO-08 (§3);
  - la arquitectura reproducible del software (§4);
  - el programa de **graduación de tareas v4.1** (§5), que sustituirá la entrada del índice.

Todo lo que se describe se reproduce desde fuentes públicas con el paquete `itea-framework` (repositorio `Aval22/ITEA`).

# 2. Qué mide ITEA

ITEA mide la **expropiabilidad algorítmica**: el potencial de que el conocimiento que usa un trabajador quede incorporado a los sistemas de la empresa. El marco separa tres planos:

- **Exposición:** qué parte del trabajo puede alcanzar la IA.
- **Expropiabilidad:** el potencial de captura, que exige a la vez exposición y conocimiento codificable.
- **Expropiación:** el hecho normativo, es decir, la pérdida de la soberanía del trabajador sobre la explotación de su saber. No se mide directamente.

Todos los índices de ITEA miden un **potencial**: qué ocupaciones tienen el conocimiento más abierto a la codificación. **No** miden automatización realizada ni transferencias efectivas de valor.

# 3. OAXI-EU: índice europeo de expropiabilidad

## 3.1 Entradas

- **Grados de tareas (AXI, heredados).** Son 47.810 enunciados de tareas de O\*NET 29.1 con cuatro escalas ordinales: automatización, codificabilidad (`CI_Grade`), impacto de la IA generativa e impacto de la IA agéntica. Proceden de un análisis de las especificaciones técnicas de fabricantes de software y hardware de negocio, aplicado por patrón tecnológico. Su documentación está en `src/itea/data/README_AXI.md`, y su fiabilidad frente a codificadores independientes es moderada en codificabilidad (α = 0,50) e insuficiente en automatización (α = 0,35). En la v4.1 se sustituyen (§5).
- **O\*NET 30.2:** tareas y enlaces de las tareas con las actividades de trabajo detalladas (DWA).
- **Crosswalks oficiales del BLS:** SOC 2018 → SOC 2010 y SOC 2010 → ISCO-08.

## 3.2 Agregación

1. **De tarea a actividad.** Cada enunciado AXI se empareja con la tarea de O\*NET 30.2 por su texto normalizado dentro de la ocupación. Coinciden 23.890 de las 47.810 tareas, porque O\*NET reescribió muchos enunciados entre versiones. Cada actividad (DWA) recibe la proporción de sus tareas con grado alto.
2. **De actividad a ocupación.** Cada una de las 923 ocupaciones de O\*NET-SOC recibe la media de las actividades que realiza. Así, también reciben valor las ocupaciones sin tareas coincidentes.
3. **De ocupación a ISCO-08.** La cadena oficial SOC 2018 → SOC 2010 → ISCO-08 es de muchos a muchos. Se reparte con pesos iguales, y opcionalmente con pesos de empleo. Resultado: **428 grupos primarios ISCO-08**.

## 3.3 Índice

Para cada grupo ISCO:

- **E** es la proporción de actividades con impacto alto de la IA generativa.
- **K** es la proporción de actividades con conocimiento codificable algorítmicamente (`CI_Grade = HIGH_ALGO`).
- Ambas se normalizan con min-max.

$$\text{núcleo} = E^{\,1-\kappa}\cdot K^{\,\kappa}, \qquad \text{OAXI-EU} = 1 + 99\cdot \text{minmax}(\text{núcleo})$$

**Por qué la forma geométrica:** la expropiabilidad exige a la vez exposición y codificabilidad, así que una ocupación sin una de las dos no puede puntuar alto.

**Valor de κ:** se fija en **0,40**, el valor que maximiza la convergencia con un índice externo independiente. El óptimo es plano entre 0,3 y 0,4, y la tabla de calibración se reproduce con `itea.kappa_grid`.

## 3.4 Validación

- **Convergencia con el índice de exposición a la IA del JRC** (JRC145832; Casas et al., 2026, tabla M.1, CC BY 4.0), a tres dígitos ISCO: **Pearson 0,736 y Spearman 0,819** sobre 127 grupos. La reproducen `itea validate` y los tests.
- **Cautela:** el índice del JRC se basa en capacidades. Es independiente de los grados AXI, pero no de la capa estructural de la v4.1, que también usa capacidades (§5). Por eso, para validar K en la v4.1 no se usa el JRC.

## 3.5 Cambios respecto a la versión beta

- **Crosswalk.** El mapeo uno a uno, tecleado en una hoja salarial, asignaba mal algunas ocupaciones y dejaba 48 grupos ISCO profesionales sin datos. Se sustituye por las tablas oficiales del BLS.
- **Cobertura.** La beta restringía el índice a las 784 ocupaciones con datos de empleo. Ahora se usan las 923 ocupaciones y se llega a 428 grupos ISCO (antes, 237).

# 4. Software y reproducibilidad

| Componente | Función |
|---|---|
| `itea fetch` | Descarga O\*NET 30.2 y los crosswalks del BLS, y verifica su SHA-256 |
| `itea build-eu` | Construye OAXI-EU y guarda los *hash* de entradas y salidas (`oaxi_eu.meta.json`) |
| `itea validate` | Calcula la convergencia con el índice del JRC empaquetado |
| `itea.rollup` | Lleva cualquier puntuación por tarea (identificada por su Task ID de O\*NET) a actividades, ocupaciones e ISCO-08 |
| `itea.v3` | Indicadores de la v3.0. La CI comprueba que reproducen la implementación R de referencia |
| `itea.grading` | Graduación de tareas v4.1 (§5) |

- **Pruebas:** la integración continua ejecuta los tests en Python 3.10, 3.12 y 3.13; además instala el paquete en limpio y comprueba la paridad entre R y Python.
- **Salidas de referencia:** los CSV de `v4.0/outputs/`.
- **Libro Excel:** `data/processed/ITEA_v4_0_Workbook.xlsx` es una copia de lectura de esas salidas, generada con `scripts/build_workbook_v4.py`.

# 5. Graduación de tareas v4.1 (en desarrollo)

## 5.1 Por qué se rehace la graduación

Los grados AXI no tienen un procedimiento reproducible tarea a tarea, tienen pocos valores distintos y su fiabilidad es baja en automatización. La v4.1 los sustituye por una graduación automática y documentada de las **18.796 tareas de O\*NET 30.2**, con estos principios:

- **Solo fuentes oficiales para construir:** las tablas de enlace de O\*NET y ESCO.
- **Referencias independientes para validar,** que nunca se usan para construir.
- **Hipótesis registradas antes de cada ejecución.**
- **Ningún grado se entrena con AXI.**

## 5.2 Seis componentes

| Pieza | Pregunta | Nivel |
|---|---|---|
| **K** (codificabilidad) | ¿El conocimiento de la tarea puede expresarse en reglas o aprenderse a partir de registros? | Tarea |
| **E** (exposición a la IA generativa) | ¿Puede la IA generativa producir el resultado principal o reducir mucho su tiempo? | Tarea |
| **T** (mediación tecnológica) | ¿Hay tecnología, documentada por su fabricante, que apoye o automatice la tarea? | Tarea × tecnología |
| **U** (utilización efectiva) | ¿Cuánto de esa tecnología se adopta y se usa? | Sector × país |
| **S** (solvencia técnica certificable) | ¿Hay una certificación que acredite la competencia? | Tarea × tecnología |
| **C** (factibilidad económica) | ¿Compensa económicamente? | Ocupación × país |

## 5.3 Estado y resultados

- **Capa 1 (estructural), hecha.**
  - Cálculo: `K_GWA = proporción cognitiva × (1 − proporción social)` y `E_GWA` = proporción de capacidades verbales, de razonamiento y cuantitativas, ambas desde las tablas *Abilities* y *Skills to Work Activities* de O\*NET; se propagan a cada tarea por sus DWA.
  - Validación: E converge con las etiquetas humanas de Eloundou et al. (2024) (ρ = 0,40), y K con el trabajo analítico no rutinario (ρ = 0,67, y 0,28 dentro de cada Job Zone).
  - K predice la exposición humana descontando la cualificación (ρ parcial = 0,40).
  - Hipótesis que fallaron: la rutina cognitiva va en sentido contrario, también en ocupaciones no manuales, y se abandona como referencia; la correlación con el Job Zone (0,70) quedó al límite.
- **Capa U, hecha:** adopción de ERP, CRM, inteligencia de negocio e IA por país y sector NACE (Eurostat, 35 territorios × 13 sectores). La profundidad de uso es un supuesto declarado: 0,10, 0,27 o 0,35. Estas tablas no cubren el sector financiero.
- **Capa T, inventario hecho:** 8.785 productos de software por ocupación (O\*NET *Technology Skills*). El piloto será en finanzas y consultoría.
- **Capa 2 (semántica), hecha:** cada tarea se enlaza con sus 5 conceptos ESCO más próximos mediante *embeddings* (all-mpnet-base-v2, en local). El 68 % de la varianza de K2 está dentro de cada actividad (el 5 % en K1), y K2 está menos ligada a la cualificación (ρ = 0,49 con el Job Zone).
- **Capa 3 (anclas NLI), resultado negativo:** no supera sus cuatro hipótesis y no se usa.
- **OAXI-EU v4.1, construido:**
  - componentes: K = K1 + K2 y E = E1 + E2;
  - incertidumbre: Monte Carlo de 1.000 réplicas, con una banda del 5–95 % por grupo (mediana: 66 de 428 puestos);
  - validación: la E final frente a Eloundou da ρ = 0,45, y la K final frente al trabajo analítico, dentro de cada Job Zone, da 0,26;
  - respecto al índice v4.0: Spearman 0,80. La mayor incertidumbre procede de E, cuyas dos fuentes coinciden poco.
- **Pendiente:** capas T, S y C.

**Detalle completo:** `docs/grading/` (metodología, registro de decisiones, hipótesis y resultados).

# 6. Limitaciones

1. **OAXI-EU v4.0 hereda las limitaciones de los grados AXI** (§3.1). Sus resultados deben leerse como provisionales hasta la reconstrucción con la v4.1.
2. **Pérdida de tareas entre versiones.** Solo la mitad de los enunciados AXI coincide con O\*NET 30.2. La agregación por actividades da valor a todas las ocupaciones, pero con menos tareas propias.
3. **Pesos iguales en el crosswalk.** Hay pesos de empleo disponibles como opción.
4. **El índice del JRC no es un criterio independiente para K** en la v4.1 (§3.4).
5. **Todos los índices miden un potencial,** no hechos realizados.

# Referencias

- Acemoglu, D. y Autor, D. (2011). Skills, tasks and technologies: Implications for employment and earnings. *Handbook of Labor Economics*, 4B, 1043–1171.
- Casas, P., Fernández-Macías, E., Martínez-Plumed, F., Gómez, E., González-Vázquez, I. y Salotti, S. (2026). *Revisiting the occupational impact of AI in the generative AI era*. JRC145832, Comisión Europea.
- Eloundou, T., Manning, S., Mishkin, P. y Rock, D. (2024). GPTs are GPTs: Labor market impact potential of LLMs. *Science*, 384(6702), 1306–1308.
- Fernández-Macías, E. y Bisello, M. (2022). A comprehensive taxonomy of tasks for assessing the impact of new technologies on work. *Social Indicators Research*, 159, 821–841.
- National Center for O\*NET Development (2026). *O\*NET 30.2 Database*. USDOL/ETA, CC BY 4.0.
- OCDE y JRC (2008). *Handbook on Constructing Composite Indicators: Methodology and User Guide*. OCDE.
