# Avanzado / Diagnóstico

## Organizar la sintonización

Avanzado/Diagnóstico expone las opciones de **OrganizeFilesEngine** sin saturar el panel principal.

Los modos de organización pueden ajustar la deduplicación, el índice de destino, las reglas de fecha únicas, los subprocesos de enumeración y movimiento, el suplemento BFS, el archivo de reanudación y raíces únicas adicionales.

La reparación mantiene solo el tiempo de reintento de red y disco lleno, carriles de hardware de gráficos detectados para verificación de video completa opcional, búfer de lectura hash y latido JSON. Otros campos son visibles por contexto pero están deshabilitados.

Cuando las fuentes o la salida se encuentran en las rutas NAS o UNC, reduzca el paralelismo, mantenga habilitado el reintento de red, deje activado el suplemento BFS para árboles SMB impares y pruebe el búfer hash de 8 MiB si el hash es lento.

# Avanzado/Diagnóstico: cada opción

## Acerca de este capítulo

Estos controles son opciones del motor. El escritorio (Windows, macOS, Linux), Android, iOS y la herramienta de línea de comandos leen los mismos valores.

Los modos **Organizar** utilizan todos los controles siguientes, a menos que la interfaz los atenúe. **Reparación** utiliza solo el reintento de red, el reintento por disco lleno, los carriles de hardware gráfico detectados (con verificación de vídeo completa), el búfer de lectura de hash, el JSON de latido, **Archivo de reanudación de estado** y **Empezar de nuevo (truncar el archivo de reanudación)**. Los demás campos permanecen visibles, pero se ignoran durante la reparación.

## Fuentes de red (NAS / UNC)

Cuando las fuentes o salidas están en recursos compartidos SMB/CIFS, volúmenes NAS o unidades asignadas, revise esta sección detenidamente.

- **Por qué ajustar**: el número de subprocesos que funcionan en un SSD local puede detener o sobrecargar un archivador.
- **Qué probar**: mantenga activado el reintento de red. Baje los subprocesos de movimiento y enumere el máximo paralelo en los tiempos de espera. Deje activado el suplemento BFS a menos que se haya verificado un recuento completo sin él. Pruebe el búfer hash de 8 MiB cuando el hash sea lento en la red.
- **Desactivar espera de red**: falla rápidamente en errores de red transitorios. Arriesgado con Wi-Fi o acciones ocupadas.

## Modo de deduplicación

Cómo decide el motor que dos archivos están duplicados.

| Modo | Qué hace | Cuándo utilizar | Compensación |
| ---- | ------------ | ----------- | --------- |
| **Hash (SHA-256)** | Lee y codifica el contenido completo de cada archivo fuente incluido, luego agrupa bytes idénticos. | Modo práctico más fuerte. Hash (SHA-256) es obligatorio para el borrado in situ (duplicados y archivos problemáticos). | Más lento en árboles grandes o NAS. Ningún algoritmo debe presentarse como una garantía absoluta. |
| **Tamaño + hora + nombre** | Clave = tamaño, ticks de última escritura UTC, nombre en minúsculas y luego verificación SHA-256 completa. | Modo de compatibilidad conservador para diseños de carpetas multimedia más antiguos. | Se pueden perder duplicados renombrados. Nunca lo use con la eliminación de duplicados ni de archivos problemáticos. |
| **Ninguno** | Sin deduplicación entre archivos. | Sólo clasificación, no limpieza duplicada. | Los duplicados permanecen en las fuentes. |

## Omitir índice de destino

- **Desactivado (predeterminado)**: escanea la salida **Única** existente y la indexa antes del hash. Más seguro al reutilizar la misma carpeta de salida.
- **Activado**: omite ese escaneo.
- **Beneficio**: más rápido en árboles de producción enormes.
- **Riesgo**: puede aparecer más contenido duplicado dentro de Unique.

## Año mínimo de Unicos

Año calendario mínimo para carpetas de fechas en **Único** en diseños de medios. **Por qué**: evita distribuir archivos muy antiguos en carpetas de años impares cuando los metadatos son incorrectos.

## Mover hilos

El archivo paralelo se mueve después de reservar los destinos.

- **Más alto**: más rápido en SSD local.
- **Inferior**: más seguro en unidades asignadas NAS, USB o Wi-Fi.

## Hilos de clasificación y hash

Trabajadores paralelos durante el escaneo de origen y el deduplicado SHA-256.

- **Hilos de clasificación** — Descubrimiento y clasificación de archivos. CLI: `--classify-threads <n>`.
- **Hilos de hash** — Trabajadores de hash de contenido. CLI: `--hash-threads <n>`.
- **Anulaciones** — Los valores manuales anulan los predeterminados del perfil de organización (`--profile`).

## Enum paralelo máximo

Límite para el listado de directorios paralelos durante el análisis.

- **0** = motor automático.
- **Inferior**: menos presión para SMB cuando se listan muchas carpetas a la vez.

## Suplemento BFS pase de directorio

- **Activado (predeterminado)** — Un recorrido adicional a lo ancho y poco profundo.
- **Por qué** — Algunas rutas NAS o árboles profundos parecen incompletos tras el primer recorrido.
- **Desactivado** — Solo tras comprobar un recuento completo de archivos sin él.
- **CLI** — `--no-bfs` desactiva este recorrido.

## Archivo de reanudación de estado

Ruta opcional UTF-8. Los movimientos exitosos agregan líneas `B64|` para que la siguiente ejecución de organización pueda omitir las fuentes terminadas.

- **Por qué**: continuar con trabajos prolongados después de una parada o un fallo.
- **Ruta predeterminada**: cuando el campo está vacío en tiempo de ejecución, el motor utiliza `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt`. Sin salida, usa `sessions\<id>\resume\OrganizeFiles.resume.txt` en el perfil de la aplicación.
- **IU de escritorio**: lista de rutas de solo lectura para seleccionar y copiar con el mouse. Cuando ya existe un archivo de reanudación en la ubicación predeterminada, la ruta aparece automáticamente. **Examinar** selecciona una carpeta de registro y agrega `OrganizeFiles.resume.txt`. **Eliminar** borra el camino. Cuando está vacía, la sugerencia muestra la ruta utilizada en tiempo de ejecución.

## Iniciar de nuevo

Trunca el archivo de reanudación cuando se inicia una ejecución de organización **real** (la ejecución de prueba no se trunca). Con **Guardar progreso y espacio de trabajo**, también se borra la instantánea de la interfaz de usuario guardada al inicio de la ejecución. **Por qué**: fuerce un recuento completo en lugar de continuar con un registro de archivo de reanudación anterior.

## Raíces de escaneo

únicas adicionales Una carpeta por línea: árboles **Únicos** adicionales para indexar (diseño heredado, otro volumen).

- **Por qué**: Dedupe puede ver archivos que ya están organizados en otro lugar sin tener que moverlos nuevamente.
- **IU de escritorio**: lista de solo lectura para copia por línea. **Agregar** agrega una carpeta seleccionada. **Eliminar** elimina la línea seleccionada (por ejemplo, un árbol antiguo `Uniques` en NAS).

## Reintento de red (segundos)

Segundos para reintentar la entrada y salida de red pasajera.

- **Por qué** — Los servidores SMB cierran las sesiones ociosas. Lo usan organizar y reparar.
- **Desactivar la espera de red** — Deja de esperar y falla en su lugar.

## Reintento de disco lleno

(segundos) / Desactivar espera de disco lleno

Mismo patrón cuando el volumen de salida se queda sin espacio. **Por qué**: es hora de liberar el disco durante ejecuciones largas.

## Carriles de la tarjeta gráfica

Solo cuando la **comprobación completa de vídeo** integrada está activada y **Usar la tarjeta gráfica detectada** también. Un valor por encima de **0** fija un número explícito de carriles para la validación en paralelo entre los fabricantes detectados (NVIDIA, AMD, Intel, Apple, móvil). **0** significa que el número de carriles se averigua solo. No significa solo procesador. Para muestrear solo en el procesador, elija **Solo CPU** en la lista de tarjetas gráficas. Las etiquetas de carril planifican la validación del flujo de bits en el procesador. No invocan la descodificación de vídeo por hardware del sistema.

- **Preajuste de la CLI** — `--hwaccel <value>` elige un preajuste de carriles de validación (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`) cuando se ejecuta la comprobación completa de vídeo.

## Búfer de lectura hash

Búfer de lectura por trabajador durante el hash (512 KiB, 1 MiB, 8 MiB). **Por qué**: los búferes más grandes ayudan cuando un NAS o un recurso compartido de alta latencia tarda en responder.

## Registrar diario de deshacer

Diario JSONL opcional de los movimientos bajo la raíz de salida de la ejecución.

- **Para qué** — Permite deshacer desde la CLI tras una ejecución real de organización.
- **Archivo** — El archivado posterior queda desactivado mientras el diario de deshacer está activo.
- **CLI** — `--record-undo-journal` (igual que la casilla de la ventana principal).

## Escribir run heartbeat JSON

Escribe el archivo opcional `Organize.Files.run.json` bajo `Output\_OrganizeMediaLogs`.

- **Por qué** — Herramientas externas pueden leer contadores en vivo (recorridos, planificados, completados) mientras se organiza o se repara.
- **Cadencia** — Cada 10.000 archivos vistos, cada 5.000 coincidencias y cada 15 segundos aproximadamente durante los recorridos de las fuentes, tras cada 1.000 archivos y como mucho cada cinco segundos durante la validación, el hasheo y los movimientos, y en cada fase importante.
