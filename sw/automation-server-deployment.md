# CLI, Docker, na Kubernetes (mpangilio wa marejeleo)

## CLI otomatiki

Sura hii inafuata mtindo wa Microsoft/HashiCorp: mstari wa matumizi, jedwali la bendera (tokeni za Kiingereza), kisha mifano ya nakala na ubandike.

CLI (OrganizeFiles.Cli)
  MATUMIZI: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  MATUMIZI: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Bendera (ndefu) | Maana
  -------------------------|----------------------------------------
  --execute | Vitendo halisi (chaguo-msingi ni uendeshaji wa majaribio tu).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | UTF-8 endelea na faili ukitumia B64| mistari.
  --delete-duplicates | Futa wagombeaji nakala (inahitaji --confirm-delete na --execute).
  --delete-issues | Futa waombaji wa kutoa ndoo (inahitaji --confirm-delete na --execute). Sio kwa malengo ya kiotomatiki ya mbali.
  --archive-after-organize | Baada ya kupanga: kwa kila faili ZIP kisha ufute asili (inahitaji --confirm-delete iliyo na --execute). Huruka viendelezi vilivyohifadhiwa kwenye kumbukumbu.

  **Kumbuka:** CLI `--mode models` huchagua miundo ya **CAD / 3D**, si vizalia vya programu vya AI. Tumia `--mode ai` au `--mode models-ai` kwa AI / ML.

  Mfano (uendeshaji wa majaribio, ndoo zote): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Mfano (hatua za Kipekee pekee, tekeleza): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Jenga: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Uendeshaji wa majaribio: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  Kwa --execute, ondoa :ro kutoka kwa chanzo cha kupachika. Tazama containers/README.md kwa sheria za workers wengi (mzizi mmoja wa pato kwa kila worker).

Kubernetes (kazi ya kumbukumbu)
  PVC za chanzo cha kusoma pekee ni halali kwa kazi zinazoendeshwa na uendeshaji wa majaribio. Hatua za kweli na --execute zinahitaji PVC za chanzo zinazoweza kuandikwa. Toa haki halali ya duka au mchapishaji kwa endeshaji zote za kupanga/kurekebisha (kausha na utekeleze). Ganda moja kwa kila mti wa pato. Mchoro mdogo umeandikwa katika containers/README.md pamoja na sampuli ya faili ya maelezo.

Maendeleo ya kazi
  Dirisha la Kazi huonyesha maendeleo kwa mizunguko ya App, CLI, Docker na Kubernetes. Hatua zenye jumla inayojulikana huonyesha asilimia. Uchanganuzi usio na jumla hubaki bila kikomo.
  Uendeshaji otomatiki huanzisha worker wa CLI kwa ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 na huondoa mistari hiyo ya alama kwenye kumbukumbu inayoonekana. Mzunguko wa CLI ulioanzishwa kwa mkono hautoi alama isipokuwa kigezo hicho kimewekwa.
  Workers wa Docker na Kubernetes hupokea kigezo hicho hicho, kwa hivyo mizunguko hiyo pia huripoti asilimia. Nambari husomwa kutoka kwenye kumbukumbu ya worker, kwa hivyo huonekana mara tu kontena au pod inapoanza kuandika.
  --list-running na --show-run hubeba sehemu za maendeleo kwa kazi zinazoendelea wakati mzunguko umeripoti kitu.

# Mifano ya uendeshaji

## Kiolesura cha Mchoro

Ongeza **Vyanzo** na folda ya matokeo, chagua hali ya uendeshaji, washa **Uendeshaji wa majaribio** kwa onyesho la awali, kisha bonyeza **Endesha**. Acha **Uendeshaji wa majaribio** ikiwa imezimwa ili kuhamisha kwa kweli. Chaguo za kufuta huomba uthibitisho kabla ya kutekeleza.

## Mifano ya CLI

CLI Uendeshaji wa majaribio: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
