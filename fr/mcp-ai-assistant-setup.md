# Assistant IA (MCP)

Les équipes sous licence connectent **OrganizeFiles.Cli** à Claude Desktop, **Cursor**, VS Code Copilot ou un autre client Model Context Protocol, appelé client MCP ci-dessous. Le connecteur est le paquet Python **organize-files-mcp**. C'est un téléchargement gratuit depuis github.com/GutRaz/organize-files-docs, dans son dossier `mcp/`.

**Dans l'application de bureau :** ouvrez **Configuration MCP…** sous **Application et données** dans la colonne des options, ou depuis le menu des outils. Choisissez **Accès MCP** : **Désactivé**, **Moniteur** ou **Contrôle**. Copiez ensuite l'extrait JSON. Rechargez MCP dans l'application d'IA après chaque changement de niveau, car **Contrôle** crée un nouveau jeton à chaque fois.

**Demandez à l'assistant de documentation** « setup mcp » ou « cum setez mcp » pour les étapes sur le système actuel.

## Niveaux d'accès MCP, réglés dans l'application

Les niveaux correspondent à trois sortes de travail : **Lecture / Aperçu / Exécution**.

| Niveau | Sorte de travail | Ce que l'IA peut faire |
|-------|--------|-------------------|
| **Désactivé** | — | Seulement `organize_mcp_status`. Aucun diagnostic et aucun accès à l'espace de travail. |
| **Moniteur** | **Lecture** | Tout ce que permet Désactivé, plus les diagnostics en lecture seule, l'historique des exécutions et des tâches, les verrous, les contrôles d'audit, **`organize_capabilities`** et **`organize_workspace_snapshot`**. `organize_capabilities` liste les modes d'exécution, dont **`ai`**, les portées de déplacement et les cibles. `organize_workspace_snapshot` montre l'espace de travail enregistré dans la fenêtre principale. Pas d'aperçu et pas d'exécution. |
| **Contrôle** | **Aperçu** / **Exécution** | Tout ce que permet Moniteur, plus **`organize_create_job`**, **`organize_run_workspace`** et **`organize_remove_empty_organize_layout`**. Il faut un **jeton de contrôle** dans les réglages MCP, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **Aperçu** correspond à `organize_run_workspace` quand l'espace de travail enregistré a **Simulation** activée, donc rien n'est écrit. **Exécution** correspond au même outil avec Simulation désactivée, donc les fichiers sont déplacés. Le connecteur omet `--confirm-destructive` sauf si l'appel définit `confirm_destructive=true`, et sans cette option la ligne de commande refuse avec `confirm_destructive_required`. |

Le fichier de contrôle est **`mcp-control.json`**, à côté de `automation-jobs.json` dans le dossier de profil de l'application. L'extrait copié ne le nomme pas, car le connecteur le trouve lui-même dans le dossier de profil par défaut. Définissez **`ORGANIZE_FILES_MCP_CONTROL_FILE`** seulement quand le fichier se trouve ailleurs. Au niveau **Contrôle**, l'extrait définit aussi **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`**.

**Déplacer et supprimer demande une seconde étape, humaine.** L'assistant coche lui-même sa confirmation, donc un texte qu'il lit pourrait l'amener à confirmer. Une exécution qui n'est pas une simulation exige donc aussi une fenêtre ouverte dans **Configuration MCP**, laquelle se referme d'elle-même au bout de 15 minutes. En dehors, l'assistant peut toujours préparer et prévisualiser une exécution, mais l'exécution elle-même est refusée. Le fichier de contrôle et la fenêtre sont tous deux signés avec une clé que garde cette installation. Un fichier de contrôle modifié à la main ou copié depuis un autre ordinateur compte comme Désactivé.

## Outils MCP par niveau

**Toujours, même à Désactivé :** `organize_mcp_status`

**Moniteur et Contrôle :** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` et `organize_run_raw_cli`, qui n'accepte que des commandes de lecture.

**Aussi dans Moniteur et Contrôle :** `organize_capabilities`, qui liste le mode d'exécution **`ai`** pour les fichiers d'IA et de ML, et `organize_workspace_snapshot`.

**Contrôle uniquement :** `organize_create_job` depuis l'espace de travail ou depuis un JSON de tâche, `organize_run_workspace` pour un aperçu ou une vraie exécution selon la Simulation de l'espace de travail, et `organize_remove_empty_organize_layout`, qui supprime les dossiers de disposition vides dans une sortie existante et ne crée jamais le dossier de sortie lui-même.

Les commandes qui déplacent ou suppriment des fichiers sont toujours bloquées par MCP en dehors du niveau **Contrôle**. Aucun autre réglage ne les autorise.

## Options de ligne de commande utilisées par le connecteur

| Option | Niveau | Rôle |
|------|-------|---------|
| `--mcp-control-status` | tous | JSON avec le niveau, le chemin du fichier de contrôle et les indicateurs Moniteur et Contrôle |
| `--mcp-capabilities` | Moniteur et plus | Liste JSON des modes d'exécution, dont **`ai`**, des portées de déplacement et des cibles |
| `--mcp-workspace-snapshot` | Moniteur et plus | L'espace de travail enregistré et sa correspondance avec une tâche |
| `--mcp-create-job` | Contrôle | Créer une tâche avec `--from-workspace` ou `--mcp-job-json` |
| `--mcp-run-workspace` | Contrôle | Exécuter l'espace de travail enregistré, avec `--allow-app-target` et `--mcp-control-token` |
| `--remove-empty-organize-layout` | Contrôle | Supprimer les dossiers de disposition vides dans un `--output` existant |
| `--confirm-destructive` | Contrôle | Nécessaire avec `--mcp-run-workspace` pour une exécution qui déplace ou supprime. Le connecteur ne la transmet que si `confirm_destructive=true` |

## Réglages dans le JSON du client MCP

| Réglage | Quand |
|----------|------|
| `ORGANIZE_FILES_CLI` | Chemin vers OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | Chemin vers `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | Chemin vers `mcp-control.json`, seulement s'il n'est pas dans le dossier de profil par défaut |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | Niveau **Contrôle** uniquement, depuis l'extrait de l'application |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | Niveau **Contrôle**, pour les exécutions de l'espace de travail enregistré |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | Facultatif. Le même jeton que l'hôte utilise pour les opérations de lecture |

## Configuration Windows

1. **Python 3.10 ou plus récent** — exécutez `python -V` dans PowerShell. Si Python manque ou est plus ancien, installez-le depuis [python.org](https://www.python.org/downloads/) et cochez **Add python.exe to PATH**.
2. **Télécharger et installer le connecteur** — téléchargez github.com/GutRaz/organize-files-docs en ZIP, décompressez-le et exécutez `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1`. Le script crée un environnement Python propre au connecteur et affiche la commande pour l'application d'IA.
3. **Dans l'application :** **Configuration MCP…**, choisissez **Moniteur** ou **Contrôle**, puis copiez le JSON.
4. **Chemins :** `%LocalAppData%\OrganizeFilesCrossPlatform\` contient les tâches et `mcp-control.json`. Cursor : `%USERPROFILE%\.cursor\mcp.json`. Claude : `%APPDATA%\Claude\claude_desktop_config.json`. VS Code : `%USERPROFILE%\.vscode\mcp.json`.
5. **Test** — exécutez `organize_mcp_status`, puis `organize_server_info`. `cliResolved` doit valoir true et `mcpLevel` doit correspondre à l'application.

## Configuration macOS

Les mêmes étapes avec **python3** et `bash mcp/install-organize-files-mcp.sh`. Si `python3 -V` affiche 3.9 ou aucun Python, installez d'abord Python depuis [python.org](https://www.python.org/downloads/macos/). Chemins : `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Configuration Linux

Les mêmes étapes avec **python3** et `bash mcp/install-organize-files-mcp.sh`. Sur Debian et Ubuntu, exécutez d'abord `sudo apt install python3-venv`. Chemins : `~/.local/share/OrganizeFilesCrossPlatform/`, ou `$XDG_DATA_HOME` quand il est défini, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Sécurité

- MCP s'exécute en tant qu'**utilisateur local** du système d'exploitation, avec les mêmes droits que la ligne de commande lancée à la main.
- Gardez secrets le **jeton de contrôle** et le **jeton de lecture**, comme des mots de passe. Copiez de nouveau le JSON après avoir activé Contrôle.
- **`organize_run_workspace`** s'exécute dans la ligne de commande, pas par le bouton Exécuter de l'application. Ne lancez pas deux tâches sur le même dossier de sortie en même temps.
- Exemples : `mcp/examples/`.

## Exécutions qui déplacent ou suppriment

`--mcp-run-workspace` exige `--confirm-destructive` pour toute exécution qui n'est pas une simulation, qu'elle déplace, supprime ou archive. Sans elle, la ligne de commande répond `confirm_destructive_required`. Le connecteur omet l'option sauf si l'appel définit `confirm_destructive=true`, ce que seul le niveau Contrôle peut faire. Par défaut, le connecteur refuse donc.

## Langues

Les réponses sur la configuration viennent du même guide traduit que la fenêtre Documentation produit et l'Assistant-guide. `organize_capabilities` indique les modes d'exécution et les cibles, pas les noms des thèmes de l'application.
