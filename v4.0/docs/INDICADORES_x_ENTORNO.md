# Matriz de indicadores × entorno (paso 2)

Qué indicador de ITEA es calculable en cada entorno, con qué dato/proxy y con
qué limitación. Tabla accionable en [`INDICADORES_x_ENTORNO.csv`](INDICADORES_x_ENTORNO.csv).
Es un inventario estructural: el **alcance definitivo** de qué se porta a v4.0
se fija en el documento de diseño (paso 3).

Nomenclatura (ver `ITEA_FAMILIA.md`): las columnas **O*NET / ESCO / Híbrido**
son **ITEA-US / ITEA-UE / ITEA BRIDGE (US–UE)** respectivamente.

**Leyenda:** `nativo` = se calcula directamente con datos propios del entorno ·
`proxy` = aproximable con otra variable · `pendiente` = requiere un paso o
fuente que aún falta · `no aplica` = el entorno carece del dato base.

| Indicador | Qué mide | O*NET | ESCO | Híbrido |
|-----------|----------|-------|------|---------|
| **AXI / AEI** | Expropiación algorítmica (task-based, núcleo) | nativo — 47.810 tareas graduadas | no aplica — ESCO no modela tareas | **nativo** — mapa tarea→skill con grados |
| **ITEA** (triple) | z(EAC)+z(EIG)+z(EIA)/3 | nativo | proxy parcial | parcial — falta recomponer en ISCO |
| EAC | Automatización de actividades | nativo (degenerado, L1) | no aplica | proxy — task→skill + Auto_Grade |
| EIG | Intensidad de conocimiento (satura, L2) | nativo | proxy — rama K de ESCO | proxy |
| EIA | Codificación de conocimiento tácito | nativo | no aplica | **nativo** — CI_Grade HIGH_ALGO |
| **GEE** | Estructuración del empleo (cualificación) | nativo — Job Zone (ρ=0,92) | **proxy pendiente — anclar en EQF** | proxy pendiente — EQF sobre ISCO |
| **K / codificabilidad** | Cristalización (reuseLevel) | proxy — CI_Grade análogo | **nativo — reuseLevel (pesos a calibrar)** | **nativo** — hereda K + grados |
| IRA | Resiliencia = 0,6·CA + 0,4·IRO_resid | nativo | pendiente — definir CA/IRO en ESCO | pendiente |
| ICT·IFS·IPI·IEF | Auxiliares del OAEI/resiliencia | nativo | por confirmar en spec | por confirmar |
| **OAXI / OAEI** | Índice compuesto ITEA×GEE×ICT×(1−IPI) | nativo — OAEI v3.0 (1-100) | no aplica | **pendiente — OAXI-EU** tras componentes + GEE-EU |
| Validación externa | Benchmark convergente | nativo — AIOE (Felten 2021) | JRC 2026 pendiente | **JRC 2026 pendiente** (paso 9) |

## Lectura estratégica

**O*NET** es el entorno completo: 10 de 11 indicadores nativos. Es la base ya
publicada (Paper 8A / workbook v3.0).

**ESCO** aporta de forma nativa **una sola cosa, pero decisiva: la
codificabilidad (K, vía reuseLevel)** — justo la dimensión que en O*NET es solo
un proxy (CI_Grade). A cambio, todo lo task-based (AXI, EAC, EIA, OAXI) **no
aplica** en ESCO puro: es su límite estructural. ESCO no compite con O*NET; lo
complementa por el lado de las competencias.

**Híbrido** es donde nace ITEA-EU: recupera lo task-based sobre el eje ISCO
(AXI, EIA ya nativos vía el mapa) y lo combina con la K de ESCO. Sus tres
"pendientes" mayores son exactamente la hoja de ruta a v4.0:

1. **Anclar GEE-EU en el EQF** (sustituto europeo del Job Zone). Sin GEE no hay OAXI.
2. **Computar y calibrar el OAXI-EU** (recomponer ITEA×GEE×… en ISCO; calibrar pesos K).
3. **Validar contra el índice JRC 2026** (paso 9) — el análogo de AIOE en Europa.

Más, transversal a los tres: la **prueba de invarianza de medición** (paso 8),
que demuestra que AXI/K miden lo mismo en estructura task-based y de competencias.

## Cómo conecta con "qué falta para v4.0"

Esta matriz operacionaliza el diagnóstico previo: las celdas `pendiente` del
Híbrido (GEE-EU, OAXI-EU, validación JRC) + la invarianza de medición son,
literalmente, el trabajo que separa el estado actual de ITEA 4.0 con ESCO
integrado. Los componentes auxiliares (ICT/IFS/IPI/IEF/IRA) se resuelven al
fijar definiciones en el spec (paso 3).
