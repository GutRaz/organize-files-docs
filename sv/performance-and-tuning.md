# Avancerat / Diagnostik

## Organisera inställningen

Avancerad / Diagnostik visar **OrganizeFilesEngine**-alternativen utan att belamra huvudpanelen.

Organiseringslägen kan ställa in dedupe, destinationsindex, unika datumregler, flytt- och uppräkningstrådar, BFS-tillägg, resume-fil och extra unika rötter.

Reparation behåller bara nätverks- och diskfulla återförsökstid, upptäckta grafikhårdvarubanor för valfri fullständig videokontroll, hash-läsbuffert och JSON-hjärtslag. Andra fält är synliga för sammanhang men inaktiverade.

När källor eller utdata är live på NAS- eller UNC-vägar, minska parallelliteten, håll nätverksförsök aktiverat, lämna tillägget BFS på för udda SMB-träd och prova 8 MiB hashbufferten om hashningen är långsam.

# Avancerat / Diagnostik — varje alternativ

## Om det här kapitlet

Dessa kontroller är motoralternativ. Skrivbordsappen (Windows, macOS, Linux), Android, iOS och kommandoradsverktyget läser samma värden.

**Ordna**-lägena använder alla kontroller nedan om inte gränssnittet gråmarkerar dem. **Reparation** använder bara nätverksförsök, nytt försök vid full disk, upptäckta grafikhårdvarubanor (med fullständig videokontroll), hash-läsbufferten, hjärtslags-JSON, **Återupptagningsfil** och **Börja om på nytt (korta av återupptagningsfilen)**. Övriga fält förblir synliga men ignoreras under reparationen.

## Nätverkskällor (NAS / UNC)

När källor eller utdata finns på SMB/CIFS-resurser, NAS-volymer eller mappade enheter, granska detta avsnitt noggrant.

- **Varför tuna** — Trådantal som fungerar på en lokal SSD kan stoppa eller överbelasta en fil.
- **Vad du ska prova** — Fortsätt att försöka igen på nätverket. Sänk flyttrådarna och räkna upp parallella max vid timeouts. Låt tillägget BFS vara på om inte en fullständig räkning har verifierats utan det. Prova 8 MiB hashbufferten när hashningen går långsamt över nätverket.
- **Inaktivera nätverksväntan** — Misslyckas snabbt vid tillfälliga nätverksfel. Riskfyllt på Wi-Fi eller upptagna delningar.

## Dedupe-läge

Hur motorn bestämmer att två filer är dubbletter.

| Läge | Vad det gör | När ska du använda | Avvägning |
| ---- | ------------ | ----------- | ---------- |
| **Hash (SHA-256)** | Läser och hashar hela innehållet i varje inkluderad källfil och grupperar sedan identiska byte. | Starkast praktiskt läge. Hash (SHA-256) krävs för radering på källan (dubbletter och problematiska filer). | Långsammast på stora träd eller NAS. Ingen algoritm ska presenteras som en absolut garanti. |
| **Storlek + tid + namn** | Nyckel = storlek, UTC sista-skriv-tickar, gemener namn, sedan fullständig SHA-256-verifiering. | Konservativt kompatibilitetsläge för äldre mediemapplayouter. | Kan missa omdöpta dubbletter. Använd aldrig med radering av dubbletter eller problematiska filer. |
| **Nej** | Ingen korsfil dedupe. | Endast sortering, inte dubblettrensning. | Dubletter stannar i källorna. |

## Hoppa över destinationsindex

- **Av (standard)** — Skannar befintlig **Unik** utdata och indexerar den före hashning. Säkrare när du återanvänder samma utdatamapp.
- **På** — Hoppar över den skanningen.
- **Fördel** — Snabbare på enorma träd.
- **Risk** — Mer duplicerat innehåll kan hamna i Unique.

## Min. år för Unika

Minsta kalenderår för datummappar under **Unik** i medialayouter. **Varför** — Undviker att sprida mycket gamla filer till mappar med udda år när metadata är fel.

## Flytta trådar

Parallella filflyttningar efter att destinationer har reserverats.

- **Högre** — Snabbare på lokal SSD.
- **Lägre** — Säkrare på NAS, USB eller Wi-Fi mappade enheter.

## Klassificerings- och hash-trådar

Parallella arbetare under källskanning och SHA-256-deduplicering.

- **Klassificeringstrådar** — Filsökning och klassificering. CLI: `--classify-threads <n>`.
- **Hashtrådar** — Arbetare för hashning av innehåll. CLI: `--hash-threads <n>`.
- **Åsidosättningar** — Manuella värden åsidosätter profilens standardvärden (`--profile`).

## Enum parallell max

Gräns för parallell kataloglistning under skanning.

- **0** = motor auto.
- **Lägre** — Mindre tryck på SMB när många mappar listas samtidigt.

## Tillägg BFS katalogpass

- **På (standard)** — En extra grund genomgång på bredden.
- **Varför** — Vissa NAS-sökvägar eller djupa träd ser ofullständiga ut efter första genomgången.
- **Av** — Först sedan ett fullständigt filantal bekräftats utan den.
- **CLI** — `--no-bfs` stänger av denna genomgång.

## Återuppta tillståndsfil Valfri

UTF-8 sökväg. Lyckade drag lägger till `B64|`-rader så att nästa organiseringskörning kan hoppa över färdiga källor.

- **Varför** — Fortsätt långa jobb efter stopp eller krasch.
- **Standardsökväg** — När fältet är tomt under körning, använder motorn `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt`. Utan utdata använder den `sessions\<id>\resume\OrganizeFiles.resume.txt` under appprofilen.
- **Skrivbordsgränssnitt** — Skrivskyddad sökvägslista för musval och kopiering. När en resume-fil redan finns på standardplatsen visas sökvägen automatiskt. **Bläddra** väljer en loggmapp och lägger till `OrganizeFiles.resume.txt`. **Ta bort** rensar banan. När den är tom visar tipset den sökväg som användes vid körning.

## Start fresh

Trunkerar resume-filen när en **riktig** organiseringskörning startar (testkörning trunkeras inte). Med **Spara framsteg och arbetsyta** rensas även den sparade ögonblicksbilden av användargränssnittet vid körningsstart. **Varför** — Framtvinga en fullständig omräkning istället för att fortsätta med en gammal resume-logg.

## Extra Unika skanningsrötter

En mapp per rad: extra **Unika** träd att indexera (legacy layout, annan volym).

- **Varför** — Dedupe kan se filer som redan är organiserade någon annanstans utan att flytta dem igen.
- **Skrivbordsgränssnitt** — Skrivskyddad lista för kopia per rad. **Lägg till** lägger till en utvald mapp. **Ta bort** tar bort den valda raden (till exempel ett gammalt `Uniques`-träd på NAS).

## Nätverksförsök igen (sekunder) /

Inaktivera nätverksväntan sekunder för att försöka igen övergående nätverks-I/O.

- **Varför** — SMB-filer släpper inaktiva sessioner. Används av organisering och reparation.
- **Inaktivera nätverksväntan** — Sluta vänta och misslyckas istället.

## Disk full igen (sekunder) / Inaktivera disk full wait

Samma mönster när utgångsvolymen tar slut. **Varför** — Dags att frigöra disken under långa körningar.

## Banor för grafikkortet

Endast när den inbyggda **fullständiga videokontrollen** är påslagen och **Använd upptäckt grafikkort** också är det. Ett värde över **0** fastställer ett bestämt antal banor för samtidig kontroll över de upptäckta tillverkarna (NVIDIA, AMD, Intel, Apple, mobil). **0** betyder att antalet banor tas fram av sig självt. Det betyder inte enbart processor. För stickprov enbart på processorn väljer du **Endast CPU** i listan över grafikkort. Banmärkena planerar bitströmskontroll på processorn. De anropar inte operativsystemets maskinvaruavkodning av video.

- **Förval på kommandoraden** — `--hwaccel <value>` väljer ett förval för kontrollbanor (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`) när den fullständiga videokontrollen körs.

## Hash-läsbuffert

Läsbuffert per arbetare under hashning (512 KiB, 1 MiB, 8 MiB). **Varför** — Större buffertar hjälper när en NAS eller en höglatensdelning är långsam att svara.

## Registrera ångra-journal

Valfri JSONL-journal över flyttar under utdatroten för körningen.

- **Varför** — Möjliggör ångra från CLI efter en riktig körning.
- **Arkiv** — Arkivering efter organisering förblir avstängd medan journalen är aktiv.
- **CLI** — `--record-undo-journal` (samma som kryssrutan i huvudfönstret).

## Skriv run heartbeat JSON

Skriver den valfria `Organize.Files.run.json` under `Output\_OrganizeMediaLogs`.

- **Varför** — Yttre verktyg kan läsa levande räknare (genomgångna, planerade, klara) medan ordnande eller reparation pågår.
- **Tidsintervall** — För var 10 000 sedda filer, var 5 000 träffar och ungefär var 15:e sekund under källgenomgångar, efter var 1 000 filer och högst var femte sekund under validering, hashning och flyttar och vid varje större skede.
