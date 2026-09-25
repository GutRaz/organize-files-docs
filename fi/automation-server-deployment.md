# CLI, Docker ja Kubernetes (viiteasettelu)

## CLI-automaatio

Tässä luvussa noudatetaan Microsoft/HashiCorp-tyyliä: käyttörivi, lipputaulukko (englanninkieliset tokenit), sitten kopioi-liitä-esimerkkejä.

CLI (OrganizeFiles.Cli)
  KÄYTTÖ: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  KÄYTTÖ: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Lippu (pitkä) | Merkitys
  -------------------------|-----------------------------------------
  --execute | Oikeat liikkeet (oletus on vain testiajo).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | UTF-8 jatkotiedosto B64|:llä rivit.
  --delete-duplicates | Poista päällekkäiset ehdokkaat (vaatii --confirm-delete ja --execute).
  --delete-issues | Poista ongelma-alueehdokkaat (vaatii --confirm-delete ja --execute). Ei etäautomaatiokohteissa.
  --archive-after-organize | Järjestämisen jälkeen: tiedostokohtainen sisarus-ZP ja poista sitten alkuperäiset (tarvitaan --confirm-delete ja --execute). Ohittaa jo arkistoidut laajennukset.

  **Huomaa:** CLI `--mode models` valitsee **CAD/3D-mallit**, ei tekoälyn esineitä. Käytä `--mode ai` tai `--mode models-ai` AI / ML.

  Esimerkki (koeajo, kaikki luokat): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Esimerkki (vain siirrot Unique-kansioon, suorita): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Koonti: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Testiajo: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  Jos kyseessä on --execute, irrota :ro lähdetelineestä. Katso containers/README.md usean workerin säännöt (yksi lähtöjuuri workeria kohti).

Kubernetes (viitetyö)
  Vain luku -lähde PVC:t ovat voimassa testiajotöissä. Oikeat liikkeet --execute:n kanssa tarvitsevat kirjoitettavan lähteen PVC:t. Anna voimassa oleva myymälän tai julkaisijan käyttöoikeus kaikille järjestämis-/korjausajoille (testiajo ja suoritus). Yksi Pod per tulospuu. Vähimmäismalli on dokumentoitu containers/README.md:ssä malliluettelon rinnalla.

Töiden edistyminen
  Työt-ikkuna näyttää edistymisen App-, CLI-, Docker- ja Kubernetes-ajoille. Vaiheet, joiden kokonaismäärä tunnetaan, näyttävät prosenttiluvun. Ilman kokonaismäärää tehdyt haut pysyvät määrittämättöminä.
  Automaatio käynnistää CLI-työprosessin asetuksella ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 ja poistaa nuo merkkirivit näkyvästä lokista. Käsin käynnistetty CLI-ajo ei lähetä merkkejä, ellei kyseistä muuttujaa ole asetettu.
  Docker- ja Kubernetes-työprosessit saavat saman muuttujan, joten myös ne ajot ilmoittavat prosenttiluvun. Luku luetaan työprosessin lokista, joten se näkyy heti, kun kontti tai podi alkaa kirjoittaa.
  --list-running ja --show-run sisältävät edistymiskentät aktiivisille töille, kun ajo on ilmoittanut jotain.

# Suoritusesimerkit

## Graafinen käyttöliittymä

Lisää **Lähteet** ja tuloskansio, valitse suoritustila, kytke **Testiajo** päälle esikatselua varten ja paina sitten **Suorita**. Jätä **Testiajo** pois päältä todellisia siirtoja varten. Poistovalinnat pyytävät vahvistuksen ennen suoritusta.

## CLI-esimerkit

CLI Testiajo: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
