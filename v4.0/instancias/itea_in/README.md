# ITEA-IN — dossier de arranque (India)

Estado: **iniciada (scaffold)**. Versión de instancia: v0 → v1.0 al lanzar.
Prioridad: **#3** (el candidato Tier-3 / imputado más fuerte).

## Sistema(s) nativo(s)

India es **competence-based** (como UE/ESCO o ES/INCUAL), no task-based:
- **NCO-2015** (National Classification of Occupations): clasificación jerárquica
  (8 dígitos), **basada en ISCO**. Mapeo oficial NCO↔cualificaciones (NCVET, 2025).
- **NSQF** (National Skills Qualifications Framework): marco de cualificaciones por
  niveles de resultados de aprendizaje → **análogo del EQF**.
- **NOS + QP** (National Occupational Standards / Qualification Packs): estándares
  de competencia por puesto, por los **Sector Skill Councils** (bajo NCVET).
  Capa equivalente a ESCO/CNECP (modelada sobre el NOS británico).

## Clase de medición

**Nivel 3 (imputado).** No hay descriptores nativos a nivel de tarea → el AXI se
imputaría de O*NET vía NCO→ISCO (supuesto de transferibilidad, atacable).

## Doble encaje en ITEA

- **Medición del AXI:** imputado (Nivel 3). Resultado de "clase débil".
- **Certificación + cualificación + microcredencial:** NSQF + NOS/QP es sustrato
  **rico y directamente aprovechable** → alimenta ITEA Global y el eje de
  certificación más que el núcleo de medición.

## Por qué es el Tier-3 más fuerte (> China)

1. NCO ISCO-based y **en inglés** → crosswalk limpio, sin barrera de idioma.
2. Capa de competencias (NOS/QP) y cualificaciones (NSQF).
3. Mapeo NCO↔cualificaciones ya oficial (2025).
4. Mayor fuerza laboral del mundo + TI/servicios muy expuestos a IA agéntica.

## Datos recibidos (2026-05-31)

- **NCO-2015** (PDF Vol I "code structure" 384 pp. + descripciones 1.519 pp.) —
  clasificación ocupacional ISCO-based. Base para el crosswalk NCO→ISCO.
- **Catálogo QP-NOS (NSDC)** — `india_qp_nos_catalogo.csv` (2.955 estándares) +
  `india_qp_por_sector_nivel.csv`. **42 sectores**; niveles **NSQF 1-9**
  (concentrado en nivel 4: 1.389). Tipos: QP-NOS 2.650, expository/discapacidad
  el resto. Es la **capa de competencias/certificación** de India (análogo del
  listado CNECP español). Fuente: nsdcindia.org/nos.
- **PENDIENTE para el índice de exposición:** empleo por ocupación **ISCO-08** de
  India (ILOSTAT, indicador con `OCU`) — sigue faltando (los xlsx subidos eran
  NEET e informalidad por sexo, sin ocupación).

## ITEA-IN v0 (resultado — primera instancia país de ITEA Global)

Construida (`itea_in_v0_por_grupo.csv` + `.meta.json`). **Imputada (Nivel 3)**: los
índices EU (IEA-EU/OAXI-EU) por gran grupo ISCO-1 se aplican —asumiendo
transferibilidad— a la **estructura de empleo real de India** (PLFS 2023-24,
Tabla 25, NCO-2015 = ISCO-08; person rural+urban).

| Indicador | Ponderado por empleo India | Media simple de grupos |
|-----------|---------------------------:|-----------------------:|
| IEA-EU (exposición) | **30,4** | 40,3 |
| OAXI-EU (expropiación) | **7,3** | 13,8 |

**Hallazgo:** el **59,2 % del empleo de India** está en agricultura (38,0 %) +
ocupaciones elementales (21,3 %) — baja exposición; solo el **10,7 %** en
directivos/profesionales/técnicos (alta exposición). La estructura de empleo
**tira el agregado hacia abajo**: India tiene focos muy expuestos (profesionales
IEA=68) pero exposición agregada baja. Conecta con la pregunta rectora: la
diferencia entre países es **estructura de empleo real**, no solo medición.

**Límites de la v0:** imputada (transferibilidad O*NET, clase débil); nivel
ISCO-1 (9 grupos, coarse); índices EU preliminares (TF-IDF, GEE carry-over).
Mejoras: 2 dígitos ISCO, índices EU finales, y eventualmente descriptores nativos.

## Plan de construcción (ITEA-IN)

1. NCO-2015 → crosswalk a ISCO-08 (ya es ISCO-based: directo).
2. Imputar contenido de tarea de O*NET sobre NCO→ISCO (declarar transferibilidad).
3. AXI-IN imputado; **declarar explícitamente** la clase Nivel 3.
4. Aprovechar NOS/QP/NSQF para el eje de certificación / cualificación (GEE-análogo).

## Pendiente / a confirmar

- Acceso a NOS/QP en formato estructurado (NSDC) y a la tabla NCO↔ISCO.
- Decidir si ITEA-IN entra como medición imputada o solo como capa de certificación.

Fuentes: nsdcindia.org/national-occupational-standards · nsdcindia.org/sector-skill-councils · ncs.gov.in (NCO-2015) · ncvet.gov.in (mapeo 2025)
