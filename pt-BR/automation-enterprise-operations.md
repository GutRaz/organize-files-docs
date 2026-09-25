# Monitoramento com Prometheus e Grafana

## O que os contadores abrangem

Os trabalhos agendados mantêm um pequeno conjunto de contadores e medidores do Prometheus. Cada nome começa com `organize_files_automation_`, e o conjunto inteiro é publicado como texto do Prometheus. Os três hospedeiros que executam trabalhos publicam o mesmo conjunto: o aplicativo de área de trabalho, o serviço `OrganizeFiles.JobAgent` e o hospedeiro de linha de comando usado dentro de contêineres.

Os contadores descrevem o agendador, não os arquivos. São contadas as passagens, os desfechos dos trabalhos, as aprovações, a entrega de webhooks e a limpeza do histórico. Nada é contado sobre os arquivos que um trabalho move.

## Exportação para arquivo, sem abrir porta

`automation-metrics.prom` é gravado na pasta de dados da automação, ao lado de `automation-jobs.json`, e atualizado após cada passagem vencida e a cada leitura. O formato é o que o coletor textfile do `node_exporter` lê, portanto uma máquina que já executa o `node_exporter` fica coberta sem porta em escuta, sem token e sem regra de firewall. O arquivo é trocado de forma atômica, e um vínculo simbólico deixado no lugar dele interrompe a gravação em vez de ser seguido.

## Ponto de leitura

O ponto de leitura existe apenas quando `ORGANIZE_FILES_METRICS_HTTP_PORT` contém uma porta entre 1 e 65535. Sem essa variável nada fica em escuta.

| Variável | Efeito |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | Porta de escuta. Se faltar ou ficar fora da faixa, não existe ponto de leitura algum. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Endereço de escuta. O padrão é `127.0.0.1`. Os valores `0.0.0.0`, `+` e `*` indicam todos os endereços, e qualquer outro volta para `127.0.0.1`. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | Token bearer exigido em `/metrics` e em `/ready`. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` deixa `/ready` responder sem esse token, para sondas de cluster. Os caminhos do hospedeiro ficam então fora da resposta. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | Códigos de saída separados por vírgula que fazem `/ready` informar que não está pronto. Substitui a lista interna. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` desconsidera o código de saída da última passagem, e também o estado anterior ao término da primeira. |
| `ORGANIZE_FILES_READY_JSON` | `1` impõe a resposta JSON em `/ready`, mesmo para quem pediu texto simples. |

Um endereço fora do laço local é recusado antes de o ouvinte abrir, caso nenhum token bearer esteja definido. A recusa é escrita na saída de erro e emitida como evento de webhook, porque essa combinação entregaria os contadores à rede inteira.

## Caminhos atendidos

- `/metrics` — os contadores como texto do Prometheus. Um pedido a `/` devolve o mesmo conteúdo.
- `/ready` — prontidão para um orquestrador. Responde `200` assim que a pasta de automação aceita uma gravação de teste, o arquivo de trabalhos abre, a pasta de histórico se resolve dentro da raiz de dados e a última passagem vencida terminou com um código de saída que não bloqueia. Caso contrário responde `503` com um motivo curto como `due_pass_not_completed` ou `last_due_pass_license_failed`.
- `/health` — apenas sinal de vida. Esse caminho continua anônimo mesmo com um token definido, porque responde `ok` e nada mais.

Os códigos de saída `3` por falha de licença, `8` por árvore de saída travada, `10` por uma exclusão nunca confirmada e `11` por conflito de reivindicação bloqueiam a prontidão por padrão. O corpo de `/ready` é JSON a menos que quem chama envie `Accept: text/plain` ou acrescente `?format=text`.

## Os contadores

| Nome | Conteúdo |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Passagens vencidas iniciadas pelo agendador. |
| `organize_files_automation_jobs_started_total` | Execuções de trabalho que chegaram ao estado em andamento. |
| `organize_files_automation_jobs_skipped_total` | Trabalhos pulados: ambiente do Docker ou do Kubernetes que não está pronto, trabalho voltado ao aplicativo em um hospedeiro sem tela, raiz de saída ocupada, ou trabalho recusado pelo orquestrador. |
| `organize_files_automation_jobs_failed_total` | Execuções de trabalho terminadas em falha. |
| `organize_files_automation_jobs_awaiting_approval_total` | Execuções reais paradas à espera de aprovação. |
| `organize_files_automation_execute_approvals_total` | Aprovações concedidas a uma execução real. |
| `organize_files_automation_execute_approvals_expired_total` | Aprovações cujo prazo venceu antes do uso. |
| `organize_files_automation_claim_conflicts_total` | Vezes em que outro hospedeiro já detinha a reivindicação sobre a raiz de saída. |
| `organize_files_automation_runs_orphaned_total` | Execuções recuperadas como órfãs, deixadas por um hospedeiro que parou. |
| `organize_files_automation_job_events_total` | Um contador por evento, com os rótulos `event`, `job_id`, `target` e `jobs_file`. |
| `organize_files_automation_webhook_posts_succeeded_total` | Entregas de webhook aceitas. |
| `organize_files_automation_webhook_posts_failed_total` | Entregas de webhook recusadas ou inalcançáveis. |
| `organize_files_automation_webhook_dead_letter_depth` | Linhas que aguardam neste momento no arquivo de webhooks não entregues. |
| `organize_files_automation_log_retention_pruned_total` | Registros de execução removidos pela retenção. |
| `organize_files_automation_runs_index_compacted_total` | Linhas retiradas do índice de execuções durante a compactação. |
| `organize_files_automation_last_due_pass_exit_code` | Código de saída da última passagem concluída. `0` é uma passagem limpa. |
| `organize_files_automation_last_due_pass_completed_utc` | Hora Unix em segundos da última passagem concluída, e `0` antes da primeira. |

## Painel e regras de alerta

Um painel do Grafana pronto é publicado com os arquivos de implantação como `grafana-organize-files-automation.json`, sob o título **OrganizeFiles Automation**. Seus dez quadros mostram as passagens vencidas, os trabalhos iniciados e falhos, os conflitos de reivindicação, a vazão de trabalhos em uma hora, o último código de saída, a profundidade das mensagens não entregues, as falhas de webhook em um dia, os trabalhos à espera de aprovação e os eventos de trabalho por estado. Cada quadro nomeia sua fonte de dados pelo marcador `${DS_PROMETHEUS}`.

As regras de alerta correspondentes são `alerts-organize-files-automation.yaml`, com `prometheus-rule-automation.yaml` como invólucro do Kubernetes para `kube-prometheus-stack`. Um último código de saída diferente de zero avisa depois de cinco minutos, uma falha de licença é crítica depois de um, e as demais regras cobrem trabalhos falhos, conflitos de reivindicação, falhas de webhook, um acúmulo de mensagens não entregues e aprovações deixadas em espera por um dia. Os dois arquivos são conferidos a cada compilação, de modo que os nomes acima acompanham os contadores.

# Saída da execução e métricas

## Linha de status

A área **Saída da execução** mostra:

- Estado atual do aplicativo e progresso do mecanismo.
- **CPU** e dois valores de **memória** apenas para este processo.
- Linhas de **GPU**, no Windows: a parcela de cada placa gráfica usada por este processo, não a placa inteira.

A mesma barra compacta de recursos é reutilizada em janelas de ferramentas secundárias, como exploração de arquivos, trabalhos agendados e reparo de arquivos.

## Etiquetas de memória

- **Bytes privados/commit** — memória virtual privada reservada pelo processo.
- **Conjunto de trabalho/memória** — RAM residente atualmente mantida por este processo. Ele pode ser diferente de outro monitor de sistema operacional porque cada rótulo de sistema operacional e ambiente de área de trabalho processa a memória de maneira diferente.

## Execute o JSON de pulsação (opcional)

Habilite **Escrever run heartbeat JSON** em **Avançado/Diagnóstico**. O mecanismo grava `Organize.Files.run.json` em `Output\_OrganizeMediaLogs` (mesma pasta do arquivo de retomada organizado padrão).

- **Caminho** — atualizado atomicamente durante execuções de organização e reparo.
- **Cadência** — enquanto as fontes são percorridas, o arquivo é reescrito a cada 10.000 arquivos vistos, a cada 5.000 correspondências e a cada 15 segundos aproximadamente enquanto a varredura continua, de modo que uma árvore de rede grande que demora a ser listada ainda mostra que a execução está viva. Durante a validação, o hashing e as movimentações, é reescrito após cada 1.000 arquivos, no máximo a cada cinco segundos. As escritas de início e de fim continuam acontecendo quando uma execução começa e termina.
- **Progresso** — enquanto a contagem de arquivos ainda cresce, a barra principal mostra os arquivos vistos até agora em vez de 100%, até que uma fase tenha um total conhecido.
- **Campos** — `schema`, `mode`, `phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`), `runState` (`active` / `completed` / `failed` / `cancelled`), `utc` (ISO-8601), `dryRun`, `outputRoot`, `validateMedia`, `deepVideoValidate`, `gpuDeviceCount`, `hwaccel`, opcional `correlationId`, contadores `progress` aninhados.
- **Log** — o painel de saída da execução imprime o caminho completo no início e quando o arquivo é salvo no final. Use **Abrir pasta de log de pulsação** / **Mostrar arquivo JSON de pulsação** em Avançado/Diagnóstico.
- **CLI** — `--heartbeat-json` em OrganizeFiles.Cli. Erros de shell fatais e de cancelamento gravam `cancelled` / `failed` `runState` quando ativado.
