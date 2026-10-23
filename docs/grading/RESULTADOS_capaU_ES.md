# Capa U: adopción y utilización por sector y país (issue #7)

**Ejecución:** 23-10-2026, `scripts/grading/build_adoption.py`.
**Fuente:** encuesta de Eurostat sobre el uso de las TIC en las empresas (`isoc_eb_iipn2`, `isoc_eb_ain2` e `isoc_eb_icsn2`), empresas de 10 o más empleados, en porcentaje de empresas, con el último año disponible en cada celda (2023–2025).
**Salidas** en `v4.0/outputs/grading/`:
- `eurostat_adoption_by_sector_raw.csv`: 4.929 celdas, con la fecha de descarga;
- `utilisation_by_sector.csv`: 2.557 celdas de país × sector × indicador, con U en tres escenarios.

## Definición

- **U = adopción × profundidad.** La adopción la mide Eurostat. La profundidad (la parte de las funciones del sistema que se usa de verdad) es un **supuesto declarado**: 0,10, 0,27 o 0,35 (decisión D10). No es una estimación.
- **Indicadores:**
  - ERP (`E_ERP1`);
  - CRM (`E_CRM1`, desde 2023);
  - inteligencia de negocio (`E_ITBI`);
  - cualquier software de gestión (`E_BSANY`);
  - integración de la cadena de suministro (`E_SISC`, solo 2023);
  - al menos una tecnología de IA (`E_AI_TANY`).
- **Cobertura:** 35 territorios (UE-27, países y agregados) y 13 sectores NACE: el total, C, D, E, F, G, H, I, J, L, M, N y el sector TIC.
- **Limitación:** **el sector financiero (NACE K) no está en estas tablas.** Para el piloto de finanzas hará falta otra fuente o un supuesto declarado.

## España frente a la UE-27 (último año, % de empresas)

| Sector | ERP ES | ERP UE | CRM ES | CRM UE | IA ES | IA UE |
|---|---|---|---|---|---|---|
| Total (sin finanzas) | 60,4 | 46,4 | 33,3 | 28,5 | 20,3 | 20,0 |
| C Industria manufacturera | 68,6 | 57,6 | 31,1 | 26,2 | 17,1 | 17,3 |
| G Comercio | 71,8 | 53,8 | 42,0 | 34,9 | 17,8 | 18,6 |
| H Transporte | 55,6 | 37,3 | 26,9 | 18,6 | 14,7 | 11,2 |
| J Información y comunicaciones | 75,7 | 61,3 | 63,3 | 63,1 | 60,6 | 62,5 |
| L Inmobiliarias | 67,6 | 50,8 | 66,0 | 39,6 | 34,4 | 24,8 |
| M Actividades profesionales | 63,9 | 47,9 | 38,0 | 36,2 | 38,4 | 40,4 |
| N Servicios administrativos | 47,0 | 41,5 | 31,2 | 30,5 | 18,8 | 19,9 |

**Lectura:** España adopta ERP por encima de la media de la UE en todos los sectores, pero no la supera en IA, salvo en inmobiliarias y transporte. Es el patrón que la capa U pretende recoger: tener el sistema no equivale a explotarlo. La hipótesis de que la IA aumenta la profundidad de uso (`METODOLOGIA_v0.2_ES.md`, capa U) se contrastará comparando estos sectores en el tiempo.
