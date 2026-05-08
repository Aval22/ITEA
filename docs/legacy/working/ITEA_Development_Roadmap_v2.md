# ITEA Framework — Development Roadmap (v2.0 baseline)
## Plan de desarrollo: Mayo → Octubre 2026
### Objetivo: Submission a JORS (octubre) y reenvío a JOSS (noviembre) con seis meses de historial público sobre v2.0

---

## Resumen ejecutivo

JOSS rechazó el envío inicial (paper v1.45) por **falta de historial de desarrollo público**: el repositorio Aval22/ITEA fue creado el 14 de abril de 2026 y registró toda su actividad en menos de 24 horas (7 commits, 0 issues, 0 PRs, 0 releases, 0 contribuyentes externos).

Este roadmap reemplaza el plan anterior (que extendía v1.45 hasta v1.50) por una estrategia consolidada sobre **v2.0 como baseline**, que incorpora la reconceptualización IRO→IRA, la articulación formal del AEI y la recalibración del OAEI. La razón: extender v1.45 durante seis meses sería simular actividad sobre una metodología que el propio autor ya considera superada.

**Triple pista editorial:**

- **JORS (octubre 2026)**: metapaper sobre la metodología y los datos. JORS no exige historial de desarrollo, así que es el camino corto. El borrador `JORS_ITEA_Metapaper.md` está listo y solo requiere reorientarse a v2.0.
- **JOSS (noviembre 2026)**: resubmisión del paper sobre el software, ya con seis meses de actividad real, paquetes R y Python instalables, tests con cobertura > 80 %, CI verde y vignettes reproducibles.
- **Zenodo**: nuevo DOI emitido para v2.0.0 al inicio del ciclo; el DOI de v1.45 queda accesible como histórico.

**Cadencia comprometida**: ~10 commits/semana, ~4 issues/mes cerrados con PR, una release/mes con tag y release notes.

---

## MES 1 — Mayo 2026: Consolidación v2.0 e infraestructura mínima

### Semana 1 (4–10 mayo) — Saneamiento del repo

**Issue #1**: "Subir datos al repo (P0 bloqueante)"
- Crear `data/raw/onet_30_2/` con los 11 .txt mínimos + Read Me oficial + SHA-256.
- Subir `data/processed/Research_Data_Workbook_ITEA_v2.xlsx`.
- Subir `data/processed/AEI_Unified_Analysis_v3_8.xlsx` (47.810 tareas, 924 ocupaciones).
- Crear `data/README.md` documentando fuente, fecha de descarga y licencia O*NET.
- Commit: "Add raw O*NET 30.2, processed workbook v2.0, and AEI dataset v3.8".

**Issue #2**: "Subir documentación al repo (P0 bloqueante)"
- Mover los .docx locales a `docs/methodology/`, `docs/guides/`, `docs/papers/`.
- Eliminar las carpetas vacías `docs/analysis/` y `docs/collaboration/` (o llenarlas).
- Crear `docs/methodology/migration_v145_to_v2.md` con el changelog detallado.
- Commit: "Add v2.0 methodology and user guides; remove placeholder dirs".

### Semana 2 (11–17 mayo) — Coherencia documental + tests mínimos

**Issue #3**: "Corregir incoherencias en README, paper.md y CITATION.cff"
- Email del autor (alb.valencia@gmail.com) y ORCID (0009-0003-1438-1633) — quitar los "[pending]".
- Corregir la fila de v1.45 en la tabla de versiones (fecha real 2026-04-14, no 2026-10).
- Actualizar el badge de versión a `v2.0.0`, el de O*NET a `30.2`.
- Eliminar la afirmación "automated tests verifying cross-language consistency to six decimal places" del paper.md *vigente* hasta tener tests reales (issues #4 y #5).
- Commit: "Fix README/paper.md/CITATION metadata".

**Issue #4**: "Tests unitarios R para los 8 indicadores"
- Crear `tests/testthat/` con `test-itea.R`, `test-ira.R`, `test-ict.R`, `test-ifs.R`, `test-ipi.R`, `test-ief.R`, `test-gee.R`, `test-imo.R`, `test-aei.R`, `test-oaei.R`.
- Casos: borde (0,0,0), (1,1,1), valores reales del workbook, validación contra valores conocidos.
- Commit: "Add R unit tests for the 10 indicators of v2.0 (8 + AEI + OAEI)".

**Issue #5**: "Tests unitarios Python equivalentes"
- Crear `tests/python/test_itea.py` etc. con `pytest`.
- Cross-language validation: leer el workbook, calcular en Python, comparar con valores R hasta 6 decimales.
- Commit: "Add Python test suite + cross-language consistency check".

### Semana 3 (18–24 mayo) — CI y release v2.0.0

**Issue #6**: "GitHub Actions: R-CMD-check + pytest"
- `.github/workflows/r-tests.yaml` (Ubuntu, R 4.3 + 4.4).
- `.github/workflows/python-tests.yaml` (3.10, 3.11, 3.12).
- `.github/workflows/streamlit-smoke.yaml` (arrancar app y verificar HTTP 200 en 30 s).
- Badges en README que reflejen el estado real.
- Commit: "Set up CI: R-CMD-check, pytest, Streamlit smoke test".

**Issue #7**: "CONTRIBUTING.md, CODE_OF_CONDUCT.md, ISSUE_TEMPLATE/"
- Plantillas de bug report y feature request.
- Code of Conduct (Contributor Covenant 2.1).
- Guía de contribución con instrucciones de fork, branch, PR y test local.
- Commit: "Add community files (contributing, conduct, issue templates)".

### Semana 4 (25 mayo–1 junio) — Release v2.0.0

**Issue #8**: "Release v2.0.0 — IRO→IRA, AEI articulado, OAEI [1, 100]"
- Tag `v2.0.0` con release notes detalladas (changelog v1.45 → v2.0).
- Publicar en Zenodo y obtener nuevo DOI.
- Anunciar en GitHub release y en LinkedIn.

**Métrica final mes 1**: ≥18 commits, 8 issues cerrados, 1 release, CI verde, repo ejecutable end-to-end por un externo.

---

## MES 2 — Junio 2026: Validación empírica del IRA v2.0

### Semana 5 (2–8 junio)

**Issue #9**: "Bootstrap de los pesos 60/40 del IRA v2.0"
- 1.000 réplicas bootstrap sobre las 846 ocupaciones efectivas.
- IC 95 % de los pesos óptimos por minimización de la correlación residual con GEE.
- Documentar en `docs/methodology/IRA_v2_validation.md`.
- Commit: "Empirical validation: bootstrap weights of IRA v2.0".

**Issue #10**: "ANOVA del cuadrante GEE × IRA"
- Test formal de la diferencia de OAEI medio entre Q1 (alto-alto) y Q4 (alto-bajo).
- Análisis de sensibilidad a la elección de la mediana como umbral (vs. terciles).
- Commit: "Quadrant analysis: GEE × IRA inversion of Insider-Outsider prediction".

### Semana 6 (9–15 junio)

**Issue #11**: "Comparativa IRO v1.45 vs IRA v2.0 sobre las 846 ocupaciones"
- Recalcular ambos sobre el mismo subconjunto.
- Tabla de cambios de ranking, top-20 movers y losers.
- Confirmar empíricamente la reducción de r con GEE: 0.904 → 0.43.
- Commit: "Comparative analysis: IRO v1.45 → IRA v2.0 ranking shifts".

### Semana 7 (16–22 junio)

**Issue #12**: "GEE: validación con regresión proportional-odds (ordinal)"
- Ejecutar `MASS::polr` sobre Job Zones.
- Comparar coeficientes OLS (0.215) vs ordinal (0.228) para C_RL.
- Documentar como sensitivity check.
- Commit: "GEE ordinal validation: confirm regression coefficients".

### Semana 8 (23–29 junio) — Release v2.1.0

**Issue #13**: "Release v2.1.0 — Validación IRA v2.0 + cobertura tests > 70 %"
- Tag `v2.1.0`, release notes, Zenodo update.
- Cobertura medida con `covr` (R) y `pytest --cov` (Python).

**Métrica final mes 2**: ≥36 commits acumulados, 13 issues cerrados, 2 releases.

---

## MES 3 — Julio 2026: Crosswalks internacionales y validación española

### Semana 9 (30 junio–6 julio)

**Issue #14**: "Crosswalk SOC ↔ CNO-11 (España)"
- Tabla de equivalencias en `data/crosswalks/SOC_CNO_11.csv`.
- Función `code/python/itea/crosswalk.py:soc_to_cno()` y equivalente R.
- Commit: "Add SOC ↔ CNO-11 crosswalk for Spanish labor market".

### Semana 10 (7–13 julio)

**Issue #15**: "Crosswalk SOC ↔ ISCO-08"
- `data/crosswalks/SOC_ISCO_08.csv`.
- Validar contra crosswalk oficial BLS-Eurostat.
- Commit: "Add SOC ↔ ISCO-08 crosswalk for international comparisons".

### Semana 11 (14–20 julio)

**Issue #16**: "Validación con Infoempleo-Adecco 2023-2024"
- Cargar dataset (n > 3.000 firmas) y mapear a CNO-11.
- Calcular ITEA, IRA, OAEI por sector y comparar con tasas de adopción declaradas.
- Documentar correlación predicha-observada.
- Commit: "Spanish labor market validation against Infoempleo-Adecco".

### Semana 12 (21–27 julio) — Release v2.2.0

**Issue #17**: "Tab dashboard: análisis sectorial CNO-11"
- Nuevo view en Streamlit con heatmap por sector CNO Major.
- Toggle SOC ↔ CNO ↔ ISCO en el selector de ocupación.
- Commit: "Dashboard: add sector heatmap and crosswalk selector".

**Release v2.2.0**: "International crosswalks and Spanish validation".

**Métrica final mes 3**: ≥54 commits, 18 issues cerrados, 3 releases, dashboard con 7 tabs.

---

## MES 4 — Agosto 2026: Migración O*NET 30.2 y robustez

### Semana 13 (28 julio–3 agosto)

**Issue #18**: "Pipeline de ingestión desde raw .txt"
- `code/ingest/build_workbook.py`: leer 11 .txt → reproducir `Research_Data_Workbook_ITEA_v2.xlsx`.
- Test de regresión: el workbook reconstruido debe coincidir byte-a-byte con el versionado.
- Commit: "Reproducible ingestion pipeline from raw O*NET 30.2".

### Semana 14 (4–10 agosto)

**Issue #19**: "Recalcular framework con O*NET 30.2 vs 29.1"
- Ejecutar pipeline con ambos releases.
- Tabla de deltas: top-20 ocupaciones con mayor cambio en cada indicador.
- Spearman entre versiones para cada indicador (decisión: si cualquiera < 0.98 → v3.0.0 breaking).
- Commit: "Compare ITEA v2.0 across O*NET 29.1 and 30.2".

### Semana 15 (11–17 agosto)

**Issue #20**: "Bootstrap IC 95 % por ocupación"
- IC para cada indicador y ocupación (1.000 réplicas).
- Añadir columnas IC_lower / IC_upper al workbook.
- Commit: "Bootstrap confidence intervals per occupation".

### Semana 16 (18–24 agosto)

**Issue #21**: "Análisis de sensibilidad de pesos"
- Perturbación ± 10 % en pesos de ITEA, ICT, IFS, IEF, IPI.
- Elasticidad de rankings; figuras de robustez para el paper.
- Commit: "Weight sensitivity analysis for formative indicators".

### Semana 17 (25–31 agosto) — Release v2.3.0

**Release v2.3.0**: "O*NET 30.2 migration and robustness analyses".

**Métrica final mes 4**: ≥72 commits, 23 issues cerrados, 4 releases.

---

## MES 5 — Septiembre 2026: Empaquetado R y Python + vignettes

### Semana 18 (1–7 septiembre)

**Issue #22**: "Estructura de paquete R"
- Crear `iteaR/` con `DESCRIPTION`, `NAMESPACE`, `R/`, `man/`.
- roxygen2 docs para todas las funciones públicas.
- `iteaR::install_github("Aval22/ITEA/iteaR")` debe funcionar limpio.
- Commit: "Restructure R code as installable package iteaR".

### Semana 19 (8–14 septiembre)

**Issue #23**: "Estructura de paquete Python"
- Crear `iteapy/` con `pyproject.toml`, `iteapy/__init__.py`, `iteapy/indicators.py`, `iteapy/aei.py`.
- Type hints completos; `pip install git+https://github.com/Aval22/ITEA.git#subdirectory=iteapy`.
- Commit: "Restructure Python code as installable package iteapy".

### Semana 20 (15–21 septiembre)

**Issue #24**: "Vignette 1: Getting started with ITEA"
- Tutorial paralelo R y Python: cargar datos, calcular un indicador, visualizar.
- Commit: "Add getting-started vignette".

**Issue #25**: "Vignette 2: Comparing occupations (Financial Analyst vs Emergency Medicine Physician)"
- Caso de uso del README; perfil radar; análisis OAEI.
- Commit: "Add occupation comparison vignette".

### Semana 21 (22–28 septiembre) — Release v2.4.0

**Issue #26**: "Vignette 3: ITEA for policy analysis (CCAA España)"
- Identificar ocupaciones vulnerables por comunidad autónoma usando crosswalk SOC ↔ CNO-11.
- Commit: "Add policy analysis vignette".

**Release v2.4.0**: "Installable R/Python packages and vignettes".

**Métrica final mes 5**: ≥90 commits, 28 issues cerrados, 5 releases, 3 vignettes, paquetes instalables.

---

## MES 6 — Octubre 2026: Submission JORS y preparación JOSS

### Semana 22 (29 septiembre–5 octubre)

**Issue #27**: "Migrar metapaper a v2.0 (JORS)"
- Reescribir `JORS_ITEA_Metapaper.md` con IRA, AEI, OAEI v2.0, O*NET 30.2.
- Añadir secciones de Reuse Potential con datos reales del Streamlit (visitas, descargas).
- Commit: "Migrate JORS metapaper to v2.0".

**Issue #28**: "Cover letter JORS"
- Carta destacando el aporte metodológico (multidimensionalidad, IRA residualizada, AEI articulada) y la diferenciación frente al artefacto JOSS (que enfocará el software).
- Commit: "Add JORS cover letter".

### Semana 23 (6–12 octubre)

**Issue #29**: "Cobertura tests > 80 % y reporte"
- `covr::report()` y `pytest --cov-report=html`.
- Subir reporte a `docs/coverage/`.
- Commit: "Test coverage report: > 80% achieved across R and Python".

**Issue #30**: "Pre-submission checklist JORS"
- Verificar plantilla, formato, archivos suplementarios, licencias.
- Commit: "JORS pre-submission checklist complete".

### Semana 24 (13–19 octubre) — Release v2.5.0 + Submission JORS

**Release v2.5.0**: "JORS-ready release" — Tag, Zenodo, anuncio.

**→ ENVIAR JORS** (semana 24).

### Semana 25 (20–26 octubre) — Preparación JOSS

**Issue #31**: "Migrar paper.md JOSS a v2.0 + maturity statement"
- Ya hecho en abril (paper.md actualizado), ahora añadir un párrafo "Maturity Statement" documentando los seis meses de roadmap ejecutado.
- Linkar issues cerrados, releases, contribuidores externos (si los hay).
- Commit: "Update JOSS paper for resubmission with 6-month maturity statement".

**Issue #32**: "Pre-submission checklist JOSS"
- Verificar todos los criterios de la página JOSS Submissions.
- Commit: "JOSS pre-submission checklist complete".

### Semana 26 (27 octubre–2 noviembre) — Submission JOSS

**→ REENVIAR A JOSS** con el repo en estado v2.5.0+.

---

## Métricas objetivo a 31 octubre 2026

| Métrica | 29/04/2026 | Objetivo 31/10/2026 |
|---------|-----------:|--------------------:|
| Commits totales | 7 | > 90 |
| Issues cerrados (con PR) | 0 | > 30 |
| Pull requests | 0 | > 20 |
| Releases (tags) | 0 | 6 (v2.0.0 → v2.5.0) |
| Tests automatizados | 0 | > 60 (R + Python) |
| Cobertura de tests | n/a | > 80 % |
| Vignettes | 0 | 3 |
| Crosswalks | 0 | 2 (CNO-11, ISCO-08) |
| Tabs dashboard | 5 | 7+ |
| Stars GitHub | 0 | > 10 |
| Contribuidores externos | 0 | ≥ 1 |
| DOIs Zenodo | 1 (v1.45) | ≥ 3 (v1.45, v2.0, v2.5) |
| Sumisiones editoriales | 0 (rechazo previo) | JORS enviado + JOSS resubmission |

---

## Cadencia semanal recomendada

- **Lunes**: revisar issues abiertos, planificar la semana, abrir nuevos issues si procede.
- **Martes a jueves**: trabajo, commits descriptivos (≥ 3 commits/día deseable; mensajes que describan el problema, no la herramienta).
- **Viernes**: cerrar issues con PR mergeado, actualizar `CHANGELOG.md`, pequeña síntesis pública (LinkedIn/Twitter).
- **Último viernes del mes**: tag de release, release notes, Zenodo upload, anuncio.

---

## Higiene editorial frente a JOSS y JORS

- **Mensajes de commit honestos**: describir el problema y la solución; evitar mensajes que delaten dependencia exclusiva de IA generativa.
- **AI Usage Disclosure**: mantenerlo en paper.md y JORS. JOSS tolera el uso de IA; lo que penaliza es la opacidad.
- **Diferenciación JOSS vs JORS**: el paper JOSS describe el software (paquetes, tests, dashboard); el metapaper JORS describe la metodología y los datos. No copy-paste.
- **Nunca prometer en el paper lo que no exista en el repo**: cada claim debe poder cerrarse con un link al issue, al test, al fichero o al commit.

---

## Riesgos y planes de contingencia

| Riesgo | Mitigación |
|--------|-----------|
| Pierdes una semana en mayo (P0 inacabado) | Posponer JOSS un mes; mantener JORS en su fecha. |
| O*NET 30.2 cambia rankings críticos (Spearman < 0.98) | Bumpear a v3.0.0 en septiembre, no en agosto; documentar como breaking change. |
| Cero contribuidores externos en octubre | Activar outreach del directorio (80 contactos) en julio para crear pull factor; aceptar PRs pequeños. |
| Tests rojos antes de un release | Bloquear el tag hasta CI verde; release notes nunca antes que el tag. |
| Auto-plagio JORS↔JOSS marcado por revisor | Diferenciación explícita en cover letter de cada revista; citas cruzadas en ambos artefactos. |

---

## Referencias internas

- Diagnóstico técnico completo: `docs/Diagnostico_Framework_ITEA_2026-04-29.docx`.
- Estrategia de difusión paralela: `docs/ITEA_Dissemination_Strategy.md`.
- Metodología v2.0: `docs/methodology/ITEA_Metodologia_v2_0.docx`.
- Migración v1.45 → v2.0: `docs/methodology/migration_v145_to_v2.md` (a redactar como issue #2).

*Última revisión del roadmap: 29 de abril de 2026.*
