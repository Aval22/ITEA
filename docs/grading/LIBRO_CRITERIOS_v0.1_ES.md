# Libro de criterios para graduar tareas en ITEA: codificabilidad (K) y exposición a la IA generativa (E)

**Versión 0.1 (borrador para revisión del autor), 23-10-2026.** Sustituye la asignación de grados AXI, que son grados heredados aplicados por patrón tecnológico, por un procedimiento explícito, reproducible y validado.

> **Cambio de enfoque v0.2 (23-10-2026, decisión del autor): graduación totalmente automática con criterios normalizados.**
>
> **Ya no hay juicio humano tarea a tarea en la construcción.** La codificabilidad de cada GWA ya no la asigna nadie: se calcula con las **tablas oficiales de enlace de O\*NET 30.2**.
> - `Abilities to Work Activities`: proporción de capacidades **cognitivas** (1.A.1) frente a psicomotoras, físicas y sensoriales.
> - `Skills to Work Activities`: proporción de habilidades **sociales** (2.B.1), que indican conocimiento relacional y tácito.
> - **Fórmula:** `K_GWA = proporción cognitiva × (1 − proporción social)`.
>
> **Ordenación resultante.**
> - **Arriba**, el análisis simbólico: *Analyzing Data*, *Processing Information*, *Evaluating Compliance*, *Administrative Activities* o *Working with Computers*, con valores de 0,80 a 1,00.
> - **En medio**, lo relacional: *Assisting and Caring* (0,36), *Selling* (0,35) o *Establishing Relationships* (0,20).
> - **Abajo**, lo corporal: *Handling and Moving Objects*, *Performing Physical Activities* o *Controlling Machines*, todos con 0,00.
>
> La tabla de §3 queda como lectura cualitativa; el valor operativo es `K_GWA`.
>
> **Cómo se valida, sin una referencia propia:**
> - **E**, con las etiquetas humanas independientes de Eloundou et al. (2024) y con el uso real del Anthropic Economic Index.
> - **K**, con medidas publicadas de contenido de tareas e idoneidad para la automatización. Se buscarán las medidas de Acemoglu y Autor (2011) y de Brynjolfsson, Mitchell y Rock (2018), si los datos son accesibles.
> - **Robustez:** con fórmulas alternativas, por ejemplo solo la proporción cognitiva, o con pesos distintos para lo social.
>
> **La codificación humana de §6 pasa a ser una auditoría opcional**, no la base del sistema.
>
> **Cautela:** como `K_GWA` usa capacidades cognitivas, el índice del JRC (también basado en capacidades) deja de ser un contraste independiente para K. Se mantiene solo para OAXI-EU y se declara así.

## 1. Principios

1. **Los criterios salen de las taxonomías oficiales.** Cada grado se justifica con categorías públicas de O\*NET y ESCO, no con reglas propias sin documentar.
2. **La unidad es la tarea oficial.** Se gradúan las **18.796 tareas de O\*NET 30.2** por su Task ID. Cada una está enlazada con al menos una actividad detallada (DWA) y, a través de ella, con una actividad intermedia (IWA) y una general (GWA). Se abandonan los 47.810 subenunciados de AXI, que partían las tareas (01a, 01b…) y solo encajaban en un 50 % con la versión vigente.
3. **No se entrena con los grados AXI antiguos.** Hacerlo heredaría sus patrones fijos. La referencia es una codificación humana nueva (§6).
4. **Lo que se construye y lo que se valida van por separado.** E no se construye con capacidades cognitivas (es la base del índice del JRC), ni con datos de uso real de la IA (Anthropic Economic Index). Ambos se reservan para validar (§7) y así no hay circularidad.
5. **Cada grado es interpretable.** Cada tarea lleva sus motivos: GWA, grupos de habilidades ESCO y anclas más cercanas.

## 2. Definiciones de los constructos

**Codificabilidad (K).** Medida en que el conocimiento que usa la tarea puede expresarse en reglas, procedimientos o representaciones explícitas, o aprenderse a partir de registros documentados, de modo que pueda incorporarse a un sistema que la organización posee.
- Se apoya en la economía de la codificación y la tacitez (Cowan, David y Foray, 2000) y en la paradoja de Polanyi (Autor, 2015).
- Se apoya también en la definición de tarea rutinaria como la que sigue reglas explícitas programables (Autor, Levy y Murnane, 2003; Acemoglu y Autor, 2011).

**Exposición a la IA generativa (E).** Medida en que un sistema de IA generativa puede producir, o reducir sustancialmente, el resultado principal de la tarea. Se adapta la rúbrica de exposición directa de Eloundou et al. (2024) y la idea de idoneidad para el aprendizaje automático de Brynjolfsson, Mitchell y Rock (2018).

Ambas son **potenciales**: no miden adopción ni transferencia de valor.

## 3. Primera capa: la jerarquía de actividades de O\*NET (criterio estructural)

Cada GWA recibe una **clase previa de codificabilidad**. La clasificación sigue la tradición de medidas de contenido de tareas construidas con descriptores de O\*NET (Acemoglu y Autor, 2011), que separa lo cognitivo-analítico y rutinario de lo interpersonal y lo manual no rutinario. **La asignación de cada GWA es una propuesta que tienes que revisar.**

| Clase previa | GWA de O\*NET 30.2 (tareas enlazadas) |
|---|---|
| **K-alta: información simbólica estructurada** | Getting Information (1.076) · Processing Information (331) · Analyzing Data or Information (704) · Evaluating Information to Determine Compliance with Standards (167) · Estimating the Quantifiable Characteristics… (365) · Documenting/Recording Information (1.658) · Working with Computers (280) · Scheduling Work and Activities (128) · Performing Administrative Activities (356) |
| **K-media: juicio, creación y asesoramiento documentables en parte** | Making Decisions and Solving Problems (683) · Thinking Creatively (1.418) · Updating and Using Relevant Knowledge (371) · Developing Objectives and Strategies (268) · Organizing, Planning, and Prioritizing Work (145) · Judging the Qualities of Objects, Services, or People (551) · Interpreting the Meaning of Information for Others (282) · Providing Consultation and Advice to Others (785) · Monitoring and Controlling Resources (547) · Communicating with Supervisors, Peers, or Subordinates (1.032) · Communicating with People Outside the Organization (302) · Training and Teaching Others (661) · Staffing Organizational Units (113) · Selling or Influencing Others (215) |
| **K-baja: conocimiento corporal, sensorial o relacional en situación** | Performing General Physical Activities (1.243) · Handling and Moving Objects (2.553) · Controlling Machines and Processes (712) · Operating Vehicles, Mechanized Devices, or Equipment (136) · Repairing and Maintaining Mechanical Equipment (654) · Inspecting Equipment, Structures, or Materials (976) · Identifying Objects, Actions, and Events (112) · Monitoring Processes, Materials, or Surroundings (796) · Assisting and Caring for Others (715) · Establishing and Maintaining Interpersonal Relationships (45) · Resolving Conflicts and Negotiating with Others (126) · Performing for or Working Directly with the Public (159) · Guiding, Directing, and Motivating Subordinates (1.368) · Coaching and Developing Others (61) |

**Casos dudosos (a decidir):**
- **Monitoring Processes e Inspecting Equipment:** hoy los automatiza la visión artificial, que no es IA generativa. ¿Codificabilidad media?
- **Guiding/Motivating Subordinates:** ¿bajo o medio?
- **Working with Computers:** ¿alto en K pero distinto en E?

**Regla:** una tarea con varias GWA (el 16,3 % de las tareas) toma la media de las puntuaciones de sus clases (alta = 1, media = 0,5, baja = 0).

## 4. Segunda capa: las habilidades de ESCO (criterio de competencias)

Cada tarea se enlaza por **similitud semántica** con sus 5 habilidades ESCO más próximas. Se calculan *embeddings* de frases con un modelo abierto de tipo Sentence-BERT (Reimers y Gurevych, 2019) y se toma la similitud del coseno. Es la misma familia de métodos con que la literatura enlaza textos con tareas de O\*NET (Webb, 2019; Atalay et al., 2020; Kogan et al., 2023; Montobbio et al., 2024). De esas habilidades se extraen estos rasgos:

| Rasgo de ESCO v1.2.1 | Dirección esperada |
|---|---|
| Proporción de habilidades de tipo **conocimiento** (3.221) frente a destreza o competencia (10.734) | Más conocimiento explícito → más K |
| **Grupo de habilidades:** *information skills*, *working with computers* | → más K y más E |
| **Grupo de habilidades:** *handling and moving*, *constructing*, *working with machinery*, *assisting and caring* | → menos K y menos E |
| **Familia transversal:** *thinking skills* | → más K |
| **Familias transversales:** *physical and manual*, *social and communication*, *life skills* | → menos K |
| Pertenencia a **DigComp** (25 competencias digitales) | → más E |
| **Nivel de reutilización** (transversal, intersectorial, sectorial, ocupacional) | **Hipótesis por contrastar**, no regla: en la v4.0 correlacionó en negativo con la exposición del JRC |

## 5. Tercera capa: anclas textuales

Para cada nivel de K y de E se redactan **3–5 frases ancla** con el vocabulario de las definiciones oficiales de las GWA y de los grupos de ESCO, y se mide la similitud de cada tarea con ellas. Ejemplos de borrador:
- **E-alta:** «Draft, summarise, translate or edit written documents»; «Write or debug software code»; «Search, retrieve and synthesise information from documents»; «Analyse data and report findings».
- **E-baja:** «Lift, carry or move objects»; «Provide physical care to patients»; «Operate vehicles or heavy equipment».
- **K-alta:** «Apply established rules or standards to classify or record information».
- **K-baja:** «Adapt actions to people or physical conditions in real time».

## 6. Referencia humana (un solo codificador: decisión del 23-10-2026)

La codificación humana la hace **solo el autor**. Sin un segundo codificador no se puede calcular la fiabilidad entre codificadores, así que el diseño la compensa con tres piezas y lo declara como limitación.

1. **Codificación principal.** Unas **400 tareas**, estratificadas por clase previa de GWA y por gran grupo ocupacional (semilla fija), en orden aleatorio. Se codifican K (alta, media, baja) y E (alta, media, baja), cada una con su motivo. **Se codifica a ciegas:** sin ver ninguna puntuación de los modelos, ni la clase de la GWA, ni los grados AXI antiguos.
2. **Fiabilidad del propio codificador.** Pasadas **al menos 3 semanas**, se recodifican a ciegas 100 tareas de la muestra, en otro orden. Se informa de la κ ponderada intracodificador. Mide la estabilidad del criterio, no el acuerdo entre personas.
3. **Referencia humana externa para E.** Las etiquetas humanas de exposición de Eloundou et al. (2024) sobre tareas de O\*NET (E0, E1, E2), publicadas con licencia MIT en `github.com/openai/GPTs-are-GPTs` (fichero `data/full_labelset.tsv`, columna `human_exposure_agg`), se cruzan por Task ID oficial. Permiten dos cosas:
   - medir el **acuerdo entre dos referencias humanas independientes** (el autor y los anotadores de Eloundou) en las tareas comunes;
   - validar los métodos de §7 sobre miles de tareas.

   Hay que adaptar la escala: E0 → baja, E1 → alta (exposición directa) y E2 → media (exposición con herramientas). La correspondencia se documenta y se prueba con alternativas.
4. **Para K no existe una referencia humana externa equivalente.** Hay que buscarla en otros trabajos; un candidato son las valoraciones por actividad de Brynjolfsson, Mitchell y Rock (2018), si se pueden obtener. Se recomienda además, **antes de enviar a una revista**, que una segunda persona (un colega o un anotador contratado, 3–4 horas) codifique a ciegas 100 tareas, para tener al menos una κ entre codificadores para K.

**Partición:** el 70 % de la muestra del autor sirve para calibrar y el 30 % se reserva para evaluar. Las etiquetas de Eloundou nunca se usan para calibrar E, solo para validar.

**Limitación declarada:** la referencia de K se apoya en un único codificador. Su fiabilidad se presenta como estabilidad intracodificador, más el acuerdo con la estructura oficial de O\*NET y, si llega, con un segundo codificador parcial.

## 7. Métodos en competencia y validación

| Método | Descripción | Transparencia |
|---|---|---|
| **A. Estructural** | Solo GWA (§3) | Total |
| **B. Estructural + ESCO + anclas** | Modelo ordinal logístico con los rasgos de §3–5, ajustado a la referencia humana | Alta (coeficientes interpretables) |
| **C. LLM documentado** (opcional) | Modelo, versión, fecha, *prompt* literal y temperatura registrados; se guarda cada respuesta con su motivo (como en Eloundou et al., 2024; Gmyrek et al., 2023) | Media |

**Elección del método:** gana el que tenga mejor κ con la referencia humana en la parte reservada. Se informa de los tres.

**Validación externa** (no se usa para construir):
- **E:** uso real de la IA por tarea según el Anthropic Economic Index (Handa et al., 2025); también la exposición de Eloundou et al. (2024), si su licencia permite usarla.
- **OAXI-EU:** convergencia con JRC145832 (Casas et al., 2026), que mantiene independencia porque se basa en capacidades.
- **Comparación con la literatura** de habilidades replicables por la automatización (Lassébie y Quintini, 2022).

## 8. Reproducibilidad y documentación

- **Módulo `itea.grading`:** *embeddings* con modelo y versión fijados, semillas, rasgos, ajuste y predicción. Tests y ficha de datos (versión de O\*NET y de ESCO, modelo de *embeddings*, métricas con la referencia humana).
- **Público en el repositorio:** el libro de criterios, las anclas, la muestra humana (con permiso de quienes codifiquen) y las predicciones para las 18.796 tareas.
- **Todo pasa por issues y *pull requests* públicos,** con su fecha real.

## 9. Literatura de apoyo (referencias verificadas en Crossref o arXiv)

| Pieza del diseño | Referencias |
|---|---|
| Definición de codificabilidad, tacitez y rutina | Cowan, David y Foray (2000), *ICC* 9(2), 10.1093/icc/9.2.211 · Autor, Levy y Murnane (2003), *QJE* 118(4), 10.1162/003355303322552801 · Autor (2015), *JEP* 29(3), 10.1257/jep.29.3.3 |
| Medidas de contenido de tareas con descriptores de O\*NET | Acemoglu y Autor (2011), *Handbook of Labor Economics* 4B, 10.1016/S0169-7218(11)02410-5 |
| Rúbricas a nivel de actividad o tarea con validación humana | Brynjolfsson, Mitchell y Rock (2018), *AEA P&P* 108, 10.1257/pandp.20181019 · Eloundou et al. (2024), *Science* 384, 10.1126/science.adj0998 · Gmyrek, Berg y Bescond (2023), OIT, 10.54394/fhem8239 |
| Emparejamiento semántico de textos con tareas de O\*NET | Webb (2019), 10.2139/ssrn.3482150 · Atalay et al. (2020), *AEJ: Applied* 12(2), 10.1257/app.20190070 · Kogan et al. (2023), NBER WP 31846, 10.3386/w31846 · Montobbio et al. (2024), *The World Economy* 47(1) (DOI por verificar; el trabajo de 2022 en *TFSC* usa modelos de temas, no emparejamiento con tareas) · Reimers y Gurevych (2019), EMNLP, 10.18653/v1/d19-1410 |
| Capacidades y habilidades replicables por la IA (contraste) | Tolan et al. (2021), *JAIR* 71, 10.1613/jair.1.12647 · Lassébie y Quintini (2022), OCDE, 10.1787/646aad77-en |
| Validación con uso real | Handa et al. (2025), arXiv:2503.04761 |
| Correspondencias O\*NET–ISCO | Hardy, Keister y Lewandowski (2018), *Economics of Transition* 26(2), 10.1111/ecot.12145 |

## 10. Decisiones pendientes del autor

1. Revisar la clase de cada GWA (§3), sobre todo los casos dudosos.
2. ~~Elegir codificadores~~: **decidido, solo el autor** (§6). Queda por fijar el calendario: unas 12–15 horas para 400 tareas, y la recodificación de 100 tareas al menos 3 semanas después. Queda también abierto si se busca un segundo codificador parcial para K antes de enviar a una revista.
3. Decidir si se incluye el método C (LLM) y con qué modelo, que quedará documentado.
4. Elegir el modelo de *embeddings*: propongo `all-mpnet-base-v2` (Sentence-Transformers, Apache-2.0), que funciona sin GPU. Su instalación la haces tú.
