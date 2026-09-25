# CLI, Docker și Kubernetes (referință)

## Automatizare CLI

Acest capitol urmează stilul Microsoft/HashiCorp: linie de utilizare, tabel de flag-uri (tokeni în engleză), apoi exemple de copiat.

CLI (OrganizeFiles.Cli)
  UTILIZARE: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  UTILIZARE: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Flag (lung)              | Semnificație
  -------------------------|----------------------------------------
  --execute                | Mutări reale (implicit rularea este doar simulare).
  --move-scope <token>     | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name>       | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file>          | Fișier de reluare UTF-8 cu linii B64|.
  --delete-duplicates      | Șterge candidații duplicat (necesită --confirm-delete cu --execute).
  --delete-issues          | Șterge candidații din coșul Probleme (necesită --confirm-delete cu --execute). Nu pe ținte de automatizare remote.
  --archive-after-organize | După organizare: ZIP separat lângă fiecare fișier, apoi șterge originalele (necesită --confirm-delete cu --execute). Sare peste extensiile deja arhivate.

  **Notă:** CLI `--mode models` selectează **modele CAD / 3D**, nu artefacte AI. Pentru AI / ML folosește `--mode ai` sau `--mode models-ai`.

  Exemplu (simulare, toate coșurile): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Exemplu (doar mutări Unique, executare): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Construire: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Simulare: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  Pentru --execute, elimină :ro din montarea sursei. Vezi containers/README.md pentru regulile cu mai mulți workeri (o rădăcină de destinație per worker).

Kubernetes (Job de referință)
  PVC-urile sursă doar în citire sunt valide pentru joburile de simulare. Mutările reale cu --execute necesită PVC-uri sursă inscriptibile. Furnizează un drept valid din magazin sau de la editor pentru toate rulările de organizare/reparare (simulare și executare). Câte un Pod pentru fiecare arbore destinație. Un model minim este documentat în containers/README.md împreună cu un manifest exemplu.

Progres joburi
  Fereastra Jobs afișează progresul pentru rulările App, CLI, Docker și Kubernetes. Etapele cu total cunoscut arată procentul. Scanările fără total rămân indeterminate.
  Automatizarea pornește worker-ul CLI cu ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 și elimină acele linii de marcaj din jurnalul vizibil. O rulare CLI pornită manual nu emite marcaje decât dacă acea variabilă este setată.
  Workerii Docker și Kubernetes primesc aceeași variabilă, deci și acele rulări raportează procent. Cifra este citită din jurnalul worker-ului, deci apare de când containerul sau pod-ul începe să scrie.
  --list-running și --show-run includ câmpuri de progres pentru joburile active, când rularea a raportat ceva.

# Exemple de rulare

## Interfață grafică

Completează **Surse**, **Destinație**, mod rulare, opțional **Mutări planificate** (implicit toate coșurile), **Simulare** pentru previzualizare, extensii, apoi **Run**. Lasă **Simulare** nebifată pentru mutări reale. Ștergerea cere confirmare la execuție.

## Exemple CLI

CLI simulare (media, Unice + Probleme): OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execuție: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI ștergere: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker, simulare: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
