# La familia ITEA — arquitectura y nomenclatura

Decisión de estructuración 2026-05-31. Documento canónico de nombres: define
qué es cada miembro de la familia ITEA y cómo se relacionan. Sustituye el uso
provisional del término "BRIDGE" (que antes englobaba la propuesta normativa).

---

## Tres tipos de entidad

### 1. `ITEA-{país}` — instancias nacionales

Una implementación del marco ITEA sobre el sistema ocupacional **nativo** de un
país o región, con sus indicadores expresados sobre el eje común **ISCO-08**.

| Instancia | Sistema base | Paradigma | Clase de medición | Estado |
|-----------|--------------|-----------|-------------------|--------|
| **ITEA-US** | O*NET 30.2 | task-based | N1 nativa independiente | ✅ v3.0 |
| **ITEA-UE** | ESCO v1.2.1 | competence-based | N1 nativa independiente | 🔧 en construcción |
| **ITEA-AU** | ASC / OSCA | híbrido AU | **N2 derivada de O*NET** ⚠️ | ⬜ futuro |
| **ITEA-JP** | jobtag (日本版O-NET) | incumbentes | N1 nativa independiente | ⬜ futuro |
| **ITEA-KR** | KNOW | incumbentes | N1 nativa independiente | ⬜ futuro |
| **ITEA-CN / ITEA-LatAm** | 大典 / SINCO / CNO | clasificación pura | **N3 imputada** ⚠️ | ⬜ futuro |

Cada instancia **hereda su clase de medición** (N1/N2/N3), que determina qué
clase de afirmación científica permite. ⚠️ ITEA-AU es N2 (la ASC se construyó
mapeando O*NET): tratarla como medición independiente introduce circularidad.

### 2. `ITEA BRIDGE` — marco puente bilateral A↔B

No es un país: es la **junta metodológica entre dos instancias**. Contiene:

1. Crosswalk entre los ejes ocupacionales de A y B (vía ISCO-08).
2. **Prueba de invarianza de medición** entre las dos estructuras.
3. Validación convergente de A contra el benchmark de B (o externo).

Cada par produce una instancia BRIDGE nombrada: **ITEA BRIDGE (US–UE)** es la
primera y la que estamos construyendo (el "entorno híbrido" + tabla comparativa).
Pares futuros: BRIDGE (US–JP), BRIDGE (UE–AU)… BRIDGE es **tejido conectivo
empírico**: convierte dos instancias aisladas en una comparación válida.

### 3. `ITEA Global` — nuestra propuesta normativa

El modelo **óptimo / de referencia** que (a) sintetiza las best practices de
todos los sistemas analizados y (b) añade nuestras innovaciones. No describe
ningún país existente: es la propuesta de cómo *debería* medirse el sistema
ocupación–competencia–demanda. Sus tres innovaciones (detalle en
`ITEA_BRIDGE_concepto.md`, que es el documento de ITEA Global):

- **Tres planos:** OFERTA (educación/ESCO) · CONTENIDO (incumbentes/O*NET) ·
  **DEMANDA** (vacantes — el hueco que ningún sistema integra).
- **Lente de expropiación:** AXI × codificabilidad (K), que atraviesa los tres planos.
- **Eje de certificación:** acreditar conocimiento vs **certificar solvencia
  demostrada** → brújula de microcredenciales.

ITEA Global es la **contribución teórica**; BRIDGE es el **método empírico** que
la hace comparable entre países.

---

## Cómo encaja lo ya construido

| Artefacto actual (`ITEA-EU_Datos/`) | En la familia |
|-------------------------------------|---------------|
| `08_outputs/entornos/onet/` | **ITEA-US** |
| `08_outputs/entornos/esco/` | **ITEA-UE** |
| `08_outputs/entornos/hibrido/` + `comparativo/itea_by_isco.parquet` | **ITEA BRIDGE (US–UE)** |
| `dashboard.html` (pestañas O*NET/ESCO/Híbrido/Comparativo) | vista de las 2 instancias + su BRIDGE |
| `ITEA_BRIDGE_concepto.md` (3 planos + certificación) | **ITEA Global** (propuesta) |
| `ITEA_v4_0_SPEC_DISENO.md` | spec de la primera entrega = ITEA-US + ITEA-UE + BRIDGE(US–UE) |

---

## Implicación para el versionado

- **v4.0** = primera entrega completa de un BRIDGE: ITEA-US + ITEA-UE +
  ITEA BRIDGE (US–UE), con invarianza y validación JRC.
- **v4.x** = nuevas instancias país (ITEA-JP primero, N1) y sus BRIDGE.
- **ITEA Global** = horizonte normativo / paper teórico; incorpora el plano de
  demanda y la certificación de solvencia cuando maduren las fuentes (Skills-OVATE).

> Nomenclatura a propagar en todos los documentos y código: usar `ITEA-US`,
> `ITEA-UE`, `ITEA BRIDGE (A–B)` e `ITEA Global` de forma consistente.
