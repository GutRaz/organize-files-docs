# CLI, Docker, and Kubernetes (reference layout)

## CLI automation

This chapter follows the Microsoft/HashiCorp style: usage line, flag table (English tokens), then copy-paste examples.

CLI (OrganizeFiles.Cli)
  USAGE: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  USAGE: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Flag (long)              | Meaning
  -------------------------|----------------------------------------
  --execute                | Real moves (default is dry-run only).
  --move-scope <token>     | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name>       | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file>          | UTF-8 resume file with B64| lines.
  --delete-duplicates      | Delete duplicate candidates (needs --confirm-delete with --execute).
  --delete-issues          | Delete issue-bucket candidates (needs --confirm-delete with --execute). Not on remote automation targets.
  --archive-after-organize | After organize: per-file sibling ZIP then delete originals (needs --confirm-delete with --execute). Skips already-archive extensions.

  **Note:** CLI `--mode models` selects **CAD / 3D models**, not AI artifacts. Use `--mode ai` or `--mode models-ai` for AI / ML.

  Example (dry-run, all buckets): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Example (only Unique moves, execute): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Build: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Dry-run: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  For --execute, remove :ro from the source mount. See containers/README.md for multi-worker rules (one output root per worker).

Kubernetes (reference Job)
  Read-only source PVCs are valid for dry-run jobs. Real moves with --execute need writable source PVCs. Provide valid store or publisher entitlement for all organize/repair runs (dry-run and execute). One Pod per output tree. A minimal pattern is documented in containers/README.md alongside a sample manifest.

Job progress
  The Jobs window reports progress for App, CLI, Docker and Kubernetes runs. Stages with a known total show a percentage. Scans without a total stay indeterminate.
  Automation starts the CLI worker with ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 and strips those marker lines from the visible log. A CLI run started by hand emits no markers unless that variable is set.
  Docker and Kubernetes workers receive the same variable, so those runs report a percentage as well. The figure is read out of the worker's log, so it starts once the container or the pod starts writing.
  --list-running and --show-run carry progress fields for active jobs when the run has reported any.

# Run examples

## Graphical UI

Add **Sources**, **Output**, run mode, optional **Planned moves** (defaults to all buckets), **Dry run** for preview, extensions, then **Run**. Leave **Dry run** clear for real moves. Delete checkboxes require confirmation on execute.

## CLI examples

CLI dry-run (media, Unique + problematic files only): OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker dry run: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
