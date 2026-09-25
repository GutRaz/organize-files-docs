# CLI, Docker och Kubernetes (referenslayout)

## CLI-automatisering

Det här kapitlet följer Microsoft/HashiCorp-stilen: användningslinje, flaggtabell (engelska tokens), sedan kopiera-klistra exempel.

CLI (OrganizeFiles.Cli)
  ANVÄNDNING: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  ANVÄNDNING: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Flagga (lång) | Mening
  --------------------------|----------------------------------------
  --execute | Riktiga drag (standard är endast testkörning).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | UTF-8 resume-fil med B64| rader.
  --delete-duplicates | Ta bort dubbletter av kandidater (behöver --confirm-delete med --execute).
  --delete-issues | Ta bort kandidater för issue-bucket (behöver --confirm-delete med --execute). Inte på fjärrautomationsmål.
  --archive-after-organize | Efter organisera: per fil syskon ZIP radera sedan original (behöver --confirm-delete med --execute). Hoppar över redan arkiverade tillägg.

  **Obs!** CLI `--mode models` väljer **CAD/3D-modeller**, inte AI-artefakter. Använd `--mode ai` eller `--mode models-ai` för AI / ML.

  Exempel (testkörning, alla skopor): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Exempel (endast Unika drag, exekvera): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Bygg: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Testkörning: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  För --execute, ta bort :ro från källfästet. Se containers/README.md för regler för flera workers (en utdatarot per worker).

Kubernetes (referensjobb)
  Skrivskyddade PVC-material är giltiga för testkörningsjobb. Riktiga drag med --execute kräver skrivbara käll-PVC. Tillhandahåll giltig butiks- eller utgivarerättighet för alla organiserings-/reparationskörningar (torkkörning och exekvering). En Pod per utgångsträd. Ett minimalt mönster finns dokumenterat i containers/README.md tillsammans med ett provmanifest.

Jobbförlopp
  Jobbfönstret visar förlopp för App-, CLI-, Docker- och Kubernetes-körningar. Steg med känd summa visar en procentandel. Genomsökningar utan summa förblir obestämda.
  Automatiseringen startar CLI-workern med ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 och tar bort de markörraderna ur den synliga loggen. En CLI-körning som startas för hand sänder inga markörer om inte den variabeln är satt.
  Docker- och Kubernetes-workers får samma variabel, så de körningarna rapporterar också en procentandel. Talet läses från workerns logg, så det visas så snart containern eller podden börjar skriva.
  --list-running och --show-run bär förloppsfält för aktiva jobb när körningen har rapporterat något.

# Körningsexempel

## Grafiskt användargränssnitt

Lägg till **Källor** och utdatamappen, välj körläge, slå på **Testkörning** för en förhandsgranskning och tryck sedan på **Kör**. Låt **Testkörning** vara av för riktiga flyttar. Raderingsalternativ kräver bekräftelse före körning.

## CLI-exempel

CLI Testkörning: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
