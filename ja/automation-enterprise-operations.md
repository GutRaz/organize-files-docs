# Prometheus と Grafana による監視

## カウンターが扱う範囲

スケジュールされたジョブは、Prometheus のカウンターとゲージを少数保持します。名前はすべて `organize_files_automation_` で始まり、一式が Prometheus のテキストとして公開されます。ジョブを実行する三つのホストはいずれも同じ一式を公開します。デスクトップアプリケーション、`OrganizeFiles.JobAgent` サービス、そしてコンテナ内で使うコマンドライン ホストです。

カウンターが表すのはスケジューラーであってファイルではありません。数えられるのは巡回、ジョブの結果、承認、webhook の配信、履歴の整理です。ジョブが動かすファイルについては何も数えません。

## ポートを開かずにファイルへ書き出す

`automation-metrics.prom` は自動化データフォルダーの `automation-jobs.json` の隣に書かれ、期限の来た巡回ごとと読み取りのたびに更新されます。書式は `node_exporter` の textfile コレクターが読むものなので、すでに `node_exporter` が動いている機械は、待ち受けポートもトークンもファイアウォール規則もなしで対象になります。ファイルは不可分に置き換えられ、その場所に置かれた記号リンクは、たどられる代わりに書き込みを止めます。

## 読み取りの受け口

受け口が存在するのは `ORGANIZE_FILES_METRICS_HTTP_PORT` が 1 から 65535 までのポートを保持しているときだけです。その変数がなければ何も待ち受けません。

| 変数 | 働き |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | 待ち受けるポート。無い場合や範囲外の場合、受け口はまったく作られません。 |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | 待ち受けアドレス。既定は `127.0.0.1` です。値 `0.0.0.0`、`+`、`*` はすべてのアドレスを表し、それ以外は `127.0.0.1` に戻ります。 |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | `/metrics` と `/ready` で求められる bearer トークン。 |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` はクラスターの検査のために `/ready` がそのトークンなしで答えることを許します。そのときホストのパスは答えから省かれます。 |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | `/ready` が未準備と報告する終了コードをコンマ区切りで指定します。組み込みの一覧を置き換えます。 |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` は直近の巡回の終了コードを無視し、最初の巡回が終わる前の状態も無視します。 |
| `ORGANIZE_FILES_READY_JSON` | `1` は平文を求めた呼び出し元に対しても `/ready` で JSON の本文を強制します。 |

ループバック以外のアドレスは、bearer トークンが設定されていなければ待ち受けを開く前に拒まれます。拒否はエラー出力に書かれ、webhook のイベントとしても送られます。その組み合わせはカウンターをネットワーク全体に渡してしまうからです。

## 提供されるパス

- `/metrics` — Prometheus テキストとしてのカウンター。`/` への要求は同じ内容を返します。
- `/ready` — オーケストレーター向けの準備状態。自動化フォルダーが試し書きを受け入れ、ジョブファイルが開き、履歴フォルダーがデータ ルートの内側に解決し、期限の来た直近の巡回が妨げにならない終了コードで終わっていれば、答えは `200` です。そうでなければ答えは `503` で、`due_pass_not_completed` や `last_due_pass_license_failed` のような短い理由が付きます。
- `/health` — 生存の合図だけです。トークンが設定されていてもこのパスは無名のままです。答えるのは `ok` だけだからです。

終了コード `3` はライセンスの失敗、`8` は施錠された出力ツリー、`10` は確認されなかった削除、`11` は要求の衝突を表し、既定では準備状態を妨げます。`/ready` の本文は、呼び出し元が `Accept: text/plain` を送るか `?format=text` を付けない限り JSON です。

## カウンター一覧

| 名前 | 内容 |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | スケジューラーが始めた、期限の来た巡回。 |
| `organize_files_automation_jobs_started_total` | 実行中の状態に達したジョブの実行。 |
| `organize_files_automation_jobs_skipped_total` | 飛ばされたジョブ。Docker や Kubernetes の環境が整っていない、画面のないホストでアプリを対象にしている、出力ルートが使用中、またはオーケストレーターが断った場合です。 |
| `organize_files_automation_jobs_failed_total` | 失敗で終わったジョブの実行。 |
| `organize_files_automation_jobs_awaiting_approval_total` | 承認待ちで止められた本番の実行。 |
| `organize_files_automation_execute_approvals_total` | 本番の実行に与えられた承認。 |
| `organize_files_automation_execute_approvals_expired_total` | 使われる前に期限が切れた承認。 |
| `organize_files_automation_claim_conflicts_total` | 別のホストが出力ルートの要求をすでに握っていた回数。 |
| `organize_files_automation_runs_orphaned_total` | 停止したホストが残し、孤立として回収された実行。 |
| `organize_files_automation_job_events_total` | 事象ごとに一つのカウンター。ラベルは `event`、`job_id`、`target`、`jobs_file` です。 |
| `organize_files_automation_webhook_posts_succeeded_total` | 受け入れられた webhook の配信。 |
| `organize_files_automation_webhook_posts_failed_total` | 断られた、または届かなかった webhook の配信。 |
| `organize_files_automation_webhook_dead_letter_depth` | 未配信 webhook のファイルで今この時点で待っている行。 |
| `organize_files_automation_log_retention_pruned_total` | 保存期間の規則が消した実行ログ。 |
| `organize_files_automation_runs_index_compacted_total` | 圧縮のときに実行の索引から外れた行。 |
| `organize_files_automation_last_due_pass_exit_code` | 直近に終わった巡回の終了コード。`0` はきれいな巡回です。 |
| `organize_files_automation_last_due_pass_completed_utc` | 直近に終わった巡回の Unix 時刻（秒）。最初の巡回の前は `0` です。 |

## ダッシュボードと警告規則

出来合いの Grafana ダッシュボードが、配備用ファイルとともに `grafana-organize-files-automation.json` という名前で、**OrganizeFiles Automation** という表題で公開されています。十枚のパネルが、期限の来た巡回、開始したジョブと失敗したジョブ、要求の衝突、一時間あたりのジョブ処理量、直近の終了コード、未配信の深さ、一日あたりの webhook 失敗、承認待ちのジョブ、状態別のジョブ事象を示します。どのパネルも `${DS_PROMETHEUS}` という差し込み名でデータソースを指します。

対応する警告規則は `alerts-organize-files-automation.yaml` にあり、`prometheus-rule-automation.yaml` は `kube-prometheus-stack` 向けの Kubernetes の包みです。直近の終了コードが零でなければ五分後に警告し、ライセンスの失敗は一分後に重大となり、残りの規則は失敗したジョブ、要求の衝突、webhook の失敗、未配信の滞留、一日置かれたままの承認を扱います。どちらのファイルもビルドのたびに検証されるので、上の名前はカウンターと歩調を合わせたままです。

# 実行出力とメトリクス

## ステータス行

**実行出力** 領域には次が表示されます。

- 現在のアプリの状態とエンジンの進行状況。
- このプロセスのみの **CPU** と 2 つの **メモリ** 値。
- **GPU** の行 (Windows): 各グラフィックス アダプターのうちこのプロセスが使った分で、カード全体ではありません。

同じコンパクトなリソース バーは、ファイル探索、スケジュールされたジョブ、ファイル修復などの二次ツール ウィンドウで再利用されます。

## メモリラベル

- **プライベート バイト / コミット** — プロセスによって予約されたプライベート仮想メモリ。
- **ワーキング セット / メモリ** — このプロセスが現在保持している常駐 RAM。 OS およびデスクトップ環境ごとにメモリの処理ラベルが異なるため、別のオペレーティング システム モニタとは異なる場合があります。

## ハートビート JSON を実行する (オプション)

**詳細設定/診断**で**実行ハートビートJSONの書き込み**を有効にします。エンジンは `Output\_OrganizeMediaLogs` の下に `Organize.Files.run.json` を書き込みます (デフォルトの整理再開ファイルと同じフォルダー)。

- **パス** — 整理および修復の実行中にアトミックに更新されます。
- **書き出しの間隔** — 情報源を走査している間、ファイルは見たファイル一万件ごと、一致五千件ごと、そして走査が続く間はおよそ十五秒ごとに書き直されます。そのため、一覧の取得が遅い大きなネットワーク上の木でも、実行が動いていることがわかります。検証・ハッシュ計算・移動の間は千件ごとに書き直され、その間隔は最短でも五秒です。実行の始めと終わりの書き出しは、これまでどおり行われます。
- **進み具合** — ファイル数がまだ増えている間、主な進み具合の帯は百パーセントではなく、これまでに見たファイル数を示します。その段階の総数が分かるまでそのままです。
- **フィールド** — `schema`、`mode`、`phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`)、`runState` (`active` / `completed` / `failed` / `cancelled`)、`utc` (ISO-8601)、`dryRun`、`outputRoot`、`validateMedia`、`deepVideoValidate`、`gpuDeviceCount`, `hwaccel`、オプション`correlationId`、ネストされた `progress` カウンター。
- **ログ** — 実行出力パネルは、開始時とファイルの終了時の保存時のフル パスを出力します。 [詳細設定] / [診断] で、**ハートビート ログ フォルダーを開く** / **ハートビート JSON ファイルを表示** を使用します。
- **CLI** — OrganizeFiles.Cli の`--heartbeat-json`。キャンセルおよび致命的なシェル エラーは、有効な場合、`cancelled` / `failed` `runState` を書き込みます。
