# ITEA Framework — Índice de Triple Exposición a la Automatización

🌐 [English](README.md) · **Español** · [Português](README_PT.md) · [中文](README_ZH.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19578916.svg)](https://doi.org/10.5281/zenodo.19578916)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![O*NET](https://img.shields.io/badge/O*NET-30.2-green)]()
[![Version](https://img.shields.io/badge/Version-3.0-blue)]()

> **Un framework multidimensional para medir la exposición ocupacional a la expropiación algorítmica bajo el régimen de IA Agentic.**

---

## ¿Qué es ITEA v3.0?

El Framework ITEA proporciona diez indicadores complementarios que cubren 1.016 ocupaciones SOC 6-dígitos de O\*NET 30.2, diseñados para medir la exposición ocupacional a la expropiación algorítmica en el régimen de IA Agentic — distinto pero complementario a los índices de automatización a nivel de tarea de la tradición Frey-Osborne (2017) o medidas de exposición basadas en habilidades como el benchmark AIOE de Felten, Raj y Seamans (2021).

Validación convergente externa frente al benchmark AIOE sobre 738 ocupaciones SOC 6-dígitos comunes: **r(OAEI v3.0+, AIOE) = 0,797**.

| Indicador | Nombre completo | Dimensión | Tipo | Estado |
|-----------|----------------|-----------|------|--------|
| **ITEA** | Índice de Triple Exposición a la Automatización | Exposición | Formativo (agregación z-score) | **Revisado en v3.0** |
| **IRA** | Índice de Resiliencia Adaptativa | Resiliencia | Reflexivo (residualización triple) | **Revisado en v3.0** |
| **ICT** | Índice de Complejidad Técnica | Complejidad | Formativo | Estable desde v2.0 |
| **IFS** | Índice de Fricción Social | Interacción social | Reflexivo | Estable desde v2.0 |
| **IPI** | Índice de Presencialidad Interpersonal | Presencialidad | Formativo | Estable desde v1.3 |
| **IEF** | Índice de Especificidad Funcional | Especificidad | Reflexivo | Estable desde v2.0 |
| **GEE** | Gradiente Educación-Experiencia | Cualificación | Calibrado (OLS+ordinal) | Estable desde v1.45 |
| **IMO** | Índice de Mutación Ocupacional | Mutación | Modelo Hurdle | Estable desde v1.2 |
| **OAEI** | Índice Ocupacional de Expropiación Algorítmica | Compuesto operacional | Multiplicativo (canónico) + aditivo (alternativo) | **Revisado en v3.0 — variante dual** |
| **AEI** | Índice de Expropiación Algorítmica | Benchmark interno | Auxiliar | Estable desde v2.0 |

---

## ¿Por qué la versión 3.0? Evidencia de un proyecto de investigación vivo

Este repositorio avanza de **v1.45 (octubre 2025)** a **v3.0 (abril 2026)**, archivando la versión previa como tag [`v1.45-legacy`](https://github.com/AVAL22/ITEA-Framework/releases/tag/v1.45-legacy). La transición no es cosmética. Refleja una revisión metodológica mayor motivada por un caso práctico documentado — tres papers de investigación (la trilogía 8A/8B/8C) que pusieron el framework en uso empírico activo y, al hacerlo, expusieron tres limitaciones específicas de v2.1 (la línea metodológica que corría paralela a v1.45). Documentar esta evolución explícitamente forma parte de la preparación para someter el framework al [Journal of Open Source Software](https://joss.theoj.org/) (ventana objetivo: mediados de 2026), que valora la evidencia de uso en la comunidad y la evolución metodológica fundamentada.

### La trilogía como caso práctico

Tres papers de investigación en circulación activa en abril de 2026 motivaron cada una de las tres revisiones centrales en v3.0:

- **Paper 8A — *"The Structural Flaw: Industrial Labour Contract Inadequacy under Agentic AI"*** (García-Lluis Valencia, 2026a). Revistas objetivo: Journal of Institutional Economics, Industrial and Corporate Change. → motivó la **agregación ITEA por z-score**.
- **Paper 8B — *"Beyond the Pigouvian Trap: Tokenised Intellectual Capital..."*** (García-Lluis Valencia, 2026b). Paper teórico que formaliza la disolución de la condición protectora Lindbeck–Snower. → motivó el **OAEI de variante dual** (multiplicativo para alineación teórica + aditivo para validez de criterio).
- **Paper 8C — *"QE and Senior Workforce Restructuring: A Labour Liability Transmission Channel"*** (García-Lluis Valencia, 2026c). Revista objetivo: *Labour Economics*. Paper empírico sobre un canal novedoso de transmisión de política monetaria. → motivó el **IRA con residualización triple**.

| Cambio en v3.0 | Motivación empírica desde la trilogía | Ganancia de validación |
|----------------|---------------------------------------|------------------------|
| ITEA: normalización z-score antes de promediar con pesos iguales | El relato del top-20 del Paper 8A divergía del ranking algorítmico de v2.1; la asimetría de varianza entre componentes diluía la señal Agentic de EIA | r(ITEA, AEI): 0,71 → 0,89; r(ITEA, AIOE): 0,36 → 0,43 |
| IRA: residualización triple frente a (GEE, ITEA, ICT) | El análisis de cuadrantes GEE × IRA del Paper 8C mostraba separación Q1-Q4 inflada por la correlación residual IRA-ITEA bajo la residualización univariante de v2.1 | r(IRA, ITEA): 0,28 → 0,14; r(IRA, ICT): 0,10 → 0,06; 84% de varianza preservada |
| OAEI: arquitectura de variante dual (multiplicativa canónica + aditiva alternativa) | La calibración de la tasa de tokenización del Paper 8B requería mayor r(OAEI, Wage) de la que la forma multiplicativa entrega, pero la compatibilidad hacia atrás con la trilogía exigía preservar la multiplicatividad | Variante aditiva: r(OAEI, Wage) 0,58 → 0,66; convergencia con AIOE preservada en 0,80 |

El razonamiento completo del caso práctico, incluyendo cómo cada hallazgo empírico específico empujó la decisión metodológica, está documentado en §4.4, §5.4 y §6.5 del [documento de Metodología Consolidada](docs/ITEA_v3_0_Consolidated_Methodology.pdf).

---

## Inicio rápido

### R

```r
source("code/v3/itea_functions_v3.R")

library(readxl)
df <- read_excel("data/processed/ITEA_v3_0_Workbook.xlsx",
                 sheet = "ITEA_INDICATORS_v3.0", skip = 2)

df$ITEA_v30_check <- itea_v3(df$EAC, df$EIG, df$EIA)
df$IRA_v30_check  <- ira_v3(df$CA, df$`IRO v1.45 (legacy)`,
                            df$`GEE v2.1`, df$ITEA_v30_check, df$ICT)
df$OAEI_v30_check <- oaei_v3_mult(df$ITEA_v30_check, df$`GEE v2.1`,
                                   df$ICT, df$IPI)
```

### Python

```python
from code.v3.itea_functions_v3 import itea_v3, ira_v3, oaei_v3_mult, oaei_v3_add
import pandas as pd

df = pd.read_excel("data/processed/ITEA_v3_0_Workbook.xlsx",
                   sheet_name="ITEA_INDICATORS_v3.0", skiprows=2)
df['ITEA_v30_check'] = itea_v3(df['EAC'], df['EIG'], df['EIA'])
```

---

## Histórico de versiones

| Versión | Fecha | Cambios principales | Impacto |
|---------|-------|---------------------|---------|
| v1.0 | 2024-03 | Versión inicial: 8 indicadores, O\*NET 28.x | Baseline |
| v1.1 | 2024-09 | IRO seguridad institucional; ITEA forma aditiva | Medio |
| v1.2 | 2025-03 | Calibración OLS de GEE (ρ 0,259 → 0,927); IMO Hurdle+cap | Alto |
| v1.3 | 2025-04 | IPI nuevo indicador; IFS extracción CI | Medio |
| v1.45 | 2025-10 | IRO 4→2 ítems; GEE dual OLS+ordinal | Medio — última versión v1.x; archivada como tag `v1.45-legacy` |
| v2.0 | 2026-04 | Paper de metodología: tipología formativo/reflexivo | Alto — primer documento metodológico |
| v2.1 | 2026-04 | Memorándum: actualización de datos a O\*NET 30.2 | Medio |
| **v3.0** | **2026-04** | **ITEA z-score · IRA residualización triple · OAEI variante dual · caso práctico de la trilogía · preparación JOSS** | **Crítico — versión única autoritativa** |

---

## Citación

```bibtex
@software{garcia-lluis2026itea,
  title     = {ITEA Framework: A Multidimensional System for Measuring Occupational
               Exposure to Algorithmic Expropriation under the Agentic AI Regime},
  author    = {García-Lluis Valencia, Alberto},
  year      = {2026},
  version   = {3.0},
  doi       = {10.5281/zenodo.19578916},
  url       = {https://github.com/AVAL22/ITEA-Framework}
}
```

---

## Contacto

**Alberto García-Lluis Valencia** · Universidad Rey Juan Carlos · ORCID: [0009-0003-1438-1633](https://orcid.org/0009-0003-1438-1633) · alb.valencia@gmail.com

*ITEA Framework v3.0 — Hacer la expropiación algorítmica medible, multidimensional y accionable.*
