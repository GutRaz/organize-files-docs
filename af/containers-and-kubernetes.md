# Houers — opstelling

## Wat word vereis

Slegs die `docker` of `kubectl` program moet bereikbaar wees op die masjien wat die taak laat loop. Niks anders is nodig nie. Docker Desktop is nie 'n vereiste nie. Docker Engine op Linux, Rancher Desktop, colima en Podman met 'n docker-versoenbare opdrag werk almal op dieselfde manier, omdat die toepassing eenvoudig die opdrag uitvoer wat dit op die stelselpad vind.

Kubernetes werk dieselfde. Enige groepering wat deur `kubectl` bereik kan word, word ondersteun, insluitend k3s, soort, minikube en bestuurde groepe soos EKS, GKE of AKS.

## Gebruik 'n ander daemoon of groepering

Om take na 'n ander Docker-demon te stuur, stel `DOCKER_HOST` of skakel met `docker context use`. Om 'n ander Kubernetes-kluster te gebruik, verander die huidige konteks met `kubectl config use-context`. Die toepassing volg alles wat die opdragreël reeds gebruik, so geen ekstra instelling is binne die toepassing nodig nie.

## Waar lêers gemonteer word

Vir Kubernetes word die gids op een van twee maniere aangeheg. Plaaslike ontwikkelingskontekste kry 'n direkte gasheerlêergids. Dit dek 'n konteks genaamd `desktop`, `colima` of `orbstack`, een wat eindig met `@desktop`, een wat begin met `kind-`, `minikube` of `k3d-`, en een waarvan die naam `docker-desktop`, `docker-for-desktop` of `rancher-desktop` bevat. Elke ander konteks word as 'n regte groepering behandel en kry eerder 'n aanhoudende volume-eis, omdat 'n regte groepknoop nie die vouers op die rekenaarmasjien kan sien nie. Om `ORGANIZE_FILES_K8S_VOLUME_MODE` op `pvc` of `hostpath` te stel, oorskryf daardie keuse vir elke konteks.

## Netwerkvouers op Windows

Docker Desktop op Windows kan nie 'n netwerkpad soos `\\server\share` aan 'n Linux-houer heg nie. Windows sien die vouer, maar die houer nie. Daar is twee maniere om dit te omseil. Gebruik 'n vouer op 'n plaaslike skyf, of voer eerder die taak met die toepassingteiken uit, wat die werk in die toepassing self doen. 'n Dryfletter wat aan die deel gekoppel is, help nie, want die toepassing volg dit terug na die netwerkpad en weier dit op dieselfde manier.

## Klaargemaakte lêers

Die Linux-opdragreëlstelle bevat gereedgemaakte lêers in hul `containers`-gids: 'n Dockerfile wat die beeld uit die stel self bou, 'n Compose-voorbeeld, Kubernetes Job-voorbeelde en `containers/README.md`, met 'n README vir elke taal daarlangs.

# Houers en CLI workers

## Geskeduleerde take — Docker- en Kubernetes-teikens

Maak **Take** oop vanaf die hoofvenster-sybalk. Klik **Nuwe werk** of **Redigeer** op 'n bestaande kaart. In die **Teiken**-aftreklys kies **Docker-opdrag** of **Kubernetes-werk**.

1. Stel **Bronne** (gasheerpaaie) en **Uitvoer** (gasheerpad — moet reeds bestaan voordat die taak loop).
2. Kies **Modus** en **Laatopsies** soos vir enige ander werk.
3. Die **Bevelvoorskou**-paneel wys die presiese `docker run`-opdrag of Kubernetes Job YAML wat toegepas sal word.
4. **Stoor** die taak en stel 'n **Skedule**, of klik **Voer nou uit** op die kaart om dadelik te begin.

Die toepassing genereer die bergvlae en volume-paaie outomaties vanaf die gestoorde momentopname. Docker daemon of `kubectl` moet op die gasheermasjien bereikbaar wees. **Preflight** kontroleer konnektiwiteit en rapporteer enige foute in die taaklogboek voor die lopie begin. Vir die goedkeuringvloei, logboekherwinning en headless skedulering, sien **Geskeduleerde take**.

## Gasheerterminaal (PowerShell / bash / cmd)

Ja — op die gasheerrekenaar loop **OrganizeFiles.Cli** vanuit PowerShell, bash of cmd. Dit is die ondersteunde terminaalpad. Die Avalonia-lessenaarvenster is 'n aparte GUI. Publiseer of installeer die CLI-stel langs die toepassing (of op PATH), en gee dan **--source** (herhaalbaar), **--output** en **--mode** deur. Doen eers 'n toetslopie. Voeg **--execute** eers by wanneer jy gereed is.

## Lessenaar-GUI en houers

Houers en outomatisering: die Avalonia-tafelblad-GUI is nie bedoel om binne 'n tipiese headless Linux-houer te loop nie. Vir een of meer geïsoleerde take, insluitend verskeie parallelle werkers, gebruik die OrganizeFiles.Cli-metgesel: in elke houer monteer bronvouers net-lees-net vir toetslopievoorskoutake. Werklike skuiwe met **--execute** vereis 'n skryfbare bronmontering omdat die enjin lêers uit die bronboom hervestig. Gebruik 'n toegewyde lees-/skryf-afvoervolume, verseker geldige winkel- of uitgewerregte vir alle organiseer-/herstellopies (toetslopie en uitvoer), gee **--source** deur (herhaalbaar), **--output** en **--mode**. Elke gelyktydige werker benodig sy eie uitsetwortel. Die **Output**-lêergids moet reeds op die gasheer bestaan voordat Docker- of Kubernetes-take loop (preflight weier 'n ontbrekende bestemming en skep dit nie). Voorbeeldpaaie: containers/README.md en containers/docker-compose.sample.yml. Jobs/JobAgent gegenereer `docker run` monteer bronne by `/in1`, `/in2`, … en voer uit by `/out`. Handmatige enkelbronvoorbeelde kan `/in` gebruik (sien containers/README.md).
