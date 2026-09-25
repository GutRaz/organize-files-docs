# Supervisión con Prometheus y Grafana

## Qué abarcan los contadores

Los trabajos programados mantienen un conjunto reducido de contadores y medidores de Prometheus. Cada nombre empieza por `organize_files_automation_`, y el conjunto completo se publica como texto de Prometheus. Los tres anfitriones que ejecutan trabajos publican el mismo conjunto: la aplicación de escritorio, el servicio `OrganizeFiles.JobAgent` y el anfitrión de línea de comandos usado dentro de contenedores.

Los contadores describen el planificador, no los archivos. Se cuentan las pasadas, los resultados de los trabajos, las aprobaciones, la entrega de webhooks y el mantenimiento del historial. No se cuenta nada sobre los archivos que un trabajo mueve.

## Exportación a un archivo, sin abrir ningún puerto

`automation-metrics.prom` se escribe en la carpeta de datos de automatización, junto a `automation-jobs.json`, y se actualiza tras cada pasada vencida y en cada lectura. El formato es el que lee el colector textfile de `node_exporter`, así que una máquina que ya ejecuta `node_exporter` queda cubierta sin puerto a la escucha, sin testigo y sin regla de cortafuegos. El archivo se reemplaza de forma atómica, y un enlace simbólico dejado en su lugar detiene la escritura en vez de seguirse.

## Punto de lectura

El punto de lectura solo existe cuando `ORGANIZE_FILES_METRICS_HTTP_PORT` contiene un puerto entre 1 y 65535. Sin esa variable no escucha nada.

| Variable | Efecto |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | Puerto de escucha. Si falta o queda fuera de rango, no hay punto de lectura alguno. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Dirección de escucha. El valor predeterminado es `127.0.0.1`. Los valores `0.0.0.0`, `+` y `*` significan todas las direcciones, y cualquier otro vuelve a `127.0.0.1`. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | Testigo bearer exigido en `/metrics` y en `/ready`. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` deja que `/ready` responda sin ese testigo, para las sondas de clúster. Las rutas del anfitrión quedan entonces fuera de la respuesta. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | Códigos de salida separados por comas que hacen que `/ready` informe de no estar listo. Sustituye a la lista incorporada. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` pasa por alto el código de salida de la última pasada, y también el estado anterior a que termine la primera. |
| `ORGANIZE_FILES_READY_JSON` | `1` impone la respuesta JSON en `/ready`, incluso para quien pidió texto sin formato. |

Una dirección fuera del bucle local se rechaza antes de abrir el escucha si no hay testigo bearer. El rechazo se escribe en la salida de error y se emite como evento de webhook, porque esa combinación entregaría los contadores a toda la red.

## Rutas servidas

- `/metrics` — los contadores como texto de Prometheus. Una petición a `/` devuelve el mismo contenido.
- `/ready` — preparación para un orquestador. Responde `200` en cuanto la carpeta de automatización acepta una escritura de prueba, el archivo de trabajos se abre, la carpeta de historial se resuelve dentro de la raíz de datos y la última pasada vencida terminó con un código de salida que no bloquea. En caso contrario responde `503` con un motivo breve como `due_pass_not_completed` o `last_due_pass_license_failed`.
- `/health` — solo señal de vida. Esa ruta sigue siendo anónima incluso con un testigo definido, porque responde `ok` y nada más.

Los códigos de salida `3` por fallo de licencia, `8` por árbol de salida bloqueado, `10` por un borrado nunca confirmado y `11` por conflicto de reclamación bloquean la preparación de forma predeterminada. El cuerpo de `/ready` es JSON salvo que quien llama envíe `Accept: text/plain` o añada `?format=text`.

## Los contadores

| Nombre | Contenido |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Pasadas vencidas iniciadas por el planificador. |
| `organize_files_automation_jobs_started_total` | Ejecuciones de trabajo que llegaron al estado en curso. |
| `organize_files_automation_jobs_skipped_total` | Trabajos omitidos: entorno de Docker o Kubernetes que no está listo, trabajo dirigido a la aplicación en un anfitrión sin interfaz, raíz de salida ocupada, o trabajo rechazado por el orquestador. |
| `organize_files_automation_jobs_failed_total` | Ejecuciones de trabajo terminadas en fallo. |
| `organize_files_automation_jobs_awaiting_approval_total` | Ejecuciones reales detenidas a la espera de aprobación. |
| `organize_files_automation_execute_approvals_total` | Aprobaciones concedidas a una ejecución real. |
| `organize_files_automation_execute_approvals_expired_total` | Aprobaciones cuyo plazo venció antes de usarse. |
| `organize_files_automation_claim_conflicts_total` | Veces en que otro anfitrión ya tenía la reclamación sobre la raíz de salida. |
| `organize_files_automation_runs_orphaned_total` | Ejecuciones recuperadas como huérfanas, dejadas por un anfitrión detenido. |
| `organize_files_automation_job_events_total` | Un contador por evento, con las etiquetas `event`, `job_id`, `target` y `jobs_file`. |
| `organize_files_automation_webhook_posts_succeeded_total` | Entregas de webhook aceptadas. |
| `organize_files_automation_webhook_posts_failed_total` | Entregas de webhook rechazadas o inalcanzables. |
| `organize_files_automation_webhook_dead_letter_depth` | Filas que esperan ahora mismo en el archivo de webhooks no entregados. |
| `organize_files_automation_log_retention_pruned_total` | Registros de ejecución eliminados por la retención. |
| `organize_files_automation_runs_index_compacted_total` | Filas retiradas del índice de ejecuciones durante la compactación. |
| `organize_files_automation_last_due_pass_exit_code` | Código de salida de la última pasada terminada. `0` es una pasada limpia. |
| `organize_files_automation_last_due_pass_completed_utc` | Hora Unix en segundos de la última pasada terminada, y `0` antes de la primera. |

## Panel y reglas de alerta

Un panel de Grafana ya preparado se publica con los archivos de despliegue como `grafana-organize-files-automation.json`, con el título **OrganizeFiles Automation**. Sus diez cuadros muestran las pasadas vencidas, los trabajos iniciados y fallidos, los conflictos de reclamación, el caudal de trabajos en una hora, el último código de salida, la profundidad de los mensajes no entregados, los fallos de webhook en un día, los trabajos que esperan aprobación y los eventos de trabajo por estado. Cada cuadro nombra su fuente de datos mediante el marcador `${DS_PROMETHEUS}`.

Las reglas de alerta correspondientes son `alerts-organize-files-automation.yaml`, con `prometheus-rule-automation.yaml` como envoltura de Kubernetes para `kube-prometheus-stack`. Un último código de salida distinto de cero avisa a los cinco minutos, un fallo de licencia es crítico al minuto, y el resto de reglas cubre los trabajos fallidos, los conflictos de reclamación, los fallos de webhook, un atasco de mensajes no entregados y las aprobaciones dejadas en espera un día. Ambos archivos se validan en cada compilación, de modo que los nombres anteriores siguen el paso de los contadores.

# Salida de la ejecución y métricas

## Fila de estado

El área **Salida de la ejecución** muestra:

- Estado actual de la aplicación y progreso del motor.
- **CPU** y dos valores de **memoria** solo para este proceso.
- Líneas de **GPU**, en Windows: la parte de cada tarjeta gráfica que usa este proceso, no la tarjeta completa.

La misma barra de recursos compacta se reutiliza en ventanas de herramientas secundarias, como exploración de archivos, trabajos programados y reparación de archivos.

## Etiquetas de memoria

- **Bytes privados/compromiso**: memoria virtual privada reservada por el proceso.
- **Conjunto de trabajo/memoria**: RAM residente que actualmente posee este proceso. Puede diferir de otro monitor de sistema operativo porque las etiquetas de cada sistema operativo y entorno de escritorio procesan la memoria de manera diferente.

## Ejecutar JSON de latido (opcional)

Habilite **Escribir JSON de latido de ejecución** en **Avanzado/Diagnóstico**. El motor escribe `Organize.Files.run.json` en `Output\_OrganizeMediaLogs` (la misma carpeta que el archivo de reanudación organizado predeterminado).

- **Ruta**: se actualiza atómicamente durante las ejecuciones de organización y reparación.
- **Cadencia** — mientras se recorren las fuentes, el archivo se reescribe cada 10.000 archivos vistos, cada 5.000 coincidencias y cada 15 segundos aproximadamente mientras el recorrido sigue en marcha, de modo que un árbol de red grande que tarda en listarse sigue mostrando que la ejecución está viva. Durante la validación, el hasheo y los movimientos se reescribe tras cada 1.000 archivos, como mucho cada cinco segundos. Las escrituras de inicio y de fin siguen ocurriendo cuando una ejecución empieza y termina.
- **Avance** — mientras el número de archivos sigue creciendo, la barra principal muestra los archivos vistos hasta ahora en lugar del 100 %, hasta que una fase tiene un total conocido.
- **Campos** — `schema`, `mode`, `phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`), `runState` (`active` / `completed` / `failed` / `cancelled`), `utc` (ISO-8601), `dryRun`, `outputRoot`, `validateMedia`, `deepVideoValidate`, `gpuDeviceCount`, `hwaccel`, opcional `correlationId`, contadores `progress` anidados.
- **Registro**: el panel de salida de ejecución imprime la ruta completa al inicio y cuando se guarda el archivo al final. Utilice **Abrir carpeta de registro de latidos** / **Mostrar archivo JSON de latidos** en Avanzado/Diagnóstico.
- **CLI** — `--heartbeat-json` en OrganizeFiles.Cli. Cancelación y errores fatales de shell escriben `cancelled` / `failed` `runState` cuando está habilitado.
