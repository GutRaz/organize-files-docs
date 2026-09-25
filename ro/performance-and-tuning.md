# Avansat / Diagnostic

## Reglaje organizare

Avansat / Diagnostic expune opțiuni **OrganizeFilesEngine** fără a aglomera panoul principal.

Organizarea reglează dedupe, index destinație, an Unice, fire mutare/enumerare, BFS suplimentar, resume și rădăcini Unice extra.

Repararea păstrează doar reîncercări rețea/disc, lane-uri hardware grafic pentru verificare video completă, buffer hash și heartbeat JSON. Câmpurile dezactivate sunt doar orientare.

Pe NAS/UNC: limitează paralelismul, păstrează reîncercarea rețea, lasă BFS suplimentar pornit și încearcă buffer 8 MiB la hash lent.

# Avansat / Diagnostic — fiecare opțiune

## Despre acest capitol

Aceste controale sunt opțiuni ale motorului. Desktop (Windows, macOS, Linux), Android, iOS și instrumentul din linia de comandă citesc aceleași valori.

La **Organizare** se folosesc toate opțiunile de mai jos, exceptând câmpurile dezactivate de UI. **Repararea** folosește doar reîncercarea rețea, reîncercarea disc plin, lane-uri hardware grafic detectate (cu verificare video completă), buffer hash, heartbeat JSON, **Fișier de reluare (resume)** și **De la zero (golește fișierul de reluare)**. Restul rămân vizibile dar sunt ignorate la reparare.

## Surse rețea (NAS / UNC)

Când **Surse** sau **Destinație** sunt pe share SMB/CIFS, NAS sau disc mapat, merită revizuită atent această secțiune.

- **De ce reglezi** — Fire la maxim pot bloca un filer, deși merg pe SSD local.
- **Ce încearcă** — Reîncercare rețea activă. Fire mutare și max. Enumerare mai mici la timeout. BFS suplimentar pornit decât dacă ai verificat enumerarea completă fără el. Buffer 8 MiB la hash lent pe rețea.
- **Fără așteptare rețea** — Eșec rapid la erori tranzitorii. Riscant pe Wi-Fi sau share aglomerat.

## Mod deduplicare

Cum decide motorul că două fișiere sunt duplicate.

| Mod | Ce face | Când | Compromis |
| --- | ------- | ---- | --------- |
| **Hash (SHA-256)** | Citește și hash-uiește integral fiecare fișier sursă inclus, apoi grupează conținutul identic. | Cel mai puternic mod practic. Hash (SHA-256) este obligatoriu pentru ștergerea la sursă (duplicate și fișiere problematice). | Cel mai lent pe arbori mari sau NAS. Niciun algoritm nu trebuie prezentat ca garanție absolută. |
| **Mărime + timp + nume** | Cheie = mărime, ticks UTC, nume mic, apoi verificare SHA-256 integrală. | Mod conservator de compatibilitate pentru layout media vechi. | Poate rata duplicate redenumite. Nu se folosește cu ștergerea duplicatelor sau a fișierelor problematice. |
| **Fără** | Fără dedupe între fișiere. | Doar sortare. | Duplicatele rămân în surse. |

## Sari indexul destinației

- **Oprit (implicit)** — Scanează **Unice** existente înainte de hash. Mai sigur la aceeași destinație refolosită.
- **Pornit** — Sare scanarea.
- **Beneficiu** — Mai rapid pe ieșiri foarte mari.
- **Risc** — Mai mult conținut duplicat în **Unice**.

## An minim în Unice

An calendaristic minim pentru foldere dată sub **Unice** (layout media).

**De ce** — Evită ani ciudați când metadatele sunt greșite.

## Fire mutări

Mutări paralele după rezervarea destinațiilor.

- **Mai multe** — Rapid pe SSD local.
- **Mai puține** — Mai sigur pe NAS, USB, Wi-Fi.

## Fire clasificare și hash

Lucrători paraleli la scanarea surselor și dedupe SHA-256.

- **Fire clasificare** — Descoperire și clasificare fișiere. CLI: `--classify-threads <n>`.
- **Fire hash** — Lucrători la hash conținut. CLI: `--hash-threads <n>`.
- **Suprascrieri** — Valorile manuale au prioritate față de profilul de organizare (`--profile`).

## Enumerare paralelă maximă

Plafon listare directoare în paralel.

- **0** = automat motor.
- **Mai mic** — Mai puțină presiune SMB.

## Parcurgere suplimentară BFS

- **Pornit (implicit)** — Pas BFS suplimentar la listare.
- **De ce** — Unele NAS par incomplete la prima trecere.
- **Oprit** — Doar după verificare că enumerarea e completă fără el.
- **CLI** — `--no-bfs` dezactivează acest pas.

## Fișier reluare (resume)

Cale UTF-8 opțională. Mutările reușite adaugă linii `B64|`.

- **De ce** — Continuă joburi lungi după oprire.
- **Cale implicită** — Când câmpul e gol la rulare, motorul folosește `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt`. Fără **Destinație**, folosește `sessions\<id>\resume\OrganizeFiles.resume.txt` în profilul aplicației.
- **UI desktop** — Listă doar citire pentru selecție și copiere cu mouse-ul. Când există deja un fișier resume la locația implicită, calea apare automat. **Alege** selectează folderul de log și adaugă `OrganizeFiles.resume.txt`. **Elimină** golește calea. Când e gol, hint-ul arată calea folosită la rulare.

## De la zero

Trunchiază fișierul resume la începutul unei **rulări reale** de organizare (simularea nu trunchiază). Cu **Salvează progres și spațiul de lucru**, șterge și snapshot-ul UI la start.

**De ce** — Numărătoare curată, fără resume vechi.

## Rădăcini extra Unice

Câte un folder pe linie: arbori **Unice** suplimentari de indexat.

- **De ce** — Dedupe vede fișiere deja organizate pe alt volum.
- **UI desktop** — Listă doar citire pentru copiere pe linie. **Adaugă** adaugă un folder ales. **Elimină** șterge linia selectată (de ex. un arbore vechi `Uniques` pe NAS).

## Reîncercare rețea (s) / Fără așteptare rețea

Secunde pentru erori I/O tranzitorii.

- **De ce** — SMB taie sesiuni idle. Folosit la organizare și reparare.
- **Fără așteptare rețea** — Oprește așteptarea și eșuează imediat.

## Reîncercare disc plin (s) / Fără așteptare disc plin

Același model când destinația rămâne fără spațiu.

**De ce** — Timp să eliberezi disc în rulări lungi.

## Lane-uri hardware grafic

Doar când **verificarea video completă** (integrată) este activă și **Folosește plăcile video detectate** e activ. O valoare peste **0** setează numărul explicit de lane-uri pentru paralelism la validare pe vendorii detectați (NVIDIA, AMD, Intel, Apple, mobile). **0** înseamnă detectare automată a lane-urilor hibride. Nu înseamnă CPU-only. Pentru eșantionare exclusiv CPU selectează **Doar CPU** la placa video. Tag-urile de bandă planifică validarea bitstream pe CPU. Nu invocă decode video hardware la OS.



- **Preset CLI** — `--hwaccel <value>` selectează un preset de bandă de validare (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`) când rulează verificarea video completă.

## Buffer citire hash

Buffer per worker la hash (512 KiB, 1 MiB, 8 MiB).

**De ce** — Buffere mari ajută NAS lent.

## Jurnal undo

Jurnal JSONL opt-in al mutărilor sub rădăcina de ieșire pentru rulare.

- **De ce** — Permite reluarea undo din CLI după o organizare reală.
- **Arhivare** — Arhivarea post-organizare rămâne oprită cât timp jurnalul undo e activ.
- **CLI** — `--record-undo-journal` (ca bifarea din Main).

## Scrie heartbeat JSON

Scrie opțional `Organize.Files.run.json` sub `Output\_OrganizeMediaLogs`.

- **De ce** — Monitorizare externă a progresului live.
- **Ritm** — La 10.000 fișiere parcurse, la 5.000 potriviri și la circa 15 secunde în scanarea surselor, după fiecare 1.000 de fișiere și cel mult o dată la 5 secunde la validare, hashing și mutări, și la fiecare fază majoră.
