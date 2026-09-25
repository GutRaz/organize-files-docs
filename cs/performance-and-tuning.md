# Pokročilé / Diagnostika

## Uspořádejte laděná

Pokročilé / Diagnostika odhaluje možnosti **OrganizeFilesEngine**, aniž by zaplňoval hlavní panel.

Režimy organizace mohou vyladit dedupe, cílový index, jedinečná pravidla pro datum, přesun a výčet vláken, doplněk BFS, soubor obnovení a další jedinečné kořeny.

Oprava zachovává pouze časováná opakování zaplněná sítě a plného disku, detekované pruhy grafického hardwaru pro volitelnou úplnou kontrolu videa, vyrovnávací paměť pro čtení hash a tep JSON. Ostatní pole jsou pro kontext viditelná, ale vypnutá.

Když zdroje nebo výstup žijí na cestách NAS nebo UNC, snižte paralelismus, ponechte zapnuté opakování sítě, nechte doplněk BFS zapnutý pro liché SMB stromy a vyzkoušejte 8 MiB hash buffer, pokud je hašování pomalé.

# Pokročilé / Diagnostika — každá možnost

## O této kapitole

Tyto ovládací prvky jsou možnosti jádra. Desktop (Windows, macOS, Linux), Android, iOS a nástroj příkazového řádku čtou stejné hodnoty.

Režimy **Uspořádat** používají všechny níže uvedené ovládací prvky, pokud je uživatelské rozhraní nezašedne. **Oprava** používá pouze opakování při síťové chybě, opakování při zaplněném disku, zjištěné pruhy grafického hardwaru (s úplnou kontrolou videa), vyrovnávací paměť pro čtení hashe, heartbeat JSON, **Soubor stavu obnovení** a **Začít znovu (zkrátit soubor obnovení)**. Ostatní pole zůstanou viditelná, ale během opravy se ignorují.

## Síťové zdroje (NAS / UNC)

Pokud jsou zdroje nebo výstup na sdílených položkách SMB/CIFS, svazcích NAS nebo namapovaných jednotkách, pečlivě si prostudujte tuto část.

- **Proč ladit** – Počty vláken, které fungují na místním SSD, se mohou zastavit nebo přetážit filer.
- **Co zkusit** — Nechte síť opakovat. Snižte přesouvání vláken a vyjmenujte paralelní maximální časové limity. Ponechejte doplněk BFS zapnutý, pokud nebyl úplný počet ověřen bez něj. Vyzkoušejte 8 MiB hash buffer, když je hašování v síti pomalé.
- **Zakázat čekání sítě** — Rychlé selhání při přechodných chybách sítě. Rizikové na Wi-Fi nebo zaneprázdněných sdílených položkách.

## Režim dedupe

Jak engine rozhodne, že dva soubory jsou duplicitní.

| Režim | Co to dělá | Kdy použít | Kompromis |
| ---- | ------------ | ----------- | --------- |
| **Hash (SHA-256)** | Čte a hashuje celý obsah každého zahrnutého zdrojového souboru a poté seskupuje identické bajty. | Nejsilnější praktický režim. Hash (SHA-256) je nutný pro mazání na zdroji (duplikáty a problematické soubory). | Nejpomalejšá na velkých stromech nebo NAS. Žádný algoritmus by neměl být prezentován jako absolutní záruka. |
| **Velikost + čas + jméno** | Klíč = velikost, zaškrtnutí posledního zápisu UTC, název s malými písmeny, poté úplné ověření SHA-256. | Režim konzervativní kompatibility pro starší rozložení složek médií. | Může přehlédnout přejmenované duplikáty. Nikdy nepoužívejte s mazáním duplikátů ani problematických souborů. |
| **Žádné** | Žádné odstranění duplicit mezi soubory. | Pouze třídění, nikoli duplicitní čištění. | Duplikáty zůstávají ve zdrojách. |

## Přeskočit cílový index

- **Vypnuto (výchozí)** — Prohledá stávající **Unikátní** výstup a před hašováním jej indexuje. Bezpečnější při opětovném použití stejné výstupní složky.
- **Zapnuto** – Přeskočí toto skenování.
- **Výhoda** — Rychlejší na velkých výstupních stromech.
- **Riziko** – V Unique může přistát více duplicitního obsahu.

## Min. rok pro Jedinecne

Minimální kalendářní rok pro datové složky pod **Unikátní** v rozložení médií. **Proč** — Zabraňuje rozptýlená velmi starých souborů do složek s lichým rokem, když jsou metadata nesprávná.

## Přesunout vlákna

Paralelní soubor se přesune po rezervaci cílů.

- **Vyššá** — Rychlejší na místním SSD.
- **Nižší** — Bezpečnější na discích mapovaných NAS, USB nebo Wi-Fi.

## Vlákna klasifikace a hashování

Paralelní pracovníci během skenování zdrojů a deduplikace SHA-256.

- **Klasifikační vlákna** — Vyhledávání a klasifikace souborů. CLI: `--classify-threads <n>`.
- **Hash vlákna** — Pracovníci hashování obsahu. CLI: `--hash-threads <n>`.
- **Přepsání** — Ruční hodnoty přepíší výchozí hodnoty profilu (`--profile`).

## Enum paralelní max

Limit pro paralelní výpis adresářů během skenování.

- **0** = automatický motor.
- **Nižší** — Menší tlak na SMB, když je seznam více složek najednou.

## Dodatek BFS adresářový průchod

- **Zapnuto (výchozí)** — Další mělký průchod do šířky.
- **Proč** — Některé cesty na NAS nebo hluboké stromy vypadají po prvním průchodu neúplně.
- **Vypnuto** — Až po ověření úplného počtu souborů bez něj.
- **CLI** — `--no-bfs` tento průchod vypne.

## Soubor obnovení stavu

Volitelná cesta UTF-8. Úspěšné přesuny připojí řádky `B64|`, takže při příštím organizování může přeskočit hotové zdroje.

- **Proč** — Po zastavení nebo havárii pokračujte v dlouhých úlohách.
- **Výchozí cesta** — Když je pole za běhu prázdné, motor používá `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt`. Bez výstupu používá `sessions\<id>\resume\OrganizeFiles.resume.txt` pod profilem aplikace.
- **Uživatelské rozhraní pro stolní počítače** — Seznam cest pouze pro čtení pro výběr a kopírování myší. Když již soubor obnovení ve výchozím umístění existuje, cesta se zobrazí automaticky. **Procházet** vybere složku protokolu a připojí `OrganizeFiles.resume.txt`. **Odstranit** uvolní cestu. Když je prázdný, nápověda ukazuje cestu použitou v době běhu.

## Start fresh

Zkrátí soubor obnovení, když se spustí **skutečný** běh organizování (zkušební běh se nezkrátá). Pomocí **Uložit průběh a pracovní prostor** také vymaže uložený snímek uživatelského rozhraní při spuštění. **Proč** — Vynutit úplné přepočítání namísto pokračování ve starém protokolu soubor obnovení.

## Extra Unikátní kořeny skenování

Jedna složka na řádek: extra **Unikátní** stromy k indexování (starší rozvržení, jiný svazek).

- **Proč** — Dedupe může vidět soubory již uspořádané jinde, aniž by je znovu přesouval.
- **Uživatelské rozhraní pro stolní počítače** — Seznam pouze pro čtení pro kopii na řádek. **Přidat** přidá vybranou složku. **Odstranit** odstraní vybraný řádek (například starý strom `Uniques` na NAS).

## Opakování sítě (sekundy) / Zakázat čekání sítě

Sekundy na opakování přechodného síťového I/O.

- **Proč** – SMB filers zahazují nečinné relace. Používá se organizováním a opravami.
- **Zakázat čekání sítě** — Přestaňte čekat a místo toho selžte.

## Opakování plného disku

(sekundy) / Zakázat čekání plného disku

Stejný vzorec, když na výstupním svazku dojde místo. **Proč** — Čas na uvolnění disku při dlouhém běhu.

## Pruhy grafického hardwaru

Jen když je zapnutá vestavěná **úplná kontrola videa** a zároveň **Použít nalezený grafický hardware**. Hodnota nad **0** stanoví pevný počet pruhů pro souběžné ověřování napříč nalezenými výrobci (NVIDIA, AMD, Intel, Apple, mobilní). **0** znamená, že se počet pruhů zjistí sám. Neznamená to jen procesor. Pro vzorkování jen na procesoru zvolte v seznamu grafických karet **Pouze procesor**. Značky pruhů plánují ověřování bitového toku na procesoru. Nevolají hardwarové dekódování videa v systému.

- **Předvolba CLI** — `--hwaccel <value>` vybere předvolbu ověřovacích pruhů (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`), když běží úplná kontrola videa.

## Vyrovnávací paměť pro

čtení na pracovníka při hashování (512 KiB, 1 MiB, 8 MiB). **Proč** — Větší vyrovnávací paměti pomáhají zpomalit NAS a sdílení s vysokou latencí.

## Zaznamenat deník zpět

Volitelný deník JSONL přesunů pod kořenem výstupu pro daný běh.

- **Proč** — Umožňuje vrácení zpět z CLI po skutečném běhu.
- **Archiv** — Archivace po uspořádání zůstává vypnutá, dokud je deník aktivní.
- **CLI** — `--record-undo-journal` (stejné jako zaškrtávací políčko v hlavním okně).

## Zápis průběžného JSON o běhu

Zapisuje volitelný soubor `Organize.Files.run.json` do `Output\_OrganizeMediaLogs`.

- **Proč** — Vnější nástroje mohou během organizování či opravy číst živé čítače (prohledáno, naplánováno, dokončeno).
- **Načasování** — Po každých 10 000 spatřených souborech, po každých 5 000 shodách a zhruba každých 15 sekund při prohledávání zdrojů, po každých 1 000 souborech a nejvýše jednou za 5 sekund při ověřování, hashování a přesunech a při každé velké fázi.
