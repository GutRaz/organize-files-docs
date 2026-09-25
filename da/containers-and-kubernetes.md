# Containere — opsætning

## Hvad kræves

Kun programmet `docker` eller `kubectl` skal være tilgængeligt på den maskine, der kører jobbet. Der er ikke behov for andet. Docker Desktop er ikke et krav. Docker Engine på Linux, Rancher Desktop, colima og Podman med en docker-kompatibel kommando fungerer alle på samme måde, fordi appen simpelthen kører den kommando, den finder på systemstien.

Kubernetes fungerer på samme måde. Enhver klynge, der kan nås via `kubectl`, er understøttet, inklusive k3s, kind, minikube og administrerede klynger såsom EKS, GKE eller AKS.

## Brug af en anden dæmon eller klynge

For at sende job til en anden Docker-dæmon skal du indstille `DOCKER_HOST` eller skifte med `docker context use`. For at bruge en anden Kubernetes-klynge skal du skifte den aktuelle kontekst med `kubectl config use-context`. Appen følger alt, hvad kommandolinjen allerede bruger, så der kræves ingen ekstra indstilling inde i appen.

## Hvor filer er monteret

For Kubernetes er mappen vedhæftet på en af to måder. Lokale udviklingskontekster får en direkte værtsmappemontering. Det dækker en kontekst med navnet `desktop`, `colima` eller `orbstack`, én der slutter med `@desktop`, én der starter med `kind-`, `minikube` eller `k3d-`, og én hvis navn indeholder `docker-desktop`, `docker-for-desktop` eller `rancher-desktop`. Hver anden kontekst behandles som en rigtig klynge og får i stedet et vedvarende volumenkrav, fordi en rigtig klyngenode ikke kan se mapperne på skrivebordsmaskinen. At sætte `ORGANIZE_FILES_K8S_VOLUME_MODE` til `pvc` eller `hostpath` tilsidesætter det valg for hver kontekst.

## Netværksmapper på Windows

Docker Desktop på Windows kan ikke vedhæfte en netværkssti såsom `\\server\share` til en Linux-container. Windows ser mappen, men beholderen gør det ikke. Der er to veje uden om det. Brug en mappe på en lokal disk, eller kør jobbet med App-målet i stedet, som udfører arbejdet i selve appen. Et drevbogstav, der er tilknyttet sharen, hjælper ikke, fordi appen følger det tilbage til netværksstien og afviser det på samme måde.

## Færdiglavede filer

Linux-kommandolinjekittene har færdige filer i mappen `containers`: en Dockerfile, der bygger imaget ud fra selve kittet, et Compose-eksempel, Kubernetes Job-eksempler og `containers/README.md` med en README for hvert sprog ved siden af.

# Containere og CLI-workers

## Planlagte job — Docker- og Kubernetes-mål

Åbn **Opgaver** fra sidebjælken i hovedvinduet. Klik på **Ny opgave** eller **Rediger** på et eksisterende kort. Vælg **Docker-kommando** eller **Kubernetes-opgave** i rullemenuen **Mål**.

1. Indstil **Kilder** (værtsstier) og **Output** (værtsstier — skal allerede eksistere, før jobbet kører).
2. Vælg **Tilstand** og **Kørindstillinger** som for ethvert andet job.
3. Panelet **Kommando forhåndsvisning** viser den nøjagtige "docker run"-kommando eller Kubernetes Job YAML, der vil blive anvendt.
4. **Gem** jobbet og indstil en **Tidsplan**, eller klik på **Kør nu** på kortet for at starte med det samme.

Appen genererer monteringsflag og volumenstier automatisk fra det gemte snapshot. Docker-dæmon eller 'kubectl' skal være tilgængelig på værtsmaskinen. **Preflight** kontrollerer forbindelsen og rapporterer eventuelle fejl i jobloggen, før kørslen starter. For godkendelsesflowet, loghentning og headless planlægning, se **Planlagte opgaver**.

## Værtsterminal (PowerShell / bash / cmd)

Ja — på værtsmaskinen kører du **OrganizeFiles.Cli** fra PowerShell, bash eller cmd. Det er den understøttede vej gennem en terminal. Avalonia-skrivebordsvinduet er en separat grafisk flade. Udgiv eller installer CLI-sættet ved siden af appen (eller på PATH), og send så **--source** (kan gentages), **--output** og **--mode**. Kør helst prøvekørsel først. Tilføj først **--execute**, når du er klar.

## Skrivebords-GUI og containere

Containere og automatisering: Avalonia desktop GUI er ikke beregnet til at køre inde i en typisk headless Linux-container. Til et eller flere isolerede job, inklusive flere parallelle arbejdere, skal du bruge OrganizeFiles.Cli-ledsageren: I hver beholder monterer kildemapper skrivebeskyttet til Prøvekørsel forhåndsvisningsjob. Rigtige træk med **--execute** kræver en skrivbar kildemontering, fordi motoren flytter filer ud af kildetræet. Brug en dedikeret læse/skrive-outputvolumen, sørg for gyldig butiks- eller udgiverberettigelse til alle organiserings-/reparationskørsler (prøvekør og udfør), angiv **--source** (gentagelig), **--output** og **--mode**. Hver samtidige arbejder har brug for sin egen output-rod. Mappen **Output** skal allerede eksistere på værten, før Docker- eller Kubernetes-job kører (preflight afviser en manglende destination og opretter den ikke). Eksempelstier: containers/README.md og containers/docker-compose.sample.yml. Jobs/JobAgent genereret `docker run` monterer kilder ved `/in1`, `/in2`, … og udsender ved `/out`. Manuelle enkeltkildeeksempler kan bruge `/in` (se containers/README.md).
