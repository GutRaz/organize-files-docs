# Avanceret / Diagnostik

## Organiser tuning

Avanceret/Diagnostik afslører mulighederne for **OrganizeFilesEngine** uden at rode på hovedpanelet.

Organiseringstilstande kan indstille dedupe, destinationsindeks, unikke datoregler, trådning af flytning og opregning, BFS-tillæg, genoptag-fil og ekstra unikke rødder.

Reparation beholder kun netværks- og diskfuld genforsøgstid, registrerede grafikhardwarebaner til valgfri fuld videokontrol, hash-læsebuffer og JSON-hjerteslag. Andre felter er synlige for kontekst, men deaktiverede.

Når kilder eller output lever på NAS- eller UNC-stier, sænk paralleliteten, hold netværksforsøg aktiveret, lad supplement BFS være slået til for ulige SMB-træer, og prøv 8 MiB hash-bufferen, hvis hash er langsom.

# Avanceret / Diagnostik — hver mulighed

## Om dette kapitel

Disse kontroller er motorindstillinger. Skrivebordsappen (Windows, macOS, Linux), Android, iOS og kommandolinjeværktøjet læser de samme værdier.

**Organiser**-tilstande bruger alle kontrolelementer nedenfor, medmindre brugergrænsefladen nedtoner dem. **Reparation** bruger kun netværksforsøg, genforsøg ved fuld disk, registrerede grafikhardwarebaner (med fuld videokontrol), hash-læsebuffer, hjerteslag-JSON, **Genoptagelsesfil** og **Start på en frisk (afkort genoptagelsesfilen)**. Andre felter forbliver synlige, men ignoreres under reparation.

## Netværkskilder (NAS / UNC)

Når kilder eller output er på SMB/CIFS-shares, NAS-diskenheder eller tilknyttede drev, skal du gennemgå dette afsnit omhyggeligt.

- **Hvorfor tune** — Trådtal, der fungerer på en lokal SSD, kan stoppe eller overbelaste en filer.
- **Hvad skal du prøve** — Lad netværket prøve igen. Sænk bevægetrådene og opregn parallel max på timeouts. Lad supplement BFS være tændt, medmindre en fuld optælling blev bekræftet uden det. Prøv 8 MiB hash-bufferen, når hashing er langsom over netværket.
- **Deaktiver netværksvent** — Mislykkes hurtigt ved forbigående netværksfejl. Risikabelt på Wi-Fi eller travle delinger.

## Dedupe-tilstand

Hvordan motoren beslutter, at to filer er dubletter.

| Tilstand | Hvad det gør | Hvornår skal du bruge | Afvejning |
| ---- | ------------ | ----------- | ---------- |
| **Hash (SHA-256)** | Læser og hashes det fulde indhold af hver inkluderet kildefil og grupperer derefter identiske bytes. | Stærkeste praktiske tilstand. Hash (SHA-256) er påkrævet til sletning på kilden (dubletter og problematiske filer). | Langsomst på store træer eller NAS. Ingen algoritme bør præsenteres som en absolut garanti. |
| **Størrelse + tid + navn** | Nøgle = størrelse, UTC-sidste-skriv-flåter, navn med små bogstaver, derefter fuld SHA-256-bekræftelse. | Konservativ kompatibilitetstilstand til ældre mediemappelayouts. | Kan gå glip af omdøbte dubletter. Brug aldrig med sletning af dubletter eller problematiske filer. |
| **Ingen** | Ingen krydsfil dedupe. | Kun sortering, ikke dobbelt oprydning. | Dubletter bliver i kilderne. |

## Spring destinationsindeks over

- **Fra (standard)** — Scanner eksisterende **Unik** output og indekserer det før hash. Sikrere, når du genbruger den samme outputmappe.
- **Til** — Springer den scanning over.
- **Fordel** — Hurtigere på enorme træer.
- **Risiko** — Mere duplikeret indhold kan lande i Unique.

## Unikke min. år

Minimum kalenderår for datomapper under **Unik** i medielayouts. **Hvorfor** — Undgår at sprede meget gamle filer i mapper med ulige år, når metadata er forkerte.

## Flyt tråde

Parallelle filflytninger, efter at destinationer er reserveret.

- **Højere** — Hurtigere på lokal SSD.
- **Nedre** — sikrere på NAS, USB eller Wi-Fi-kortlagte drev.

## Klassificerings- og hash-tråde

Parallelle workers under kildescanning og SHA-256-deduplikering.

- **Klassificeringstråde** — Filsøgning og klassificering. CLI: `--classify-threads <n>`.
- **Hash tråde** — Workers til hashing af indhold. CLI: `--hash-threads <n>`.
- **Tilsidesættelser** — Manuelle værdier tilsidesætter profilens standardværdier (`--profile`).

## Maks. Parallel opregning

Grænse for parallel katalogliste under scanning.

- **0** = motor auto.
- **Lavere** — Mindre pres på SMB, når mange mapper vises på én gang.

## Supplement BFS katalogpas

- **Til (standard)** — En ekstra flad bredde-først-gennemgang.
- **Hvorfor** — Nogle NAS-stier eller dybe træer ser ufuldstændige ud efter første gennemgang.
- **Fra** — Først efter at et fuldt filtal er bekræftet uden den.
- **CLI** — `--no-bfs` slår denne gennemgang fra.

## Genoptag tilstandsfil Valgfri

UTF-8-sti. Vellykkede træk tilføjer `B64|`-linjer, så den næste organiseringskørsel kan springe færdige kilder over.

- **Hvorfor** — Fortsæt lange job efter stop eller nedbrud.
- **Standardsti** — Når feltet er tomt på køretid, bruger motoren `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt`. Uden output bruger den `sessions\<id>\resume\OrganizeFiles.resume.txt` under appprofilen.
- **Desktop UI** — Skrivebeskyttet stiliste til musevalg og -kopiering. Når en genoptag-fil allerede findes på standardplaceringen, vises stien automatisk. **Gennemse** vælger en logmappe og tilføjer `OrganizeFiles.resume.txt`. **Fjern** rydder stien. Når den er tom, viser tippet den sti, der blev brugt under kørsel.

## Start frisk

Afkorter genoptag-filen, når en **rigtig** organiseringskørsel starter (prøvekørsel afkortes ikke). Med **Gem fremskridt og arbejdsområde** rydder du også det gemte UI-snapshot ved start af kørsel. **Hvorfor** — Gennemtving en fuld gentælling i stedet for at fortsætte en gammel genoptag-log.

## Ekstra unikke

En mappe pr. linje: ekstra **Unique**-træer at indeksere (gammelt layout, andet drev).

- **Hvorfor** — Dedupe kan se filer der allerede er ordnet et andet sted, uden at flytte dem igen.
- **Skrivebordsflade** — Skrivebeskyttet liste til kopiering linje for linje. **Tilføj** føjer en valgt mappe til. **Fjern** sletter den valgte linje (for eksempel et gammelt `Uniques`-træ på NAS).

## Netværksforsøg igen (sekunder) /

Deaktiver netværksvent sekunder for at prøve forbigående netværks-I/O igen.

- **Hvorfor** — SMB-filer dropper inaktive sessioner. Anvendes til organisering og reparation.
- **Deaktiver netværksvent** — Stop med at vente og mislykkes i stedet.

## Disk fuld genforsøg

(sekunder) / Deaktiver disk fuld ventetid

Samme mønster, når outputvolumen løber tør for plads. **Hvorfor** — Tid til at frigøre disk under lange ture.

## Baner til grafikhardware

Kun når det indbyggede **fulde videotjek** er slået til og **Brug fundet grafikhardware** er slået til. En værdi over **0** fastsætter et bestemt antal baner til parallel validering på tværs af de fundne producenter (NVIDIA, AMD, Intel, Apple, mobil). **0** betyder at banetallet findes af sig selv. Det betyder ikke kun CPU. Vælg **Kun CPU** i listen over grafikkort for stikprøver alene på CPU'en. Banemærker planlægger bitstrømsvalidering på CPU'en. De kalder ikke styresystemets hardwarevideoafkodning.

- **CLI-forvalg** — `--hwaccel <value>` vælger et forvalg for valideringsbaner (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`), når det fulde videotjek kører.

## Hash-læsebuffer

Læsebuffer pr. arbejder under hashing (512 KiB, 1 MiB, 8 MiB). **Hvorfor** — Større buffere hjælper når en NAS eller en høj latens-deling er langsom til at svare.

## Registrer fortryd-journal

Valgfri JSONL-journal over flytninger under outputroden for kørslen.

- **Hvorfor** — Muliggør fortrydelse fra CLI efter en rigtig kørsel.
- **Arkiv** — Arkivering efter organisering forbliver slået fra, mens journalen er aktiv.
- **CLI** — `--record-undo-journal` (samme som afkrydsningsfeltet i hovedvinduet).

## Skriv run heartbeat JSON

Skriver den valgfrie `Organize.Files.run.json` under `Output\_OrganizeMediaLogs`.

- **Hvorfor** — Eksterne værktøjer kan læse levende tællere (skannet, planlagt, fuldført) mens der organiseres eller repareres.
- **Tidsintervaller** — For hver 10.000 sete filer, hver 5.000 træffere og cirka hvert 15. sekund under kildeskanninger, efter hver 1.000 filer og højst hvert 5. sekund under validering, hashing og flytninger og ved hver større fase.
