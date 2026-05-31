# ITEA v4.0 — Documento de diseño (spec)

Borrador 2026-05-31 · Autor: Alberto García-Lluis Valencia (URJC)
Estado: **propuesta para ratificar.** Fija el alcance de la integración ESCO y
qué significa, formalmente, "ITEA 4.0". Las decisiones marcadas 🟠 requieren
visto bueno del autor antes de implementar.

---

## 1. Qué es ITEA v4.0

**Definición propuesta:** versión de ITEA que integra ESCO/ISCO de forma nativa
y permite, en todo momento, análisis **comparativo y unificado** entre tres
entornos (O*NET, ESCO, Híbrido) sobre un eje común (ISCO-08), con la
**invarianza de medición demostrada** entre la estructura task-based y la de
competencias, y con **validación convergente europea** (índice JRC 2026).

Lo que v4.0 **no** es: no sustituye a O*NET ni compite con el JRC. ESCO entra
como capa complementaria de competencias; el JRC como benchmark externo.

**Decisión 1 — Alcance generacional. ✅ RESUELTA (2026-05-31): Opción A.**
v4.0 = solo **ITEA BRIDGE (US–UE)** = ITEA-US + ITEA-UE + el puente con invarianza
y validación JRC. IRC (L6) e ITEA Global (plano demanda + certificación) se difieren
a v4.x / horizonte teórico. **Matiz (Decisión 10):** entra una *semilla* del IDA en
v4.0 — un proxy estático de cambio basado en las Emerging Tasks de O*NET (IMO); el
IDA dinámico completo queda en v4.x. Alcance cerrado, tesis nítida, riesgo bajo.

---

## 2. Arquitectura de tres entornos (ya construida)

Eje común **ISCO-08 (4 dígitos)**, vía crosswalk SOC↔ISCO (877 SOC).

Nomenclatura de la familia (ver `ITEA_FAMILIA.md`): los tres "entornos" son, con
propiedad, **ITEA-US** (O*NET), **ITEA-UE** (ESCO) e **ITEA BRIDGE (US–UE)** (el
puente). v4.0 = la primera entrega completa de esos tres.

- **ITEA-US** (O*NET) — task-based, US, eje SOC. Indicadores v3.0 ya calculados.
- **ITEA-UE** (ESCO) — competence-based, EU, eje ISCO. Aporta nativamente la
  codificabilidad (K, reuseLevel). No modela tareas.
- **ITEA BRIDGE (US–UE)** — puente bilateral tarea→skill→ISCO. Donde nace ITEA-EU.

Capa de datos: `08_outputs/entornos/{onet,esco,hibrido,comparativo}/`; tabla
unificada `comparativo/itea_by_isco.parquet` (434 ISCO; 238 en los tres).

---

## 3. Catálogo de indicadores — definiciones resueltas

Todas las fórmulas v3.0 y sus componentes auxiliares (antes "por confirmar"):

| Indicador | Fórmula | Base de datos |
|-----------|---------|---------------|
| ITEA | z(EAC)+z(EIG)+z(EIA)/3 → min-max | O*NET descriptores |
| AEI/AXI | %HIGH·100 + %TRANS·50 + %HIGH_ALGO·200 | 47.810 tareas graduadas |
| GEE | norm(0,215·C_RL + 0,004·C_RW); ρ(Job Zone)=0,920 | O*NET ETE (Educ/Train/Exp) |
| ICT | 0,35·ITD + 0,30·ATE + 0,35·(1−DTS) | O*NET Skills/Work Activities/Work Context |
| IFS | 0,35·CDE + 0,40·DHS + 0,25·CC_comm (α=0,749) | O*NET Work Context/Activities |
| IPI | 0,70·CI_pres + 0,30·(1−CI_rem) | O*NET Work Context (presencial/remoto) |
| IEF | 0,35·DPF + 0,30·ERA + 0,35·DCF (α=0,919) | O*NET Work Context |
| IRA | 0,60·CA_norm + 0,40·IRO_residual_norm | O*NET (CA, IRO residualizado) |
| OAEI/OAXI | ITEA × GEE × ICT × (1−IPI) → [1,100] | composición de los anteriores |

**Hallazgo clave:** todos los auxiliares se construyen sobre **descriptores
O*NET a nivel de ocupación** (no de tarea). Eso significa que pueden **portarse
a ISCO por crosswalk** sin necesidad de ESCO. La única dimensión que ESCO aporta
de forma genuinamente nativa es la **codificabilidad (K)**; y la única tarea que
exige el mapa híbrido es el **AXI** (lo task-based puro).

---

## 4. Estrategia de portabilidad a Europa (la decisión central)

Para cada indicador hay tres vías posibles de llevarlo al eje ISCO:

- **(a) Carry-over** — tomar el valor O*NET de la ocupación y crosswalkear
  SOC→ISCO. Inmediato, pero arrastra la estructura del mercado laboral USA.
- **(b) Nativo-EU** — recomputar desde fuentes europeas. Verdaderamente europeo,
  pero más trabajo y cobertura parcial.
- **(c) Híbrido** — nativo donde hay equivalente EU, carry-over donde no.

**Decisión 2 — Vía de portabilidad. ✅ RESUELTA (2026-05-31): Opción híbrida.**
Nativo-EU donde Europa aporta mejor + carry-over donde no hay equivalente,
declarando cada celda. Tabla:

| Indicador | Vía propuesta | Fuente EU / justificación |
|-----------|---------------|---------------------------|
| **K / codificabilidad** | nativo-EU | reuseLevel de ESCO (ya disponible) |
| **AXI** | híbrido | tareas O*NET→skills ESCO (mapa) + grados |
| **GEE** | nativo-EU | **EQF** (autonomía-responsabilidad) sustituye Job Zone |
| ICT, IPI, IEF, IFS | carry-over | sin equivalente ESCO directo; O*NET→ISCO |
| ITEA (EAC/EIG/EIA) | híbrido | EIA/EAC vía mapa; EIG vía competencias K + carry-over |
| OAXI-EU | composición | recomponer con los anteriores en ISCO |
| Validación | nativo-EU | índice JRC 2026 (sustituye AIOE) |

*Racional:* lo que ESCO/EQF aportan mejor que O*NET (codificabilidad,
cualificación) se hace nativo; lo que no tiene equivalente europeo claro
(contexto físico/tecnológico) se transporta por crosswalk y se marca como tal.

---

## 5. Alcance definitivo por entorno (a ratificar)

**Decisión 3 — Set comprometido. ✅ RESUELTA (2026-05-31): Opción A (núcleo).**
Comprometer AXI, K, GEE y OAXI en los tres entornos; el resto completo en ITEA-US
y carry-over en BRIDGE; en ESCO puro solo lo nativo. Detalle:

- **Núcleo obligatorio en los 3 entornos:** AXI, codificabilidad (K), GEE, OAXI.
  Son el corazón de la tesis de expropiación y los que sostienen la comparación.
- **Completos en O*NET, carry-over a ISCO en Híbrido:** ITEA, ICT, IPI, IEF, IRA.
- **Solo donde es nativo, sin forzar:** en ESCO puro, únicamente K y los
  recuentos de competencias (essential/optional). No se inventa AXI en ESCO.

Esto evita el error de "fabricar" indicadores donde el entorno no da el dato
(principio de integridad): cada celda de la matriz declara su vía y su límite.

---

## 6. Trabajo pendiente para alcanzar v4.0

Mapeado a los pasos del pipeline:

1. **GEE-EU (EQF).** Descargar/mapear los 8 niveles EQF a ISCO; recalibrar GEE
   sustituyendo el ancla Job Zone. *Bloquea OAXI-EU.*
2. **OAXI-EU.** Recomponer ITEA×GEE×ICT×(1−IPI) en ISCO con las vías de §4;
   **calibrar el peso K** (hoy 0,25/0,5/0,75/1,0 son propuestos).
3. **Paso 8 — invarianza de medición** O*NET↔ESCO. El hito metodológico.
4. **Paso 9 — validación convergente** vs índice JRC 2026 (descargar JRC145832).
5. **Mapa v2.0-embeddings** (multilingüe, en GPU) y comparación de estabilidad
   vs v1.0-tfidf; **corpus ES** para el aterrizaje español (ISCO-08→CNO-11).
6. **Cobertura:** cerrar el hueco del crosswalk (877/1.016 SOC) y de ISCO
   (238/434 en los 3 entornos); descargar ESJS2 y Skills-Occupations Matrix.

---

## 7. Definition of Done — criterios para declarar v4.0

v4.0 se podrá declarar cerrada cuando:

- [ ] OAXI-EU calculado en ISCO y con peso K calibrado (no propuesto).
- [ ] GEE-EU anclado en EQF, con correlación documentada frente al GEE-O*NET.
- [ ] Prueba de invarianza de medición superada (umbral a fijar; p.ej. ΔCFI<0,01
      en invarianza métrica entre estructura task-based y de competencias).
- [ ] Validación convergente OAXI-EU ↔ JRC 2026 con r ≥ 0,70.
- [ ] Mapa en versión embeddings y estabilidad top-k documentada vs TF-IDF.
- [ ] Tabla unificada por ISCO completa y los 3 entornos reproducibles por script.
- [ ] Workbook ITEA v4.0 + documento de metodología + depósito Zenodo.

---

## 8. Entregables y versionado

- `ITEA_v4.0_Workbook.xlsx` — indicadores por ISCO en los 3 entornos.
- Documento de metodología v4.0 (extiende el consolidado v3.0).
- Paper ITEA-EU (invarianza + validación JRC); ventana JOSS.
- Depósito Zenodo con DOI de versión; tags en el repo público `Aval22/ITEA`.

---

## 9. Decisiones abiertas (para el autor)

1. 🟠 Alcance generacional: ¿v4.0 = solo ESCO, difiriendo IDA/IRC? (§1)
2. 🟠 Vía de portabilidad por indicador: ¿se acepta la propuesta híbrida? (§4)
3. 🟠 Set comprometido por entorno: ¿núcleo AXI/K/GEE/OAXI en los 3? (§5)
4. ✅ RESUELTA: invarianza **ΔCFI < 0,01** (configural→métrica→escalar);
   validación convergente OAXI-EU↔JRC **r ≥ 0,70** (coherente con AIOE del 8A).
5. ✅ RESUELTA: GEE-EU en **dos tiempos** — carry-over GEE-O*NET→ISCO para el
   OAXI-EU preliminar (valida la tubería), luego EQF nativo para la versión definitiva.

Una vez ratificadas, el siguiente paso operativo es **GEE-EU + OAXI-EU**
(desbloquean el núcleo), en paralelo al diseño de la prueba de invarianza.
