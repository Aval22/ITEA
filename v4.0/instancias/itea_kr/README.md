# ITEA-KR — dossier de arranque (Corea del Sur)

Estado: **iniciada (scaffold)**. Versión de instancia: v0 → v1.0 al lanzar.
Prioridad: **#2** (Nivel 1 nativo).

## Sistema nativo

**KNOW (Korea Network for Occupations and Workers)** — gestionado por **KEIS
(Korea Employment Information Service)**, bajo el Ministry of Employment and
Labor. Sitio: <https://www.keis.or.kr/keis/en/index.do>.
- KEIS fundado en 1979; primer *Korea Dictionary of Occupational Titles* en 1986.
- Encuesta anual a trabajadores en activo (*Korean Occupational Information
  Survey of Incumbents*) desde 2001; dominios casi calcados del Content Model de
  O*NET (capacidades/valores, actividades laborales, entorno, conocimientos).
- 5ª edición integrada del diccionario (2020): ~**12.816 ocupaciones**.

## Clase de medición

**Nivel 1 (nativa e independiente).** Encuesta propia a incumbentes.

## Consideraciones

- **Ventaja:** estructura de dominios muy O*NET → mapeo de descriptores directo.
- **Reto:** granularidad de **12.816 ocupaciones** frente a ~1.000 de O*NET →
  el crosswalk a ISCO-08 es trabajoso (muchos-a-uno) y hay que agregar.
- **No tiene** un benchmark de automatización publicado equivalente al JILPT
  japonés → la validación externa es más débil que en ITEA-JP.

## Eje ocupacional y crosswalk

Ocupación KECO (Korean Employment Classification of Occupations) → (crosswalk) →
**ISCO-08** → comparación con US/UE.

## Plan de construcción (ITEA-KR)

1. Obtener los descriptores KNOW por ocupación (KECO).
2. Crosswalk/agregación KECO (12.816) → ISCO-08.
3. AXI-KR nativo desde las actividades/tareas KNOW.
4. **ITEA BRIDGE (US–KR o UE–KR)**: invarianza + validación.

## Pendiente / a confirmar

- Acceso a los microdatos KNOW (¿descarga KEIS, API?); idioma (KR).
- Si KNOW modela "tareas" explícitas o solo actividades generales (afecta al AXI).

Fuentes: keis.or.kr · KNOW (Korea Network for Occupations and Workers)
