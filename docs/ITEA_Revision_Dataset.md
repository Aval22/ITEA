# Revisión del data set de ITEA

> Auditoría interna del conjunto de datos canónico del framework (v3.0), en cuatro frentes:
> cobertura y ausencias, reproducibilidad, mapa al modelo de tres capas de ITEA 4.0, y coherencia
> documental. Documento de repositorio; los datos operativos siguen **bajo solicitud**.

Fecha de la revisión: **2026-07-01**. Fichero auditado: `ITEA-EU_Datos/07_workbooks_ITEA/ITEA_v3.0_Workbook.xlsx`.

---

## 0. Objeto y estructura

El data set canónico es el **workbook v3.0**: 12 hojas. La hoja de datos, `ITEA_INDICATORS_v3.0`, contiene **1.016 ocupaciones SOC de 6 dígitos × 27 campos** (base O*NET 30.2). El identificador `SOC Code` es **único, sin duplicados**. Campos: identificadores (SOC Code, Job Title, SOC Major, Job Zone), componentes (AEI, EAC, EIG, EIA, C_RL, C_RW, CA), indicadores (ITEA, IRA, IRO, ICT, IFS, IPI, IEF, GEE), compuestos (OAEI v2.1 / v3.0 / v3.0+ aditivo), y externos (AIOE, salario mediano, Δ rank). Rangos coherentes con lo esperado (ITEA y GEE normalizados en [0,1]; OAEI en [1,100]; AIOE en z-scores).

---

## 1. Frente 1 · Cobertura y ausencias

**Hallazgo principal:** una de cada siete ocupaciones no tiene valor en el índice estrella. De 1.016 ocupaciones, **878 tienen OAEI v3.0 y 138 (≈14 %) no**. La ausencia es **parcialmente sistemática**:

- **Ocupaciones militares (SOC 55): 100 % sin OAEI** (las 19). Es una exclusión *estructural* —O*NET no publica Job Zone/salario para el grupo militar—, no un error. **Debe declararse explícitamente.**
- Fuera de lo militar, la ausencia está *moderadamente repartida* (del 22 % en Community/Social y Computer/Math al 4 % en Install/Repair); no hay un segundo sesgo fuerte concentrado.

**Causa raíz de las 138 ausencias de OAEI:** las 138 carecen de **GEE** (cualificación) y 137 de **salario**; como el OAEI se compone con el GEE, sin GEE no hay OAEI. Un subconjunto de **93** carece además del **Job Zone** de O*NET → y por arrastre les faltan también AEI, EAC, EIG, EIA e **ITEA**. Hay, pues, dos huecos anidados: 93 sin base O*NET y ~45 más que tienen ITEA pero no GEE/salario.

**Impacto en la validación — RESUELTO:** el solapamiento OAEI × AIOE es de **769** ocupaciones. La propia hoja `AIOE_CONVERGENCE_v3.0` del workbook confirma **"769 common occupations"** y `r(OAEI v3.0+ additive, AIOE) = 0,7968 ≈ 0,797`, cifra que se reprodujo de forma independiente. Por tanto, **el número correcto es 769**, y el **«738» que citaban los README era erróneo → corregido a 769** (EN/ES/PT/ZH).

**Recomendaciones:** (a) declarar la exclusión militar en `LIMITATIONS` — hecho como *nota de cobertura* en README; (b) documentar por qué 138 ocupaciones carecen de GEE/salario (¿sin dato BLS de salario? ¿sin inputs de educación/experiencia?); (c) ~~reconciliar el *n* (738 vs 769)~~ **hecho**: corregido a 769 en los cuatro README.

| Grupo | N | Sin OAEI | % |
|---|---|---|---|
| Military | 19 | 19 | 100 % |
| Community/Social | 18 | 4 | 22 % |
| Computer/Math | 38 | 8 | 21 % |
| … (resto) | … | … | 4–20 % |
| **Total** | **1.016** | **138** | **14 %** |

---

## 2. Frente 2 · Reproducibilidad

**Resultado: correcto.** La suite de pruebas `code/v3/tests/test_itea_v3.py` (**14 tests**) reconcilia la salida del código con los valores almacenados en el workbook y **pasa 14/14** (`14 passed`). Existen implementaciones espejo en **R** (`code/v3/itea_functions_v3.R`) y **Python** (`code/v3/itea_functions_v3.py`), más la línea legacy v1.45. La cadena de cómputo declarada —`ITEA = itea_v3(EAC, EIG, EIA)`, `IRA = ira_v3(...)`, `OAEI = oaei_v3_mult(ITEA, GEE, ICT, IPI)`— es la que reproducen los tests.

**Recomendación:** ninguna correctiva; mantener los tests como *gate* de cada release (buena práctica ya adoptada, valorada de cara a JOSS).

---

## 3. Frente 3 · Mapa al modelo de tres capas (ITEA 4.0)

Cómo se sitúa el data set actual respecto a la arquitectura de ITEA 4.0 (expropiabilidad → evento → consecuencias):

| Capa (ITEA 4.0) | ¿En el data set v3.0? | Dónde / qué falta |
|---|---|---|
| **Expropiabilidad** (potencial medible) | ✅ **Completa** | Es el OAEI/AEI y sus componentes (ITEA·GEE·ICT·IPI). El data set *ya* es la capa de expropiabilidad. |
| **IES — soberanía** (el evento) | 🔴 No | Dimensión normativa (incumbencia + no-consentimiento); no derivable de estas columnas. |
| **IAV — apropiación** (la firma) | 🟠 Fuera de este workbook | Requiere panel de empresa; existe en `ICADE_GenAI_Panel/` (SEC/EDGAR) + caso MBB (Paper 8C), no a nivel SOC. |
| **IDE — dilución** (el mercado) | 🔴 No | Requiere el DiD en banca (márgenes vs diferenciales); dato por construir. |

**Lectura:** el workbook v3.0 cubre **íntegramente** la capa de *expropiabilidad*; las otras tres capas de ITEA 4.0 no están en él (una vive en el panel ICADE; dos son datos por construir). Coincide con el semáforo del spec de ITEA 4.0.

---

## 4. Frente 4 · Coherencia documental

Tras el renombrado *expropiación → expropiabilidad*, se verificó el texto interno del workbook (hojas `README_v3.0`, `METHODOLOGY_v3.0`, `LIMITATIONS_v3.0`): **no contienen la palabra «expropriation» ni «expropriability»** (0 ocurrencias) — el workbook se documenta con **siglas** (OAEI, AEI, ITEA), no con el término. **Conclusión: el renombrado no afecta al workbook**; el término vive en `README.md`/web (ya actualizados). Sin acción.

---

## 5. Síntesis y acciones

| Frente | Estado | Acción pendiente |
|---|---|---|
| Cobertura | ⚠️→✅ | Exclusión militar y hueco GEE/salario **documentados** en README (nota de cobertura); *n* de validación **corregido a 769** (era 738) en los 4 README. Queda por precisar el motivo BLS/educación de las 138. |
| Reproducibilidad | ✅ OK | Ninguna. |
| Mapa 3 capas | ✅ Claro | Expropiabilidad cubierta; IES/IDE por construir; IAV en panel ICADE. |
| Coherencia doc. | ✅ OK | Ninguna. |

El data set es **sólido y reproducible**; el único frente con trabajo es la **documentación de la cobertura** (ausencias sistemáticas del militar y del GEE/salario). Ninguna ausencia es un error de cómputo; son huecos de *input* que conviene declarar para blindar la validación ante un revisor.

---

## 6 · Actualización 2025 (salarios O\*NET/BLS + perfiles completos)

**Salarios refrescados 2024 → 2025** (fuente: BLS OEWS 2025, vía O\*NET). Script `04_crosswalk_salarios/actualizar_salarios_2025.py` (descarga reanudable) → `ONET_wages_2025.csv` y `Salarios_2025_ONET_actualizado.csv`.

- **Cobertura: 879 → 992 / 1016** con salario (**+116 huecos rellenados**). Quedan **24 sin dato** (19 `http_404` + 5 `sin_datos`): el núcleo estructural "All Other" + militar.
- **Cambio interanual** (n=876): mediana **+3,0 %** (Δ medio +$3.825); 805 suben, 69 bajan. Coherente con inflación salarial.
- **Corrección de calidad (importante):** **18 ocupaciones médicas** estaban *top-codeadas* a **$239.200** en 2024 (tope anual de BLS OEWS = $115/h × 2.080) — infravaloradas. El dato 2025 reporta su valor real (p. ej. Radiólogos $420.860). Se adopta el 2025 por ser **más preciso**; la "subida" es artefacto del top-coding, no un cambio real.
- **5 swings de muestra pequeña** señalados (ocupaciones diminutas, estimación BLS volátil): Models (−46 %), Makeup Artists (+93 %), I-O Psychologists (+77 %), Terrazzo Workers (+33 %), Timing Device Assemblers (+54 %). Adoptados con nota.
- Flags en el fichero: `updated` (853) · `new` (116) · `topcode_fixed` (18) · `smallsample_swing` (5) · `still_missing` (24).

**Perfiles O\*NET completos.** Script `02_ONET_30.2/construir_perfiles_onet.py` ensambla el perfil íntegro de cada ocupación **desde la base local O\*NET 30.2** (sin scraping): tareas (Core/relevancia), DWA, work activities, work context, knowledge/skills/abilities/work styles con sus valoraciones, RIASEC, Job Zone, tecnologías (Hot/In-Demand), relacionadas… Contiene *más* que la web (valoraciones completas, no solo el top-10). Salida: **1.016 JSON** en `perfiles_onet/` + `perfiles_onet_TODOS.jsonl`.

**Sobre recomputar OAEI/GEE para v3.1 — verificado y descartado.** Contra la intuición inicial, el **OAEI no usa el salario** (fórmulas reales: `OAEI_mult = ITEA×GEE×ICT×(1−IPI)`; `OAEI_add = 0,5·GEE+0,3·ITEA+0,2·ICT·(1−IPI)`; el GEE = `0,215·C_RL+0,004·C_RW`, de educación/experiencia O\*NET). Por tanto:

- Rellenar salarios **no reduce** el hueco de 138 sin OAEI.
- El hueco es **irrecuperable**: O\*NET **no tiene datos de educación/experiencia** para ninguna de esas 138 (solo los tiene para 878 = las que ya tienen GEE). Es exclusión estructural de O\*NET, no un fallo del workbook.
- Vía alternativa (GEE-proxy desde Job Zone) recuperaría **≤16** ocupaciones (solo esas tienen también IPI), mezclando GEE calibrado con proxy → coste metodológico alto, ganancia mínima. **No recomendado.**
- Efecto del refresh en la validez de criterio: r(OAEI additivo, salario) 0,660 → **0,628** (Pearson; Spearman plano 0,73). La leve caída la causan las 18 correcciones de top-coding médico y es **coherente con la tesis** (salario ≠ expropiabilidad; en la cima divergen).

**Entregable v3.1 real:** la **tabla de salarios 2025** (`Salarios_2025_ONET_actualizado.csv`), que mejora el análisis de sustitución/incentivo (dependiente de salario), no los índices. Los índices OAEI/ITEA/GEE se mantienen v3.0.

---

*Revisión interna del Programa ITEA · 2026. Documento vivo. Actualizado con el refresh 2025.*
