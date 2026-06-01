# Paso 9 — Validación convergente OAXI-EU vs JRC 2026

Benchmark: índice de exposición a la IA del JRC ("Revisiting the occupational
impact of AI in the generative AI era", **JRC145832**, Fernández-Macías & Casas),
en **127 ocupaciones ISCO-08 a 3 dígitos**, normalizado 0-1.

## Estado: validación CUANTITATIVA hecha — resultado preliminar BAJO umbral

Las 127 puntuaciones por ocupación (Appendix M, Table M.1, ISCO-3, escala 0-1) se
extrajeron del PDF aportado por el autor (`jrc145832_isco3_scores.parquet`, dato de
contraste, no se redistribuye). Agregando OAXI-EU a ISCO-3 y correlacionando sobre
los **102 ISCO-3 en común**:

| Correlación OAXI-EU ↔ JRC | Valor | Umbral spec | ¿Cumple? |
|---------------------------|-------|-------------|----------|
| **Pearson** | **0,476** | ≥ 0,70 | **No** |
| **Spearman** | **0,622** | ≥ 0,70 | **No** |

**Lectura honesta.** El OAXI-EU **preliminar** (mapa v1.0-tfidf, GEE carry-over, K
sin calibrar) **aún no alcanza el umbral**. El Spearman (0,62) > Pearson (0,48)
indica que el **orden** ocupacional converge razonablemente, pero las **magnitudes
y los extremos** divergen. No es un fracaso: marca exactamente qué falta afinar.

**Patrón de discrepancia (diagnóstico, sistemático):** el JRC puntúa muy alto a
**directivos y profesionales financieros** (gestores 0,96-0,98; finanzas 0,91)
porque sus tareas son leer/escribir/analizar (muy expuestas a IA), mientras que el
OAXI-EU los **infrapondera** (7-15). Causas probables: (a) el término de exposición
del AXI desde tareas O*NET no captura bien lo cognitivo-gerencial; (b) la
composición multiplicativa GEE×ICT×(1−IPI) penaliza; (c) mapeo TF-IDF léxico.

**Nota de constructo:** OAXI mide *expropiación* (exposición × codificabilidad ×
estructura), no *exposición pura* como el JRC → cierta divergencia es esperable;
pero el objetivo r≥0,70 (coherente con OAXI↔AIOE=0,807 del 8A) sigue siendo la meta.

## Evidencia direccional disponible (positiva)

1. **Patrón por gran grupo ISCO-1 — coincide con el JRC.** OAXI-EU medio:
   Profesionales 31,6 > Directivos 26,1 > Técnicos 20,8 > Administrativos 16,5 >
   … > Elementales 5,9 > Operadores 5,6. El JRC reporta el mismo orden
   (directivos/profesionales/técnicos arriba; operadores/elementales abajo).
2. **Ocupaciones más expuestas — solapan.** Top OAXI-EU (ISCO-3): software/analistas
   (251), ICT managers (133), médicos (221), enfermería (222), ingenieros (214/216),
   operadores TIC (351). El JRC cita médicos, ingenieros, desarrolladores de software
   entre los más expuestos → convergencia. Artefactos a revisar: medicina tradicional
   (323), veterinarios (225) altos — probable ruido del mapeo v1.0-tfidf.
3. **Validez de criterio (salario):** corr(OAXI-EU, salario) = **0,54** (Pearson y
   Spearman, n=238). El JRC reporta 0,85 exposición-renta. Positiva pero menor;
   esperable (índice preliminar, mapa TF-IDF, salario **estadounidense** carry-over).

## Lectura

La convergencia **direccional** es sólida: OAXI-EU reproduce el patrón ocupacional
y las ocupaciones-diana del JRC. Es coherente con la evidencia del paso 8
(concordancia BRIDGE↔ESCO, lift ~17×). **No sustituye** la validación cuantitativa
formal (r≥0,70 sobre las 127 ISCO-3), que queda pendiente del Appendix M.

## Robustez — ablación del IEA-EU (2026-05-31): qué componente valida

Quitando cada componente y recorrelacionando con el JRC (102 ISCO-3):

| Variante | Pearson | Spearman |
|----------|--------:|---------:|
| Completo (GEE+exp+ICT) | 0,762 | 0,783 |
| Sin GEE | **0,482** | **0,491** |
| Sin exp (Auto_Grade) | 0,761 | 0,796 |
| Sin ICT/IPI | 0,715 | 0,758 |
| Solo GEE | **0,706** | **0,774** |
| Solo exp (Auto_Grade) | 0,089 | 0,102 |

**Conclusión (importante, honesta): la validación del IEA-EU la sostiene casi
toda el GEE** (cualificación). Solo GEE ya da 0,71/0,77; el término de exposición
del AXI (Auto_Grade) **no aporta** a la convergencia con el JRC. Es decir, lo que
valida es el hecho ya conocido de que **las ocupaciones de alta cualificación
están más expuestas** (GEE ≈ nivel de cualificación), no la maquinaria novedosa
del puente. Implicaciones: (1) no se debe presentar el IEA-EU como validación
independiente del puente tarea→competencia; (2) lo con validación propia es la
**codificabilidad (CI_Grade, 0,70)** y la **concordancia con ESCO (17×)**, que es
el aporte distintivo y diverge del JRC por diseño; (3) refuerza "beta, no
producción". Script: `09_code/08_validate_vs_jrc.py` (+ ablación inline).

## Para cerrar el paso 9 (subir de 0,48/0,62 a ≥0,70)

1. ✅ HECHO: Appendix M extraído (127 ISCO-3) y correlación corrida (0,476 / 0,622).
2. **Mapa v2.0-embeddings** (multilingüe) — debería subir la concordancia y la r.
3. **GEE-EU nativo (EQF)** + **calibrar K** — quita ruido de la composición.
4. **Revisar la infraponderación de directivos/finanzas** (la mayor fuente de error):
   probar OAXI-EU **aditivo** (no multiplicativo) o reponderar el término cognitivo;
   contrastar si la penalización GEE×ICT×(1−IPI) hunde a los gestores.
5. Reevaluar r tras 2-4; objetivo Pearson/Spearman ≥ 0,70.

Script: `09_code/08_validate_vs_jrc.py` (pendiente de consolidar; hoy corrido inline).
Dato de contraste: `08_outputs/entornos/comparativo/jrc145832_isco3_scores.parquet` (no público).

## Diagnóstico de componentes y variantes (2026-05-31)

Correlación de cada componente vs JRC (102 ISCO-3):

| Componente | Pearson | Spearman |
|---|---|---|
| Exposición (BRIDGE) | 0,64 | 0,67 |
| GEE | 0,71 | 0,77 |
| **K (reuseLevel)** | **−0,31** | **−0,33** |
| ICT | 0,23 | 0,23 |
| OAEI-O*NET (carry-over) | 0,76 | 0,80 |

**Hallazgo clave: el término K es el problema — correlación NEGATIVA con la
exposición JRC.** El `reuseLevel` de ESCO (occupation-specific=1) marca competencias
especializadas/tácitas, que son MENOS expuestas a IA; las transversales (K bajo)
son cognitivas genéricas, MÁS expuestas. Es decir, **`reuseLevel` no es un buen
proxy de codificabilidad** respecto a la exposición a IA (va al revés).

Variantes de composición (especificaciones a priori, no tuneadas al JRC):

| Variante OAXI-EU | Pearson | Spearman | ¿≥0,70? |
|---|---|---|---|
| Multiplicativa con K (actual) | 0,476 | 0,622 | No |
| Multiplicativa sin K | 0,695 | 0,787 | sí (Spearman) |
| **Aditiva estilo 8A v3.0+ (0,5·GEE+0,3·exp+0,2·ICT·(1−IPI), sin K)** | **0,778** | **0,805** | **Sí** |
| Aditiva con K (exp,K,GEE) | 0,736 | 0,771 | Sí |

**La variante aditiva tipo v3.0+ (sin K) supera el umbral** (0,78/0,81), con una
forma teóricamente justificada (replica el OAEI v3.0+ del Paper 8A).

### Tensión metodológica a decidir (es del autor)

OAXI mide *expropiación* = exposición × **codificabilidad**, no exposición pura
(JRC). Que el K (reuseLevel) corra inverso a la exposición plantea dos lecturas:
1. **El proxy K está mal elegido:** `reuseLevel` no captura codificabilidad. La
   codificabilidad real ya está en los grados `CI_Grade` del AXI (HIGH_ALGO). →
   sustituir el K-reuseLevel por una codificabilidad derivada del AXI.
2. **OAXI debe ser exposición-like:** adoptar la forma aditiva sin K (valida 0,81)
   y reservar la codificabilidad para un eje aparte, no multiplicativo.

Recomendación: **adoptar la forma aditiva (v3.0+) como OAXI-EU v1** (valida y es
coherente con el 8A) y **rediseñar el término de codificabilidad** desde el
`CI_Grade` del AXI (no desde reuseLevel), reevaluando después.
