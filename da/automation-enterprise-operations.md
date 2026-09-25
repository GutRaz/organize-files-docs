# Overvågning med Prometheus og Grafana

## Hvad tællerne dækker

Planlagte job fører et lille sæt Prometheus-tællere og -målere. Hvert navn begynder med `organize_files_automation_`, og hele sættet udgives som Prometheus-tekst. Alle tre værter, der kører job, udgiver det samme sæt: skrivebordsprogrammet, tjenesten `OrganizeFiles.JobAgent` og kommandolinjeværten, der bruges inde i containere.

Tællerne beskriver planlæggeren, ikke filerne. Der tælles gennemløb, jobudfald, godkendelser, webhook-levering og oprydning i historikken. Der tælles intet om de filer, et job flytter.

## Eksport til en fil, uden åben port

`automation-metrics.prom` skrives i automatiseringens datamappe ved siden af `automation-jobs.json` og opdateres efter hvert forfaldent gennemløb og ved hver aflæsning. Formatet er det, som textfile-samleren i `node_exporter` læser, så en maskine, der allerede kører `node_exporter`, er dækket uden lyttende port, uden token og uden firewallregel. Filen udskiftes atomisk, og et symbolsk link efterladt på dens plads standser skrivningen i stedet for at blive fulgt.

## Aflæsningspunkt

Aflæsningspunktet findes kun, når `ORGANIZE_FILES_METRICS_HTTP_PORT` indeholder en port mellem 1 og 65535. Uden den variabel lytter intet.

| Variabel | Virkning |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | Porten der lyttes på. Mangler den eller ligger den uden for området, findes der slet intet aflæsningspunkt. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Lytteadresse. Standarden er `127.0.0.1`. Værdierne `0.0.0.0`, `+` og `*` betyder alle adresser, og alt andet falder tilbage til `127.0.0.1`. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | Bearer-token, der kræves på `/metrics` og på `/ready`. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` lader `/ready` svare uden det token, til klyngeprøver. Værtsstier udelades så af svaret. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | Kommaadskilte afslutningskoder, der får `/ready` til at melde ikke klar. Erstatter den indbyggede liste. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` ser bort fra sidste gennemløbs afslutningskode og også fra tilstanden, før det første gennemløb er færdigt. |
| `ORGANIZE_FILES_READY_JSON` | `1` gennemtvinger JSON-svaret på `/ready`, også for en kalder, der bad om ren tekst. |

En adresse uden for loopback afvises, før lytteren åbnes, hvis der ikke er sat et bearer-token. Afvisningen skrives på fejludgangen og sendes som webhook-hændelse, for den kombination ville give hele netværket tællerne.

## Betjente stier

- `/metrics` — tællerne som Prometheus-tekst. En forespørgsel til `/` giver samme indhold.
- `/ready` — parathed til en orkestrator. Svaret er `200`, så snart automatiseringsmappen tager imod en prøveskrivning, jobfilen kan åbnes, historikmappen ligger inden for datamappen, og det seneste forfaldne gennemløb sluttede på en afslutningskode, der ikke blokerer. Ellers lyder svaret `503` med en kort grund som `due_pass_not_completed` eller `last_due_pass_license_failed`.
- `/health` — kun livstegn. Den sti forbliver anonym, selv når et token er sat, for den svarer `ok` og intet andet.

Afslutningskoderne `3` for en licensfejl, `8` for et låst udgangstræ, `10` for en sletning, der aldrig blev bekræftet, og `11` for en krav-konflikt blokerer paratheden som standard. Indholdet på `/ready` er JSON, medmindre kalderen sender `Accept: text/plain` eller tilføjer `?format=text`.

## Tællerne

| Navn | Indhold |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Forfaldne gennemløb, planlæggeren begyndte. |
| `organize_files_automation_jobs_started_total` | Jobkørsler, der nåede den kørende tilstand. |
| `organize_files_automation_jobs_skipped_total` | Sprunget over: et Docker- eller Kubernetes-miljø, der ikke er klar, et job rettet mod programmet på en vært uden skærm, en optaget udgangsmappe, eller et job, orkestratoren afviste. |
| `organize_files_automation_jobs_failed_total` | Jobkørsler, der endte i fejl. |
| `organize_files_automation_jobs_awaiting_approval_total` | Rigtige kørsler sat på pause for godkendelse. |
| `organize_files_automation_execute_approvals_total` | Godkendelser givet til en rigtig kørsel. |
| `organize_files_automation_execute_approvals_expired_total` | Godkendelser, hvis frist udløb før brug. |
| `organize_files_automation_claim_conflicts_total` | Gange hvor en anden vært allerede havde kravet på udgangsmappen. |
| `organize_files_automation_runs_orphaned_total` | Kørsler gendannet som forældreløse, efterladt af en vært, der stoppede. |
| `organize_files_automation_job_events_total` | En tæller pr. hændelse, med mærkaterne `event`, `job_id`, `target` og `jobs_file`. |
| `organize_files_automation_webhook_posts_succeeded_total` | Accepterede webhook-leveringer. |
| `organize_files_automation_webhook_posts_failed_total` | Afviste eller uopnåelige webhook-leveringer. |
| `organize_files_automation_webhook_dead_letter_depth` | Rækker, der lige nu venter i webhook-filen med ikke leverede beskeder. |
| `organize_files_automation_log_retention_pruned_total` | Kørselslogge fjernet af opbevaringen. |
| `organize_files_automation_runs_index_compacted_total` | Rækker taget ud af kørselsindekset ved sammenpresning. |
| `organize_files_automation_last_due_pass_exit_code` | Afslutningskoden for det senest afsluttede gennemløb. `0` er et rent gennemløb. |
| `organize_files_automation_last_due_pass_completed_utc` | Unix-tid i sekunder for det senest afsluttede gennemløb, og `0` før det første. |

## Instrumentbræt og alarmregler

Et færdigt Grafana-instrumentbræt udgives med installationsfilerne som `grafana-organize-files-automation.json` under titlen **OrganizeFiles Automation**. Dets ti ruder viser forfaldne gennemløb, startede og fejlede job, krav-konflikter, jobgennemstrømning over en time, den seneste afslutningskode, dybden af ikke leverede beskeder, webhook-fejl over et døgn, job der venter på godkendelse, og jobhændelser efter tilstand. Hver rude navngiver sin datakilde gennem pladsholderen `${DS_PROMETHEUS}`.

De tilhørende alarmregler er `alerts-organize-files-automation.yaml`, med `prometheus-rule-automation.yaml` som Kubernetes-indpakning til `kube-prometheus-stack`. En seneste afslutningskode forskellig fra nul advarer efter fem minutter, en licensfejl er kritisk efter ét minut, og de øvrige regler dækker fejlede job, krav-konflikter, webhook-fejl, en bunke ikke leverede beskeder og godkendelser, der har ventet et døgn. Begge filer kontrolleres ved hver bygning, så navnene ovenfor følger tællerne.

# Kørselsoutput og metrikker

## Statusrække

Området **Kørselsoutput** viser:

- Appens aktuelle tilstand og motorens fremdrift.
- **CPU** og to **hukommelsesværdier** kun for denne proces.
- **GPU**-linjer, på Windows: denne proces' andel af hvert grafikkort, ikke hele kortet.

Den samme kompakte ressourcelinje genbruges i sekundære værktøjsvinduer, såsom filudforskning, planlagte job og filreparation.

## Hukommelsesetiketter

- **Private bytes / commit** — privat virtuel hukommelse reserveret af processen.
- **Arbejdssæt/hukommelse** — resident RAM, som i øjeblikket opbevares af denne proces. Den kan adskille sig fra en anden operativsystemskærm, fordi hvert operativsystem og skrivebordsmiljø mærker proceshukommelse forskelligt.

## Kør heartbeat JSON (valgfrit)

Aktiver **Write run heartbeat JSON** under **Avanceret/Diagnostik**. Motoren skriver `Organize.Files.run.json` under `Output\_OrganizeMediaLogs` (samme mappe som standard genoptag-filen for organisering).

- **Sti** — opdateret atomisk under organisering og reparationskørsler.
- **Tidsintervaller** – mens kilder skannes, skrives filen om for hver 10.000 sete filer, hver 5.000 træffere og cirka hvert 15. sekund, så længe scanningen kører, så et stort netværkstræ, der er langsomt at liste, stadig viser, at kørslen lever. Under validering, hashing og flytninger skrives den om efter hver 1.000 filer, højst hvert 5. sekund. Skrivning ved start og slut sker stadig, når en kørsel begynder og slutter.
- **Fremdrift** – så længe filtallene stadig vokser, viser hovedforløbslinjen antallet af sete filer i stedet for 100 %, indtil en fase har et kendt samlet tal.
- **Felter** — `schema`, `mode`, `phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`), `runState`(`active`/`completed`/`failed`/`cancelled`), `utc` (ISO-8601), `dryRun`, `outputRoot`, `validateMedia`, `deepVideoValidate`, `gpuDeviceCount`, `hwaccel`, valgfrit `correlationId`, indlejret `progress` tællere.
- **Log** — Kør-outputpanelet udskriver den fulde sti ved start, og når filen gemmes i slutningen. Brug **Åbn heartbeat-log-mappe** / **Vis heartbeat-JSON-fil** under Avanceret / Diagnostik.
- **CLI** — `--heartbeat-json` på OrganizeFiles.Cli. Annuller og fatale shell-fejl skriv `cancelled`/`failed` `runState` når den er aktiveret.
