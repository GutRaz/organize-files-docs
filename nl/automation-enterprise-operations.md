# Bewaking met Prometheus en Grafana

## Wat de tellers dekken

Geplande taken houden een kleine set Prometheus-tellers en -meters bij. Elke naam begint met `organize_files_automation_`, en de hele set wordt als Prometheus-tekst gepubliceerd. Alle drie de hosts die taken uitvoeren publiceren dezelfde set: de desktoptoepassing, de dienst `OrganizeFiles.JobAgent` en de opdrachtregelhost die in containers draait.

De tellers beschrijven de planner, niet de bestanden. Geteld worden de doorgangen, de afloop van taken, de goedkeuringen, de webhook-bezorging en het onderhoud van de geschiedenis. Over de bestanden die een taak verplaatst wordt niets geteld.

## Export naar een bestand, zonder open poort

`automation-metrics.prom` wordt geschreven in de gegevensmap van de automatisering, naast `automation-jobs.json`, en ververst na elke vervallen doorgang en bij elke uitlezing. De opmaak is die welke de textfile-verzamelaar van `node_exporter` leest, dus een machine waarop `node_exporter` al draait is gedekt zonder luisterende poort, zonder token en zonder firewallregel. Het bestand wordt atomair vervangen, en een symbolische koppeling die op die plek is achtergelaten stopt het schrijven in plaats van gevolgd te worden.

## Uitleespunt

Het uitleespunt bestaat alleen wanneer `ORGANIZE_FILES_METRICS_HTTP_PORT` een poort tussen 1 en 65535 bevat. Zonder die variabele luistert niets.

| Variabele | Gevolg |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | Poort om op te luisteren. Ontbreekt hij of valt hij buiten het bereik, dan is er helemaal geen uitleespunt. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Luisteradres. De standaard is `127.0.0.1`. De waarden `0.0.0.0`, `+` en `*` betekenen elk adres, en al het andere valt terug op `127.0.0.1`. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | Bearer-token dat op `/metrics` en op `/ready` wordt geëist. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` laat `/ready` antwoorden zonder dat token, voor clusterproeven. Hostpaden blijven dan uit het antwoord. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | Door komma's gescheiden afsluitcodes waarbij `/ready` niet gereed meldt. Vervangt de ingebouwde lijst. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` negeert de afsluitcode van de laatste doorgang, en ook de toestand voordat de eerste doorgang klaar is. |
| `ORGANIZE_FILES_READY_JSON` | `1` dwingt het JSON-antwoord op `/ready` af, ook voor een aanroeper die platte tekst vroeg. |

Een adres buiten de lokale lus wordt geweigerd voordat de luisteraar opengaat, tenzij een bearer-token is ingesteld. De weigering wordt naar de foutuitvoer geschreven en als webhook-gebeurtenis verstuurd, want die combinatie zou de tellers aan het hele netwerk geven.

## Bediende paden

- `/metrics` — de tellers als Prometheus-tekst. Een verzoek aan `/` levert dezelfde inhoud.
- `/ready` — gereedheid voor een orkestrator. Het antwoord is `200` zodra de automatiseringsmap een proefschrijfactie aanvaardt, het takenbestand opengaat, de geschiedenismap binnen de gegevenswortel valt en de laatste vervallen doorgang eindigde op een afsluitcode die niet blokkeert. Anders luidt het antwoord `503` met een korte reden zoals `due_pass_not_completed` of `last_due_pass_license_failed`.
- `/health` — alleen levensteken. Dat pad blijft anoniem ook als een token is ingesteld, want het antwoordt `ok` en verder niets.

De afsluitcodes `3` voor een licentiefout, `8` voor een vergrendelde uitvoerboom, `10` voor een nooit bevestigde verwijdering en `11` voor een claimconflict blokkeren de gereedheid standaard. De inhoud van `/ready` is JSON tenzij de aanroeper `Accept: text/plain` stuurt of `?format=text` toevoegt.

## De tellers

| Naam | Inhoud |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Vervallen doorgangen die de planner begon. |
| `organize_files_automation_jobs_started_total` | Taakuitvoeringen die de lopende toestand bereikten. |
| `organize_files_automation_jobs_skipped_total` | Overgeslagen taken: een Docker- of Kubernetes-omgeving die niet gereed is, een taak gericht op de toepassing op een host zonder scherm, een bezette uitvoerwortel, of een taak die de orkestrator weigerde. |
| `organize_files_automation_jobs_failed_total` | Taakuitvoeringen die op een fout eindigden. |
| `organize_files_automation_jobs_awaiting_approval_total` | Echte uitvoeringen die op goedkeuring wachten. |
| `organize_files_automation_execute_approvals_total` | Verleende goedkeuringen voor een echte uitvoering. |
| `organize_files_automation_execute_approvals_expired_total` | Goedkeuringen waarvan de termijn verliep voor gebruik. |
| `organize_files_automation_claim_conflicts_total` | Keren dat een andere host de claim op de uitvoerwortel al had. |
| `organize_files_automation_runs_orphaned_total` | Uitvoeringen die als wees zijn hersteld, achtergelaten door een gestopte host. |
| `organize_files_automation_job_events_total` | Eén teller per gebeurtenis, met de labels `event`, `job_id`, `target` en `jobs_file`. |
| `organize_files_automation_webhook_posts_succeeded_total` | Aanvaarde webhook-bezorgingen. |
| `organize_files_automation_webhook_posts_failed_total` | Geweigerde of onbereikbare webhook-bezorgingen. |
| `organize_files_automation_webhook_dead_letter_depth` | Regels die op dit moment wachten in het bestand met onbestelbare webhooks. |
| `organize_files_automation_log_retention_pruned_total` | Uitvoeringslogboeken die het bewaarbeleid verwijderde. |
| `organize_files_automation_runs_index_compacted_total` | Regels die bij het verdichten uit de uitvoeringsindex vielen. |
| `organize_files_automation_last_due_pass_exit_code` | Afsluitcode van de laatst voltooide doorgang. `0` is een schone doorgang. |
| `organize_files_automation_last_due_pass_completed_utc` | Unix-tijd in seconden van de laatst voltooide doorgang, en `0` voor de eerste. |

## Dashboard en alarmregels

Een kant-en-klaar Grafana-dashboard wordt met de uitrolbestanden gepubliceerd als `grafana-organize-files-automation.json`, onder de titel **OrganizeFiles Automation**. De tien panelen tonen vervallen doorgangen, gestarte en mislukte taken, claimconflicten, taakdoorvoer over een uur, de laatste afsluitcode, de diepte van onbestelbare berichten, webhook-fouten over een dag, taken die op goedkeuring wachten, en taakgebeurtenissen per toestand. Elk paneel noemt zijn gegevensbron via de plaatshouder `${DS_PROMETHEUS}`.

De bijbehorende alarmregels zijn `alerts-organize-files-automation.yaml`, met `prometheus-rule-automation.yaml` als Kubernetes-omhulsel voor `kube-prometheus-stack`. Een laatste afsluitcode die niet nul is waarschuwt na vijf minuten, een licentiefout is na één minuut kritiek, en de overige regels dekken mislukte taken, claimconflicten, webhook-fouten, een stuwmeer van onbestelbare berichten en goedkeuringen die een dag blijven wachten. Beide bestanden worden bij elke bouw gecontroleerd, zodat de namen hierboven gelijk blijven lopen met de tellers.

# Uitvoer van de run en statistieken

## Statusrij

In het gebied **Uitvoer van de run** wordt het volgende weergegeven:

- Huidige status van de app en voortgang van de engine.
- **CPU** en twee **geheugen**-waarden, alleen voor dit proces.
- **GPU**-regels, op Windows: het aandeel van dit proces in elke grafische kaart, niet de hele kaart.

Dezelfde compacte bronnenbalk wordt hergebruikt in secundaire toolvensters, zoals bestandsverkenning, geplande taken en bestandsreparatie.

## Geheugenlabels

- **Privé bytes / commit** — privé virtueel geheugen gereserveerd door het proces.
- **Werkset/geheugen** — intern RAM-geheugen dat momenteel door dit proces wordt vastgehouden. Het kan verschillen van een andere besturingssysteemmonitor omdat elk besturingssysteem en elke desktopomgeving het geheugen anders verwerkt.

## Heartbeat JSON uitvoeren (optioneel)

Schakel **Write run heartbeat JSON** in onder **Geavanceerd / Diagnostiek**. De engine schrijft `Organize.Files.run.json` onder `Output\_OrganizeMediaLogs` (dezelfde map als het standaard Hervattingsbestand).

- **Pad** — atomair bijgewerkt tijdens organisatie- en reparatieruns.
- **Tijdsafstand** – terwijl bronnen worden doorzocht, wordt het bestand herschreven per 10.000 geziene bestanden, per 5.000 treffers en ongeveer elke 15 seconden zolang het doorzoeken loopt, zodat een grote netwerkboom die traag te lijsten is toch laat zien dat de uitvoering leeft. Tijdens validatie, hashing en verplaatsingen wordt het na elke 1.000 bestanden herschreven, hooguit elke 5 seconden. Het schrijven aan het begin en aan het eind gebeurt nog steeds wanneer een uitvoering begint en eindigt.
- **Voortgang** – zolang de bestandsaantallen nog groeien, toont de hoofdvoortgangsbalk de tot nu toe geziene bestanden in plaats van 100%, totdat een fase een bekend totaal heeft.
- **Velden** — `schema`, `mode`, `phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`), `runState` (`active` / `completed` / `failed` / `cancelled`), `utc` (ISO-8601), `dryRun`, `outputRoot`, `validateMedia`, `deepVideoValidate`, `gpuDeviceCount`, `hwaccel`, optioneel `correlationId`, geneste `progress` tellers.
- **Logboek** — het run-uitvoerpaneel drukt het volledige pad af aan het begin en wanneer het bestand aan het einde wordt opgeslagen. Gebruik **Open heartbeat-logboekmap** / **Heartbeat-JSON-bestand weergeven** onder Geavanceerd / Diagnostiek.
- **CLI** — `--heartbeat-json` op OrganizeFiles.Cli. Annuleren en fatale shell-fouten schrijven `cancelled` / `failed` `runState` indien ingeschakeld.
