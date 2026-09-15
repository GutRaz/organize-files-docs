# Asistente de IA (MCP)

Los equipos con licencia conectan **OrganizeFiles.Cli** con Claude Desktop, **Cursor**, VS Code Copilot u otro cliente de Model Context Protocol, llamado cliente MCP más abajo. El conector es el paquete de Python **organize-files-mcp**. Es una descarga gratuita desde github.com/GutRaz/organize-files-docs, en su carpeta `mcp/`.

**En la aplicación de escritorio:** abra **Configuración del MCP...** en **Aplicación y datos**, en la columna de opciones, o desde el menú de herramientas. Elija **Acceso MCP**: **Desactivado**, **Monitor** o **Control**. Después copie el fragmento JSON. Vuelva a cargar MCP en la aplicación de IA después de cada cambio de nivel, porque **Control** crea un token nuevo cada vez.

**Pregunte al asistente de documentación** “setup mcp” o “cum setez mcp” para los pasos del sistema actual.

## Niveles de acceso MCP, ajustados en la aplicación

Los niveles corresponden a tres tipos de trabajo: **Lectura / Vista previa / Ejecución**.

| Nivel | Tipo de trabajo | Qué puede hacer la IA |
|-------|--------|-------------------|
| **Desactivado** | — | Solo `organize_mcp_status`. Sin diagnóstico y sin acceso al espacio de trabajo. |
| **Monitor** | **Lectura** | Todo lo de Desactivado, más diagnóstico de solo lectura, historial de ejecuciones y tareas, bloqueos, comprobaciones de auditoría, **`organize_capabilities`** y **`organize_workspace_snapshot`**. `organize_capabilities` lista los modos de ejecución, entre ellos **`ai`**, los ámbitos de movimiento y los destinos. `organize_workspace_snapshot` muestra el espacio de trabajo guardado en la ventana principal. Sin vista previa y sin ejecución. |
| **Control** | **Vista previa** / **Ejecución** | Todo lo de Monitor, más **`organize_create_job`**, **`organize_run_workspace`** y **`organize_remove_empty_organize_layout`**. Necesita un **token de control** en los ajustes de MCP, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **Vista previa** es `organize_run_workspace` cuando el espacio de trabajo guardado tiene **Simulación** activada, así que no se escribe nada. **Ejecución** es la misma herramienta con Simulación desactivada, así que los archivos se mueven. El conector omite `--confirm-destructive` salvo que la llamada fije `confirm_destructive=true`, y sin esa opción la línea de comandos se niega con `confirm_destructive_required`. |

El archivo de control es **`mcp-control.json`**, junto a `automation-jobs.json` en la carpeta de perfil de la aplicación. El fragmento copiado no lo nombra, porque el conector lo encuentra por sí mismo en la carpeta de perfil predeterminada. Fije **`ORGANIZE_FILES_MCP_CONTROL_FILE`** solo cuando el archivo esté en otro lugar. En **Control**, el fragmento también fija **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`**.

**Mover y eliminar exige un segundo paso, humano.** El asistente marca su propia confirmación, así que un texto que lea podría convencerlo de confirmar. Por eso, una ejecución que no es simulación necesita además una ventana abierta en **Configuración del MCP**, que se cierra sola a los 15 minutos. Fuera de ella el asistente puede preparar y previsualizar una ejecución, pero la ejecución en sí se rechaza. Tanto el archivo de control como la ventana están firmados con una clave que guarda esta instalación. Un archivo de control cambiado a mano o copiado de otro equipo cuenta como Desactivado.

## Herramientas MCP por nivel

**Siempre, también en Desactivado:** `organize_mcp_status`

**Monitor y Control:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` y `organize_run_raw_cli`, que solo acepta comandos de lectura.

**También en Monitor y Control:** `organize_capabilities`, que lista el modo de ejecución **`ai`** para archivos de IA y ML, y `organize_workspace_snapshot`.

**Solo Control:** `organize_create_job` desde el espacio de trabajo o desde un JSON de tarea, `organize_run_workspace` para una vista previa o una ejecución real según indique la Simulación del espacio de trabajo, y `organize_remove_empty_organize_layout`, que elimina carpetas de diseño vacías dentro de una salida existente y nunca crea la carpeta de salida en sí.

Los comandos que mueven o eliminan archivos siempre están bloqueados por MCP fuera del nivel **Control**. Ningún otro ajuste los permite.

## Opciones de línea de comandos que usa el conector

| Opción | Nivel | Propósito |
|------|-------|---------|
| `--mcp-control-status` | cualquiera | JSON con el nivel, la ruta del archivo de control y los indicadores de Monitor y Control |
| `--mcp-capabilities` | Monitor y superior | Lista JSON de los modos de ejecución, entre ellos **`ai`**, de los ámbitos de movimiento y de los destinos |
| `--mcp-workspace-snapshot` | Monitor y superior | El espacio de trabajo guardado y cómo se convierte en una tarea |
| `--mcp-create-job` | Control | Crear una tarea con `--from-workspace` o `--mcp-job-json` |
| `--mcp-run-workspace` | Control | Ejecutar el espacio de trabajo guardado, con `--allow-app-target` y `--mcp-control-token` |
| `--remove-empty-organize-layout` | Control | Eliminar carpetas de diseño vacías dentro de un `--output` existente |
| `--confirm-destructive` | Control | Necesaria con `--mcp-run-workspace` para una ejecución que mueve o elimina. El conector solo la pasa cuando `confirm_destructive=true` |

## Ajustes en el JSON del cliente MCP

| Ajuste | Cuándo |
|----------|------|
| `ORGANIZE_FILES_CLI` | Ruta a OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | Ruta a `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | Ruta a `mcp-control.json`, solo cuando no está en la carpeta de perfil predeterminada |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | Solo nivel **Control**, desde el fragmento de la aplicación |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | Nivel **Control**, para ejecuciones del espacio de trabajo guardado |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | Opcional. El mismo token que usa el anfitrión para las operaciones de lectura |

## Configuración en Windows

1. **Python 3.10 o posterior** — ejecute `python -V` en PowerShell. Si falta Python o es más antiguo, instálelo desde [python.org](https://www.python.org/downloads/) y marque **Add python.exe to PATH**.
2. **Descargar e instalar el conector** — descargue github.com/GutRaz/organize-files-docs como ZIP, descomprímalo y ejecute `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1`. El script crea un entorno de Python propio para el conector y muestra el comando para la aplicación de IA.
3. **En la aplicación:** **Configuración del MCP...**, elija **Monitor** o **Control** y copie el JSON.
4. **Rutas:** `%LocalAppData%\OrganizeFilesCrossPlatform\` guarda las tareas y `mcp-control.json`. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **Prueba** — ejecute `organize_mcp_status` y después `organize_server_info`. `cliResolved` debe ser true y `mcpLevel` debe coincidir con la aplicación.

## Configuración en macOS

Los mismos pasos con **python3** y `bash mcp/install-organize-files-mcp.sh`. Si `python3 -V` muestra 3.9 o ningún Python, instale primero Python desde [python.org](https://www.python.org/downloads/macos/). Rutas: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Configuración en Linux

Los mismos pasos con **python3** y `bash mcp/install-organize-files-mcp.sh`. En Debian y Ubuntu, ejecute primero `sudo apt install python3-venv`. Rutas: `~/.local/share/OrganizeFilesCrossPlatform/`, o `$XDG_DATA_HOME` cuando está definido, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Seguridad

- MCP se ejecuta como **el usuario local** del sistema operativo, con los mismos permisos que la línea de comandos ejecutada a mano.
- Mantenga en secreto el **token de control** y el **token de lectura**, como contraseñas. Vuelva a copiar el JSON después de activar Control.
- **`organize_run_workspace`** se ejecuta en la línea de comandos, no con el botón Ejecutar de la aplicación. No ejecute dos tareas sobre la misma carpeta de salida al mismo tiempo.
- Ejemplos: `mcp/examples/`.

## Ejecuciones que mueven o eliminan

`--mcp-run-workspace` exige `--confirm-destructive` para toda ejecución que no sea una simulación, ya mueva, elimine o archive. Sin ella, la línea de comandos responde `confirm_destructive_required`. El conector omite la opción salvo que la llamada fije `confirm_destructive=true`, y eso solo lo puede hacer el nivel Control. Por eso, de forma predeterminada, el conector se niega.

## Idiomas

Las respuestas sobre la configuración vienen de la misma guía traducida que la ventana Documentación y el Asistente de guía. `organize_capabilities` informa de los modos de ejecución y los destinos, no de nombres de temas de la aplicación.
