# AI asszisztens (MCP)

Az engedéllyel rendelkező csapatok az **OrganizeFiles.Cli** programot a Claude Desktop, a **Cursor**, a VS Code Copilot vagy egy másik Model Context Protocol-kliens alkalmazáshoz kapcsolják, amelyet alább MCP-kliensnek nevezünk. Az összekötő az **organize-files-mcp** Python-csomag. Ingyenesen letölthető a github.com/GutRaz/organize-files-docs oldalról, annak `mcp/` mappájából.

**Az asztali alkalmazásban:** nyissa meg az **MCP beállítás…** ablakot az **Alkalmazás és adatok** csoportban a beállítások oszlopában, vagy az eszközök menüből. Válassza ki az **MCP hozzáférés** szintjét: **Ki**, **Monitor** vagy **Vezérlés**. Ezután másolja ki a JSON-kódrészletet. Minden szintváltás után töltse be újra az MCP-t az AI-alkalmazásban, mert a **Vezérlés** minden alkalommal új tokent készít.

**Kérdezze meg a dokumentációs asszisztenst**: „setup mcp” vagy „cum setez mcp”, és megkapja az aktuális rendszer lépéseit.

## MCP hozzáférési szintek, az alkalmazásban beállítva

A szintek háromféle munkának felelnek meg: **olvasás / előnézet / végrehajtás**.

| Szint | Munka fajtája | Mit tehet az AI |
|-------|--------|-------------------|
| **Ki** | — | Csak `organize_mcp_status`. Nincs diagnosztika és nincs hozzáférés a munkaterülethez. |
| **Monitor** | **Olvasás** | Minden, ami a Ki szinten, továbbá csak olvasható diagnosztika, futtatások és feladatok előzményei, zárolások, auditellenőrzések, **`organize_capabilities`** és **`organize_workspace_snapshot`**. Az `organize_capabilities` felsorolja a futtatási módokat, köztük az **`ai`** módot, az áthelyezési hatóköröket és a célokat. Az `organize_workspace_snapshot` megmutatja a főablakban mentett munkaterületet. Nincs előnézet és nincs végrehajtás. |
| **Vezérlés** | **Előnézet** / **Végrehajtás** | Minden, ami a Monitor szinten, továbbá **`organize_create_job`**, **`organize_run_workspace`** és **`organize_remove_empty_organize_layout`**. Ehhez **vezérlő token** kell az MCP-beállításokban, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. Az **Előnézet** az `organize_run_workspace`, amikor a mentett munkaterületen be van kapcsolva a **Próbafuttatás**, így semmi sem íródik. A **Végrehajtás** ugyanez az eszköz kikapcsolt Próbafuttatás mellett, így a fájlok áthelyeződnek. Az összekötő kihagyja a `--confirm-destructive` kapcsolót, hacsak a hívás nem állítja be a `confirm_destructive=true` értéket, és enélkül a parancssor ezzel utasítja el a kérést: `confirm_destructive_required`. |

A vezérlőfájl a **`mcp-control.json`**, az `automation-jobs.json` mellett, az alkalmazás profilmappájában. A kimásolt kódrészlet nem nevezi meg a fájlt, mert az összekötő megtalálja az alapértelmezett profilmappában. Az **`ORGANIZE_FILES_MCP_CONTROL_FILE`** értéket csak akkor állítsa be, ha a fájl máshol van. **Vezérlés** szinten a kódrészlet az **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`** értéket is beállítja.

**Az áthelyezés és a törlés második, emberi lépést kíván.** Az asszisztens maga állítja be a megerősítést, így egy általa olvasott szöveg rábeszélhetné a megerősítésre. Ezért egy olyan futtatáshoz, amely nem próbafuttatás, az **MCP beállítás** ablakban megnyitott időablak is kell, és ez az időablak 15 perc után magától bezárul. Ezen kívül az asszisztens továbbra is előkészíthet egy futtatást és megmutathatja az előnézetét, de magát a futtatást a program elutasítja. A vezérlőfájlt és az időablakot is egy olyan kulcs írja alá, amely ennél a telepítésnél van. A kézzel módosított vagy másik számítógépről másolt vezérlőfájl Ki szintnek számít.

## MCP-eszközök szintenként

**Mindig, a Ki szinten is:** `organize_mcp_status`

**Monitor és Vezérlés:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` és `organize_run_raw_cli`, amely csak olvasó parancsokat fogad el.

**Szintén Monitor és Vezérlés szinten:** `organize_capabilities`, amely felsorolja az **`ai`** futtatási módot az AI- és ML-fájlokhoz, és `organize_workspace_snapshot`.

**Csak Vezérlés:** `organize_create_job` a munkaterületből vagy feladat-JSON-ból, `organize_run_workspace` előnézethez vagy valódi futtatáshoz, ahogy a munkaterület Próbafuttatás beállítása mondja, és `organize_remove_empty_organize_layout`, amely egy meglévő kimeneten belül eltávolítja az üres elrendezésmappákat, és magát a kimeneti mappát soha nem hozza létre.

A fájlokat áthelyező vagy törlő parancsok a **Vezérlés** szinten kívül mindig tiltva vannak az MCP-n keresztül. Semmilyen más beállítás nem engedi ezeket.

## Parancssori kapcsolók, amelyeket az összekötő használ

| Kapcsoló | Szint | Cél |
|------|-------|---------|
| `--mcp-control-status` | bármelyik | JSON a szinttel, a vezérlőfájl elérési útjával és a Monitor és Vezérlés jelzőivel |
| `--mcp-capabilities` | Monitor és felette | JSON-lista a futtatási módokról, köztük az **`ai`** módról, az áthelyezési hatókörökről és a célokról |
| `--mcp-workspace-snapshot` | Monitor és felette | A mentett munkaterület, és hogyan lesz belőle feladat |
| `--mcp-create-job` | Vezérlés | Feladat létrehozása a `--from-workspace` vagy a `--mcp-job-json` kapcsolóval |
| `--mcp-run-workspace` | Vezérlés | A mentett munkaterület futtatása a `--allow-app-target` és a `--mcp-control-token` kapcsolóval |
| `--remove-empty-organize-layout` | Vezérlés | Üres elrendezésmappák eltávolítása egy meglévő `--output` mappán belül |
| `--confirm-destructive` | Vezérlés | A `--mcp-run-workspace` mellett kell az olyan futtatáshoz, amely áthelyez vagy töröl. Az összekötő csak akkor adja át, ha `confirm_destructive=true` |

## Beállítások az MCP-kliens JSON-jában

| Beállítás | Mikor |
|----------|------|
| `ORGANIZE_FILES_CLI` | Az OrganizeFiles.Cli elérési útja |
| `ORGANIZE_FILES_JOBS_FILE` | Az `automation-jobs.json` elérési útja |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | Az `mcp-control.json` elérési útja, csak ha a fájl nincs az alapértelmezett profilmappában |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | Csak **Vezérlés** szinten, az alkalmazás kódrészletéből |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | **Vezérlés** szinten, a mentett munkaterület futtatásaihoz |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | Nem kötelező. Ugyanaz a token, amelyet a gazdagép az olvasási műveletekhez használ |

## Beállítás Windows rendszeren

1. **Python 3.10 vagy újabb** — futtassa a `python -V` parancsot a PowerShellben. Ha a Python hiányzik vagy régebbi, telepítse a [python.org](https://www.python.org/downloads/) oldalról, és jelölje be az **Add python.exe to PATH** lehetőséget.
2. **Az összekötő letöltése és telepítése** — töltse le a github.com/GutRaz/organize-files-docs tartalmát ZIP-fájlként, csomagolja ki, és futtassa az `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1` szkriptet. A szkript külön Python-környezetet hoz létre az összekötőnek, és kiírja az AI-alkalmazáshoz szükséges parancsot.
3. **Az alkalmazásban:** **MCP beállítás…**, válassza a **Monitor** vagy a **Vezérlés** szintet, majd másolja ki a JSON-t.
4. **Elérési utak:** a `%LocalAppData%\OrganizeFilesCrossPlatform\` mappa tartalmazza a feladatokat és az `mcp-control.json` fájlt. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **Teszt** — futtassa az `organize_mcp_status`, majd az `organize_server_info` eszközt. A `cliResolved` értékének true kell lennie, és az `mcpLevel` értékének egyeznie kell az alkalmazással.

## Beállítás macOS rendszeren

Ugyanezek a lépések a **python3** és a `bash mcp/install-organize-files-mcp.sh` használatával. Ha a `python3 -V` 3.9-et mutat, vagy egyáltalán nem mutat Pythont, először telepítse a Pythont a [python.org](https://www.python.org/downloads/macos/) oldalról. Elérési utak: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Beállítás Linux rendszeren

Ugyanezek a lépések a **python3** és a `bash mcp/install-organize-files-mcp.sh` használatával. Debian és Ubuntu rendszeren először futtassa a `sudo apt install python3-venv` parancsot. Elérési utak: `~/.local/share/OrganizeFilesCrossPlatform/`, vagy `$XDG_DATA_HOME`, ha be van állítva, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Biztonság

- Az MCP az operációs rendszer **helyi felhasználójaként** fut, ugyanazokkal a jogokkal, mint a kézzel futtatott parancssor.
- Tartsa titokban a **vezérlő tokent** és az **olvasási tokent**, mint a jelszavakat. A Vezérlés bekapcsolása után másolja ki újra a JSON-t.
- Az **`organize_run_workspace`** a parancssorban fut, nem az alkalmazás Futtatás gombján keresztül. Ne futtasson két feladatot egyszerre ugyanarra a kimeneti mappára.
- Példák: `mcp/examples/`.

## Áthelyező vagy törlő futtatások

A `--mcp-run-workspace` minden olyan futtatáshoz megköveteli a `--confirm-destructive` kapcsolót, amely nem próbafuttatás, akár áthelyez, akár töröl, akár archivál. Enélkül a parancssor ezt válaszolja: `confirm_destructive_required`. Az összekötő kihagyja a kapcsolót, hacsak a hívás nem állítja be a `confirm_destructive=true` értéket, és erre csak a Vezérlés szint képes. Alapértelmezés szerint tehát az összekötő elutasítja a futtatást.

## Nyelvek

A beállítási válaszok ugyanabból a lefordított útmutatóból származnak, mint a Dokumentáció ablak és az Útmutató asszisztens. Az `organize_capabilities` futtatási módokat és célokat jelent, nem az alkalmazás témáinak nevét.
