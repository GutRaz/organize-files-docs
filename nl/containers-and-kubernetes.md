# Containers — installatie

## Wat is vereist

Alleen het programma `docker` of `kubectl` moet bereikbaar zijn op de machine die de taak uitvoert. Er is niets anders nodig. Docker Desktop is geen vereiste. Docker Engine op Linux, Rancher Desktop, colima en Podman met een docker-compatibele opdracht werken allemaal op dezelfde manier, omdat de app eenvoudigweg de opdracht uitvoert die hij op het systeempad vindt.

Kubernetes werkt hetzelfde. Elk cluster dat bereikbaar is via `kubectl` wordt ondersteund, inclusief k3s, kind, minikube en beheerde clusters zoals EKS, GKE of AKS.

## Een andere daemon of cluster gebruiken

Om taken naar een andere Docker-daemon te verzenden, stelt u `DOCKER_HOST` in of schakelt u over met `docker context use`. Als u een ander Kubernetes-cluster wilt gebruiken, schakelt u de huidige context met `kubectl config use-context`. De app volgt alles wat de opdrachtregel al gebruikt, dus er zijn geen extra instellingen nodig in de app.

## Waar bestanden worden gemount

Voor Kubernetes wordt de map op twee manieren bijgevoegd. Lokale ontwikkelingscontexten krijgen een directe hostmapkoppeling. Dat omvat een context met de naam `desktop`, `colima` of `orbstack`, een context die eindigt op `@desktop`, een context die begint met `kind-`, `minikube` of `k3d-`, en een context waarvan de naam `docker-desktop`, `docker-for-desktop` of `rancher-desktop` bevat. Elke andere context wordt behandeld als een echt cluster en krijgt in plaats daarvan een persistente volumeclaim, omdat een echt clusterknooppunt de mappen op de desktopcomputer niet kan zien. Het instellen van `ORGANIZE_FILES_K8S_VOLUME_MODE` op `pvc` of `hostpath` overschrijft die keuze voor elke context.

## Netwerkmappen op Windows

Docker Desktop op Windows kan geen netwerkpad zoals `\\server\share` aan een Linux-container koppelen. Windows ziet de map, maar de container niet. Er zijn twee manieren om dit te omzeilen. Gebruik een map op een lokale schijf, of voer de taak uit met het App-doel, dat het werk in de app zelf doet. Een stationsletter die aan de share is gekoppeld, helpt niet, want de app volgt die terug naar het netwerkpad en weigert die op dezelfde manier.

## Kant-en-klare bestanden

De Linux-opdrachtregelkits bevatten kant-en-klare bestanden in hun map `containers`: een Dockerfile die de image uit de kit zelf bouwt, een Compose-voorbeeld, Kubernetes Job-voorbeelden en `containers/README.md`, met daarnaast een README voor elke taal.

# Containers en CLI-werknemers

## Geplande taken — Docker- en Kubernetes-doelen

Open **Vacatures** vanuit de zijbalk van het hoofdvenster. Klik op **Nieuwe vacature** of **Bewerken** op een bestaande kaart. In de vervolgkeuzelijst **Doel** selecteert u **Docker-opdracht** of **Kubernetes-taak**.

1. Stel **Bronnen** (hostpaden) en **Uitvoer** (hostpad in – moet al bestaan voordat de taak wordt uitgevoerd).
2. Kies **Modus** en **Uitvoeropties** zoals voor elke andere taak.
3. Het paneel **Opdrachtvoorbeeld** toont de exacte opdracht `docker run` of Kubernetes Job YAML die zal worden toegepast.
4. **Sla** de taak op en stel een **Planning** in, of klik op **Nu uitvoeren** op de kaart om onmiddellijk te starten.

De app genereert automatisch de mount-vlaggen en volumepaden op basis van de opgeslagen momentopname. Docker-daemon of `kubectl` moet bereikbaar zijn op de hostmachine. **Preflight** controleert de connectiviteit en rapporteert eventuele fouten in het takenlogboek voordat de run begint. Zie **Geplande taken** voor de goedkeuringsstroom, het ophalen van logboeken en het plannen headless.

## Terminal van de hostcomputer (PowerShell / bash / cmd)

Ja — draai op de hostcomputer **OrganizeFiles.Cli** vanuit PowerShell, bash of cmd. Dat is de ondersteunde weg via een terminal. Het Avalonia-bureaubladvenster is een aparte grafische schil. Publiceer of installeer de CLI-set naast de toepassing (of op PATH) en geef dan **--source** (herhaalbaar), **--output** en **--mode** mee. Begin bij voorkeur met een proefrun. Voeg **--execute** pas toe wanneer u zover bent.

## Bureaubladschil en containers

Containers en automatisering: de Avalonia desktop GUI is niet bedoeld om in een typische headless Linux-container te draaien. Voor een of meer geïsoleerde taken, inclusief meerdere parallelle werkers, gebruikt u de begeleidende OrganizeFiles.Cli: in elke container worden bronmappen alleen-lezen gekoppeld voor proefafdruktaken. Echte zetten met **--execute** vereisen een beschrijfbare bronaankoppeling omdat de engine bestanden uit de bronboom verplaatst. Gebruik een speciaal lees-/schrijfuitvoervolume, zorg voor geldige winkel- of uitgeversrechten voor alle organisatie-/reparatieruns (Proefrun en execute), geef **--source** (herhaalbaar), **--output** en **--mode** door. Elke gelijktijdige werker heeft zijn eigen uitvoerwortel nodig. De map **Output** moet al op de host bestaan voordat Docker- of Kubernetes-taken worden uitgevoerd (preflight weigert een ontbrekende bestemming en maakt deze niet aan). Voorbeeldpaden: containers/README.md en containers/docker-compose.sample.yml. Jobs/JobAgent gegenereerd `docker run` koppelt bronnen op `/in1`, `/in2`, … en uitvoer op `/out`. Bij handmatige voorbeelden uit één bron kan `/in` worden gebruikt (zie containers/README.md).
