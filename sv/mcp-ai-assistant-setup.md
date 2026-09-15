# AI-assistent (MCP)

Licensierade team ansluter **OrganizeFiles.Cli** till Claude Desktop, **Cursor**, VS Code Copilot eller en annan Model Context Protocol-klient, nedan kallad MCP-klient. Kopplingen är Python-paketet **organize-files-mcp**. Paketet kan laddas ner gratis från github.com/GutRaz/organize-files-docs, i mappen `mcp/`.

**I skrivbordsappen:** öppna **MCP-inställningar...** under **Applikation & data** i alternativkolumnen, eller från verktygsmenyn. Välj **MCP-åtkomst**: **Av**, **Monitor** eller **Kontroll**. Kopiera sedan JSON-kodavsnittet. Ladda om MCP i AI-appen efter varje byte av nivå, eftersom **Kontroll** skapar en ny token varje gång.

**Fråga dokumentationsassistenten** ”setup mcp” eller ”cum setez mcp” om stegen på det aktuella systemet.

## MCP-åtkomstnivåer, inställda i appen

Nivåerna motsvarar tre sorters arbete: **läsning / förhandsgranskning / körning**.

| Nivå | Sorts arbete | Vad AI kan göra |
|-------|--------|-------------------|
| **Av** | — | Endast `organize_mcp_status`. Ingen diagnostik och ingen åtkomst till arbetsytan. |
| **Monitor** | **Läsning** | Allt från nivån Av, plus skrivskyddad diagnostik, historik över körningar och jobb, låsningar, granskningskontroller, **`organize_capabilities`** och **`organize_workspace_snapshot`**. `organize_capabilities` listar körlägena, bland dem **`ai`**, flyttomfången och målen. `organize_workspace_snapshot` visar arbetsytan som är sparad i huvudfönstret. Ingen förhandsgranskning och ingen körning. |
| **Kontroll** | **Förhandsgranskning** / **Körning** | Allt från nivån Monitor, plus **`organize_create_job`**, **`organize_run_workspace`** och **`organize_remove_empty_organize_layout`**. Kräver en **kontrolltoken** i MCP-inställningarna, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **Förhandsgranskning** är `organize_run_workspace` när den sparade arbetsytan har **Testkörning** på, så inget skrivs. **Körning** är samma verktyg med Testkörning av, så filer flyttas. Kopplingen utelämnar `--confirm-destructive` om inte anropet sätter `confirm_destructive=true`, och utan den flaggan vägrar kommandoraden med `confirm_destructive_required`. |

Kontrollfilen är **`mcp-control.json`**, bredvid `automation-jobs.json` i appens profilmapp. Det kopierade kodavsnittet nämner inte filen, eftersom kopplingen hittar filen i standardprofilmappen. Ange **`ORGANIZE_FILES_MCP_CONTROL_FILE`** bara när filen ligger någon annanstans. Vid **Kontroll** sätter kodavsnittet också **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`**.

**Att flytta och ta bort kräver ett andra, mänskligt steg.** Assistenten sätter själv bekräftelsen, så text som den läser skulle kunna övertala den att bekräfta. En körning som inte är en testkörning kräver därför också ett fönster som har öppnats i **MCP-inställningar**, och det fönstret stängs av sig självt efter 15 minuter. Utanför fönstret kan assistenten fortfarande förbereda och förhandsgranska en körning, men själva körningen nekas. Både kontrollfilen och fönstret är signerade med en nyckel som den här installationen har. En kontrollfil som har ändrats för hand eller kopierats från en annan dator räknas som Av.

## MCP-verktyg efter nivå

**Alltid, även vid Av:** `organize_mcp_status`

**Monitor och Kontroll:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` och `organize_run_raw_cli`, som bara tar emot skrivskyddade kommandon.

**Även i Monitor och Kontroll:** `organize_capabilities`, som listar körläget **`ai`** för AI- och ML-filer, och `organize_workspace_snapshot`.

**Endast Kontroll:** `organize_create_job` från arbetsytan eller från jobb-JSON, `organize_run_workspace` för en förhandsgranskning eller en riktig körning enligt arbetsytans Testkörning, och `organize_remove_empty_organize_layout`, som tar bort tomma layoutmappar i en befintlig utdata och aldrig skapar själva utdatamappen.

Kommandon som flyttar eller tar bort filer är alltid blockerade via MCP utanför nivån **Kontroll**. Ingen annan inställning tillåter dem.

## Kommandoradsflaggor som kopplingen använder

| Flagga | Nivå | Syfte |
|------|-------|---------|
| `--mcp-control-status` | alla | JSON med nivån, sökvägen till kontrollfilen och flaggorna för Monitor och Kontroll |
| `--mcp-capabilities` | Monitor och högre | JSON-lista över körlägen, bland dem **`ai`**, flyttomfång och mål |
| `--mcp-workspace-snapshot` | Monitor och högre | Den sparade arbetsytan och hur den blir ett jobb |
| `--mcp-create-job` | Kontroll | Skapa ett jobb med `--from-workspace` eller `--mcp-job-json` |
| `--mcp-run-workspace` | Kontroll | Kör den sparade arbetsytan, med `--allow-app-target` och `--mcp-control-token` |
| `--remove-empty-organize-layout` | Kontroll | Ta bort tomma layoutmappar i en befintlig `--output` |
| `--confirm-destructive` | Kontroll | Krävs med `--mcp-run-workspace` för en körning som flyttar eller tar bort. Kopplingen skickar den bara när `confirm_destructive=true` |

## Inställningar i MCP-klientens JSON

| Inställning | När |
|----------|------|
| `ORGANIZE_FILES_CLI` | Sökväg till OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | Sökväg till `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | Sökväg till `mcp-control.json`, bara när filen inte ligger i standardprofilmappen |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | Endast nivån **Kontroll**, från appens kodavsnitt |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | Nivån **Kontroll**, för körningar av den sparade arbetsytan |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | Valfritt. Samma token som värden använder för läsåtgärder |

## Installation på Windows

1. **Python 3.10 eller nyare** — kör `python -V` i PowerShell. Om Python saknas eller är äldre, installera Python från [python.org](https://www.python.org/downloads/) och markera **Add python.exe to PATH**.
2. **Ladda ner och installera kopplingen** — ladda ner github.com/GutRaz/organize-files-docs som ZIP, packa upp filen och kör `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1`. Skriptet skapar en egen Python-miljö för kopplingen och skriver ut kommandot för AI-appen.
3. **I appen:** **MCP-inställningar...**, välj **Monitor** eller **Kontroll** och kopiera sedan JSON.
4. **Sökvägar:** `%LocalAppData%\OrganizeFilesCrossPlatform\` innehåller jobben och `mcp-control.json`. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **Test** — kör `organize_mcp_status` och sedan `organize_server_info`. `cliResolved` måste vara true och `mcpLevel` måste stämma med appen.

## Installation på macOS

Samma steg med **python3** och `bash mcp/install-organize-files-mcp.sh`. Om `python3 -V` visar 3.9 eller ingen Python alls, installera först Python från [python.org](https://www.python.org/downloads/macos/). Sökvägar: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Installation på Linux

Samma steg med **python3** och `bash mcp/install-organize-files-mcp.sh`. På Debian och Ubuntu, kör först `sudo apt install python3-venv`. Sökvägar: `~/.local/share/OrganizeFilesCrossPlatform/`, eller `$XDG_DATA_HOME` när den är satt, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Säkerhet

- MCP körs som **den lokala användaren** i operativsystemet, med samma rättigheter som kommandoraden körd för hand.
- Håll **kontrolltoken** och **lästoken** hemliga, som lösenord. Kopiera JSON igen efter att Kontroll har slagits på.
- **`organize_run_workspace`** körs i kommandoraden, inte via appens knapp Kör. Kör inte två jobb mot samma utdatamapp samtidigt.
- Exempel: `mcp/examples/`.

## Körningar som flyttar eller tar bort

`--mcp-run-workspace` kräver `--confirm-destructive` för varje körning som inte är en testkörning, oavsett om den flyttar, tar bort eller arkiverar. Utan flaggan svarar kommandoraden `confirm_destructive_required`. Kopplingen utelämnar flaggan om inte anropet sätter `confirm_destructive=true`, och det kan bara nivån Kontroll göra. Som standard vägrar kopplingen alltså.

## Språk

Svaren om installationen kommer från samma översatta guide som fönstret Dokumentation och Guideassistent. `organize_capabilities` rapporterar körlägen och mål, inte namn på teman i appen.
