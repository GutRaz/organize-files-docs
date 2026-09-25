# CLI、Docker、および Kubernetes (参照レイアウト)

## CLI の自動化

この章は Microsoft/HashiCorp スタイルに従っています。つまり、使用行、フラグ テーブル (英語のトークン)、その後のコピーと貼り付けの例です。

CLI (OrganizeFiles.Cli）
  使用法： OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  使用法： OrganizeFiles.Cli --output <dir> --mode repair [options]

  旗（長） |意味
  ------------------------|--------------------------------------------
  --execute                |実際の動き (デフォルトはドライランのみ)。
  --move-scope <token>     | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name>       | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file>          | UTF-8 B64 でファイルを再開|線。
  --delete-duplicates      |重複した候補を削除します (--confirm-delete と --execute が必要です)。
  --delete-issues          |課題バケット候補の削除（必要な --confirm-delete と --execute ）。リモート自動化ターゲットではありません。
  --archive-after-organize |整理後: ファイルごとに兄弟 ZIP を作成し、元のファイルを削除します (必要 --confirm-delete と --execute ）。すでにアーカイブされている拡張機能はスキップします。

  **注意:** CLI `--mode models` AI アーティファクトではなく **CAD/3D モデル**を選択します。 AI / ML には `--mode ai` または `--mode models-ai` を使用してください。

  例 (ドライラン、すべてのバケット): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  例 (ユニークな動きのみ、実行): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  ビルド: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  ドライラン: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  のために --execute 、ソースマウントから:roを削除します。見る containers/README.md マルチワーカー ルールの場合 (ワーカーごとに 1 つの出力ルート)。

Kubernetes (参照ジョブ)
  読み取り専用ソース PVC はドライラン ジョブに有効です。実際の動き --execute 書き込み可能なソース PVC が必要です。すべての整理/修復実行 (ドライランと実行) に対して有効なストアまたは発行者の権利を提供します。出力ツリーごとに 1 つのポッド。最小限のパターンが文書化されています。 containers/README.md サンプルマニフェストと一緒に。

ジョブの進行状況
  ジョブ ウィンドウは App、CLI、Docker、Kubernetes の実行について進行状況を表示します。合計が分かっている段階は百分率を表示します。合計のないスキャンは不定のままです。
  自動化は ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 を付けて CLI ワーカーを起動し、その目印の行を見える記録から取り除きます。手で起動した CLI 実行は、その変数が設定されていない限り目印を出しません。
  Docker と Kubernetes のワーカーも同じ変数を受け取るため、それらの実行も百分率を示します。この数値はワーカーのログから読み取られるため、コンテナーまたはポッドが書き込みを始めた時点で表示されます。
  --list-running と --show-run は、実行が何かを報告している場合に、動作中のジョブの進行状況の欄を持ちます。

# 実行例

## グラフィカル UI

**ソース** と出力フォルダーを追加し、実行モードを選び、プレビューのために **ドライラン** をオンにしてから **実行** を押します。実際に移動するには **ドライラン** をオフのままにします。削除オプションは実行前に確認を求めます。

## CLI の例

CLI ドライラン: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
