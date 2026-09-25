# Felügyelet Prometheus és Grafana eszközzel

## Mit fednek le a számlálók

Az ütemezett munkák kis készlet Prometheus-számlálót és -mérőt vezetnek. Minden név így kezdődik: `organize_files_automation_`, és az egész készlet Prometheus-szövegként jelenik meg. Mindhárom gazda, amely munkákat futtat, ugyanazt a készletet teszi közzé: az asztali alkalmazás, az `OrganizeFiles.JobAgent` szolgáltatás és a konténerekben használt parancssori gazda.

A számlálók az ütemezőt írják le, nem a fájlokat. Az átfutások, a munkák kimenetele, a jóváhagyások, a webhook-kézbesítés és az előzmények karbantartása számít bele. A munka által mozgatott fájlokról semmi sem kerül bele.

## Kiírás fájlba, nyitott port nélkül

Az `automation-metrics.prom` az automatizálás adatmappájába kerül, az `automation-jobs.json` mellé, és minden esedékes átfutás után, valamint minden leolvasáskor frissül. A formátum az, amelyet a `node_exporter` textfile-gyűjtője olvas, így az a gép, amelyen a `node_exporter` már fut, figyelő port, token és tűzfalszabály nélkül is lefedett. A fájl cseréje atomi, és a helyén hagyott jelképes hivatkozás megállítja az írást ahelyett, hogy követné.

## Leolvasási végpont

A végpont csak akkor létezik, ha az `ORGANIZE_FILES_METRICS_HTTP_PORT` 1 és 65535 közötti portot tartalmaz. E változó nélkül semmi sem figyel.

| Változó | Hatás |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | A figyelt port. Ha hiányzik vagy a tartományon kívül esik, végpont egyáltalán nincs. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Figyelési cím. Az alapérték `127.0.0.1`. A `0.0.0.0`, `+` és `*` értékek minden címet jelentenek, minden más visszaáll erre: `127.0.0.1`. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | A `/metrics` és a `/ready` útvonalon megkövetelt bearer token. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | Az `1` engedi, hogy a `/ready` e token nélkül válaszoljon, fürtszondák kedvéért. A gazda útvonalai ilyenkor kimaradnak a válaszból. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | Vesszővel elválasztott kilépési kódok, amelyekre a `/ready` nem készet jelent. Felváltja a beépített listát. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | Az `1` figyelmen kívül hagyja az utolsó átfutás kilépési kódját, és az első átfutás befejezése előtti állapotot is. |
| `ORGANIZE_FILES_READY_JSON` | Az `1` kikényszeríti a JSON-választ a `/ready` útvonalon, annak a hívónak is, aki sima szöveget kért. |

A visszacsatolási címen kívüli cím elutasításra kerül a figyelő megnyitása előtt, ha nincs beállítva bearer token. Az elutasítás a hibakimenetre kerül, és webhook-eseményként is elmegy, mert ez a párosítás az egész hálózatnak adná a számlálókat.

## Kiszolgált útvonalak

- `/metrics` — a számlálók Prometheus-szövegként. A `/` útvonalra érkező kérés ugyanazt a tartalmat adja.
- `/ready` — készenlét egy vezénylő számára. A válasz `200`, amint az automatizálás mappája elfogad egy próbaírást, a munkafájl megnyílik, az előzménymappa az adatgyökéren belülre oldódik fel, és az utolsó esedékes átfutás olyan kilépési kóddal zárult, amely nem gátol. Egyébként a válasz `503` és egy rövid ok, például `due_pass_not_completed` vagy `last_due_pass_license_failed`.
- `/health` — csak életjel. Ez az útvonal beállított token mellett is névtelen marad, mert `ok` a válasza és semmi más.

A `3` kilépési kód licenchibára, a `8` zárolt kimeneti fára, a `10` soha meg nem erősített törlésre és a `11` igénylési ütközésre alapértelmezés szerint gátolja a készenlétet. A `/ready` törzse JSON, hacsak a hívó nem küld `Accept: text/plain` fejlécet vagy nem fűzi hozzá ezt: `?format=text`.

## A számlálók

| Név | Tartalom |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Az ütemező által megkezdett esedékes átfutások. |
| `organize_files_automation_jobs_started_total` | Munkafuttatások, amelyek elérték a futó állapotot. |
| `organize_files_automation_jobs_skipped_total` | Kihagyott munkák: nem kész Docker- vagy Kubernetes-környezet, alkalmazásra irányuló munka képernyő nélküli gazdán, foglalt kimeneti gyökér, vagy a vezénylő által elutasított munka. |
| `organize_files_automation_jobs_failed_total` | Hibával zárult munkafuttatások. |
| `organize_files_automation_jobs_awaiting_approval_total` | Jóváhagyásra félretett valódi futtatások. |
| `organize_files_automation_execute_approvals_total` | Valódi futtatásra megadott jóváhagyások. |
| `organize_files_automation_execute_approvals_expired_total` | Jóváhagyások, amelyek határideje használat előtt lejárt. |
| `organize_files_automation_claim_conflicts_total` | Esetek, amikor egy másik gazda már birtokolta a kimeneti gyökér igénylését. |
| `organize_files_automation_runs_orphaned_total` | Árvaként helyreállított futtatások, amelyeket egy leállt gazda hagyott hátra. |
| `organize_files_automation_job_events_total` | Eseményenként egy számláló, `event`, `job_id`, `target` és `jobs_file` címkékkel. |
| `organize_files_automation_webhook_posts_succeeded_total` | Elfogadott webhook-kézbesítések. |
| `organize_files_automation_webhook_posts_failed_total` | Elutasított vagy elérhetetlen webhook-kézbesítések. |
| `organize_files_automation_webhook_dead_letter_depth` | Sorok, amelyek épp most várakoznak a kézbesítetlen webhookok fájljában. |
| `organize_files_automation_log_retention_pruned_total` | A megőrzés által eltávolított futtatási naplók. |
| `organize_files_automation_runs_index_compacted_total` | Tömörítéskor a futtatási mutatóból kivett sorok. |
| `organize_files_automation_last_due_pass_exit_code` | A legutóbb befejezett átfutás kilépési kódja. A `0` tiszta átfutást jelent. |
| `organize_files_automation_last_due_pass_completed_utc` | A legutóbb befejezett átfutás Unix-ideje másodpercben, az első előtt pedig `0`. |

## Műszerfal és riasztási szabályok

Kész Grafana-műszerfal jelenik meg a telepítési fájlokkal `grafana-organize-files-automation.json` néven, **OrganizeFiles Automation** címmel. Tíz panelje az esedékes átfutásokat, az elindított és meghiúsult munkákat, az igénylési ütközéseket, a munkák egy órára vetített átbocsátását, az utolsó kilépési kódot, a kézbesítetlen üzenetek mélységét, a napi webhook-hibákat, a jóváhagyásra váró munkákat és a munkaeseményeket állapot szerint mutatja. Minden panel a `${DS_PROMETHEUS}` helyőrzővel nevezi meg az adatforrását.

A hozzájuk tartozó riasztási szabályok az `alerts-organize-files-automation.yaml`, a `prometheus-rule-automation.yaml` pedig a Kubernetes-burok a `kube-prometheus-stack` számára. A nem nulla utolsó kilépési kód öt perc után figyelmeztet, a licenchiba egy perc után kritikus, a többi szabály pedig a meghiúsult munkákat, az igénylési ütközéseket, a webhook-hibákat, a kézbesítetlen üzenetek torlódását és az egy napja várakozó jóváhagyásokat fedi le. Mindkét fájlt minden fordításkor ellenőrzik, így a fenti nevek lépést tartanak a számlálókkal.

# Futtatás kimenete és metrikák

## Állapot sor

A **Futtatás kimenete** területen a következők láthatók:

- Az alkalmazás aktuális állapota és a motor előrehaladása.
- **CPU** és két **memória** érték csak ehhez a folyamathoz.
- **GPU**-sorok, Windowson: ennek a folyamatnak a részesedése az egyes grafikus kártyákból, nem a teljes kártya.

Ugyanazt a kompakt erőforrássávot használja újra a másodlagos eszközablakok, például a fájlfeltárás, az ütemezett feladatok és a fájljavítás.

## Memóriacímkék

- **Privát bájtok / véglegesítés** – a folyamat által lefoglalt privát virtuális memória.
- **Munkakészlet / memória** – a folyamat által jelenleg tárolt rezidens RAM. Eltérhet egy másik operációs rendszer-monitortól, mivel minden operációs rendszer és asztali környezet címkéje eltérően dolgozza fel a memóriát.

## Heartbeat JSON futtatása (opcionális)

Engedélyezze a **Write run heartbeat JSON** beállítást a **Speciális / Diagnosztika** részben. A motor ezt az `Organize.Files.run.json` fájlba írja ki az `Output\_OrganizeMediaLogs` alatt (ugyanaz a mappa, mint az alapértelmezett szervezési folytatási fájl).

- **Útvonal** – atomszerűen frissítve a rendszerezési és javítási futások során.
- **Időzítés** — a források átvizsgálása közben a fájl minden 10 000 látott fájlnál, minden 5000 találatnál és körülbelül 15 másodpercenként újraíródik, amíg a vizsgálat tart, így egy lassan listázódó nagy hálózati fa is mutatja, hogy a futás él. Az ellenőrzés, a hasítás és az áthelyezések alatt minden 1000 fájl után íródik újra, legfeljebb 5 másodpercenként. A futás elején és végén az írás továbbra is megtörténik.
- **Haladás** — amíg a fájlszámok még nőnek, a fő haladásjelző az eddig látott fájlokat mutatja 100% helyett, addig, amíg egy szakasznak ismertté nem válik a végösszege.
- **Mezők** — `schema`, `mode`, `phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`), `runState`(`active`/`completed`/`failed`/`cancelled`), `utc` (ISO-8601), `dryRun`, `outputRoot`, `validateMedia`, `deepVideoValidate`, `gpuDeviceCount`, `hwaccel`, nem kötelező `correlationId`, beágyazott `progress` számlálók.
- **Log** — a futás kimeneti panelje a teljes elérési utat kinyomtatja az elején és a fájl mentésekor a végén. Használja a **Szívverésnapló-mappa megnyitása** / **Show heartbeat JSON-fájl** lehetőséget a Speciális / Diagnosztika részben.
- **CLI** — `--heartbeat-json` be OrganizeFiles.Cli. Mégse és végzetes shell-hibák esetén írja be a `cancelled`/`failed` `runState` értéket, amikor engedélyezve van.
