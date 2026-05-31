# ITEA v4.0 — beta (Work In Progress)

> ⚠️ **VERSIÓN BETA — TRABAJO EN CURSO.** Resultados **preliminares**, no
> revisados por pares y **sujetos a cambio**. No citar como definitivos. Esta
> carpeta acompaña al desarrollo de ITEA v4.0 (integración europea); la release
> estable del marco es la **v3.0** en la raíz de este repositorio.

ITEA v4.0 extiende ITEA al ecosistema europeo (ESCO/ISCO) y establece una
arquitectura de **tres entornos** sobre el eje común **ISCO-08** para análisis
comparativo y unificado:

- **ITEA-US** — sobre O*NET (task-based, EE.UU.). Indicadores v3.0 ya publicados.
- **ITEA-UE** — sobre ESCO (competence-based, UE). Aporta la codificabilidad (K).
- **ITEA BRIDGE (US–UE)** — el marco puente bilateral (tarea O*NET → competencia
  ESCO, vía crosswalk SOC↔ISCO), donde nace el índice europeo **OAXI-EU**.

Nomenclatura completa de la familia en [`docs/ITEA_FAMILIA.md`](docs/ITEA_FAMILIA.md).

## Estado de los resultados (beta)

| Pieza | Estado |
|-------|--------|
| Mapeo tarea→competencia | **v1.0-tfidf** (1ª pasada léxica; pendiente pasada de embeddings multilingües) |
| OAXI-EU | **v0-carryover** (GEE por crosswalk de O*NET; pendiente anclaje EQF) |
| Peso de codificabilidad K | **propuesto, sin calibrar** (0,25/0,50/0,75/1,00) |
| Invarianza de medición (paso 8) | pendiente |
| Validación convergente vs JRC 2026 (paso 9) | pendiente |

## Contenido

- `code/` — pipeline reproducible (`01`–`06`): carga ESCO → corpus → mapeo
  tarea→skill → agregación a ISCO → entornos → dashboard → OAXI-EU.
- `docs/` — diseño y metodología: familia ITEA, spec v4.0, matriz indicador ×
  entorno, versionado del mapeo.
- `outputs/` — **resultados ligeros agregados por ISCO** (no contienen datos
  crudos de terceros ni el texto de tareas): perfiles ESCO/Híbrido por ISCO,
  tabla unificada `itea_by_isco.parquet`, índice `occ_oaxi_eu.parquet`, y un
  `dashboard.html` interactivo autocontenido.

## Reproducir

Las **fuentes primarias no se redistribuyen aquí** (se descargan de su origen):

- **ESCO v1.2.1** (CC BY 4.0): <https://esco.ec.europa.eu/en/use-esco/download>
- **O*NET 30.2** (CC BY 4.0): <https://www.onetcenter.org/database.html>
- Crosswalk SOC↔ISCO-08 y la base de tareas graduadas (AXI) son material del
  autor / fuentes externas; ver la metodología.

Con los datos en su sitio, cada script acepta `--base <ruta_raíz_datos>` y
regenera su salida (ver cabecera de cada `code/0*.py`). El orden es 01→06.

## Cita y licencia

Marco ITEA — Alberto García-Lluis Valencia (URJC). Repositorio:
<https://github.com/Aval22/ITEA>. La v4.0 es **beta**; para citación estable usar
la v3.0 y su DOI de Zenodo. Atribución requerida a O*NET y ESCO (CC BY 4.0).
