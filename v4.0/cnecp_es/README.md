# CNECP (INCUAL) — sustrato para ITEA-ES y el GEE-EU

Primer artefacto estructurado del **aterrizaje español (ITEA-ES)**, extraído del
listado oficial del **Catálogo Nacional de Estándares de Competencias
Profesionales** (CNECP, INCUAL, edición enero 2026). Procedencia y base legal en
`_PROVENANCE.txt`. Material de investigación (gitignored).

## Qué hay aquí

- **`cnecp_familias.csv`** — las **28 familias profesionales** con el reparto de
  Estándares de Competencia Profesional (ECP) por nivel: **N1=232, N2=1.091,
  N3=1.307 → 2.630 ECP** en total. Integridad verificada por suma de columnas
  contra el listado oficial. Incluye la familia nueva *Inteligencia Artificial y
  Data (IAD)* (5 ECP, todos Nivel 3) y *Actividades y Competencias Transversales (ACT)*.
- **`cnecp_niveles_descriptores.csv`** — los **descriptores de los 3 niveles** de
  competencia (Conocimientos · Capacidades · **Responsabilidad y Autonomía**),
  con un campo `orden_autonomia` (1<2<3).

## Cómo alimenta a ITEA

**GEE-EU (ancla EQF — el cuello de botella del núcleo v4.0).** La dimensión
*Responsabilidad y Autonomía* del CNECP es el descriptor de autonomía del EQF en
clave española y escalonado por nivel. Da una **escala ordinal de autonomía**
(N1→N3) anclable a cada ECP/ocupación, que es justo lo que el GEE necesita en
Europa (sustituto del Job Zone de O*NET). Es la materia prima de la fase 2 del
GEE-EU (decisión 3 del spec).

**Eje de certificación (ITEA Global).** Cada ECP es certificable por la vía de
**acreditación de competencias (PAC)** —desempeño demostrado, no examen—, lo que
da una contraparte institucional real al eje "certificar solvencia vs acreditar
conocimiento".

**ITEA-ES.** Las familias y niveles son el esqueleto para una instancia española
sobre eje CNO-11 (y, vía ESCO, ISCO-08), cerrando la estimación por analogía del
Paper 8A.

## Pendiente

- Ingerir el **listado completo de ECP** (2.630 entradas, código `ECPnnnn_n` +
  título) a una tabla fila-a-fila.
- Mapear **ECP/familia ↔ CNO-11 ↔ ISCO-08 ↔ ESCO** (puente del aterrizaje ES).
- Convertir `orden_autonomia` en un **score GEE-EU** por ocupación.
