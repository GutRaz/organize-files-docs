# Ufuatiliaji kwa Prometheus na Grafana

## Vipimo hivi vinashughulikia nini

Kazi zilizoratibiwa hutunza seti ndogo ya vihesabio na vipimo vya Prometheus. Kila jina huanza na `organize_files_automation_`, na seti nzima huchapishwa kama maandishi ya Prometheus. Pangoni zote tatu zinazoendesha kazi huchapisha seti ile ile: programu ya eneo-kazi, huduma ya `OrganizeFiles.JobAgent`, na pango la mstari wa amri linalotumika ndani ya vyombo.

Vihesabio vinaeleza mratibu, si mafaili. Vinahesabu mizunguko, matokeo ya kazi, idhini, uwasilishaji wa webhook, na usafi wa historia. Hakuna kinachohesabiwa kuhusu mafaili ambayo kazi huyahamisha.

## Kuhamisha kwenye faili, bila kufungua mlango

`automation-metrics.prom` huandikwa katika folda ya data ya uendeshaji, kando ya `automation-jobs.json`, na huboreshwa baada ya kila mzunguko uliofika muda wake na kila usomaji. Muundo ni ule unaosomwa na mkusanyaji wa textfile wa `node_exporter`, hivyo mashine inayoendesha `node_exporter` tayari inafunikwa bila mlango unaosikiliza, bila tokeni, na bila sheria ya ngome. Faili hubadilishwa kwa hatua moja, na kiungo cha ishara kilichoachwa mahali pake husimamisha uandishi badala ya kufuatwa.

## Kituo cha usomaji

Kituo cha usomaji kipo tu wakati `ORGANIZE_FILES_METRICS_HTTP_PORT` ina mlango kati ya 1 na 65535. Bila kigezo hicho hakuna kinachosikiliza.

| Kigezo | Athari |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | Mlango wa kusikiliza. Ukikosekana au ukiwa nje ya upeo, hakuna kituo cha usomaji hata kimoja. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Anwani ya kusikiliza. Chaguo-msingi ni `127.0.0.1`. Thamani `0.0.0.0`, `+` na `*` zinamaanisha anwani zote, na kingine chochote hurudi kwa `127.0.0.1`. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | Tokeni ya bearer inayohitajika kwenye `/metrics` na kwenye `/ready`. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` huruhusu `/ready` kujibu bila tokeni hiyo, kwa ajili ya uchunguzi wa nguzo. Njia za pango huachwa nje ya jibu hilo. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | Misimbo ya kutoka iliyotenganishwa kwa koma inayofanya `/ready` kuripoti hakiko tayari. Hubadilisha orodha iliyojengwa ndani. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` hupuuza msimbo wa kutoka wa mzunguko wa mwisho, na pia hali ya kabla mzunguko wa kwanza haujakamilika. |
| `ORGANIZE_FILES_READY_JSON` | `1` hulazimisha jibu la JSON kwenye `/ready`, hata kwa mwitaji aliyeomba maandishi sahili. |

Anwani iliyo nje ya kitanzi cha ndani hukataliwa kabla msikilizaji haujafunguliwa, ikiwa hakuna tokeni ya bearer iliyowekwa. Kukataa huko huandikwa kwenye pato la makosa na hutumwa kama tukio la webhook, kwa sababu mchanganyiko huo ungetoa vihesabio kwa mtandao mzima.

## Njia zinazohudumiwa

- `/metrics` — vihesabio kama maandishi ya Prometheus. Ombi kwa `/` hurudisha maudhui yale yale.
- `/ready` — utayari kwa mratibu wa mfumo. Jibu ni `200` mara tu folda ya uendeshaji inapokubali uandishi wa majaribio, faili la kazi linapofunguka, folda ya historia inapotatuliwa ndani ya shina la data, na mzunguko wa mwisho uliofika muda wake ulipoishia kwa msimbo wa kutoka usiozuia. Vinginevyo jibu ni `503` pamoja na sababu fupi kama `due_pass_not_completed` au `last_due_pass_license_failed`.
- `/health` — ishara ya uhai tu. Njia hiyo hubaki bila utambulisho hata tokeni ikiwekwa, kwa sababu hujibu `ok` na si kingine.

Misimbo ya kutoka `3` kwa kasoro ya leseni, `8` kwa mti wa matokeo uliofungwa, `10` kwa ufutaji ambao haukuthibitishwa, na `11` kwa mgongano wa madai huzuia utayari kwa chaguo-msingi. Mwili wa `/ready` ni JSON isipokuwa mwitaji atume `Accept: text/plain` au aongeze `?format=text`.

## Vihesabio

| Jina | Maudhui |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Mizunguko iliyofika muda wake ambayo mratibu aliianzisha. |
| `organize_files_automation_jobs_started_total` | Utekelezaji wa kazi uliofikia hali ya kuendeshwa. |
| `organize_files_automation_jobs_skipped_total` | Kazi zilizorukwa: mazingira ya Docker au Kubernetes ambayo hayako tayari, kazi inayolenga programu kwenye pango lisilo na skrini, shina la matokeo lililoshughulika, au kazi iliyokataliwa na mratibu wa mfumo. |
| `organize_files_automation_jobs_failed_total` | Utekelezaji wa kazi ulioishia kwa kushindwa. |
| `organize_files_automation_jobs_awaiting_approval_total` | Utekelezaji halisi uliowekwa kando kusubiri idhini. |
| `organize_files_automation_execute_approvals_total` | Idhini zilizotolewa kwa utekelezaji halisi. |
| `organize_files_automation_execute_approvals_expired_total` | Idhini ambazo muda wake uliisha kabla ya kutumika. |
| `organize_files_automation_claim_conflicts_total` | Mara ambazo pango jingine lilikuwa tayari linashikilia dai juu ya shina la matokeo. |
| `organize_files_automation_runs_orphaned_total` | Utekelezaji uliookolewa kama yatima, ulioachwa na pango lililosimama. |
| `organize_files_automation_job_events_total` | Kihesabio kimoja kwa kila tukio, chenye lebo `event`, `job_id`, `target` na `jobs_file`. |
| `organize_files_automation_webhook_posts_succeeded_total` | Uwasilishaji wa webhook uliokubaliwa. |
| `organize_files_automation_webhook_posts_failed_total` | Uwasilishaji wa webhook uliokataliwa au usiofikika. |
| `organize_files_automation_webhook_dead_letter_depth` | Mistari inayosubiri kwa sasa katika faili la webhook zisizowasilishwa. |
| `organize_files_automation_log_retention_pruned_total` | Kumbukumbu za utekelezaji zilizoondolewa na sera ya kutunza. |
| `organize_files_automation_runs_index_compacted_total` | Mistari iliyotolewa kwenye faharasa ya utekelezaji wakati wa kubana. |
| `organize_files_automation_last_due_pass_exit_code` | Msimbo wa kutoka wa mzunguko wa mwisho uliokamilika. `0` ni mzunguko safi. |
| `organize_files_automation_last_due_pass_completed_utc` | Muda wa Unix kwa sekunde wa mzunguko wa mwisho uliokamilika, na `0` kabla ya wa kwanza. |

## Dashibodi na sheria za tahadhari

Dashibodi tayari ya Grafana huchapishwa pamoja na mafaili ya usambazaji kama `grafana-organize-files-automation.json`, chini ya kichwa **OrganizeFiles Automation**. Paneli zake kumi huonyesha mizunguko iliyofika muda wake, kazi zilizoanzishwa na zilizoshindwa, migongano ya madai, kasi ya kazi kwa saa moja, msimbo wa mwisho wa kutoka, kina cha ujumbe usiowasilishwa, kasoro za webhook kwa siku moja, kazi zinazosubiri idhini, na matukio ya kazi kwa hali. Kila paneli hutaja chanzo chake cha data kwa kishika nafasi `${DS_PROMETHEUS}`.

Sheria za tahadhari zinazolingana ni `alerts-organize-files-automation.yaml`, na `prometheus-rule-automation.yaml` ni gamba la Kubernetes kwa `kube-prometheus-stack`. Msimbo wa mwisho wa kutoka usio sifuri huonya baada ya dakika tano, kasoro ya leseni ni mbaya sana baada ya dakika moja, na sheria zilizobaki hushughulikia kazi zilizoshindwa, migongano ya madai, kasoro za webhook, mrundikano wa ujumbe usiowasilishwa, na idhini zilizoachwa zikisubiri siku moja. Mafaili yote mawili hukaguliwa kila ujenzi, hivyo majina ya juu hubaki sambamba na vihesabio.

# Matokeo ya uendeshaji na vipimo

## Safu ya hali

Eneo la **Matokeo ya uendeshaji** linaonyesha:

- Hali ya sasa ya programu na maendeleo ya injini.
- **CPU** na thamani mbili **kumbukumbu** kwa mchakato huu pekee.
- Mistari ya **GPU**, kwenye Windows: sehemu ya mchakato huu katika kila kadi ya michoro, si kadi nzima.

Upau wa rasilimali uliounganishwa hutumika tena katika madirisha ya zana za upili kama vile uchunguzi wa faili, kazi zilizoratibiwa na ukarabati wa faili.

## Lebo za kumbukumbu

- **Baiti za kibinafsi / ahadi** - kumbukumbu ya kibinafsi ya kibinafsi iliyohifadhiwa na mchakato.
- **Seti / kumbukumbu inayofanya kazi** — RAM ya mkazi inayoshikiliwa na mchakato huu kwa sasa. Inaweza kutofautiana na kifuatiliaji kingine cha mfumo wa uendeshaji kwa sababu kila OS na lebo za mazingira ya eneo-kazi huchakata kumbukumbu tofauti.

## Endesha mapigo ya moyo JSON (si lazima)

Washa **Andika mapigo ya moyo yakiendeshwa JSON** chini ya **Uchunguzi wa Kina/Uchunguzi**. Injini inaandika `Organize.Files.run.json` chini ya `Output\_OrganizeMediaLogs` (folda sawa na chaguo-msingi panga faili ya kuanza tena).

- **Njia** - imesasishwa kwa atomi wakati wa kupanga na kurekebisha.
- **Muda kati ya maandishi** — wakati vyanzo vinachunguzwa, faili huandikwa upya kwa kila faili 10,000 zilizoonekana, kila milinganisho 5,000 na takriban kila sekunde 15 uchunguzi ukiendelea, hivyo mti mkubwa wa mtandao unaoorodheshwa polepole bado huonyesha kwamba uendeshaji uko hai. Wakati wa uthibitishaji, uwekaji hashi na uhamishaji, huandikwa upya baada ya kila faili 1,000, si mara nyingi kuliko kila sekunde 5. Kuandika mwanzoni na mwishoni bado hufanyika wakati uendeshaji unaanza na kumalizika.
- **Maendeleo** — maadamu idadi ya faili bado inaongezeka, upau mkuu wa maendeleo huonyesha faili zilizoonekana hadi sasa badala ya asilimia mia moja, hadi hatua ipate jumla inayojulikana.
- **Mashamba** — `schema`,`mode`,`phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`),`runState`(`active`/`completed`/`failed`/`cancelled`),`utc`(ISO-8601), `dryRun`,`outputRoot`,`validateMedia`,`deepVideoValidate`,`gpuDeviceCount`, `hwaccel`, hiari`correlationId`, kiota`progress` vihesabio.
- **Kumbukumbu** - paneli ya pato la kuendesha huchapisha njia kamili mwanzoni na wakati faili imehifadhiwa mwishoni. Tumia **Fungua folda ya kumbukumbu ya mapigo ya moyo** / **Onyesha faili ya JSON ya mapigo ya moyo** chini ya Kina / Uchunguzi.
- **CLI** — `--heartbeat-json`washa OrganizeFiles.Cli. Ghairi na makosa mabaya ya ganda andika `cancelled`/`failed` `runState` inapowezeshwa.
