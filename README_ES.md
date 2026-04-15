# ITEA Framework — Índice de Triple Exposición a la Automatización

🌐 [English](README.md) · **Español** · [Português](README_PT.md) · [中文](README_ZH.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19578916.svg)](https://doi.org/10.5281/zenodo.19578916)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-blue)](https://itea-framework.streamlit.app)

> **Un framework multidimensional para medir la exposición ocupacional a la automatización, el desplazamiento por IA y la transformación del mercado laboral.**

## Descripción

El Framework ITEA proporciona 8 indicadores complementarios que cubren 1.016 ocupaciones de O\*NET 2024 (v29.1), superando las limitaciones de los índices binarios de automatización (Frey & Osborne, 2017):

| Indicador | Nombre completo | Dimensión | Tipo |
|-----------|----------------|-----------|------|
| **ITEA** | Índice de Triple Exposición a la Automatización | Exposición | Formativo |
| **IRO** | Índice de Resiliencia Ocupacional | Resiliencia | Reflexivo |
| **ICT** | Índice de Complejidad Técnica | Complejidad | Formativo |
| **IFS** | Índice de Fricción Social | Interacción social | Reflexivo |
| **IPI** | Índice de Presencialidad Interpersonal | Presencialidad | Formativo |
| **IEF** | Índice de Especificidad Funcional | Especificidad | Reflexivo |
| **GEE** | Gradiente Educación-Experiencia | Cualificación | Calibrado (OLS) |
| **IMO** | Índice de Mutación Ocupacional | Mutación | Modelo Hurdle |

## Características principales

- **Multidimensional**: 8 indicadores capturan diferentes facetas de la exposición a la automatización
- **Granular**: 1.016 ocupaciones individuales (cobertura completa de la economía de EE.UU.)
- **Dinámico**: IMO rastrea la evolución ocupacional a lo largo del tiempo
- **Validado**: α de Cronbach, VIF, tests de consistencia cruzada R↔Python
- **Abierto**: Fórmulas completas, código y datos para replicación

## Inicio rápido

### R
```r
source("code/R/itea_functions_v1.45.R")
itea <- calcular_itea(eac = 0.0, eig = 1.0, eia = 0.3)  # 0.4333
```

### Python
```python
from code.Python.itea_functions_v1_45 import *
itea = calcular_itea(eac=0.0, eig=1.0, eia=0.3)  # 0.4333
```

### Dashboard interactivo
Explora las 1.016 ocupaciones en: **https://itea-framework.streamlit.app**

## Estructura del repositorio

```
ITEA-Framework/
├── data/processed/          # Datos ocupacionales (Excel)
├── code/R/                  # Funciones R (8 indicadores)
├── code/Python/             # Funciones Python (8 indicadores)
├── docs/methodology/        # Documentación metodológica v1.0→v1.45
├── docs/guides/             # Guías de uso (ES + EN)
├── docs/analysis/           # Análisis interpretativo Infoempleo
├── docs/papers/             # Paper 02 (QE y empleo sénior)
├── figures/                 # 10 gráficos de análisis
├── paper/                   # Artículo académico (paper.md)
├── streamlit_app/           # Dashboard Streamlit
├── CITATION.cff             # Información de citación
└── LICENSE                  # Licencia MIT
```

## Citación

Si utiliza este framework en su investigación, por favor cite:

```bibtex
@techreport{garcia-lluis2026itea,
  title     = {ITEA: A Multidimensional Framework for Measuring Occupational 
               Exposure to Automation},
  author    = {García-Lluis Valencia, Alberto},
  year      = {2026},
  institution = {Universidad Rey Juan Carlos},
  doi       = {10.5281/zenodo.19578916},
  url       = {https://github.com/Aval22/ITEA}
}
```

## Contacto

**Alberto García-Lluis Valencia**  
Universidad Rey Juan Carlos, Madrid  
Programa de Investigación Doctoral — Economía Laboral  
ORCID: [0009-0003-1438-1633](https://orcid.org/0009-0003-1438-1633)

---
*ITEA Framework — Haciendo el riesgo de automatización medible, multidimensional y accionable.*
