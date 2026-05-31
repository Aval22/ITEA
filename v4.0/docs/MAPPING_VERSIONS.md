# task_skill_map — mapa canónico tarea AXI → competencia ESCO

`task_skill_map.parquet` es el **artefacto canónico y evolucionable** del mapeo
entre las tareas graduadas del AXI y las competencias ESCO. No es preliminar:
cada regeneración queda auto-documentada en `task_skill_map.meta.json`
(procedencia, sha256 de entradas/salida, estadísticas) y cada fila lleva las
columnas `method` y `map_version`, de modo que distintas pasadas pueden
compararse o concatenarse sin ambigüedad.

## Esquema de la tabla

Una fila por (tarea × top-k skill). Columnas:

`task_id` · `task_text` · `rank` (1..k) · `similarity` · `esco_skill` ·
`esco_uri` · `skillType` · `reuseLevel` · `k_weight` · `explicacion` (frase en
lenguaje natural) · `method` · `map_version` · `Auto_Grade` · `CI_Grade`.

`task_id` = `task_uid` único del AXI (`AXI00001`…), trazable a `soc_task`
(`SOC_CODE_TaskID`) vía `axi_tasks_input.parquet`.

## Versionado

`map_version` sigue `MAJOR.MINOR-método`:
- **MAJOR** cambia con el método o el universo de datos (tfidf → embeddings, EN → bilingüe).
- **MINOR** cambia con ajustes de parámetros (top-k, pesos K, limpieza de texto).

| Versión | Método | Corpus | Estado | Notas |
|---------|--------|--------|--------|-------|
| `1.0-tfidf` | TF-IDF + coseno (EN↔EN) | ESCO v1.2.1 EN | ✅ **ACTUAL** | 47.810 tareas AXI, top-5, sim. media top-1 = 0,307 |
| `2.0-embeddings` | sentence-transformers `paraphrase-multilingual-MiniLM-L12-v2` | ESCO v1.2.1 EN | ⬜ pendiente | requiere GPU/máquina local; mejor calidad semántica |
| `2.1-embeddings-es` | embeddings multilingües | ESCO v1.2.1 EN+ES | ⬜ pendiente | aterrizaje español; descargar skills_es/occupations_es |

Las versiones superadas se conservan en `_archivo/` (no borrar: sirven de línea
base para medir estabilidad del top-k entre métodos).

## Cómo regenerar / evolucionar

> Nota: tras la reorganización en entornos, los artefactos viven en
> `08_outputs/entornos/` (`esco/`, `onet/`, `hibrido/`). Rutas actualizadas abajo.

Pasada actual (reproducible):

```
python3 ../09_code/02_map_tasks_to_skills.py \
  --skills entornos/esco/esco_skills_corpus.parquet \
  --tasks  entornos/onet/axi_tasks_input.parquet \
  --task-text-col task_statement --task-id-col task_uid \
  --topk 5 --method tfidf --map-version 1.0-tfidf --esco-version v1.2.1 \
  --out entornos/hibrido/task_skill_map.parquet
```

Pasada de embeddings (en máquina con GPU; el flag ya está cableado):

```
pip install sentence-transformers
python3 ../09_code/02_map_tasks_to_skills.py ... --method embeddings --map-version 2.0-embeddings \
  --out task_skill_map_v2.parquet
```

Comparar estabilidad entre versiones: unir por `task_id`+`rank` los dos parquet
y medir solapamiento del top-k y correlación de `similarity`.

## Roadmap

1. Pasada `2.0-embeddings` en local y comparación de estabilidad vs `1.0-tfidf`.
2. Agregar a ocupación vía `occupationSkillRelations` → ISCO (paso 7), ponderando
   tareas con `Task Ratings` de O*NET.
3. Prueba de invarianza de medición O*NET↔ESCO (paso 8): contrastar la estructura
   de competencias derivada del mapa con los perfiles O*NET (Skills/Knowledge/
   Abilities/Work Activities) y la capa DWA.
4. Validación convergente vs índice JRC 2026 (127 ISCO-3).
