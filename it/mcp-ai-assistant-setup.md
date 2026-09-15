# Assistente AI (MCP)

I team con licenza collegano **OrganizeFiles.Cli** a Claude Desktop, **Cursor**, VS Code Copilot o a un altro client Model Context Protocol, di seguito chiamato client MCP. Il connettore è il pacchetto Python **organize-files-mcp**. È un download gratuito da github.com/GutRaz/organize-files-docs, nella cartella `mcp/`.

**Nell'app desktop:** apri **Configurazione MCP…** in **Applicazione e dati** nella colonna delle opzioni, oppure dal menu degli strumenti. Scegli **Accesso MCP**: **Spento**, **Monitor** o **Controllo**. Poi copia il frammento JSON. Ricarica MCP nell'app di IA dopo ogni cambio di livello, perché **Controllo** crea ogni volta un nuovo token.

**Chiedi all'assistente della documentazione** «setup mcp» o «cum setez mcp» per i passaggi sul sistema in uso.

## Livelli di accesso MCP, impostati nell'app

I livelli corrispondono a tre tipi di lavoro: **lettura / anteprima / esecuzione**.

| Livello | Tipo di lavoro | Cosa può fare l'IA |
|-------|--------|-------------------|
| **Spento** | — | Solo `organize_mcp_status`. Nessuna diagnostica e nessun accesso allo spazio di lavoro. |
| **Monitor** | **Lettura** | Tutto ciò che c'è in Spento, più diagnostica di sola lettura, cronologia di esecuzioni e processi, blocchi, verifiche di audit, **`organize_capabilities`** e **`organize_workspace_snapshot`**. `organize_capabilities` elenca le modalità di esecuzione, tra cui **`ai`**, gli ambiti di spostamento e le destinazioni. `organize_workspace_snapshot` mostra lo spazio di lavoro salvato nella finestra principale. Nessuna anteprima e nessuna esecuzione. |
| **Controllo** | **Anteprima** / **Esecuzione** | Tutto ciò che c'è in Monitor, più **`organize_create_job`**, **`organize_run_workspace`** e **`organize_remove_empty_organize_layout`**. Serve un **token di controllo** nelle impostazioni MCP, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **Anteprima** è `organize_run_workspace` quando lo spazio di lavoro salvato ha **Simulazione** attiva, quindi non viene scritto nulla. **Esecuzione** è lo stesso strumento con Simulazione disattivata, quindi i file vengono spostati. Il connettore omette `--confirm-destructive` a meno che la chiamata non imposti `confirm_destructive=true`, e senza questa opzione la riga di comando rifiuta con `confirm_destructive_required`. |

Il file di controllo è **`mcp-control.json`**, accanto a `automation-jobs.json` nella cartella del profilo dell'app. Il frammento copiato non nomina il file, perché il connettore trova il file nella cartella del profilo predefinita. Imposta **`ORGANIZE_FILES_MCP_CONTROL_FILE`** solo quando il file si trova altrove. In **Controllo** il frammento imposta anche **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`**.

**Spostare ed eliminare richiede un secondo passaggio, umano.** L'assistente imposta da sé la conferma, quindi un testo letto durante il lavoro potrebbe portare l'assistente a confermare. Un'esecuzione che non è una simulazione richiede perciò anche una finestra aperta in **Configurazione MCP**, e quella finestra si chiude da sola dopo 15 minuti. Fuori da questa finestra l'assistente può ancora preparare un'esecuzione e mostrarne l'anteprima, ma l'esecuzione vera e propria viene rifiutata. Sia il file di controllo sia la finestra sono firmati con una chiave che questa installazione conserva. Un file di controllo modificato a mano o copiato da un altro computer vale come Spento.

## Strumenti MCP per livello

**Sempre, anche in Spento:** `organize_mcp_status`

**Monitor e Controllo:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` e `organize_run_raw_cli`, che accetta solo comandi di sola lettura.

**Anche in Monitor e Controllo:** `organize_capabilities`, che elenca la modalità di esecuzione **`ai`** per i file di IA e ML, e `organize_workspace_snapshot`.

**Solo Controllo:** `organize_create_job` dallo spazio di lavoro o da un JSON di processo, `organize_run_workspace` per un'anteprima o un'esecuzione reale secondo la Simulazione dello spazio di lavoro, e `organize_remove_empty_organize_layout`, che rimuove le cartelle di layout vuote dentro un output esistente e non crea mai la cartella di output stessa.

I comandi che spostano o eliminano file sono sempre bloccati tramite MCP fuori dal livello **Controllo**. Nessun'altra impostazione li consente.

## Opzioni della riga di comando usate dal connettore

| Opzione | Livello | Scopo |
|------|-------|---------|
| `--mcp-control-status` | qualsiasi | JSON con il livello, il percorso del file di controllo e gli indicatori di Monitor e Controllo |
| `--mcp-capabilities` | Monitor e superiori | Elenco JSON delle modalità di esecuzione, tra cui **`ai`**, degli ambiti di spostamento e delle destinazioni |
| `--mcp-workspace-snapshot` | Monitor e superiori | Lo spazio di lavoro salvato e come diventa un processo |
| `--mcp-create-job` | Controllo | Crea un processo con `--from-workspace` o `--mcp-job-json` |
| `--mcp-run-workspace` | Controllo | Esegue lo spazio di lavoro salvato, con `--allow-app-target` e `--mcp-control-token` |
| `--remove-empty-organize-layout` | Controllo | Rimuove le cartelle di layout vuote dentro un `--output` esistente |
| `--confirm-destructive` | Controllo | Necessaria con `--mcp-run-workspace` per un'esecuzione che sposta o elimina. Il connettore passa questa opzione solo quando `confirm_destructive=true` |

## Impostazioni nel JSON del client MCP

| Impostazione | Quando |
|----------|------|
| `ORGANIZE_FILES_CLI` | Percorso di OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | Percorso di `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | Percorso di `mcp-control.json`, solo quando il file non è nella cartella del profilo predefinita |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | Solo livello **Controllo**, dal frammento dell'app |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | Livello **Controllo**, per le esecuzioni dello spazio di lavoro salvato |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | Facoltativo. Lo stesso token che l'host usa per le operazioni di lettura |

## Configurazione su Windows

1. **Python 3.10 o successivo** — esegui `python -V` in PowerShell. Se Python manca o è più vecchio, installa Python da [python.org](https://www.python.org/downloads/) e spunta **Add python.exe to PATH**.
2. **Scarica e installa il connettore** — scarica github.com/GutRaz/organize-files-docs come ZIP, estrai l'archivio ed esegui `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1`. Lo script crea un ambiente Python riservato al connettore e mostra il comando per l'app di IA.
3. **Nell'app:** **Configurazione MCP…**, scegli **Monitor** o **Controllo**, poi copia il JSON.
4. **Percorsi:** `%LocalAppData%\OrganizeFilesCrossPlatform\` contiene i processi e `mcp-control.json`. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **Test** — esegui `organize_mcp_status`, poi `organize_server_info`. `cliResolved` deve essere true e `mcpLevel` deve corrispondere all'app.

## Configurazione su macOS

Gli stessi passaggi con **python3** e `bash mcp/install-organize-files-mcp.sh`. Se `python3 -V` mostra 3.9 o nessun Python, installa prima Python da [python.org](https://www.python.org/downloads/macos/). Percorsi: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Configurazione su Linux

Gli stessi passaggi con **python3** e `bash mcp/install-organize-files-mcp.sh`. Su Debian e Ubuntu esegui prima `sudo apt install python3-venv`. Percorsi: `~/.local/share/OrganizeFilesCrossPlatform/`, oppure `$XDG_DATA_HOME` quando è impostata, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Sicurezza

- MCP viene eseguito come **l'utente locale** del sistema operativo, con gli stessi diritti della riga di comando eseguita a mano.
- Tieni segreti il **token di controllo** e il **token di lettura**, come le password. Copia di nuovo il JSON dopo aver attivato Controllo.
- **`organize_run_workspace`** viene eseguito nella riga di comando, non tramite il pulsante Esegui dell'app. Non eseguire due processi sulla stessa cartella di output nello stesso momento.
- Esempi: `mcp/examples/`.

## Esecuzioni che spostano o eliminano

`--mcp-run-workspace` richiede `--confirm-destructive` per ogni esecuzione che non è una simulazione, che sposti, elimini o archivi. Senza questa opzione la riga di comando risponde `confirm_destructive_required`. Il connettore omette l'opzione a meno che la chiamata non imposti `confirm_destructive=true`, e solo il livello Controllo può farlo. Quindi, per impostazione predefinita, il connettore rifiuta.

## Lingue

Le risposte sulla configurazione vengono dalla stessa guida tradotta della finestra Documentazione e dell'Assistente guida. `organize_capabilities` riporta modalità di esecuzione e destinazioni, non nomi di temi dell'app.
