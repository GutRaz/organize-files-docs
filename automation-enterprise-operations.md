# Prometheus and Grafana monitoring

## What the counters cover

Scheduled jobs keep a small set of Prometheus counters and gauges. Every name starts with `organize_files_automation_`, and the whole set is published as Prometheus text. All three hosts that run jobs publish the same set: the desktop application, the `OrganizeFiles.JobAgent` service, and the command-line host used inside containers.

The counters describe the scheduler, not the files. Passes, job outcomes, approvals, webhook delivery and history housekeeping are counted. Nothing is counted about the files a job moves.

## Export to a file, with no port open

`automation-metrics.prom` is written into the automation data folder, beside `automation-jobs.json`, and refreshed after every due pass and on every scrape. The layout is the one the `node_exporter` textfile collector reads, so a machine that already runs `node_exporter` is covered without a listening port, without a token and without a firewall rule. The file is replaced atomically, and a symbolic link left in its place stops the write instead of being followed.

## Scrape endpoint

The endpoint exists only when `ORGANIZE_FILES_METRICS_HTTP_PORT` holds a port between 1 and 65535. Without that variable nothing listens.

| Variable | Effect |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | Port to listen on. Missing or out of range means no endpoint at all. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Listen address. The default is `127.0.0.1`. The values `0.0.0.0`, `+` and `*` all mean every address, and anything else falls back to `127.0.0.1`. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | Bearer token required on `/metrics` and on `/ready`. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` lets `/ready` answer without that token, for cluster probes. Host paths are then left out of the answer. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | Comma-separated exit codes that make `/ready` report not ready. Replaces the built-in list. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` ignores the last due-pass exit code, and also the state before the first pass has finished. |
| `ORGANIZE_FILES_READY_JSON` | `1` forces the JSON body on `/ready`, even for a caller that asked for plain text. |

An address outside loopback is refused before the listener opens unless a bearer token is set. The refusal is printed on standard error and emitted as a webhook event, because that combination would hand the counters to the whole network.

## Paths served

- `/metrics` — the counters as Prometheus text. A request to `/` returns the same body.
- `/ready` — readiness for an orchestrator. It answers `200` once the automation folder accepts a probe write, the jobs file opens, the run-history folder resolves inside the data root, and the last due pass ended on an exit code that does not block. Otherwise it answers `503` with a short reason such as `due_pass_not_completed` or `last_due_pass_license_failed`.
- `/health` — liveness only. It stays anonymous even when a token is set, because it answers `ok` and nothing else.

Exit codes `3` for a license failure, `8` for a locked output tree, `10` for a delete that was never confirmed and `11` for a claim conflict block readiness by default. The `/ready` body is JSON unless the caller sends `Accept: text/plain` or adds `?format=text`.

## The counters

| Name | What it holds |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Due passes the scheduler began. |
| `organize_files_automation_jobs_started_total` | Job runs that reached the running state. |
| `organize_files_automation_jobs_skipped_total` | Jobs passed over: a Docker or Kubernetes environment that is not ready, an app-target job on a headless host, a busy output root, or a job the orchestrator refused. |
| `organize_files_automation_jobs_failed_total` | Job runs that ended in failure. |
| `organize_files_automation_jobs_awaiting_approval_total` | Execute runs parked for approval. |
| `organize_files_automation_execute_approvals_total` | Approvals granted for an execute run. |
| `organize_files_automation_execute_approvals_expired_total` | Approvals that ran out of time before use. |
| `organize_files_automation_claim_conflicts_total` | Times another host already held the claim on the output root. |
| `organize_files_automation_runs_orphaned_total` | Runs recovered as orphans, left behind by a host that stopped. |
| `organize_files_automation_job_events_total` | One counter per event, with the labels `event`, `job_id`, `target` and `jobs_file`. |
| `organize_files_automation_webhook_posts_succeeded_total` | Webhook deliveries accepted. |
| `organize_files_automation_webhook_posts_failed_total` | Webhook deliveries refused or unreachable. |
| `organize_files_automation_webhook_dead_letter_depth` | Rows waiting in the webhook dead-letter file right now. |
| `organize_files_automation_log_retention_pruned_total` | Run logs removed by retention. |
| `organize_files_automation_runs_index_compacted_total` | Rows dropped from the run index during compaction. |
| `organize_files_automation_last_due_pass_exit_code` | Exit code of the most recent finished pass. `0` is a clean pass. |
| `organize_files_automation_last_due_pass_completed_utc` | Unix time in seconds of the most recent finished pass, and `0` before the first one. |

## Dashboard and alert rules

A ready-made Grafana dashboard is published with the deployment files as `grafana-organize-files-automation.json`, under the title **OrganizeFiles Automation**. Its ten panels show due passes, jobs started and failed, claim conflicts, job throughput over an hour, the last exit code, dead-letter depth, webhook failures over a day, jobs awaiting approval, and job events by state. Every panel names its data source through the placeholder `${DS_PROMETHEUS}`.

The matching alert rules are `alerts-organize-files-automation.yaml`, with `prometheus-rule-automation.yaml` as the Kubernetes wrapper for `kube-prometheus-stack`. A non-zero last exit code warns after five minutes, a license failure is critical after one, and the remaining rules cover failing jobs, claim conflicts, webhook failures, a dead-letter backlog and approvals left waiting for a day. Both files are validated on every build, so the names above stay in step with the counters.

# Run output and metrics

## Status row

The **Run output** area shows:

- Current app state and engine progress.
- **CPU** and two **memory** values for this process only.
- **GPU** lines, on Windows: this process's share of each graphics adapter, not the whole card.

The same compact resource bar is reused in secondary tool windows such as file exploration, scheduled jobs, and file repair.

## Memory labels

- **Private bytes / commit** — private virtual memory reserved by the process.
- **Working set / memory** — resident RAM currently held by this process. It can differ from another operating-system monitor because each OS and desktop environment labels process memory differently.

## Run heartbeat JSON (optional)

Enable **Write run heartbeat JSON** under **Advanced / Diagnostics**. The engine writes `Organize.Files.run.json` under `Output\_OrganizeMediaLogs` (same folder as the default organize resume file).

- **Path** — updated atomically during organize and repair runs.
- **Timing** — while scanning sources, the file is rewritten every 10,000 files seen, every 5,000 matches, and about every 15 seconds while the scan is still running, so a large network tree that is slow to list still shows that the run is alive. During validation, hashing and moves it is rewritten after every 1,000 files, and at most every 5 seconds. Start and end writes still happen when a run begins and finishes.
- **Progress** — while file counts are still growing, the main progress bar shows files seen so far instead of 100% until a phase has a known total.
- **Fields** — `schema`, `mode`, `phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`), `runState` (`active` / `completed` / `failed` / `cancelled`), `utc` (ISO-8601), `dryRun`, `outputRoot`, `validateMedia`, `deepVideoValidate`, `gpuDeviceCount`, `hwaccel`, optional `correlationId`, nested `progress` counters.
- **Log** — the run output panel prints the full path at start and when the file is saved at the end. Use **Open heartbeat log folder** / **Show heartbeat JSON file** under Advanced / Diagnostics.
- **CLI** — `--heartbeat-json` on OrganizeFiles.Cli. Cancel and fatal shell errors write `cancelled` / `failed` `runState` when enabled.
