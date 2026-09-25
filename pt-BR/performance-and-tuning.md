# Avançado/Diagnóstico

## Organize o ajuste

Avançado/Diagnóstico expõe as opções do **OrganizeFilesEngine** sem sobrecarregar o painel principal.

Os modos de organização podem ajustar desduplicação, índice de destino, regras de data exclusivas, encadeamento de movimentação e enumeração, suplemento BFS, arquivo de retomada e raízes exclusivas extras.

O reparo mantém apenas o tempo de repetição de rede e disco cheio, pistas de hardware gráfico detectadas para verificação de vídeo completa opcional, buffer de leitura de hash e pulsação JSON. Outros campos ficam visíveis para contexto, mas desabilitados.

Quando as fontes ou a saída residem nos caminhos NAS ou UNC, diminua o paralelismo, mantenha a nova tentativa de rede ativada, deixe o suplemento BFS ativado para árvores SMB ímpares e tente o buffer de hash de 8 MiB se o hash for lento.

# Avançado/Diagnóstico — cada opção

## Sobre este capítulo

Esses controles são opções do mecanismo. O desktop (Windows, macOS, Linux), Android, iOS e a ferramenta de linha de comando leem os mesmos valores.

Os modos **Organizar** usam todos os controles abaixo, a menos que a interface os esmaeça. **Reparo** usa apenas as novas tentativas de rede, as novas tentativas por disco cheio, as pistas de hardware gráfico detectadas (com verificação completa de vídeo), o buffer de leitura de hash, o JSON de pulsação, **Arquivo de retomada de estado** e **Comece do zero (truncar o arquivo de retomada)**. Os demais campos permanecem visíveis, mas são ignorados durante o reparo.

## Fontes de rede (NAS / UNC)

Quando as origens ou saídas estão em compartilhamentos SMB/CIFS, volumes NAS ou unidades mapeadas, revise esta seção cuidadosamente.

- **Por que ajustar** — Contagens de threads que funcionam em um SSD local podem paralisar ou sobrecarregar um arquivador.
- **O que tentar** — Mantenha a nova tentativa de rede ativada. Reduza os threads de movimentação e enum paralelo máximo nos tempos limite. Deixe o suplemento BFS ativado, a menos que uma contagem completa tenha sido verificada sem ele. Experimente o buffer de hash de 8 MiB quando o hash estiver lento na rede.
- **Desativar espera de rede** — Falha rapidamente em erros de rede transitórios. Arriscado em Wi-Fi ou compartilhamentos ocupados.

## Modo de desduplicação

Como o mecanismo decide que dois arquivos são duplicados.

| Modo | O que faz | Quando usar | Troca |
| ---- | ------------ | ----------- | --------- |
| **Hash (SHA-256)** | Lê e faz hash do conteúdo completo de cada arquivo de origem incluído e agrupa bytes idênticos. | Modo prático mais forte. Hash (SHA-256) é obrigatório para exclusão no local (duplicatas e arquivos problemáticos). | Mais lento em árvores grandes ou NAS. Nenhum algoritmo deve ser apresentado como garantia absoluta. |
| **Tamanho + hora + nome** | Chave = tamanho, ticks da última gravação UTC, nome em letras minúsculas e verificação SHA-256 completa. | Modo de compatibilidade conservador para layouts de pastas de mídia mais antigos. | Pode perder duplicatas renomeadas. Nunca use com a exclusão de duplicatas ou de arquivos problemáticos. |
| **Nenhum** | Sem desduplicação entre arquivos. | Apenas classificação, não limpeza duplicada. | As duplicatas permanecem nas fontes. |

## Ignorar índice de destino

- **Desligado (padrão)** — Verifica a saída **Única** existente e a indexa antes do hash. Mais seguro ao reutilizar a mesma pasta de saída.
- **Ativado** — Ignora essa verificação.
- **Benefício** — Mais rápido em grandes árvores de produção.
- **Risco** — Mais conteúdo duplicado pode chegar ao Unique.

## Ano mínimo de Unicos

Ano civil mínimo para pastas de data em **Exclusivo** em layouts de mídia. **Por que** — Evita espalhar arquivos muito antigos em pastas de anos ímpares quando os metadados estão errados.

## Mover threads

O arquivo paralelo é movido após os destinos serem reservados.

- **Maior** — Mais rápido em SSD local.
- **Inferior** — Mais seguro em unidades mapeadas NAS, USB ou Wi-Fi.

## Tópicos de classificação e hash

Trabalhadores paralelos durante a varredura de origem e a deduplicação SHA-256.

- **Threads de classificação** — Descoberta e classificação de arquivos. CLI: `--classify-threads <n>`.
- **Threads de hash** — Trabalhadores de hash de conteúdo. CLI: `--hash-threads <n>`.
- **Substituições** — Valores manuais substituem os padrões do perfil de organização (`--profile`).

## Enum paralelo máximo

Limite para listagem de diretórios paralelos durante a varredura.

- **0** = motor automático.
- **Menor** — Menos pressão sobre as pequenas e médias empresas quando muitas pastas são listadas ao mesmo tempo.

## Suplemento

- **Ligado (padrão)** — Um percurso adicional em largura, pouco profundo.
- **Por quê** — Alguns caminhos NAS ou árvores profundas parecem incompletos após o primeiro percurso.
- **Desligado** — Somente depois de comprovar uma contagem completa de arquivos sem ele.
- **CLI** — `--no-bfs` desliga este percurso.

## Arquivo de retomada de estado

Caminho UTF-8 opcional. Movimentos bem-sucedidos acrescentam linhas `B64|` para que a próxima execução de organização possa pular as fontes concluídas.

- **Por que** — Continue trabalhos longos após parar ou travar.
- **Caminho padrão** — Quando o campo está vazio em tempo de execução, o mecanismo usa `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt`. Sem saída, ele usa `sessions\<id>\resume\OrganizeFiles.resume.txt` no perfil do aplicativo.
- **IU da área de trabalho** — Lista de caminhos somente leitura para seleção e cópia do mouse. Quando já existe um arquivo de retomada no local padrão, o caminho aparece automaticamente. **Navegar** escolhe uma pasta de log e anexa `OrganizeFiles.resume.txt`. **Remover** limpa o caminho. Quando vazia, a dica mostra o caminho utilizado em tempo de execução.

## Iniciar do zero

Trunca o arquivo de retomada quando uma execução organizada **real** é iniciada (a simulação não trunca). Com **Salvar progresso e espaço de trabalho**, também limpa o instantâneo da IU salvo no início da execução. **Por que** — Força uma recontagem completa em vez de continuar um registro de arquivo de retomada antigo.

## Raízes de varredura extras

Uma pasta por linha: árvores **Unique** adicionais para indexar (layout antigo, outro volume).

- **Por quê** — A remoção de duplicatas enxerga arquivos já organizados em outro lugar sem movê-los de novo.
- **Interface de área de trabalho** — Lista somente leitura, para copiar linha a linha. **Adicionar** anexa uma pasta escolhida. **Remover** apaga a linha selecionada (por exemplo uma árvore `Uniques` antiga no NAS).

## Nova tentativa de rede

Segundos para tentar de novo a entrada e saída de rede passageira.

- **Por quê** — Servidores SMB derrubam sessões ociosas. Usado pela organização e pelo reparo.
- **Desligar a espera de rede** — Para de esperar e falha em vez disso.

## Nova tentativa de disco cheio

(segundos) / Desativar espera de disco cheio

Mesmo padrão quando o volume de saída fica sem espaço. **Por que** — Tempo para liberar disco durante execuções longas.

## Faixas da placa gráfica

Somente quando a **verificação completa de vídeo** integrada está ligada e **Usar a placa gráfica detectada** também. Um valor acima de **0** fixa um número explícito de faixas para a verificação em paralelo entre os fabricantes detectados (NVIDIA, AMD, Intel, Apple, móvel). **0** significa que o número de faixas é descoberto sozinho. Não significa apenas processador. Para amostrar apenas no processador, escolha **Somente CPU** na lista de placas gráficas. As marcas de faixa planejam a verificação do fluxo de bits no processador. Elas não acionam a decodificação de vídeo por hardware do sistema.

- **Predefinição da linha de comando** — `--hwaccel <value>` escolhe uma predefinição de faixas de verificação (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`) quando a verificação completa de vídeo é executada.

## Buffer de leitura de hash

Buffer de leitura por trabalhador durante o hash (512 KiB, 1 MiB, 8 MiB). **Por que** — Buffers maiores ajudam a desacelerar NAS e compartilhamentos de alta latência.

## Registrar diário de desfazer

Diário JSONL opcional dos movimentos sob a raiz de saída da execução.

- **Para quê** — Permite desfazer pela CLI após uma execução real.
- **Arquivo** — O arquivamento pós-organização fica desativado enquanto o diário está ativo.
- **CLI** — `--record-undo-journal` (igual à caixa de seleção da janela principal).

## Gravar JSON de andamento da execução

Escreve o arquivo opcional `Organize.Files.run.json` em `Output\_OrganizeMediaLogs`.

- **Por quê** — Ferramentas externas podem ler contadores ao vivo (percorridos, planejados, concluídos) durante a organização ou o reparo.
- **Cadência** — A cada 10.000 arquivos vistos, a cada 5.000 correspondências e a cada 15 segundos aproximadamente durante os percursos das fontes, após cada 1.000 arquivos e no máximo a cada cinco segundos durante a validação, o hashing e as movimentações e em cada fase importante.
