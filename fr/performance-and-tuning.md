# Avancé / Diagnostics

## Organiser le réglage

Advanced/Diagnostics expose les options **OrganizeFilesEngine** sans encombrer le panneau principal.

Les modes d'organisation peuvent régler la déduplication, l'index de destination, les règles de date uniques, le thread de déplacement et d'énumération, le supplément BFS, le fichier de reprise et des racines uniques supplémentaires.

La réparation conserve uniquement le timing des tentatives de réseau et de disque plein, les voies matérielles graphiques détectées pour une vérification vidéo complète facultative, le tampon de lecture de hachage et le rythme cardiaque JSON. D'autres champs sont visibles pour le contexte mais désactivés.

Lorsque les sources ou la sortie vivent sur des chemins NAS ou UNC, réduisez le parallélisme, laissez la nouvelle tentative réseau activée, laissez le supplément BFS activé pour les arborescences SMB impaires et essayez le tampon de hachage de 8 Mio si le hachage est lent.

# Avancé/Diagnostics — chaque option

## À propos de ce chapitre

Ces contrôles sont des options du moteur. Le bureau (Windows, macOS, Linux), Android, iOS et l'outil en ligne de commande lisent les mêmes valeurs.

Les modes **Organiser** utilisent tous les contrôles ci-dessous, sauf lorsque l'interface les grise. **Réparation** n'utilise que la nouvelle tentative réseau, la nouvelle tentative sur disque plein, les voies matérielles graphiques détectées (avec vérification vidéo complète), le tampon de lecture de hachage, le JSON de battement, **Fichier d'état de reprise** et **Recommencer à zéro (tronquer le fichier de reprise)**. Les autres champs restent visibles mais sont ignorés lors de la réparation.

## Sources réseau (NAS / UNC)

Lorsque les sources ou la sortie se trouvent sur des partages SMB/CIFS, des volumes NAS ou des lecteurs mappés, lisez attentivement cette section.

- **Pourquoi régler** – Le nombre de threads qui fonctionnent sur un SSD local peut bloquer ou surcharger un gestionnaire de fichiers.
- **Que faut-il essayer** : conservez les nouvelles tentatives réseau. Réduisez le déplacement des threads et énumérez le nombre maximum de parallèles en cas d'expiration des délais. Laissez le supplément BFS activé, sauf si un décompte complet a été vérifié sans ce supplément. Essayez le tampon de hachage de 8 Mio lorsque le hachage est lent sur le réseau.
- **Désactiver l'attente réseau** : échoue rapidement en cas d'erreurs réseau transitoires. Risqué sur le Wi-Fi ou les partages occupés.

## Mode de déduplication

Comment le moteur décide que deux fichiers sont des doublons.

| Mode | Ce qu'il fait | Quand utiliser | Compromis |
| ---- | ------------ | ----------- | --------- |
| **Hachage (SHA-256)** | Lit et hache le contenu complet de chaque fichier source inclus, puis regroupe les octets identiques. | Mode pratique le plus puissant. Hash (SHA-256) est obligatoire pour la suppression sur place (doublons et fichiers problématiques). | Le plus lent sur les grands arbres ou NAS. Aucun algorithme ne doit être présenté comme une garantie absolue. |
| **Taille + heure + nom** | Clé = taille, ticks UTC de dernière écriture, nom en minuscule, puis vérification complète de SHA-256. | Mode de compatibilité conservateur pour les anciennes présentations de dossiers multimédias. | Peut manquer des doublons renommés. Ne jamais utiliser avec la suppression des doublons ni celle des fichiers problématiques. |
| **Aucun** | Pas de déduplication entre fichiers. | Tri uniquement, pas de nettoyage en double. | Les doublons restent dans les sources. |

## Ignorer l'index de destination

- **Désactivé (par défaut)** — Analyse la sortie **Unique** existante et l'indexe avant le hachage. Plus sûr lors de la réutilisation du même dossier de sortie.
- **Activé** : ignore cette analyse.
- **Avantage** — Plus rapide sur les arbres de sortie énormes.
- **Risque** – Davantage de contenu en double peut atterrir dans Unique.

## Année min. pour Uniques

Année civile minimale pour les dossiers de date sous **Unique** dans les mises en page multimédia. **Pourquoi** – Évite de disperser des fichiers très anciens dans des dossiers d'années impaires lorsque les métadonnées sont erronées.

## Déplacer les threads

Les fichiers parallèles se déplacent une fois les destinations réservées.

- **Plus élevé** — Plus rapide sur le SSD local.
- **Inférieur** — Plus sûr sur les lecteurs mappés NAS, USB ou Wi-Fi.

## Threads de classement et de hachage

Fils d'exécution parallèles pendant l'analyse des sources et la déduplication SHA-256.

- **Fils de classement** — Découverte et classement des fichiers. En ligne de commande : `--classify-threads <n>`.
- **Fils de hachage** — Fils qui hachent le contenu. En ligne de commande : `--hash-threads <n>`.
- **Remplacements** — Les valeurs manuelles remplacent les valeurs par défaut du profil (`--profile`).

## Enum parallèle max

Limite pour la liste des répertoires parallèles pendant l'analyse.

- **0** = moteur automatique.
- **Inférieur** — Moins de pression sur SMB lorsque plusieurs dossiers sont répertoriés en même temps.

## Supplément BFS Répertoire

- **Activé (par défaut)** — Un parcours supplémentaire en largeur, peu profond.
- **Pourquoi** — Certains chemins NAS ou arbres profonds paraissent incomplets après le premier parcours.
- **Désactivé** — Seulement après avoir vérifié un décompte complet des fichiers sans lui.
- **CLI** — `--no-bfs` désactive ce parcours.

## Reprendre le fichier d'état

Chemin UTF-8 facultatif. Les mouvements réussis ajoutent des lignes `B64|` afin que la prochaine exécution d'organisation puisse ignorer les sources terminées.

- **Pourquoi** – Poursuivre les tâches longues après un arrêt ou un crash.
- **Chemin par défaut** — Lorsque le champ est vide au moment de l'exécution, le moteur utilise `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt`. Sans sortie, il utilise `sessions\<id>\resume\OrganizeFiles.resume.txt` sous le profil de l'application.
- **Interface utilisateur de bureau** : liste de chemins en lecture seule pour la sélection et la copie avec la souris. Lorsqu'un fichier de reprise existe déjà à l'emplacement par défaut, le chemin apparaît automatiquement. **Parcourir** sélectionne un dossier de journaux et ajoute `OrganizeFiles.resume.txt`. **Supprimer** efface le chemin. Lorsqu'il est vide, l'indice affiche le chemin utilisé au moment de l'exécution.

## Start Fresh

Tronque le fichier de reprise lorsqu'une **véritable** exécution d'organisation démarre (la simulation ne tronque pas). Avec **Enregistrer la progression et l'espace de travail**, efface également l'instantané de l'interface utilisateur enregistré au démarrage de l'exécution. **Pourquoi** – Forcez un recomptage complet au lieu de poursuivre un ancien journal de reprise.

## Racines d'analyse uniques

Un dossier par ligne : arbres **Unique** supplémentaires à indexer (ancienne disposition, autre volume).

- **Pourquoi** — La déduplication voit les fichiers déjà rangés ailleurs sans les déplacer une seconde fois.
- **Interface de bureau** — Liste en lecture seule, pour copier ligne à ligne. **Ajouter** ajoute un dossier choisi. **Retirer** supprime la ligne sélectionnée (par exemple un ancien arbre `Uniques` sur un NAS).

## Nouvelle tentative réseau (secondes)

Secondes pendant lesquelles réessayer les entrées-sorties réseau passagères.

- **Pourquoi** — Les serveurs SMB coupent les sessions inactives. Utilisé par l'organisation et la réparation.
- **Désactiver l'attente réseau** — Cesser d'attendre et échouer à la place.

## Nouvelle tentative de disque plein

(secondes) /

Désactiver l'attente de disque plein

Même modèle lorsque le volume de sortie manque d'espace. **Pourquoi** – Il est temps de libérer le disque lors de longues exécutions.

## Voies de la carte graphique

Seulement quand la **vérification vidéo complète** intégrée est activée et que **Utiliser la carte graphique détectée** l'est aussi. Une valeur supérieure à **0** fixe un nombre de voies explicite pour la vérification en parallèle chez les fabricants détectés (NVIDIA, AMD, Intel, Apple, mobile). **0** signifie que le nombre de voies est trouvé tout seul. Cela ne veut pas dire processeur seul. Pour un échantillonnage sur le processeur seul, choisissez **Processeur seul** dans la liste des cartes graphiques. Les étiquettes de voie planifient la vérification du flux binaire sur le processeur. Elles n'appellent pas le décodage vidéo matériel du système.

- **Préréglage en ligne de commande** — `--hwaccel <value>` choisit un préréglage de voies de vérification (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`) quand la vérification vidéo complète est lancée.

## Tampon de lecture de hachage

Tampon de lecture par travailleur pendant le hachage (512 Ko, 1 MiB, 8 MiB). **Pourquoi** – Des tampons plus grands aident lorsque le NAS ou le partage à forte latence répond lentement.

## Enregistrer le journal des annulations

Journal JSONL facultatif des déplacements sous la racine de sortie de l exécution.

- **Pourquoi** — Permet l annulation via la CLI après une exécution réelle.
- **Archivage** — L archivage après organisation reste désactivé tant que le journal est actif.
- **CLI** — `--record-undo-journal` (identique à la case de la fenêtre principale).

## Écrire le rythme cardiaque d'exécution

Écrit le fichier facultatif `Organize.Files.run.json` sous `Output\_OrganizeMediaLogs`.

- **Pourquoi** — Des outils extérieurs peuvent lire les compteurs en direct (parcourus, planifiés, terminés) pendant l'organisation ou la réparation.
- **Cadence** — Tous les 10 000 fichiers vus, toutes les 5 000 correspondances et toutes les 15 secondes environ pendant le parcours des sources, après chaque tranche de 1 000 fichiers et au plus toutes les cinq secondes pendant la validation, le hachage et les déplacements, et à chaque phase importante.
