# AI-assistent (MCP)

Teams met een licentie verbinden **OrganizeFiles.Cli** met Claude Desktop, **Cursor**, VS Code Copilot of een andere Model Context Protocol-client, hieronder MCP-client genoemd. De connector is het Python-pakket **organize-files-mcp**. Het is een gratis download van github.com/GutRaz/organize-files-docs, in de map `mcp/`.

**In de desktop-app:** open **MCP-installatie…** onder **Toepassing & gegevens** in de optiekolom, of vanuit het gereedschapsmenu. Kies **MCP-toegang**: **Uit**, **Monitor** of **Controle**. Kopieer daarna het JSON-fragment. Laad MCP opnieuw in de AI-app na elke wijziging van niveau, want **Controle** maakt elke keer een nieuw token.

**Vraag de documentatieassistent** “setup mcp” of “cum setez mcp” voor de stappen op het huidige systeem.

## MCP-toegangsniveaus, ingesteld in de app

De niveaus passen bij drie soorten werk: **lezen / voorbeeld / uitvoeren**.

| Niveau | Soort werk | Wat de AI kan doen |
|-------|--------|-------------------|
| **Uit** | — | Alleen `organize_mcp_status`. Geen diagnose en geen toegang tot de werkruimte. |
| **Monitor** | **Lezen** | Alles van Uit, plus alleen-lezen-diagnose, geschiedenis van runs en taken, vergrendelingen, auditcontroles, **`organize_capabilities`** en **`organize_workspace_snapshot`**. `organize_capabilities` toont de runmodi, waaronder **`ai`**, de verplaatsingsbereiken en de doelen. `organize_workspace_snapshot` toont de werkruimte die in het hoofdvenster is opgeslagen. Geen voorbeeld en geen uitvoering. |
| **Controle** | **Voorbeeld** / **Uitvoeren** | Alles van Monitor, plus **`organize_create_job`**, **`organize_run_workspace`** en **`organize_remove_empty_organize_layout`**. Hiervoor is een **controletoken** nodig in de MCP-instellingen, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **Voorbeeld** is `organize_run_workspace` wanneer in de opgeslagen werkruimte **Proefrun** aan staat, dus er wordt niets geschreven. **Uitvoeren** is hetzelfde hulpmiddel met Proefrun uit, dus bestanden worden verplaatst. De connector laat `--confirm-destructive` weg tenzij de aanroep `confirm_destructive=true` instelt, en zonder die optie weigert de opdrachtregel met `confirm_destructive_required`. |

Het controlebestand is **`mcp-control.json`**, naast `automation-jobs.json` in de profielmap van de app. Het gekopieerde fragment noemt het bestand niet, omdat de connector het bestand in de standaardprofielmap vindt. Stel **`ORGANIZE_FILES_MCP_CONTROL_FILE`** alleen in wanneer het bestand ergens anders staat. Bij **Controle** stelt het fragment ook **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`** in.

**Verplaatsen en verwijderen vraagt een tweede, menselijke stap.** De assistent zet de bevestiging zelf, dus gelezen tekst kan de assistent overhalen om te bevestigen. Een run die geen proefrun is, heeft daarom ook een venster nodig dat in **MCP-installatie** is geopend, en dat venster sluit na 15 minuten vanzelf. Daarbuiten kan de assistent een run nog voorbereiden en als voorbeeld tonen, maar de run zelf wordt geweigerd. Zowel het controlebestand als het venster zijn ondertekend met een sleutel van deze installatie. Een controlebestand dat met de hand is gewijzigd of van een andere computer is gekopieerd, telt als Uit.

## MCP-hulpmiddelen per niveau

**Altijd, ook bij Uit:** `organize_mcp_status`

**Monitor en Controle:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` en `organize_run_raw_cli`, dat alleen leesopdrachten accepteert.

**Ook in Monitor en Controle:** `organize_capabilities`, dat de runmodus **`ai`** voor AI- en ML-bestanden toont, en `organize_workspace_snapshot`.

**Alleen Controle:** `organize_create_job` vanuit de werkruimte of vanuit taak-JSON, `organize_run_workspace` voor een voorbeeld of een echte run zoals de Proefrun van de werkruimte aangeeft, en `organize_remove_empty_organize_layout`, dat lege indelingsmappen in een bestaande uitvoer verwijdert en de uitvoermap zelf nooit aanmaakt.

Opdrachten die bestanden verplaatsen of verwijderen, zijn via MCP buiten het niveau **Controle** altijd geblokkeerd. Geen enkele andere instelling staat ze toe.

## Opdrachtregelopties die de connector gebruikt

| Optie | Niveau | Doel |
|------|-------|---------|
| `--mcp-control-status` | elk | JSON met het niveau, het pad van het controlebestand en de vlaggen voor Monitor en Controle |
| `--mcp-capabilities` | Monitor en hoger | JSON-lijst van runmodi, waaronder **`ai`**, verplaatsingsbereiken en doelen |
| `--mcp-workspace-snapshot` | Monitor en hoger | De opgeslagen werkruimte en hoe die een taak wordt |
| `--mcp-create-job` | Controle | Een taak maken met `--from-workspace` of `--mcp-job-json` |
| `--mcp-run-workspace` | Controle | De opgeslagen werkruimte uitvoeren, met `--allow-app-target` en `--mcp-control-token` |
| `--remove-empty-organize-layout` | Controle | Lege indelingsmappen in een bestaande `--output` verwijderen |
| `--confirm-destructive` | Controle | Nodig met `--mcp-run-workspace` voor een run die verplaatst of verwijdert. De connector geeft deze optie alleen door bij `confirm_destructive=true` |

## Instellingen in de JSON van de MCP-client

| Instelling | Wanneer |
|----------|------|
| `ORGANIZE_FILES_CLI` | Pad naar OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | Pad naar `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | Pad naar `mcp-control.json`, alleen wanneer het bestand niet in de standaardprofielmap staat |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | Alleen niveau **Controle**, uit het fragment van de app |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | Niveau **Controle**, voor runs van de opgeslagen werkruimte |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | Optioneel. Hetzelfde token dat de host voor leesbewerkingen gebruikt |

## Installatie op Windows

1. **Python 3.10 of nieuwer** — voer `python -V` uit in PowerShell. Als Python ontbreekt of ouder is, installeer Python dan vanaf [python.org](https://www.python.org/downloads/) en vink **Add python.exe to PATH** aan.
2. **Download en installeer de connector** — download github.com/GutRaz/organize-files-docs als ZIP, pak het bestand uit en voer `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1` uit. Het script maakt een eigen Python-omgeving voor de connector en toont de opdracht voor de AI-app.
3. **In de app:** **MCP-installatie…**, kies **Monitor** of **Controle** en kopieer daarna de JSON.
4. **Paden:** `%LocalAppData%\OrganizeFilesCrossPlatform\` bevat de taken en `mcp-control.json`. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **Test** — voer `organize_mcp_status` uit en daarna `organize_server_info`. `cliResolved` moet true zijn en `mcpLevel` moet overeenkomen met de app.

## Installatie op macOS

Dezelfde stappen met **python3** en `bash mcp/install-organize-files-mcp.sh`. Als `python3 -V` 3.9 of helemaal geen Python toont, installeer dan eerst Python vanaf [python.org](https://www.python.org/downloads/macos/). Paden: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Installatie op Linux

Dezelfde stappen met **python3** en `bash mcp/install-organize-files-mcp.sh`. Voer op Debian en Ubuntu eerst `sudo apt install python3-venv` uit. Paden: `~/.local/share/OrganizeFilesCrossPlatform/`, of `$XDG_DATA_HOME` wanneer die is ingesteld, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Beveiliging

- MCP draait als **de lokale gebruiker** van het besturingssysteem, met dezelfde rechten als de opdrachtregel die met de hand wordt uitgevoerd.
- Houd het **controletoken** en het **leestoken** geheim, net als wachtwoorden. Kopieer de JSON opnieuw nadat Controle is ingeschakeld.
- **`organize_run_workspace`** draait in de opdrachtregel, niet via de knop Uitvoeren van de app. Voer niet tegelijk twee taken uit op dezelfde uitvoermap.
- Voorbeelden: `mcp/examples/`.

## Runs die verplaatsen of verwijderen

`--mcp-run-workspace` vereist `--confirm-destructive` voor elke run die geen proefrun is, of die nu verplaatst, verwijdert of archiveert. Zonder die optie antwoordt de opdrachtregel `confirm_destructive_required`. De connector laat de optie weg tenzij de aanroep `confirm_destructive=true` instelt, en dat kan alleen het niveau Controle. Standaard weigert de connector dus.

## Talen

De antwoorden over de installatie komen uit dezelfde vertaalde gids als het venster Documentatie en de Gids assistent. `organize_capabilities` meldt runmodi en doelen, geen namen van thema's in de app.
