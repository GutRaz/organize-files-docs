# Geavanceerd / Diagnostiek

## Organiseer afstemming

Geavanceerd / Diagnostiek onthult **OrganizeFilesEngine**-opties zonder het hoofdpaneel onoverzichtelijk te maken.

De organisatiemodi kunnen dedupe, bestemmingsindex, unieke datumregels, verplaatsings- en opsommingsthreading, BFS-supplement, hervattingsbestand en extra unieke hoofdmappen afstemmen.

Reparatie houdt alleen de timing van nieuwe pogingen van het netwerk en de schijf vol, gedetecteerde grafische hardwarelanen voor optionele volledige videocontrole, hash-leesbuffer en JSON-hartslag. Andere velden zijn zichtbaar voor context, maar uitgeschakeld.

Wanneer bronnen of uitvoer live zijn op NAS- of UNC-paden, verlaag dan de parallelliteit, laat het opnieuw proberen van het netwerk ingeschakeld, laat supplement BFS ingeschakeld voor oneven SMB-bomen, en probeer de 8 MiB-hashbuffer als het hashen langzaam is.

# Geavanceerd / Diagnostiek — elke optie

## Over dit hoofdstuk

Deze besturingselementen zijn engine-opties. De desktop (Windows, macOS, Linux), Android, iOS en het opdrachtregelprogramma lezen dezelfde waarden.

De **Organisatie**-modi gebruiken elk besturingselement hieronder, tenzij de gebruikersinterface het grijs weergeeft. **Reparatie** gebruikt alleen nieuwe netwerkpogingen, nieuwe pogingen bij een volle schijf, gedetecteerde grafische hardwarelanen (met volledige videocontrole), de hash-leesbuffer, heartbeat-JSON, **Hervattingsbestand** en **Opnieuw beginnen (hervattingsbestand afkappen)**. Andere velden blijven zichtbaar, maar worden tijdens de reparatie genegeerd.

## Netwerkbronnen (NAS / UNC)

Als bronnen of uitvoer op SMB/CIFS-shares, NAS-volumes of toegewezen schijven staan, lees dan dit gedeelte aandachtig door.

- **Waarom afstemmen**: threadaantallen die op een lokale SSD werken, kunnen een filer blokkeren of overbelasten.
- **Wat u kunt proberen** — Laat netwerk opnieuw proberen ingeschakeld. Verlaag de verplaatsingsthreads en enum parallelle max. bij time-outs. Laat supplement BFS ingeschakeld, tenzij zonder dit supplement een volledige telling is geverifieerd. Probeer de hashbuffer van 8 MiB als het hashen via het netwerk langzaam gaat.
- **Netwerkwachten uitschakelen**: mislukt snel bij tijdelijke netwerkfouten. Riskant op wifi of drukke aandelen.

## Dedupe-modus

Hoe de engine beslist dat twee bestanden duplicaten zijn.

| Modus | Wat het doet | Wanneer | Afruil |
| ---- | ------------ | ----------- | --------- |
| **Hash (SHA-256)** | Leest en hasht de volledige inhoud van elk opgenomen bronbestand en groepeert vervolgens identieke bytes. | Sterkste praktische modus. Hash (SHA-256) is vereist voor verwijderen op de bron (duplicaten en problematische bestanden). | Het langzaamst op grote bomen of NAS. Geen enkel algoritme mag worden gepresenteerd als een absolute garantie. |
| **Grootte + tijd + naam** | Sleutel = grootte, UTC-tekens voor laatste schrijfbeurt, naam in kleine letters en vervolgens volledige SHA-256-verificatie. | Conservatieve compatibiliteitsmodus voor oudere mediamapindelingen. | Kan hernoemde duplicaten missen. Nooit gebruiken met het verwijderen van duplicaten of problematische bestanden. |
| **Geen** | Geen ontdubbeling tussen bestanden. | Alleen sorteren, geen dubbele opruiming. | Duplicaten blijven in bronnen. |

## Bestemmingsindex overslaan

- **Uit (standaard)** — Scant bestaande **Unieke** uitvoer en indexeert deze voordat deze wordt gehasht. Veiliger bij hergebruik van dezelfde uitvoermap.
- **Aan** — Slaat die scan over.
- **Voordeel** — Sneller bij grote outputbomen.
- **Risico** — Er kan meer dubbele inhoud in Unique terechtkomen.

## Min. jaar voor Uniek

Minimum kalenderjaar voor datummappen onder **Uniek** in media-indelingen. **Waarom** — Voorkomt dat zeer oude bestanden in oneven jaarmappen worden verspreid als de metagegevens onjuist zijn.

## Verplaats threads

Parallelle bestandsverplaatsingen nadat bestemmingen zijn gereserveerd.

- **Hoger** — Sneller op lokale SSD.
- **Lager** — Veiliger op NAS-, USB- of Wi-Fi-toegewezen schijven.

## Classificatie- en hash-threads

Parallelle workers tijdens de bronscan en de SHA-256-deduplicatie.

- **Classificatiedraden** — Bestanden zoeken en classificeren. CLI: `--classify-threads <n>`.
- **Hash-draden** — Workers voor het hashen van inhoud. CLI: `--hash-threads <n>`.
- **Overschrijvingen** — Handmatige waarden overschrijven de standaardwaarden van het profiel (`--profile`).

## Opsomming parallel max

Limiet voor parallelle directoryvermelding tijdens scan.

- **0** = motor automatisch.
- **Lager** — Minder druk op SMB wanneer er veel mappen tegelijk worden weergegeven.

## Supplement BFS directorypas

- **Aan (standaard)** — Een extra ondiepe doorgang in de breedte.
- **Waarom** — Sommige NAS-paden of diepe bomen ogen na de eerste doorgang onvolledig.
- **Uit** — Pas nadat een volledig bestandsaantal zonder deze doorgang is vastgesteld.
- **CLI** — `--no-bfs` zet deze doorgang uit.

## Statusbestand hervatten Optioneel

UTF-8-pad. Succesvolle zetten voegen `B64|`-regels toe, zodat de volgende organisatierun voltooide bronnen kan overslaan.

- **Waarom** — Ga door met lange klussen na een stop of crash.
- **Standaardpad** — Wanneer het veld tijdens runtime leeg is, gebruikt de engine `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt`. Zonder uitvoer gebruikt het `sessions\<id>\resume\OrganizeFiles.resume.txt` onder het app-profiel.
- **Bureaubladgebruikersinterface** — Alleen-lezen padlijst voor muisselectie en kopiëren. Wanneer er al een Hervattingsbestand bestaat op de standaardlocatie, verschijnt het pad automatisch. **Bladeren** kiest een logmap en voegt `OrganizeFiles.resume.txt` toe. **Verwijderen** maakt het pad vrij. Wanneer deze leeg is, toont de hint het pad dat tijdens runtime werd gebruikt.

## Start opnieuw

Kapt het Hervattingsbestand af wanneer een **echte** organisatierun start (Proefrun wordt niet afgekapt). Met **Voortgang en werkruimte opslaan** wordt ook de opgeslagen momentopname van de gebruikersinterface gewist bij het starten van de uitvoering. **Waarom** — Forceer een volledige hertelling in plaats van door te gaan met een oud hervattingslogboek.

## Extra Unieke scanwortels

Eén map per regel: extra **Unieke** bomen om te indexeren (verouderde lay-out, ander volume).

- **Waarom** — Dedupe kan bestanden zien die al ergens anders zijn geordend, zonder ze opnieuw te verplaatsen.
- **Bureaubladgebruikersinterface** — Alleen-lezenlijst voor kopiëren per regel. **Toevoegen** voegt een gekozen map toe. **Verwijderen** verwijdert de geselecteerde regel (bijvoorbeeld een oude `Uniques`-boom op NAS).

## Netwerk opnieuw proberen (seconden)

Seconden om voorbijgaande netwerk-in- en uitvoer opnieuw te proberen.

- **Waarom** — SMB-servers laten inactieve sessies vallen. Gebruikt bij ordenen en herstellen.
- **Netwerkwachten uitzetten** — Stop met wachten en faal in plaats daarvan.

## Nieuwe poging schijf vol

(seconden) / Wachttijd schijf vol uitschakelen

Hetzelfde patroon wanneer het uitvoervolume onvoldoende ruimte heeft. **Waarom** — Tijd om schijf vrij te maken tijdens lange runs.

## Banen voor grafische hardware

Alleen wanneer de ingebouwde **volledige videocontrole** aan staat en **Gevonden grafische hardware gebruiken** ook. Een waarde boven **0** legt een vast aantal banen vast voor gelijktijdige controle over de gevonden makers heen (NVIDIA, AMD, Intel, Apple, mobiel). **0** betekent dat het aantal banen zelf wordt bepaald. Het betekent niet alleen-processor. Kies **Alleen CPU** in de lijst met grafische kaarten om alleen op de processor te bemonsteren. Baanaanduidingen plannen bitstroomcontrole op de processor. Ze roepen de hardwarematige videodecodering van het besturingssysteem niet aan.

- **Voorkeuze op de opdrachtregel** — `--hwaccel <value>` kiest een voorkeuze voor controlebanen (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`) wanneer de volledige videocontrole draait.

## Hash-leesbuffer

Leesbuffer per werknemer tijdens hashen (512 KiB, 1 MiB, 8 MiB). **Waarom** — Grotere buffers helpen wanneer een NAS of een share met hoge latentie traag reageert.

## Ongedaan-maken-journaal vastleggen

Optioneel JSONL-journaal van de verplaatsingen onder de uitvoermap van de run.

- **Waarvoor** — Maakt ongedaan maken via de CLI mogelijk na een echte run.
- **Archief** — Archiveren na het ordenen blijft uit zolang het journaal actief is.
- **CLI** — `--record-undo-journal` (hetzelfde als het vinkje in het hoofdvenster).

## Schrijfrun heartbeat JSON

Schrijft het optionele `Organize.Files.run.json` onder `Output\_OrganizeMediaLogs`.

- **Waarom** — Externe hulpmiddelen kunnen tijdens ordenen of herstellen levende tellers lezen (doorzocht, gepland, voltooid).
- **Tijdsafstand** — Per 10.000 geziene bestanden, per 5.000 treffers en ongeveer elke 15 seconden tijdens bronzoekopdrachten, na elke 1.000 bestanden en hooguit elke 5 seconden tijdens validatie, hashing en verplaatsingen en bij elke grote fase.
