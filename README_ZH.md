# ITEA 框架 — 转型与算法可剥夺性指数

🌐 [English](README.md) · [Español](README_ES.md) · [Português](README_PT.md) · **中文**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19578915.svg)](https://doi.org/10.5281/zenodo.19578915)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-3.0-blue)]()

> **一个多维框架，用于衡量在 Agentic AI 体制下的职业算法可剥夺性。**

---

## 什么是 ITEA v3.0？

ITEA 框架提供十个互补指标，涵盖来自 O\*NET 30.2 的 1,016 个 SOC 6 位职业，旨在衡量 Agentic AI 体制下的职业算法可剥夺性——与 Frey-Osborne (2017) 传统的任务级自动化指数或 Felten、Raj 和 Seamans (2021) 的 AIOE 基准等基于能力的暴露衡量不同但互补。

针对 AIOE 基准的外部收敛验证，覆盖 769 个共同的 SOC 6 位职业：**r(OAEI v3.0+, AIOE) = 0.797**。

| 指标 | 全称 | 维度 | 类型 | 状态 |
|------|------|------|------|------|
| **ITEA** | 转型与算法可剥夺性指数 | 暴露程度 | 形成性（z-score 聚合）| **v3.0 已修订** |
| **IRA** | 适应性韧性指数 | 韧性 | 反映性（三重残差化）| **v3.0 已修订** |
| **ICT** | 技术复杂性指数 | 复杂性 | 形成性 | 自 v2.0 起稳定 |
| **IFS** | 社会摩擦指数 | 社会互动 | 反映性 | 自 v2.0 起稳定 |
| **IPI** | 人际在场指数 | 在场性 | 形成性 | 自 v1.3 起稳定 |
| **IEF** | 功能特异性指数 | 特异性 | 反映性 | 自 v2.0 起稳定 |
| **GEE** | 教育-经验梯度 | 资质 | 校准（OLS+顺序）| 自 v1.45 起稳定 |
| **IMO** | 职业变异指数 | 变异 | Hurdle 模型 | 自 v1.2 起稳定 |
| **OAEI** | 职业算法可剥夺性指数 | 操作性合成 | 乘法（标准）+ 加法（替代）| **v3.0 已修订——双变体** |
| **AEI** | 算法可剥夺性指数 | 内部基准 | 辅助 | 自 v2.0 起稳定 |

---

## 为什么是 3.0 版本？一个活跃研究项目的证据

本仓库从 **v1.45（2025 年 10 月）** 推进至 **v3.0（2026 年 4 月）**，将之前版本归档为 [`v1.45-legacy`](https://github.com/Aval22/ITEA/releases/tag/v1.45-legacy) 标签。这一过渡并非表面修改，而是反映了由一个有据可查的案例研究所推动的重大方法论修订——三篇研究论文（三部曲 8A/8B/8C）将该框架投入到积极的实证使用中，并在此过程中暴露了 v2.1 的三个具体局限。明确记录这一演变是该框架准备提交给 [Journal of Open Source Software](https://joss.theoj.org/) 的一部分（目标窗口：2026 年中），该期刊重视社区使用证据和有原则的方法论演变。

### 三部曲作为案例研究

2026 年 4 月在积极流通中的三篇研究论文，分别推动了 v3.0 的三项核心修订：

- **Paper 8A — *"The Structural Flaw: Industrial Labour Contract Inadequacy under Agentic AI"*** (García-Lluis Valencia, 2026a)。→ 推动了 **ITEA z-score 聚合**。
- **Paper 8B — *"Beyond the Pigouvian Trap: Tokenised Intellectual Capital..."*** (García-Lluis Valencia, 2026b)。→ 推动了 **OAEI 双变体**。
- **Paper 8C — *"QE and Senior Workforce Restructuring: A Labour Liability Transmission Channel"*** (García-Lluis Valencia, 2026c)。→ 推动了 **IRA 三重残差化**。

| v3.0 变更 | 来自三部曲的实证动机 | 验证收益 |
|-----------|---------------------|----------|
| ITEA：等权平均前 z-score 标准化 | Paper 8A 的前 20 名叙述与 v2.1 的算法排名分歧；分量方差不对称稀释了 EIA Agentic 体制信号 | r(ITEA, AEI)：0.71 → 0.89；r(ITEA, AIOE)：0.36 → 0.43 |
| IRA：针对 (GEE, ITEA, ICT) 的三重残差化 | Paper 8C 的 GEE × IRA 象限分析显示 Q1-Q4 分离因 v2.1 单变量残差化下的 IRA-ITEA 残余相关而被夸大 | r(IRA, ITEA)：0.28 → 0.14；保留 84% 的方差 |
| OAEI：双变体架构（乘法标准 + 加法替代）| Paper 8B 的代币化率校准要求比乘法形式更高的 r(OAEI, Wage)，但三部曲向后兼容性要求保留乘法性 | 加法变体：r(OAEI, Wage) 0.58 → 0.66 |

完整的案例研究推理记录在[整合方法论文档](docs/ITEA_v3_0_Consolidated_Methodology.pdf) §4.4、§5.4 和 §6.5 中。

---

## 快速开始

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

## 版本历史

| 版本 | 日期 | 主要变更 | 影响 |
|------|------|----------|------|
| v1.0 | 2024-03 | 初始版本：8 个指标 | 基线 |
| v1.45 | 2025-10 | 最后的 v1.x 版本；归档为 `v1.45-legacy` 标签 | 中等 |
| v2.0 | 2026-04 | 第一份方法论文档 | 高 |
| v2.1 | 2026-04 | 备忘录：数据更新至 O\*NET 30.2 | 中等 |
| **v3.0** | **2026-04** | **ITEA z-score · IRA 三重 · OAEI 双变体 · 三部曲 · JOSS 准备** | **关键** |

---

## 引用

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

## 联系方式

**Alberto García-Lluis Valencia** · Universidad Rey Juan Carlos · ORCID: [0009-0003-1438-1633](https://orcid.org/0009-0003-1438-1633) · alb.valencia@gmail.com

*ITEA Framework v3.0 — 让算法剥夺变得可衡量、多维和可操作。*
