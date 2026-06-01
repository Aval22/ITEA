# ITEA v4.0 — Changelog y trazabilidad de versiones

Registro de versiones de la línea v4.0 (ITEA-EU / BRIDGE US–UE). Formato basado
en *Keep a Changelog*; fechas en ISO (AAAA-MM-DD).

**Convención de versionado**
- **Marco:** `vMAJOR.MINOR[-estado]`. `v4.0` = integración ESCO + arquitectura de
  3 entornos (ITEA-US / ITEA-UE / ITEA BRIDGE US–UE) sobre ISCO-08.
- **Estado:** `beta`/WIP hasta cumplir la *Definition of Done* del spec
  (`docs/ITEA_v4_0_SPEC_DISENO.md` §7).
- **Componentes:** cada artefacto lleva su propia versión semántica y su
  **procedencia** (sha256 de entradas/salida, fecha) en un `.meta.json` adjunto.

---

## [v4.0-beta.4] — 2026-05-31 — robustez de la validación (ablación)

**Changed**
- `docs/VALIDACION_paso9.md`: añadida la **ablación** del IEA-EU. Hallazgo honesto:
  la validación contra el JRC la sostiene casi toda el **GEE (cualificación)** —
  solo GEE da 0,71/0,77; el término de exposición del AXI no aporta. Lo que tiene
  validación propia es la codificabilidad (CI_Grade) y la concordancia con ESCO,
  que es el aporte distintivo y diverge por diseño.

**Interno (no publicado, pendiente del paper)**
- Modelo de expropiación de 3 niveles (robot/Gen-IA/agéntica) + coste de
  oportunidad capital-salario por país; validación de lo distintivo; y la
  conjetura tarea-vs-título. Se mantienen fuera del repo por scooping.

---

## [v4.0-beta.3] — 2026-05-31 — instancias país + ITEA-IN v0 + CNECP

**Added**
- `instancias/` — arranque de la familia global: dossiers ITEA-JP / ITEA-KR /
  ITEA-IN, `README.md` (versionado por instancia + cola de prioridad) y
  `GUIA_DATOS.md` (dónde descargar los datos de cada país).
- `instancias/itea_in/` — **ITEA-IN v0** (primera instancia país, imputada): empleo
  de India por ISCO-1 (PLFS 2023-24, NCO-2015) ponderando los índices EU →
  **IEA-EU=30,4 / OAXI-EU=7,3**. Catálogo QP-NOS/NSQF por sector.
- `cnecp_es/` — sustrato España (INCUAL/CNECP): 28 familias × nivel (2.630 ECP) +
  descriptores de nivel (ancla EQF para GEE-EU).

**Notas**
- ITEA-IN v0 es **imputada (Nivel 3)** y a ISCO-1: preliminar, no producción.
- Datos de terceros (NCO/PLFS PDFs) y la pregunta de investigación rectora **no
  se redistribuyen**. Hallazgo: ILOSTAT no publica empleo por ocupación de India.

---

## [v4.0-beta.2] — 2026-05-31 — validación (pasos 8 y 9) + dos índices

**Added**
- `code/07_bridge_concordance.py` y `code/08_validate_vs_jrc.py` (pasos 8 y 9).
- `docs/INVARIANZA_paso8.md`, `docs/VALIDACION_paso9.md`, `docs/DECISION_dos_indices.md`.
- `outputs/occ_indices_EU_v1.parquet` (los dos índices), `bridge_concordance_by_isco.parquet`.

**Changed / Decided**
- **Dos índices** (decisión del autor): **IEA-EU** (exposición) y **OAXI-EU**
  (expropiación). IEA-EU **valida vs JRC145832** (Pearson 0,76 / Spearman 0,78 ≥ 0,70);
  OAXI-EU diverge por diseño (mide expropiación, no exposición pura).
- **`reuseLevel` jubilado como peso de codificabilidad** (correlación negativa con
  la exposición a IA); la codificabilidad pasa a derivarse del `CI_Grade` del AXI.
- Paso 8: evidencia de invarianza (concordancia BRIDGE↔ESCO, lift ~17× sobre azar).

**Notas**
- Datos del JRC (scores por ocupación) y del AXI **no se redistribuyen**; se usan
  solo como contraste, citados (JRC145832). Sigue pendiente, para v4.0 estable:
  CFA formal, embeddings, GEE-EU (EQF) y calibración de pesos.

---

## [v4.0-beta] — 2026-05-31 — PUBLICADA (commit `c06836d`)

Primera publicación pública (beta/WIP) de la línea europea.

**Added**
- Arquitectura de 3 entornos sobre eje ISCO-08 y tabla unificada `itea_by_isco`
  (434 grupos ISCO; 238 en los tres entornos).
- Pipeline reproducible `code/01`–`06` (carga ESCO → mapeo tarea→skill →
  agregación a ISCO → entornos → dashboard → OAXI-EU).
- **OAXI-EU** preliminar (primer índice europeo de expropiación, 238 ISCO).
- Documentos de diseño: taxonomía de la familia, spec v4.0, matriz
  indicador×entorno, versionado del mapeo.
- Dashboard interactivo de 3 entornos.

**Decided** — 10 decisiones de diseño cerradas (ver spec §9 y concepto):
v4.0 = solo BRIDGE US–UE · portabilidad híbrida · GEE-EU en 2 tiempos · núcleo
AXI/K/GEE/OAXI · umbrales ΔCFI<0,01 y JRC r≥0,70 · salida skill↔microcredencial ·
demanda solo OVATE · certificación recomendada+proxy futuro · Global diseño vivo ·
IDA por fases.

**Licensing** — Licencia de fuentes verificada en origen: **ESCO v1.2.1 = CC BY
4.0**; O*NET (USDOL/ETA) = CC BY 4.0 (marca registrada). Atribución reforzada en
el README; datos derivados marcados como "modificados".

---

## Versiones por componente

| Componente | Versión actual | Fecha | Método / estado | Próxima versión |
|------------|----------------|-------|------------------|-----------------|
| `task_skill_map` | **1.0-tfidf** | 2026-05-31 | TF-IDF+coseno (EN↔EN), 1ª pasada | `2.0-embeddings` (multilingüe, GPU) + corpus ES |
| `OAXI-EU` | **v0-carryover** | 2026-05-31 | GEE por carry-over O*NET; K sin calibrar | `v1` con GEE-EU (EQF) + K calibrado |
| GEE-EU | **fase 1 (carry-over)** | 2026-05-31 | crosswalk SOC→ISCO del GEE-O*NET | fase 2: anclaje nativo en EQF |
| entornos / tabla unificada | **1.0** | 2026-05-31 | 434 ISCO | — |

---

## Roadmap de versiones (planificado, no fechado)

- **v4.0 (estable):** al cumplir la *Definition of Done* — invarianza ΔCFI<0,01,
  validación OAXI-EU↔JRC r≥0,70, OAXI-EU con GEE-EU (EQF) y K calibrado, mapa en
  embeddings. Se acompañará de DOI de Zenodo.
- **v4.1+:** nuevas instancias país sobre la misma arquitectura (ITEA-JP, …) y sus
  ITEA BRIDGE bilaterales.
- **ITEA Global (horizonte):** plano de demanda + eje de certificación +
  brújula de microcredenciales (ver `docs/ITEA_FAMILIA.md`).

---

## Trazabilidad y procedencia

- **Versión↔commit:** cada versión del marco apunta a su commit en
  `github.com/Aval22/ITEA`. v4.0-beta = `c06836d`.
- **Artefacto↔procedencia:** `outputs/*.meta.json` registran versión, método,
  fecha y sha256 de entradas y salida de cada índice.
- **Inventario completo (privado):** `ITEA-EU_Datos/00_DOCS/MANIFEST.csv` (sha256
  de las 119 piezas de datos; no se publica por incluir fuentes de terceros y
  datos sin publicar).
