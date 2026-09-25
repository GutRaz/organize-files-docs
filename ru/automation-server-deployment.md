# CLI, Docker и Kubernetes (эталонный макет)

## Автоматизация CLI

Эта глава выполнена в стиле Microsoft/HashiCorp: строка использования, таблица флагов (английские токены), затем примеры копирования и вставки.

Интерфейс командной строки (OrganizeFiles.Cli)
  ИСПОЛЬЗОВАНИЕ: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  ИСПОЛЬЗОВАНИЕ: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Флаг (длинный) | Значение
  -------------------------|----------------------------------------
  --execute | Реальные ходы (по умолчанию — только пробный прогон).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode/-m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | UTF-8 файл возобновления с B64| линии.
  --delete-duplicates | Удалите повторяющиеся кандидаты (требуется --confirm-delete и --execute).
  --delete-issues | Удалить кандидатов в корзину задач (требуется --confirm-delete и --execute). Не на удаленных объектах автоматизации.
  --archive-after-organize | После организации: ZIP-архив для каждого файла, затем удалите оригиналы (требуется --confirm-delete с --execute). Пропускает уже архивированные расширения.

  **Примечание.** CLI `--mode models` выбирает **модели CAD/3D**, а не артефакты искусственного интеллекта. Используйте `--mode ai` или `--mode models-ai` для AI/ML.

  Пример (пробный прогон, все категории): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Пример (только перемещения в Unique, выполнение): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Сборка: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Пробный прогон: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  Для --execute удалите :ro из исходного монтирования. См. containers/README.md для правил нескольких рабочих процессов (один выходной корень на каждого рабочего).

Kubernetes (справочное задание)
  Исходные PVC только для чтения действительны для пробных заданий. Для реальных действий с --execute необходимы записываемые исходные PVC. Предоставьте действительные права магазина или издателя для всех запусков организации/восстановления (пробный запуск и выполнение). Один модуль на каждое выходное дерево. Минимальный шаблон описан в containers/README.md вместе с образцом манифеста.

Ход выполнения заданий
  Окно заданий показывает ход выполнения для запусков App, CLI, Docker и Kubernetes. Этапы с известным итогом показывают процент. Сканирования без итога остаются неопределёнными.
  Автоматизация запускает рабочий процесс CLI с ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 и убирает эти строки меток из видимого журнала. Запуск CLI, сделанный вручную, не выдаёт меток, пока эта переменная не задана.
  Рабочие процессы Docker и Kubernetes получают ту же переменную, поэтому такие запуски тоже сообщают процент. Значение считывается из журнала рабочего процесса, поэтому оно появляется, как только контейнер или под начинает запись.
  --list-running и --show-run несут поля хода выполнения для активных заданий, когда запуск что-либо сообщил.

# Запуск примеров

## Графический интерфейс

Добавьте **Источники** и папку вывода, выберите режим запуска, включите **Пробный запуск** для предварительного просмотра, затем нажмите **Запуск**. Оставьте **Пробный запуск** выключенным для реального перемещения. Параметры удаления запрашивают подтверждение перед выполнением.

## Примеры CLI

CLI Пробный запуск: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
