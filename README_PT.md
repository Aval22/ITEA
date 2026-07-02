# ITEA Framework — Índice de Transformação e Expropriabilidade Algorítmica

🌐 [English](README.md) · [Español](README_ES.md) · **Português** · [中文](README_ZH.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19578915.svg)](https://doi.org/10.5281/zenodo.19578915)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-3.0-blue)]()

> **Um framework multidimensional para medir a expropriabilidade algorítmica ocupacional sob o regime de IA Agentic.**

---

## O que é ITEA v3.0?

O Framework ITEA fornece dez indicadores complementares cobrindo 1.016 ocupações SOC 6-dígitos do O\*NET 30.2, projetados para medir a expropriabilidade algorítmica ocupacional no regime de IA Agentic — distinto mas complementar aos índices de automação ao nível da tarefa da tradição Frey-Osborne (2017) ou medidas de exposição baseadas em habilidades como o benchmark AIOE de Felten, Raj e Seamans (2021).

Validação convergente externa contra o benchmark AIOE sobre 769 ocupações SOC 6-dígitos comuns: **r(OAEI v3.0+, AIOE) = 0,797**.

| Indicador | Nome completo | Dimensão | Tipo | Estado |
|-----------|--------------|----------|------|--------|
| **ITEA** | Índice de Transformação e Expropriabilidade Algorítmica | Exposição | Formativo (agregação z-score) | **Revisado em v3.0** |
| **IRA** | Índice de Resiliência Adaptativa | Resiliência | Reflexivo (residualização tripla) | **Revisado em v3.0** |
| **ICT** | Índice de Complexidade Técnica | Complexidade | Formativo | Estável desde v2.0 |
| **IFS** | Índice de Fricção Social | Interação social | Reflexivo | Estável desde v2.0 |
| **IPI** | Índice de Presencialidade Interpessoal | Presencialidade | Formativo | Estável desde v1.3 |
| **IEF** | Índice de Especificidade Funcional | Especificidade | Reflexivo | Estável desde v2.0 |
| **GEE** | Gradiente Educação-Experiência | Qualificação | Calibrado (OLS+ordinal) | Estável desde v1.45 |
| **IMO** | Índice de Mutação Ocupacional | Mutação | Modelo Hurdle | Estável desde v1.2 |
| **OAEI** | Índice Ocupacional de Expropriabilidade Algorítmica | Composto operacional | Multiplicativo + aditivo | **Revisado em v3.0 — variante dupla** |
| **AEI** | Índice de Expropriabilidade Algorítmica | Benchmark interno | Auxiliar | Estável desde v2.0 |

---

## Por que a versão 3.0? Evidência de um projeto de pesquisa vivo

Este repositório avança de **v1.45 (outubro 2025)** para **v3.0 (abril 2026)**, arquivando a versão anterior como tag [`v1.45-legacy`](https://github.com/Aval22/ITEA/releases/tag/v1.45-legacy). A transição não é cosmética. Reflete uma revisão metodológica maior motivada por um caso prático documentado — três artigos de pesquisa (a trilogia 8A/8B/8C) que colocaram o framework em uso empírico ativo e, ao fazê-lo, expuseram três limitações específicas da v2.1. Documentar essa evolução explicitamente faz parte da preparação para submissão ao [Journal of Open Source Software](https://joss.theoj.org/) (janela alvo: meados de 2026), que valoriza evidências de uso na comunidade e evolução metodológica fundamentada.

### A trilogia como caso prático

Três artigos de pesquisa em circulação ativa em abril de 2026 motivaram cada uma das três revisões centrais em v3.0:

- **Paper 8A — *"The Structural Flaw: Industrial Labour Contract Inadequacy under Agentic AI"*** (García-Lluis Valencia, 2026a). → motivou a **agregação ITEA por z-score**.
- **Paper 8B — *"Beyond the Pigouvian Trap: Tokenised Intellectual Capital..."*** (García-Lluis Valencia, 2026b). → motivou o **OAEI de variante dupla**.
- **Paper 8C — *"QE and Senior Workforce Restructuring: A Labour Liability Transmission Channel"*** (García-Lluis Valencia, 2026c). → motivou o **IRA com residualização tripla**.

| Mudança em v3.0 | Motivação empírica da trilogia | Ganho de validação |
|-----------------|-------------------------------|---------------------|
| ITEA: normalização z-score antes de média com pesos iguais | A narrativa do top-20 do Paper 8A divergia do ranking algorítmico v2.1 | r(ITEA, AEI): 0,71 → 0,89; r(ITEA, AIOE): 0,36 → 0,43 |
| IRA: residualização tripla contra (GEE, ITEA, ICT) | A análise de quadrantes GEE × IRA do Paper 8C mostrava separação Q1-Q4 inflada | r(IRA, ITEA): 0,28 → 0,14; 84% de variância preservada |
| OAEI: arquitetura de variante dupla | A calibração da taxa de tokenização do Paper 8B requeria maior r(OAEI, Wage) | Variante aditiva: r(OAEI, Wage) 0,58 → 0,66 |

O raciocínio completo do caso prático está documentado em §4.4, §5.4 e §6.5 do [documento de Metodologia Consolidada](docs/ITEA_v3_0_Consolidated_Methodology.pdf).

---

## Início rápido

### R

```r
source("code/v3/itea_functions_v3.R")
df$ITEA_v30 <- itea_v3(df$EAC, df$EIG, df$EIA)
df$IRA_v30  <- ira_v3(df$CA, df$IRO_v145, df$GEE, df$ITEA_v30, df$ICT)
df$OAEI_v30 <- oaei_v3_mult(df$ITEA_v30, df$GEE, df$ICT, df$IPI)
```

### Python

```python
from code.v3.itea_functions_v3 import itea_v3, ira_v3, oaei_v3_mult, oaei_v3_add
df['ITEA_v30'] = itea_v3(df['EAC'], df['EIG'], df['EIA'])
```

---

## Histórico de versões

| Versão | Data | Mudanças principais | Impacto |
|---------|------|---------------------|---------|
| v1.0 | 2024-03 | Versão inicial: 8 indicadores | Baseline |
| v1.45 | 2025-10 | Última versão v1.x; arquivada como tag `v1.45-legacy` | Médio |
| v2.0 | 2026-04 | Primeiro documento metodológico | Alto |
| v2.1 | 2026-04 | Memorando: atualização para O\*NET 30.2 | Médio |
| **v3.0** | **2026-04** | **ITEA z-score · IRA tripla · OAEI dupla · trilogia · preparação JOSS** | **Crítico** |

---

## Citação

```bibtex
@software{garcia-lluis2026itea,
  title   = {ITEA Framework},
  author  = {García-Lluis Valencia, Alberto},
  year    = {2026},
  version = {3.0},
  doi     = {10.5281/zenodo.20083102},
  url     = {https://github.com/Aval22/ITEA}
}
```

---

## Contato

**Alberto García-Lluis Valencia** · Universidad Rey Juan Carlos · ORCID: [0009-0003-1438-1633](https://orcid.org/0009-0003-1438-1633) · alb.valencia@gmail.com

*ITEA Framework v3.0 — Tornar a expropriabilidade algorítmica mensurável, multidimensional e acionável.*
