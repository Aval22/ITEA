# Paso 8 — Invarianza de medición O*NET↔ESCO

Pregunta: ¿la estructura **task-based** (O*NET) y la **competence-based** (ESCO)
miden el mismo constructo ocupacional? Si el puente tarea→competencia reproduce
el perfil de competencias que la propia ESCO asigna a cada ocupación, es
evidencia de invarianza.

## Evidencia empírica (concordancia BRIDGE↔ESCO) — HECHO

Script `09_code/07_bridge_concordance.py`; salida
`08_outputs/entornos/comparativo/bridge_concordance_by_isco.parquet`. Sobre **238
grupos ISCO** (los presentes en los tres entornos):

| Métrica | Valor | Lectura |
|---------|-------|---------|
| **lift (vs azar)** | **media 17,0 · mediana 11,6** | el puente acierta competencias esenciales de ESCO ~12-17× más que el azar |
| % ISCO con lift > 2 | **87,8 %** | la concordancia es sistemática, no anecdótica |
| recall esencial | media 0,088 | recupera ~9 % de las esenciales de ESCO (suelo de la v1.0) |
| precision | 0,120 | de las skills que surface el puente, el 12 % las endosa ESCO |
| Jaccard | 0,043 | solape absoluto modesto |

**Interpretación.** La señal **direccional es fuerte** (lift ~17×): el puente no
es ruido, converge con el perfil nativo de ESCO muy por encima del azar — primera
evidencia de invarianza. El **nivel absoluto es bajo** y es esperable: (1) mapeo
**v1.0-tfidf** (léxico, no semántico); (2) se usa el **top-1** skill por tarea →
el puente surface un subconjunto; (3) **agregación a grupo ISCO** (mezcla varias
ocupaciones). Se prevé que recall/precision suban con la pasada de **embeddings**.

## Lo que falta para la invarianza FORMAL (pendiente)

Esto es evidencia de concordancia, **no** la prueba multigrupo formal que fija el
spec (ΔCFI < 0,01). La invarianza formal requiere:

1. **Indicadores a nivel de ítem** del constructo (no conjuntos de skills): p.ej.
   puntuaciones continuas de exposición/codificabilidad por ocupación en cada
   estructura (AXI desde tareas vs K/competencias desde ESCO).
2. Un **modelo de medición** (CFA multigrupo) con los dos "grupos" = las dos
   estructuras, contrastando invarianza configural → métrica → escalar.
3. Entorno estadístico (p.ej. `semopy`/lavaan) y N suficiente por grupo.
4. Idealmente, repetir tras la pasada de **embeddings** (la v1.0-tfidf marca el suelo).

**Plan:** (a) construir las puntuaciones por ocupación en ambas estructuras;
(b) correr la CFA multigrupo; (c) reportar ΔCFI. La concordancia actual ya
justifica seguir: el puente es válido por encima del azar.
