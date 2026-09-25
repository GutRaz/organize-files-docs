# Kina / Uchunguzi

## Panga urekebishaji

Uchunguzi wa Kina/Uchunguzi hufichua chaguo za **OrganizeFilesEngine** bila kusumbua kidirisha kikuu.

Njia za kupanga zinaweza kurekebisha dedupe, faharasa ya lengwa, sheria za Kipekee za tarehe, kusogeza na kuorodhesha, nyongeza ya BFS, faili ya resume na mizizi ya ziada ya Kipekee.

Urekebishaji huweka tu muda wa kujaribu tena wa mtandao na diski kamili, njia za maunzi za michoro zilizogunduliwa kwa ukaguzi wa hiari wa video kamili, bafa ya kusoma kwa heshi na mapigo ya moyo ya JSON. Sehemu zingine zinaonekana kwa muktadha lakini zimezimwa.

Wakati vyanzo au pato linapatikana kwenye njia za NAS au UNC, usambamba wa chini, weka kipengele cha kujaribu tena mtandao, waashe ziada ya BFS ili upate miti isiyo ya kawaida ya SMB, na ujaribu bafa ya heshi 8 ikiwa hashing ni polepole.

# Advanced / Diagnostics - kila chaguo

## Kuhusu sura hii

Vidhibiti hivi ni chaguo za injini. Programu ya kompyuta (Windows, macOS, Linux), Android, iOS na zana ya mstari wa amri husoma thamani zilezile.

Modi za **Panga** hutumia kila kidhibiti kilicho hapa chini isipokuwa kiolesura kikikifanya kijivu. **Rekebisha** hutumia tu kujaribu tena kwa mtandao, kujaribu tena diski ikijaa, njia za maunzi ya michoro zilizotambuliwa (pamoja na ukaguzi kamili wa video), bafa ya kusoma hashi, JSON ya mpigo wa moyo, **Faili ya hali ya kuendelea** na **Anza upya (punguza faili ya hali ya kuendelea)**. Sehemu nyingine hubaki zikionekana lakini hazizingatiwi wakati wa kurekebisha.

## Vyanzo vya mtandao (NAS / UNC)

Wakati Vyanzo au Pato ziko kwenye hisa za SMB/CIFS, juzuu za NAS, au hifadhi zilizopangwa, kagua sehemu hii kwa makini.

- **Kwa nini utunge** — Hesabu za nyuzi zinazofanya kazi kwenye SSD ya ndani zinaweza kusimamisha au kupakia faili nyingi.
- **Cha kujaribu** — Endelea kujaribu mtandao. Punguza minyororo ya kusogeza chini na enum max sambamba kwenye muda wa kuisha. Wacha kiambatanisho BFS isipokuwa kama hesabu kamili ilithibitishwa bila hiyo. Jaribu bafa ya 8 MiB wakati hashing ni polepole kwenye mtandao.
- **Zima kusubiri kwa mtandao** — Inashindwa haraka kwenye hitilafu za muda mfupi za mtandao. Hatari kwenye Wi-Fi au kushiriki kwa shughuli nyingi.

## Dedupe mode

Jinsi injini huamua faili mbili ni nakala.

| Hali | Inafanya nini | Wakati wa kutumia | Biashara |
| ---- | ------------ | ----------- | --------- |
| **Hashi (SHA-256)** | Husoma na kuharakisha maudhui kamili ya kila faili asili iliyojumuishwa, kisha hupanga baiti zinazofanana. | Njia kali zaidi ya vitendo. Hash (SHA-256) inahitajika kwa kufuta kwenye chanzo (nakala na faili zenye tatizo). | Polepole kwenye miti mikubwa au NAS. Hakuna algorithm inapaswa kuwasilishwa kama dhamana kamili. |
| **Ukubwa + wakati + jina** | Ufunguo = saizi, tiki za UTC za mwisho kuandika, jina lenye herufi ndogo, kisha uthibitishaji kamili wa SHA-256. | Hali ya upatanifu ya kihafidhina kwa mipangilio ya folda za media za zamani. | Inaweza kukosa nakala zilizopewa jina jipya. Kamwe usitumie kwa kufuta nakala au faili zenye tatizo. |
| **Hakuna** | Hakuna ugawaji wa faili tofauti. | Inapanga tu, si kusafisha nakala. | Nakala hukaa katika vyanzo. |

## Ruka faharasa lengwa

- **Imezimwa (chaguo-msingi)** — Huchanganua towe lililopo la **Kipekee** na kulifahasa kabla ya hashing. Salama zaidi unapotumia tena folda ile ile ya towe.
- **Imewashwa** — Huruka skanning.
- **Faida** — Haraka zaidi kwenye miti mikubwa ya mazao.
- **Hatari** — Maudhui zaidi rudufu yanaweza kutua ndani ya Kipekee.

## Mwaka wa chini wa Kipekee

Kima cha chini cha mwaka wa kalenda kwa folda za tarehe chini ya **Kipekee** katika mipangilio ya midia. **Kwa nini** — Huepuka kutawanya faili za zamani sana kwenye folda za mwaka usio wa kawaida wakati metadata si sahihi.

## Hamisha nyuzi

Usogezi wa faili sambamba baada ya marudio kuhifadhiwa.

- **Juu** — Haraka zaidi kwenye SSD ya ndani.
- **Chini** — Salama zaidi kwenye viendeshi vya ramani vya NAS, USB, au Wi-Fi.

## Nyuzi za uainishaji na hash

Wafanyakazi sambamba wakati wa kuchanganua vyanzo na kuondoa nakala SHA-256.

- **Nyuzi za uainishaji** — Kugundua na kuainisha faili. CLI: `--classify-threads <n>`.
- **Nyuzi za hashi** — Wafanyakazi wa hashing ya maudhui. CLI: `--hash-threads <n>`.
- **Ubatilishaji** — Thamani za mkono hubatilisha chaguo-msingi za wasifu (`--profile`).

## Enum sambamba max

Kikomo kwa uorodheshaji wa saraka sambamba wakati wa kuchanganua.

- **0** = injini otomatiki.
- **Chini** — Shinikizo kidogo kwenye SMB wakati folda nyingi zinaorodheshwa mara moja.

## Nyongeza ya BFS pasi

- **Washa (chaguomsingi)** — Pita moja ya ziada, ya juujuu, kwa upana kwanza.
- **Kwa nini** — Baadhi ya njia za NAS au miti mirefu huonekana haijakamilika baada ya pita ya kwanza.
- **Zima** — Baada tu ya kuthibitisha idadi kamili ya faili bila hiyo.
- **CLI** — `--no-bfs` huzima pita hii.

## Rejesha faili ya hali

Chaguo la UTF-8. Hatua zilizofanikiwa huongeza mistari ya `B64|` ili uratibu unaofuata uweze kuruka vyanzo vilivyokamilika.

- **Kwa nini** — Endelea na kazi ndefu baada ya kusimama au kuacha kufanya kazi.
- **Njia chaguo-msingi** — Uga unapokuwa tupu wakati wa kuendesha, injini hutumia `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt`. Bila Output, hutumia `sessions\<id>\resume\OrganizeFiles.resume.txt` chini ya wasifu wa programu.
- **UI ya Eneo-kazi** — Orodha ya njia za kusoma pekee kwa ajili ya uteuzi wa kipanya na kunakili. Wakati faili ya resume tayari iko kwenye eneo la msingi, njia inaonekana moja kwa moja. **Vinjari** huchagua folda ya kumbukumbu na kuambatanisha `OrganizeFiles.resume.txt`. **Ondoa** husafisha njia. Wakati tupu, kidokezo kinaonyesha njia inayotumiwa wakati wa kuendesha.

## Anza upya

Inapunguza faili ya kuanza tena wakati uendeshaji wa upangaji **halisi** unapoanza (wa majaribio haikatiki). Kwa **Hifadhi maendeleo na nafasi ya kazi**, pia hufuta muhtasari wa UI uliohifadhiwa wakati wa kuanza. **Kwa nini** — Lazimisha kuhesabiwa upya kamili badala ya kuendeleza kumbukumbu ya zamani ya kuanza tena.

## Mizizi ya Kipekee zaidi ya kuchanganua

Folda moja kwa kila mstari: miti ya ziada **Kipekee** ili kuorodhesha (mpangilio wa urithi, ujazo mwingine).

- **Kwa nini** — Dedupe inaweza kuona faili ambazo tayari zimepangwa mahali pengine bila kuzihamisha tena.
- **UI ya Eneo-kazi** — Orodha ya kusoma tu kwa nakala kwa kila mstari. **Ongeza** huongeza folda iliyochaguliwa. **Ondoa** hufuta laini iliyochaguliwa (kwa mfano mti wa zamani `Uniques` kwenye NAS).

## Jaribu tena mtandao (sekunde) / Zima kusubiri kwa mtandao

Sekunde ili kujaribu tena mtandao wa muda mfupi I/O.

- **Kwa nini** — Vijalada vya SMB huacha vipindi visivyofanya kazi. Inatumiwa na kupanga na kutengeneza.
- **Zima kusubiri kwa mtandao** — Acha kusubiri na ushindwe badala yake.

## Jaribio kamili la diski

(sekunde) / Zima kusubiri kwa diski-kamili

Mchoro sawa wakati kiasi cha towe kinapoishiwa na nafasi. **Kwa nini** — Wakati wa kufungia diski wakati wa kuendesha kwa muda mrefu.

## Njia za kadi ya michoro

Ni pale tu ambapo **ukaguzi kamili wa video** uliojengwa ndani umewashwa na **Tumia kadi ya michoro iliyogunduliwa** pia imewashwa. Thamani zaidi ya **0** huweka idadi kamili ya njia kwa ukaguzi sambamba kati ya watengenezaji waliogunduliwa (NVIDIA, AMD, Intel, Apple, simu). **0** humaanisha idadi ya njia hutafutwa yenyewe. Haimaanishi kichakataji pekee. Ili kuchukua sampuli kwenye kichakataji pekee, chagua **CPU pekee** kwenye orodha ya kadi za michoro. Alama za njia hupanga ukaguzi wa mtiririko wa biti kwenye kichakataji. Hazitii mfumo wa kusimbua video kwa vifaa.

- **Mpangilio wa mstari wa amri** — `--hwaccel <value>` huchagua mpangilio wa njia za ukaguzi (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`) wakati ukaguzi kamili wa video unaendelea.

## Bafa ya kusoma kwa hashi kwa kila

mfanyakazi husoma bafa huku akiharakisha (512 KiB, 1 MiB, 8 MiB). **Kwa nini** — Vihifadhi vikubwa zaidi husaidia kupunguza kasi ya NAS na kushiriki kwa muda wa juu.

## Rekodi jarida la kutendua

Jarida la hiari la JSONL la uhamishaji chini ya mzizi wa matokeo kwa uendeshaji huu.

- **Kwa nini** — Huwezesha kutendua kupitia CLI baada ya uendeshaji halisi.
- **Kumbukumbu** — Kuhifadhi baada ya kupanga hubaki kimezimwa jarida likiwa hai.
- **CLI** — `--record-undo-journal` (sawa na kisanduku cha dirisha kuu).

## Andika mapigo ya moyo yanayoendelea

Huandika faili ya hiari `Organize.Files.run.json` chini ya `Output\_OrganizeMediaLogs`.

- **Kwa nini** — Zana za nje zinaweza kusoma vihesabu hai (zilizochunguzwa, zilizopangwa, zilizokamilika) wakati wa kupanga au kutengeneza.
- **Muda kati ya maandishi** — Kila faili 10,000 zilizoonekana, kila milinganisho 5,000 na takriban kila sekunde 15 wakati wa uchunguzi wa vyanzo, baada ya kila faili 1,000 na si mara nyingi kuliko kila sekunde 5 wakati wa uthibitishaji, uwekaji hashi na uhamishaji, na kwenye kila hatua kubwa.
