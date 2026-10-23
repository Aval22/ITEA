# Metodología de graduación de tareas de ITEA v4.1, versión 0.2

**23-10-2026.** Documento consolidado. Sustituye como referencia a `LIBRO_CRITERIOS_v0.1_ES.md` (capas K y E) y a `DISENO_capa_tecnologica_y_certificacion_v0.1_ES.md` (capas T, U y S), que se conservan como historial. Las decisiones están en `DECISIONES_ES.md`, la justificación bibliográfica en `INFORME_investigacion_2026-10-23.md`, la procedencia de AXI en `PROCEDENCIA_AXI_ES.md`, y los resultados en `RESULTADOS_capa1_ES.md`, `RESULTADOS_discriminante_ES.md` y `RESULTADOS_capaU_ES.md`. Hay versión en inglés: `METHODOLOGY_v0.2_EN.md` y `VALIDATION_RESULTS_EN.md`.

## 1. Qué se mide

ITEA mide la **expropiabilidad algorítmica**: el potencial de que el conocimiento que usa un trabajador quede incorporado a sistemas de la empresa. Se descompone en seis piezas, cada una con su fuente.

| Pieza | Pregunta | Nivel | Estado |
|---|---|---|---|
| **K** (codificabilidad) | ¿El conocimiento de la tarea puede expresarse en reglas o aprenderse a partir de registros? | Tarea | Capa 1 hecha; capas 2–3 pendientes |
| **E** (exposición a la IA generativa) | ¿Puede la IA generativa producir el resultado principal de la tarea o reducir mucho su tiempo? | Tarea | Capa 1 hecha; capas 2–3 pendientes |
| **T** (mediación tecnológica) | ¿Hay tecnología, documentada por su fabricante, que apoye o automatice la tarea en esta ocupación? | Tarea × tecnología | Inventario hecho; corpus pendiente |
| **U** (utilización efectiva) | ¿Cuánto de esa tecnología se adopta y se usa realmente? | Sector × país | Adopción (Eurostat) descargada; profundidad como supuesto (0,10–0,35) |
| **S** (solvencia técnica certificable) | ¿Existe una certificación que acredite la competencia necesaria? | Tarea × tecnología | Pendiente |
| **C** (factibilidad económica) | ¿Compensa económicamente y cuánta reorganización exige? | Ocupación × país | Pendiente (capa posterior) |

**Las piezas no se mezclan.** K y E son propiedades de la tarea, T y S de su entorno tecnológico, y U y C de su realización. La expropiabilidad potencial es K × E. La realizable añade T × U, y la brecha de solvencia es T × (1 − S).

## 2. Unidad y fuentes

- **Unidad:** las 18.796 tareas de O\*NET 30.2, por su Task ID oficial.
- **Fuentes de construcción, todas públicas:**
  - O\*NET 30.2: tareas, enlaces con DWA, IWA y GWA, tablas de capacidades y habilidades por actividad, *Technology Skills* y *Tools Used*;
  - ESCO v1.2.1 (habilidades, tipos, grupos, transversales, DigComp);
  - documentación pública de fabricantes (para T);
  - programas públicos de certificación (para S);
  - Eurostat (para U).
- **Fuentes de validación, que nunca se usan para construir:**
  - las etiquetas humanas de exposición de Eloundou et al. (2024, MIT, 18.739 tareas comunes);
  - el Anthropic Economic Index;
  - los índices de tareas de Acemoglu y Autor (2011);
  - el Job Zone;
  - JRC145832 (solo para OAXI-EU, no para K).

## 3. Capas de construcción de K y E

| Capa | Método | Estado |
|---|---|---|
| **1. Estructural** | `K_GWA = proporción cognitiva × (1 − proporción social)` y `E_GWA = proporción de capacidades verbales, de razonamiento y cuantitativas`, ambas con las tablas oficiales de O\*NET. Se propagan a cada tarea como media sobre sus DWA (`itea.grading.structural`) | **Hecha y validada** (§5) |
| **2. Semántica ESCO** | *Embeddings* de frases (all-mpnet-base-v2). Cada tarea se enlaza con sus 5 conceptos ESCO más próximos (variante B; la A, con umbral global, dejaba sin enlazar el 46 %). K2 y E2 salen de los grupos oficiales ESCO (social, manual, informacional) | **Hecha y validada** (H9B–H13B) |
| **3. Anclas** | Clasificación *zero-shot* con un modelo NLI y anclas de Fernández-Macías y Bisello (K) y de Eloundou et al. (E) | **Hecha; resultado negativo** (falla H14–H17, D20) |
| **4. LLM (opcional)** | Modelo de pesos abiertos, en local, con temperatura 0, anclado por recuperación de casos parecidos como en la OIT (2025), y con todo registrado | Pendiente; opcional |
| **5. Combinación** | Rangos percentiles con pesos iguales de los componentes validados (K1+K2, E1+E2) y Monte Carlo de 1.000 réplicas sobre pesos, componentes, normalización y κ | **Hecha** (H18–H20; OAXI-EU v4.1) |

## 4. Capas T, U y S

**T (mediación tecnológica)**
- **Inventario por ocupación** (`itea.grading.technology`): 8.785 productos de software y 18.105 herramientas.
- **Presencia de fabricantes:** Microsoft en 894 ocupaciones, SAP en 303, IBM en 241, Oracle en 240 y Cisco en 43.
- **Objetivo del piloto de finanzas y consultoría:** 967 productos (116 *Hot Technology*); SAP aparece en 18 de 27 ocupaciones.
- **Corpus de capacidades declaradas** por los fabricantes: en dos fases (software de negocio e IA incorporada), con URL y copia archivada.
- **Emparejamiento tarea por tarea** dentro de cada ocupación.

**U (utilización efectiva) = adopción × profundidad**
- **Adopción:** Eurostat (`itea.grading.eurostat`; por tamaño, `isoc_eb_iip`, `isoc_eb_ics` e `isoc_eb_ai`; por sector NACE y país, `isoc_eb_iipn2`, `isoc_eb_ain2` e `isoc_eb_icsn2`, en `RESULTADOS_capaU_ES.md`). En 2025, en empresas de 10 o más empleados, España tiene ERP en el 60,4 % de las empresas (UE-27: 46,5 %) e IA en el 20,3 % (UE-27: 20,0 %). **Cautela:** ese agregado excluye el sector financiero (NACE K).
- **Profundidad:** un supuesto de 0,10–0,35 (valor central 0,27), respaldado por McGrenere y Moore (2000), Aberdeen (2006–2007) y Pendo (2019). Se recorre entero en el Monte Carlo.
- **Hipótesis central:** la IA eleva la profundidad de uso porque rebaja la barrera de pericia.

**S (solvencia técnica certificable)**
- Corpus de objetivos de examen de certificación (Microsoft, SAP, Oracle, IBM, Cisco, AWS) y marcos europeos (e-CF, DigComp, ESCO).
- **Brecha = T × (1 − S).**

## 5. Validación

- **Hipótesis registradas antes de ver los datos:** `HIPOTESIS_PREREGISTRADAS_ES.md`.
- **Resultados de la capa 1** (`RESULTADOS_capa1_ES.md`):
  - E1 converge con la exposición humana de Eloundou (ρ = 0,40);
  - K1 converge con el trabajo analítico no rutinario (ρ = 0,67);
  - K1 va en sentido contrario a la rutina cognitiva (ρ = −0,21; la hipótesis no se cumple, y la diferencia de constructo es informativa);
  - el riesgo de confundir K con la cualificación está al límite (ρ = 0,70 con el Job Zone);
  - solo el 5,3 % de la varianza de K1 está dentro de cada actividad general, así que hacen falta las capas 2–4.
- **Validación discriminante** (`RESULTADOS_discriminante_ES.md`, hipótesis H6–H8):
  - K1 sigue asociado al trabajo analítico al comparar dentro de cada Job Zone (ρ parcial = 0,28);
  - K1 predice la exposición humana de Eloundou descontando la cualificación (ρ parcial = 0,40);
  - la rutina cognitiva sigue en sentido contrario en las ocupaciones no manuales (ρ = −0,21), y se abandona como referencia (D15).
- **Siguientes pruebas obligatorias:**
  - la mejora de las capas 2–3 sobre H1, H6, H8 y la varianza dentro de cada actividad;
  - una matriz multirrasgo-multimétodo;
  - un Monte Carlo según el JRC-COIN.

## 6. Reproducibilidad
- **Código:** en `src/itea/grading/`, con tests en `tests/test_grading_*.py`.
- **Ejecución:** con `scripts/grading/`.
- **Salidas:** en `v4.0/outputs/grading/`.
- **Fuentes externas:** se descargan con `itea fetch` y se verifican por SHA-256; las de Eloundou, fijadas en el commit `0471612`.
- **Política:** ningún grado se entrena con AXI; ningún commit se antedata.
