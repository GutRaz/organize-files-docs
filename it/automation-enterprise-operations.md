# Monitoraggio con Prometheus e Grafana

## Che cosa coprono i contatori

I lavori programmati tengono un piccolo insieme di contatori e indicatori Prometheus. Ogni nome inizia con `organize_files_automation_`, e l'insieme completo viene pubblicato come testo Prometheus. Tutti e tre gli host che eseguono lavori pubblicano lo stesso insieme: l'applicazione desktop, il servizio `OrganizeFiles.JobAgent` e l'host a riga di comando usato nei contenitori.

I contatori descrivono il pianificatore, non i file. Si contano le passate, gli esiti dei lavori, le approvazioni, la consegna dei webhook e la manutenzione della cronologia. Sui file che un lavoro sposta non viene contato nulla.

## Esportazione su file, senza aprire porte

`automation-metrics.prom` viene scritto nella cartella dati dell'automazione, accanto a `automation-jobs.json`, e aggiornato dopo ogni passata scaduta e a ogni lettura. Il formato è quello che legge il collettore textfile di `node_exporter`, quindi una macchina che esegue già `node_exporter` è coperta senza porta in ascolto, senza token e senza regola del firewall. Il file viene sostituito in modo atomico, e un collegamento simbolico lasciato al suo posto ferma la scrittura invece di essere seguito.

## Punto di lettura

Il punto di lettura esiste solo quando `ORGANIZE_FILES_METRICS_HTTP_PORT` contiene una porta compresa tra 1 e 65535. Senza quella variabile non ascolta nulla.

| Variabile | Effetto |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | Porta di ascolto. Se manca o è fuori intervallo, non esiste alcun punto di lettura. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Indirizzo di ascolto. Il valore predefinito è `127.0.0.1`. I valori `0.0.0.0`, `+` e `*` indicano ogni indirizzo, e qualsiasi altro ricade su `127.0.0.1`. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | Token bearer richiesto su `/metrics` e su `/ready`. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` lascia rispondere `/ready` senza quel token, per le sonde del cluster. I percorsi dell'host restano allora fuori dalla risposta. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | Codici di uscita separati da virgole che fanno segnalare a `/ready` lo stato non pronto. Sostituisce l'elenco incorporato. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` trascura il codice di uscita dell'ultima passata, e anche lo stato precedente alla fine della prima. |
| `ORGANIZE_FILES_READY_JSON` | `1` impone la risposta JSON su `/ready`, anche per un chiamante che ha chiesto testo semplice. |

Un indirizzo fuori dal loopback viene rifiutato prima dell'apertura dell'ascoltatore se non è impostato un token bearer. Il rifiuto viene scritto sull'uscita di errore ed emesso come evento webhook, perché quella combinazione consegnerebbe i contatori a tutta la rete.

## Percorsi serviti

- `/metrics` — i contatori come testo Prometheus. Una richiesta a `/` restituisce lo stesso contenuto.
- `/ready` — prontezza per un orchestratore. Risponde `200` quando la cartella di automazione accetta una scrittura di prova, il file dei lavori si apre, la cartella della cronologia si risolve dentro la radice dei dati e l'ultima passata scaduta si è chiusa con un codice di uscita che non blocca. Altrimenti risponde `503` con un motivo breve come `due_pass_not_completed` oppure `last_due_pass_license_failed`.
- `/health` — solo segno di vita. Quel percorso resta anonimo anche quando un token è impostato, perché risponde `ok` e niente altro.

I codici di uscita `3` per un errore di licenza, `8` per un albero di destinazione bloccato, `10` per un'eliminazione mai confermata e `11` per un conflitto di rivendicazione bloccano la prontezza in modo predefinito. Il corpo di `/ready` è JSON a meno che il chiamante non invii `Accept: text/plain` o aggiunga `?format=text`.

## I contatori

| Nome | Contenuto |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Passate scadute avviate dal pianificatore. |
| `organize_files_automation_jobs_started_total` | Esecuzioni di lavoro giunte allo stato in corso. |
| `organize_files_automation_jobs_skipped_total` | Lavori saltati: ambiente Docker o Kubernetes non pronto, lavoro rivolto all'applicazione su un host senza interfaccia, radice di destinazione occupata, oppure lavoro respinto dall'orchestratore. |
| `organize_files_automation_jobs_failed_total` | Esecuzioni di lavoro chiuse con esito negativo. |
| `organize_files_automation_jobs_awaiting_approval_total` | Esecuzioni reali messe in attesa di approvazione. |
| `organize_files_automation_execute_approvals_total` | Approvazioni concesse per un'esecuzione reale. |
| `organize_files_automation_execute_approvals_expired_total` | Approvazioni scadute prima dell'uso. |
| `organize_files_automation_claim_conflicts_total` | Volte in cui un altro host deteneva già la rivendicazione sulla radice di destinazione. |
| `organize_files_automation_runs_orphaned_total` | Esecuzioni recuperate come orfane, lasciate da un host fermato. |
| `organize_files_automation_job_events_total` | Un contatore per evento, con le etichette `event`, `job_id`, `target` e `jobs_file`. |
| `organize_files_automation_webhook_posts_succeeded_total` | Consegne webhook accettate. |
| `organize_files_automation_webhook_posts_failed_total` | Consegne webhook rifiutate o irraggiungibili. |
| `organize_files_automation_webhook_dead_letter_depth` | Righe in attesa in questo momento nel file dei webhook non consegnati. |
| `organize_files_automation_log_retention_pruned_total` | Registri di esecuzione rimossi dalla conservazione. |
| `organize_files_automation_runs_index_compacted_total` | Righe tolte dall'indice delle esecuzioni durante la compattazione. |
| `organize_files_automation_last_due_pass_exit_code` | Codice di uscita dell'ultima passata conclusa. `0` indica una passata pulita. |
| `organize_files_automation_last_due_pass_completed_utc` | Ora Unix in secondi dell'ultima passata conclusa, e `0` prima della prima. |

## Cruscotto e regole di allerta

Un cruscotto Grafana già pronto viene pubblicato con i file di distribuzione come `grafana-organize-files-automation.json`, con il titolo **OrganizeFiles Automation**. I suoi dieci riquadri mostrano le passate scadute, i lavori avviati e falliti, i conflitti di rivendicazione, la portata dei lavori su un'ora, l'ultimo codice di uscita, la profondità dei messaggi non consegnati, gli errori webhook su un giorno, i lavori in attesa di approvazione e gli eventi di lavoro per stato. Ogni riquadro nomina la propria origine dati tramite il segnaposto `${DS_PROMETHEUS}`.

Le regole di allerta corrispondenti sono `alerts-organize-files-automation.yaml`, con `prometheus-rule-automation.yaml` come involucro Kubernetes per `kube-prometheus-stack`. Un ultimo codice di uscita diverso da zero avvisa dopo cinque minuti, un errore di licenza è critico dopo uno, e le altre regole coprono i lavori falliti, i conflitti di rivendicazione, gli errori webhook, un arretrato di messaggi non consegnati e le approvazioni lasciate in attesa per un giorno. Entrambi i file sono convalidati a ogni compilazione, così i nomi qui sopra restano al passo con i contatori.

# Output dell'esecuzione e metriche

## Riga di stato

L'area **Output dell'esecuzione** mostra:

- Stato attuale dell'app e avanzamento del motore.
- **CPU** e due valori di **memoria** solo per questo processo.
- Righe **GPU**, su Windows: la quota di ogni scheda grafica usata da questo processo, non l'intera scheda.

La stessa barra delle risorse compatta viene riutilizzata nelle finestre degli strumenti secondari come l'esplorazione dei file, i processi pianificati e la riparazione dei file.

## Etichette di memoria

- **Byte privati/commit**: memoria virtuale privata riservata dal processo.
- **Working set/memoria**: RAM residente attualmente conservata da questo processo. Può differire da un altro monitor del sistema operativo perché ogni sistema operativo e ambiente desktop etichetta l'elaborazione della memoria in modo diverso.

## Esegui heartbeat JSON (facoltativo)

Abilita **Scrivi JSON run heartbeat** in **Avanzate/Diagnostica**. Il motore scrive `Organize.Files.run.json` in `Output\_OrganizeMediaLogs` (stessa cartella del file di ripristino organizzato predefinito).

- **Percorso**: aggiornato atomicamente durante le esecuzioni di organizzazione e riparazione.
- **Cadenza** — mentre si percorrono le fonti, il file viene riscritto ogni 10.000 file visti, ogni 5.000 corrispondenze e all'incirca ogni 15 secondi finché la scansione continua, quindi un grande albero di rete lento da elencare mostra comunque che l'esecuzione è viva. Durante la convalida, l'hashing e gli spostamenti viene riscritto dopo ogni 1.000 file, al massimo ogni 5 secondi. Le scritture di inizio e di fine avvengono ancora quando un'esecuzione comincia e finisce.
- **Avanzamento** — finché il numero di file cresce ancora, la barra principale mostra i file visti finora invece del 100%, fino a quando una fase non conosce il proprio totale.
- **Campi** — `schema`, `mode`, `phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`), `runState` (`active` / `completed` / `failed` / `cancelled`), `utc` (ISO-8601), `dryRun`, `outputRoot`, `validateMedia`, `deepVideoValidate`, `gpuDeviceCount`, `hwaccel`, opzionale `correlationId`, contatori nidificati `progress`.
- **Log**: il pannello di output dell'esecuzione stampa il percorso completo all'inizio e quando il file viene salvato alla fine. Utilizza **Apri cartella registro heartbeat**/**Mostra file JSON heartbeat** in Avanzate/Diagnostica.
- **CLI** — `--heartbeat-json` su OrganizeFiles.Cli. Gli errori irreversibili e di annullamento della shell scrivono `cancelled` / `failed` `runState` quando abilitato.
