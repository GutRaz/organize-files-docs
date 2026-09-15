# Asistent AI (MCP)

Echipele cu licență conectează **OrganizeFiles.Cli** la Claude Desktop, **Cursor**, VS Code Copilot sau alt client Model Context Protocol, numit mai jos client MCP. Conectorul este pachetul Python **organize-files-mcp**. Se descarcă gratuit de la github.com/GutRaz/organize-files-docs, din folderul `mcp/`.

**În aplicația desktop:** deschide **Configurare MCP…** din **Aplicație și date**, în coloana de opțiuni, sau din meniul de unelte. Alege **Acces MCP**: **Oprit**, **Monitor** sau **Control**. Apoi copiază fragmentul JSON. Reîncarcă MCP în aplicația AI după fiecare schimbare de nivel, pentru că **Control** creează de fiecare dată un token nou.

**Întreabă asistentul de documentație** „cum setez mcp” sau „setup mcp” pentru pașii de pe sistemul curent.

## Niveluri de acces MCP, setate în aplicație

Nivelurile corespund celor trei feluri de lucru: **citire / previzualizare / execuție**.

| Nivel | Fel de lucru | Ce poate face AI-ul |
|-------|----------|---------------------|
| **Oprit** | — | Doar `organize_mcp_status`. Fără diagnostic și fără acces la spațiul de lucru. |
| **Monitor** | **Citire** | Tot ce are Oprit, plus diagnostic doar pentru citire, istoricul rulărilor și al joburilor, blocări, verificări de audit, **`organize_capabilities`** și **`organize_workspace_snapshot`**. `organize_capabilities` arată modurile de rulare, printre ele **`ai`**, felurile de mutare și țintele. `organize_workspace_snapshot` arată spațiul de lucru salvat din fereastra principală. Fără previzualizare și fără execuție. |
| **Control** | **Previzualizare** / **Execuție** | Tot ce are Monitor, plus **`organize_create_job`**, **`organize_run_workspace`** și **`organize_remove_empty_organize_layout`**. Are nevoie de un **token de control** în setările MCP, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **Previzualizare** înseamnă `organize_run_workspace` când spațiul de lucru salvat are **Simulare** pornită, deci nu se scrie nimic. **Execuție** înseamnă același instrument cu Simulare oprită, deci fișierele se mută. Conectorul lasă deoparte `--confirm-destructive` dacă apelul nu setează `confirm_destructive=true`, iar fără el linia de comandă refuză cu `confirm_destructive_required`. |

Fișierul de control este **`mcp-control.json`**, lângă `automation-jobs.json`, în folderul de profil al aplicației. Fragmentul copiat nu îl numește, pentru că conectorul îl găsește singur în folderul de profil implicit. Setează **`ORGANIZE_FILES_MCP_CONTROL_FILE`** doar când fișierul este în alt loc. La **Control**, fragmentul setează și **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`**.

**Mutarea și ștergerea cer un al doilea pas, făcut de om.** Asistentul își pune singur confirmarea, deci un text pe care îl citește l-ar putea convinge să confirme. De aceea, o rulare care nu este simulare are nevoie și de o fereastră deschisă din **Configurare MCP**, iar fereastra se închide singură după 15 minute. În afara ei, asistentul poate pregăti și previzualiza o rulare, dar rularea propriu-zisă este refuzată. Atât fișierul de control, cât și fereastra sunt semnate cu o cheie păstrată de această instalare. Un fișier de control schimbat de mână sau copiat de pe alt calculator contează ca Oprit.

## Instrumente MCP pe niveluri

**Mereu, și la Oprit:** `organize_mcp_status`

**Monitor și Control:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` și `organize_run_raw_cli`, care acceptă doar comenzi de citire.

**Tot în Monitor și Control:** `organize_capabilities`, care arată modul de rulare **`ai`** pentru fișiere AI și ML, și `organize_workspace_snapshot`.

**Doar Control:** `organize_create_job` din spațiul de lucru sau din JSON-ul unui job, `organize_run_workspace` pentru previzualizare sau rulare reală, după cum spune Simularea din spațiul de lucru, și `organize_remove_empty_organize_layout`, care șterge folderele goale de așezare dintr-un folder de ieșire existent și nu creează niciodată folderul de ieșire.

Comenzile care mută sau șterg fișiere sunt mereu blocate prin MCP în afara nivelului **Control**. Nicio altă setare nu le permite.

## Opțiunile liniei de comandă folosite de conector

| Opțiune | Nivel | Scop |
|------|-------|------|
| `--mcp-control-status` | orice | JSON cu nivelul, calea fișierului de control și indicatorii Monitor și Control |
| `--mcp-capabilities` | Monitor și peste | Listă JSON cu modurile de rulare, printre ele **`ai`**, felurile de mutare și țintele |
| `--mcp-workspace-snapshot` | Monitor și peste | Spațiul de lucru salvat și cum devine el un job |
| `--mcp-create-job` | Control | Creează un job cu `--from-workspace` sau `--mcp-job-json` |
| `--mcp-run-workspace` | Control | Rulează spațiul de lucru salvat, cu `--allow-app-target` și `--mcp-control-token` |
| `--remove-empty-organize-layout` | Control | Șterge folderele goale de așezare dintr-un `--output` existent |
| `--confirm-destructive` | Control | Necesar cu `--mcp-run-workspace` pentru o rulare care mută sau șterge. Conectorul îl trimite doar când `confirm_destructive=true` |

## Setări în JSON-ul clientului MCP

| Setare | Când |
|-----------|------|
| `ORGANIZE_FILES_CLI` | Calea către OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | Calea către `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | Calea către `mcp-control.json`, doar când nu este în folderul de profil implicit |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | Doar la nivelul **Control**, din fragmentul aplicației |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | Nivelul **Control**, pentru rulările spațiului de lucru salvat |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | Opțional. Același token pe care îl folosește gazda pentru operațiile de citire |

## Windows

1. **Python 3.10 sau mai nou** — rulează `python -V` în PowerShell. Dacă Python lipsește sau e mai vechi, instalează-l de pe [python.org](https://www.python.org/downloads/) și bifează **Add python.exe to PATH**.
2. **Descarcă și instalează conectorul** — descarcă github.com/GutRaz/organize-files-docs ca ZIP, dezarhivează-l și rulează `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1`. Scriptul face un mediu Python separat pentru conector și afișează comanda pentru aplicația AI.
3. **În aplicație:** **Configurare MCP…**, alege **Monitor** sau **Control**, apoi copiază JSON-ul.
4. **Căi:** `%LocalAppData%\OrganizeFilesCrossPlatform\` ține joburile și `mcp-control.json`. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **Test** — rulează `organize_mcp_status`, apoi `organize_server_info`. `cliResolved` trebuie să fie true, iar `mcpLevel` trebuie să fie ca în aplicație.

## macOS

Aceiași pași cu **python3** și `bash mcp/install-organize-files-mcp.sh`. Dacă `python3 -V` arată 3.9 sau deloc Python, instalează mai întâi Python de pe [python.org](https://www.python.org/downloads/macos/). Căi: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Linux

Aceiași pași cu **python3** și `bash mcp/install-organize-files-mcp.sh`. Pe Debian și Ubuntu, rulează mai întâi `sudo apt install python3-venv`. Căi: `~/.local/share/OrganizeFilesCrossPlatform/`, sau `$XDG_DATA_HOME` când este setat, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Securitate

- MCP rulează ca **utilizatorul local** al sistemului de operare, cu aceleași drepturi ca linia de comandă rulată de mână.
- Păstrează secrete **tokenul de control** și **tokenul de citire**, ca pe parole. Copiază din nou JSON-ul după ce pornești Control.
- **`organize_run_workspace`** rulează în linia de comandă, nu prin butonul Rulează din aplicație. Nu rula două joburi pe același folder de ieșire în același timp.
- Exemple: `mcp/examples/`.

## Rulări care mută sau șterg

`--mcp-run-workspace` cere `--confirm-destructive` pentru orice rulare care nu este simulare, fie că mută, șterge sau arhivează. Fără el, linia de comandă răspunde `confirm_destructive_required`. Conectorul lasă deoparte opțiunea dacă apelul nu setează `confirm_destructive=true`, iar asta o poate face doar nivelul Control. Așa că, implicit, conectorul refuză.

## Limbi

Răspunsurile despre configurare vin din același ghid tradus ca fereastra Documentație și fereastra Asistent ghid. `organize_capabilities` arată modurile de rulare și țintele, nu numele temelor din aplicație.
