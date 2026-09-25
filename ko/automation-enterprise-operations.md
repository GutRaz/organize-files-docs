# Prometheus 및 Grafana 모니터링

## 카운터가 다루는 범위

예약된 작업은 Prometheus 카운터와 게이지를 적은 수로 유지합니다. 모든 이름은 `organize_files_automation_` 으로 시작하며, 전체 묶음은 Prometheus 텍스트로 게시됩니다. 작업을 실행하는 세 호스트 모두 같은 묶음을 게시합니다. 데스크톱 응용 프로그램, `OrganizeFiles.JobAgent` 서비스, 그리고 컨테이너 안에서 쓰는 명령줄 호스트입니다.

카운터가 설명하는 것은 예약기이지 파일이 아닙니다. 순회, 작업 결과, 승인, webhook 전달, 기록 정리가 집계됩니다. 작업이 옮기는 파일에 대해서는 아무것도 집계하지 않습니다.

## 포트를 열지 않고 파일로 내보내기

`automation-metrics.prom` 은 자동화 데이터 폴더에서 `automation-jobs.json` 옆에 기록되며, 기한이 된 순회마다 그리고 읽어 갈 때마다 새로 쓰입니다. 형식은 `node_exporter` 의 textfile 수집기가 읽는 그 형식이라, `node_exporter` 를 이미 돌리는 기계는 듣고 있는 포트도, 토큰도, 방화벽 규칙도 없이 포함됩니다. 파일은 한 번에 통째로 교체되며, 그 자리에 남겨 둔 기호 연결은 따라가지 않고 쓰기를 멈춥니다.

## 수집 지점

수집 지점은 `ORGANIZE_FILES_METRICS_HTTP_PORT` 가 1 에서 65535 사이의 포트를 담고 있을 때에만 존재합니다. 그 변수가 없으면 아무것도 듣지 않습니다.

| 변수 | 효과 |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | 듣게 될 포트. 없거나 범위를 벗어나면 수집 지점은 아예 없습니다. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | 듣는 주소. 기본값은 `127.0.0.1` 입니다. 값 `0.0.0.0`, `+`, `*` 는 모든 주소를 뜻하고, 그 밖의 값은 `127.0.0.1` 로 되돌아갑니다. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | `/metrics` 와 `/ready` 에서 요구하는 bearer 토큰. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` 은 클러스터 점검을 위해 `/ready` 가 그 토큰 없이 답하도록 둡니다. 그때 호스트 경로는 답에서 빠집니다. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | `/ready` 가 준비되지 않음으로 알리게 하는 종료 코드를 쉼표로 나열합니다. 내장 목록을 대신합니다. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` 은 마지막 순회의 종료 코드를 무시하고, 첫 순회가 끝나기 전 상태도 무시합니다. |
| `ORGANIZE_FILES_READY_JSON` | `1` 은 일반 텍스트를 요청한 호출자에게도 `/ready` 에서 JSON 본문을 강제합니다. |

루프백 밖의 주소는 bearer 토큰이 설정되지 않았다면 수신기를 열기 전에 거절됩니다. 거절은 오류 출력에 기록되고 webhook 사건으로도 전송됩니다. 그 조합은 카운터를 네트워크 전체에 넘겨주기 때문입니다.

## 제공되는 경로

- `/metrics` — Prometheus 텍스트 형태의 카운터. `/` 로 보낸 요청도 같은 내용을 돌려줍니다.
- `/ready` — 오케스트레이터를 위한 준비 상태. 자동화 폴더가 시험 쓰기를 받아들이고, 작업 파일이 열리고, 기록 폴더가 데이터 뿌리 안에서 풀리고, 기한이 된 마지막 순회가 가로막지 않는 종료 코드로 끝났다면 답은 `200` 입니다. 그렇지 않으면 답은 `503` 이며 `due_pass_not_completed` 나 `last_due_pass_license_failed` 같은 짧은 사유가 붙습니다.
- `/health` — 살아 있다는 신호뿐입니다. 토큰이 설정되어 있어도 이 경로는 익명으로 남습니다. `ok` 만 답하고 그 밖의 것은 담지 않기 때문입니다.

종료 코드 `3` 은 라이선스 실패, `8` 은 잠긴 출력 트리, `10` 은 확인되지 않은 삭제, `11` 은 점유 충돌을 뜻하며 기본적으로 준비 상태를 막습니다. `/ready` 본문은 호출자가 `Accept: text/plain` 을 보내거나 `?format=text` 를 덧붙이지 않는 한 JSON 입니다.

## 카운터 목록

| 이름 | 내용 |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | 예약기가 시작한, 기한이 된 순회. |
| `organize_files_automation_jobs_started_total` | 실행 중 상태에 이른 작업 수행. |
| `organize_files_automation_jobs_skipped_total` | 건너뛴 작업. Docker 나 Kubernetes 환경이 준비되지 않았거나, 화면 없는 호스트에서 응용 프로그램을 겨냥했거나, 출력 뿌리가 쓰이는 중이거나, 오케스트레이터가 거절한 경우입니다. |
| `organize_files_automation_jobs_failed_total` | 실패로 끝난 작업 수행. |
| `organize_files_automation_jobs_awaiting_approval_total` | 승인을 기다리며 세워 둔 실제 수행. |
| `organize_files_automation_execute_approvals_total` | 실제 수행에 내준 승인. |
| `organize_files_automation_execute_approvals_expired_total` | 쓰이기 전에 기한이 지난 승인. |
| `organize_files_automation_claim_conflicts_total` | 다른 호스트가 출력 뿌리의 점유를 이미 쥐고 있던 횟수. |
| `organize_files_automation_runs_orphaned_total` | 멈춘 호스트가 남겨, 고아로 되찾은 수행. |
| `organize_files_automation_job_events_total` | 사건마다 카운터 하나. 라벨은 `event`, `job_id`, `target`, `jobs_file` 입니다. |
| `organize_files_automation_webhook_posts_succeeded_total` | 받아들여진 webhook 전달. |
| `organize_files_automation_webhook_posts_failed_total` | 거절되었거나 닿지 못한 webhook 전달. |
| `organize_files_automation_webhook_dead_letter_depth` | 전달되지 못한 webhook 파일에서 지금 기다리는 줄. |
| `organize_files_automation_log_retention_pruned_total` | 보관 기간 규칙이 지운 수행 기록. |
| `organize_files_automation_runs_index_compacted_total` | 압축할 때 수행 색인에서 빠진 줄. |
| `organize_files_automation_last_due_pass_exit_code` | 가장 최근에 끝난 순회의 종료 코드. `0` 은 깨끗한 순회입니다. |
| `organize_files_automation_last_due_pass_completed_utc` | 가장 최근에 끝난 순회의 Unix 시각(초). 첫 순회 전에는 `0` 입니다. |

## 대시보드와 경보 규칙

이미 만들어진 Grafana 대시보드가 배포 파일과 함께 `grafana-organize-files-automation.json` 이라는 이름으로, **OrganizeFiles Automation** 이라는 제목 아래 게시됩니다. 열 개의 판은 기한이 된 순회, 시작된 작업과 실패한 작업, 점유 충돌, 한 시간 동안의 작업 처리량, 마지막 종료 코드, 미전달 깊이, 하루 동안의 webhook 실패, 승인을 기다리는 작업, 상태별 작업 사건을 보여 줍니다. 모든 판은 `${DS_PROMETHEUS}` 자리 표시자로 데이터 원본을 가리킵니다.

짝이 되는 경보 규칙은 `alerts-organize-files-automation.yaml` 이며, `prometheus-rule-automation.yaml` 은 `kube-prometheus-stack` 을 위한 Kubernetes 껍데기입니다. 마지막 종료 코드가 영이 아니면 오 분 뒤에 경고하고, 라이선스 실패는 일 분 뒤 심각으로 오르며, 나머지 규칙은 실패한 작업, 점유 충돌, webhook 실패, 미전달 적체, 하루 동안 기다린 승인을 다룹니다. 두 파일 모두 빌드마다 검증되므로 위의 이름은 카운터와 발을 맞춥니다.

# 실행 출력 및 측정항목

## 상태 행

**실행 출력** 영역에는 다음이 표시됩니다.

- 현재 앱 상태와 엔진 진행 상황.
- 이 프로세스에만 **CPU** 및 두 개의 **메모리** 값이 있습니다.
- **GPU** 줄(Windows): 각 그래픽 어댑터에서 이 프로세스가 차지한 몫이며 카드 전체가 아닙니다.

파일 탐색, 예약된 작업 및 파일 복구와 같은 보조 도구 창에서 동일한 압축 리소스 표시줄이 재사용됩니다.

## 메모리 라벨

- **전용 바이트/커밋** — 프로세스에서 예약한 전용 가상 메모리입니다.
- **작업 세트/메모리** — 현재 이 프로세스가 보유하고 있는 상주 RAM입니다. 각 OS 및 데스크탑 환경 레이블은 메모리를 다르게 처리하므로 다른 운영 체제 모니터와 다를 수 있습니다.

## 하트비트 JSON 실행(선택 사항)

**고급/진단**에서 **쓰기 실행 하트비트 JSON**을 활성화합니다. 엔진은 `Output\_OrganizeMediaLogs` 아래에 `Organize.Files.run.json`를 씁니다(기본 정리 재개 상태 파일과 동일한 폴더).

- **경로** — 정리 및 복구 실행 중에 원자적으로 업데이트됩니다.
- **기록 간격** — 출처를 훑는 동안 파일은 본 파일 1만 개마다, 일치 5천 건마다, 그리고 훑기가 계속되는 동안 약 15초마다 다시 쓰이므로, 목록을 느리게 읽는 큰 네트워크 트리에서도 실행이 살아 있음을 보여 줍니다. 검증과 해싱, 이동 중에는 파일 1천 개마다 다시 쓰이며, 많아야 5초에 한 번입니다. 실행이 시작될 때와 끝날 때의 기록은 여전히 이루어집니다.
- **진행** — 파일 수가 아직 늘고 있는 동안 주 진행 막대는 100%가 아니라 지금까지 본 파일 수를 보여 주며, 그 단계의 총수가 알려질 때까지 그렇습니다.
- **필드** — `schema`, `mode`, `phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`), `runState` (`active` / `completed` / `failed` / `cancelled`), `utc`(ISO-8601), `dryRun`, `outputRoot`, `validateMedia`, `deepVideoValidate`, `gpuDeviceCount`, `hwaccel`, 선택 사항 `correlationId`, 중첩된 `progress` 카운터.
- **로그** — 실행 출력 패널은 시작 시 전체 경로를 인쇄하고 파일이 마지막에 저장될 때를 인쇄합니다. 고급/진단에서 **하트비트 로그 폴더 열기** / **하트비트 JSON 파일 표시**를 사용하세요.
- **CLI** — OrganizeFiles.Cli의 `--heartbeat-json`. 취소 및 치명적인 쉘 오류가 활성화되면 `cancelled` / `failed` `runState`를 씁니다.
