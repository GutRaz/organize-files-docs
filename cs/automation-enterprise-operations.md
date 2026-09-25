# Sledování pomocí Prometheus a Grafana

## Co čítače pokrývají

Naplánované úlohy vedou malou sadu čítačů a ukazatelů Prometheus. Každý název začíná na `organize_files_automation_` a celá sada se zveřejňuje jako text Prometheus. Všichni tři hostitelé, kteří spouštějí úlohy, zveřejňují tutéž sadu: aplikace na ploše, služba `OrganizeFiles.JobAgent` a hostitel příkazového řádku používaný v kontejnerech.

Čítače popisují plánovač, nikoli soubory. Počítají se průchody, výsledky úloh, schválení, doručení webhooků a údržba historie. O souborech, které úloha přesouvá, se nepočítá nic.

## Export do souboru, bez otevřeného portu

`automation-metrics.prom` se zapisuje do datové složky automatizace vedle souboru `automation-jobs.json` a obnovuje se po každém splatném průchodu a při každém odečtu. Formát je ten, který čte sběrač textfile nástroje `node_exporter`, takže stroj, na němž `node_exporter` už běží, je pokryt bez naslouchajícího portu, bez tokenu a bez pravidla brány firewall. Soubor se nahrazuje atomicky a symbolický odkaz ponechaný na jeho místě zápis zastaví, místo aby jej následoval.

## Odečtový bod

Odečtový bod existuje jen tehdy, když `ORGANIZE_FILES_METRICS_HTTP_PORT` obsahuje port mezi 1 a 65535. Bez té proměnné nic nenaslouchá.

| Proměnná | Účinek |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | Port, na kterém se naslouchá. Pokud chybí nebo leží mimo rozsah, žádný odečtový bod neexistuje. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Adresa naslouchání. Výchozí je `127.0.0.1`. Hodnoty `0.0.0.0`, `+` a `*` znamenají všechny adresy a cokoli jiného se vrací k `127.0.0.1`. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | Token bearer vyžadovaný na `/metrics` a na `/ready`. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` nechá `/ready` odpovědět bez toho tokenu, kvůli sondám clusteru. Cesty hostitele pak v odpovědi chybí. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | Čárkami oddělené návratové kódy, při nichž `/ready` hlásí nepřipraveno. Nahrazuje vestavěný seznam. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` pomíjí návratový kód posledního průchodu i stav před dokončením prvního průchodu. |
| `ORGANIZE_FILES_READY_JSON` | `1` vynutí odpověď JSON na `/ready`, i pro volajícího, který požádal o prostý text. |

Adresa mimo místní smyčku je odmítnuta ještě před otevřením posluchače, pokud není nastaven token bearer. Odmítnutí se zapíše na chybový výstup a odešle jako událost webhooku, protože ta kombinace by vydala čítače celé síti.

## Obsluhované cesty

- `/metrics` — čítače jako text Prometheus. Požadavek na `/` vrátí tentýž obsah.
- `/ready` — připravenost pro orchestrátor. Odpověď je `200`, jakmile složka automatizace přijme zkušební zápis, soubor úloh se otevře, složka historie se rozliší uvnitř datového kořene a poslední splatný průchod skončil návratovým kódem, který neblokuje. Jinak je odpovědí `503` s krátkým důvodem, jako `due_pass_not_completed` nebo `last_due_pass_license_failed`.
- `/health` — jen známka života. Ta cesta zůstává anonymní i tehdy, když je token nastaven, protože odpovídá `ok` a nic jiného.

Návratové kódy `3` pro selhání licence, `8` pro uzamčený výstupní strom, `10` pro nikdy nepotvrzené smazání a `11` pro konflikt nároku blokují připravenost ve výchozím nastavení. Tělo odpovědi na `/ready` je JSON, pokud volající nepošle `Accept: text/plain` nebo nepřidá `?format=text`.

## Čítače

| Název | Obsah |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Splatné průchody, které plánovač zahájil. |
| `organize_files_automation_jobs_started_total` | Běhy úloh, které dosáhly spuštěného stavu. |
| `organize_files_automation_jobs_skipped_total` | Přeskočené úlohy: prostředí Docker nebo Kubernetes, které není připravené, úloha mířící do aplikace na hostiteli bez obrazovky, obsazený výstupní kořen, nebo úloha, kterou orchestrátor odmítl. |
| `organize_files_automation_jobs_failed_total` | Běhy úloh, které skončily chybou. |
| `organize_files_automation_jobs_awaiting_approval_total` | Skutečné běhy odložené ke schválení. |
| `organize_files_automation_execute_approvals_total` | Schválení udělená skutečnému běhu. |
| `organize_files_automation_execute_approvals_expired_total` | Schválení, jimž vypršela lhůta před použitím. |
| `organize_files_automation_claim_conflicts_total` | Případy, kdy jiný hostitel už držel nárok na výstupní kořen. |
| `organize_files_automation_runs_orphaned_total` | Běhy obnovené jako osiřelé, zanechané hostitelem, který se zastavil. |
| `organize_files_automation_job_events_total` | Jeden čítač na událost, se značkami `event`, `job_id`, `target` a `jobs_file`. |
| `organize_files_automation_webhook_posts_succeeded_total` | Přijatá doručení webhooků. |
| `organize_files_automation_webhook_posts_failed_total` | Odmítnutá nebo nedosažitelná doručení webhooků. |
| `organize_files_automation_webhook_dead_letter_depth` | Řádky, které právě teď čekají v souboru nedoručených webhooků. |
| `organize_files_automation_log_retention_pruned_total` | Protokoly běhů odstraněné uchováváním. |
| `organize_files_automation_runs_index_compacted_total` | Řádky vyřazené z indexu běhů při zhuštění. |
| `organize_files_automation_last_due_pass_exit_code` | Návratový kód naposledy dokončeného průchodu. `0` je čistý průchod. |
| `organize_files_automation_last_due_pass_completed_utc` | Čas Unix v sekundách naposledy dokončeného průchodu, a `0` před prvním. |

## Přehled a pravidla výstrah

Hotový přehled Grafana se zveřejňuje s nasazovacími soubory jako `grafana-organize-files-automation.json`, pod názvem **OrganizeFiles Automation**. Jeho deset panelů ukazuje splatné průchody, zahájené a neúspěšné úlohy, konflikty nároku, propustnost úloh za hodinu, poslední návratový kód, hloubku nedoručených zpráv, chyby webhooků za den, úlohy čekající na schválení a události úloh podle stavu. Každý panel pojmenovává svůj zdroj dat zástupným symbolem `${DS_PROMETHEUS}`.

Odpovídající pravidla výstrah jsou `alerts-organize-files-automation.yaml`, s `prometheus-rule-automation.yaml` jako obalem Kubernetes pro `kube-prometheus-stack`. Poslední návratový kód různý od nuly varuje po pěti minutách, selhání licence je kritické po jedné minutě a zbývající pravidla pokrývají neúspěšné úlohy, konflikty nároku, chyby webhooků, nahromadění nedoručených zpráv a schválení ponechaná den v čekání. Oba soubory se ověřují při každém sestavení, takže názvy výše drží krok s čítači.

# Výstup běhu a metriky

## Stavový řádek

Oblast **Výstup běhu** zobrazuje:

- Aktuální stav aplikace a průběh motoru.
- **CPU** a dvě hodnoty **paměť** pouze pro tento proces.
- Řádky **GPU**, ve Windows: podíl tohoto procesu na každé grafické kartě, ne celá karta.

Stejný kompaktní panel prostředků se znovu používá v oknech sekundárních nástrojů, jako je průzkum souborů, plánované úlohy a opravy souborů.

## Štítky paměti

- **Private bytes / commit** — soukromá virtuální paměť rezervovaná procesem.
- **Pracovní sada / paměť** — rezidentní paměť RAM, kterou tento proces aktuálně drží. Může se lišit od jiného monitoru operačního systému, protože každý OS a desktopové prostředí označuje procesná paměť odlišně.

## Spustit heartbeat JSON (volitelné)

Povolte **Zapisování běhu prezenčního signálu JSON** v části **Pokročilé / Diagnostika**. Motor píše `Organize.Files.run.json`pod`Output\_OrganizeMediaLogs` (stejná složka jako výchozí soubor obnovení pro uspořádání).

- **Cesta** – aktualizována atomicky během organizování a oprav.
- **Načasování** — během prohledávání zdrojů se soubor přepisuje po každých 10 000 spatřených souborech, po každých 5 000 shodách a zhruba každých 15 sekund, dokud prohledávání běží, takže i velký síťový strom, který se vypisuje pomalu, ukazuje, že běh žije. Při ověřování, hashování a přesunech se přepisuje po každých 1 000 souborech, nejvýše jednou za 5 sekund. Zápis na začátku a na konci se stále děje, když běh začíná a končí.
- **Postup** — dokud počty souborů ještě rostou, hlavní ukazatel postupu ukazuje dosud spatřené soubory místo sta procent, dokud fáze nezná svůj celek.
- **Pole** — `schema`,`mode`,`phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`),`runState` (`active`/`completed`/`failed`/`cancelled`), `utc` (ISO-8601), `dryRun`,`outputRoot`,`validateMedia`,`deepVideoValidate`,`gpuDeviceCount`, `hwaccel`, volitelný`correlationId`, vnořený `progress` pulty.
- **Log** – panel výstupu běhu vytiskne úplnou cestu na začátku a při uložení souboru na konci. Použijte **Otevřít složku protokolu srdečního tepu** / **Zobrazit soubor JSON srdečního tepu** v části Upřesnit / Diagnostika.
- **CLI** – `--heartbeat-json` v OrganizeFiles.Cli. Zrušení a fatální chyby shellu zapíší `runState` `cancelled` / `failed`, pokud je zapnuto.
