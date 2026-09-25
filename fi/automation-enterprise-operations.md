# Seuranta Prometheus- ja Grafana-työkaluilla

## Mitä laskurit kattavat

Ajastetut työt pitävät pientä joukkoa Prometheus-laskureita ja -mittareita. Jokainen nimi alkaa merkinnällä `organize_files_automation_`, ja koko joukko julkaistaan Prometheus-tekstinä. Kaikki kolme isäntää, jotka suorittavat töitä, julkaisevat saman joukon: työpöytäsovellus, palvelu `OrganizeFiles.JobAgent` ja konteissa käytettävä komentorivi-isäntä.

Laskurit kuvaavat ajastinta, eivät tiedostoja. Laskettavia ovat läpikäynnit, töiden lopputulokset, hyväksynnät, webhook-toimitus ja historian siivous. Työn siirtämistä tiedostoista ei lasketa mitään.

## Vienti tiedostoon ilman avointa porttia

`automation-metrics.prom` kirjoitetaan automaation datakansioon tiedoston `automation-jobs.json` viereen ja päivitetään jokaisen erääntyneen läpikäynnin jälkeen sekä jokaisella luvulla. Muoto on se, jota `node_exporter`-työkalun textfile-kerääjä lukee, joten kone, jolla `node_exporter` jo toimii, on katettu ilman kuuntelevaa porttia, ilman tunnistetta ja ilman palomuurisääntöä. Tiedosto korvataan atomisesti, ja sen paikalle jätetty symbolinen linkki pysäyttää kirjoituksen sen sijaan, että sitä seurattaisiin.

## Lukupiste

Lukupiste on olemassa vain, kun `ORGANIZE_FILES_METRICS_HTTP_PORT` sisältää portin väliltä 1 ja 65535. Ilman tuota muuttujaa mikään ei kuuntele.

| Muuttuja | Vaikutus |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | Kuunneltava portti. Jos se puuttuu tai on alueen ulkopuolella, lukupistettä ei ole lainkaan. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Kuunteluosoite. Oletus on `127.0.0.1`. Arvot `0.0.0.0`, `+` ja `*` tarkoittavat kaikkia osoitteita, ja mikä tahansa muu palautuu arvoon `127.0.0.1`. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | Bearer-tunniste, jota vaaditaan poluilla `/metrics` ja `/ready`. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` antaa polun `/ready` vastata ilman tuota tunnistetta, klusterin koettimia varten. Isännän polut jäävät silloin pois vastauksesta. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | Pilkuin erotellut paluukoodit, joilla `/ready` ilmoittaa, ettei ole valmis. Korvaa sisäänrakennetun luettelon. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` jättää huomiotta viimeisen läpikäynnin paluukoodin sekä tilan ennen ensimmäisen läpikäynnin päättymistä. |
| `ORGANIZE_FILES_READY_JSON` | `1` pakottaa JSON-vastauksen polulla `/ready`, myös kutsujalle, joka pyysi pelkkää tekstiä. |

Loopbackin ulkopuolinen osoite hylätään ennen kuuntelijan avaamista, ellei bearer-tunnistetta ole asetettu. Hylkäys kirjoitetaan virhetulosteeseen ja lähetetään webhook-tapahtumana, koska tuo yhdistelmä luovuttaisi laskurit koko verkolle.

## Palvellut polut

- `/metrics` — laskurit Prometheus-tekstinä. Pyyntö polkuun `/` palauttaa saman sisällön.
- `/ready` — valmius orkestroijalle. Vastaus on `200` heti kun automaatiokansio ottaa vastaan koekirjoituksen, työtiedosto aukeaa, historiakansio ratkeaa datajuuren sisälle ja viimeisin erääntynyt läpikäynti päättyi paluukoodiin, joka ei estä. Muussa tapauksessa vastaus on `503` ja lyhyt syy, kuten `due_pass_not_completed` tai `last_due_pass_license_failed`.
- `/health` — pelkkä elonmerkki. Tuo polku pysyy nimettömänä silloinkin, kun tunniste on asetettu, koska se vastaa `ok` eikä muuta.

Paluukoodit `3` lisenssivirheestä, `8` lukitusta tulospuusta, `10` vahvistamattomasta poistosta ja `11` varausristiriidasta estävät valmiuden oletuksena. Polun `/ready` sisältö on JSON, ellei kutsuja lähetä otsaketta `Accept: text/plain` tai lisää tarkennetta `?format=text`.

## Laskurit

| Nimi | Sisältö |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Ajastimen aloittamat erääntyneet läpikäynnit. |
| `organize_files_automation_jobs_started_total` | Työsuoritukset, jotka pääsivät käynnissä olevaan tilaan. |
| `organize_files_automation_jobs_skipped_total` | Ohitetut työt: Docker- tai Kubernetes-ympäristö, joka ei ole valmis, sovellukseen kohdistuva työ näytöttömällä isännällä, varattu tulosjuuri, tai orkestroijan hylkäämä työ. |
| `organize_files_automation_jobs_failed_total` | Työsuoritukset, jotka päättyivät virheeseen. |
| `organize_files_automation_jobs_awaiting_approval_total` | Todelliset suoritukset, jotka odottavat hyväksyntää. |
| `organize_files_automation_execute_approvals_total` | Todelliselle suoritukselle myönnetyt hyväksynnät. |
| `organize_files_automation_execute_approvals_expired_total` | Hyväksynnät, joiden määräaika umpeutui ennen käyttöä. |
| `organize_files_automation_claim_conflicts_total` | Kerrat, jolloin toinen isäntä piti jo varausta tulosjuureen. |
| `organize_files_automation_runs_orphaned_total` | Orvoiksi palautetut suoritukset, jotka pysähtynyt isäntä jätti jälkeensä. |
| `organize_files_automation_job_events_total` | Yksi laskuri tapahtumaa kohti, tunnisteinaan `event`, `job_id`, `target` ja `jobs_file`. |
| `organize_files_automation_webhook_posts_succeeded_total` | Hyväksytyt webhook-toimitukset. |
| `organize_files_automation_webhook_posts_failed_total` | Hylätyt tai tavoittamattomat webhook-toimitukset. |
| `organize_files_automation_webhook_dead_letter_depth` | Rivit, jotka odottavat juuri nyt toimittamattomien webhook-viestien tiedostossa. |
| `organize_files_automation_log_retention_pruned_total` | Säilytyksen poistamat suorituslokit. |
| `organize_files_automation_runs_index_compacted_total` | Rivit, jotka tiivistys poisti suoritusten hakemistosta. |
| `organize_files_automation_last_due_pass_exit_code` | Viimeksi päättyneen läpikäynnin paluukoodi. `0` on puhdas läpikäynti. |
| `organize_files_automation_last_due_pass_completed_utc` | Viimeksi päättyneen läpikäynnin Unix-aika sekunteina, ja `0` ennen ensimmäistä. |

## Koontinäyttö ja hälytyssäännöt

Valmis Grafana-koontinäyttö julkaistaan käyttöönottotiedostojen mukana nimellä `grafana-organize-files-automation.json`, otsikkona **OrganizeFiles Automation**. Sen kymmenen ruutua näyttävät erääntyneet läpikäynnit, aloitetut ja epäonnistuneet työt, varausristiriidat, töiden läpimenon tunnin ajalta, viimeisimmän paluukoodin, toimittamattomien viestien määrän, webhook-virheet vuorokauden ajalta, hyväksyntää odottavat työt ja työtapahtumat tiloittain. Jokainen ruutu nimeää tietolähteensä paikkamerkillä `${DS_PROMETHEUS}`.

Vastaavat hälytyssäännöt ovat `alerts-organize-files-automation.yaml`, ja `prometheus-rule-automation.yaml` on Kubernetes-kuori työkalulle `kube-prometheus-stack`. Nollasta poikkeava viimeisin paluukoodi varoittaa viiden minuutin jälkeen, lisenssivirhe on kriittinen yhden minuutin jälkeen, ja loput säännöt kattavat epäonnistuneet työt, varausristiriidat, webhook-virheet, toimittamattomien viestien ruuhkan ja vuorokauden odottaneet hyväksynnät. Molemmat tiedostot tarkistetaan jokaisessa käännöksessä, joten yllä olevat nimet pysyvät laskurien tahdissa.

# Ajon tuloste ja mittarit

## Tilarivi

**Ajon tuloste** -alue näyttää:

- Sovelluksen nykyinen tila ja moottorin edistyminen.
- **CPU** ja kaksi **muisti**-arvoa vain tälle prosessille.
- **GPU**-rivit, Windowsissa: tämän prosessin osuus kustakin näytönohjaimesta, ei koko näytönohjain.

Samaa kompaktia resurssipalkkia käytetään uudelleen toissijaisissa työkaluikkunoissa, kuten tiedostojen tutkimisessa, ajoitetuissa töissä ja tiedostojen korjauksessa.

## Muistitarrat

- **Yksityiset tavut / commit** — prosessin varaama yksityinen virtuaalimuisti.
- **Työsarja / muisti** — tämän prosessin hallussa oleva pysyvä RAM. Se voi erota toisesta käyttöjärjestelmänäytöstä, koska jokainen käyttöjärjestelmä- ja työpöytäympäristön nimike käsittelee muistia eri tavalla.

## Suorita heartbeat JSON (valinnainen)

Ota käyttöön **Kirjoita run heartbeat JSON** kohdassa **Lisäasetukset/Diagnostiikka**. Moottori kirjoittaa `Organize.Files.run.json` alla `Output\_OrganizeMediaLogs` (sama kansio kuin oletusjärjestyksen jatkotiedosto).

- **Polku** — päivitetään atomisesti järjestely- ja korjausajojen aikana.
- **Ajoitus** — lähteitä selattaessa tiedosto kirjoitetaan uudelleen jokaista 10 000 nähtyä tiedostoa ja jokaista 5 000 osumaa kohden sekä noin 15 sekunnin välein niin kauan kuin selaus jatkuu, joten hitaasti listautuva suuri verkkopuu näyttää silti, että ajo on käynnissä. Tarkistuksen, tiivistämisen ja siirtojen aikana se kirjoitetaan uudelleen jokaisen 1 000 tiedoston jälkeen, enintään viiden sekunnin välein. Kirjoitukset alussa ja lopussa tapahtuvat yhä, kun ajo alkaa ja päättyy.
- **Edistyminen** — niin kauan kuin tiedostomäärät yhä kasvavat, pääedistymispalkki näyttää tähän mennessä nähdyt tiedostot sadan prosentin sijaan, kunnes vaiheella on tiedossa oleva kokonaismäärä.
- **Kentät** — `schema`, `mode`, `phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`), `runState`(`active`/`completed`/`failed`/`cancelled`), `utc` (ISO-8601), `dryRun`, `outputRoot`, `validateMedia`, `deepVideoValidate`, `gpuDeviceCount`, `hwaccel`, valinnainen`correlationId`, sisäkkäinen `progress` laskurit.
- **Loki** — Run-tulostuspaneeli tulostaa koko polun alussa ja kun tiedosto tallennetaan lopussa. Käytä **Avaa heartbeat log -kansio** / **Näytä heartbeat JSON-tiedosto** kohdassa Lisäasetukset / Diagnostiikka.
- **CLI** — `--heartbeat-json` päällä OrganizeFiles.Cli. Peruuta ja kohtalokkaat shell-virheet kirjoittaa `cancelled`/`failed` `runState` kun käytössä.
