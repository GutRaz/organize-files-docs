# CLI, Docker e Kubernetes (layout di riferimento)

## Automazione della CLI

Questo capitolo segue lo stile Microsoft/HashiCorp: riga di utilizzo, tabella dei flag (token inglesi), quindi esempi di copia-incolla.

CLI (OrganizeFiles.Cli)
  UTILIZZO: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  UTILIZZO: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Bandiera (lunga) | Significato
  ------------------------|----------------------------------------
  --execute | Mosse reali (l'impostazione predefinita è solo prova).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | UTF-8 file di ripristino con B64| linee.
  --delete-duplicates | Elimina i candidati duplicati (richiede --confirm-delete con --execute).
  --delete-issues | Elimina i candidati al bucket dei problemi (richiede --confirm-delete con --execute). Non su obiettivi di automazione remota.
  --archive-after-organize | Dopo l'organizzazione: ZIP di pari livello per file, quindi elimina gli originali (richiede --confirm-delete con --execute). Salta le estensioni già archiviate.

  **Nota:** la CLI `--mode models` seleziona **modelli CAD/3D**, non artefatti AI. Utilizza `--mode ai` o `--mode models-ai` per AI/ML.

  Esempio (Simulazione, tutti i bucket): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Esempio (solo spostamenti in Unique, esegui): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Compilazione: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Simulazione: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  Per --execute, rimuovere :ro dal montaggio sorgente. Vedere containers/README.md per le regole multi-worker (una root di output per worker).

Kubernetes (lavoro di riferimento)
  I PVC di origine di sola lettura sono validi per i processi di prova. I movimenti reali con --execute richiedono PVC di origine scrivibili. Fornire un diritto valido del negozio o dell'editore per tutte le esecuzioni di organizzazione/riparazione (esecuzione di prova ed esecuzione). Un Pod per albero di output. Un modello minimo è documentato in containers/README.md insieme a un manifest di esempio.

Avanzamento processi
  La finestra Processi mostra l'avanzamento per le esecuzioni App, CLI, Docker e Kubernetes. Le fasi con un totale noto mostrano una percentuale. Le scansioni senza totale restano indeterminate.
  L'automazione avvia il processo di lavoro CLI con ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 e rimuove quelle righe di marcatura dal registro visibile. Un'esecuzione CLI avviata a mano non emette marcature a meno che quella variabile non sia impostata.
  I processi di lavoro Docker e Kubernetes ricevono la stessa variabile, quindi anche quelle esecuzioni riportano una percentuale. Il valore viene letto dal registro del processo di lavoro, quindi compare non appena il contenitore o il pod inizia a scrivere.
  --list-running e --show-run portano campi di avanzamento per i processi attivi quando l'esecuzione ha riportato qualcosa.

# Esempi di esecuzione

## Interfaccia utente grafica

Aggiungi **Sorgenti** e la cartella di output, scegli la modalità di esecuzione, attiva **Simulazione** per un’anteprima, quindi premi **Esegui**. Lascia **Simulazione** disattivata per spostamenti reali. Le opzioni di eliminazione chiedono conferma prima dell’esecuzione.

## Esempi CLI

CLI Simulazione: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
