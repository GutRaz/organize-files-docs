# CLI, Docker a Kubernetes (referenční rozvržení)

## Automatizace CLI

Tato kapitola se řídí stylem Microsoft/HashiCorp: řádek použití, tabulka příznaků (anglické tokeny), potom příklady kopírování a vkládání.

CLI (OrganizeFiles.Cli)
  POUŽITÍ: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  POUŽITÍ: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Vlajka (dlouhá) | Význam
  -------------------------|----------------------------------------
  --execute | Skutečné pohyby (výchozí je pouze běh nanečisto).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | Soubor obnovení UTF-8 s B64| linky.
  --delete-duplicates | Odstraňte duplicitní kandidáty (potřebuje --confirm-delete s --execute).
  --delete-issues | Odstraňte kandidáty na skupinu problémů (potřebuje --confirm-delete s --execute). Ne na vzdálené automatizační cíle.
  --archive-after-organize | Po uspořádání: ZIP sourozence pro jednotlivé soubory a poté smažte originály (potřebuje --confirm-delete s --execute). Přeskočí již archivovaná rozšíření.

  **Poznámka:** CLI `--mode models` vybírá **CAD / 3D modely**, nikoli artefakty AI. Pro AI / ML použijte `--mode ai` nebo `--mode models-ai`.

  Příklad (zkušební běh, všechny kategorie): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Příklad (pouze přesuny do Unique, provedení): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Sestavení: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Chod nanečisto: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  U --execute odstraňte :ro z držáku zdroje. Pravidla pro více workerů (jeden výstupní kořen na workera) najdete v containers/README.md.

Kubernetes (referenční práce)
  Zdrojové PVC pouze pro čtení jsou platné pro úlohy se zkušebním během. Skutečné pohyby s --execute vyžadují zapisovatelné zdrojové PVC. Poskytněte platné oprávnění obchodu nebo vydavatele pro všechny běhy organizování/oprav (zkušební běh a spuštění). Jeden modul na výstupní strom. Minimální vzor je zdokumentován v containers/README.md spolu s ukázkovým manifestem.

Průběh úloh
  Okno Úlohy ukazuje průběh pro běhy App, CLI, Docker a Kubernetes. Fáze se známým celkem ukazují procenta. Prohledávání bez celkového počtu zůstávají neurčitá.
  Automatizace spouští pracovní proces CLI s ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 a tyto řádky značek odstraňuje z viditelného protokolu. Ručně spuštěný běh CLI nevydává žádné značky, pokud tato proměnná není nastavena.
  Pracovní procesy Docker a Kubernetes dostávají stejnou proměnnou, takže i tyto běhy hlásí procenta. Hodnota se čte z protokolu pracovního procesu, takže se objeví, jakmile kontejner nebo pod začne zapisovat.
  --list-running a --show-run nesou pole průběhu pro aktivní úlohy, pokud běh něco nahlásil.

# Příklady spuštění

## Grafické uživatelské rozhraní

Přidejte **Zdroje** a výstupní složku, zvolte režim běhu, zapněte **Zkušební běh** pro náhled a poté stiskněte **Spustit**. Pro skutečné přesuny nechte **Zkušební běh** vypnutý. Možnosti mazání vyžadují potvrzení před spuštěním.

## Příklady CLI

CLI Zkušební běh: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
