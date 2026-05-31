# ITEA — Instancias país (arranque)

Scaffold de las nuevas instancias nacionales de la familia ITEA. Cada subcarpeta
es el dossier de una instancia, lista para recibir datos. Material de
investigación (gitignored).

## Convención de versionado (dos ejes ortogonales)

- **Versión de familia / arquitectura:** `ITEA v4.0` (los 3 entornos, el BRIDGE,
  ISCO como eje). Es la generación del método compartido.
- **Versión de instancia:** la madurez de ITEA sobre los datos de *ese* país.
  Independiente de la versión de familia.

| Instancia | Versión de instancia | Clase de medición |
|-----------|----------------------|-------------------|
| ITEA-US | **v3.0** (madura, publicada) | N1 nativa |
| ITEA-UE | **v1.0** (primer build EU) | N1 nativa |
| ITEA-JP | **v0 → v1.0 al lanzar** | N1 nativa |
| ITEA-KR | **v0 → v1.0 al lanzar** | N1 nativa |
| ITEA-IN | **v0 → v1.0 al lanzar** | N3 imputada |

Una instancia puede ir por su v1.0 dentro de la familia v4.0; no se confunden.

## Cola de prioridad (por validez científica)

1. **Japón (ITEA-JP)** — Nivel 1 nativo + benchmark JILPT. *El más importante.*
2. **Corea (ITEA-KR)** — Nivel 1 nativo.
3. **Grupo imputado (Nivel 3):** **India (ITEA-IN)** / LatAm antes que China.

Australia (ASC) queda fuera de la cola por validez: su clasificación deriva de
O*NET (Nivel 2) → circularidad. Sirve como aterrizaje/crosswalk, no como punto
independiente.

## Patrón común de construcción de una instancia

1. Identificar el sistema nativo y su **eje ocupacional** → crosswalk a **ISCO-08**.
2. Conseguir los **descriptores/estándares** (nativos si N1; imputar de O*NET si N3).
3. Calcular el **AXI/OAXI** sobre el eje del país, expresado en ISCO.
4. **ITEA BRIDGE (A–B)** contra US o EU: crosswalk + invarianza + validación.
5. Anclar el GEE (Job Zone-análogo / marco de cualificaciones nacional).
