# Diseño de las capas T (tecnología) y S (solvencia técnica certificable) de ITEA

**Versión 0.1, 23-10-2026.** Complementa `LIBRO_CRITERIOS_v0.1_ES.md` (capas K y E) y el informe *Método automático de graduación de tareas*. Rehace de forma reproducible el análisis original de AXI: tarea por tarea, dentro de cada ocupación, con la documentación pública de los fabricantes.

## 1. Qué se quiere medir: dos preguntas distintas

| Capa | Pregunta | Por qué importa |
|---|---|---|
| **T: mediación tecnológica** | ¿Hay tecnología, documentada por su fabricante, capaz de **apoyar** o **automatizar** esta tarea en esta ocupación? ¿Y desde cuándo incorpora IA? | La expropiación ocurre a través de sistemas concretos que registran el trabajo (CRM, ERP, motores de riesgo o de *pricing*). Una tarea solo es «aprendible desde registros» si esos sistemas existen. |
| **S: solvencia técnica certificable** | ¿Existe una **certificación reconocida** que acredite que el trabajador sabe ejecutar esta tarea con esa tecnología? | Que la tecnología pueda hacerlo no equivale a que la plantilla sepa hacerlo. Hoy la solvencia técnica solo se certifica en ecosistemas concretos (SAP, Oracle, IBM, Microsoft, Cisco y pocos más). |

**El indicador nuevo y diferencial es la brecha:** **T alta con S baja** significa capacidad tecnológica sin solvencia acreditada. Ahí la empresa puede absorber el conocimiento del trabajador sin que exista ningún reconocimiento formal de su pericia. Conecta directamente con la «solvencia técnica» de ITEA (el descriptor de competencia del EQF: responsabilidad y autonomía).

**Separación de constructos:**
- K y E miden propiedades de la tarea;
- T, la tecnología disponible (lo que declara el fabricante);
- **U, cuánto de esa tecnología se usa realmente** (§5 bis);
- S, la acreditación de quien la usa.

El coste y la exigencia organizativa (C) quedan como capa posterior de factibilidad económica, que se cruza con U a través del ROI.

## 2. Inventario tecnológico por ocupación (fuente oficial)

| Fuente (O\*NET 30.2, CC BY 4.0) | Contenido |
|---|---|
| `Technology Skills.txt` | 32.773 filas: 923 ocupaciones × 8.785 productos de software, en 137 clases UNSPSC. Marcas *Hot Technology* (171 productos) e *In Demand* |
| `Tools Used.txt` | 41.662 filas: 18.105 herramientas y equipos, en 4.126 clases UNSPSC |
| `UNSPSC Reference.txt` | Definiciones oficiales de las clases |
| `Emerging Tasks.txt` | Tareas nuevas identificadas por O\*NET, útiles para la tipología de tareas nuevas, modernizadas e híbridas |

**Presencia de los fabricantes citados** (ocupaciones donde aparece al menos un producto): Microsoft 894 · SAP 303 · IBM 241 · Oracle 240 · Adobe 250 · Autodesk 197 · Google 195 · Salesforce 92 · AWS 62 · Cisco 43.

## 3. Corpus de capacidades declaradas por los fabricantes

Para cada producto *Hot Technology* (171) y para cada clase UNSPSC (137), se construye un corpus de **enunciados de capacidad** a partir de documentación **pública** del fabricante: fichas de producto, documentación técnica y notas de versión. Se separan dos fases, como en el análisis original.
- **Fase 1, tecnología de negocio:** qué automatiza o soporta el producto. Por ejemplo, el *pipeline* comercial a partir de los datos que introducen los comerciales en el CRM.
- **Fase 2, IA incorporada:** funciones de IA del producto, como Microsoft Copilot, SAP Joule, Salesforce Einstein o IBM watsonx, y su fecha de lanzamiento.

**Cada enunciado lleva estos campos:**
- producto, fabricante, versión y fecha;
- URL y **copia archivada** (Wayback Machine) con fecha de acceso;
- el enunciado: una cita de ≤ 25 palabras o una paráfrasis;
- el tipo: apoyo, automatización o función de IA;
- la **calidad de la fuente: grado C** (autodeclaración comercial, según la jerarquía de fuentes de ITEA).

**Extracción:** un modelo de lenguaje de pesos abiertos, ejecutado en local con temperatura 0, propone los enunciados, y se registran el *prompt*, el modelo y la versión. Se revisa una muestra aleatoria. Solo se usa documentación pública sin registro, respetando `robots.txt` y las condiciones de uso.

**Cautela:** lo que declara un fabricante es lo que dice que hace su producto, no lo que hace en cada empresa. T mide **capacidad declarada**, y así se presenta.

## 4. Emparejamiento tarea por tarea dentro de cada ocupación

Para cada tarea de O\*NET 30.2 se toman **solo las tecnologías de su ocupación**, según *Technology Skills* y *Tools Used*, y:
1. se recuperan sus enunciados de capacidad más próximos con *embeddings* de frases, usando umbrales relativos por percentil como Kogan et al. (2023) y Hampole et al. (2025);
2. se reordenan con un clasificador NLI (*zero-shot*), con hipótesis como «This software performs the task» frente a «This software assists a worker in performing the task»;
3. se obtienen tres puntuaciones por tarea, en [0, 1], cada una con su **evidencia enlazada** (enunciado y URL): **T_apoyo**, **T_automatiza** y **T_IA**.

El enfoque replica la lógica de Webb (2019) y Kogan et al. (2023), que comparan el texto de lo que hace una tecnología (patentes) con el texto de las tareas, pero con documentación de producto en lugar de patentes.

## 5. Capa S: solvencia técnica certificable

Se construye un corpus de **objetivos de examen de certificación**, públicos en los programas de los fabricantes:
- Microsoft: las guías *skills measured* de cada certificación;
- Cisco: los *exam topics*;
- SAP, Oracle, IBM y AWS: sus áreas temáticas de certificación.

Se añaden los marcos europeos no comerciales: **e-CF (EN 16234-1)**, DigComp y las habilidades de ESCO.

Para cada par de tarea y capacidad emparejada en §4, se mide la similitud con los objetivos de certificación del mismo producto o clase y se obtienen:
- **S_cert:** si existe una certificación que cubra esa competencia (0/1 y similitud) y de qué tipo es (de fabricante o de un marco europeo);
- **Brecha = T × (1 − S_cert):** capacidad tecnológica sin solvencia certificable.

*Por verificar antes de construir:* las condiciones de uso de cada portal de certificación y la versión vigente de cada programa.

## 5 bis. Capa U: grado de utilización efectiva (aportación del autor, 23-10-2026)

**Idea.** Una tecnología tiene unas posibilidades máximas (el 100 % de lo que declara el fabricante), pero en la práctica las empresas usan normalmente **entre el 10 % y el 35 %** de ellas. Esa infrautilización genera problemas de **amortización y de retorno de la inversión (ROI)**, y la IA puede reducirla. T mide la capacidad declarada; U mide cuánto de esa capacidad se usa de verdad.

**Dos componentes, con fuentes distintas:**

| Componente | Qué mide | Fuente | Calidad |
|---|---|---|---|
| **U_adopción** (margen extensivo) | Proporción de empresas que tienen la tecnología | **Eurostat**, encuesta de uso de TIC en empresas: `isoc_eb_iip` (integración de procesos internos: ERP, CRM), `isoc_eb_ics` (cadena de suministro) e `isoc_eb_ai` (uso de IA), por sector NACE, tamaño y país | Oficial (grado A) |
| **U_profundidad** (margen intensivo) | Proporción de las capacidades del producto que se usan | No hay estadística oficial. Se trata como **supuesto explícito**: un rango de 0,10–0,35 según la experiencia profesional del autor, a contrastar con la literatura de sistemas de información y con informes del sector | Supuesto declarado; se recorre entero en el Monte Carlo |

**Realización tecnológica esperada de una tarea:** `R = T × U_adopción(sector, tamaño, país) × U_profundidad`.

**Hipótesis teórica central (publicable):** la IA eleva U_profundidad porque **reduce la barrera de competencia** que mantenía dormidas el 65–90 % de las funciones. Con una interfaz en lenguaje natural, los usuarios llegan a funciones que antes exigían pericia certificada. Hay tres consecuencias:
1. mejora el ROI de inversiones tecnológicas ya hechas y amortizadas solo en parte, lo que da a la empresa un incentivo a desplegar IA sobre sus sistemas existentes;
2. **la IA sustituye en parte a la solvencia técnica certificada (S)** como llave de acceso a las capacidades, y por tanto reduce el valor de negociación de esa pericia;
3. acelera la transferencia del conocimiento registrado en esos sistemas, lo que conecta con la tesis «almacenado ≠ codificado».

Contraste empírico posible: comparar sectores y países con distinta adopción de IA (`isoc_eb_ai`) y su evolución en el uso de ERP y CRM.

**Literatura de apoyo (verificada):**
- **Uso superficial frente a uso profundo:** Burton-Jones y Straub (2006), *ISR* 17(3), 10.1287/isre.1060.0096.
- **Conducta posterior a la adopción y uso de un subconjunto de funciones:** Jasperson, Carter y Zmud (2005), *MIS Quarterly* 29(3), 10.2307/25148694.
- **Uso ampliado de sistemas complejos:** Hsieh y Wang (2007), *EJIS* 16(3), 10.1057/palgrave.ejis.3000663.
- **Complementos organizativos y la curva en J del rendimiento:** Bresnahan, Brynjolfsson y Hitt (2002); Brynjolfsson, Rock y Syverson (2021).
- **La IA beneficia más a los trabajadores menos expertos:** Brynjolfsson, Li y Raymond (2025), *QJE* 140(2), 10.1093/qje/qjae044.

**Evidencia que cuantifica U_profundidad (búsqueda del 23-10-2026).** Las cuatro fuentes caen dentro del rango del autor, aunque ninguna es reciente y solo una es académica.

| Fuente | Ámbito y método | Resultado | Calidad |
|---|---|---|---|
| **McGrenere y Moore (2000)**, «Are We All In the Same "Bloat"?», *Graphics Interface 2000*, pp. 187–196, [PDF](http://www.graphicsinterface.org/wp-content/uploads/gi2000-25.pdf) (sin DOI en Crossref) | 53 usuarios de Microsoft Word 97; 265 funciones de primer nivel; cuestionario y entrevistas (autodeclarado) | **Uso medio del 27 % de las funciones** (rango 3–45 %); conocían el 51 %. El 15,8 % no lo usaba nadie y solo el 21,5 % lo usaba más de la mitad | **Académica revisada por pares** (verificada en el texto del PDF) |
| **Aberdeen Group (2006)**, *ERP in Manufacturing Benchmark* | Más de 1.000 empresas manufactureras; encuesta | **Uso del 27,6 % de las funciones del ERP**, aunque dos tercios lo eligieron por funcionalidad. La edición de 2007 da un 31,2 % (media ponderada) | Analista del sector. Solo verificada en prensa especializada ([Reliable Plant](https://www.reliableplant.com/Read/2571/study-finds-companies-use-just-276-of-erp-systems); [IndustryWeek](https://www.industryweek.com/information-technology/why-do-manufacturers-use-less-30-their-erp-capabilities), que da un 26,6 %); el informe original no se ha localizado |
| **Pendo (2019)**, *Feature Adoption Report* | Telemetría de 615 suscripciones de software en la nube | **El 80 % de las funciones se usa poco o nunca**; el 80 % de los clics se concentra en el 12 % de las funciones | Fabricante con interés comercial (grado C), aunque basado en datos de uso reales; [informe](https://go.pendo.io/rs/185-LQW-370/images/2019%20Feature%20Adoption%20Report%20Digital.pdf) |
| **Standish Group** (J. Johnson, ponencia en XP 2002) | 4 aplicaciones internas | Uso «siempre» del 7 %, «a menudo» del 13 % y «a veces» del 16 % (del 20 % al 36 % según el corte); el 45 % no se usa nunca | Débil: muestra mínima y sin documento original ([análisis de Cohn](https://www.mountaingoatsoftware.com/blog/are-64-of-features-really-rarely-or-never-used)) |

**Lectura:** el estudio académico (27 %) y el benchmark de ERP (27,6–31,2 %) sitúan el uso habitual en torno al **25–30 %**, y la telemetría de Pendo apunta a menos del 20 % de uso regular. Esto respalda un rango de **0,10–0,35** para U_profundidad, con un valor central de aproximadamente **0,27**. **Limitación declarada:** las fuentes son antiguas (2000–2007) o comerciales, así que el rango sigue siendo un supuesto bien informado y no una medición actual. Una aportación propia posible sería medirlo en entornos de ERP o CRM con IA.

## 6. Validación (sin referencia humana propia)

| Capa | Contraste externo |
|---|---|
| T_IA | Microsoft *Working with AI* (aplicabilidad por actividad intermedia, CC BY 4.0) y Anthropic Economic Index (uso real por tarea) |
| T | Marcas *Hot Technology* e *In Demand* de O\*NET, y cambios de empleo por ocupación |
| E frente a T_IA | Deben correlacionar de forma positiva pero no perfecta, porque la capacidad abstracta no es lo mismo que el producto disponible |
| S | Contraste con la presencia de certificaciones en ofertas de empleo, si se encuentran datos abiertos |

**Robustez:** se repite con otros umbrales, otros modelos de *embeddings* y con y sin `Tools Used`.

## 7. Piloto propuesto

**Finanzas y consultoría:** 27 ocupaciones de O\*NET (SOC 13-1111, 13-2xxx, 43-3xxx y 11-3031), 955 productos y 73 clases. Es el ámbito donde el autor tiene experiencia, el de los papers en curso y donde hay ecosistemas certificados (SAP FI/CO, Oracle Financials, Microsoft Dynamics, Salesforce). Se estiman 2–3 semanas.

**Criterio para escalar al resto:** que el emparejamiento sea plausible al revisar los extremos (validez aparente), que haya varianza dentro de cada ocupación y que converja con la referencia de Microsoft y Anthropic.

## 8. Literatura de apoyo (verificada en esta sesión)
- **Texto de la tecnología frente a tareas:** Webb (2019), 10.2139/ssrn.3482150 · Kogan et al. (2023), NBER w31846, 10.3386/w31846.
- **Tecnología y reorganización del trabajo:** Bresnahan, Brynjolfsson y Hitt (2002), *QJE* 117(1), 10.1162/003355302753399526 · Brynjolfsson, Rock y Syverson (2021), *AEJ: Macroeconomics* 13(1), 10.1257/mac.20180386.
- **Exposición frente a rentabilidad de automatizar:** Svanberg, Li, Fleming y Goehring (2024), SSRN 10.2139/ssrn.4700751.
- *Por buscar:* literatura sobre certificaciones profesionales de TI como señal de competencia y su efecto salarial; aplicabilidad por actividad intermedia de Tomlinson et al. (2025, Microsoft).

## 9. Decisiones pendientes
1. Empezar por el piloto de finanzas y consultoría.
2. Fijar la lista de fabricantes y programas de certificación del piloto.
3. Aprobar que la extracción de capacidades la haga un LLM local documentado. La alternativa es una curación manual, mucho más lenta.
4. Instalar las herramientas: `sentence-transformers`, `transformers` (NLI) y un modelo local (`llama.cpp`/`ollama`). Te daré los comandos.
