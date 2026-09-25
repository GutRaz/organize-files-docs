# Conteneurs — configuration

## Ce qui est requis

Seul le programme `docker` ou `kubectl` doit être accessible sur la machine qui exécute le travail. Rien d'autre n'est nécessaire. Docker Desktop n'est pas une exigence. Docker Engine sous Linux, Rancher Desktop, colima et Podman avec une commande compatible Docker fonctionnent tous de la même manière, car l'application exécute simplement la commande qu'elle trouve sur le chemin du système.

Kubernetes fonctionne de la même manière. Tout cluster accessible via `kubectl` est pris en charge, y compris les clusters k3s, kind, minikube et gérés tels que EKS, GKE ou AKS.

## Utiliser un autre démon ou cluster

Pour envoyer des tâches à un autre démon Docker, définissez `DOCKER_HOST` ou basculez avec `docker context use`. Pour utiliser un autre cluster Kubernetes, changez le contexte actuel avec `kubectl config use-context`. L'application suit tout ce que la ligne de commande utilise déjà, donc aucun paramètre supplémentaire n'est nécessaire dans l'application.

## Où les fichiers sont montés

Pour Kubernetes, le dossier est joint de deux manières. Les contextes de développement locaux bénéficient d'un montage direct du dossier hôte. Cela couvre un contexte nommé `desktop`, `colima` ou `orbstack`, un contexte qui se termine par `@desktop`, un contexte qui commence par `kind-`, `minikube` ou `k3d-`, et un contexte dont le nom contient `docker-desktop`, `docker-for-desktop` ou `rancher-desktop`. Tout autre contexte est traité comme un cluster réel et obtient à la place une revendication de volume persistante, car un nœud de cluster réel ne peut pas voir les dossiers sur l'ordinateur de bureau. Régler `ORGANIZE_FILES_K8S_VOLUME_MODE` sur `pvc` ou `hostpath` remplace ce choix pour chaque contexte.

## Dossiers réseau sous Windows

Docker Desktop sous Windows ne peut pas attacher un chemin réseau tel que `\\server\share` à un conteneur Linux. Windows voit le dossier, mais pas le conteneur. Il existe deux façons de contourner ce problème. Utilisez un dossier sur un disque local, ou exécutez plutôt la tâche avec la cible App, qui effectue le travail dans l'application elle-même. Une lettre de lecteur associée au partage n'aide pas, car l'application remonte jusqu'au chemin réseau et la refuse de la même façon.

## Fichiers prêts à l'emploi

Les kits en ligne de commande pour Linux contiennent des fichiers prêts à l'emploi dans leur dossier `containers` : un Dockerfile qui construit l'image à partir du kit lui-même, un exemple Compose, des exemples de Job Kubernetes et `containers/README.md`, avec un README pour chaque langue à côté.

# Conteneurs et workers CLI

## Tâches planifiées — Cibles Docker et Kubernetes

Ouvrez **Tâches** à partir de la barre latérale de la fenêtre principale. Cliquez sur **Nouvelle tâche** ou **Modifier** sur une carte existante. Dans la liste déroulante **Cible**, sélectionnez **Commande Docker** ou **Tâche Kubernetes**.

1. Définissez **Sources de fichiers** (chemins d'accès à l'hôte) et **Sortie** (chemin d'accès à l'hôte — doit déjà exister avant l'exécution du travail).
2. Choisissez **Mode** et **Options d'exécution** comme pour toute autre tâche.
3. Le panneau **Aperçu de la commande** affiche la commande exacte « docker run » ou le YAML du travail Kubernetes qui sera appliqué.
4. **Enregistrez** la tâche et définissez un **Planification**, ou cliquez sur **Exécuter maintenant** sur la carte pour démarrer immédiatement.

L'application génère automatiquement les indicateurs de montage et les chemins de volume à partir de l'instantané enregistré. Le démon Docker ou `kubectl` doit être accessible sur la machine hôte. **Preflight** vérifie la connectivité et signale toute erreur dans le journal du travail avant le début de l'exécution. Pour le flux d'approbation, la récupération des journaux et la planification sans interface utilisateur, voir **Tâches planifiées**.

## Terminal de la machine hôte (PowerShell / bash / cmd)

Oui — sur la machine hôte, lancez **OrganizeFiles.Cli** depuis PowerShell, bash ou cmd. C'est la voie prise en charge pour un terminal. La fenêtre de bureau Avalonia est une interface graphique distincte. Publiez ou installez le kit CLI à côté de l'application (ou dans PATH), puis passez **--source** (répétable), **--output** et **--mode**. Commencez de préférence par un essai à blanc. N'ajoutez **--execute** qu'une fois prêt.

## Interface de bureau et conteneurs

Conteneurs et automatisation : l'interface graphique du bureau Avalonia n'est pas destinée à s'exécuter dans un conteneur Linux headless typique. Pour une ou plusieurs tâches isolées, y compris plusieurs travailleurs parallèles, utilisez le compagnon OrganizeFiles.Cli : dans chaque dossier source de montage de conteneur en lecture seule pour les tâches de prévisualisation de la simulation. Les mouvements réels avec **--execute** nécessitent un montage source inscriptible car le moteur déplace les fichiers hors de l'arborescence source. Utilisez un volume de sortie en lecture/écriture dédié, garantissez un droit valide du magasin ou de l'éditeur pour toutes les exécutions d'organisation/réparation (simulation et exécution), transmettez **--source** (répétable), **--output** et **--mode**. Chaque travailleur simultané a besoin de sa propre racine de sortie. Le dossier **Output** doit déjà exister sur l'hôte avant l'exécution des tâches Docker ou Kubernetes (le contrôle en amont refuse une destination manquante et ne la crée pas). Exemples de chemins : containers/README.md et containers/docker-compose.sample.yml. Jobs/JobAgent généré `docker run` monte les sources à `/in1`, `/in2`,… et sort à `/out`. Les exemples manuels à source unique peuvent utiliser `/in` (voir containers/README.md).
