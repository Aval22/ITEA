# Codificación humana de referencia (K y E)

Procedimiento definido en `docs/grading/LIBRO_CRITERIOS_v0.1_ES.md`, §6.

| Fichero | Contenido |
|---|---|
| `ITEA_codificacion_K_E_400.xlsx` | Formulario: 400 tareas de O\*NET 30.2 con instrucciones y listas desplegables |
| `scripts/grading/make_human_sample.py` | Genera la muestra y el formulario (semilla 20261023; reproducible) |
| Clave de la muestra (privada, fuera del repositorio) | GWA, clase previa, estrato y marca de recodificación de cada tarea. **No se abre hasta terminar la codificación** |

## Muestra
- **400 tareas** de 327 ocupaciones distintas, con como máximo 3 por ocupación, que cubren los 22 grandes grupos SOC.
- **Reparto por clase previa de codificabilidad** (según la GWA): 134 alta, 133 media y 133 baja. Dentro de cada clase, el reparto es proporcional al gran grupo SOC.
- **100 tareas marcadas para recodificar** (34, 33 y 33), elegidas al azar dentro de cada clase. La marca solo está en la clave.

## Procedimiento
1. **Codificar las 400 tareas en sesiones de 40–50,** sin consultar O\*NET, ESCO, los grados AXI ni modelos. Durante la codificación tampoco hay que releer la §3 del libro de criterios, que asigna clases a las GWA.
2. **Al terminar,** guardar el formulario con la fecha en el nombre y no modificarlo más.
3. **Al menos 3 semanas después,** generar el formulario de recodificación (las 100 tareas marcadas, en otro orden) y codificarlo a ciegas, sin mirar el primero.
4. **Calcular los acuerdos:**
   - la κ ponderada intracodificador;
   - el acuerdo con las etiquetas humanas de Eloundou et al. (2024) para E, en las tareas comunes.

## Licencia
Los enunciados de las tareas son de O\*NET 30.2 (USDOL/ETA, CC BY 4.0). Las codificaciones del autor se publicarán con CC BY 4.0.
