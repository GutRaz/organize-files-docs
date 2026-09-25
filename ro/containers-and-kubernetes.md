# Containere — configurare

## Ce este necesar

Doar programul `docker` sau `kubectl` trebuie să fie accesibil pe calculatorul care rulează jobul. Nimic altceva. Docker Desktop nu este obligatoriu. Docker Engine pe Linux, Rancher Desktop, colima și Podman cu o comandă compatibilă docker funcționează la fel, pentru că aplicația pur și simplu rulează comanda găsită în calea sistemului.

Kubernetes funcționează la fel. Orice cluster accesibil prin `kubectl` este suportat, inclusiv k3s, kind, minikube și clustere administrate precum EKS, GKE sau AKS.

## Folosirea altui daemon sau cluster

Pentru a trimite joburi către alt daemon Docker, setați `DOCKER_HOST` sau comutați cu `docker context use`. Pentru alt cluster Kubernetes, comutați contextul curent cu `kubectl config use-context`. Aplicația urmează ce folosește deja linia de comandă, deci nu este nevoie de nicio setare suplimentară în aplicație.

## Unde se montează fișierele

La Kubernetes, folderul se atașează în două feluri. Contextele locale de dezvoltare primesc montare directă a folderului gazdă. Asta acoperă un context numit `desktop`, `colima` sau `orbstack`, unul care se termină în `@desktop`, unul care începe cu `kind-`, `minikube` sau `k3d-`, și unul al cărui nume conține `docker-desktop`, `docker-for-desktop` sau `rancher-desktop`. Orice alt context este tratat ca un cluster real și primește în schimb o revendicare de volum persistent, pentru că un nod de cluster real nu vede folderele de pe calculatorul local. Setarea `ORGANIZE_FILES_K8S_VOLUME_MODE` la `pvc` sau `hostpath` înlocuiește alegerea asta pentru orice context.

## Foldere de rețea pe Windows

Docker Desktop pe Windows nu poate atașa o cale de rețea precum `\\server\share` la un container Linux. Windows vede folderul, containerul nu. Există două soluții. Folosiți un folder de pe un disc local, sau rulați jobul cu ținta App, care face treaba în aplicație. O literă de unitate mapată pe share nu ajută, pentru că aplicația o urmărește înapoi până la calea de rețea și o refuză la fel.

## Fișiere gata făcute

Kiturile Linux de linie de comandă au fișiere gata făcute în folderul `containers`: un Dockerfile care construiește imaginea chiar din kit, o mostră Compose, mostre de Job pentru Kubernetes și `containers/README.md`, cu câte un README pentru fiecare limbă alături.

# Containere și CLI

## Joburi programate — ținte Docker și Kubernetes

Deschide **Joburi** din bara laterală a ferestrei principale. Apasă **Job nou** sau **Editează** pe o fișă existentă. În dropdown-ul **Țintă** alege **Comandă Docker** sau **Job Kubernetes**.

1. Setează **Surse** (căi pe calculator) și **Destinație** (cale pe calculator — trebuie să existe deja înainte de rulare).
2. Alege **Mod** și **Opțiuni rulare** ca pentru orice alt job.
3. Panoul **Previzualizare comandă** arată exact comanda docker run sau YAML-ul Job Kubernetes care va fi aplicat.
4. **Salvează** jobul și setează o **Planificare**, sau apasă **Rulează acum** pe fișă pentru a porni imediat.

Aplicația generează automat flag-urile de montare și căile de volum din snapshot-ul salvat. Docker daemon sau kubectl trebuie să fie accesibil pe calculatorul gazdă. **Preflight** verifică conectivitatea și raportează erorile în jurnalul jobului înainte de pornire. Pentru fluxul de aprobare, preluarea jurnalelor și planificarea headless, vezi **Joburi programate**.

## Terminal pe calculator (PowerShell / bash / cmd)

Da — pe calculator rulezi **OrganizeFiles.Cli** din PowerShell, bash sau cmd. Asta e calea din terminal. Fereastra Avalonia e GUI separat. Publică sau instalează kit-ul CLI lângă aplicație (sau pe PATH), apoi transmite **--source** (repetabil), **--output** și **--mode**. Preferă mai întâi simularea. Adaugă **--execute** doar când ești gata.

## GUI desktop și containere

Containere: GUI-ul Avalonia desktop nu rulează în containere Linux headless. Pentru unul sau mai multe job-uri izolate, inclusiv mai mulți workeri în paralel, folosește OrganizeFiles.Cli. Montează sursele read-only doar pentru simulare. Pentru **--execute** sursa trebuie să fie writable, fiindcă motorul mută fișierele din arborele sursă. Folosește ieșire dedicată, asigură drept valid din magazin sau publisher pentru toate rulările organize/repair (simulare și execute), apoi transmite **--source** (repetabil), **--output** și **--mode**. Fiecare worker care rulează în paralel are nevoie de propria rădăcină de ieșire. Folderul **Output** trebuie să existe deja pe gazdă înainte de a porni job-uri Docker sau Kubernetes (verificarea preliminară refuză o destinație lipsă și nu o creează). Exemple: containers/README.md și containers/docker-compose.sample.yml. `docker run` generat de Jobs/JobAgent montează sursele la `/in1`, `/in2`, … și ieșirea la `/out`. Exemplele manuale cu o singură sursă pot folosi `/in`, așa cum arată containers/README.md.
