# Kontena — usanidi

## Kinachotakiwa

Ni mpango wa `docker` au `kubectl` pekee ambao unapaswa kufikiwa kwenye mashine inayoendesha kazi hiyo. Hakuna kingine kinachohitajika. Eneo-kazi la Docker sio hitaji. Injini ya Docker kwenye Linux, Rancher Desktop, colima, na Podman yenye amri inayoendana na kizimbani zote hufanya kazi kwa njia ile ile, kwa sababu programu huendesha tu amri inayoipata kwenye njia ya mfumo.

Kubernetes inafanya kazi sawa. Kundi lolote linaloweza kufikiwa kupitia `kubectl` linatumika, ikiwa ni pamoja na k3s, kind, minikube, na makundi yanayodhibitiwa kama vile EKS, GKE, au AKS.

## Kwa kutumia daemoni au nguzo tofauti

Ili kutuma kazi kwa daemoni nyingine ya Docker, weka `DOCKER_HOST` au ubadilishe na `docker context use`. Ili kutumia nguzo nyingine ya Kubernetes, badilisha muktadha wa sasa na `kubectl config use-context`. Programu hufuata chochote ambacho mstari wa amri tayari unatumia, kwa hivyo hakuna mpangilio wa ziada unaohitajika ndani ya programu.

## Mahali ambapo faili zimewekwa

Kwa Kubernetes, folda imeunganishwa kwa moja ya njia mbili. Miktadha ya ukuzaji wa eneo lako hupata folda ya mwenyeji wa moja kwa moja. Hiyo inashughulikia muktadha unaoitwa `desktop`, `colima` au `orbstack`, ule unaoishia na `@desktop`, ule unaoanza na `kind-`, `minikube` au `k3d-`, na ule ambao jina lake lina `docker-desktop`, `docker-for-desktop` au `rancher-desktop`. Kila muktadha mwingine unachukuliwa kama nguzo halisi na hupata dai la hifadhi ya kudumu, kwa sababu nodi halisi ya nguzo haiwezi kuona folda kwenye mashine ya mezani. Kuweka `ORGANIZE_FILES_K8S_VOLUME_MODE` kuwa `pvc` au `hostpath` kunabatilisha chaguo hilo kwa kila muktadha.

## Folda za mtandao kwenye Windows

Docker Desktop kwenye Windows haiwezi kuambatisha njia ya mtandao kama vile `\\server\share` kwenye chombo cha Linux. Windows huona folda, lakini chombo hakioni. Kuna njia mbili za kuepuka hili. Tumia folda kwenye diski ya ndani, au endesha kazi hiyo kwa Lengo la Programu badala yake, ambayo hufanya kazi katika programu yenyewe. Herufi ya diski iliyounganishwa na folda iliyoshirikiwa haisaidii, kwa sababu programu huifuatilia hadi njia ya mtandao na kuikataa vivyo hivyo.

## Faili zilizotengenezwa tayari

Vifurushi vya mstari wa amri vya Linux vina faili zilizo tayari katika folda yao ya `containers`: Dockerfile inayojenga picha kutoka kifurushi chenyewe, mfano wa Compose, mifano ya Job ya Kubernetes na `containers/README.md`, pamoja na README ya kila lugha kando yake.

# Vyombo na workers wa CLI

## Kazi zilizoratibiwa - Malengo ya Docker na Kubernetes

Fungua **Kazi** kutoka kwa upau wa kando wa dirisha kuu. Bofya **Kazi mpya** au **Badilisha** kwenye kadi iliyopo. Katika kushuka kwa **Lengo** chagua **Amri ya Docker** au **kazi ya Kubernetes**.

1. Weka **Vyanzo** (njia za mwenyeji) na **Pato** (njia ya mwenyeji - lazima iwe tayari kuwepo kabla ya kazi kuanza).
2. Chagua **Njia** na **Endesha chaguzi** kama kwa kazi nyingine yoyote.
3. Paneli ya **Onyesho la kukagua Amri** inaonyesha amri kamili ya `docker run` au Kubernetes Job YAML ambayo itatumika.
4. **Hifadhi** kazi na uweke **Ratiba**, au bofya **Endesha sasa** kwenye kadi ili kuanza mara moja.

Programu hutoa bendera za kupachika na njia za sauti kiotomatiki kutoka kwa muhtasari uliohifadhiwa. Daemon ya docker au `kubectl` lazima ipatikane kwenye mashine ya kupangisha. **Preflight** hukagua muunganisho na kuripoti hitilafu zozote kwenye kumbukumbu ya kazi kabla ya operesheni kuanza. Kwa mtiririko wa idhini, urejeshaji kumbukumbu, na upangaji usio na kiolesura, angalia **Kazi Zilizoratibiwa**.

## Kituo cha mashine mwenyeji (PowerShell / bash / cmd)

Ndiyo — kwenye mashine mwenyeji endesha **OrganizeFiles.Cli** kutoka PowerShell, bash, au cmd. Hiyo ndiyo njia ya kituo inayoungwa mkono. Dirisha la eneo-kazi la Avalonia ni kiolesura tofauti cha picha. Chapisha au sakinisha seti ya CLI kando ya programu (au kwenye PATH), kisha pitisha **--source** (inaweza kurudiwa), **--output**, na **--mode**. Ni afadhali kuanza na uendeshaji wa majaribio. Ongeza **--execute** pale tu utakapokuwa tayari.

## Kiolesura cha eneo-kazi na vyombo

Vyombo na otomatiki: GUI ya eneo-kazi la Avalonia haikusudiwi kufanya kazi ndani ya chombo cha kawaida cha Linux kisicho na kiolesura. Kwa kazi moja au zaidi zilizotengwa, ikijumuisha wafanyikazi kadhaa sambamba, tumia OrganizeFiles.Cli mwandani: katika kila kontena weka folda za chanzo zinazosomwa tu kwa kazi za kukagua bila kukauka. Usogezaji halisi ukitumia **--execute** unahitaji kupachika chanzo kinachoweza kuandikwa kwa sababu injini huhamisha faili kutoka kwenye mti chanzo. Tumia sauti maalum ya kusoma/kuandika, hakikisha kwamba hifadhi halali au haki ya mchapishaji kwa uendeshaji/urekebishaji wote (kausha na utekeleze), pitisha **--source** (inayorudiwa), **--output**, na **--mode**. Kila mfanyakazi wa wakati mmoja anahitaji mzizi wake wa pato. Folda ya **Output** lazima iwe tayari kuwepo kwenye seva pangishi kabla ya Docker au Kubernetes jobs kutekelezwa (preflight inakataa mahali inapokosekana na isiiunde). Mfano wa njia: containers/README.md na containers/docker-compose.sample.yml. Jobs/JobAgent imetengenezwa `docker run` huweka vyanzo katika `/in1`, `/in2`, … na kutoa kwa `/out`. Mifano ya mwongozo ya chanzo-moja inaweza kutumia `/in` (ona containers/README.md).
