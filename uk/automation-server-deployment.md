# CLI, Docker і Kubernetes (еталонний макет)

## Автоматизація CLI

Цей розділ дотримується стилю Microsoft/HashiCorp: рядок використання, таблиця прапорів (англійські маркери), потім копіювання та вставлення прикладів.

CLI (OrganizeFiles.Cli)
  ВИКОРИСТАННЯ: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  ВИКОРИСТАННЯ: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Прапор (довгий) | Значення
  ------------------------|----------------------------------------
  --execute | Справжні ходи (за замовчуванням лише пробний запуск).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | UTF-8 файл відновлення з B64| лінії.
  --delete-duplicates | Видаліть повторювані кандидати (потрібно --confirm-delete із --execute).
  --delete-issues | Видалити кандидатів у сегмент випуску (потрібно --confirm-delete із --execute). Не на віддалених цілях автоматизації.
  --archive-after-organize | Після впорядкування: по-файловий однорідний ZIP потім видаліть оригінали (потрібно --confirm-delete із --execute). Пропускає вже заархівовані розширення.

  **Примітка.** CLI `--mode models` вибирає **CAD/3D-моделі**, а не артефакти AI. Використовуйте `--mode ai` або `--mode models-ai` для AI / ML.

  Приклад (пробний запуск, усі ковші): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Приклад (тільки унікальні ходи, виконати): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Збірка: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Пробний запуск: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  Для --execute видаліть :ro з вихідного кріплення. Див. containers/README.md для кількох робочих правил (один вихідний корінь на робочого).

Kubernetes (довідкова робота)
  Вихідні PVCs, доступні лише для читання, дійсні для робіт із пробного запуску. Реальні рухи з --execute потребують записуваних вихідних PVC. Надайте дійсне дозвіл магазину або видавця для всіх запусків організації/відновлення (пробний запуск і виконання). Один Pod на вихідне дерево. Мінімальний шаблон задокументовано в containers/README.md разом із зразком маніфесту.

Перебіг завдань
  Вікно завдань показує перебіг для запусків App, CLI, Docker і Kubernetes. Етапи з відомим підсумком показують відсоток. Сканування без підсумку лишаються невизначеними.
  Автоматизація запускає робочий процес CLI з ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 і прибирає ті рядки позначок з видимого журналу. Запуск CLI, зроблений вручну, не видає позначок, доки ця змінна не задана.
  Робочі процеси Docker і Kubernetes отримують ту саму змінну, тому такі запуски теж повідомляють відсоток. Значення читається з журналу робочого процесу, тому воно з'являється, щойно контейнер або под починає запис.
  --list-running і --show-run несуть поля перебігу для активних завдань, коли запуск щось повідомив.

# Приклади запуску

## Графічний UI

Додайте **Джерела** і папку виводу, виберіть режим запуску, увімкніть **Пробний запуск** для попереднього перегляду, а потім натисніть **Запустити**. Залиште **Пробний запуск** вимкненим для реального переміщення. Параметри видалення запитують підтвердження перед виконанням.

## Приклади CLI

CLI Пробний запуск: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
