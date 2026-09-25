# Lisäasetukset / Diagnostiikka

## Järjestä viritys

Lisäasetukset / Diagnostiikka paljastaa **OrganizeFilesEngine**-vaihtoehdot turhauttamatta pääpaneelia.

Järjestämistilat voivat virittää dedupe-toiminnon, kohdehakemiston, ainutlaatuiset päivämääräsäännöt, siirto- ja luettelosäikeistyksen, BFS-lisäosan, jatkotiedoston ja ylimääräisiä ainutlaatuisia juuria.

Korjaus säilyttää vain verkon ja levyn täyteen uudelleenyritysten ajoituksen, havaitut grafiikkalaitteiston kaistat valinnaista täydellistä videotarkistusta varten, hash-lukupuskurin ja JSON-sykeen. Muut kentät ovat näkyvissä kontekstille, mutta ne eivät ole käytössä.

Kun lähteet tai lähtö reaaliajassa NAS- tai UNC-poluilla, pienennä rinnakkaisuutta, pidä verkon uudelleenyritys käytössä, jätä BFS-lisä päälle parittomille SMB-puille ja kokeile 8 MiB:n hajautuspuskuria, jos hajautus on hidasta.

# Lisäasetukset / Diagnostiikka - jokainen vaihtoehto

## Tietoja tästä luvusta

Nämä säätimet ovat moottorin asetuksia. Työpöytä (Windows, macOS, Linux), Android, iOS ja komentorivityökalu lukevat samat arvot.

**Järjestä**-tilat käyttävät kaikkia alla olevia säätimiä, ellei käyttöliittymä himmennä niitä. **Korjaus** käyttää vain verkon uudelleenyritystä, levyn täyttymisen uudelleenyritystä, havaittuja grafiikkalaitteiston kaistoja (täydellä videotarkistuksella), tiivisteen lukupuskuria, heartbeat-JSONia, **Jatkamistilatiedosto** ja **Aloita alusta (typistää jatkotiedosto)**. Muut kentät pysyvät näkyvissä, mutta ne ohitetaan korjauksen aikana.

## Verkkolähteet (NAS / UNC)

Kun lähteet tai lähtö ovat SMB/CIFS-osuuksissa, NAS-taltioissa tai yhdistetyissä asemissa, katso tämä osio huolellisesti.

- **Miksi virittää** — Paikallisella SSD-levyllä toimivat säikeet voivat pysäyttää tai ylikuormittaa tiedostoa.
- **Mitä kokeilla** — Pidä verkon uudelleenyritys päällä. Alenna siirtolankoja ja enum rinnakkain max aikakatkaisuissa. Jätä lisäosa BFS päälle, ellei täyttä määrää ole vahvistettu ilman sitä. Kokeile 8 MiB:n hajautuspuskuria, kun hajautus on hidasta verkossa.
- **Poista verkon odotus käytöstä** — Epäonnistuu nopeasti ohimenevien verkkovirheiden yhteydessä. Riskialtista Wi-Fi-yhteydellä tai varattuilla jaoilla.

## Dedupe-tila

Kuinka moottori päättää, että kaksi tiedostoa on kaksoiskappale.

| Tila | Mitä se tekee | Milloin käyttää | Kompromissi |
| ---- | ------------ | ----------- | --------- |
| **Hash (SHA-256)** | Lukee ja hajauttaa jokaisen sisällytetyn lähdetiedoston koko sisällön ja ryhmittelee sitten identtiset tavut. | Vahvin käytännöllinen tila. Hash (SHA-256) on pakollinen lähteessä poistamiseen (kaksoiskappaleet ja ongelmalliset tiedostot). | Hitain suurilla puilla tai NAS. Mitään algoritmia ei pidä esittää ehdottomana takuuna. |
| **Koko + aika + nimi** | Avain = koko, UTC-viimeisen kirjoitusmerkinnät, pienillä kirjaimilla kirjoitettu nimi, sitten täydellinen SHA-256-vahvistus. | Konservatiivinen yhteensopivuustila vanhemmille mediakansioasetteluille. | Uudelleennimetyt kaksoiskappaleet saattavat jäädä huomaamatta. Älä koskaan käytä kaksoiskappaleiden tai ongelmallisten tiedostojen poiston kanssa. |
| **Ei mitään** | Ei tiedostojen välisten kopioiden poistamista. | Vain lajittelu, ei kaksoissiivous. | Kaksoiskappaleet pysyvät lähteissä. |

## Ohita kohdeindeksi

- **Pois (oletus)** — Tarkistaa olemassa olevan **Ainutlaatuisen**-ulostulon ja indeksoi sen ennen tiivistystä. Turvallisempaa käytettäessä samaa tulostuskansiota uudelleen.
- **Päällä** — Ohittaa skannauksen.
- **Etu** — Nopeampi suurilla tuotantopuilla.
- **Riski** — Uniquen sisälle voi päätyä enemmän päällekkäistä sisältöä.

## Uniikit min. vuosi

Vähimmäiskalenterivuosi media-asetteluissa **Ainutlaatuinen**-kohdan päivämääräkansioille. **Miksi** — Estää erittäin vanhojen tiedostojen hajoamisen parittoman vuoden kansioihin, kun metatiedot ovat vääriä.

## Siirrä säikeitä

Rinnakkaistiedostot siirretään kohteiden varauksen jälkeen.

- **Korkeampi** — Nopeampi paikallisella SSD:llä.
- **Matala** — Turvallisempi NAS-, USB- tai Wi-Fi-kartoitetuissa asemissa.

## Luokittelu- ja tiivistesäikeet

Rinnakkaiset työntekijät lähdeskannauksen ja SHA-256-deduplikoinnin aikana.

- **Luokittelusäikeet** — Tiedostojen etsintä ja luokittelu. Komentorivillä: `--classify-threads <n>`.
- **Hash-säikeet** — Sisällön tiivistäjät. Komentorivillä: `--hash-threads <n>`.
- **Ohitukset** — Manuaaliset arvot ohittavat profiilin oletusarvot (`--profile`).

## Enum rinnakkain max

Rajoitus rinnakkaisten hakemistojen listalle skannauksen aikana.

- **0** = moottorin automaattinen.
- **Matala** — Vähemmän painetta SMB:lle, kun luettelossa on monta kansiota kerralla.

## Täydennys BFS hakemistopassi

- **Päällä (oletus)** — Ylimääräinen matala leveyssuuntainen läpikäynti.
- **Miksi** — Jotkin NAS-polut tai syvät puut näyttävät ensimmäisen läpikäynnin jälkeen keskeneräisiltä.
- **Pois** — Vasta kun täysi tiedostomäärä on varmistettu ilman sitä.
- **CLI** — `--no-bfs` kytkee tämän läpikäynnin pois.

## Jatkamistilatiedosto Valinnainen

UTF-8-polku. Onnistuneet siirrot lisäävät rivit `B64|`, jotta seuraava järjestysajo voi ohittaa valmiit lähteet.

- **Miksi** — Jatka pitkiä töitä pysähtymisen tai kaatumisen jälkeen.
- **Oletuspolku** — Kun kenttä on tyhjä ajon aikana, moottori käyttää `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt`. Ilman lähtöä se käyttää `sessions\<id>\resume\OrganizeFiles.resume.txt` sovellusprofiilin alla.
- **Työpöytäkäyttöliittymä** — Vain luku -polkuluettelo hiiren valintaa ja kopiointia varten. Kun jatkotiedosto on jo olemassa oletussijainnissa, polku tulee näkyviin automaattisesti. **Selaa** valitsee lokikansion ja lisää siihen `OrganizeFiles.resume.txt`. **Poista** tyhjentää polun. Kun vihje on tyhjä, se näyttää ajon aikana käytetyn polun.

## Aloita uudelleen

Katkaisee jatkamistiedoston, kun **todellinen** järjestelyajo alkaa (testiajo ei katkaise). **Tallenna edistyminen ja työtila** -toiminto poistaa myös tallennetun käyttöliittymän tilannevedoksen ajon alkaessa. **Miksi** — Pakota täydellinen uudelleenlaskenta sen sijaan, että jatkaisit vanhaa jatkolokia.

## Ainutlaatuiset tarkistuksen

Yksi kansio riviä kohden: lisää indeksoitavia **Unique**-puita (vanha rakenne, toinen levy).

- **Miksi** — Kaksoiskappaleiden karsinta näkee muualla jo järjestetyt tiedostot siirtämättä niitä uudelleen.
- **Työpöydän käyttöliittymä** — Vain luettava luettelo rivi kerrallaan kopioitavaksi. **Lisää** liittää valitun kansion. **Poista** poistaa valitun rivin (esimerkiksi vanhan `Uniques`-puun NAS-levyltä).

## Verkon uudelleenyritys (sekuntia) /

Sekunnit, joiden ajan ohimenevää verkkoliikennettä yritetään uudelleen.

- **Miksi** — SMB-palvelimet katkaisevat joutilaat istunnot. Käytössä järjestelyssä ja korjauksessa.
- **Poista verkon odotus** — Lopeta odottaminen ja epäonnistu sen sijaan.

## Levy täynnä uudelleenyritys (sekuntia) /

Disk-full-odota käytöstä.

Sama kuvio, kun tulostustaltio loppuu. **Miksi** — Aika vapauttaa levy pitkien ajojen aikana.

## Näytönohjaimen kaistat

Vain kun sisäänrakennettu **täysi videotarkistus** on päällä ja **Käytä havaittua näytönohjainta** on päällä. Nollaa suurempi arvo asettaa kiinteän kaistamäärän rinnakkaiselle tarkistukselle havaittujen valmistajien kesken (NVIDIA, AMD, Intel, Apple, mobiili). **0** tarkoittaa, että kaistamäärä selvitetään itse. Se ei tarkoita pelkkää suoritinta. Pelkällä suorittimella näytteistämiseen valitse näytönohjainluettelosta **Vain suoritin**. Kaistamerkinnät suunnittelevat bittivirran tarkistuksen suorittimella. Ne eivät kutsu käyttöjärjestelmän laitteistopohjaista videonpurkua.

- **Komentorivin esiasetus** — `--hwaccel <value>` valitsee tarkistuskaistojen esiasetuksen (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`), kun täysi videotarkistus on käynnissä.

## Hash-lukupuskuri

Työntekijäkohtainen lukupuskuri tiivistyksen aikana (512 KiB, 1 MiB, 8 MiB). **Miksi** — Suuremmat puskurit auttavat hidastamaan NAS:n ja korkean viiveen jakoja.

## Tallenna kumoamisloki

Valinnainen JSONL-loki siirroista ajon tuloskansion alla.

- **Miksi** — Mahdollistaa kumoamisen CLI:stä todellisen ajon jälkeen.
- **Arkisto** — Järjestelyn jälkeinen arkistointi pysyy pois päältä lokin ollessa aktiivinen.
- **CLI** — `--record-undo-journal` (sama kuin päänäkymän valintaruutu).

## Kirjoita run heartbeat JSON

Kirjoittaa valinnaisen tiedoston `Organize.Files.run.json` polkuun `Output\_OrganizeMediaLogs`.

- **Miksi** — Ulkoiset työkalut voivat lukea eläviä laskureita (selattu, suunniteltu, valmis) järjestelyn tai korjauksen aikana.
- **Ajoitus** — Jokaista 10 000 nähtyä tiedostoa ja jokaista 5 000 osumaa kohden sekä noin 15 sekunnin välein lähteitä selattaessa, jokaisen 1 000 tiedoston jälkeen ja enintään viiden sekunnin välein tarkistuksen, tiivistämisen ja siirtojen aikana sekä jokaisessa suuressa vaiheessa.
