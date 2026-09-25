# CLI、Docker 和 Kubernetes（参考布局）

## CLI 自动化

本章遵循 Microsoft/HashiCorp 风格：使用行、标志表（英语标记），然后复制粘贴示例。

命令行界面 (OrganizeFiles.Cli)
  用途：OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  用途：OrganizeFiles.Cli --output <dir> --mode repair [options]

  旗帜（长）|含义
  ----------------------------------|----------------------------------------
  --execute |真实动作（默认仅是空跑）。
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | UTF-8 恢复状态文件与 B64|线。
  --delete-duplicates |删除重复的候选者（需要 --confirm-delete 和 --execute ）。
  --delete-issues |删除候选问题桶（需要 --confirm-delete 和 --execute ）。不适用于远程自动化目标。
  --archive-after-organize |整理后：每个文件同级 ZIP，然后删除原始文件（需要 --confirm-delete 和 --execute ）。跳过已经存档的扩展。

  **注意：** CLI `--mode models` 选择 **CAD / 3D 模型**，而不是 AI 工件。使用`--mode ai`或`--mode models-ai`进行 AI/ML。

  示例（试运行，所有存储桶）：OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  示例（仅唯一移动，执行）：OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  构建：docker build -f containers/Dockerfile -t organize-files-cli:latest .
  试运行：docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  对于 --execute ，从源安装中删除 :ro。请参阅 containers/README.md 了解多工作器规则（每个工作器一个输出根）。

Kubernetes（参考作业）
  只读源 PVC 对于试运行作业有效。 --execute 的实际移动需要可写源 PVC。为所有整理/修复运行（试运行和执行）提供有效的商店或发布者权利。每个输出树一个 Pod。 containers/README.md 中记录了最小模式以及示例清单。

作业进度
  作业窗口为 App、CLI、Docker 与 Kubernetes 运行显示进度。总数已知的阶段显示百分比。没有总数的扫描保持不确定。
  自动化以 ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 启动 CLI 工作进程，并从可见日志中去掉那些标记行。手动启动的 CLI 运行不会发出标记，除非设置了该变量。
  Docker 与 Kubernetes 工作进程也会收到该变量，因此这些运行同样报告百分比。该数值从工作进程的日志中读取，因此容器或 Pod 开始写入时才会出现。
  --list-running 与 --show-run 在运行报告过内容时，为活动作业带有进度字段。

# 运行示例

## 图形用户界面

添加 **来源** 和输出文件夹，选择运行模式，勾选 **试运行** 以进行预览，然后按 **运行**。执行实际移动时保持 **试运行** 关闭。删除选项在执行前会请求确认。

## CLI 示例

CLI 试运行: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
