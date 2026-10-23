# Procedencia y limitaciones de los grados AXI heredados

**Fecha:** 23-10-2026.
**Ámbito:** el fichero `src/itea/data/axi_task_grades.csv.gz`, con 47.810 enunciados de tareas de O\*NET 29.1 y 923 ocupaciones. Es la entrada de OAXI-EU en ITEA v4.0.
**Versión en inglés:** `AXI_PROVENANCE_EN.md`.

## 1. Cómo se obtuvieron (según el autor)

- **Análisis tarea a tarea en su contexto profesional:** cómo la ejecuta la tecnología existente. Por ejemplo, un CRM que construye el embudo comercial con los datos que introducen los comerciales, o los motores de evaluación del riesgo operativo o de precios con datos de mercado.
- **Fuente:** las especificaciones técnicas públicas de varios fabricantes de software y hardware de negocio.
- **Tipología:** tareas nuevas, antiguas modernizadas e híbridas, y tareas que una herramienta nueva hace mejor y que obligan a reorganizar procesos.
- **Segunda fase:** cuánto amplían ese apoyo la IA generativa y la agéntica incorporadas a esas herramientas.
- **El coste de la tecnología se analizó, pero no se incorporó a los grados.**
- **Aplicación por patrones:** los juicios se aplicaron por **patrón tecnológico**. Cada patrón lleva grados y textos fijos, y hay un catálogo asociado de 244 tecnologías con fabricante y versión.
- **Lo que no quedó registrado:** cómo se asignaron los patrones a las 47.810 tareas (a mano, por *script* o con ayuda de un modelo de lenguaje). **Esa asignación no se puede reproducir.**

## 2. Lo que muestran los datos (análisis forense)

| Prueba | Resultado |
|---|---|
| El mismo enunciado en ocupaciones distintas (6.451 textos repetidos) | Grados idénticos en las cuatro escalas, sin ninguna inconsistencia |
| Diversidad de los textos explicativos | 5 justificaciones, 16 descripciones de IA generativa y 18 de IA agéntica, cada una ligada a un único grado |
| Poder predictivo del verbo inicial | La moda del verbo acierta el 95,5 % de los grados de automatización y el 95,4 % de los de codificabilidad |
| Escalas ligadas | `Auto_Grade = LOW` coincide exactamente con `CI_Grade = LOW_TRANS` (2.784 tareas) |
| Concentración | El 90,6 % de las tareas tiene el mismo grado de codificabilidad (`MEDIUM_SC`) |
| Unidad | Los enunciados de O\*NET están partidos en subenunciados (01a, 01b…); solo 23.890 encajan con O\*NET 30.2 |

## 3. Fiabilidad y validez medidas

**Codificadores automáticos independientes (junio de 2026).** Sobre 500 tareas estratificadas, con modelos de cuatro proveedores (DeepSeek, OpenAI, Perplexity y Google):

| Escala | α de Krippendorff | Lectura |
|---|---|---|
| Codificabilidad (`CI_Grade`) | 0,50 | Moderada |
| Automatización (`Auto_Grade`) | 0,35 | Insuficiente |

- **Codebook determinista:** un *codebook* basado en el verbo inicial reproduce los grados con κ ponderada de 0,74 (CI) y 0,70 (Auto), fuera de muestra. Los grados siguen patrones regulares, pero distinguen poco entre tareas parecidas.

**Panel humano y agentes documentados (julio de 2026).**
- **El estudio:** 20 evaluadores aportaron 580 valoraciones sobre 295 tareas, en una escala de codificabilidad de 0 a 3. Esas mismas tareas las graduaron también agentes de IA que documentaban sus fuentes.
- **Fiabilidad del panel:** la de una valoración individual es baja (α ≈ 0,14), como suele ocurrir con juicios no documentados.
- **El panel y los agentes convergen entre sí** (ρ = 0,39).
- **Cruzados con `CI_Grade`** en las mismas tareas, **la convergencia es casi nula:** ρ = 0,08 con la media del panel y entre −0,01 y 0,04 con los agentes. La media humana apenas cambia entre grados: 1,31 en LOW, 1,64 en MEDIUM y 1,58 en HIGH.

**Lectura:** el resultado agregado de OAXI-EU v4.0 converge con un índice europeo independiente (JRC145832: Pearson 0,736 y Spearman 0,819). En cambio, **la codificabilidad tarea a tarea de AXI no está validada**: las referencias independientes de esa misma escala no la reproducen.

## 4. Correcciones de la documentación anterior de ITEA

Algunos textos anteriores de ITEA describían los grados AXI como una clasificación hecha tarea a tarea, con justificación propia y una fiabilidad mayor que la medida. Entre ellos están la primera versión de la ficha de datos y el primer borrador del paper de JOSS. **Las únicas cifras de fiabilidad válidas son las de §3.**

## 5. Qué se hace con ellos

- **v4.0:** se mantienen como «grados heredados», con esta nota, para que los resultados publicados puedan reproducirse.
- **v4.1:** se sustituyen por la graduación automática y documentada de `itea.grading`, que **no se entrena con ellos** y se valida frente a referencias independientes con hipótesis registradas (`RESULTADOS_capa3_y_v41_ES.md`). OAXI-EU v4.1 conserva el orden general del índice v4.0 (Spearman 0,80).
