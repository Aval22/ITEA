# ITEA Framework — Índice de Triple Exposición a la Automatización

[![DOI](https://img.shields.io/badge/DOI-Pending-blue)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![O*NET](https://img.shields.io/badge/O*NET-2024%20v29.1-green)]()
[![Version](https://img.shields.io/badge/Version-1.45-orange)]()

> **A multidimensional framework for measuring occupational exposure to automation, AI displacement, and labor market transformation.**

## Overview

The ITEA Framework provides 8 complementary indicators covering 1,016 occupations from O\*NET 2024 (v29.1), addressing the limitations of binary automation indices (e.g., Frey & Osborne, 2017):

| Indicator | Full Name | Dimension | Type |
|-----------|-----------|-----------|------|
| **ITEA** | Triple Automation Exposure Index | Exposure | Formative |
| **IRO** | Occupational Resilience Index | Resilience | Reflective |
| **ICT** | Technical Complexity Index | Complexity | Formative |
| **IFS** | Social Friction Index | Social interaction | Reflective |
| **IPI** | Interpersonal Presence Index | Presentiality | Formative |
| **IEF** | Functional Specificity Index | Specificity | Reflective |
| **GEE** | Education-Experience Gradient | Qualification | Calibrated (OLS) |
| **IMO** | Occupational Mutation Index | Mutation | Hurdle model |

## Key Features

- **Multidimensional**: 8 indicators capture different facets of automation exposure
- **Granular**: 1,016 individual occupations (complete U.S. economy coverage)
- **Dynamic**: IMO tracks occupational evolution over time
- **Validated**: Cronbach's α, VIF, cross-language R↔Python consistency tests
- **Open**: Full formulas, code, and data for replication

## Repository Structure

```
ITEA-Framework/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── .gitignore
│
├── data/
│   ├── raw/                           # O*NET source extracts (pending)
│   └── processed/
│       ├── Research_Data_Workbook_ITEA_v1.35.xlsx   # Main data (current)
│       ├── Research_Data_Workbook_ITEA_v1.2.xlsx    # Historical
│       └── Analisis_Infoempleo_Adecco_ITEA_2023_2024.xlsx  # Spanish validation
│
├── code/
│   ├── R/
│   │   └── itea_functions_v1.45.R     # All 8 indicator functions
│   └── Python/
│       └── itea_functions_v1_45.py    # All 8 indicator functions
│
├── docs/
│   ├── methodology/
│   │   ├── ITEA_Metodologia_v1_45.docx   # Current methodology (complete)
│   │   ├── ITEA_Metodologia_v1_4.docx
│   │   ├── ITEA_Metodologia_v1_3.docx
│   │   ├── ITEA_Metodologia_v1_2.docx
│   │   ├── ITEA_v1_1_Robustness_Report.docx
│   │   └── ITEA_v1_2_Notas_de_Version_Anexo.docx
│   ├── guides/
│   │   ├── Guia_de_Uso_ITEA_v1_3.docx          # User guide (ES)
│   │   ├── ITEA_v1_35_User_Guide_EN.docx       # User guide (EN)
│   │   ├── Guia_Didactica_Workbook_ITEA_v1_3.docx
│   │   ├── Workbook_User_Guide_ITEA_v1_3_EN.docx
│   │   └── Anexo_Guia_Estilos_Visualizacion_ITEA_v1_3.docx
│   ├── analysis/
│   │   └── Interpretacion_Datos_Infoempleo_ITEA_v6_FINAL.docx
│   ├── papers/
│   │   └── Paper_02_QE_Reestructuracion_Empleo_Senior.docx
│   └── collaboration/
│       ├── MK_ITEA_v1_3_Research_Collaboration_ES.docx
│       └── MK_ITEA_v1_3_Research_Collaboration_EN.docx
│
├── figures/
│   ├── fig1_paradoja.png              # Adoption paradox
│   ├── fig2_formacion.png             # Training gap
│   ├── fig3_salarios_aei.png          # Wage structure × AEI
│   ├── fig4_deciles.png               # D10/D1 compression
│   ├── fig5_ccaa.png                  # Regional inequality
│   ├── fig6_tijera.png                # Scissors effect
│   ├── fig7_dcf_occupations.png       # DCF by occupation
│   ├── fig8_fiscal.png                # Fiscal externalities
│   ├── fig9_variables_map.png         # LLR variable map
│   └── fig10_dualidad.png             # Spain-US duality
│
└── reports/                           # Generated reports (future)
```

## Quick Start

### R
```r
source("code/R/itea_functions_v1.45.R")

# Calculate ITEA for a single occupation
itea <- calcular_itea(eac = 0.0, eig = 1.0, eia = 0.3)
# Result: 0.4333

# Calculate all indicators
library(readxl)
df <- read_excel("data/processed/Research_Data_Workbook_ITEA_v1.35.xlsx",
                 sheet = "ITEA_8_INDICADORES_v1.3")
```

### Python
```python
from code.Python.itea_functions_v1_45 import *

# Calculate ITEA
itea = calcular_itea(eac=0.0, eig=1.0, eia=0.3)
# Result: 0.4333

# Load data
import pandas as pd
df = pd.read_excel("data/processed/Research_Data_Workbook_ITEA_v1.35.xlsx",
                   sheet_name="ITEA_8_INDICADORES_v1.3")
```

## Version History

| Version | Date | Key Changes | Impact |
|---------|------|-------------|--------|
| v1.0 | 2024-03 | Initial release | Baseline |
| v1.1 | 2024-09 | IRO: institutional security; ITEA: additive | Medium |
| v1.2 | 2025-03 | GEE: OLS calibration (ρ .259→.927); IMO: Hurdle+cap | **High** |
| v1.3 | 2026-04 | IPI: new indicator; IFS: CI extraction | Medium |
| **v1.45** | **2026-10** | **IRO: CC 4→2 items; GEE: dual OLS+ordinal** | **Medium** |

## Related Papers

1. **Paper 02** — *Quantitative Easing and Senior Employment Restructuring: A Labour Liability Restructuring Channel* (García-Lluis Valencia, 2026). Working paper, URJC. → `docs/papers/`

2. **Paper 03** — *QE, Algorithmic Expropriation, and the Dual Displacement Equilibrium* (in preparation).

3. **Paper 04** — *A Three-Pillar Contractual Model for Algorithmic Expropriation* (in preparation, targeting *Industrial and Corporate Change*).

## Data Sources

- **O\*NET 2024 v29.1**: 1,016 occupations, 47,810 task statements. U.S. Department of Labor.
- **BLS OES**: Occupational wage data by percentile.
- **Infoempleo-Adecco 2023-2024**: Spanish labor market validation.
- **Monitor Adecco de Salarios 2025**: Eurostat/INE wage data for Spain.
- **Informe Grados Economía y ADE 2026**: Educational obsolescence data (17 countries, 680 programs).

## Citation

```bibtex
@techreport{garcia-lluis2026itea,
  title     = {ITEA: A Multidimensional Framework for Measuring Occupational 
               Exposure to Automation},
  author    = {García-Lluis Valencia, Alberto},
  year      = {2026},
  institution = {Universidad Rey Juan Carlos},
  type      = {Working Paper},
  note      = {Version 1.45. Available at https://github.com/[username]/ITEA-Framework}
}
```

## License

This work is licensed under [MIT](LICENSE).

- **Academic use**: Free with citation
- **Commercial use**: Contact the author
- **Data**: O\*NET data follows U.S. DOL public domain terms

## Contact

**Alberto García-Lluis Valencia**  
Universidad Rey Juan Carlos, Madrid  
Doctoral Research Program — Labor Economics  
[Email pending] · [ORCID pending]

---

*ITEA Framework — Making automation risk measurable, multidimensional, and actionable.*
