# Monitorizare cu Prometheus și Grafana

## Ce acoperă contoarele

Joburile programate țin un set mic de contoare și indicatori Prometheus. Fiecare nume începe cu `organize_files_automation_`, iar setul întreg este publicat ca text Prometheus. Toate cele trei gazde care rulează joburi publică același set: aplicația desktop, serviciul `OrganizeFiles.JobAgent` și gazda de linie de comandă folosită în containere.

Contoarele descriu planificatorul, nu fișierele. Se numără trecerile, rezultatele joburilor, aprobările, livrarea webhook și curățenia istoricului. Nu se numără nimic despre fișierele pe care le mută un job.

## Export în fișier, fără port deschis

`automation-metrics.prom` se scrie în folderul de date al automatizării, lângă `automation-jobs.json`, și se împrospătează după fiecare trecere scadentă și la fiecare citire. Formatul este cel pe care îl citește colectorul textfile din `node_exporter`, deci o mașină care rulează deja `node_exporter` este acoperită fără port în ascultare, fără token și fără regulă de firewall. Fișierul se înlocuiește atomic, iar o legătură simbolică lăsată în locul lui oprește scrierea în loc să fie urmată.

## Punctul de colectare

Punctul de colectare există doar când `ORGANIZE_FILES_METRICS_HTTP_PORT` conține un port între 1 și 65535. Fără acea variabilă nimic nu ascultă.

| Variabilă | Efect |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | Portul pe care se ascultă. Lipsa lui sau o valoare în afara intervalului înseamnă niciun punct de colectare. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Adresa de ascultare. Implicit este `127.0.0.1`. Valorile `0.0.0.0`, `+` și `*` înseamnă toate adresele, iar orice altceva revine la `127.0.0.1`. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | Tokenul bearer cerut pe `/metrics` și pe `/ready`. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` lasă `/ready` să răspundă fără acel token, pentru sondele de cluster. Căile de pe gazdă lipsesc atunci din răspuns. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | Coduri de ieșire separate prin virgulă care fac `/ready` să raporteze nepregătit. Înlocuiesc lista implicită. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` ignoră codul de ieșire al ultimei treceri, precum și starea de dinainte ca prima trecere să se încheie. |
| `ORGANIZE_FILES_READY_JSON` | `1` impune răspunsul JSON pe `/ready`, chiar și pentru un apelant care a cerut text simplu. |

O adresă din afara buclei locale este refuzată înainte de deschiderea ascultătorului dacă nu există token bearer. Refuzul este scris pe ieșirea de eroare și trimis ca eveniment webhook, fiindcă acea combinație ar da contoarele întregii rețele.

## Căile servite

- `/metrics` — contoarele ca text Prometheus. O cerere către `/` întoarce același conținut.
- `/ready` — pregătirea pentru un orchestrator. Răspunde `200` după ce folderul de automatizare acceptă o scriere de test, fișierul de joburi se deschide, folderul de istoric se rezolvă în rădăcina de date, iar ultima trecere scadentă s-a încheiat cu un cod de ieșire care nu blochează. Altfel răspunde `503` cu un motiv scurt, cum ar fi `due_pass_not_completed` sau `last_due_pass_license_failed`.
- `/health` — doar semnal de viață. Rămâne anonim chiar și când există token, fiindcă răspunde `ok` și nimic altceva.

Codurile de ieșire `3` pentru licență, `8` pentru arbore de ieșire blocat, `10` pentru o ștergere neconfirmată și `11` pentru conflict de revendicare blochează implicit pregătirea. Conținutul de pe `/ready` este JSON dacă apelantul nu trimite `Accept: text/plain` sau nu adaugă `?format=text`.

## Contoarele

| Nume | Ce conține |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Trecerile scadente începute de planificator. |
| `organize_files_automation_jobs_started_total` | Rulări de job care au ajuns în starea de execuție. |
| `organize_files_automation_jobs_skipped_total` | Joburi sărite: mediu Docker sau Kubernetes nepregătit, job cu țintă în aplicație pe o gazdă fără interfață, rădăcină de ieșire ocupată sau job respins de orchestrator. |
| `organize_files_automation_jobs_failed_total` | Rulări de job încheiate cu eșec. |
| `organize_files_automation_jobs_awaiting_approval_total` | Rulări reale oprite pentru aprobare. |
| `organize_files_automation_execute_approvals_total` | Aprobări acordate pentru o rulare reală. |
| `organize_files_automation_execute_approvals_expired_total` | Aprobări cărora le-a expirat timpul înainte de folosire. |
| `organize_files_automation_claim_conflicts_total` | Dăți în care altă gazdă deținea deja revendicarea pe rădăcina de ieșire. |
| `organize_files_automation_runs_orphaned_total` | Rulări recuperate ca orfane, lăsate de o gazdă oprită. |
| `organize_files_automation_job_events_total` | Un contor pe eveniment, cu etichetele `event`, `job_id`, `target` și `jobs_file`. |
| `organize_files_automation_webhook_posts_succeeded_total` | Livrări webhook acceptate. |
| `organize_files_automation_webhook_posts_failed_total` | Livrări webhook respinse sau fără destinatar. |
| `organize_files_automation_webhook_dead_letter_depth` | Rânduri aflate acum în fișierul webhook de mesaje nelivrate. |
| `organize_files_automation_log_retention_pruned_total` | Jurnale de rulare șterse de politica de păstrare. |
| `organize_files_automation_runs_index_compacted_total` | Rânduri scoase din indexul rulărilor la compactare. |
| `organize_files_automation_last_due_pass_exit_code` | Codul de ieșire al ultimei treceri încheiate. `0` înseamnă trecere curată. |
| `organize_files_automation_last_due_pass_completed_utc` | Timpul Unix în secunde al ultimei treceri încheiate, iar `0` înainte de prima. |

## Tablou de bord și reguli de alertă

Un tablou de bord Grafana gata făcut este publicat cu fișierele de instalare ca `grafana-organize-files-automation.json`, sub titlul **OrganizeFiles Automation**. Cele zece panouri arată trecerile scadente, joburile pornite și eșuate, conflictele de revendicare, debitul de joburi pe o oră, ultimul cod de ieșire, adâncimea mesajelor nelivrate, eșecurile webhook pe o zi, joburile care așteaptă aprobare și evenimentele de job pe stări. Fiecare panou își numește sursa de date prin marcajul `${DS_PROMETHEUS}`.

Regulile de alertă potrivite sunt `alerts-organize-files-automation.yaml`, cu `prometheus-rule-automation.yaml` drept învelișul Kubernetes pentru `kube-prometheus-stack`. Un ultim cod de ieșire diferit de zero avertizează după cinci minute, un eșec de licență este critic după unul, iar restul regulilor acoperă joburile eșuate, conflictele de revendicare, eșecurile webhook, un teanc de mesaje nelivrate și aprobările lăsate în așteptare o zi. Ambele fișiere sunt validate la fiecare compilare, deci numele de mai sus rămân în pas cu contoarele.

# Jurnal și metrici

## Rând stare

Zona **Jurnal rulare** arată:

- Starea curentă a aplicației și progresul motorului.
- **CPU** și două valori de **memorie** doar pentru acest proces.
- Liniile **GPU**, pe Windows: cota acestui proces din fiecare placă video, nu toată placa.

Aceeași bară compactă de resurse este refolosită în ferestrele de instrumente, cum ar fi explorarea fișierelor, joburile programate și repararea fișierelor.

## Etichete memorie

- **Memorie privată / commit** — memorie virtuală privată rezervată de proces.
- **Working set / memorie** — RAM rezident ținut curent de acest proces. Poate diferi față de alt monitor al sistemului de operare, deoarece fiecare OS și mediu desktop etichetează diferit memoria proceselor.

## Heartbeat JSON rulare (optional)

Activează **Scrie fișierul JSON de heartbeat în jurnalul de rulare** la **Avansat / Diagnostic**. Motorul scrie `Organize.Files.run.json` în `Output\_OrganizeMediaLogs` (același folder ca fișierul implicit de reluare. În UI apare ca folderul Destinație).

- **Cale** — actualizat atomic la organizare și reparare.
- **Ritm** — la scanarea surselor, fișierul se rescrie la fiecare 10.000 de fișiere văzute, la fiecare 5.000 de potriviri și la circa 15 secunde cât timp scanarea continuă, deci un arbore mare de rețea care se listează greu arată totuși că rularea e vie. La validare, la hashing și la mutări se rescrie după fiecare 1.000 de fișiere, cel mult o dată la 5 secunde. Scrieri la start și la final când rularea începe sau se termină.
- **Progres** — cât timp numerele cresc, bara principală arată fișiere văzute până acum, nu 100%, până când o fază are total cunoscut.
- **Câmpuri** — `schema`, `mode`, `phase` (ex. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`), `runState` (`active` / `completed` / `failed` / `cancelled`), `utc` (ISO-8601), `dryRun`, `outputRoot`, `validateMedia`, `deepVideoValidate`, `gpuDeviceCount`, `hwaccel`, `correlationId` opțional, contoare `progress` imbricate.
- **Jurnal** — jurnalul de rulare afișează calea completă la start și la salvare. Folosește **Deschide folderul jurnalului heartbeat** / **Arată fișierul JSON heartbeat** la Avansat / Diagnostic.
- **CLI** — `--heartbeat-json` pe OrganizeFiles.Cli. Anularea și erorile fatale din shell scriu `cancelled` / `failed` când e activ.
