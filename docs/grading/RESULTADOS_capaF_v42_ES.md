# Capa F (ITEA 4.2): primeros resultados

**26-10-2026.** Construida con `scripts/grading/build_families.py` **después** del commit `fa627ec`, que fija el libro de criterios v0.1 y las hipótesis H21–H25 (decisión D29).

**Ficheros** (en `v4.0/outputs/grading/`):
- `task_families_v42.csv`: los 18.796 enunciados de tarea, con su vector de familia F1–F7 y de tipo T_A–T_E;
- `surface_by_family_v42.json`;
- `eurostat_ai_families.csv`: UE-27 y España, 2024–2025, 50 agregados NACE.

**Parámetros:**
- **En juego:** K ≥ 0,5124 y E ≥ 0,6198 (umbral central). Son 5.125 tareas.
- **Pesos:** importancia de la tarea dentro de su ocupación; **cada ocupación pesa igual**. Las cifras ponderadas por empleo van en el paper, con la OEWS.
- **Cobertura:** todas las tareas tienen enlace con una DWA (ninguna imputada).
- **Banda de sensibilidad:** 1.000 perturbaciones de los pesos de la regla (±20 %).

## 1. Qué familia de IA actúa sobre la superficie alienable

| Familia | Parte de la superficie alienable | Banda 5–95 % | Fuera de juego (media, como contraste) |
|---|---|---|---|
| F2. Generación de lenguaje o código | **32,2 %** | 31,1–33,2 % | 28,2 % |
| F1. Análisis de texto | **21,4 %** | 20,3–22,6 % | 7,8 % |
| F6. Automatización de flujos y apoyo a la decisión | **19,1 %** | 18,2–19,9 % | 8,4 % |
| F5. Aprendizaje automático para análisis y predicción | **18,1 %** | 17,3–19,0 % | 7,0 % |
| F3. Voz | 5,7 % | 5,0–6,4 % | 6,9 % |
| F4. Visión | 3,3 % | 3,0–3,7 % | 8,1 % |
| F7. Robótica | 0,3 % | 0,3–0,4 % | 33,7 % |

**Familia principal de cada tarea en juego:** F2 en el 43 %, F5 en el 25 %, F1 en el 18 %, F6 en el 13 %; visión y robótica en el 1,6 % entre las dos.

**H22 (descriptiva):** F1 + F2 = **53,5 %** (banda aproximada 51–56 %). **Se cumple la expectativa registrada** (> 50 %). Como depende de la regla, no valida nada; describe.

**Lectura:**
1. **La alienabilidad es sobre todo lingüística, pero no solo.** Un 37 % de la superficie corresponde al aprendizaje automático y a la automatización de flujos: las familias que trabajan sobre **registros** (regímenes 1–2 del paper). La alienación del saber hacer no empieza con los LLM; los LLM la amplían.
2. **Visión y robótica casi no intervienen en lo alienable.** Dominan fuera de juego (robótica: 34 % del trabajo no alienable), coherente con que K penaliza lo manual. Es la discrepancia conceptual pendiente para la v4.3: K mide la explicitud cognitiva, no la decisión.
3. **La banda es estrecha (±1 punto):** el reparto entre familias es robusto a perturbaciones moderadas de los pesos. Pero la robustez a la perturbación **no es validez**: la regla es un juicio y su validez depende de H21 (patentes) y H25 (juicio humano), aún sin contrastar.

## 2. Adopción por familia en la empresa (Eurostat, último año disponible)

España, % de empresas de 10 o más empleados (2024–2025):

| Sector | F1 Texto | F2 Generación | F3 Voz | F4 Visión | F5 Aprendizaje automático | F6 Flujos | F7 Robótica |
|---|---|---|---|---|---|---|---|
| Total (sin sector financiero) | 10,0 | 8,9 | 7,2 | 5,6 | 5,6 | 6,7 | 1,6 |
| Industria (C) | 7,4 | 6,5 | 4,7 | 4,1 | 4,1 | 4,6 | 2,5 |
| Construcción (F) | 5,0 | 4,2 | 4,2 | 2,7 | 1,8 | 2,8 | 0,8 |
| Comercio (G) | 8,4 | 6,3 | 6,7 | 5,1 | 4,4 | 5,5 | 1,2 |
| Información y comunicaciones (J) | 41,4 | 40,4 | 28,1 | 23,1 | 33,7 | 28,7 | 5,6 |
| Actividades profesionales (M) | 19,6 | 17,3 | 12,7 | 9,7 | 12,7 | 16,1 | 2,7 |
| Inmobiliarias (L68) | 23,1 | 18,0 | 5,1 | 6,4 | 5,0 | 10,1 | 0,9 |

**Primera observación, no contrastada (pertenece a H24):** el aprendizaje automático y la automatización de flujos suman el 37 % de la superficie alienable, pero su adopción empresarial es menor que la de las familias de texto, salvo en información y comunicaciones. El potencial de alienación por registros estaría menos explotado hoy que el lingüístico. **No se afirma hasta contrastar H24** a nivel sectorial, con el empleo por industria.

## 3. Estado de las hipótesis

| H | Estado |
|---|---|
| H21: regla frente a patentes | **Pendiente.** Hay que descargar el USPTO AIPD y calcular la similitud semántica |
| H22: F1 + F2 > 50 % | **Se cumple (53,5 %).** Descriptiva |
| H23: API frente a claude.ai, mayo de 2026 | **Pendiente.** Falta el fichero `aei_1p_api_2026-06-26.csv` |
| H24: superficie frente a adopción por sector | **Pendiente.** Hace falta el empleo por industria (OEWS por NAICS → NACE) |
| H25: regla frente a juicio humano | **Pendiente.** Muestra de unas 300 tareas y dos codificadores |

**Hasta que H21 y H25 se cumplan, la capa F se publica como medida en desarrollo**, no como medida validada (interpretación prevista en el registro).
