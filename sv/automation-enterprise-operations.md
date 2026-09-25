# Övervakning med Prometheus och Grafana

## Vad räknarna täcker

Schemalagda jobb för en liten uppsättning Prometheus-räknare och -mätare. Varje namn börjar med `organize_files_automation_`, och hela uppsättningen publiceras som Prometheus-text. Alla tre värdar som kör jobb publicerar samma uppsättning: skrivbordsprogrammet, tjänsten `OrganizeFiles.JobAgent` och kommandoradsvärden som används i containrar.

Räknarna beskriver schemaläggaren, inte filerna. Det som räknas är genomgångar, jobbutfall, godkännanden, webhook-leverans och skötsel av historiken. Ingenting räknas om de filer ett jobb flyttar.

## Export till en fil, utan öppen port

`automation-metrics.prom` skrivs i automatiseringens datamapp intill `automation-jobs.json` och uppdateras efter varje förfallen genomgång och vid varje avläsning. Formatet är det som textfile-samlaren i `node_exporter` läser, så en maskin som redan kör `node_exporter` täcks utan lyssnande port, utan token och utan brandväggsregel. Filen byts ut atomiskt, och en symbolisk länk som lämnats på dess plats stoppar skrivningen i stället för att följas.

## Avläsningspunkt

Avläsningspunkten finns bara när `ORGANIZE_FILES_METRICS_HTTP_PORT` innehåller en port mellan 1 och 65535. Utan den variabeln lyssnar ingenting.

| Variabel | Verkan |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | Porten att lyssna på. Saknas den eller ligger den utanför intervallet finns ingen avläsningspunkt alls. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Lyssningsadress. Standarden är `127.0.0.1`. Värdena `0.0.0.0`, `+` och `*` betyder alla adresser, och allt annat faller tillbaka på `127.0.0.1`. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | Bearer-token som krävs på `/metrics` och på `/ready`. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` låter `/ready` svara utan den token, för klusterprov. Värdens sökvägar utelämnas då ur svaret. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | Kommaseparerade slutkoder som får `/ready` att rapportera icke redo. Ersätter den inbyggda listan. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` bortser från den senaste genomgångens slutkod, och även från läget innan den första genomgången är klar. |
| `ORGANIZE_FILES_READY_JSON` | `1` tvingar fram JSON-svaret på `/ready`, även för en anropare som bad om ren text. |

En adress utanför loopback avvisas innan lyssnaren öppnas om ingen bearer-token är satt. Avvisningen skrivs på felutgången och sänds som webhook-händelse, eftersom den kombinationen skulle lämna räknarna till hela nätet.

## Betjänade sökvägar

- `/metrics` — räknarna som Prometheus-text. En begäran till `/` ger samma innehåll.
- `/ready` — beredskap för en orkestrerare. Svaret är `200` så snart automatiseringsmappen tar emot en provskrivning, jobbfilen går att öppna, historikmappen löses inom datamappen och den senaste förfallna genomgången slutade på en slutkod som inte blockerar. Annars blir svaret `503` med ett kort skäl såsom `due_pass_not_completed` eller `last_due_pass_license_failed`.
- `/health` — endast livstecken. Den sökvägen förblir anonym även när en token är satt, eftersom den svarar `ok` och inget mer.

Slutkoderna `3` för ett licensfel, `8` för ett låst utdataträd, `10` för en radering som aldrig bekräftades och `11` för en anspråkskonflikt blockerar beredskapen som standard. Innehållet på `/ready` är JSON om inte anroparen sänder `Accept: text/plain` eller lägger till `?format=text`.

## Räknarna

| Namn | Innehåll |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Förfallna genomgångar som schemaläggaren påbörjade. |
| `organize_files_automation_jobs_started_total` | Jobbkörningar som nådde det pågående läget. |
| `organize_files_automation_jobs_skipped_total` | Överhoppade jobb: en Docker- eller Kubernetes-miljö som inte är klar, ett jobb riktat mot programmet på en värd utan skärm, en upptagen utdatarot, eller ett jobb som orkestreraren avvisade. |
| `organize_files_automation_jobs_failed_total` | Jobbkörningar som slutade i fel. |
| `organize_files_automation_jobs_awaiting_approval_total` | Riktiga körningar som står och väntar på godkännande. |
| `organize_files_automation_execute_approvals_total` | Godkännanden som getts en riktig körning. |
| `organize_files_automation_execute_approvals_expired_total` | Godkännanden vars frist gick ut före användning. |
| `organize_files_automation_claim_conflicts_total` | Gånger då en annan värd redan höll anspråket på utdataroten. |
| `organize_files_automation_runs_orphaned_total` | Körningar som återfunnits föräldralösa, lämnade av en värd som stannade. |
| `organize_files_automation_job_events_total` | En räknare per händelse, med etiketterna `event`, `job_id`, `target` och `jobs_file`. |
| `organize_files_automation_webhook_posts_succeeded_total` | Mottagna webhook-leveranser. |
| `organize_files_automation_webhook_posts_failed_total` | Avvisade eller onåbara webhook-leveranser. |
| `organize_files_automation_webhook_dead_letter_depth` | Rader som just nu väntar i webhook-filen för ej levererade meddelanden. |
| `organize_files_automation_log_retention_pruned_total` | Körningsloggar som bevarandet tog bort. |
| `organize_files_automation_runs_index_compacted_total` | Rader som togs ur körningsindexet vid komprimering. |
| `organize_files_automation_last_due_pass_exit_code` | Slutkoden för den senast avslutade genomgången. `0` är en ren genomgång. |
| `organize_files_automation_last_due_pass_completed_utc` | Unix-tid i sekunder för den senast avslutade genomgången, och `0` före den första. |

## Instrumentpanel och larmregler

En färdig Grafana-instrumentpanel publiceras med installationsfilerna som `grafana-organize-files-automation.json`, under titeln **OrganizeFiles Automation**. Dess tio rutor visar förfallna genomgångar, startade och misslyckade jobb, anspråkskonflikter, jobbgenomströmning över en timme, den senaste slutkoden, djupet av ej levererade meddelanden, webhook-fel över ett dygn, jobb som väntar på godkännande, och jobbhändelser per läge. Varje ruta namnger sin datakälla genom platshållaren `${DS_PROMETHEUS}`.

De tillhörande larmreglerna är `alerts-organize-files-automation.yaml`, med `prometheus-rule-automation.yaml` som Kubernetes-hölje för `kube-prometheus-stack`. En senaste slutkod skild från noll varnar efter fem minuter, ett licensfel är kritiskt efter en minut, och de övriga reglerna täcker misslyckade jobb, anspråkskonflikter, webhook-fel, en hög av ej levererade meddelanden och godkännanden som väntat ett dygn. Båda filerna kontrolleras vid varje bygge, så namnen ovan håller jämna steg med räknarna.

# Körningens utdata och mätvärden

## Statusrad

Området **Körningens utdata** visar:

- Appens aktuella status och motorns förlopp.
- **CPU** och två **minne**-värden endast för denna process.
- **GPU**-rader, på Windows: den här processens andel av varje grafikkort, inte hela kortet.

Samma kompakta resursfält återanvänds i sekundära verktygsfönster som filutforskning, schemalagda jobb och filreparation.

## Minnesetiketter

- **Privata bytes / commit** — privat virtuellt minne reserverat av processen.
- **Arbetsuppsättning / minne** — inbyggt RAM som för närvarande innehas av denna process. Den kan skilja sig från en annan operativsystemmonitor eftersom varje operativsystem och skrivbordsmiljö märker processminne på olika sätt.

## Kör heartbeat JSON (valfritt)

Aktivera **Write run heartbeat JSON** under **Avancerat / Diagnostik**. Motorn skriver `Organize.Files.run.json` under `Output\_OrganizeMediaLogs` (samma mapp som standardfilen för organisering av resume-fil).

- **Väg** — uppdaterad atomärt under organiserings- och reparationskörningar.
- **Tidsintervall** – medan källor gås igenom skrivs filen om för var 10 000 sedda filer, var 5 000 träffar och ungefär var 15:e sekund så länge genomgången pågår, så ett stort nätverksträd som är långsamt att lista visar ändå att körningen lever. Under validering, hashning och flyttar skrivs den om efter var 1 000 filer, högst var femte sekund. Skrivningarna vid start och slut sker fortfarande när en körning börjar och avslutas.
- **Framsteg** – så länge filantalen ännu växer visar huvudförloppsraden de filer som setts hittills i stället för 100 %, tills ett skede har ett känt totalantal.
- **Fält** — `schema`, `mode`, `phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`), `runState`(`active`/`completed`/`failed`/`cancelled`), `utc` (ISO-8601), `dryRun`, `outputRoot`, `validateMedia`, `deepVideoValidate`, `gpuDeviceCount`, `hwaccel`, valfritt `correlationId`, kapslad `progress` räknare.
- **Logg** — utdatapanelen för körning skriver ut hela sökvägen vid start och när filen sparas i slutet. Använd **Öppna hjärtslagsloggmapp** / **Visa JSON-fil för hjärtslag** under Avancerat / Diagnostik.
- **CLI** — `--heartbeat-json` på OrganizeFiles.Cli. Avbryt och fatala skalfel skriv `cancelled`/`failed` `runState` när den är aktiverad.
