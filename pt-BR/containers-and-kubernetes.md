# Contêineres — configuração

## O que é necessário

Somente o programa `docker` ou `kubectl` deve estar acessível na máquina que executa o trabalho. Nada mais é necessário. Docker Desktop não é um requisito. Docker Engine no Linux, Rancher Desktop, colima e Podman com um comando compatível com docker funcionam da mesma maneira, porque o aplicativo simplesmente executa o comando que encontra no caminho do sistema.

Kubernetes funciona da mesma forma. Qualquer cluster acessível por meio de `kubectl` é compatível, incluindo k3s, kind, minikube e clusters gerenciados, como EKS, GKE ou AKS.

## Usando um daemon ou cluster diferente

Para enviar trabalhos para outro daemon Docker, defina `DOCKER_HOST` ou alterne com `docker context use`. Para usar outro cluster Kubernetes, alterne o contexto atual com `kubectl config use-context`. O aplicativo segue tudo o que a linha de comando já usa, portanto, nenhuma configuração extra é necessária dentro do aplicativo.

## Onde os arquivos são montados

Para Kubernetes, a pasta é anexada de duas maneiras. Os contextos de desenvolvimento local obtêm uma montagem direta na pasta do host. Isso abrange um contexto chamado `desktop`, `colima` ou `orbstack`, um que termina em `@desktop`, um que começa com `kind-`, `minikube` ou `k3d-`, e um cujo nome contém `docker-desktop`, `docker-for-desktop` ou `rancher-desktop`. Todos os outros contextos são tratados como um cluster real e, em vez disso, recebem uma declaração de volume persistente, porque um nó de cluster real não pode ver as pastas na máquina desktop. Definir `ORGANIZE_FILES_K8S_VOLUME_MODE` como `pvc` ou `hostpath` substitui essa escolha para todos os contextos.

## Pastas de rede no Windows

O Docker Desktop no Windows não pode anexar um caminho de rede como `\\server\share` a um contêiner Linux. O Windows vê a pasta, mas o contêiner não. Existem duas maneiras de contornar isso. Use uma pasta em um disco local ou execute o trabalho com o destino App, que faz o trabalho no próprio aplicativo. Uma letra de unidade mapeada para o compartilhamento não resolve, porque o aplicativo a segue até o caminho de rede e a recusa da mesma forma.

## Arquivos prontos

Os kits de linha de comando para Linux trazem arquivos prontos na pasta `containers`: um Dockerfile que cria a imagem a partir do próprio kit, um exemplo de Compose, exemplos de Job do Kubernetes e `containers/README.md`, com um README para cada idioma ao lado.

# Contêineres e workers CLI

## Jobs agendados — alvos Docker e Kubernetes

Abra **Trabalhos** na barra lateral da janela principal. Clique em **Novo trabalho** ou **Editar** em um cartão existente. No menu suspenso **Destino**, selecione **Comando do Docker** ou **Trabalho do Kubernetes**.

1. Defina **Origens** (caminhos de host) e **Saída** (caminho de host — já deve existir antes da execução do trabalho).
2. Escolha **Modo** e **Opções de execução** como para qualquer outro trabalho.
3. O painel **Visualização do comando** mostra o comando `docker run` exato ou YAML do trabalho do Kubernetes que será aplicado.
4. **Salve** o trabalho e defina um **Programação** ou clique em **Executar agora** no cartão para começar imediatamente.

O aplicativo gera sinalizadores de montagem e caminhos de volume automaticamente a partir do instantâneo salvo. O daemon Docker ou `kubectl` deve estar acessível na máquina host. **Preflight** verifica a conectividade e relata quaisquer erros no log de trabalho antes do início da execução. Para o fluxo de aprovação, recuperação de log e agendamento headless, consulte **Tarefas agendadas**.

## Terminal da máquina anfitriã (PowerShell / bash / cmd)

Sim — na máquina anfitriã execute o **OrganizeFiles.Cli** pelo PowerShell, bash ou cmd. Esse é o caminho de terminal com suporte. A janela de área de trabalho do Avalonia é uma interface gráfica à parte. Publique ou instale o kit da CLI ao lado do aplicativo (ou no PATH) e então passe **--source** (repetível), **--output** e **--mode**. É melhor começar por um ensaio. Acrescente **--execute** apenas quando estiver pronto.

## Interface de área de trabalho e contêineres

Contêineres e automação: a GUI do desktop Avalonia não foi projetada para ser executada dentro de um contêiner Linux headless típico. Para um ou mais trabalhos isolados, incluindo vários trabalhadores paralelos, use o complemento OrganizeFiles.Cli: em cada contêiner, monte as pastas de origem somente leitura para trabalhos de visualização de simulação. Movimentos reais com **--execute** requerem uma montagem de origem gravável porque o mecanismo realoca os arquivos para fora da árvore de origem. Use um volume de saída de leitura/gravação dedicado, garanta direitos válidos de armazenamento ou editor para todas as execuções de organização/reparo (ensaio e execução), aprovação **--source** (repetível), **--output** e **--mode**. Cada trabalhador simultâneo precisa de sua própria raiz de saída. A pasta **Output** já deve existir no host antes da execução dos trabalhos do Docker ou Kubernetes (o preflight recusa um destino ausente e não o cria). Caminhos de exemplo: containers/README.md e containers/docker-compose.sample.yml. Jobs/JobAgent gerado `docker run` monta fontes em `/in1`, `/in2`,… e saída em `/out`. Exemplos manuais de fonte única podem usar `/in` (consulte containers/README.md).
