# Monitering met Prometheus en Grafana

## Wat die tellers dek

Geskeduleerde take hou 'n klein stel Prometheus-tellers en -meters. Elke naam begin met `organize_files_automation_`, en die hele stel word as Prometheus-teks gepubliseer. Al drie gashere wat take uitvoer publiseer dieselfde stel: die werkskermtoepassing, die diens `OrganizeFiles.JobAgent` en die opdraglyn-gasheer wat in houers gebruik word.

Die tellers beskryf die skeduleerder, nie die lêers nie. Getel word deurlope, taakuitkomste, goedkeurings, webhook-aflewering en die opruiming van die geskiedenis. Oor die lêers wat 'n taak skuif word niks getel nie.

## Uitvoer na 'n lêer, sonder oop poort

`automation-metrics.prom` word in die outomatiseringsdatagids langs `automation-jobs.json` geskryf en na elke opeisbare deurloop en by elke aflesing opgedateer. Die uitleg is die een wat die textfile-versamelaar van `node_exporter` lees, dus is 'n masjien waarop `node_exporter` reeds loop gedek sonder 'n luisterende poort, sonder 'n teken en sonder 'n brandmuurreël. Die lêer word atomies vervang, en 'n simboliese skakel wat in sy plek gelaat is stop die skryf eerder as om gevolg te word.

## Aflesingspunt

Die aflesingspunt bestaan slegs wanneer `ORGANIZE_FILES_METRICS_HTTP_PORT` 'n poort tussen 1 en 65535 bevat. Sonder daardie veranderlike luister niks.

| Veranderlike | Uitwerking |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | Poort om op te luister. Ontbreek dit of val dit buite die reeks, dan is daar glad geen aflesingspunt nie. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Luisteradres. Die verstek is `127.0.0.1`. Die waardes `0.0.0.0`, `+` en `*` beteken elke adres, en enigiets anders val terug op `127.0.0.1`. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | Bearer-teken wat op `/metrics` en op `/ready` vereis word. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` laat `/ready` sonder daardie teken antwoord, vir trosproewe. Gasheerpaaie bly dan uit die antwoord. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | Kommageskeide afsluitkodes waarby `/ready` nie gereed meld nie. Vervang die ingeboude lys. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` ignoreer die afsluitkode van die laaste deurloop, en ook die toestand voordat die eerste deurloop klaar is. |
| `ORGANIZE_FILES_READY_JSON` | `1` dwing die JSON-liggaam op `/ready` af, selfs vir 'n oproeper wat gewone teks gevra het. |

'n Adres buite die terugluslyn word geweier voordat die luisteraar oopgaan, tensy 'n bearer-teken gestel is. Die weiering word na die foutafvoer geskryf en as webhook-gebeurtenis gestuur, want daardie kombinasie sou die tellers aan die hele netwerk gee.

## Bediende paaie

- `/metrics` — die tellers as Prometheus-teks. 'n Versoek aan `/` lewer dieselfde inhoud.
- `/ready` — gereedheid vir 'n orkestreerder. Die antwoord is `200` sodra die outomatiseringsgids 'n toetsskryf aanvaar, die taaklêer oopgaan, die geskiedenisgids binne die datawortel oplos, en die laaste opeisbare deurloop op 'n afsluitkode geëindig het wat nie blokkeer nie. Andersins is die antwoord `503` met 'n kort rede soos `due_pass_not_completed` of `last_due_pass_license_failed`.
- `/health` — slegs lewensteken. Daardie pad bly anoniem selfs wanneer 'n teken gestel is, want dit antwoord `ok` en niks anders nie.

Die afsluitkodes `3` vir 'n lisensiefout, `8` vir 'n geslote afvoerboom, `10` vir 'n skrapping wat nooit bevestig is nie en `11` vir 'n eisbotsing blokkeer die gereedheid by verstek. Die liggaam van `/ready` is JSON tensy die oproeper `Accept: text/plain` stuur of `?format=text` byvoeg.

## Die tellers

| Naam | Inhoud |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Opeisbare deurlope wat die skeduleerder begin het. |
| `organize_files_automation_jobs_started_total` | Taakuitvoerings wat die lopende toestand bereik het. |
| `organize_files_automation_jobs_skipped_total` | Oorgeslaan take: 'n Docker- of Kubernetes-omgewing wat nie gereed is nie, 'n taak gemik op die toepassing op 'n gasheer sonder skerm, 'n besette afvoerwortel, of 'n taak wat die orkestreerder geweier het. |
| `organize_files_automation_jobs_failed_total` | Taakuitvoerings wat op 'n fout geëindig het. |
| `organize_files_automation_jobs_awaiting_approval_total` | Werklike uitvoerings wat vir goedkeuring wag. |
| `organize_files_automation_execute_approvals_total` | Goedkeurings aan 'n werklike uitvoering verleen. |
| `organize_files_automation_execute_approvals_expired_total` | Goedkeurings waarvan die tyd voor gebruik verstryk het. |
| `organize_files_automation_claim_conflicts_total` | Kere waar 'n ander gasheer die eis op die afvoerwortel reeds gehad het. |
| `organize_files_automation_runs_orphaned_total` | Uitvoerings wat as weeskinders herwin is, gelaat deur 'n gasheer wat gestop het. |
| `organize_files_automation_job_events_total` | Een teller per gebeurtenis, met die etikette `event`, `job_id`, `target` en `jobs_file`. |
| `organize_files_automation_webhook_posts_succeeded_total` | Aanvaarde webhook-afleweringe. |
| `organize_files_automation_webhook_posts_failed_total` | Geweierde of onbereikbare webhook-afleweringe. |
| `organize_files_automation_webhook_dead_letter_depth` | Reëls wat op hierdie oomblik in die lêer van onafgelewerde webhooks wag. |
| `organize_files_automation_log_retention_pruned_total` | Uitvoeringsjoernale wat die bewaringsreël verwyder het. |
| `organize_files_automation_runs_index_compacted_total` | Reëls wat tydens verdigting uit die uitvoeringsindeks geval het. |
| `organize_files_automation_last_due_pass_exit_code` | Afsluitkode van die laaste voltooide deurloop. `0` is 'n skoon deurloop. |
| `organize_files_automation_last_due_pass_completed_utc` | Unix-tyd in sekondes van die laaste voltooide deurloop, en `0` voor die eerste. |

## Paneelbord en alarmreëls

'n Klaargemaakte Grafana-paneelbord word saam met die ontplooiingslêers gepubliseer as `grafana-organize-files-automation.json`, onder die titel **OrganizeFiles Automation**. Sy tien panele wys opeisbare deurlope, begonne en mislukte take, eisbotsings, taakdeurset oor 'n uur, die laaste afsluitkode, die diepte van onafgelewerde boodskappe, webhook-foute oor 'n dag, take wat vir goedkeuring wag, en taakgebeurtenisse volgens toestand. Elke paneel noem sy databron deur die plekhouer `${DS_PROMETHEUS}`.

Die passende alarmreëls is `alerts-organize-files-automation.yaml`, met `prometheus-rule-automation.yaml` as die Kubernetes-omhulsel vir `kube-prometheus-stack`. 'n Laaste afsluitkode anders as nul waarsku na vyf minute, 'n lisensiefout is na een minuut krities, en die res van die reëls dek mislukte take, eisbotsings, webhook-foute, 'n opeenhoping van onafgelewerde boodskappe en goedkeurings wat 'n dag lank wag. Albei lêers word by elke bou nagegaan, sodat die name hierbo tred hou met die tellers.

# Lopie-uitset en statistieke

## Status ry

Die **Lopie-uitset** area wys:

- Huidige toestand van die program en vordering van die enjin.
- **CPU** en twee **geheue** waardes slegs vir hierdie proses.
- **GPU**-reëls, op Windows: hierdie proses se aandeel van elke grafiese kaart, nie die hele kaart nie.

Dieselfde kompakte hulpbronbalk word hergebruik in sekondêre gereedskapvensters soos lêerverkenning, geskeduleerde take en lêerherstel.

## Geheue-etikette

- **Privaat grepe / commit** - private virtuele geheue wat deur die proses gereserveer word.
- **Werkstel / geheue** — inwonende RAM wat tans deur hierdie proses gehou word. Dit kan verskil van 'n ander bedryfstelselmonitor omdat elke bedryfstelsel en rekenaaromgewing die geheue verskillend verwerk.

## Lopie-hartklop JSON (opsioneel)

Aktiveer **Write run heartbeat JSON** onder **Gevorderd / Diagnostiek**. Die enjin skryf `Organize.Files.run.json`onder `Output\_OrganizeMediaLogs` (dieselfde vouer as die verstek organiseer hervatlêer).

- **Pad** - atomies opgedateer tydens organisering en herstellopies.
- **Tydsberekening** – terwyl bronne geskandeer word, word die lêer herskryf vir elke 10 000 lêers gesien, elke 5 000 passings en ongeveer elke 15 sekondes solank die skandering nog loop, sodat 'n groot netwerkboom wat stadig lys steeds wys dat die lopie lewe. Tydens validering, hashing en skuiwe word dit ná elke 1 000 lêers herskryf, hoogstens elke 5 sekondes. Skryfwerk aan die begin en die einde gebeur steeds wanneer 'n lopie begin en klaarmaak.
- **Vordering** – terwyl lêertellings nog groei, wys die hoofvorderingsbalk die lêers wat tot dusver gesien is in plaas van 100%, totdat 'n fase 'n bekende totaal het.
- **Velde** — `schema`, `mode`, `phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`), `runState`(`active` / `completed` / `failed` / `cancelled`), `utc` (ISO-8601), `dryRun`, `outputRoot`, `validateMedia`, `deepVideoValidate`, `gpuDeviceCount`, `hwaccel`, opsioneel `correlationId`, geneste `progress` tellers.
- **Log** — die uitvoerpaneel druk die volledige pad af aan die begin en wanneer die lêer aan die einde gestoor word. Gebruik **Maak hartkloploglêer oop** / **Wys hartklop JSON-lêer** onder Gevorderd / Diagnostiek.
- **CLI** — `--heartbeat-json`aan OrganizeFiles.Cli. Kanselleer en noodlottige dopfoute skryf `cancelled` / `failed` `runState` wanneer dit geaktiveer is.
