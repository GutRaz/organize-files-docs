# KI-assistent (MCP)

Gelisensieerde spanne koppel **OrganizeFiles.Cli** aan Claude Desktop, **Cursor**, VS Code Copilot of 'n ander Model Context Protocol-kliënt, hieronder 'n MCP-kliënt genoem. Die koppelaar is die Python-pakket **organize-files-mcp**. Dit is 'n gratis aflaai van github.com/GutRaz/organize-files-docs, in die vouer `mcp/`.

**In die rekenaartoepassing:** maak **MCP-opstelling …** oop onder **Toepassing en data** in die opsiekolom, of vanuit die gereedskapkieslys. Kies **MCP toegang**: **Af**, **Monitor** of **Beheer**. Kopieer dan die JSON-brokkie. Herlaai MCP in die KI-toepassing ná elke verandering van vlak, want **Beheer** maak elke keer 'n nuwe token.

**Vra die dokumentasie-assistent** “setup mcp” of “cum setez mcp” vir die stappe op die huidige stelsel.

## MCP-toegangsvlakke, ingestel in die toepassing

Die vlakke pas by drie soorte werk: **lees / voorskou / uitvoering**.

| Vlak | Soort werk | Wat die KI kan doen |
|-------|--------|-------------------|
| **Af** | — | Slegs `organize_mcp_status`. Geen diagnostiek en geen toegang tot die werkspasie nie. |
| **Monitor** | **Lees** | Alles van Af, plus leesalleen-diagnostiek, geskiedenis van lopies en take, slotte, ouditkontroles, **`organize_capabilities`** en **`organize_workspace_snapshot`**. `organize_capabilities` lys die lopiemodusse, **`ai`** onder hulle, die skuifbestekke en die teikens. `organize_workspace_snapshot` wys die werkspasie wat in die hoofvenster gestoor is. Geen voorskou en geen uitvoering nie. |
| **Beheer** | **Voorskou** / **Uitvoering** | Alles van Monitor, plus **`organize_create_job`**, **`organize_run_workspace`** en **`organize_remove_empty_organize_layout`**. Dit het 'n **beheertoken** in die MCP-instellings nodig, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **Voorskou** is `organize_run_workspace` wanneer die gestoorde werkspasie **Toetslopie** aan het, so niks word geskryf nie. **Uitvoering** is dieselfde hulpmiddel met Toetslopie af, so lêers word geskuif. Die koppelaar laat `--confirm-destructive` weg tensy die oproep `confirm_destructive=true` stel, en daarsonder weier die opdragreël met `confirm_destructive_required`. |

Die beheerlêer is **`mcp-control.json`**, langs `automation-jobs.json` in die toepassing se profielvouer. Die gekopieerde brokkie noem die lêer nie, want die koppelaar vind die lêer in die verstek-profielvouer. Stel **`ORGANIZE_FILES_MCP_CONTROL_FILE`** slegs wanneer die lêer elders is. By **Beheer** stel die brokkie ook **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`**.

**Skuif en skrap verg 'n tweede, menslike stap.** Die assistent stel self die bevestiging, so teks wat dit lees, kan dit oorreed om te bevestig. 'n Lopie wat nie 'n toetslopie is nie, het daarom ook 'n venster nodig wat in **MCP-opstelling** oopgemaak is, en daardie venster sluit vanself ná 15 minute. Daarbuite kan die assistent steeds 'n lopie voorberei en voorskou, maar die lopie self word geweier. Sowel die beheerlêer as die venster is onderteken met 'n sleutel wat hierdie installasie hou. 'n Beheerlêer wat met die hand verander of van 'n ander rekenaar gekopieer is, tel as Af.

## MCP-hulpmiddels volgens vlak

**Altyd, ook by Af:** `organize_mcp_status`

**Monitor en Beheer:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` en `organize_run_raw_cli`, wat slegs leesalleen-opdragte aanvaar.

**Ook in Monitor en Beheer:** `organize_capabilities`, wat die lopiemodus **`ai`** vir KI- en ML-lêers lys, en `organize_workspace_snapshot`.

**Slegs Beheer:** `organize_create_job` vanuit die werkspasie of vanuit taak-JSON, `organize_run_workspace` vir 'n voorskou of 'n regte lopie soos die werkspasie se Toetslopie aandui, en `organize_remove_empty_organize_layout`, wat leë uitlegvouers binne 'n bestaande afvoer verwyder en nooit die afvoervouer self skep nie.

Opdragte wat lêers skuif of skrap, word buite die vlak **Beheer** altyd deur MCP geblokkeer. Geen ander instelling laat dit toe nie.

## Opdragreël-vlae wat die koppelaar gebruik

| Vlag | Vlak | Doel |
|------|-------|---------|
| `--mcp-control-status` | enige | JSON met die vlak, die pad van die beheerlêer en die vlae vir Monitor en Beheer |
| `--mcp-capabilities` | Monitor en hoër | JSON-lys van lopiemodusse, **`ai`** onder hulle, skuifbestekke en teikens |
| `--mcp-workspace-snapshot` | Monitor en hoër | Die gestoorde werkspasie en hoe dit na 'n taak oorgaan |
| `--mcp-create-job` | Beheer | Skep 'n taak met `--from-workspace` of `--mcp-job-json` |
| `--mcp-run-workspace` | Beheer | Voer die gestoorde werkspasie uit, met `--allow-app-target` en `--mcp-control-token` |
| `--remove-empty-organize-layout` | Beheer | Verwyder leë uitlegvouers binne 'n bestaande `--output` |
| `--confirm-destructive` | Beheer | Nodig saam met `--mcp-run-workspace` vir 'n lopie wat skuif of skrap. Die koppelaar gee dit slegs deur wanneer `confirm_destructive=true` |

## Instellings in die MCP-kliënt se JSON

| Instelling | Wanneer |
|----------|------|
| `ORGANIZE_FILES_CLI` | Pad na OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | Pad na `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | Pad na `mcp-control.json`, slegs wanneer die lêer nie in die verstek-profielvouer is nie |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | Slegs die vlak **Beheer**, uit die toepassing se brokkie |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | Die vlak **Beheer**, vir lopies van die gestoorde werkspasie |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | Opsioneel. Dieselfde token wat die gasheer vir leesbewerkings gebruik |

## Opstelling op Windows

1. **Python 3.10 of nuwer** — voer `python -V` in PowerShell uit. As Python ontbreek of ouer is, installeer Python vanaf [python.org](https://www.python.org/downloads/) en merk **Add python.exe to PATH**.
2. **Laai die koppelaar af en installeer dit** — laai github.com/GutRaz/organize-files-docs as 'n ZIP af, pak dit uit en voer `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1` uit. Die skrip maak 'n private Python-omgewing vir die koppelaar en wys die opdrag vir die KI-toepassing.
3. **In die toepassing:** **MCP-opstelling …**, kies **Monitor** of **Beheer** en kopieer dan die JSON.
4. **Paaie:** `%LocalAppData%\OrganizeFilesCrossPlatform\` bevat die take en `mcp-control.json`. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **Toets** — voer `organize_mcp_status` uit, dan `organize_server_info`. `cliResolved` moet true wees en `mcpLevel` moet by die toepassing pas.

## Opstelling op macOS

Dieselfde stappe met **python3** en `bash mcp/install-organize-files-mcp.sh`. As `python3 -V` 3.9 of glad geen Python wys nie, installeer eers Python vanaf [python.org](https://www.python.org/downloads/macos/). Paaie: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Opstelling op Linux

Dieselfde stappe met **python3** en `bash mcp/install-organize-files-mcp.sh`. Voer op Debian en Ubuntu eers `sudo apt install python3-venv` uit. Paaie: `~/.local/share/OrganizeFilesCrossPlatform/`, of `$XDG_DATA_HOME` wanneer dit gestel is, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Sekuriteit

- MCP loop as **die plaaslike gebruiker** van die bedryfstelsel, met dieselfde regte as die opdragreël wat met die hand uitgevoer word.
- Hou die **beheertoken** en die **leestoken** geheim, soos wagwoorde. Kopieer die JSON weer nadat Beheer aangeskakel is.
- **`organize_run_workspace`** loop in die opdragreël, nie deur die toepassing se knoppie Voer uit nie. Moenie twee take tegelyk op dieselfde afvoervouer laat loop nie.
- Voorbeelde: `mcp/examples/`.

## Lopies wat skuif of skrap

`--mcp-run-workspace` het `--confirm-destructive` nodig vir elke lopie wat nie 'n toetslopie is nie, of dit nou skuif, skrap of argiveer. Daarsonder antwoord die opdragreël `confirm_destructive_required`. Die koppelaar laat die vlag weg tensy die oproep `confirm_destructive=true` stel, en dit kan slegs die vlak Beheer doen. Die koppelaar weier dus by verstek.

## Tale

Die opstellingsantwoorde kom uit dieselfde vertaalde gids as die venster Dokumentasie en die Gids assistent. `organize_capabilities` rapporteer lopiemodusse en teikens, nie name van temas in die toepassing nie.
