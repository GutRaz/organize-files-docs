# Gevorderd / Diagnostiek

## Organiseer stemming

Gevorderde / Diagnostiek stel **OrganizeFilesEngine**-opsies bloot sonder om die hoofpaneel deurmekaar te maak.

Organiseermodusse kan dedupe, bestemmingsindeks, unieke datumreëls, skuif- en opsommingsdraad, BFS-aanvulling, hervatlêer en ekstra unieke wortels instel.

Herstel hou slegs netwerk- en skyf-vol herprobeertydsberekening, bespeurde grafiese hardeware-bane vir opsionele volledige videokontrole, hash-leesbuffer en JSON-hartklop. Ander velde is sigbaar vir konteks, maar gedeaktiveer.

Wanneer bronne of uitset op NAS- of UNC-paaie leef, verlaag parallelisme, hou netwerkherprobeer geaktiveer, laat aanvulling BFS aan vir vreemde SMB-bome, en probeer die 8 MiB hash-buffer as hash stadig is.

# Gevorderd / Diagnostiek - elke opsie

## Oor hierdie hoofstuk

Hierdie kontroles is enjinopsies. Die rekenaarprogram (Windows, macOS, Linux), Android, iOS en die opdragreëlhulpmiddel lees dieselfde waardes.

**Organiseer**-modusse gebruik elke kontrole hieronder, tensy die UI dit grys maak. **Herstel** gebruik slegs netwerkherprobering, skyfvol-herprobering, bespeurde grafiese hardeware-bane (met volledige videokontrole), hash-leesbuffer, hartklop-JSON, **Hervattingslêer** en **Begin nuut (kap hervatlêer af)**. Ander velde bly sigbaar, maar word tydens herstel geïgnoreer.

## Netwerkbronne (NAS / UNC) Wanneer

Bronne of Afvoer op SMB/CIFS-aandele, NAS-volumes of gekarteerde aandrywers is, hersien hierdie afdeling noukeurig.

- **Hoekom stem** — Draadtellings wat op 'n plaaslike SSD werk, kan 'n lêer oorlaai of oorlaai.
- **Wat om te probeer** — Hou netwerk herprobeer aan. Verlaag skuifdrade en noem parallelle maksimum op time-outs. Laat aanvulling BFS aan tensy 'n volle telling daarsonder geverifieer is. Probeer die 8 MiB hash buffer wanneer hash stadig oor die netwerk is.
- **Deaktiveer netwerkwag** — Misluk vinnig op kortstondige netwerkfoute. Risikovol op Wi-Fi of besige aandele.

## Dedupe-modus

Hoe die enjin besluit twee lêers is duplikate.

| Modus | Wat dit doen | Wanneer om te gebruik | Afruiling |
| ---- | ------------ | ---------- | ---------- |
| **Hash (SHA-256)** | Lees en hashes die volle inhoud van elke ingeslote bronlêer, groepeer dan identiese grepe. | Sterkste praktiese modus. Hash (SHA-256) is vereis vir skrapping by die bron (duplikate en problematiese lêers). | Stadigste op groot bome of NAS. Geen algoritme moet as 'n absolute waarborg aangebied word nie. |
| **Grootte + tyd + naam** | Sleutel = grootte, UTC laaste-skryf regmerkies, kleinletters naam, dan volledige SHA-256 verifikasie. | Konserwatiewe versoenbaarheidsmodus vir ouer mediavoueruitlegte. | Kan hernoemde duplikate mis. Moet nooit met die skrapping van duplikate of problematiese lêers gebruik word nie. |
| **Geen** | Geen kruislêer dedupe nie. | Sorteer slegs, nie duplikaatopruiming nie. | Duplikate bly in bronne. |

## Slaan bestemmingsindeks oor

- **Af (verstek)** — Skandeer bestaande **Unieke** afvoer en indekseer dit voor hash. Veiliger wanneer dieselfde uitvoergids hergebruik word.
- **Aan** — Slaan daardie skandering oor.
- **Voordeel** — Vinniger op groot uitsetbome.
- **Risiko** - Meer duplikaatinhoud kan in Uniek beland.

## Uniek min. jaar

Minimum kalenderjaar vir datumvouers onder **Uniek** in media-uitlegte. **Hoekom** — Vermy die verstrooiing van baie ou lêers in vreemde jaarvouers wanneer metadata verkeerd is.

## Skuif drade

Parallelle lêerbewegings nadat bestemmings gereserveer is.

- **Hoër** — Vinniger op plaaslike SSD.
- **Laer** — Veiliger op NAS, USB of Wi-Fi gekarteer dryf.

## Klassifiseer- en hash-drade

Parallelle werkers tydens die bronskandering en SHA-256-ontdubbeling.

- **Klassifikasiedrade** — Lêerontdekking en klassifikasie. CLI: `--classify-threads <n>`.
- **Hash drade** — Werkers vir inhoud-hashing. CLI: `--hash-threads <n>`.
- **Oorskryf** — Handmatige waardes oorskryf die profiel se verstekwaardes (`--profile`).

## Enum parallel maks

Limiet vir parallelle gidslys tydens skandering.

- **0** = motor outomaties.
- **Laer** — Minder druk op SMB wanneer baie vouers gelyktydig lys.

## Byvoegsel BFS gidspas

- **Aan (verstek)** — 'n Ekstra vlak breedte-eerste noteringspas.
- **Hoekom** — Sommige NAS-paaie of diep bome lyk onvolledig ná die eerste pas.
- **Af** — Slegs nadat 'n volledige lêertelling daarsonder bevestig is.
- **CLI** — `--no-bfs` skakel hierdie pas af.

## Hervat staat lêer

Opsionele UTF-8 pad. Suksesvolle skuiwe voeg `B64|`-reëls by sodat die volgende organiseerlopie voltooide bronne kan oorslaan.

- **Hoekom** — Gaan voort met lang take na stop of ineenstorting.
- **Verstekpad** — Wanneer die veld leeg is tydens looptyd, gebruik die enjin `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt`. Sonder afvoer gebruik dit `sessions\<id>\resume\OrganizeFiles.resume.txt` onder die toepassingprofiel.
- **Desktop UI** — Leesalleen-padlys vir muiskeuse en -kopie. Wanneer 'n hervatlêer reeds op die verstekplek bestaan, verskyn die pad outomaties. **Blaai** kies 'n loglêergids en voeg `OrganizeFiles.resume.txt` by. **Verwyder** maak die pad skoon. Wanneer dit leeg is, wys die wenk die pad wat tydens lopietyd gebruik is.

## Begin vars

Knip die hervatlêer af wanneer 'n **regte** organiseerlopie begin (toetslopie word nie afgekap nie). Met **Stoor vordering en werkspasie**, vee ook die gestoorde UI-snapshot uit wanneer die lopie begin. **Hoekom** — Dwing 'n volledige hertelling af in plaas van om voort te gaan met 'n ou hervatlogboek.

## Ekstra

Een vouer per reël: ekstra **Unique**-bome om te indekseer (ou uitleg, ander volume).

- **Hoekom** — Dedupe kan lêers sien wat reeds elders georden is, sonder om hulle weer te skuif.
- **Lessenaarkoppelvlak** — Leesalleen-lys vir kopiëring per reël. **Voeg by** voeg 'n gekose vouer aan. **Verwyder** skrap die gekose reël (byvoorbeeld 'n ou `Uniques`-boom op NAS).

## Netwerk herprobeer (sekondes) /

Sekondes om vlietende netwerk-I/O weer te probeer.

- **Hoekom** — SMB-lêerbedieners laat ledige sessies val. Gebruik deur organiseer en herstel.
- **Netwerkwag afskakel** — Hou op wag en misluk eerder.

## Skyf vol herprobeer

(sekondes) / Deaktiveer skyf vol wag

Dieselfde patroon wanneer die uitsetvolume nie meer spasie het nie. **Hoekom** — Tyd om skyf vry te maak tydens lang lopies.

## Bane vir grafiese hardeware

Slegs wanneer die geïntegreerde **volledige videokontrole** aan is en **Gebruik bespeurde grafiese hardeware** aan is. 'n Waarde bo **0** stel 'n vaste aantal bane vir gelyktydige validering oor die bespeurde makers (NVIDIA, AMD, Intel, Apple, mobiel). **0** beteken die aantal bane word self bepaal. Dit beteken nie slegs-SVE nie. Kies **Slegs SVE** in die lys van grafiese kaarte vir monsterneming op die SVE alleen. Baanmerkers beplan bisstroomvalidering op die SVE. Hulle roep nie die bedryfstelsel se hardewarevideodekodering op nie.

- **CLI-voorinstelling** — `--hwaccel <value>` kies 'n voorinstelling vir valideringsbane (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`) wanneer die volledige videokontrole loop.

## Hash-leesbuffer

Per-werker leesbuffer tydens hashing (512 KiB, 1 MiB, 8 MiB). **Hoekom** — Groter buffers help wanneer 'n NAS of 'n hoë-latency-netwerkdeel stadig reageer.

## Teken ontdoen-joernaal aan

Opsionele JSONL-joernaal van skuiwe onder die uitsetwortel vir die lopie.

- **Waarvoor** — Maak ontdoen vanaf die CLI moontlik ná n werklike lopie.
- **Argief** — Argivering ná organisering bly af terwyl die joernaal aktief is.
- **CLI** — `--record-undo-journal` (dieselfde as die merkblokkie in die hoofvenster).

## Skryf lopie-hartklop JSON

Skryf die opsionele `Organize.Files.run.json` onder `Output\_OrganizeMediaLogs`.

- **Hoekom** — Buite-gereedskap kan lewende tellers (geskandeer, beplan, voltooi) lees terwyl georganiseer of herstel word.
- **Tydsberekening** — Elke 10 000 lêers gesien, elke 5 000 passings en ongeveer elke 15 sekondes gedurende bronskanderings, ná elke 1 000 lêers en hoogstens elke 5 sekondes tydens validering, hashing en skuiwe, en by elke groot fase.
