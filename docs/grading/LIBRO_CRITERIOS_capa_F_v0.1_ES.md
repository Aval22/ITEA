# Libro de criterios de la capa F (familias de IA)

**Versión 0.1. Fijada el 26-10-2026, antes de calcular ningún resultado con estas reglas.** Desarrolla `DISENO_capa_F_familias_IA_v0.1_ES.md`. Las reglas no se modifican a la vista de los resultados; si cambian, se crea la v0.2 con su fecha y su motivo, y se registra la decisión.

**Implementación:** `src/itea/grading/families.py`.

## 1. Qué produce

Para cada tarea de O\*NET 30.2:
- un **vector de familia** F1–F7 que suma 1;
- un **vector de tipo de tarea** A–E que suma 1.

**El vector de familia es condicional a la exposición.** Responde a *si la tarea se hace con IA, con qué familia*, no a *cuánto*. El *cuánto* sigue siendo E (y K para la alienabilidad). La superficie alienable de una familia es la suma, sobre las tareas en juego, de su peso en el trabajo por su parte de la familia.

## 2. Familias (eje 1)

| Código | Familia | Indicador de Eurostat (`isoc_eb_ai`, `isoc_eb_ain2`) |
|---|---|---|
| F1 | Análisis de texto (minería de textos, recuperación, grafos de conocimiento) | E_AI_TTM |
| F2 | Generación de lenguaje o código (modelos de lenguaje generativos) | E_AI_TNLG |
| F3 | Voz (reconocimiento y síntesis) | E_AI_TSR |
| F4 | Visión (reconocimiento y procesamiento de imagen) | E_AI_TIR |
| F5 | Aprendizaje automático para análisis de datos y predicción | E_AI_TML |
| F6 | Automatización de flujos y apoyo a la decisión (RPA con IA, reglas, optimización) | E_AI_TPA |
| F7 | Robótica y movimiento autónomo | E_AI_TAR |

## 3. Regla estructural: actividad de trabajo generalizada (GWA) → familia

Cada tarea se enlaza con sus DWA mediante `Tasks to DWAs.txt`, y cada DWA con su GWA mediante `DWA Reference.txt`. El vector de la tarea es la media de los vectores de las GWA de sus DWA. Una tarea sin DWA recibe el vector medio de su ocupación y se marca como tal.

**Pesos por GWA** (juicio documentado del diseño; se valida en la §6). Criterio: qué familia ejecutaría la parte automatizable de la actividad según el estado de la técnica en 2025–2026.

| GWA | Actividad | F1 | F2 | F3 | F4 | F5 | F6 | F7 |
|---|---|---|---|---|---|---|---|---|
| 4.A.1.a.1 | Getting Information | 0,7 | 0,3 | | | | | |
| 4.A.1.a.2 | Monitoring Processes, Materials, or Surroundings | | | | 0,5 | 0,5 | | |
| 4.A.1.b.1 | Identifying Objects, Actions, and Events | | | | 0,7 | 0,3 | | |
| 4.A.1.b.2 | Inspecting Equipment, Structures, or Materials | | | | 0,8 | | | 0,2 |
| 4.A.1.b.3 | Estimating the Quantifiable Characteristics… | | | | 0,3 | 0,7 | | |
| 4.A.2.a.1 | Judging the Qualities of Objects, Services, or People | 0,3 | | | 0,3 | 0,4 | | |
| 4.A.2.a.2 | Processing Information | 0,5 | | | | | 0,5 | |
| 4.A.2.a.3 | Evaluating Information to Determine Compliance | 0,5 | | | | | 0,5 | |
| 4.A.2.a.4 | Analyzing Data or Information | 0,3 | | | | 0,7 | | |
| 4.A.2.b.1 | Making Decisions and Solving Problems | | 0,2 | | | 0,3 | 0,5 | |
| 4.A.2.b.2 | Thinking Creatively | | 1,0 | | | | | |
| 4.A.2.b.3 | Updating and Using Relevant Knowledge | 0,6 | 0,4 | | | | | |
| 4.A.2.b.4 | Developing Objectives and Strategies | | 0,5 | | | 0,25 | 0,25 | |
| 4.A.2.b.5 | Scheduling Work and Activities | | | | | | 1,0 | |
| 4.A.2.b.6 | Organizing, Planning, and Prioritizing Work | | 0,3 | | | | 0,7 | |
| 4.A.3.a.1 | Performing General Physical Activities | | | | | | | 1,0 |
| 4.A.3.a.2 | Handling and Moving Objects | | | | | | | 1,0 |
| 4.A.3.a.3 | Controlling Machines and Processes | | | | | | 0,4 | 0,6 |
| 4.A.3.a.4 | Operating Vehicles, Mechanized Devices, or Equipment | | | | | | | 1,0 |
| 4.A.3.b.1 | Working with Computers | | 0,5 | | | | 0,5 | |
| 4.A.3.b.2 | Drafting, Laying Out, and Specifying Technical Devices… | | 0,5 | | 0,5 | | | |
| 4.A.3.b.4 | Repairing and Maintaining Mechanical Equipment | | | | | 0,3 | | 0,7 |
| 4.A.3.b.5 | Repairing and Maintaining Electronic Equipment | | | | | 0,4 | | 0,6 |
| 4.A.3.b.6 | Documenting/Recording Information | 0,3 | 0,4 | 0,3 | | | | |
| 4.A.4.a.1 | Interpreting the Meaning of Information for Others | 0,3 | 0,7 | | | | | |
| 4.A.4.a.2 | Communicating with Supervisors, Peers, or Subordinates | | 0,7 | 0,3 | | | | |
| 4.A.4.a.3 | Communicating with People Outside the Organization | | 0,6 | 0,4 | | | | |
| 4.A.4.a.4 | Establishing and Maintaining Interpersonal Relationships | | 0,5 | 0,5 | | | | |
| 4.A.4.a.5 | Assisting and Caring for Others | | 0,25 | 0,25 | | | | 0,5 |
| 4.A.4.a.6 | Selling or Influencing Others | | 0,6 | | | 0,4 | | |
| 4.A.4.a.7 | Resolving Conflicts and Negotiating with Others | | 1,0 | | | | | |
| 4.A.4.a.8 | Performing for or Working Directly with the Public | | 0,5 | 0,5 | | | | |
| 4.A.4.b.1 | Coordinating the Work and Activities of Others | | 0,3 | | | | 0,7 | |
| 4.A.4.b.2 | Developing and Building Teams | | 0,5 | | | 0,5 | | |
| 4.A.4.b.3 | Training and Teaching Others | | 0,7 | 0,3 | | | | |
| 4.A.4.b.4 | Guiding, Directing, and Motivating Subordinates | | 0,5 | | | | 0,5 | |
| 4.A.4.b.5 | Coaching and Developing Others | | 0,7 | | | 0,3 | | |
| 4.A.4.b.6 | Providing Consultation and Advice to Others | 0,3 | 0,7 | | | | | |
| 4.A.4.c.1 | Performing Administrative Activities | 0,3 | | | | | 0,7 | |
| 4.A.4.c.2 | Staffing Organizational Units | | | | | 0,5 | 0,5 | |
| 4.A.4.c.3 | Monitoring and Controlling Resources | | | | | 0,5 | 0,5 | |

**Advertencias:**
- Son juicios del diseño, no datos. Por eso la capa F nunca se publica solo con esta fuente: se contrasta con la fuente semántica (patentes) y con el uso observado (§6).
- La GWA es un nivel grueso. La v0.2 podrá bajar a DWA si la validación lo pide.

## 4. Tipo de tarea (A–E)

Son las mismas categorías usadas en el análisis del paper del 26-10-2026, fijadas antes de calcular:

| Tipo (columna `T_A`–`T_E` en el código) | GWA |
|---|---|
| A. Dirigir y supervisar personas | 4.A.4.b.1, 4.A.4.b.2, 4.A.4.b.4, 4.A.4.b.5, 4.A.4.c.2, 4.A.4.c.3 |
| B. Decidir, planificar y crear | 4.A.2.b.1, 4.A.2.b.2, 4.A.2.b.4, 4.A.2.b.5, 4.A.2.b.6 |
| C. Asesorar, formar y relacionarse | 4.A.4.a.\*, 4.A.4.b.3, 4.A.4.b.6 |
| D. Analizar y procesar información | 4.A.1.a.1, 4.A.1.b.3, 4.A.2.a.\*, 4.A.2.b.3, 4.A.3.b.1, 4.A.3.b.6, 4.A.4.c.1 |
| E. Trabajo físico y técnico | 4.A.1.a.2, 4.A.1.b.1, 4.A.1.b.2, 4.A.3.a.\*, 4.A.3.b.2, 4.A.3.b.4, 4.A.3.b.5 |

## 5. Modo de operación (eje 2)

Solo con uso observado (Anthropic Economic Index) y para F1–F2:
- **asistido:** claude.ai;
- **integrado:** API (sin Claude Code);
- **parte automatizada:** modos de colaboración directivo y de bucle de retroalimentación, frente a iteración, aprendizaje y validación.
- **Unidad:** el enunciado de la tarea, uno por observación. Las celdas no publicadas (menos de 15 conversaciones) cuentan como «sin uso observado», no como cero.

## 6. Validación prevista

1. **Fuente semántica independiente:** similitud de cada tarea con las patentes de IA de cada componente del USPTO AIPD. Es otra fuente, no otra versión de la regla.
2. **Validación humana:** unas 300 tareas estratificadas por GWA, codificadas por dos personas con la pregunta «¿qué familia de IA ejecutaría la parte automatizable?», y el α de Krippendorff por familia.
3. **Sensibilidad:** perturbación aleatoria de los pesos de la §3 (±0,2, renormalizados; 1.000 réplicas), con la banda de la superficie por familia.
