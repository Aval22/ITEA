# ITEA-JP — dossier de arranque (Japón)

Estado: **iniciada (scaffold)**. Versión de instancia: v0 → v1.0 al lanzar.
Prioridad: **#1** (la más importante tras US/UE).

## Sistema nativo

**jobtag (職業情報提供サイト / 日本版O-NET)** — Ministerio de Salud, Trabajo y
Bienestar (MHLW). Sitio: <https://shigoto.mhlw.go.jp/User>.
- Modelado sobre el **O*NET** estadounidense (US DOL); construcción desde 2018.
- ~**500 perfiles ocupacionales** (a abril 2023), con job / **task** / skill,
  intereses, valores, conocimientos, habilidades.
- Información numérica **basada en los ítems de O*NET**, pero **poblada con
  encuestas a trabajadores japoneses** → medición independiente (datos propios).

## Clase de medición

**Nivel 1 (nativa e independiente).** Matiz: el *instrumento* es O*NET-modelado
(estructura de ítems compartida), lo que **facilita el crosswalk y la
comparación**, pero hay que documentarlo (instrumento común). Atención: el JILPT
publicó una nota sobre malentendidos en la información numérica de jobtag —
revisar antes de usar los valores.

## Por qué es la #1

- Nivel 1 nativo (misma clase metodológica que US/UE).
- **Benchmark de validación externa ya publicado:** el JILPT replicó
  Frey-Osborne sobre el propio O-NET japonés (<https://www.jil.go.jp/activity/project/o-net/index.html>)
  → ancla de validación + literatura + prueba de factibilidad.
- jobtag tiene capa de **tareas** → permite el AXI nativo (no imputado).

## Eje ocupacional y crosswalk

jobtag usa la clasificación japonesa (vinculada a JSCO / ISCO). Camino:
ocupación jobtag → (crosswalk) → **ISCO-08** → comparación con US/UE.

## Plan de construcción (ITEA-JP)

1. Obtener el dataset de jobtag (perfiles + tareas + descriptores numéricos).
2. Crosswalk ocupación-jobtag → ISCO-08.
3. AXI-JP nativo desde las tareas jobtag (no imputado).
4. **ITEA BRIDGE (US–JP)**: invarianza + validación contra el benchmark JILPT.

## Pendiente / a confirmar

- Vía de descarga/acceso de los microdatos de jobtag (¿API, descarga, scraping?).
- Versión y fecha actuales del dataset; idioma (JP) → traducción para el mapeo.
- Leer la nota JILPT sobre la información numérica antes de calcular.

Fuentes: shigoto.mhlw.go.jp · jil.go.jp/activity/project/o-net
