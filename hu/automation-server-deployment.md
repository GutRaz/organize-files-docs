# CLI, Docker és Kubernetes (referencia elrendezés)

## CLI automatizálás

Ez a fejezet a Microsoft/HashiCorp stílust követi: használati sor, jelzőtábla (angol tokenek), majd másolás-beillesztés példák.

CLI (OrganizeFiles.Cli)
  HASZNÁLAT: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  HASZNÁLAT: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Zászló (hosszú) | Jelentése
  -------------------------|-----------------------------------------
  --execute | Valódi lépések (az alapértelmezés csak próbafuttatás).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | UTF-8 folytatási fájl a B64|-el vonalak.
  --delete-duplicates | Törölje az ismétlődő jelölteket (--confirm-delete és --execute szükséges).
  --delete-issues | Törölje a problémacsoport jelöltjeit (--confirm-delete és --execute szükséges). Távoli automatizálási célokon nem.
  --archive-after-organize | Rendezés után: fájlonként testvér ZIP, majd törölje az eredetiket (szükség van a --confirm-delete és a --execute fájlra). Kihagyja a már archivált bővítményeket.

  **Megjegyzés:** A CLI `--mode models` a **CAD/3D modelleket** választja ki, nem pedig az AI műtermékeket. Használja a `--mode ai` vagy a `--mode models-ai` értéket az AI/ML-hez.

  Példa (próbafuttatás, minden vödör): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Példa (csak Unique áthelyezések, végrehajtás): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Építés: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Próbafuttatás: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  A --execute esetén távolítsa el a :ro elemet a forrástartóról. Lásd a containers/README.md több workert érintő szabályokat (workerenként egy kimeneti gyökér).

Kubernetes (referenciamunka)
  A csak olvasható forrású PVC-k próbafuttatásként futó munkákhoz érvényesek. A --execute valódi lépéseihez írható forrású PVC-kre van szükség. Minden szervezési/javítási futtatáshoz (próbafuttatás és végrehajtás) biztosítson érvényes áruházi vagy kiadói jogosultságot. Egy Pod kimeneti fánként. A containers/README.md dokumentumban egy minimális minta van dokumentálva egy jegyzékminta mellett.

Feladatok haladása
  A Feladatok ablak az App, a CLI, a Docker és a Kubernetes futásokhoz mutat haladást. Az ismert összesítésű szakaszok százalékot mutatnak. Az összesítés nélküli vizsgálatok határozatlanok maradnak.
  Az automatizálás az ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 értékkel indítja a CLI munkafolyamatot, és eltávolítja ezeket a jelölősorokat a látható naplóból. A kézzel indított CLI futás nem küld jelölőket, hacsak nincs beállítva az a változó.
  A Docker és a Kubernetes munkafolyamatok ugyanazt a változót kapják meg, ezért azok a futások is jeleznek százalékot. A szám a munkafolyamat naplójából olvasható ki, így akkor jelenik meg, amikor a konténer vagy a pod írni kezd.
  A --list-running és a --show-run haladási mezőket hoz az aktív feladatokhoz, ha a futás jelzett valamit.

# Futtatási példák

## Grafikus felhasználói felület

Adja hozzá a(z) **Források** elemet és a kimeneti mappát, válassza ki a futtatási módot, kapcsolja be a(z) **Próbafuttatás** beállítást az előnézethez, majd nyomja meg a(z) **Futtatás** gombot. Valódi áthelyezéshez hagyja kikapcsolva a(z) **Próbafuttatás** beállítást. A törlési beállítások végrehajtás előtt megerősítést kérnek.

## CLI-példák

CLI Próbafuttatás: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
