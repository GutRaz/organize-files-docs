# CLI, Docker e Kubernetes (layout de referência)

## Automação CLI

Este capítulo segue o estilo Microsoft/HashiCorp: linha de uso, tabela de sinalizadores (tokens em inglês) e exemplos de copiar e colar.

CLI (OrganizeFiles.Cli)
  USO: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  USO: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Bandeira (longa) | Significado
  -------------------------|-------------------------------------------
  --execute | Movimentos reais (o padrão é apenas simulação).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | Arquivo de retomada UTF-8 com B64| linhas.
  --delete-duplicates | Exclua candidatos duplicados (precisa de --confirm-delete com --execute).
  --delete-issues | Exclua candidatos de bucket de problemas (precisa de --confirm-delete com --execute). Não em alvos de automação remota.
  --archive-after-organize | Após organizar: ZIP irmão por arquivo e exclua os originais (precisa de --confirm-delete com --execute). Ignora extensões já arquivadas.

  **Observação:** CLI `--mode models` seleciona **modelos CAD/3D**, não artefatos de IA. Use `--mode ai` ou `--mode models-ai` para AI/ML.

  Exemplo (ensaio, todos os buckets): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Exemplo (apenas movimentos únicos, execute): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Construir: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Teste: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  Para --execute, remova :ro da montagem de origem. Consulte containers/README.md para regras de vários workers (uma raiz de saída por worker).

Kubernetes (trabalho de referência)
  Os PVCs de origem somente leitura são válidos para trabalhos de simulação. Movimentos reais com --execute precisam de PVCs de origem graváveis. Forneça direitos válidos de armazenamento ou editor para todas as execuções de organização/reparo (ensaio e execução). Um pod por árvore de saída. Um padrão mínimo está documentado em containers/README.md junto com um exemplo de manifesto.

Progresso das tarefas
  A janela Tarefas mostra o progresso das execuções App, CLI, Docker e Kubernetes. As etapas com total conhecido mostram uma porcentagem. As varreduras sem total permanecem indeterminadas.
  A automação inicia o processo de trabalho CLI com ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 e remove essas linhas de marca do registro visível. Uma execução CLI iniciada à mão não emite marcas a menos que essa variável esteja definida.
  Os processos de trabalho do Docker e do Kubernetes recebem a mesma variável, então essas execuções também informam porcentagem. O valor é lido do registro do processo de trabalho, então aparece assim que o contêiner ou o pod começa a escrever.
  --list-running e --show-run levam campos de progresso para as tarefas ativas quando a execução informou algo.

# Exemplos de execução

## UI gráfica

Adicione **Origens** e a pasta de saída, escolha o modo de execução, ative **Execução de teste** para uma prévia e pressione **Executar**. Deixe **Execução de teste** desmarcado para mover de verdade. As opções de exclusão pedem confirmação antes de executar.

## Exemplos de CLI

CLI Simulação: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
