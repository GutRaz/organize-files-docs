# 使用 Prometheus 和 Grafana 监控

## 计数器涵盖什么

预定作业保存着一小组 Prometheus 计数器和量表。每个名称都以 `organize_files_automation_` 开头，整组以 Prometheus 文本发布。运行作业的三个宿主发布同一组：桌面应用、`OrganizeFiles.JobAgent` 服务，以及在容器内使用的命令行宿主。

计数器描述的是调度器，不是文件。计入的是轮次、作业结果、批准、webhook 投递和历史清理。对于作业搬动的文件，不作任何计数。

## 导出到文件，不开放端口

`automation-metrics.prom` 写入自动化数据文件夹，位于 `automation-jobs.json` 旁边，并在每次到期轮次之后以及每次读取时刷新。其版式正是 `node_exporter` 的 textfile 采集器所读取的版式，因此已经运行 `node_exporter` 的机器无需监听端口、无需令牌、无需防火墙规则即被覆盖。文件以一次性方式替换，若原处留有符号链接，写入会就此停止，而不会顺着链接走。

## 抓取端点

只有当 `ORGANIZE_FILES_METRICS_HTTP_PORT` 中是 1 到 65535 之间的端口时，端点才存在。没有该变量就没有任何监听。

| 变量 | 作用 |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | 监听的端口。缺失或超出范围时，根本不会有端点。 |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | 监听地址。默认是 `127.0.0.1`。取值 `0.0.0.0`、`+` 和 `*` 表示所有地址，其他任何取值都退回 `127.0.0.1`。 |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | 在 `/metrics` 和 `/ready` 上要求的 bearer 令牌。 |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` 让 `/ready` 在没有该令牌时也能作答，供集群探测使用。此时宿主路径不出现在答复里。 |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | 以逗号分隔的退出码，遇到时 `/ready` 报告尚未就绪。取代内置清单。 |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` 忽略最近一次轮次的退出码，也忽略首次轮次尚未结束的状态。 |
| `ORGANIZE_FILES_READY_JSON` | `1` 在 `/ready` 上强制 JSON 正文，即便调用方要的是纯文本。 |

若未设置 bearer 令牌，回环之外的地址会在监听器打开之前被拒绝。拒绝会写入错误输出，并作为 webhook 事件发出，因为那种组合会把计数器交给整个网络。

## 提供的路径

- `/metrics` — 以 Prometheus 文本呈现的计数器。对 `/` 的请求返回同样的内容。
- `/ready` — 面向编排器的就绪状态。当自动化文件夹接受试写、作业文件可以打开、历史文件夹解析在数据根目录之内，且最近一次到期轮次以不构成阻挡的退出码结束时，答复为 `200`。否则答复为 `503`，并附上简短原因，例如 `due_pass_not_completed` 或 `last_due_pass_license_failed`。
- `/health` — 只是存活信号。即便设置了令牌，该路径依然匿名，因为它只回答 `ok`，别无其他。

退出码 `3` 表示许可失败，`8` 表示输出树被锁，`10` 表示删除从未被确认，`11` 表示占用冲突，默认情况下它们都会阻挡就绪。除非调用方发送 `Accept: text/plain` 或追加 `?format=text`，否则 `/ready` 的正文是 JSON。

## 计数器一览

| 名称 | 内容 |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | 调度器开始的到期轮次。 |
| `organize_files_automation_jobs_started_total` | 进入运行状态的作业执行。 |
| `organize_files_automation_jobs_skipped_total` | 被跳过的作业：Docker 或 Kubernetes 环境尚未就绪、在无屏幕宿主上指向应用的作业、输出根目录被占用，或者被编排器拒绝的作业。 |
| `organize_files_automation_jobs_failed_total` | 以失败告终的作业执行。 |
| `organize_files_automation_jobs_awaiting_approval_total` | 为等待批准而搁置的真实执行。 |
| `organize_files_automation_execute_approvals_total` | 为真实执行授予的批准。 |
| `organize_files_automation_execute_approvals_expired_total` | 在使用前已过期的批准。 |
| `organize_files_automation_claim_conflicts_total` | 另一宿主已经持有输出根目录占用权的次数。 |
| `organize_files_automation_runs_orphaned_total` | 作为孤儿被回收的执行，由停止的宿主遗留。 |
| `organize_files_automation_job_events_total` | 每个事件一个计数器，带有 `event`、`job_id`、`target` 和 `jobs_file` 标签。 |
| `organize_files_automation_webhook_posts_succeeded_total` | 已被接受的 webhook 投递。 |
| `organize_files_automation_webhook_posts_failed_total` | 被拒绝或无法抵达的 webhook 投递。 |
| `organize_files_automation_webhook_dead_letter_depth` | 此刻在未投递 webhook 文件中等待的行数。 |
| `organize_files_automation_log_retention_pruned_total` | 被保留策略移除的运行日志。 |
| `organize_files_automation_runs_index_compacted_total` | 压实时从运行索引中剔除的行。 |
| `organize_files_automation_last_due_pass_exit_code` | 最近一次结束的轮次的退出码。`0` 表示干净的一轮。 |
| `organize_files_automation_last_due_pass_completed_utc` | 最近一次结束的轮次的 Unix 时间（秒），首轮之前为 `0`。 |

## 仪表板与告警规则

现成的 Grafana 仪表板随部署文件一同发布，文件名为 `grafana-organize-files-automation.json`，标题为 **OrganizeFiles Automation**。它的十个面板显示到期轮次、已启动与失败的作业、占用冲突、一小时内的作业吞吐、最近一次退出码、未投递深度、一天内的 webhook 失败、等待批准的作业，以及按状态划分的作业事件。每个面板都通过占位符 `${DS_PROMETHEUS}` 指明自己的数据源。

与之配套的告警规则是 `alerts-organize-files-automation.yaml`，`prometheus-rule-automation.yaml` 则是给 `kube-prometheus-stack` 用的 Kubernetes 外壳。最近一次退出码不为零会在五分钟后告警，许可失败在一分钟后升为严重，其余规则涵盖失败的作业、占用冲突、webhook 失败、未投递积压，以及搁置一天的批准。两个文件在每次构建时都会校验，因此上面的名称与计数器保持同步。

# 运行输出和指标

## 状态行

**运行输出**区域显示：

- 当前应用程序状态和引擎进度。
- **CPU** 和两个 **内存** 值仅适用于此进程。
- **GPU** 行（Windows）：本进程在每块显卡上占用的份额，而不是整块显卡。

相同的紧凑资源栏可在辅助工具窗口中重复使用，例如文件浏览、计划作业和文件修复。

## 内存标签

- **私有字节/提交** — 进程保留的私有虚拟内存。
- **工作集/内存** — 该进程当前持有的驻留 RAM。它可能与其他操作系统监视器不同，因为每个操作系统和桌面环境对进程内存的标记不同。

## 运行心跳 JSON（可选）

在**高级/诊断**下启用**写入运行心跳 JSON**。引擎将`Organize.Files.run.json`写入`Output\_OrganizeMediaLogs`下（与默认整理恢复状态文件相同的文件夹）。

- **路径** — 在整理和修复运行期间自动更新。
- **写入间隔** — 扫描来源期间，文件每看到 10,000 个文件、每匹配 5,000 项重写一次，扫描仍在进行时还会大约每 15 秒重写一次，因此列出缓慢的大型网络目录树也能显示运行仍在进行。校验、哈希与移动期间每处理 1,000 个文件重写一次，最多每 5 秒一次。开始与结束时的写入依旧在运行开始和结束时发生。
- **进度** — 只要文件计数仍在增长，主进度条显示的就是迄今看到的文件数而非 100%，直到某个阶段有了已知的总数为止。
- **字段** — `schema`、`mode`、`phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`)、`runState` (`active` / `completed` / `failed` / `cancelled`)、`utc` (ISO-8601)、`dryRun`、`outputRoot`、`validateMedia`、`deepVideoValidate`、`gpuDeviceCount`, `hwaccel`，可选`correlationId`，嵌套`progress`计数器。
- **日志** — 运行输出面板在开始时和最后保存文件时打印完整路径。使用“高级/诊断”下的 **打开心跳日志文件夹** / **显示心跳 JSON 文件**。
- **CLI** — OrganizeFiles.Cli 上的`--heartbeat-json`。启用时，取消和致命 shell 错误会写入 `cancelled` / `failed` `runState`。
