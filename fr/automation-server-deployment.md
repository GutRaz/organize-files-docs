# CLI, Docker et Kubernetes (mise en page de référence)

## Automatisation de la CLI

Ce chapitre suit le style Microsoft/HashiCorp : ligne d'utilisation, table de flags (jetons anglais), puis exemples copier-coller.

CLI (OrganizeFiles.Cli)
  UTILISATION : OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  UTILISATION : OrganizeFiles.Cli --output <dir> --mode repair [options]

  Drapeau (long) | Signification
  -------------------------|--------------------------------------------
  --execute | Mouvements réels (par défaut, simulation uniquement).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | Fichier de reprise UTF-8 avec B64| lignes.
  --delete-duplicates | Supprimez les candidats en double (nécessite --confirm-delete avec --execute).
  --delete-issues | Supprimez les candidats de la tranche de problèmes (nécessite --confirm-delete avec --execute). Pas sur les cibles d'automatisation à distance.
  --archive-after-organize | Après l'organisation : ZIP frère par fichier, puis supprimez les originaux (nécessite --confirm-delete avec --execute). Ignore les extensions déjà archivées.

  **Remarque :** La CLI `--mode models` sélectionne les **modèles CAO/3D**, pas les artefacts IA. Utilisez `--mode ai` ou `--mode models-ai` pour AI/ML.

  Exemple (simulation, toutes les catégories) : OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Exemple (uniquement les déplacements vers Unique, exécuter) : OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Compilation : docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Simulation : docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  Pour --execute, supprimez :ro du montage source. Voir containers/README.md pour les règles multi-workers (une racine de sortie par worker).

Kubernetes (Travail de référence)
  Les PVC sources en lecture seule sont valides pour les travaux en simulation. Les mouvements réels avec --execute nécessitent des PVC sources inscriptibles. Fournissez un droit valide au magasin ou à l'éditeur pour toutes les exécutions d'organisation/réparation (simulation et exécution). Un pod par arborescence de sortie. Un modèle minimal est documenté dans containers/README.md avec un exemple de manifeste.

Progression des tâches
  La fenêtre Tâches affiche la progression des exécutions App, CLI, Docker et Kubernetes. Les étapes dont le total est connu affichent un pourcentage. Les analyses sans total restent indéterminées.
  L'automatisation lance le processus de travail CLI avec ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 et retire ces lignes de marqueur du journal visible. Une exécution CLI lancée à la main n'émet aucun marqueur tant que cette variable n'est pas définie.
  Les processus de travail Docker et Kubernetes reçoivent la même variable, donc ces exécutions affichent aussi un pourcentage. La valeur est lue dans le journal du processus de travail, elle apparaît donc dès que le conteneur ou le pod commence à écrire.
  --list-running et --show-run portent des champs de progression pour les tâches actives lorsque l'exécution a signalé quelque chose.

# Exemples d'exécution

## Interface utilisateur graphique

Ajoutez **Sources de fichiers** et le dossier de sortie, choisissez le mode d’exécution, activez **Simulation** pour un aperçu, puis appuyez sur **Exécuter**. Laissez **Simulation** décoché pour des déplacements réels. Les options de suppression demandent une confirmation avant l’exécution.

## Exemples CLI

CLI Simulation : OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
