# Asystent AI (MCP)

Zespoły z licencją łączą **OrganizeFiles.Cli** z Claude Desktop, **Cursor**, VS Code Copilot lub innym klientem Model Context Protocol, dalej nazywanym klientem MCP. Konektor to pakiet Pythona **organize-files-mcp**. Pakiet można pobrać bezpłatnie z github.com/GutRaz/organize-files-docs, z folderu `mcp/`.

**W aplikacji desktopowej:** otwórz okno **Konfiguracja MCP…** w grupie **Aplikacja i dane** w kolumnie opcji albo z menu narzędzi. Wybierz **Dostęp do MCP**: **Wyłączone**, **Monitor** lub **Kontrola**. Następnie skopiuj fragment JSON. Po każdej zmianie poziomu załaduj ponownie MCP w aplikacji AI, ponieważ **Kontrola** za każdym razem tworzy nowy token.

**Zapytaj asystenta dokumentacji** „setup mcp” lub „cum setez mcp”, aby poznać kroki dla bieżącego systemu.

## Poziomy dostępu do MCP, ustawiane w aplikacji

Poziomy odpowiadają trzem rodzajom pracy: **odczyt / podgląd / wykonanie**.

| Poziom | Rodzaj pracy | Co może AI |
|-------|--------|-------------------|
| **Wyłączone** | — | Tylko `organize_mcp_status`. Bez diagnostyki i bez dostępu do obszaru roboczego. |
| **Monitor** | **Odczyt** | Wszystko z poziomu Wyłączone, a do tego diagnostyka tylko do odczytu, historia przebiegów i zadań, blokady, kontrole audytu, **`organize_capabilities`** i **`organize_workspace_snapshot`**. `organize_capabilities` wymienia tryby przebiegu, w tym **`ai`**, zakresy przenoszenia i cele. `organize_workspace_snapshot` pokazuje obszar roboczy zapisany w oknie głównym. Bez podglądu i bez wykonania. |
| **Kontrola** | **Podgląd** / **Wykonanie** | Wszystko z poziomu Monitor, a do tego **`organize_create_job`**, **`organize_run_workspace`** i **`organize_remove_empty_organize_layout`**. Wymaga **tokenu kontrolnego** w ustawieniach MCP, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **Podgląd** to `organize_run_workspace`, gdy zapisany obszar roboczy ma włączoną opcję **Przebieg próbny**, więc nic nie zostaje zapisane. **Wykonanie** to to samo narzędzie, gdy Przebieg próbny jest wyłączony, więc pliki zostają przeniesione. Konektor pomija `--confirm-destructive`, chyba że wywołanie ustawi `confirm_destructive=true`, a bez tej opcji wiersz poleceń odmawia z `confirm_destructive_required`. |

Plik sterujący to **`mcp-control.json`**, obok `automation-jobs.json` w folderze profilu aplikacji. Skopiowany fragment nie podaje tego pliku, ponieważ konektor sam znajduje plik w domyślnym folderze profilu. Ustaw **`ORGANIZE_FILES_MCP_CONTROL_FILE`** tylko wtedy, gdy plik jest w innym miejscu. Na poziomie **Kontrola** fragment ustawia także **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`**.

**Przenoszenie i usuwanie wymaga drugiego kroku, wykonanego przez człowieka.** Asystent sam ustawia potwierdzenie, więc przeczytany tekst mógłby skłonić asystenta do potwierdzenia. Dlatego przebieg, który nie jest przebiegiem próbnym, wymaga też okna czasowego otwartego w oknie **Konfiguracja MCP**, a to okno czasowe zamyka się samo po 15 minutach. Poza tym oknem czasowym asystent nadal może przygotować przebieg i pokazać podgląd przebiegu, ale sam przebieg zostaje odrzucony. Zarówno plik sterujący, jak i okno czasowe są podpisane kluczem, który ma ta instalacja. Plik sterujący zmieniony ręcznie albo skopiowany z innego komputera liczy się jako poziom Wyłączone.

## Narzędzia MCP według poziomu

**Zawsze, także na poziomie Wyłączone:** `organize_mcp_status`

**Monitor i Kontrola:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` oraz `organize_run_raw_cli`, które przyjmuje wyłącznie polecenia do odczytu.

**Także na poziomach Monitor i Kontrola:** `organize_capabilities`, które wymienia tryb przebiegu **`ai`** dla plików AI i ML, oraz `organize_workspace_snapshot`.

**Tylko Kontrola:** `organize_create_job` z obszaru roboczego lub z JSON zadania, `organize_run_workspace` do podglądu albo prawdziwego przebiegu zgodnie z ustawieniem Przebieg próbny w obszarze roboczym oraz `organize_remove_empty_organize_layout`, które usuwa puste foldery układu w istniejącym wyjściu i nigdy nie tworzy samego folderu wyjściowego.

Polecenia, które przenoszą lub usuwają pliki, są przez MCP zawsze blokowane poza poziomem **Kontrola**. Żadne inne ustawienie na nie nie pozwala.

## Opcje wiersza poleceń używane przez konektor

| Opcja | Poziom | Cel |
|------|-------|---------|
| `--mcp-control-status` | dowolny | JSON z poziomem, ścieżką pliku sterującego i flagami poziomów Monitor i Kontrola |
| `--mcp-capabilities` | Monitor i wyżej | Lista JSON trybów przebiegu, w tym **`ai`**, zakresów przenoszenia i celów |
| `--mcp-workspace-snapshot` | Monitor i wyżej | Zapisany obszar roboczy i sposób, w jaki staje się zadaniem |
| `--mcp-create-job` | Kontrola | Tworzy zadanie z `--from-workspace` lub `--mcp-job-json` |
| `--mcp-run-workspace` | Kontrola | Uruchamia zapisany obszar roboczy, z `--allow-app-target` i `--mcp-control-token` |
| `--remove-empty-organize-layout` | Kontrola | Usuwa puste foldery układu w istniejącym `--output` |
| `--confirm-destructive` | Kontrola | Potrzebna z `--mcp-run-workspace` dla przebiegu, który przenosi lub usuwa. Konektor przekazuje tę opcję tylko przy `confirm_destructive=true` |

## Ustawienia w JSON klienta MCP

| Ustawienie | Kiedy |
|----------|------|
| `ORGANIZE_FILES_CLI` | Ścieżka do OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | Ścieżka do `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | Ścieżka do `mcp-control.json`, tylko gdy plik nie jest w domyślnym folderze profilu |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | Tylko poziom **Kontrola**, z fragmentu aplikacji |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | Poziom **Kontrola**, dla przebiegów zapisanego obszaru roboczego |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | Opcjonalne. Ten sam token, którego host używa do operacji odczytu |

## Konfiguracja w systemie Windows

1. **Python 3.10 lub nowszy** — uruchom `python -V` w PowerShell. Jeśli brakuje Pythona albo jest starszy, zainstaluj Python z [python.org](https://www.python.org/downloads/) i zaznacz **Add python.exe to PATH**.
2. **Pobierz i zainstaluj konektor** — pobierz github.com/GutRaz/organize-files-docs jako ZIP, rozpakuj archiwum i uruchom `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1`. Skrypt tworzy dla konektora osobne środowisko Pythona i wyświetla polecenie dla aplikacji AI.
3. **W aplikacji:** **Konfiguracja MCP…**, wybierz **Monitor** lub **Kontrola**, a następnie skopiuj JSON.
4. **Ścieżki:** `%LocalAppData%\OrganizeFilesCrossPlatform\` zawiera zadania i `mcp-control.json`. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **Test** — uruchom `organize_mcp_status`, a potem `organize_server_info`. `cliResolved` musi mieć wartość true, a `mcpLevel` musi odpowiadać aplikacji.

## Konfiguracja w systemie macOS

Te same kroki z **python3** i `bash mcp/install-organize-files-mcp.sh`. Jeśli `python3 -V` pokazuje 3.9 albo w ogóle nie ma Pythona, najpierw zainstaluj Python z [python.org](https://www.python.org/downloads/macos/). Ścieżki: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Konfiguracja w systemie Linux

Te same kroki z **python3** i `bash mcp/install-organize-files-mcp.sh`. W systemach Debian i Ubuntu najpierw uruchom `sudo apt install python3-venv`. Ścieżki: `~/.local/share/OrganizeFilesCrossPlatform/`, albo `$XDG_DATA_HOME`, jeśli jest ustawiona, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Bezpieczeństwo

- MCP działa jako **użytkownik lokalny** systemu operacyjnego, z tymi samymi uprawnieniami co wiersz poleceń uruchomiony ręcznie.
- Zachowaj w tajemnicy **token kontrolny** i **token odczytu**, tak jak hasła. Skopiuj JSON ponownie po włączeniu poziomu Kontrola.
- **`organize_run_workspace`** działa w wierszu poleceń, a nie przez przycisk Uruchom w aplikacji. Nie uruchamiaj dwóch zadań na tym samym folderze wyjściowym w tym samym czasie.
- Przykłady: `mcp/examples/`.

## Przebiegi, które przenoszą lub usuwają

`--mcp-run-workspace` wymaga `--confirm-destructive` dla każdego przebiegu, który nie jest przebiegiem próbnym, niezależnie od tego, czy przenosi, usuwa, czy archiwizuje. Bez tej opcji wiersz poleceń odpowiada `confirm_destructive_required`. Konektor pomija tę opcję, chyba że wywołanie ustawi `confirm_destructive=true`, a może to zrobić tylko poziom Kontrola. Domyślnie konektor więc odmawia.

## Języki

Odpowiedzi dotyczące konfiguracji pochodzą z tego samego przetłumaczonego przewodnika co okno Dokumentacja i Asystent przewodnika. `organize_capabilities` podaje tryby przebiegu i cele, a nie nazwy motywów w aplikacji.
