# Diseño de la capa F (familias de IA) para ITEA 4.2

**Versión 0.1, 26-10-2026. Propuesta de diseño; no implementada.** Complementa:
- las capas T (mediación tecnológica) y U (utilización), en `DISENO_capa_tecnologica_y_certificacion_v0.1_ES.md`;
- las capas K y E de la v4.1.

Responde a una pregunta que ITEA no se plantea hasta ahora: **dentro de las tareas alienables, ¿con qué tipo de IA se hacen y qué porcentaje representa cada tipo?**

## 1. Qué se quiere medir

| Capa | Pregunta |
|---|---|
| K, E (v4.1) | ¿Es codificable la tarea? ¿Está expuesta a la IA? |
| T | ¿Qué productos concretos la apoyan o automatizan en esta ocupación? |
| **F (nueva)** | **¿Qué familia de IA puede ejecutarla, y en qué modo opera: asistida, integrada o agéntica?** |
| U | ¿Cuánto se usa de verdad, por país y sector? |

**Por qué importa:**
- La alienación no la produce «la IA» en abstracto. Cada familia trabaja sobre un tipo distinto de conocimiento:
  - la analítica y predictiva aprende de **registros** (el *qué*);
  - la de lenguaje, de **textos y conversaciones** (parte del *cómo*);
  - la agéntica con memoria acumula **procedimientos** (el *cómo* y parte del *porqué*).
- F conecta ITEA con los cuatro regímenes técnicos del paper del binomio (registros → analítica → IA generativa → IA agéntica) y permite medirlos tarea a tarea.

## 2. Taxonomía operativa

La clasificación de partida (12 familias técnicas, más disciplinas, arquitecturas y métodos de aprendizaje) es útil como marco conceptual. Pero no es una lista oficial, y sus familias se solapan: un LLM es a la vez de lenguaje, generativo y de programación.

Para medir se necesitan categorías **con datos detrás**. Se proponen dos ejes ortogonales.

### Eje 1. Familia funcional (7 categorías)

Anclada en la clasificación oficial de la encuesta TIC de Eurostat (`isoc_eb_ai`), que da la adopción por país y sector:

| Familia F | Código Eurostat | Equivalencia con las 12 familias | Componente de patentes (USPTO AIPD) |
|---|---|---|---|
| F1. Análisis de texto | E_AI_TTM | 1, 2 (PLN, grafos de conocimiento, RAG) | Natural language processing; knowledge processing |
| F2. Generación de lenguaje y código | E_AI_TNLG | 1, 3, 12 (LLM, IA de programación, IA generativa) | Natural language processing |
| F3. Voz | E_AI_TSR | 7 | Speech |
| F4. Visión | E_AI_TIR | 6 | Vision |
| F5. Aprendizaje automático analítico y predictivo | E_AI_TML | 4, 5 | Machine learning |
| F6. Automatización de flujos y apoyo a la decisión | E_AI_TPA | 10, 11 (sistemas expertos, RPA, optimización) | Planning/control; knowledge processing; evolutionary computation |
| F7. Robótica y movimiento autónomo | E_AI_TAR | 9 (parte física), 11 | Planning/control; AI hardware |

La familia 8 (multimodal) se reparte entre F1–F4, porque sus componentes ya están en ellas.

### Eje 2. Modo de operación (3 categorías)

| Modo | Qué es | Cómo se observa |
|---|---|---|
| M1. Asistido | Conversación con una persona que decide, sesión a sesión | AEI, claude.ai; modos de aumento (iteración, aprendizaje, validación) |
| M2. Integrado o automatizado | La IA se invoca desde sistemas de la empresa | AEI, uso por API; modos directivo y de bucle |
| M3. Agéntico con memoria | Encadena tareas, usa herramientas y acumula memoria y procedimientos | Autonomía de la IA (AEI), tareas de varios pasos, memoria persistente y *skills* (revisión técnica del 25-10-2026) |

La familia 9 de la clasificación de partida (agéntica y multiagente) no es una familia: es un **modo** que puede usar cualquier familia.

## 2 bis. Las familias no expropian igual: cuatro atributos (aportación del autor, 26-10-2026)

Alberto: «No es lo mismo el grado de expropiación del conocimiento ni la forma que tiene de hacerlo una IA LLM que una de análisis semántico, ni su grado de ser reproducible ni su valor de mercado por ser más escaso».

Por tanto, F no basta con decir *qué familia* actúa. Hay que decir **qué hace cada familia con el conocimiento**. Se proponen cuatro atributos por familia y modo, que se miden por separado:

| Atributo | Pregunta | Escala propuesta | Cómo se mide |
|---|---|---|---|
| **G. Grado de captura** | ¿Qué parte del conocimiento captura? | 1 = el *qué* (resultados, entidades) · 2 = patrones del *qué* · 3 = el *cómo* (procedimiento, estilo) · 4 = el *cómo* y parte del *porqué* (criterio, excepciones) | Rúbrica por familia y modo, juzgada por un panel de expertos (Delphi, dos rondas) con α de Krippendorff |
| **Fo. Forma de captura** | ¿Dónde queda lo capturado? | registro · modelo estadístico · grafo o índice semántico · pesos · memoria declarativa | Literatura técnica (revisión del 25-10-2026); no requiere juicio |
| **R. Reproducibilidad** | ¿Puede reutilizarse sin su autor, copiarse, portarse y atribuirse? | Cuatro propiedades: reutilizable sin el autor, copiable a coste casi nulo, portable entre sistemas, atribuible a una persona; 0–1 cada una | Propiedades técnicas del formato (tabla 8.3 de `REVISION_memoria_agentes.md`) |
| **V. Escasez y valor de mercado** | ¿Es escaso el activo que resulta? | Bajo (capacidad genérica y abundante) → alto (activo específico de la empresa y difícil de replicar) | Indicadores de oferta y de especificidad (abajo) |

**Ejemplo que motiva la distinción.**
- **Un LLM** que aprende el procedimiento de un profesional captura en profundidad (G = 3–4) y el resultado es muy reproducible. Pero la capacidad de partida es genérica y cada vez más barata.
- **Un análisis semántico** (minería de textos, grafo de conocimiento) sobre los registros de la empresa captura menos (G = 1–2: entidades y relaciones del *qué*). Pero el activo resultante, un mapa del conocimiento propio de esa empresa, es específico y escaso.

**El grado de expropiación y el valor de mercado no tienen por qué ir juntos.** Esta es la razón para medirlos por separado.

**Indicadores posibles de escasez (V), por verificar su disponibilidad:**
- **Concentración de la oferta por familia:** número de titulares y concentración (HHI) de las patentes de cada componente en el USPTO AIPD.
- **Especificidad:** la parte de las empresas que desarrolla o adapta su IA con personal propio frente a la que usa producto comercial listo (Eurostat `isoc_eb_ai`: E_AI_ADOWN, E_AI_AMOWN, E_AI_ARDY). Hay que comprobar si Eurostat la cruza por familia.
- **Precio de la capacidad genérica:** evolución del precio por unidad de uso de los modelos de lenguaje (abaratamiento = abundancia).
- **Demanda de pericia:** marcas *Hot Technology* e *In Demand* de O\*NET Technology Skills por familia de producto.

**Cómo se combinan.** Al principio, **no** se combinan: se publican como cuatro dimensiones. Un índice compuesto (por ejemplo, intensidad de expropiación = G × R, y valor en juego = G × R × V) solo se construiría después de validar cada atributo por separado. Multiplicar juicios sin validar daría una precisión falsa.

**Qué añade al paper del binomio.** Los derechos sobre la capa de adaptación importan más donde la captura es **profunda (G alto)**, el resultado es **reproducible (R alto)** y el activo es **escaso (V alto)**. Es el caso de un LLM o un agente adaptado con el conocimiento de un profesional sobre procesos propios de la empresa. Donde la captura es superficial y el activo abundante, la asignación de derechos importa poco.

**Hipótesis adicionales (para registrar con H21–H25):**
- **H26.** G y V están poco correlacionados entre familias (|ρ| < 0,5): profundidad de captura y escasez son dimensiones distintas.
- **H27.** En las tareas en juego, la parte de la superficie con G ≥ 3 (captura del *cómo*) es mayor en los modos integrado y agéntico que en el asistido.

## 3. Asignación tarea → familia

Cada tarea de O\*NET 30.2 recibe un **vector de pertinencia** sobre F1–F7, de suma 1, como la capa 2 de la v4.1. Se combinan tres fuentes independientes, igual que K y E:

1. **Estructural** (reglas fijadas antes de calcular). A partir del enlace oficial tarea → DWA → actividad de trabajo:
   - analizar datos → F5;
   - documentar o registrar → F1 y F2;
   - inspeccionar o identificar objetos → F4;
   - comunicar → F2 y F3;
   - programar el trabajo → F6;
   - manejar vehículos o maquinaria → F7.

   La tabla completa irá en el libro de criterios.
2. **Semántica.** Similitud entre el enunciado de la tarea y los resúmenes de las patentes de IA de cada componente del *USPTO AI Patent Dataset*. La clasificación es de Giczy, Pairolero y Toole (2022, *Journal of Technology Transfer*). El método es el de Webb (2020) y Kogan et al. (2021). Se reutiliza la infraestructura de *embeddings* locales de la capa 2. Las patentes miden **invención**, no despliegue: por eso esta fuente se combina con las otras dos.
3. **Observada:**
   - el AEI, por tarea, solo para F1–F2 y para el modo;
   - el inventario de software de O\*NET (Technology Skills), por ocupación: OCR, reconocimiento de voz, sistemas expertos, inteligencia de negocio, aprendizaje automático;
   - la fase 2 de la capa T: las funciones de IA de cada producto, clasificadas por familia.

### 3 bis. Uso observado: tres proveedores, más un control independiente (decisión del 26-10-2026)

Para no depender de un solo proveedor, el uso observado se triangula con tres grandes laboratorios y una fuente que no es de ningún proveedor:

| Proveedor | Fuente | Granularidad | Canal y modo | Periodo | Acceso | Límites |
|---|---|---|---|---|---|---|
| **Anthropic** | Anthropic Economic Index | **Enunciado de tarea O\*NET**, con modos de colaboración y autonomía | claude.ai (asistido) y API (integrado); Claude Code (agéntico) | agosto de 2025 → abril–mayo de 2026, cada 3–6 meses | Público, ya descargado | Un proveedor; las tareas con menos de 15 conversaciones no se publican |
| **OpenAI** | Chatterji et al. (2025), *How People Use ChatGPT*, NBER w34255 | **Actividad de trabajo generalizada (GWA)** y tipo de mensaje (*Asking/Doing/Expressing*) | ChatGPT de consumo (asistido) | mayo de 2024 → julio de 2025 | Tablas agregadas del documento; sin datos por tarea [COMPROBAR si hay anexo descargable] | Autores empleados de OpenAI; clasificadores automáticos; mucho uso no laboral |
| **Microsoft** | Tomlinson et al. (2025), *Working with AI*, arXiv:2507.07935 | **Actividad de trabajo intermedia (IWA)**, separando el objetivo del usuario de lo que hace la IA | Bing Copilot (asistido); el Work Trend Index añade el uso en la empresa (M365) | enero → septiembre de 2024 | [COMPROBAR la publicación de los datos por IWA] | Un producto de consumo; datos de 2024; clasificados por LLM |
| *Control independiente* | Encuestas a trabajadores (por ejemplo, Bick, Blandin y Deming; Humlum y Vestergaard) [COMPROBAR referencias] | Ocupación | Uso declarado, de todos los proveedores | 2024–2025 | Publicado | Uso declarado, no observado; sin detalle por tarea |

**Por qué Microsoft como tercero y no Google:**
- Es el único otro laboratorio con un índice público de uso **por actividad de trabajo de O\*NET**. Además, separa lo que pide el usuario de lo que hace la IA, que es la división del trabajo del binomio.
- Cubre el canal **empresarial** (Copilot integrado en M365), que es el más cercano al modo integrado.
- **Google** no tiene ningún informe equivalente verificable (revisión del 25-10-2026, §3.4). Se usa para la memoria y la portabilidad (Gemini), no para el uso por tarea.

**Cómo se combinan:**
- **Nivel común: la actividad de trabajo generalizada (GWA).** Es el nivel al que llegan las tres fuentes, y sobre ella se definen los tipos de tarea A–E. Anthropic y Microsoft se agregan a GWA con el enlace oficial tarea → DWA → IWA → GWA.
- **Contraste:** concordancia de rangos entre proveedores por GWA. Si los tres coinciden, el resultado no es un artefacto de un producto.
- **Solo Anthropic llega a la tarea y al modo** (API y autonomía). Para el modo, la triangulación se apoya en el Work Trend Index (empresa) y en las encuestas de uso.
- **Las tres fuentes cubren solo modelos de lenguaje (F1–F2).** Las familias F3–F7 siguen apoyándose en reglas, patentes y Eurostat.

**Combinación:** rangos percentiles con pesos iguales y un Monte Carlo sobre las decisiones de método, como la OAXI-EU v4.1.

**Resultados por tarea, ocupación, ISCO-08 y sector:** el porcentaje de la superficie alienable (tareas en juego) que corresponde a cada familia y a cada modo.

## 4. Ponderación por adopción (enlace con la capa U)

Eurostat publica la adopción de cada familia por país y sector. Primera lectura, 2025, empresas de 10 o más empleados, sin el sector financiero:

| Familia | España | UE-27 |
|---|---|---|
| F1. Análisis de texto | 10,1 % | 11,8 % |
| F2. Generación de lenguaje o código | 8,9 % | 8,8 % |
| F3. Voz | 7,2 % | 7,2 % |
| F6. Automatización de flujos y decisión | 6,7 % | 5,4 % |
| F5. Aprendizaje automático | 5,6 % | 5,1 % |
| F4. Visión | 5,6 % | 3,8 % |
| F7. Robótica autónoma | 1,6 % | 1,4 % |
| Alguna tecnología de IA | 20,3 % | 20,0 % |

**Utilización esperada por familia** = superficie alienable de la familia × adopción de la familia en el país y el sector. Así U deja de ser un único número de «IA» y pasa a tener composición.

## 5. Prueba de viabilidad (prototipo, 26-10-2026)

Script: `Paper_Binomio_IA_Trabajador/estimacion/prototipo_familias_IA.py`.
- **Datos:** AEI, una semana (5–12 de febrero de 2026), Claude, solo modelos de lenguaje (F1–F2).
- **Unidad:** el enunciado de la tarea, uno por observación.
- **En juego:** umbral central de la v4.1.

| | claude.ai (asistido) | API (integrado) |
|---|---|---|
| Enunciados en juego con uso observado | 22 % (fuera de juego: 13 %) | 18 % (fuera de juego: 8 %) |
| Parte de las conversaciones que cae en tareas en juego | 44 % | **64 %** |
| Parte automatizada del uso (modos directivo y de bucle) | 48 % | **92 %** |

**Lectura prudente:**
- El uso por API, el modo integrado, se concentra en las tareas alienables y es casi todo automatizado.
- Dentro de las tareas en juego, el uso es menor en las de dirigir y supervisar personas (6–7 % con uso) que en las de analizar o decidir (18–27 %).

**Lo que no demuestra:**
- Es un solo proveedor y una sola semana.
- Las tareas con menos de 15 conversaciones no se publican.
- La autonomía media del AEI (2,7 por API frente a 3,4 en claude.ai) necesita leerse con su documentación antes de interpretarla.
- **Estas regularidades ya se han visto.** No pueden registrarse como hipótesis confirmatorias con estos mismos datos. Se contrastan con la publicación de junio de 2026 (abril–mayo) u otra posterior.

## 6. Hipótesis para registrar (H21–H25, antes de ejecutar)

| H | Enunciado | Contraste |
|---|---|---|
| H21 | La pertinencia de F4 (visión) se concentra en tareas de inspección e identificación (actividades 4.A.1.b.*) | Media de F4 en esas tareas frente al resto; d > 0,5 |
| H22 | En las tareas en juego, F1 + F2 (lenguaje) son la familia principal en más de la mitad de la superficie | Parte ponderada por importancia y empleo |
| H23 | La parte del uso por API que cae en tareas en juego es mayor que la de claude.ai | Publicación de junio de 2026 (confirmatoria; la de febrero ya se ha visto) |
| H24 | A nivel sectorial, la superficie alienable de cada familia se asocia positivamente con su adopción en Eurostat | Spearman > 0,3 entre sectores NACE, por familia |
| H25 | El vector de familias es estable entre fuentes: estructural frente a semántica | Spearman por familia > 0,4 entre tareas |

**Validación humana:** muestra estratificada de unas 300 tareas, codificada por dos personas, con el α de Krippendorff por familia. Mismo protocolo que el panel de julio de 2026.

## 7. Qué aporta (y a qué)

- **A ITEA:**
  - la composición tecnológica de la alienabilidad: qué familia actúa sobre qué parte del trabajo;
  - una capa U con composición por familia;
  - la dinámica observada, con cada publicación nueva del AEI (cada 3–6 meses), sin pasar a la prospectiva.
- **Al paper del binomio (H2):** la medida de los cuatro regímenes técnicos.
  - F5 y F6 operan sobre registros (regímenes 1–2).
  - F1 y F2 en modo asistido corresponden a la IA generativa (régimen 3).
  - Cualquier familia en modo agéntico corresponde al régimen 4.
  - La capa de adaptación portable del binomio tiene sentido sobre todo donde dominan F1–F2 en modo integrado o agéntico.
- **A la investigación en general:** según la búsqueda en JTT del 26-10-2026, ningún índice de exposición publicado distingue a la vez la familia de IA y el modo de operación, tarea a tarea. Hay que confirmarlo con una revisión más amplia antes de afirmarlo.

## 8. Límites

- **El uso observado por tarea solo existe para los modelos de lenguaje** (AEI) y para un proveedor. F3–F7 se apoyan en reglas, patentes y adopción empresarial, sin uso por tarea.
- **Las patentes miden invención, no despliegue.** Eurostat mide adopción por empresa, no por tarea.
- **Las familias se solapan** (multimodalidad). Por eso se usa un vector y no una etiqueta única.
- **Sin el sector financiero** en las tablas de Eurostat.

## 9. Pasos (propuesta)

1. Libro de criterios de F (reglas estructurales) y registro de H21–H25 en OSF.
2. Descarga del USPTO AIPD (componentes y resúmenes) y de `isoc_eb_ai` y `isoc_eb_ain2` por sector.
3. Las tres fuentes y su combinación, con tests.
4. Validación humana.
5. Contraste confirmatorio de H23 con la publicación de junio de 2026 del AEI.
6. Integrar F en el libro de datos y en la OAXI-EU (vista por familia).

**Pendiente de verificar:**
- la ficha de Giczy, Pairolero y Toole (2022) en JTT (Crossref la registra en 2021, DOI 10.1007/s10961-021-09900-2) y la licencia de descarga del AIPD;
- las referencias de Webb (2020) y Kogan et al. (2021).
