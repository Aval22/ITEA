# Decisión: dos índices EU separados — exposición vs expropiación

Fecha: 2026-05-31. Decisión del autor (opción 3). Este documento registra **la
decisión y sus razones**, según lo solicitado.

## La decisión

Se separa la medida europea en **dos índices relacionados pero distintos**:

- **IEA-EU — Índice de Exposición a IA (Europa).** Mide *exposición* (qué trabajo
  está expuesto a la IA), tipo JRC/AIOE. Sirve de **ancla de comparabilidad**: se
  valida contra benchmarks externos.
- **OAXI-EU — índice de expropiación (Europa).** Mide *expropiación* =
  exposición × **codificabilidad**. Es la **contribución distintiva de ITEA**:
  identifica qué trabajo expuesto es además codificable/expropiable. **Diverge del
  índice de exposición por diseño.**

## Por qué (las razones)

La validación cuantitativa contra el JRC (JRC145832, 102 ISCO-3 comunes) destapó tres
hechos que obligan a separar los constructos:

1. **`reuseLevel` (el K original) es un mal proxy de codificabilidad.** Correlaciona
   **negativo** con la exposición JRC (−0,33): las skills *occupation-specific* (K=1)
   son especializadas/tácitas → menos expuestas; las transversales → más. Iba al revés.
2. **`Auto_Grade` (automatabilidad clásica) es casi ortogonal a la exposición a IA**
   del JRC (r≈0,10). Automatizar no es lo mismo que estar expuesto a IA generativa.
3. **`CI_Grade` (codificación algorítmica de conocimiento tácito, HIGH_ALGO) sí alinea**
   con el JRC (r≈0,70), y **GEE** (cualificación) alinea fuerte (0,71/0,77).

**Conclusión conceptual:** "exposición a IA" (JRC) y "expropiación" (ITEA) son
constructos **relacionados pero distintos**. Forzar el OAXI a validar contra el JRC
lo convertiría en un duplicado del JRC y se perdería el aporte propio. La salida
correcta es tener (a) un índice de **exposición que valida** (comparabilidad
externa) y (b) un índice de **expropiación que aporta lo distintivo** (la
codificabilidad), aceptando —y explicando— su divergencia.

## Los dos índices (v1) y su validación

| Índice | Definición v1 | vs JRC (Pearson/Spearman) |
|--------|---------------|---------------------------|
| **IEA-EU** (exposición) | aditivo `0,5·GEE + 0,3·exp(Auto_Grade) + 0,2·ICT·(1−IPI)` | **0,76 / 0,78 ≥ 0,70 ✓** |
| **OAXI-EU** (expropiación) | `exposición × codificabilidad(CI_Grade)` | 0,63 / 0,71 (diverge, por diseño) |

Salida: `08_outputs/entornos/hibrido/occ_indices_EU_v1.parquet`. corr(IEA-EU,
OAXI-EU) = 0,64 (relacionados, no idénticos — como debe ser).

Nota honesta: el IEA-EU valida apoyado **sobre todo en GEE** (la cualificación);
el término `Auto_Grade` aporta poco (coherente con el hallazgo 2). Esto es
defendible —la exposición a IA se concentra en trabajo cognitivo de alta
cualificación, como reporta el propio JRC— pero hay que declararlo.

## Cambios que implica

- **Se jubila `reuseLevel` como K de expropiación.** La codificabilidad pasa a
  derivarse del **`CI_Grade` del AXI** (señal validada). `reuseLevel` queda como
  rasgo secundario (cristalización inter-ocupacional), no como peso de expropiación.
- v4.0 reporta **dos índices** (exposición + expropiación), no uno.

## Pendiente (sin sobreajustar al JRC)

- Afinar pesos del IEA-EU con criterio teórico (no maximizando r contra el JRC).
- Repetir tras la pasada de **embeddings**.
- Formalizar la invarianza (paso 8) con estos índices.
- Decidir si el OAXI-EU lleva backbone estructural (GEE/ICT) o se queda en
  exposición×codificabilidad puro.
