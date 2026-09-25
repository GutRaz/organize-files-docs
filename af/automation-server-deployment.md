# CLI, Docker en Kubernetes (verwysingsuitleg)

## CLI outomatisering

Hierdie hoofstuk volg die Microsoft/HashiCorp-styl: gebruikslyn, vlagtabel (Engelse tokens), dan kopieer-plak voorbeelde.

CLI (OrganizeFiles.Cli)
  GEBRUIK: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  GEBRUIK: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Vlag (lank) | Betekenis
  --------------------------|----------------------------------------
  --execute | Regte bewegings (verstek is slegs toetslopie).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | UTF-8 hervatlêer met B64| lyne.
  --delete-duplicates | Vee duplikaatkandidate uit (benodig --confirm-delete met --execute).
  --delete-issues | Vee kwessie-emmer-kandidate uit (benodig --confirm-delete met --execute). Nie op afgeleë outomatiseringsteikens nie.
  --archive-after-organize | Na organiseer: per-lêer broer en suster zip dan verwyder oorspronklike (benodig --confirm-delete met --execute). Slaan reeds-argief-uitbreidings oor.

  **Let wel:** CLI `--mode models` kies **CAD / 3D-modelle**, nie KI-artefakte nie. Gebruik `--mode ai` of `--mode models-ai` vir AI / ML.

  Voorbeeld (toetslopie, alle kategorieë): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Voorbeeld (slegs skuiwe na Unique, voer uit): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Bou: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Toetslopie: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  Vir --execute, verwyder :ro van die bronmontering. Sien containers/README.md vir multi-worker reëls (een uitset wortel per worker).

Kubernetes (verwysingswerk)
  Leesalleen-bron-PVC's is geldig vir toetslopie werke. Regte bewegings met --execute benodig skryfbare bron-PVC's. Verskaf geldige winkel- of uitgewerregte vir alle organiseer-/herstellopies (toetslopie en uitvoer). Een peul per uitsetboom. 'n Minimale patroon word saam met 'n monstermanifes in containers/README.md gedokumenteer.

Taakvordering
  Die Take-venster wys vordering vir App-, CLI-, Docker- en Kubernetes-lopies. Fases met 'n bekende totaal wys 'n persentasie. Skanderings sonder 'n totaal bly onbepaald.
  Outomatisering begin die CLI-worker met ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 en verwyder daardie merkerreëls uit die sigbare log. 'n CLI-lopie wat met die hand begin word, gee geen merkers nie, tensy daardie veranderlike gestel is.
  Docker- en Kubernetes-workers kry dieselfde veranderlike, dus rapporteer daardie lopies ook 'n persentasie. Die getal word uit die worker se log gelees, dus verskyn dit sodra die houer of die pod begin skryf.
  --list-running en --show-run dra vorderingsvelde vir aktiewe take wanneer die lopie enigiets gerapporteer het.

# Lopie-voorbeelde

## Grafiese UI

Voeg **Bronne** en die afvoergids by, kies die loopmodus, skakel **Toetslopie** aan vir ’n voorskou, en druk dan **Voer uit**. Laat **Toetslopie** ongemerk vir werklike skuiwe. Skrapopsies vra eers bevestiging voor uitvoering.

## CLI-voorbeelde

CLI Toetslopie: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
