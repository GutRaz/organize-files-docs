# AI-assistent (MCP)

Licenserede teams forbinder **OrganizeFiles.Cli** med Claude Desktop, **Cursor**, VS Code Copilot eller en anden Model Context Protocol-klient, herefter kaldet MCP-klient. Connectoren er Python-pakken **organize-files-mcp**. Den kan hentes gratis fra github.com/GutRaz/organize-files-docs, i mappen `mcp/`.

**I skrivebordsappen:** åbn **MCP opsætning...** under **Applikation & data** i indstillingskolonnen eller fra værktøjsmenuen. Vælg **MCP adgang**: **Fra**, **Monitor** eller **Kontrol**. Kopier derefter JSON-kodestykket. Genindlæs MCP i AI-appen efter hver ændring af niveau, fordi **Kontrol** laver et nyt token hver gang.

**Spørg dokumentationsassistenten** »setup mcp« eller »cum setez mcp« om trinene på det aktuelle system.

## MCP-adgangsniveauer, indstillet i appen

Niveauerne svarer til tre slags arbejde: **læsning / forhåndsvisning / udførelse**.

| Niveau | Slags arbejde | Hvad AI kan gøre |
|-------|--------|-------------------|
| **Fra** | — | Kun `organize_mcp_status`. Ingen diagnostik og ingen adgang til arbejdsområdet. |
| **Monitor** | **Læsning** | Alt fra niveauet Fra, plus skrivebeskyttet diagnostik, historik over kørsler og opgaver, låse, revisionstjek, **`organize_capabilities`** og **`organize_workspace_snapshot`**. `organize_capabilities` viser kørselstilstandene, heriblandt **`ai`**, flytteområderne og målene. `organize_workspace_snapshot` viser det arbejdsområde, der er gemt i hovedvinduet. Ingen forhåndsvisning og ingen udførelse. |
| **Kontrol** | **Forhåndsvisning** / **Udførelse** | Alt fra niveauet Monitor, plus **`organize_create_job`**, **`organize_run_workspace`** og **`organize_remove_empty_organize_layout`**. Kræver et **kontroltoken** i MCP-indstillingerne, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **Forhåndsvisning** er `organize_run_workspace`, når det gemte arbejdsområde har **Prøvekørsel** slået til, så intet bliver skrevet. **Udførelse** er det samme værktøj med Prøvekørsel slået fra, så filer bliver flyttet. Connectoren udelader `--confirm-destructive`, medmindre kaldet sætter `confirm_destructive=true`, og uden flaget afviser kommandolinjen med `confirm_destructive_required`. |

Kontrolfilen er **`mcp-control.json`**, ved siden af `automation-jobs.json` i appens profilmappe. Det kopierede kodestykke nævner ikke filen, fordi connectoren finder filen i standardprofilmappen. Sæt kun **`ORGANIZE_FILES_MCP_CONTROL_FILE`**, når filen ligger et andet sted. Ved **Kontrol** sætter kodestykket også **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`**.

**At flytte og slette kræver et andet, menneskeligt trin.** Assistenten sætter selv bekræftelsen, så tekst, som assistenten læser, kunne overtale assistenten til at bekræfte. En kørsel, der ikke er en prøvekørsel, kræver derfor også et vindue åbnet i **MCP opsætning**, og det vindue lukker af sig selv efter 15 minutter. Uden for vinduet kan assistenten stadig forberede og forhåndsvise en kørsel, men selve kørslen bliver afvist. Både kontrolfilen og vinduet er signeret med en nøgle, som denne installation har. En kontrolfil, der er ændret i hånden eller kopieret fra en anden computer, gælder som Fra.

## MCP-værktøjer efter niveau

**Altid, også ved Fra:** `organize_mcp_status`

**Monitor og Kontrol:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` og `organize_run_raw_cli`, som kun accepterer skrivebeskyttede kommandoer.

**Også i Monitor og Kontrol:** `organize_capabilities`, som viser kørselstilstanden **`ai`** for AI- og ML-filer, og `organize_workspace_snapshot`.

**Kun Kontrol:** `organize_create_job` fra arbejdsområdet eller fra opgave-JSON, `organize_run_workspace` til en forhåndsvisning eller en rigtig kørsel, som arbejdsområdets Prøvekørsel angiver, og `organize_remove_empty_organize_layout`, som fjerner tomme layoutmapper i et eksisterende output og aldrig opretter selve outputmappen.

Kommandoer, der flytter eller sletter filer, er altid blokeret via MCP uden for niveauet **Kontrol**. Ingen anden indstilling tillader dem.

## Kommandolinjeflag, som connectoren bruger

| Flag | Niveau | Formål |
|------|-------|---------|
| `--mcp-control-status` | alle | JSON med niveauet, stien til kontrolfilen og flagene for Monitor og Kontrol |
| `--mcp-capabilities` | Monitor og højere | JSON-liste over kørselstilstande, heriblandt **`ai`**, flytteområder og mål |
| `--mcp-workspace-snapshot` | Monitor og højere | Det gemte arbejdsområde, og hvordan det svarer til en opgave |
| `--mcp-create-job` | Kontrol | Opret en opgave med `--from-workspace` eller `--mcp-job-json` |
| `--mcp-run-workspace` | Kontrol | Kør det gemte arbejdsområde med `--allow-app-target` og `--mcp-control-token` |
| `--remove-empty-organize-layout` | Kontrol | Fjern tomme layoutmapper i et eksisterende `--output` |
| `--confirm-destructive` | Kontrol | Nødvendigt med `--mcp-run-workspace` for en kørsel, der flytter eller sletter. Connectoren sender det kun, når `confirm_destructive=true` |

## Indstillinger i MCP-klientens JSON

| Indstilling | Hvornår |
|----------|------|
| `ORGANIZE_FILES_CLI` | Sti til OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | Sti til `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | Sti til `mcp-control.json`, kun når filen ikke ligger i standardprofilmappen |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | Kun niveauet **Kontrol**, fra appens kodestykke |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | Niveauet **Kontrol**, til kørsler af det gemte arbejdsområde |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | Valgfrit. Det samme token, som værten bruger til læsehandlinger |

## Opsætning på Windows

1. **Python 3.10 eller nyere** — kør `python -V` i PowerShell. Hvis Python mangler eller er ældre, så installer Python fra [python.org](https://www.python.org/downloads/), og sæt flueben ved **Add python.exe to PATH**.
2. **Hent og installer connectoren** — hent github.com/GutRaz/organize-files-docs som ZIP, pak filen ud, og kør `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1`. Scriptet laver et privat Python-miljø til connectoren og viser kommandoen til AI-appen.
3. **I appen:** **MCP opsætning...**, vælg **Monitor** eller **Kontrol**, og kopier derefter JSON.
4. **Stier:** `%LocalAppData%\OrganizeFilesCrossPlatform\` rummer opgaverne og `mcp-control.json`. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **Test** — kør `organize_mcp_status` og derefter `organize_server_info`. `cliResolved` skal være true, og `mcpLevel` skal svare til appen.

## Opsætning på macOS

De samme trin med **python3** og `bash mcp/install-organize-files-mcp.sh`. Hvis `python3 -V` viser 3.9 eller slet ingen Python, så installer først Python fra [python.org](https://www.python.org/downloads/macos/). Stier: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Opsætning på Linux

De samme trin med **python3** og `bash mcp/install-organize-files-mcp.sh`. På Debian og Ubuntu skal `sudo apt install python3-venv` køres først. Stier: `~/.local/share/OrganizeFilesCrossPlatform/`, eller `$XDG_DATA_HOME`, når den er sat, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Sikkerhed

- MCP kører som **den lokale bruger** af styresystemet, med de samme rettigheder som kommandolinjen kørt i hånden.
- Hold **kontroltokenet** og **læsetokenet** hemmelige, ligesom adgangskoder. Kopier JSON igen, når Kontrol er slået til.
- **`organize_run_workspace`** kører i kommandolinjen, ikke via appens knap Kør. Kør ikke to opgaver på den samme outputmappe på samme tid.
- Eksempler: `mcp/examples/`.

## Kørsler, der flytter eller sletter

`--mcp-run-workspace` kræver `--confirm-destructive` for hver kørsel, der ikke er en prøvekørsel, uanset om kørslen flytter, sletter eller arkiverer. Uden flaget svarer kommandolinjen `confirm_destructive_required`. Connectoren udelader flaget, medmindre kaldet sætter `confirm_destructive=true`, og det kan kun niveauet Kontrol. Som standard afviser connectoren altså.

## Sprog

Svarene om opsætning kommer fra den samme oversatte vejledning som vinduet Dokumentation og Guide assistent. `organize_capabilities` rapporterer kørselstilstande og mål, ikke navne på temaer i appen.
