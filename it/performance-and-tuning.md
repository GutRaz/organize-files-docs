# Avanzato/Diagnostica

## Organizza l'accordatura

Avanzate/Diagnostica espone le opzioni **OrganizeFilesEngine** senza ingombrare il pannello principale.

Le modalità di organizzazione possono ottimizzare la deduplica, l'indice di destinazione, le regole della data univoca, il threading di spostamento ed enumerazione, il supplemento BFS, il file di ripristino e le radici univoche aggiuntive.

La riparazione mantiene solo i tempi di ripetizione dei tentativi di rete e disco pieno, le corsie hardware grafiche rilevate per il controllo video completo opzionale, il buffer di lettura dell'hash e il battito cardiaco JSON. Altri campi sono visibili per contesto ma disabilitati.

Quando le origini o l'output sono attivi sui percorsi NAS o UNC, abbassare il parallelismo, mantenere abilitati i tentativi di rete, lasciare attivo il supplemento BFS per alberi SMB dispari e provare il buffer hash da 8 MiB se l'hashing è lento.

# Avanzate/Diagnostica: ciascuna opzione

## Informazioni su questo capitolo

Questi controlli sono opzioni del motore. Il desktop (Windows, macOS, Linux), Android, iOS e lo strumento da riga di comando leggono gli stessi valori.

Le modalità **Organizza** utilizzano tutti i controlli riportati di seguito, a meno che l'interfaccia non li disattivi. **Riparazione** utilizza solo i nuovi tentativi di rete, i nuovi tentativi con disco pieno, le corsie hardware grafiche rilevate (con controllo video completo), il buffer di lettura hash, il JSON heartbeat, **File di stato per la ripresa** e **Ricomincia da capo (tronca il file di stato per la ripresa)**. Gli altri campi restano visibili ma vengono ignorati durante la riparazione.

## Origini di rete (NAS / UNC)

Quando le origini o l'output si trovano su condivisioni SMB/CIFS, volumi NAS o unità mappate, rivedere attentamente questa sezione.

- **Perché ottimizzare**: i conteggi dei thread che funzionano su un SSD locale possono bloccare o sovraccaricare un filer.
- **Cosa provare**: mantieni attivo il tentativo di rete. Abbassa i thread di spostamento ed enumera il massimo parallelo sui timeout. Lasciare attivo il supplemento BFS a meno che non sia stato verificato un conteggio completo senza di esso. Prova il buffer hash da 8 MiB quando l'hashing è lento sulla rete.
- **Disabilita attesa rete**: fallisce rapidamente in caso di errori di rete temporanei. Rischioso su Wi-Fi o condivisioni occupate.

## Modalità deduplica

Modalità in cui il motore decide che due file sono duplicati.

| Modalità | Cosa fa | Quando utilizzare | Scambio |
| ---- | ------------ | ----------- | --------- |
| **Hash (SHA-256)** | Legge ed esegue l'hashing dell'intero contenuto di ogni file sorgente incluso, quindi raggruppa byte identici. | Modalità pratica più potente. Hash (SHA-256) è obbligatorio per l'eliminazione in loco (duplicati e file problematici). | Più lento su alberi di grandi dimensioni o NAS. Nessun algoritmo dovrebbe essere presentato come una garanzia assoluta. |
| **Taglia + ora + nome** | Chiave = dimensione, segni di spunta dell'ultima scrittura UTC, nome in minuscolo, quindi verifica SHA-256 completa. | Modalità di compatibilità conservativa per i layout delle cartelle multimediali meno recenti. | Possono mancare i duplicati rinominati. Non utilizzare mai con l'eliminazione di duplicati o di file problematici. |
| **Nessuno** | Nessuna deduplica tra file. | Solo ordinamento, non pulizia duplicata. | I duplicati rimangono nelle fonti. |

## Salta indice di destinazione

- **Off (impostazione predefinita)**: analizza l'output **Unique** esistente e lo indicizza prima dell'hashing. Più sicuro quando si riutilizza la stessa cartella di output.
- **On**: salta la scansione.
- **Vantaggio** — Più veloce su alberi di output enormi.
- **Rischio**: più contenuti duplicati possono finire all'interno di Unique.

## Anno minimo per Unici

Anno solare minimo per le cartelle di date in **Unico** nei layout multimediali. **Perché**: evita di disperdere file molto vecchi in cartelle di anni dispari quando i metadati sono errati.

## Sposta thread

I file paralleli si spostano dopo che le destinazioni sono state riservate.

- **Più alto**: più veloce sull'SSD locale.
- **Inferiore**: più sicuro su unità mappate NAS, USB o Wi-Fi.

## Thread di classificazione e hash

Worker paralleli durante la scansione delle origini e la deduplicazione SHA-256.

- **Thread di classificazione** — Rilevamento e classificazione dei file. CLI: `--classify-threads <n>`.
- **Thread di hash** — Worker per l hashing dei contenuti. CLI: `--hash-threads <n>`.
- **Override** — I valori manuali sovrascrivono i predefiniti del profilo di organizzazione (`--profile`).

## Enumerazione parallela max

Limite per l'elenco delle directory parallele durante la scansione.

- **0** = motore automatico.
- **Inferiore**: meno pressione su SMB quando vengono elencate più cartelle contemporaneamente.

## Supplemento

- **Attivo (predefinito)** — Un passaggio aggiuntivo in ampiezza, poco profondo.
- **Perché** — Certi percorsi NAS o alberi profondi sembrano incompleti dopo il primo passaggio.
- **Disattivo** — Solo dopo aver verificato un conteggio completo dei file senza di esso.
- **CLI** — `--no-bfs` disattiva questo passaggio.

## Riprendi file di stato

Percorso UTF-8 facoltativo. Le mosse riuscite aggiungono le righe `B64|` in modo che la successiva esecuzione di organizzazione possa saltare le fonti completate.

- **Perché** — Continua i lavori lunghi dopo un'interruzione o un arresto anomalo.
- **Percorso predefinito**: quando il campo è vuoto in fase di esecuzione, il motore utilizza `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt`. Senza output, utilizza `sessions\<id>\resume\OrganizeFiles.resume.txt` nel profilo dell'app.
- **Interfaccia utente desktop**: elenco di percorsi di sola lettura per la selezione e la copia con il mouse. Quando un file di ripristino esiste già nella posizione predefinita, il percorso viene visualizzato automaticamente. **Sfoglia** seleziona una cartella di registro e aggiunge `OrganizeFiles.resume.txt`. **Rimuovi** cancella il percorso. Quando è vuoto, il suggerimento mostra il percorso utilizzato in fase di esecuzione.

## Inizia da zero

Tronca il file di ripristino quando viene avviata un'esecuzione di organizzazione **reale** (l'esecuzione di prova non viene troncata). Con **Salva avanzamento e area di lavoro**, cancella anche lo snapshot dell'interfaccia utente salvato all'avvio dell'esecuzione. **Perché**: forza un riconteggio completo invece di continuare un vecchio registro di ripristino.

## Root di scansione extra

Una cartella per riga: alberi **Unique** aggiuntivi da indicizzare (disposizione vecchia, altro volume).

- **Perché** — La deduplica vede i file già ordinati altrove senza spostarli di nuovo.
- **Interfaccia desktop** — Elenco di sola lettura, per copiare riga per riga. **Aggiungi** accoda una cartella scelta. **Rimuovi** cancella la riga selezionata (per esempio un vecchio albero `Uniques` su NAS).

## Nuovo tentativo di rete

Secondi per riprovare gli scambi di rete passeggeri.

- **Perché** — I server SMB lasciano cadere le sessioni inattive. Usato dall'organizzazione e dalla riparazione.
- **Disattiva l'attesa di rete** — Smette di attendere e fallisce invece.

## Nuovo tentativo di disco pieno

(secondi) / Disabilita attesa disco pieno

Stesso schema quando il volume di output esaurisce lo spazio. **Perché**: tempo necessario per liberare il disco durante le esecuzioni prolungate.

## Corsie della scheda grafica

Solo quando la **verifica video completa** integrata è attiva e lo è anche **Usa la scheda grafica rilevata**. Un valore superiore a **0** fissa un numero esplicito di corsie per la verifica in parallelo fra i produttori rilevati (NVIDIA, AMD, Intel, Apple, mobile). **0** significa che il numero di corsie si ricava da sé. Non significa solo processore. Per campionare sul solo processore scegliere **Solo CPU** nell'elenco delle schede grafiche. Le etichette di corsia pianificano la verifica del flusso di bit sul processore. Non richiamano la decodifica video hardware del sistema.

- **Preimpostazione da riga di comando** — `--hwaccel <value>` sceglie una preimpostazione di corsie di verifica (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`) quando la verifica video completa è in corso.

## Buffer di lettura hash

Buffer di lettura per lavoratore durante l'hashing (512 KiB, 1 MiB, 8 MiB). **Perché** — Buffer più grandi aiutano con NAS lenti e condivisioni ad alta latenza.

## Registra il diario degli annullamenti

Diario JSONL facoltativo degli spostamenti sotto la radice di output dell esecuzione.

- **Perché** — Consente l annullamento da CLI dopo un esecuzione reale.
- **Archivio** — L archiviazione post-organizzazione resta disattivata mentre il diario è attivo.
- **CLI** — `--record-undo-journal` (come la casella nella finestra principale).

## Scrive run heartbeat JSON

Scrive il file facoltativo `Organize.Files.run.json` sotto `Output\_OrganizeMediaLogs`.

- **Perché** — Strumenti esterni possono leggere i contatori in tempo reale (percorsi, pianificati, completati) durante l'organizzazione o la riparazione.
- **Cadenza** — Ogni 10.000 file visti, ogni 5.000 corrispondenze e all'incirca ogni 15 secondi durante le scansioni delle fonti, dopo ogni 1.000 file e al massimo ogni 5 secondi durante la convalida, l'hashing e gli spostamenti e a ogni fase importante.
