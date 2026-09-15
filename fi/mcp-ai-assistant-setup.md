# AI-avustaja (MCP)

Lisensoidut tiimit yhdistävät **OrganizeFiles.Cli** -ohjelman johonkin näistä: Claude Desktop, **Cursor**, VS Code Copilot tai muu Model Context Protocol -asiakasohjelma, jota kutsutaan alla MCP-asiakkaaksi. Liitin on Python-paketti **organize-files-mcp**. Sen voi ladata ilmaiseksi osoitteesta github.com/GutRaz/organize-files-docs, kansiosta `mcp/`.

**Työpöytäsovelluksessa:** avaa **MCP-asetukset…** kohdasta **Sovellus ja tiedot** asetussarakkeessa tai työkaluvalikosta. Valitse **MCP-yhteys**: **Pois päältä**, **Seuranta** tai **Hallinta**. Kopioi sitten JSON-koodinpätkä. Lataa MCP uudelleen tekoälysovelluksessa jokaisen tason muutoksen jälkeen, koska **Hallinta** luo joka kerta uuden tunnuksen.

**Kysy ohjeavustajalta** ”setup mcp” tai ”cum setez mcp”, niin saat nykyisen järjestelmän vaiheet.

## MCP-käyttötasot, jotka asetetaan sovelluksessa

Tasot vastaavat kolmea työn lajia: **luku / esikatselu / suoritus**.

| Taso | Työn laji | Mitä tekoäly voi tehdä |
|-------|--------|-------------------|
| **Pois päältä** | — | Vain `organize_mcp_status`. Ei diagnostiikkaa eikä pääsyä työtilaan. |
| **Seuranta** | **Luku** | Kaikki tason Pois päältä toiminnot sekä vain luku -diagnostiikka, ajojen ja tehtävien historia, lukitukset, auditointitarkistukset, **`organize_capabilities`** ja **`organize_workspace_snapshot`**. `organize_capabilities` luettelee ajotilat, niiden joukossa **`ai`**, siirtoalueet ja kohteet. `organize_workspace_snapshot` näyttää pääikkunaan tallennetun työtilan. Ei esikatselua eikä suoritusta. |
| **Hallinta** | **Esikatselu** / **Suoritus** | Kaikki tason Seuranta toiminnot sekä **`organize_create_job`**, **`organize_run_workspace`** ja **`organize_remove_empty_organize_layout`**. Tarvitsee **ohjaustunnuksen** MCP-asetuksiin, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **Esikatselu** on `organize_run_workspace`, kun tallennetussa työtilassa **Testiajo** on päällä, joten mitään ei kirjoiteta. **Suoritus** on sama työkalu, kun Testiajo on pois päältä, joten tiedostot siirretään. Liitin jättää `--confirm-destructive` pois, ellei kutsu aseta `confirm_destructive=true`, ja ilman sitä komentorivi kieltäytyy ilmoituksella `confirm_destructive_required`. |

Ohjaustiedosto on **`mcp-control.json`**, tiedoston `automation-jobs.json` vieressä sovelluksen profiilikansiossa. Kopioitu koodinpätkä ei mainitse sitä, koska liitin löytää sen oletusprofiilikansiosta. Aseta **`ORGANIZE_FILES_MCP_CONTROL_FILE`** vain, kun tiedosto on muualla. Tasolla **Hallinta** koodinpätkä asettaa myös **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`**.

**Siirtäminen ja poistaminen vaatii toisen, ihmisen tekemän vaiheen.** Avustaja asettaa vahvistuksen itse, joten sen lukema teksti voisi houkutella sen vahvistamaan. Ajo, joka ei ole testiajo, vaatii siksi myös kohdassa **MCP-asetukset** avatun ikkunan, ja se ikkuna sulkeutuu itsestään 15 minuutin kuluttua. Ikkunan ulkopuolella avustaja voi yhä valmistella ajon ja näyttää ajon esikatselun, mutta itse ajo hylätään. Sekä ohjaustiedosto että ikkuna on allekirjoitettu avaimella, joka on tällä asennuksella. Käsin muutettu tai toiselta tietokoneelta kopioitu ohjaustiedosto lasketaan tasoksi Pois päältä.

## MCP-työkalut tasoittain

**Aina, myös tasolla Pois päältä:** `organize_mcp_status`

**Seuranta ja Hallinta:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` ja `organize_run_raw_cli`, joka hyväksyy vain lukevia komentoja.

**Myös tasoilla Seuranta ja Hallinta:** `organize_capabilities`, joka luettelee ajotilan **`ai`** tekoäly- ja ML-tiedostoille, ja `organize_workspace_snapshot`.

**Vain Hallinta:** `organize_create_job` työtilasta tai tehtävän JSONista, `organize_run_workspace` esikatseluun tai todelliseen ajoon työtilan Testiajo-asetuksen mukaan, ja `organize_remove_empty_organize_layout`, joka poistaa tyhjät asettelukansiot olemassa olevan tulosteen sisältä eikä koskaan luo itse tulostekansiota.

Tiedostoja siirtävät tai poistavat komennot on MCP:n kautta aina estetty tason **Hallinta** ulkopuolella. Mikään muu asetus ei salli niitä.

## Komentorivin valitsimet, joita liitin käyttää

| Valitsin | Taso | Tarkoitus |
|------|-------|---------|
| `--mcp-control-status` | mikä tahansa | JSON, jossa on taso, ohjaustiedoston polku sekä tasojen Seuranta ja Hallinta merkinnät |
| `--mcp-capabilities` | Seuranta ja ylempi | JSON-luettelo ajotiloista, niiden joukossa **`ai`**, siirtoalueista ja kohteista |
| `--mcp-workspace-snapshot` | Seuranta ja ylempi | Tallennettu työtila ja miten siitä tulee tehtävä |
| `--mcp-create-job` | Hallinta | Luo tehtävän valitsimella `--from-workspace` tai `--mcp-job-json` |
| `--mcp-run-workspace` | Hallinta | Ajaa tallennetun työtilan valitsimilla `--allow-app-target` ja `--mcp-control-token` |
| `--remove-empty-organize-layout` | Hallinta | Poistaa tyhjät asettelukansiot olemassa olevan `--output`-kansion sisältä |
| `--confirm-destructive` | Hallinta | Tarvitaan valitsimen `--mcp-run-workspace` kanssa ajossa, joka siirtää tai poistaa. Liitin välittää sen vain, kun `confirm_destructive=true` |

## Asetukset MCP-asiakkaan JSONissa

| Asetus | Milloin |
|----------|------|
| `ORGANIZE_FILES_CLI` | Polku ohjelmaan OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | Polku tiedostoon `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | Polku tiedostoon `mcp-control.json`, vain kun se ei ole oletusprofiilikansiossa |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | Vain taso **Hallinta**, sovelluksen koodinpätkästä |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | Taso **Hallinta**, tallennetun työtilan ajoihin |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | Valinnainen. Sama tunnus, jota isäntä käyttää lukutoimintoihin |

## Asennus Windowsissa

1. **Python 3.10 tai uudempi** — suorita `python -V` PowerShellissä. Jos Python puuttuu tai on vanhempi, asenna Python osoitteesta [python.org](https://www.python.org/downloads/) ja valitse **Add python.exe to PATH**.
2. **Lataa ja asenna liitin** — lataa github.com/GutRaz/organize-files-docs ZIP-tiedostona, pura se ja suorita `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1`. Skripti luo liittimelle oman Python-ympäristön ja näyttää komennon tekoälysovellusta varten.
3. **Sovelluksessa:** **MCP-asetukset…**, valitse **Seuranta** tai **Hallinta** ja kopioi sitten JSON.
4. **Polut:** `%LocalAppData%\OrganizeFilesCrossPlatform\` sisältää tehtävät ja tiedoston `mcp-control.json`. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **Testi** — suorita `organize_mcp_status` ja sitten `organize_server_info`. Kohdan `cliResolved` on oltava true ja kohdan `mcpLevel` on vastattava sovellusta.

## Asennus macOS:ssä

Samat vaiheet komennoilla **python3** ja `bash mcp/install-organize-files-mcp.sh`. Jos `python3 -V` näyttää 3.9 tai ei Pythonia lainkaan, asenna ensin Python osoitteesta [python.org](https://www.python.org/downloads/macos/). Polut: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Asennus Linuxissa

Samat vaiheet komennoilla **python3** ja `bash mcp/install-organize-files-mcp.sh`. Suorita Debianissa ja Ubuntussa ensin `sudo apt install python3-venv`. Polut: `~/.local/share/OrganizeFilesCrossPlatform/`, tai `$XDG_DATA_HOME`, kun se on asetettu, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Turvallisuus

- MCP toimii käyttöjärjestelmän **paikallisena käyttäjänä**, samoin oikeuksin kuin käsin ajettu komentorivi.
- Pidä **ohjaustunnus** ja **lukemistunnus** salassa kuten salasanat. Kopioi JSON uudelleen, kun Hallinta on otettu käyttöön.
- **`organize_run_workspace`** toimii komentorivillä, ei sovelluksen Suorita-painikkeen kautta. Älä aja kahta tehtävää samaan tulostekansioon samaan aikaan.
- Esimerkit: `mcp/examples/`.

## Ajot, jotka siirtävät tai poistavat

`--mcp-run-workspace` vaatii valitsimen `--confirm-destructive` jokaiseen ajoon, joka ei ole testiajo, siirtääpä ajo, poistaa tai arkistoi. Ilman valitsinta komentorivi vastaa `confirm_destructive_required`. Liitin jättää valitsimen pois, ellei kutsu aseta `confirm_destructive=true`, ja sen voi tehdä vain taso Hallinta. Oletuksena liitin siis kieltäytyy.

## Kielet

Asennusvastaukset tulevat samasta käännetystä oppaasta kuin Dokumentaatio-ikkuna ja Opas-avustaja. `organize_capabilities` ilmoittaa ajotilat ja kohteet, ei sovelluksen teemojen nimiä.
