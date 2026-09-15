# KI-Assistent (MCP)

Lizenzierte Teams verbinden **OrganizeFiles.Cli** mit Claude Desktop, **Cursor**, VS Code Copilot oder einem anderen Model-Context-Protocol-Client, unten MCP-Client genannt. Der Connector ist das Python-Paket **organize-files-mcp**. Er ist ein kostenloser Download von github.com/GutRaz/organize-files-docs, im Ordner `mcp/`.

**In der Desktop-App:** Öffnen Sie **MCP-Setup…** unter **Anwendung & Daten** in der Optionsspalte oder im Werkzeugmenü. Wählen Sie **MCP-Zugriff**: **Aus**, **Monitor** oder **Kontrolle**. Kopieren Sie dann das JSON-Snippet. Laden Sie MCP in der KI-App nach jedem Wechsel der Stufe neu, denn **Kontrolle** erzeugt jedes Mal ein neues Token.

**Fragen Sie den Dokumentationsassistenten** „setup mcp“ oder „cum setez mcp“ nach den Schritten für das aktuelle System.

## MCP-Zugriffsstufen, in der App eingestellt

Die Stufen entsprechen drei Arten von Arbeit: **Lesen / Vorschau / Ausführen**.

| Stufe | Art der Arbeit | Was die KI kann |
|-------|--------|-------------------|
| **Aus** | — | Nur `organize_mcp_status`. Keine Diagnose und kein Zugriff auf den Arbeitsbereich. |
| **Monitor** | **Lesen** | Alles aus Aus, dazu schreibgeschützte Diagnose, Verlauf von Läufen und Aufgaben, Sperren, Audit-Prüfungen, **`organize_capabilities`** und **`organize_workspace_snapshot`**. `organize_capabilities` listet die Laufmodi, darunter **`ai`**, die Verschiebebereiche und die Ziele. `organize_workspace_snapshot` zeigt den im Hauptfenster gespeicherten Arbeitsbereich. Keine Vorschau und keine Ausführung. |
| **Kontrolle** | **Vorschau** / **Ausführen** | Alles aus Monitor, dazu **`organize_create_job`**, **`organize_run_workspace`** und **`organize_remove_empty_organize_layout`**. Dafür ist ein **Kontrolltoken** in den MCP-Einstellungen nötig, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **Vorschau** ist `organize_run_workspace`, wenn im gespeicherten Arbeitsbereich **Testlauf** an ist, also wird nichts geschrieben. **Ausführen** ist dasselbe Werkzeug mit Testlauf aus, also werden Dateien verschoben. Der Connector lässt `--confirm-destructive` weg, außer der Aufruf setzt `confirm_destructive=true`, und ohne diese Option lehnt die Befehlszeile mit `confirm_destructive_required` ab. |

Die Steuerdatei ist **`mcp-control.json`**, neben `automation-jobs.json` im Profilordner der App. Das kopierte Snippet nennt sie nicht, denn der Connector findet sie im Standard-Profilordner selbst. Setzen Sie **`ORGANIZE_FILES_MCP_CONTROL_FILE`** nur, wenn die Datei an einem anderen Ort liegt. Bei **Kontrolle** setzt das Snippet auch **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`**.

**Verschieben und Löschen erfordert einen zweiten, menschlichen Schritt.** Der Assistent setzt seine Bestätigung selbst, sodass ein Text, den er liest, ihn zum Bestätigen bewegen könnte. Ein Lauf, der kein Testlauf ist, braucht deshalb zusätzlich ein in **MCP-Setup** geöffnetes Zeitfenster, das sich nach 15 Minuten von selbst schließt. Außerhalb davon kann der Assistent einen Lauf weiterhin vorbereiten und in der Vorschau zeigen, der Lauf selbst wird jedoch abgelehnt. Steuerdatei und Zeitfenster sind beide mit einem Schlüssel dieser Installation signiert. Eine Steuerdatei, die von Hand geändert oder von einem anderen Computer kopiert wurde, gilt als Aus.

## MCP-Werkzeuge nach Stufe

**Immer, auch bei Aus:** `organize_mcp_status`

**Monitor und Kontrolle:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` und `organize_run_raw_cli`, das nur lesende Befehle annimmt.

**Ebenfalls in Monitor und Kontrolle:** `organize_capabilities`, das den Laufmodus **`ai`** für KI- und ML-Dateien listet, und `organize_workspace_snapshot`.

**Nur Kontrolle:** `organize_create_job` aus dem Arbeitsbereich oder aus Aufgaben-JSON, `organize_run_workspace` für eine Vorschau oder einen echten Lauf, je nachdem, was der Testlauf des Arbeitsbereichs sagt, und `organize_remove_empty_organize_layout`, das leere Layoutordner in einer vorhandenen Ausgabe entfernt und den Ausgabeordner selbst nie anlegt.

Befehle, die Dateien verschieben oder löschen, sind über MCP außerhalb der Stufe **Kontrolle** immer gesperrt. Keine andere Einstellung erlaubt sie.

## Befehlszeilenoptionen, die der Connector verwendet

| Option | Stufe | Zweck |
|------|-------|---------|
| `--mcp-control-status` | jede | JSON mit der Stufe, dem Pfad der Steuerdatei und den Kennzeichen für Monitor und Kontrolle |
| `--mcp-capabilities` | ab Monitor | JSON-Liste der Laufmodi, darunter **`ai`**, der Verschiebebereiche und der Ziele |
| `--mcp-workspace-snapshot` | ab Monitor | Der gespeicherte Arbeitsbereich und wie er zu einer Aufgabe wird |
| `--mcp-create-job` | Kontrolle | Eine Aufgabe mit `--from-workspace` oder `--mcp-job-json` anlegen |
| `--mcp-run-workspace` | Kontrolle | Den gespeicherten Arbeitsbereich ausführen, mit `--allow-app-target` und `--mcp-control-token` |
| `--remove-empty-organize-layout` | Kontrolle | Leere Layoutordner in einem vorhandenen `--output` entfernen |
| `--confirm-destructive` | Kontrolle | Nötig mit `--mcp-run-workspace` für einen Lauf, der verschiebt oder löscht. Der Connector übergibt sie nur bei `confirm_destructive=true` |

## Einstellungen im JSON des MCP-Clients

| Einstellung | Wann |
|----------|------|
| `ORGANIZE_FILES_CLI` | Pfad zu OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | Pfad zu `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | Pfad zu `mcp-control.json`, nur wenn die Datei nicht im Standard-Profilordner liegt |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | Nur Stufe **Kontrolle**, aus dem Snippet der App |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | Stufe **Kontrolle**, für Läufe des gespeicherten Arbeitsbereichs |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | Optional. Dasselbe Token, das der Host für Leseoperationen verwendet |

## Windows-Setup

1. **Python 3.10 oder neuer** — führen Sie `python -V` in PowerShell aus. Fehlt Python oder ist es älter, installieren Sie es von [python.org](https://www.python.org/downloads/) und setzen Sie den Haken bei **Add python.exe to PATH**.
2. **Connector herunterladen und installieren** — laden Sie github.com/GutRaz/organize-files-docs als ZIP herunter, entpacken Sie es und führen Sie `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1` aus. Das Skript legt eine eigene Python-Umgebung für den Connector an und gibt den Befehl für die KI-App aus.
3. **In der App:** **MCP-Setup…**, wählen Sie **Monitor** oder **Kontrolle** und kopieren Sie dann das JSON.
4. **Pfade:** `%LocalAppData%\OrganizeFilesCrossPlatform\` enthält die Aufgaben und `mcp-control.json`. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **Test** — führen Sie `organize_mcp_status` aus, dann `organize_server_info`. `cliResolved` muss true sein, und `mcpLevel` muss der App entsprechen.

## macOS-Setup

Dieselben Schritte mit **python3** und `bash mcp/install-organize-files-mcp.sh`. Zeigt `python3 -V` die Version 3.9 oder gar kein Python, installieren Sie zuerst Python von [python.org](https://www.python.org/downloads/macos/). Pfade: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Linux-Setup

Dieselben Schritte mit **python3** und `bash mcp/install-organize-files-mcp.sh`. Unter Debian und Ubuntu führen Sie zuerst `sudo apt install python3-venv` aus. Pfade: `~/.local/share/OrganizeFilesCrossPlatform/`, oder `$XDG_DATA_HOME`, wenn es gesetzt ist, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Sicherheit

- MCP läuft als **lokaler Benutzer** des Betriebssystems, mit denselben Rechten wie die von Hand ausgeführte Befehlszeile.
- Halten Sie das **Kontrolltoken** und das **Lesetoken** geheim, wie Passwörter. Kopieren Sie das JSON erneut, nachdem Sie Kontrolle eingeschaltet haben.
- **`organize_run_workspace`** läuft in der Befehlszeile, nicht über die Schaltfläche Ausführen der App. Führen Sie nicht zwei Aufgaben gleichzeitig auf demselben Ausgabeordner aus.
- Beispiele: `mcp/examples/`.

## Läufe, die verschieben oder löschen

`--mcp-run-workspace` verlangt `--confirm-destructive` für jeden Lauf, der kein Testlauf ist, ob er verschiebt, löscht oder archiviert. Ohne diese Option antwortet die Befehlszeile `confirm_destructive_required`. Der Connector lässt die Option weg, außer der Aufruf setzt `confirm_destructive=true`, und das kann nur die Stufe Kontrolle. Standardmäßig lehnt der Connector also ab.

## Sprachen

Die Antworten zur Einrichtung stammen aus derselben übersetzten Anleitung wie das Fenster Dokumentation und der Dokumentationsassistent. `organize_capabilities` meldet Laufmodi und Ziele, keine Namen von Designs der App.
