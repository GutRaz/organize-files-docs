# AI asistent (MCP)

Licencované týmy připojují **OrganizeFiles.Cli** k Claude Desktop, **Cursor**, VS Code Copilot nebo jinému klientovi Model Context Protocol, dále jen klient MCP. Konektor je balíček Pythonu **organize-files-mcp**. Je zdarma ke stažení z github.com/GutRaz/organize-files-docs, ve složce `mcp/`.

**V desktopové aplikaci:** otevřete **Nastavení MCP…** ve skupině **Aplikace a data** ve sloupci možností nebo z nabídky nástrojů. Zvolte **MCP přístup**: **Vypnuto**, **Monitor** nebo **Kontrola**. Pak zkopírujte fragment JSON. Po každé změně úrovně znovu načtěte MCP v aplikaci AI, protože úroveň **Kontrola** pokaždé vytvoří nový token.

**Zeptejte se asistenta dokumentace** „setup mcp“ nebo „cum setez mcp“ a dostanete kroky pro aktuální systém.

## Úrovně přístupu MCP, nastavené v aplikaci

Úrovně odpovídají třem druhům práce: **čtení / náhled / spuštění**.

| Úroveň | Druh práce | Co může AI dělat |
|-------|--------|-------------------|
| **Vypnuto** | — | Jen `organize_mcp_status`. Žádná diagnostika a žádný přístup k pracovnímu prostoru. |
| **Monitor** | **Čtení** | Vše z úrovně Vypnuto a navíc diagnostika jen pro čtení, historie běhů a úloh, zámky, kontroly auditu, **`organize_capabilities`** a **`organize_workspace_snapshot`**. `organize_capabilities` vypíše režimy běhu, mezi nimi **`ai`**, rozsahy přesunu a cíle. `organize_workspace_snapshot` ukáže pracovní prostor uložený v hlavním okně. Žádný náhled a žádné spuštění. |
| **Kontrola** | **Náhled** / **Spuštění** | Vše z úrovně Monitor a navíc **`organize_create_job`**, **`organize_run_workspace`** a **`organize_remove_empty_organize_layout`**. Potřebuje **kontrolní token** v nastavení MCP, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **Náhled** je `organize_run_workspace`, když má uložený pracovní prostor zapnutý **Zkušební běh**, takže se nic nezapíše. **Spuštění** je tentýž nástroj, když je Zkušební běh vypnutý, takže se soubory přesunou. Konektor vynechá `--confirm-destructive`, pokud volání nenastaví `confirm_destructive=true`, a bez tohoto přepínače příkazový řádek odmítne s `confirm_destructive_required`. |

Řídicí soubor je **`mcp-control.json`**, vedle `automation-jobs.json` ve složce profilu aplikace. Zkopírovaný fragment tento soubor neuvádí, protože konektor soubor najde ve výchozí složce profilu. **`ORGANIZE_FILES_MCP_CONTROL_FILE`** nastavte jen tehdy, když je soubor jinde. Na úrovni **Kontrola** fragment nastaví také **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`**.

**Přesun a mazání vyžadují druhý krok, který udělá člověk.** Asistent si potvrzení nastavuje sám, takže text, který asistent čte, by asistenta mohl k potvrzení přemluvit. Běh, který není zkušebním během, proto potřebuje také okno otevřené v **Nastavení MCP**, a to okno se samo zavře po 15 minutách. Mimo toto okno může asistent běh stále připravit a zobrazit náhled běhu, ale samotný běh je odmítnut. Řídicí soubor i okno jsou podepsané klíčem, který má tato instalace. Řídicí soubor změněný ručně nebo zkopírovaný z jiného počítače platí jako úroveň Vypnuto.

## Nástroje MCP podle úrovně

**Vždy, i na úrovni Vypnuto:** `organize_mcp_status`

**Monitor a Kontrola:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` a `organize_run_raw_cli`, který přijímá jen příkazy pro čtení.

**Také na úrovních Monitor a Kontrola:** `organize_capabilities`, který vypisuje režim běhu **`ai`** pro soubory AI a ML, a `organize_workspace_snapshot`.

**Jen Kontrola:** `organize_create_job` z pracovního prostoru nebo z JSON úlohy, `organize_run_workspace` pro náhled nebo skutečný běh podle nastavení Zkušební běh v pracovním prostoru, a `organize_remove_empty_organize_layout`, který odstraní prázdné složky rozvržení uvnitř existujícího výstupu a nikdy nevytvoří samotnou výstupní složku.

Příkazy, které přesouvají nebo mažou soubory, jsou přes MCP mimo úroveň **Kontrola** vždy blokované. Žádné jiné nastavení je nepovolí.

## Přepínače příkazového řádku, které konektor používá

| Přepínač | Úroveň | Účel |
|------|-------|---------|
| `--mcp-control-status` | jakákoli | JSON s úrovní, cestou k řídicímu souboru a příznaky úrovní Monitor a Kontrola |
| `--mcp-capabilities` | Monitor a výše | Seznam JSON s režimy běhu, mezi nimi **`ai`**, s rozsahy přesunu a s cíli |
| `--mcp-workspace-snapshot` | Monitor a výše | Uložený pracovní prostor a jak se z tohoto prostoru stane úloha |
| `--mcp-create-job` | Kontrola | Vytvoří úlohu s `--from-workspace` nebo `--mcp-job-json` |
| `--mcp-run-workspace` | Kontrola | Spustí uložený pracovní prostor, s `--allow-app-target` a `--mcp-control-token` |
| `--remove-empty-organize-layout` | Kontrola | Odstraní prázdné složky rozvržení uvnitř existujícího `--output` |
| `--confirm-destructive` | Kontrola | Nutný s `--mcp-run-workspace` pro běh, který přesouvá nebo maže. Konektor tento přepínač předá jen při `confirm_destructive=true` |

## Nastavení v JSON klienta MCP

| Nastavení | Kdy |
|----------|------|
| `ORGANIZE_FILES_CLI` | Cesta k OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | Cesta k `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | Cesta k `mcp-control.json`, jen když soubor není ve výchozí složce profilu |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | Jen úroveň **Kontrola**, z fragmentu aplikace |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | Úroveň **Kontrola**, pro běhy uloženého pracovního prostoru |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | Volitelné. Stejný token, který hostitel používá pro čtení |

## Nastavení ve Windows

1. **Python 3.10 nebo novější** — spusťte `python -V` v PowerShellu. Pokud Python chybí nebo je starší, nainstalujte Python z [python.org](https://www.python.org/downloads/) a zaškrtněte **Add python.exe to PATH**.
2. **Stáhněte a nainstalujte konektor** — stáhněte github.com/GutRaz/organize-files-docs jako ZIP, rozbalte archiv a spusťte `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1`. Skript vytvoří pro konektor vlastní prostředí Pythonu a vypíše příkaz pro aplikaci AI.
3. **V aplikaci:** **Nastavení MCP…**, zvolte **Monitor** nebo **Kontrola** a pak zkopírujte JSON.
4. **Cesty:** `%LocalAppData%\OrganizeFilesCrossPlatform\` obsahuje úlohy a `mcp-control.json`. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **Test** — spusťte `organize_mcp_status`, pak `organize_server_info`. `cliResolved` musí být true a `mcpLevel` musí odpovídat aplikaci.

## Nastavení v macOS

Stejné kroky s **python3** a `bash mcp/install-organize-files-mcp.sh`. Pokud `python3 -V` ukáže 3.9 nebo vůbec žádný Python, nejprve nainstalujte Python z [python.org](https://www.python.org/downloads/macos/). Cesty: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Nastavení v Linuxu

Stejné kroky s **python3** a `bash mcp/install-organize-files-mcp.sh`. V systémech Debian a Ubuntu nejprve spusťte `sudo apt install python3-venv`. Cesty: `~/.local/share/OrganizeFilesCrossPlatform/`, nebo `$XDG_DATA_HOME`, pokud je nastavená, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Zabezpečení

- MCP běží jako **místní uživatel** operačního systému, se stejnými právy jako příkazový řádek spuštěný ručně.
- **Kontrolní token** a **čtecí token** uchovávejte v tajnosti, jako hesla. Po zapnutí úrovně Kontrola zkopírujte JSON znovu.
- **`organize_run_workspace`** běží v příkazovém řádku, ne přes tlačítko Spustit v aplikaci. Nespouštějte dvě úlohy na stejnou výstupní složku současně.
- Příklady: `mcp/examples/`.

## Běhy, které přesouvají nebo mažou

`--mcp-run-workspace` vyžaduje `--confirm-destructive` pro každý běh, který není zkušebním během, ať přesouvá, maže, nebo archivuje. Bez tohoto přepínače příkazový řádek odpoví `confirm_destructive_required`. Konektor přepínač vynechá, pokud volání nenastaví `confirm_destructive=true`, a to umí jen úroveň Kontrola. Ve výchozím stavu tedy konektor odmítne.

## Jazyky

Odpovědi k nastavení pocházejí ze stejného přeloženého průvodce jako okno Dokumentace a Asistent dokumentace. `organize_capabilities` hlásí režimy běhu a cíle, ne názvy motivů v aplikaci.
