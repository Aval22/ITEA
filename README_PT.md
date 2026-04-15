# ITEA Framework — Índice de Tripla Exposição à Automação

🌐 [English](README.md) · [Español](README_ES.md) · **Português** · [中文](README_ZH.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19578916.svg)](https://doi.org/10.5281/zenodo.19578916)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-blue)](https://itea-framework.streamlit.app)

> **Um framework multidimensional para medir a exposição ocupacional à automação, ao deslocamento por IA e à transformação do mercado de trabalho.**

## Descrição

O Framework ITEA fornece 8 indicadores complementares cobrindo 1.016 ocupações do O\*NET 2024 (v29.1), superando as limitações dos índices binários de automação (Frey & Osborne, 2017):

| Indicador | Nome completo | Dimensão | Tipo |
|-----------|--------------|----------|------|
| **ITEA** | Índice de Tripla Exposição à Automação | Exposição | Formativo |
| **IRO** | Índice de Resiliência Ocupacional | Resiliência | Reflexivo |
| **ICT** | Índice de Complexidade Técnica | Complexidade | Formativo |
| **IFS** | Índice de Fricção Social | Interação social | Reflexivo |
| **IPI** | Índice de Presencialidade Interpessoal | Presencialidade | Formativo |
| **IEF** | Índice de Especificidade Funcional | Especificidade | Reflexivo |
| **GEE** | Gradiente Educação-Experiência | Qualificação | Calibrado (OLS) |
| **IMO** | Índice de Mutação Ocupacional | Mutação | Modelo Hurdle |

## Características principais

- **Multidimensional**: 8 indicadores capturam diferentes facetas da exposição à automação
- **Granular**: 1.016 ocupações individuais (cobertura completa da economia dos EUA)
- **Dinâmico**: IMO rastreia a evolução ocupacional ao longo do tempo
- **Validado**: α de Cronbach, VIF, testes de consistência cruzada R↔Python
- **Aberto**: Fórmulas completas, código e dados para replicação

## Início rápido

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

### Dashboard interativo
Explore as 1.016 ocupações em: **https://itea-framework.streamlit.app**

## Estrutura do repositório

```
ITEA-Framework/
├── data/processed/          # Dados ocupacionais (Excel)
├── code/R/                  # Funções R (8 indicadores)
├── code/Python/             # Funções Python (8 indicadores)
├── docs/methodology/        # Documentação metodológica v1.0→v1.45
├── docs/guides/             # Guias de uso (ES + EN)
├── docs/analysis/           # Análise interpretativa Infoempleo
├── docs/papers/             # Paper 02 (QE e emprego sênior)
├── figures/                 # 10 gráficos de análise
├── paper/                   # Artigo acadêmico (paper.md)
├── streamlit_app/           # Dashboard Streamlit
├── CITATION.cff             # Informação de citação
└── LICENSE                  # Licença MIT
```

## Citação

Se utilizar este framework na sua pesquisa, por favor cite:

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

## Contato

**Alberto García-Lluis Valencia**  
Universidad Rey Juan Carlos, Madrid  
Programa de Pesquisa Doutoral — Economia do Trabalho  
ORCID: [0009-0003-1438-1633](https://orcid.org/0009-0003-1438-1633)

---
*ITEA Framework — Tornando o risco de automação mensurável, multidimensional e acionável.*
