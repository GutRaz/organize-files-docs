# Surveillance avec Prometheus et Grafana

## Ce que couvrent les compteurs

Les travaux planifiés tiennent un petit ensemble de compteurs et de jauges Prometheus. Chaque nom commence par `organize_files_automation_`, et l'ensemble est publié en texte Prometheus. Les trois hôtes qui exécutent des travaux publient le même ensemble : l'application de bureau, le service `OrganizeFiles.JobAgent` et l'hôte en ligne de commande utilisé dans les conteneurs.

Les compteurs décrivent le planificateur, pas les fichiers. Sont comptés les passes, les issues des travaux, les approbations, la livraison des webhooks et l'entretien de l'historique. Rien n'est compté au sujet des fichiers qu'un travail déplace.

## Export dans un fichier, sans port ouvert

`automation-metrics.prom` est écrit dans le dossier de données d'automatisation, à côté de `automation-jobs.json`, et rafraîchi après chaque passe échue et à chaque relevé. La mise en forme est celle que lit le collecteur textfile de `node_exporter`, donc une machine qui exécute déjà `node_exporter` est couverte sans port en écoute, sans jeton et sans règle de pare-feu. Le fichier est remplacé de façon atomique, et un lien symbolique laissé à sa place arrête l'écriture au lieu d'être suivi.

## Point de relevé

Le point de relevé n'existe que si `ORGANIZE_FILES_METRICS_HTTP_PORT` contient un port compris entre 1 et 65535. Sans cette variable, rien n'écoute.

| Variable | Effet |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | Port d'écoute. Absent ou hors plage, il n'y a aucun point de relevé. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Adresse d'écoute. La valeur par défaut est `127.0.0.1`. Les valeurs `0.0.0.0`, `+` et `*` désignent toutes les adresses, et toute autre valeur retombe sur `127.0.0.1`. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | Jeton bearer exigé sur `/metrics` et sur `/ready`. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` laisse `/ready` répondre sans ce jeton, pour les sondes de cluster. Les chemins de l'hôte sont alors absents de la réponse. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | Codes de sortie séparés par des virgules qui font répondre `/ready` non prêt. Remplace la liste intégrée. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` ignore le code de sortie de la dernière passe, ainsi que l'état précédant la fin de la première. |
| `ORGANIZE_FILES_READY_JSON` | `1` impose la réponse JSON sur `/ready`, même pour un appelant qui a demandé du texte brut. |

Une adresse hors boucle locale est refusée avant l'ouverture de l'écouteur si aucun jeton bearer n'est défini. Le refus est écrit sur la sortie d'erreur et émis comme événement webhook, car cette combinaison livrerait les compteurs à tout le réseau.

## Chemins servis

- `/metrics` — les compteurs en texte Prometheus. Une requête vers `/` renvoie le même contenu.
- `/ready` — l'état de préparation pour un orchestrateur. La réponse est `200` dès que le dossier d'automatisation accepte une écriture de test, que le fichier des travaux s'ouvre, que le dossier d'historique se résout dans la racine de données et que la dernière passe échue s'est terminée sur un code de sortie qui ne bloque pas. Sinon la réponse est `503` avec un motif court tel que `due_pass_not_completed` ou `last_due_pass_license_failed`.
- `/health` — signe de vie uniquement. Ce chemin reste anonyme même quand un jeton est défini, car il répond `ok` et rien d'autre.

Les codes de sortie `3` pour un échec de licence, `8` pour une arborescence de sortie verrouillée, `10` pour une suppression jamais confirmée et `11` pour un conflit de revendication bloquent la préparation par défaut. Le corps de `/ready` est du JSON sauf si l'appelant envoie `Accept: text/plain` ou ajoute `?format=text`.

## Les compteurs

| Nom | Contenu |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Passes échues entamées par le planificateur. |
| `organize_files_automation_jobs_started_total` | Exécutions de travaux parvenues à l'état en cours. |
| `organize_files_automation_jobs_skipped_total` | Travaux écartés : environnement Docker ou Kubernetes non prêt, travail ciblant l'application sur un hôte sans interface, racine de sortie occupée, ou travail refusé par l'orchestrateur. |
| `organize_files_automation_jobs_failed_total` | Exécutions de travaux terminées en échec. |
| `organize_files_automation_jobs_awaiting_approval_total` | Exécutions réelles mises en attente d'approbation. |
| `organize_files_automation_execute_approvals_total` | Approbations accordées pour une exécution réelle. |
| `organize_files_automation_execute_approvals_expired_total` | Approbations dont le délai a expiré avant usage. |
| `organize_files_automation_claim_conflicts_total` | Fois où un autre hôte détenait déjà la revendication sur la racine de sortie. |
| `organize_files_automation_runs_orphaned_total` | Exécutions récupérées comme orphelines, laissées par un hôte arrêté. |
| `organize_files_automation_job_events_total` | Un compteur par événement, avec les étiquettes `event`, `job_id`, `target` et `jobs_file`. |
| `organize_files_automation_webhook_posts_succeeded_total` | Livraisons webhook acceptées. |
| `organize_files_automation_webhook_posts_failed_total` | Livraisons webhook refusées ou injoignables. |
| `organize_files_automation_webhook_dead_letter_depth` | Lignes en attente à cet instant dans le fichier webhook des messages non remis. |
| `organize_files_automation_log_retention_pruned_total` | Journaux d'exécution supprimés par la rétention. |
| `organize_files_automation_runs_index_compacted_total` | Lignes retirées de l'index des exécutions lors du compactage. |
| `organize_files_automation_last_due_pass_exit_code` | Code de sortie de la dernière passe terminée. `0` désigne une passe propre. |
| `organize_files_automation_last_due_pass_completed_utc` | Heure Unix en secondes de la dernière passe terminée, et `0` avant la première. |

## Tableau de bord et règles d'alerte

Un tableau de bord Grafana prêt à l'emploi est publié avec les fichiers de déploiement sous le nom `grafana-organize-files-automation.json`, avec le titre **OrganizeFiles Automation**. Ses dix panneaux montrent les passes échues, les travaux démarrés et en échec, les conflits de revendication, le débit de travaux sur une heure, le dernier code de sortie, la profondeur des messages non remis, les échecs webhook sur une journée, les travaux en attente d'approbation et les événements de travaux par état. Chaque panneau nomme sa source de données par l'espace réservé `${DS_PROMETHEUS}`.

Les règles d'alerte correspondantes sont `alerts-organize-files-automation.yaml`, avec `prometheus-rule-automation.yaml` comme enveloppe Kubernetes pour `kube-prometheus-stack`. Un dernier code de sortie non nul avertit au bout de cinq minutes, un échec de licence est critique au bout d'une minute, et les autres règles couvrent les travaux en échec, les conflits de revendication, les échecs webhook, un arriéré de messages non remis et les approbations laissées en attente une journée. Les deux fichiers sont validés à chaque compilation, afin que les noms ci-dessus restent alignés sur les compteurs.

# Sortie de l'exécution et métriques

## Ligne d'état

La zone **Sortie de l'exécution** affiche :

- État actuel de l'application et progression du moteur.
- **CPU** et deux valeurs de **mémoire** pour ce processus uniquement.
- Lignes **GPU**, sous Windows : la part de chaque carte graphique utilisée par ce processus, pas la carte entière.

La même barre de ressources compacte est réutilisée dans les fenêtres d'outils secondaires telles que l'exploration de fichiers, les tâches planifiées et la réparation de fichiers.

## Étiquettes de mémoire

- **Private bytes / commit** — mémoire virtuelle privée réservée par le processus.
- **Ensemble de travail/mémoire** — RAM résidente actuellement détenue par ce processus. Il peut différer d'un autre moniteur de système d'exploitation, car chaque étiquette de système d'exploitation et d'environnement de bureau traite la mémoire différemment.

## Exécuter le heartbeat JSON (facultatif)

Activez **Write run heartbeat JSON** sous **Advanced/Diagnostics**. Le moteur écrit `Organize.Files.run.json` sous `Output\_OrganizeMediaLogs` (même dossier que le fichier de reprise d'organisation par défaut).

- **Chemin** — mis à jour de manière atomique lors des exécutions d'organisation et de réparation.
- **Cadence** — pendant le parcours des sources, le fichier est réécrit tous les 10 000 fichiers vus, toutes les 5 000 correspondances et toutes les 15 secondes environ tant que le parcours se poursuit, si bien qu'un grand arbre réseau lent à lister montre quand même que l'exécution est vivante. Pendant la validation, le hachage et les déplacements, il est réécrit après chaque tranche de 1 000 fichiers, au plus toutes les cinq secondes. Les écritures de début et de fin ont toujours lieu au démarrage et à l'achèvement d'une exécution.
- **Avancement** — tant que le nombre de fichiers croît encore, la barre principale affiche les fichiers vus jusque-là plutôt que 100 %, jusqu'à ce qu'une phase connaisse son total.
- **Champs** — `schema`, `mode`, `phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`), `runState` (`active` / `completed` / `failed` / `cancelled`), `utc` (ISO-8601), `dryRun`, `outputRoot`, `validateMedia`, `deepVideoValidate`, `gpuDeviceCount`, `hwaccel`, en option `correlationId`, compteurs `progress` imbriqués.
- **Log** — le panneau de sortie d'exécution imprime le chemin complet au début et lorsque le fichier est enregistré à la fin. Utilisez **Ouvrir le dossier du journal de battement de coeur** / **Afficher le fichier JSON de battement de coeur** sous Avancé/Diagnostics.
- **CLI** — `--heartbeat-json` sur OrganizeFiles.Cli. Les erreurs d'annulation et fatales du shell écrivent `cancelled` / `failed` `runState` lorsqu'elles sont activées.
