# ITEA 框架 — 自动化三重暴露指数

🌐 [English](README.md) · [Español](README_ES.md) · [Português](README_PT.md) · **中文**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19578916.svg)](https://doi.org/10.5281/zenodo.19578916)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-blue)](https://itea-framework.streamlit.app)

> **一个多维框架，用于衡量职业自动化暴露、人工智能替代和劳动力市场转型。**

## 概述

ITEA框架提供8个互补指标，涵盖O\*NET 2024（v29.1）中的1,016个职业，克服了二元自动化指数的局限性（Frey & Osborne, 2017）：

| 指标 | 全称 | 维度 | 类型 |
|------|------|------|------|
| **ITEA** | 自动化三重暴露指数 | 暴露程度 | 形成性 |
| **IRO** | 职业韧性指数 | 韧性 | 反映性 |
| **ICT** | 技术复杂性指数 | 复杂性 | 形成性 |
| **IFS** | 社会摩擦指数 | 社会互动 | 反映性 |
| **IPI** | 人际在场指数 | 在场性 | 形成性 |
| **IEF** | 功能特异性指数 | 特异性 | 反映性 |
| **GEE** | 教育-经验梯度 | 资质 | 校准（OLS） |
| **IMO** | 职业变异指数 | 变异 | Hurdle模型 |

## 主要特点

- **多维性**：8个指标捕捉自动化暴露的不同方面
- **粒度性**：1,016个独立职业（美国经济完整覆盖）
- **动态性**：IMO追踪职业随时间的演变
- **经验证**：Cronbach α系数、VIF、R↔Python跨语言一致性测试
- **开放性**：完整的公式、代码和数据可供复制

## 快速开始

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

### 交互式仪表板
在以下网址探索1,016个职业：**https://itea-framework.streamlit.app**

## 仓库结构

```
ITEA-Framework/
├── data/processed/          # 职业数据（Excel）
├── code/R/                  # R函数（8个指标）
├── code/Python/             # Python函数（8个指标）
├── docs/methodology/        # 方法论文档 v1.0→v1.45
├── docs/guides/             # 使用指南（西班牙语 + 英语）
├── docs/analysis/           # Infoempleo解释性分析
├── docs/papers/             # 论文02（量化宽松与高级就业）
├── figures/                 # 10个分析图表
├── paper/                   # 学术论文（paper.md）
├── streamlit_app/           # Streamlit仪表板
├── CITATION.cff             # 引用信息
└── LICENSE                  # MIT许可证
```

## 引用

如果您在研究中使用了此框架，请引用：

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

## 联系方式

**Alberto García-Lluis Valencia**  
马德里胡安·卡洛斯国王大学  
博士研究项目 — 劳动经济学  
ORCID: [0009-0003-1438-1633](https://orcid.org/0009-0003-1438-1633)

---
*ITEA框架 — 让自动化风险可衡量、多维化且可操作。*
