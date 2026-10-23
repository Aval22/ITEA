# OAXI-EU reconstruido con la graduación nueva (vista previa, capa 1)

**Ejecución:** 23-10-2026, `scripts/grading/build_oaxi_eu_v41.py`, con K1 y E1 de la capa estructural.
**Salidas** en `v4.0/outputs/grading/`:
- `oaxi_eu_layer1.csv`: el índice;
- `occupation_scores_layer1.csv`: las puntuaciones por ocupación;
- `oaxi_eu_layer1.meta.json`: los metadatos.

**Estado:** es una **vista previa**, no el índice v4.1. Este se construirá cuando estén las capas 2–3 y la combinación. Basta volver a ejecutar el mismo *script* con `--grades` y `--label v41`.

## Qué cambia respecto a OAXI-EU v4.0

| | v4.0 (AXI heredado) | Vista previa v4.1 (capa 1) |
|---|---|---|
| Entrada | Proporción de tareas con grado alto, en 47.810 enunciados de O\*NET 29.1 | K1 y E1 continuos de las 18.796 tareas de O\*NET 30.2 |
| Tareas perdidas al emparejar | 23.920 (la mitad) | Ninguna |
| Agregación | Tarea → DWA → ocupación → ISCO-08 | Igual |
| κ | 0,40 | 0,40, sin recalibrar (D17) |
| Grupos ISCO-08 | 428 | 428 |

## Resultados

- **Acuerdo con OAXI-EU v4.0:** Spearman 0,75 y Pearson 0,68 en los 428 grupos, pero solo **3 de los 20 primeros** coinciden. El orden general se parece; la cabeza del índice cambia mucho.
- **Convergencia con el JRC145832** a tres dígitos ISCO: Pearson 0,82 y Spearman 0,84 (127 grupos). **No es una validación independiente:** la capa 1 y el índice del JRC se basan en capacidades (D17).

## Lectura

1. **El índice cambia de perfil.**
   - **v4.0:** lo encabezan profesiones científicas y técnicas, como meteorólogos, administradores de sistemas o desarrolladores.
   - **Vista previa:** lo encabezan ocupaciones de gestión, análisis y comercio, como compradores, analistas de organización, analistas financieros o gerentes de comercio.

   Es coherente con lo que mide la capa 1, que es contenido cognitivo no social. Pero también refleja su limitación: **K1 apenas distingue entre tareas de una misma actividad** (solo el 5,3 % de la varianza está dentro de cada actividad general, H5).
2. **Algunos casos piden prudencia.** Que los «tenderos» (5221) puntúen como los gerentes de comercio (1420) se debe a que comparten las mismas actividades y una sola ocupación de O\*NET. Las capas semánticas deben resolverlo.
3. **No se publica como resultado del índice** hasta tener la graduación completa. Sirve para comprobar que la cadena funciona de principio a fin con las notas nuevas.
