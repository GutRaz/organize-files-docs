# Haladó / Diagnosztika

## Hangolás megszervezése

A Haladó / Diagnosztika az **OrganizeFilesEngine** opciókat teszi elérhetővé anélkül, hogy a fő panelt összezavarná.

A rendezési módok behangolhatják a dedupe-ot, a célindexet, az egyedi dátumszabályokat, az áthelyezési és felsorolási szálakat, a BFS kiegészítést, a folytatási fájlt és az extra egyedi gyökereket.

A javítás csak a hálózat és a lemez megtelt újrapróbálkozási időzítését, az észlelt grafikus hardversávokat az opcionális teljes videoellenőrzéshez, a hash olvasási puffert és a JSON szívverését tartja meg. Más mezők láthatók a környezet számára, de le vannak tiltva.

Ha a források vagy a kimenet éles a NAS vagy UNC útvonalakon, csökkentse a párhuzamosságot, hagyja engedélyezve a hálózati újrapróbálkozást, hagyja bekapcsolva a BFS kiegészítést a páratlan SMB-fák számára, és próbálja ki a 8 MiB-os hash puffert, ha a kivonatolás lassú.

# Speciális / Diagnosztika – mindegyik opció

## Erről a fejezetről

Ezek a vezérlők a motor beállításai. Az asztali alkalmazás (Windows, macOS, Linux), az Android, az iOS és a parancssori eszköz ugyanazokat az értékeket olvassa.

A **Rendezés** módok minden alábbi vezérlőt használnak, kivéve ha a kezelőfelület kiszürkíti őket. A **Javítás** csak a hálózati újrapróbálkozást, a lemez megtelése miatti újrapróbálkozást, az észlelt grafikus hardversávokat (teljes videóellenőrzéssel), a hash olvasási puffert, a szívverés-JSON-t, **Folytatási állapotfájl** és **Kezdje újra (a folytatási fájl csonkolása)** használja. A többi mező látható marad, de a javítás során figyelmen kívül marad.

## Hálózati források (NAS / UNC)

Ha a források vagy a kimenetek a SMB/CIFS megosztásokon, NAS köteteken vagy leképezett meghajtókon vannak, figyelmesen olvassa el ezt a részt.

- **Miért érdemes hangolni** — A helyi SSD-n működő szálszámok leállíthatják vagy túlterhelhetik a fájlt.
- **Mit érdemes kipróbálni** — A hálózati újrapróbálkozást tartsa bekapcsolva. Alsó mozgási szálak és enum párhuzamos max az időtúllépéseknél. Hagyja bekapcsolva a BFS kiegészítést, hacsak nem ellenőrizték a teljes számot anélkül. Próbálja ki a 8 MiB-os hash puffert, ha a kivonatolás lassú a hálózaton.
- **Hálózati várakozás letiltása** — Gyorsan meghiúsul átmeneti hálózati hibák esetén. Kockázatos Wi-Fi-n vagy elfoglalt megosztásokon.

## Dedupe mód

Hogyan dönt a motor úgy, hogy két fájl duplikált.

| mód | Mit csinál | Mikor kell használni | Kompromisszum |
| ---- | ------------ | ----------- | --------- |
| **Hash (SHA-256)** | Minden mellékelt forrásfájl teljes tartalmát beolvassa és kivonatolja, majd azonos bájtokat csoportosít. | A legerősebb gyakorlati mód. Hash (SHA-256) kötelező a forráshelyi törléshez (másolatok és problémás fájlok). | Leglassabb nagy fákon vagy NAS. Semmilyen algoritmust nem szabad abszolút garanciaként bemutatni. |
| **Méret + idő + név** | Kulcs = méret, UTC utolsó írásjelek, kisbetűs név, majd teljes SHA-256 ellenőrzés. | Konzervatív kompatibilitási mód régebbi médiamappa-elrendezésekhez. | Hiányozhatnak az átnevezett ismétlődések. Soha ne használja a másolatok vagy a problémás fájlok törlésével. |
| **Nincs** | Nincs keresztfájl-visszaállítás. | Csak rendezés, nem ismétlődő tisztítás. | A másolatok a forrásokban maradnak. |

## Célindex átugrása

- **Ki (alapértelmezett)** — A meglévő **Egyedi** kimenet vizsgálata és indexelése a kivonatolás előtt. Biztonságosabb, ha ugyanazt a kimeneti mappát használja.
- **Be** – Kihagyja a keresést.
- **Előny** — Gyorsabb a hatalmas kimeneti fákon.
- **Kockázat** – Több ismétlődő tartalom kerülhet az Unique-ba.

## Egyediek min. év

Minimális naptári év a dátummappákhoz az **Egyedi** alatt a médiaelrendezésekben. **Miért** – Megakadályozza, hogy a nagyon régi fájlok páratlan évjáratú mappákba szórjanak, ha a metaadatok hibásak.

## Szálak áthelyezése

Párhuzamos fájlmozgatás a célhelyek lefoglalása után.

- **Magasabb** – Gyorsabb a helyi SSD-n.
- **Alsóbb** – Biztonságosabb a NAS, USB- vagy Wi-Fi-leképezett meghajtókon.

## Osztályozó és hash szálak

Párhuzamos munkaszálak a forrás vizsgálata és a SHA-256 deduplikáció során.

- **Osztályozási szálak** — Fájlok felderítése és osztályozása. CLI: `--classify-threads <n>`.
- **Hash szálak** — Tartalom hash-elő munkaszálak. CLI: `--hash-threads <n>`.
- **Felülbírálások** — A kézi értékek felülírják a profil alapértelmezéseit (`--profile`).

## Enum párhuzamos max

Limit a párhuzamos könyvtárak listázásához a vizsgálat során.

- **0** = automatikus motor.
- **Alsó** – Kevesebb nyomás nehezedik az SMB-re, ha egyszerre több mappa jelenik meg.

## Kiegészítés BFS címtárjegy

- **Be (alapértelmezett)** — Egy további sekély, szélességi bejárás.
- **Miért** — Egyes NAS-útvonalak vagy mély fák az első bejárás után hiányosnak látszanak.
- **Ki** — Csak azután, hogy nélküle is teljes fájlszámot igazoltunk.
- **CLI** — A `--no-bfs` kikapcsolja ezt a bejárást.

## Folytatási állapotfájl Opcionális

UTF-8 elérési út. A sikeres lépések hozzáfűzik a `B64|` sorokat, így a következő rendezési futás kihagyhatja a kész forrásokat.

- **Miért** — Folytassa a hosszú munkát leállás vagy összeomlás után.
- **Alapértelmezett elérési út** — Ha a mező üres a futási időben, a motor a `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt` értéket használja. Kimenet nélkül a `sessions\<id>\resume\OrganizeFiles.resume.txt` értéket használja az alkalmazásprofil alatt.
- **Asztali felhasználói felület** – Csak olvasható útvonallista az egér kiválasztásához és másolásához. Ha az alapértelmezett helyen már létezik folytatási fájl, az elérési út automatikusan megjelenik. A **Tallózás** kiválaszt egy naplómappát, és hozzáfűzi a `OrganizeFiles.resume.txt` értéket. **Eltávolítás** törli az elérési utat. Ha üres, a tipp a futási időben használt útvonalat mutatja.

## Indítás frissen

Levágja a folytatási fájlt, amikor egy **igazi** szervezési futás indul (a próbafuttatás nem csonkol). A **Felhaladás és munkaterület mentése** funkcióval a futás indításakor a mentett felhasználói felület pillanatképet is törli. **Miért** — Teljes újraszámlálás kényszerítése a régi folytatási napló folytatása helyett.

## Extra egyedi vizsgálati

Soronként egy mappa: további indexelendő **Unique** fák (régi elrendezés, másik kötet).

- **Miért** — A duplikátumszűrés látja a máshol már rendezett fájlokat anélkül, hogy újra áthelyezné őket.
- **Asztali felület** — Csak olvasható lista, soronkénti másoláshoz. A **Hozzáadás** egy kiválasztott mappát fűz hozzá. Az **Eltávolítás** törli a kijelölt sort (például egy régi `Uniques` fát a NAS-on).

## Hálózati újrapróbálkozás (másodpercben) /

Hány másodpercig próbálkozzon újra az átmeneti hálózati be- és kimenettel.

- **Miért** — Az SMB-kiszolgálók elejtik a tétlen munkameneteket. A rendezés és a javítás is használja.
- **Hálózati várakozás kikapcsolása** — Ne várjon tovább, hanem hibázzon.

## Lemez megtelt újrapróbálkozás

(másodperc) / Lemez megtelt várakozás letiltása

Ugyanaz a minta, amikor a kimeneti köteten elfogy a hely. **Miért** — A lemez felszabadításának ideje hosszú futás közben.

## A videokártya sávjai

Csak akkor, ha a beépített **teljes videoellenőrzés** be van kapcsolva, és a **Talált videokártya használata** is. A **0**-nál nagyobb érték rögzített sávszámot szab az egyidejű ellenőrzésre a megtalált gyártók között (NVIDIA, AMD, Intel, Apple, mobil). A **0** azt jelenti, hogy a sávszám magától áll be. Nem azt jelenti, hogy csak a processzor. Ha csak a processzoron akar mintát venni, válassza a videokártyák listájából a **Csak processzor** lehetőséget. A sávcímkék a processzoron végzett bitfolyam-ellenőrzést tervezik meg. Nem hívják meg a rendszer hardveres videodekódolását.

- **Parancssori előbeállítás** — A `--hwaccel <value>` az ellenőrzősávok előbeállítását választja ki (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`), amikor a teljes videoellenőrzés fut.

## Kivonatolvasó puffer

Dolgozónkénti olvasási puffer kivonatolás közben (512 KiB, 1 MiB, 8 MiB). **Miért** – A nagyobb pufferek segítenek, ha a NAS vagy a magas késleltetésű megosztás lassan válaszol.

## Visszavonási napló rögzítése

Választható JSONL napló az áthelyezésekről a futtatás kimeneti gyökere alatt.

- **Miért** — Lehetővé teszi a visszavonást a CLI-ből egy valódi futtatás után.
- **Archívum** — A rendezés utáni archiválás kikapcsolva marad, amíg a napló aktív.
- **CLI** — `--record-undo-journal` (ugyanaz, mint a főablak jelölőnégyzete).

## Futás közbeni JSON írása

Kiírja a nem kötelező `Organize.Files.run.json` fájlt az `Output\_OrganizeMediaLogs` alá.

- **Miért** — Külső eszközök rendezés vagy javítás közben is olvashatják az élő számlálókat (átvizsgált, tervezett, kész).
- **Időzítés** — Minden 10 000 látott fájlnál, minden 5000 találatnál és körülbelül 15 másodpercenként a forrásátvizsgálás alatt, minden 1000 fájl után és legfeljebb 5 másodpercenként az ellenőrzés, a hasítás és az áthelyezések alatt, és minden nagyobb szakasznál.
