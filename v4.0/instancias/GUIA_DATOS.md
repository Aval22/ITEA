# Guía de datos para arrancar ITEA-IN / ITEA-JP / ITEA-KR

Qué descargar, de dónde y en qué formato para desbloquear cada instancia. Una vez
tengas el fichero, súbelo (como hicimos con O*NET/ESCO/AXI/JRC) y lo proceso.

---

## ITEA-IN (India) — imputada · arrancable con UN fichero público

**Necesito (mínimo para v0):** empleo de India por ocupación **ISCO-08**.

- **Fuente:** ILOSTAT (ilostat.ilo.org/data) → indicador **"Employment by sex and
  occupation (ISCO-08)"** (código tipo `EMP_TEMP_SEX_OCU_NB`).
- **Filtra:** Reference area = **India**; último año disponible; clasificación
  ISCO-08 (a 1 dígito basta para v0; 2 dígitos mejor).
- **Descarga:** botón de exportar → **CSV** (queda una tabla pequeña).
- *Qué hago con él:* aplico nuestros índices ISCO (IEA-EU/OAXI-EU) a la
  estructura de empleo de India (transferibilidad declarada) → **ITEA-IN v0
  imputada**: exposición agregada de India + qué ocupaciones concentran el riesgo.

**Opcional (enriquece, no bloquea):**
- **NCO-2015** (lista de ocupaciones, ISCO-based): `ncs.gov.in` (PDF Vol I/II).
- **NOS / QP** (capa de competencias/certificación): `nsdcindia.org/nos`.

---

## ITEA-JP (Japón) — nativa · la más valiosa

**Necesito (para un AXI-JP real, no imputado):** los **datos numéricos de jobtag**
por ocupación (tareas + skills/knowledge/abilities) y el crosswalk a ISCO.

- **Fuente 1 — jobtag (MHLW):** `shigoto.mhlw.go.jp`. Busca la descarga de
  **"数値情報" (información numérica) / "job tag 数値データ ダウンロード"**
  (la sección de datos descargables del sitio; suele ser Excel/CSV con los
  ~500 perfiles y sus puntuaciones por tarea/skill).
- **Fuente 2 — JILPT:** `jil.go.jp/activity/project/o-net/` — publica los datos y
  estudios del O-NET japonés (incluido el benchmark de automatización). Mira si
  ofrecen el dataset subyacente descargable.
- **Crosswalk:** la clasificación de jobtag se vincula a **JSCO** (Japan Standard
  Classification of Occupations) → ISCO-08. Busca "JSCO ISCO-08 correspondence".
- *Idioma:* japonés (lo traduzco para el mapeo).
- *Qué hago:* AXI-JP nativo desde las tareas jobtag + BRIDGE (US–JP) con el
  benchmark JILPT como validación.

---

## ITEA-KR (Corea) — nativa

**Necesito:** los **descriptores de KNOW** por ocupación (KECO) + crosswalk a ISCO.

- **Fuente 1 — KEIS / KNOW:** `keis.or.kr` (y el portal KNOW). Busca la descarga
  de los datos de la **"한국직업정보 (KNOW)"** / *Korea Network for Occupations
  and Workers*.
- **Fuente 2 — datos abiertos:** portal coreano **data.go.kr** (공공데이터포털),
  buscar "직업정보" / "KNOW" → suele haber datasets descargables (CSV/Excel).
- **Crosswalk:** **KECO** (Korean Employment Classification of Occupations) →
  ISCO-08 (12.816 ocupaciones → habrá que agregar).
- *Idioma:* coreano.
- *Qué hago:* AXI-KR nativo desde las actividades/tareas KNOW + BRIDGE.

---

## Resumen de prioridad

1. **India:** sube el CSV de ILOSTAT (empleo por ISCO-08) → construyo ITEA-IN v0 ya.
2. **Japón:** consigue el dataset numérico de jobtag → instancia nativa #1.
3. **Corea:** consigue los datos KNOW (vía data.go.kr) → instancia nativa #2.

Si alguno de los portales nativos (jobtag/KNOW) no deja descargar fácil, dímelo y
buscamos la vía alternativa (a veces el dato está en data.go.kr, e-Stat Japón, o
en repositorios académicos que ya los han extraído).
