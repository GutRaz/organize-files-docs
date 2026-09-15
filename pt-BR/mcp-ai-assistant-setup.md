# Assistente de IA (MCP)

Equipes licenciadas conectam o **OrganizeFiles.Cli** ao Claude Desktop, ao **Cursor**, ao VS Code Copilot ou a outro cliente do Model Context Protocol, chamado de cliente MCP a seguir. O conector é o pacote Python **organize-files-mcp**. O pacote é um download gratuito em github.com/GutRaz/organize-files-docs, na pasta `mcp/`.

**No aplicativo de desktop:** abra **Configuração do MCP…** em **Aplicativo e dados**, na coluna de opções, ou pelo menu de ferramentas. Escolha **Acesso MCP**: **Desligado**, **Monitor** ou **Controle**. Depois copie o trecho JSON. Recarregue o MCP no aplicativo de IA após cada mudança de nível, porque **Controle** cria um novo token a cada vez.

**Pergunte ao assistente de documentação** “setup mcp” ou “cum setez mcp” para ver os passos no sistema atual.

## Níveis de acesso MCP, definidos no aplicativo

Os níveis correspondem a três tipos de trabalho: **leitura / prévia / execução**.

| Nível | Tipo de trabalho | O que a IA pode fazer |
|-------|--------|-------------------|
| **Desligado** | — | Somente `organize_mcp_status`. Sem diagnóstico e sem acesso ao espaço de trabalho. |
| **Monitor** | **Leitura** | Tudo o que há em Desligado, mais diagnóstico somente leitura, histórico de execuções e tarefas, bloqueios, verificações de auditoria, **`organize_capabilities`** e **`organize_workspace_snapshot`**. `organize_capabilities` lista os modos de execução, entre eles **`ai`**, os escopos de movimentação e os destinos. `organize_workspace_snapshot` mostra o espaço de trabalho salvo na janela principal. Sem prévia e sem execução. |
| **Controle** | **Prévia** / **Execução** | Tudo o que há em Monitor, mais **`organize_create_job`**, **`organize_run_workspace`** e **`organize_remove_empty_organize_layout`**. Precisa de um **token de controle** nas configurações do MCP, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **Prévia** é `organize_run_workspace` quando o espaço de trabalho salvo está com **Simulação** ligada, então nada é gravado. **Execução** é a mesma ferramenta com Simulação desligada, então os arquivos são movidos. O conector omite `--confirm-destructive`, a menos que a chamada defina `confirm_destructive=true`, e sem essa opção a linha de comando recusa com `confirm_destructive_required`. |

O arquivo de controle é **`mcp-control.json`**, ao lado de `automation-jobs.json` na pasta de perfil do aplicativo. O trecho copiado não cita esse arquivo, porque o conector encontra o arquivo na pasta de perfil padrão. Defina **`ORGANIZE_FILES_MCP_CONTROL_FILE`** somente quando o arquivo estiver em outro lugar. Em **Controle**, o trecho também define **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`**.

**Mover e excluir exige um segundo passo, humano.** O assistente marca a própria confirmação, então um texto lido durante o trabalho poderia levar o assistente a confirmar. Por isso, uma execução que não é uma simulação também precisa de uma janela aberta em **Configuração do MCP**, e essa janela se fecha sozinha após 15 minutos. Fora dessa janela, o assistente ainda pode preparar uma execução e mostrar a prévia, mas a execução em si é recusada. Tanto o arquivo de controle quanto a janela são assinados com uma chave que esta instalação guarda. Um arquivo de controle alterado à mão ou copiado de outro computador conta como Desligado.

## Ferramentas MCP por nível

**Sempre, também em Desligado:** `organize_mcp_status`

**Monitor e Controle:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` e `organize_run_raw_cli`, que aceita apenas comandos somente leitura.

**Também em Monitor e Controle:** `organize_capabilities`, que lista o modo de execução **`ai`** para arquivos de IA e ML, e `organize_workspace_snapshot`.

**Somente Controle:** `organize_create_job` a partir do espaço de trabalho ou de um JSON de tarefa, `organize_run_workspace` para uma prévia ou uma execução real conforme a Simulação do espaço de trabalho, e `organize_remove_empty_organize_layout`, que remove pastas de layout vazias dentro de uma saída existente e nunca cria a própria pasta de saída.

Comandos que movem ou excluem arquivos são sempre bloqueados pelo MCP fora do nível **Controle**. Nenhuma outra configuração permite esses comandos.

## Opções de linha de comando que o conector usa

| Opção | Nível | Finalidade |
|------|-------|---------|
| `--mcp-control-status` | qualquer | JSON com o nível, o caminho do arquivo de controle e os indicadores de Monitor e Controle |
| `--mcp-capabilities` | Monitor ou superior | Lista JSON dos modos de execução, entre eles **`ai`**, dos escopos de movimentação e dos destinos |
| `--mcp-workspace-snapshot` | Monitor ou superior | O espaço de trabalho salvo e como esse espaço vira uma tarefa |
| `--mcp-create-job` | Controle | Cria uma tarefa com `--from-workspace` ou `--mcp-job-json` |
| `--mcp-run-workspace` | Controle | Executa o espaço de trabalho salvo, com `--allow-app-target` e `--mcp-control-token` |
| `--remove-empty-organize-layout` | Controle | Remove pastas de layout vazias dentro de um `--output` existente |
| `--confirm-destructive` | Controle | Necessária com `--mcp-run-workspace` para uma execução que move ou exclui. O conector só repassa essa opção quando `confirm_destructive=true` |

## Configurações no JSON do cliente MCP

| Configuração | Quando |
|----------|------|
| `ORGANIZE_FILES_CLI` | Caminho para OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | Caminho para `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | Caminho para `mcp-control.json`, somente quando o arquivo não está na pasta de perfil padrão |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | Somente nível **Controle**, do trecho do aplicativo |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | Nível **Controle**, para execuções do espaço de trabalho salvo |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | Opcional. O mesmo token que o host usa para operações de leitura |

## Configuração no Windows

1. **Python 3.10 ou mais recente** — execute `python -V` no PowerShell. Se o Python estiver ausente ou for mais antigo, instale o Python a partir de [python.org](https://www.python.org/downloads/) e marque **Add python.exe to PATH**.
2. **Baixe e instale o conector** — baixe github.com/GutRaz/organize-files-docs como ZIP, extraia o arquivo e execute `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1`. O script cria um ambiente Python próprio para o conector e mostra o comando para o aplicativo de IA.
3. **No aplicativo:** **Configuração do MCP…**, escolha **Monitor** ou **Controle** e depois copie o JSON.
4. **Caminhos:** `%LocalAppData%\OrganizeFilesCrossPlatform\` guarda as tarefas e `mcp-control.json`. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **Teste** — execute `organize_mcp_status` e depois `organize_server_info`. `cliResolved` deve ser true e `mcpLevel` deve corresponder ao aplicativo.

## Configuração no macOS

Os mesmos passos com **python3** e `bash mcp/install-organize-files-mcp.sh`. Se `python3 -V` mostrar 3.9 ou nenhum Python, instale primeiro o Python a partir de [python.org](https://www.python.org/downloads/macos/). Caminhos: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Configuração no Linux

Os mesmos passos com **python3** e `bash mcp/install-organize-files-mcp.sh`. No Debian e no Ubuntu, execute primeiro `sudo apt install python3-venv`. Caminhos: `~/.local/share/OrganizeFilesCrossPlatform/`, ou `$XDG_DATA_HOME` quando estiver definida, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Segurança

- O MCP é executado como **o usuário local** do sistema operacional, com os mesmos direitos da linha de comando executada manualmente.
- Mantenha em segredo o **token de controle** e o **token de leitura**, como senhas. Copie o JSON novamente depois de ligar o Controle.
- **`organize_run_workspace`** é executado na linha de comando, não pelo botão Executar do aplicativo. Não execute duas tarefas na mesma pasta de saída ao mesmo tempo.
- Exemplos: `mcp/examples/`.

## Execuções que movem ou excluem

`--mcp-run-workspace` exige `--confirm-destructive` para toda execução que não seja uma simulação, seja para mover, excluir ou arquivar. Sem essa opção, a linha de comando responde `confirm_destructive_required`. O conector omite a opção, a menos que a chamada defina `confirm_destructive=true`, e só o nível Controle pode fazer isso. Então, por padrão, o conector recusa.

## Idiomas

As respostas sobre a configuração vêm do mesmo guia traduzido que a janela Documentação e o Assistente de guia. `organize_capabilities` informa modos de execução e destinos, não nomes de temas do aplicativo.
