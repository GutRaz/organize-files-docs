# CLI, Docker og Kubernetes (referencelayout)

## CLI-automatisering

Dette kapitel følger Microsoft/HashiCorp-stilen: brugslinje, flagtabel (engelske tokens), derefter kopier-indsæt eksempler.

CLI (OrganizeFiles.Cli)
  BRUG: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  BRUG: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Flag (langt) | Betydning
  --------------------------|----------------------------------------
  --execute | Rigtige træk (standard er kun prøvekørsel).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | UTF-8 genoptag-fil med B64| linjer.
  --delete-duplicates | Slet dubletkandidater (kræver --confirm-delete med --execute).
  --delete-issues | Slet issue-bucket-kandidater (kræver --confirm-delete med --execute). Ikke på fjernautomatiseringsmål.
  --archive-after-organize | Efter organisering: per-fil søskende ZIP og derefter slette originaler (kræver --confirm-delete med --execute). Springer allerede arkiverede udvidelser over.

  **Bemærk:** CLI `--mode models` vælger **CAD/3D-modeller**, ikke AI-artefakter. Brug `--mode ai` eller `--mode models-ai` til AI/ML.

  Eksempel (Prøvekørsel, alle kategorier): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Eksempel (kun flytninger til Unique, udfør): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Byg: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Prøvekørsel: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  For --execute skal du fjerne :ro fra kildebeslaget. Se containers/README.md for regler for flere workers (én outputrod pr. worker).

Kubernetes (referencejob)
  Skrivebeskyttede PVC'er er gyldige til prøvekørselsjob. Rigtige træk med --execute kræver skrivbare kilde-PVC'er. Angiv gyldig butiks- eller udgiverrettigheder for alle organiserings-/reparationskørsel (prøvekørsel og udførelse). Én Pod pr. outputtræ. Et minimalt mønster er dokumenteret i containers/README.md sammen med et prøvemanifest.

Jobfremdrift
  Job-vinduet viser fremdrift for App-, CLI-, Docker- og Kubernetes-kørsler. Faser med et kendt total viser en procentdel. Scanninger uden et total forbliver ubestemte.
  Automatisering starter CLI-workeren med ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 og fjerner de markørlinjer fra den synlige log. En CLI-kørsel startet i hånden udsender ingen markører, medmindre den variabel er sat.
  Docker- og Kubernetes-workers modtager den samme variabel, så de kørsler rapporterer også en procentdel. Tallet læses fra workerens log, så det vises, så snart containeren eller podden begynder at skrive.
  --list-running og --show-run bærer fremdriftsfelter for aktive job, når kørslen har rapporteret noget.

# Kørselseksempler

## Grafisk brugergrænseflade

Tilføj **Kilder** og outputmappen, vælg kørselstilstand, slå **Prøvekørsel** til for et eksempel, og tryk derefter på **Kør**. Lad **Prøvekørsel** være slået fra for rigtige flytninger. Sletteindstillinger kræver bekræftelse før kørsel.

## CLI-eksempler

CLI Prøvekørsel: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
