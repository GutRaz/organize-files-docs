# Container — configurazione

## Cosa è richiesto

Solo il programma `docker` o `kubectl` deve essere raggiungibile sulla macchina che esegue il lavoro. Non è necessario nient'altro. Docker Desktop non è un requisito. Docker Engine su Linux, Rancher Desktop, colima e Podman con un comando compatibile con docker funzionano tutti allo stesso modo, perché l'app esegue semplicemente il comando che trova nel percorso di sistema.

Kubernetes funziona allo stesso modo. È supportato qualsiasi cluster raggiungibile tramite `kubectl`, inclusi k3s, kind, minikube e cluster gestiti come EKS, GKE o AKS.

## Utilizzo di un demone o cluster diverso

Per inviare lavori a un altro demone Docker, imposta `DOCKER_HOST` o cambia con `docker context use`. Per utilizzare un altro cluster Kubernetes, cambia il contesto corrente con `kubectl config use-context`. L'app segue tutto ciò che già utilizza la riga di comando, quindi non è necessaria alcuna impostazione aggiuntiva all'interno dell'app.

## Dove sono montati i file

Per Kubernetes, la cartella viene allegata in due modi. I contesti di sviluppo locale ottengono un montaggio diretto della cartella host. Ciò copre un contesto denominato `desktop`, `colima` o `orbstack`, uno che termina con `@desktop`, uno che inizia con `kind-`, `minikube` o `k3d-`, e uno il cui nome contiene `docker-desktop`, `docker-for-desktop` o `rancher-desktop`. Ogni altro contesto viene trattato come un cluster reale e riceve invece una richiesta di volume persistente, poiché un nodo del cluster reale non può vedere le cartelle sul computer desktop. Impostare `ORGANIZE_FILES_K8S_VOLUME_MODE` su `pvc` o `hostpath` sostituisce questa scelta per ogni contesto.

## Cartelle di rete su Windows

Docker Desktop su Windows non può collegare un percorso di rete come `\\server\share` a un contenitore Linux. Windows vede la cartella, ma il contenitore no. Ci sono due modi per aggirare il problema. Utilizza una cartella su un disco locale oppure esegui invece il lavoro con la destinazione App, che esegue il lavoro nell'app stessa. Una lettera di unità associata alla condivisione non aiuta, perché l'app la riconduce al percorso di rete e la rifiuta allo stesso modo.

## File già pronti

I kit a riga di comando per Linux contengono file pronti nella cartella `containers`: un Dockerfile che crea l'immagine dal kit stesso, un esempio Compose, esempi di Job Kubernetes e `containers/README.md`, con accanto un README per ogni lingua.

# Contenitori e operatori CLI

## Lavori pianificati: target Docker e Kubernetes

Apri **Lavori** dalla barra laterale della finestra principale. Fai clic su **Nuovo lavoro** o **Modifica** su una scheda esistente. Nel menu a discesa **Destinazione** seleziona **Comando Docker** o **Processo Kubernetes**.

1. Impostare **Sorgenti** (percorsi host) e **Output** (percorso host: deve già esistere prima dell'esecuzione del lavoro).
2. Scegli **Modalità** e **Opzioni di esecuzione** come per qualsiasi altro lavoro.
3. Il pannello **Anteprima comando** mostra l'esatto comando "docker run" o YAML del processo Kubernetes che verrà applicato.
4. **Salva** il lavoro e imposta una **Programma** oppure fai clic su **Esegui ora** sulla scheda per iniziare immediatamente.

L'app genera automaticamente i flag di montaggio e i percorsi del volume dallo snapshot salvato. Il demone Docker o "kubectl" deve essere raggiungibile sul computer host. **Preflight** controlla la connettività e segnala eventuali errori nel registro del lavoro prima dell'avvio dell'esecuzione. Per il flusso di approvazione, il recupero dei log e la pianificazione headless, vedere **Lavori pianificati**.

## Terminale della macchina ospite (PowerShell / bash / cmd)

Sì — sulla macchina ospite avviare **OrganizeFiles.Cli** da PowerShell, bash o cmd. È la via supportata da terminale. La finestra desktop di Avalonia è un'interfaccia grafica a parte. Pubblicare o installare il kit della CLI accanto all'applicazione (o in PATH), poi passare **--source** (ripetibile), **--output** e **--mode**. Meglio cominciare con una prova a vuoto. Aggiungere **--execute** solo quando si è pronti.

## Interfaccia desktop e contenitori

Contenitori e automazione: la GUI desktop di Avalonia non è pensata per essere eseguita all'interno di un tipico contenitore Linux headless. Per uno o più lavori isolati, inclusi diversi lavoratori paralleli, utilizzare il compagno OrganizeFiles.Cli: in ogni contenitore montare cartelle di origine di sola lettura per lavori di anteprima di prova. Gli spostamenti reali con **--execute** richiedono un montaggio sorgente scrivibile perché il motore riposiziona i file fuori dall'albero sorgente. Utilizza un volume di output di lettura/scrittura dedicato, assicurati un diritto valido del negozio o dell'editore per tutte le esecuzioni di organizzazione/riparazione (esecuzione di prova ed esecuzione), passa **--source** (ripetibile), **--output** e **--mode**. Ogni lavoratore simultaneo necessita della propria root di output. La cartella **Output** deve già esistere sull'host prima dell'esecuzione dei lavori Docker o Kubernetes (il preflight rifiuta una destinazione mancante e non la crea). Percorsi di esempio: containers/README.md e containers/docker-compose.sample.yml. Jobs/JobAgent generato `docker run` monta le sorgenti su `/in1`, `/in2`, … e l'output su `/out`. Gli esempi manuali a sorgente singola possono utilizzare `/in` (vedi containers/README.md).
