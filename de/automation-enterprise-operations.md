# Überwachung mit Prometheus und Grafana

## Was die Zähler abdecken

Geplante Jobs führen einen kleinen Satz von Prometheus-Zählern und -Messwerten. Jeder Name beginnt mit `organize_files_automation_`, und der gesamte Satz wird als Prometheus-Text veröffentlicht. Alle drei Hosts, die Jobs ausführen, veröffentlichen denselben Satz: die Desktop-Anwendung, der Dienst `OrganizeFiles.JobAgent` und der Kommandozeilen-Host in Containern.

Die Zähler beschreiben den Planer, nicht die Dateien. Gezählt werden Durchläufe, Job-Ergebnisse, Freigaben, Webhook-Zustellung und die Pflege der Historie. Über die Dateien, die ein Job verschiebt, wird nichts gezählt.

## Export in eine Datei, ohne offenen Port

`automation-metrics.prom` wird in den Automatisierungsordner neben `automation-jobs.json` geschrieben und nach jedem fälligen Durchlauf sowie bei jedem Abruf aktualisiert. Das Format liest der Textfile-Collector von `node_exporter`, deshalb ist ein Rechner, auf dem `node_exporter` bereits läuft, ohne lauschenden Port, ohne Token und ohne Firewallregel abgedeckt. Die Datei wird atomar ersetzt, und ein an ihrer Stelle hinterlassener symbolischer Link stoppt das Schreiben, statt ihm zu folgen.

## Abrufendpunkt

Den Endpunkt gibt es nur, wenn `ORGANIZE_FILES_METRICS_HTTP_PORT` einen Port zwischen 1 und 65535 enthält. Ohne diese Variable lauscht nichts.

| Variable | Wirkung |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | Port zum Lauschen. Fehlt er oder liegt er außerhalb des Bereichs, gibt es gar keinen Endpunkt. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Lauschadresse. Voreingestellt ist `127.0.0.1`. Die Werte `0.0.0.0`, `+` und `*` bedeuten alle Adressen, alles andere fällt auf `127.0.0.1` zurück. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | Bearer-Token, das auf `/metrics` und auf `/ready` verlangt wird. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` lässt `/ready` ohne dieses Token antworten, für Cluster-Prüfungen. Hostpfade fehlen dann in der Antwort. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | Durch Komma getrennte Exit-Codes, bei denen `/ready` nicht bereit meldet. Ersetzt die eingebaute Liste. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` ignoriert den Exit-Code des letzten Durchlaufs und ebenso den Zustand, bevor der erste Durchlauf beendet ist. |
| `ORGANIZE_FILES_READY_JSON` | `1` erzwingt die JSON-Antwort auf `/ready`, auch für einen Aufrufer, der reinen Text verlangt hat. |

Eine Adresse außerhalb des Loopbacks wird vor dem Öffnen des Listeners abgelehnt, sofern kein Bearer-Token gesetzt ist. Die Ablehnung wird auf die Fehlerausgabe geschrieben und als Webhook-Ereignis gesendet, denn diese Kombination würde die Zähler dem ganzen Netz überlassen.

## Bediente Pfade

- `/metrics` — die Zähler als Prometheus-Text. Eine Anfrage an `/` liefert denselben Inhalt.
- `/ready` — Bereitschaft für einen Orchestrator. Die Antwort ist `200`, sobald der Automatisierungsordner eine Testschreibung annimmt, die Jobdatei sich öffnen lässt, der Verlaufsordner innerhalb des Datenstamms liegt und der letzte fällige Durchlauf mit einem Exit-Code endete, der nicht blockiert. Sonst lautet die Antwort `503` mit einem kurzen Grund wie `due_pass_not_completed` oder `last_due_pass_license_failed`.
- `/health` — nur Lebenszeichen. Der Pfad bleibt anonym, auch wenn ein Token gesetzt ist, denn er antwortet `ok` und sonst nichts.

Die Exit-Codes `3` für einen Lizenzfehler, `8` für einen gesperrten Zielbaum, `10` für eine nie bestätigte Löschung und `11` für einen Anspruchskonflikt blockieren die Bereitschaft standardmäßig. Der Inhalt von `/ready` ist JSON, sofern der Aufrufer nicht `Accept: text/plain` sendet oder `?format=text` anhängt.

## Die Zähler

| Name | Inhalt |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Vom Planer begonnene fällige Durchläufe. |
| `organize_files_automation_jobs_started_total` | Jobläufe, die den laufenden Zustand erreicht haben. |
| `organize_files_automation_jobs_skipped_total` | Übergangene Jobs: eine nicht bereite Docker- oder Kubernetes-Umgebung, ein Job mit Ziel in der Anwendung auf einem Host ohne Oberfläche, ein belegter Zielordner oder ein vom Orchestrator abgelehnter Job. |
| `organize_files_automation_jobs_failed_total` | Jobläufe, die mit einem Fehler endeten. |
| `organize_files_automation_jobs_awaiting_approval_total` | Echte Läufe, die auf Freigabe warten. |
| `organize_files_automation_execute_approvals_total` | Erteilte Freigaben für einen echten Lauf. |
| `organize_files_automation_execute_approvals_expired_total` | Freigaben, deren Frist vor der Nutzung ablief. |
| `organize_files_automation_claim_conflicts_total` | Fälle, in denen ein anderer Host den Anspruch auf den Zielordner bereits hielt. |
| `organize_files_automation_runs_orphaned_total` | Als verwaist wiederhergestellte Läufe, von einem gestoppten Host hinterlassen. |
| `organize_files_automation_job_events_total` | Ein Zähler je Ereignis, mit den Kennzeichen `event`, `job_id`, `target` und `jobs_file`. |
| `organize_files_automation_webhook_posts_succeeded_total` | Angenommene Webhook-Zustellungen. |
| `organize_files_automation_webhook_posts_failed_total` | Abgelehnte oder nicht erreichbare Webhook-Zustellungen. |
| `organize_files_automation_webhook_dead_letter_depth` | Zeilen, die gerade in der Webhook-Datei für unzustellbare Meldungen warten. |
| `organize_files_automation_log_retention_pruned_total` | Von der Aufbewahrung entfernte Laufprotokolle. |
| `organize_files_automation_runs_index_compacted_total` | Beim Verdichten aus dem Laufindex entfernte Zeilen. |
| `organize_files_automation_last_due_pass_exit_code` | Exit-Code des zuletzt beendeten Durchlaufs. `0` ist ein sauberer Durchlauf. |
| `organize_files_automation_last_due_pass_completed_utc` | Unix-Zeit in Sekunden des zuletzt beendeten Durchlaufs, und `0` vor dem ersten. |

## Dashboard und Alarmregeln

Ein fertiges Grafana-Dashboard wird mit den Installationsdateien als `grafana-organize-files-automation.json` veröffentlicht, unter dem Titel **OrganizeFiles Automation**. Seine zehn Tafeln zeigen fällige Durchläufe, gestartete und fehlgeschlagene Jobs, Anspruchskonflikte, den Jobdurchsatz über eine Stunde, den letzten Exit-Code, die Tiefe der unzustellbaren Meldungen, Webhook-Fehler über einen Tag, Jobs, die auf Freigabe warten, und Job-Ereignisse nach Zustand. Jede Tafel benennt ihre Datenquelle über den Platzhalter `${DS_PROMETHEUS}`.

Die passenden Alarmregeln sind `alerts-organize-files-automation.yaml`, mit `prometheus-rule-automation.yaml` als Kubernetes-Hülle für `kube-prometheus-stack`. Ein letzter Exit-Code ungleich null warnt nach fünf Minuten, ein Lizenzfehler ist nach einer Minute kritisch, und die übrigen Regeln decken fehlgeschlagene Jobs, Anspruchskonflikte, Webhook-Fehler, einen Rückstau unzustellbarer Meldungen und einen Tag lang wartende Freigaben ab. Beide Dateien werden bei jedem Build geprüft, damit die Namen oben zu den Zählern passen.

# Ausgabe des Laufs und Metriken

## Statuszeile

Der Bereich **Ausgabe des Laufs** zeigt:

- Aktueller App-Status und Fortschritt der Engine.
- **CPU** und zwei **Speicherwerte** nur für diesen Prozess.
- **GPU**-Zeilen, unter Windows: der Anteil dieses Prozesses an jeder Grafikkarte, nicht die gesamte Karte.

Die gleiche kompakte Ressourcenleiste wird in sekundären Toolfenstern wie der Dateidurchsuchung, geplanten Jobs und der Dateireparatur wiederverwendet.

## Speicheretiketten

- **Private Bytes / Commit** – privater virtueller Speicher, der vom Prozess reserviert wird.
- **Arbeitssatz/Speicher** – residenter RAM, der derzeit von diesem Prozess belegt wird. Er kann sich von einem anderen Betriebssystemmonitor unterscheiden, da jedes Betriebssystem und jede Desktop-Umgebung den Prozessspeicher anders beschriftet.

## Heartbeat JSON ausführen (optional)

Aktivieren Sie **Run Heartbeat JSON schreiben** unter **Erweitert/Diagnose**. Die Engine schreibt `Organize.Files.run.json` unter `Output\_OrganizeMediaLogs` (derselbe Ordner wie die Standard-Fortsetzungsdateiorganisationsdatei).

- **Pfad** – wird während der Organisations- und Reparaturläufe atomar aktualisiert.
- **Zeitabstände** – während des Durchsuchens der Quellen wird die Datei nach je 10.000 gesehenen Dateien, je 5.000 Treffern und etwa alle 15 Sekunden neu geschrieben, solange die Suche läuft. Ein großer Netzwerkbaum, der sich nur langsam auflisten lässt, zeigt so trotzdem, dass der Lauf lebt. Bei Prüfung, Hashing und Verschiebungen wird sie nach je 1.000 Dateien neu geschrieben, höchstens alle 5 Sekunden. Das Schreiben zu Beginn und am Ende erfolgt weiterhin, wenn ein Lauf anfängt und endet.
- **Fortschritt** – solange die Dateizahlen noch wachsen, zeigt der Hauptfortschrittsbalken die bisher gesehenen Dateien statt 100 %, bis eine Phase eine bekannte Gesamtzahl hat.
- **Felder** — `schema`, `mode`, `phase` (z. B. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`), `runState` (`active` / `completed` / `failed` / `cancelled`), `utc` (ISO-8601), `dryRun`, `outputRoot`, `validateMedia`, `deepVideoValidate`, `gpuDeviceCount`, `hwaccel`, optional `correlationId`, verschachtelte `progress`-Zähler.
- **Protokoll** – Das Ausführungsausgabefeld druckt den vollständigen Pfad beim Start und beim Speichern der Datei am Ende. Verwenden Sie **Heartbeat-Protokollordner öffnen** / **Heartbeat-JSON-Datei anzeigen** unter Erweitert / Diagnose.
- **CLI** – `--heartbeat-json` auf OrganizeFiles.Cli. Abbrechen und schwerwiegende Shell-Fehler schreiben `cancelled` / `failed` `runState`, wenn aktiviert.
