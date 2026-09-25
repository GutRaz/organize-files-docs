# Containrar — konfiguration

## Vad krävs

Endast programmet `docker` eller `kubectl` måste vara tillgängligt på den maskin som kör jobbet. Inget annat behövs. Docker Desktop är inget krav. Docker Engine på Linux, Rancher Desktop, colima och Podman med ett docker-kompatibelt kommando fungerar alla på samma sätt, eftersom appen helt enkelt kör kommandot den hittar på systemvägen.

Kubernetes fungerar likadant. Alla kluster som kan nås via `kubectl` stöds, inklusive k3s, kind, minikube och hanterade kluster som EKS, GKE eller AKS.

## Använda en annan demon eller kluster

För att skicka jobb till en annan Docker-demon, ställ in `DOCKER_HOST` eller byt med `docker context use`. För att använda ett annat Kubernetes-kluster, byt aktuellt sammanhang med `kubectl config use-context`. Appen följer vad kommandoraden redan använder, så ingen extra inställning behövs inuti appen.

## Där filerna är monterade

För Kubernetes bifogas mappen på ett av två sätt. Lokala utvecklingssammanhang får en direkt värdmappsmontering. Det täcker ett sammanhang som heter `desktop`, `colima` eller `orbstack`, ett som slutar med `@desktop`, ett som börjar med `kind-`, `minikube` eller `k3d-`, och ett vars namn innehåller `docker-desktop`, `docker-for-desktop` eller `rancher-desktop`. Alla andra sammanhang behandlas som ett riktigt kluster och får istället ett beständigt volymkrav, eftersom en riktig klusternod inte kan se mapparna på den stationära maskinen. Att sätta `ORGANIZE_FILES_K8S_VOLUME_MODE` till `pvc` eller `hostpath` åsidosätter det valet för alla sammanhang.

## Nätverksmappar på Windows

Docker Desktop på Windows kan inte koppla en nätverkssökväg som `\\server\share` till en Linux-behållare. Windows ser mappen, men behållaren gör det inte. Det finns två vägar runt det. Använd en mapp på en lokal disk, eller kör jobbet med appmålet istället, som gör jobbet i själva appen. En enhetsbokstav som är mappad till delningen hjälper inte, eftersom appen följer den tillbaka till nätverkssökvägen och nekar den på samma sätt.

## Färdiga filer

Linux-kommandoradskiten innehåller färdiga filer i mappen `containers`: en Dockerfile som bygger avbildningen från själva kitet, ett Compose-exempel, Kubernetes Job-exempel och `containers/README.md`, med en README för varje språk bredvid.

# Containers och CLI-workers

## Schemalagda jobb — Docker- och Kubernetes-mål

Öppna **Jobb** från sidofältet i huvudfönstret. Klicka på **Nytt jobb** eller **Redigera** på ett befintligt kort. I rullgardinsmenyn **Mål** väljer du **Docker-kommando** eller **Kubernetes-jobb**.

1. Ställ in **Källor** (värdsökvägar) och **Utdata** (värdsökväg — måste redan finnas innan jobbet körs).
2. Välj **Läge** och **Köralternativ** som för alla andra jobb.
3. Panelen **Kommandoförhandsgranskning** visar det exakta kommandot 'dockerkörning' eller Kubernetes Job YAML som kommer att tillämpas.
4. **Spara** jobbet och ställ in ett **Schema**, eller klicka på **Kör nu** på kortet för att starta omedelbart.

Appen genererar monteringsflaggor och volymbanor automatiskt från den sparade ögonblicksbilden. Docker-demon eller "kubectl" måste vara tillgänglig på värddatorn. **Preflight** kontrollerar anslutningen och rapporterar eventuella fel i jobbloggen innan körningen startar. För godkännandeflödet, logghämtning och headless schemaläggning, se **Schemalagda jobb**.

## Värddatorns terminal (PowerShell / bash / cmd)

Ja — kör **OrganizeFiles.Cli** på värddatorn från PowerShell, bash eller cmd. Det är den stödda vägen via en terminal. Avalonias skrivbordsfönster är ett eget grafiskt skal. Publicera eller installera CLI-satsen bredvid programmet (eller på PATH) och skicka sedan **--source** (kan upprepas), **--output** och **--mode**. Börja helst med en testkörning. Lägg till **--execute** först när du är redo.

## Skrivbordsskal och behållare

Behållare och automatisering: Avalonia desktop GUI är inte tänkt att köras i en typisk headless Linux-behållare. För ett eller flera isolerade jobb, inklusive flera parallella arbetare, använd OrganizeFiles.Cli-kompanjonen: i varje behållare monteras källmappar skrivskyddade för testkörda förhandsgranskningsjobb. Verkliga drag med **--execute** kräver en skrivbar källmontering eftersom motorn flyttar filer från källträdet. Använd en dedikerad läs-/skrivvolym, säkerställ giltig lagrings- eller utgivarbehörighet för alla organiserings-/reparationskörningar (testkörning och exekvering), ange **--source** (repeterbar), **--output** och **--mode**. Varje samtidig arbetare behöver sin egen utdatarot. Mappen **Output** måste redan finnas på värden innan Docker- eller Kubernetes-jobb körs (preflight vägrar en saknad destination och skapar den inte). Exempelsökvägar: containers/README.md och containers/docker-compose.sample.yml. Jobs/JobAgent genererad `docker run` monterar källor vid `/in1`, `/in2`, … och matar ut vid `/out`. Manuella exempel med en källa kan använda `/in` (se containers/README.md).
