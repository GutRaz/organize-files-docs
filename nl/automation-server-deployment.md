# CLI, Docker en Kubernetes (referentie-indeling)

## CLI-automatisering

Dit hoofdstuk volgt de Microsoft/HashiCorp-stijl: gebruiksregel, vlagtabel (Engelse tokens) en vervolgens voorbeelden kopiëren en plakken.

CLI (OrganizeFiles.Cli)
  GEBRUIK: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  GEBRUIK: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Vlag (lang) | Betekenis
  ----------------------|------------------------------------
  --execute | Echte zetten (standaard is alleen proefrun).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | UTF-8 Hervattingsbestand met B64| lijnen.
  --delete-duplicates | Verwijder dubbele kandidaten (vereist --confirm-delete met --execute).
  --delete-issues | Kandidaten voor probleembuckets verwijderen (vereist --confirm-delete met --execute). Niet op doelstellingen voor automatisering op afstand.
  --archive-after-organize | Na het organiseren: ZIP per bestand, verwijder dan de originelen (vereist --confirm-delete met --execute). Slaat reeds gearchiveerde extensies over.

  **Opmerking:** CLI `--mode models` selecteert **CAD/3D-modellen**, geen AI-artefacten. Gebruik `--mode ai` of `--mode models-ai` voor AI/ML.

  Voorbeeld (Proefrun, alle buckets): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Voorbeeld (alleen verplaatsingen naar Unique, uitvoeren): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Bouwen: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Proefrun: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  Voor --execute verwijdert u :ro van de bronhouder. Zie containers/README.md voor regels voor meerdere werknemers (één uitvoerroot per werknemer).

Kubernetes (referentietaak)
  Alleen-lezen bron-PVC's zijn geldig voor proefrunopdrachten. Voor echte bewegingen met --execute zijn beschrijfbare bron-PVC's nodig. Geef een geldig winkel- of uitgeversrecht op voor alle organisatie-/reparatieruns (Proefrun en execute). Eén pod per uitvoerboom. Een minimaal patroon is gedocumenteerd in containers/README.md naast een voorbeeldmanifest.

Taakvoortgang
  Het venster Taken toont voortgang voor App-, CLI-, Docker- en Kubernetes-uitvoeringen. Fasen met een bekend totaal tonen een percentage. Scans zonder totaal blijven onbepaald.
  Automatisering start de CLI-worker met ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 en haalt die markeringsregels uit het zichtbare logboek. Een met de hand gestarte CLI-uitvoering geeft geen markeringen tenzij die variabele is ingesteld.
  Docker- en Kubernetes-workers krijgen dezelfde variabele, dus die uitvoeringen melden ook een percentage. Het cijfer wordt gelezen uit het logboek van de worker, dus het verschijnt zodra de container of de pod begint te schrijven.
  --list-running en --show-run dragen voortgangsvelden voor actieve taken wanneer de uitvoering iets heeft gemeld.

# Uitvoeringsvoorbeelden

## Grafische gebruikersinterface

Voeg **Bronnen** en de uitvoermap toe, kies de uitvoeringsmodus, zet **Proefrun** aan voor een voorbeeld en druk daarna op **Uitvoeren**. Laat **Proefrun** uit staan voor echte verplaatsingen. Verwijderopties vragen om bevestiging voordat ze worden uitgevoerd.

## CLI-voorbeelden

CLI Proefrun: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
