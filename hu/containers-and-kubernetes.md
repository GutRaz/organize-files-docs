# Konténerek — beállítás

## Mi szükséges

Csak az `docker` vagy `kubectl` programnak kell elérhetőnek lennie a feladatot futtató gépen. Semmi másra nincs szükség. A Docker Desktop nem követelmény. A Docker Engine Linuxon, a Rancher Desktopon, a colimán és a Docker-kompatibilis paranccsal rendelkező Podmanen ugyanúgy működik, mert az alkalmazás egyszerűen futtatja a rendszer elérési útjában talált parancsot.

A Kubernetes ugyanúgy működik. Minden `kubectl`-on keresztül elérhető fürt támogatott, beleértve a k3s-t, a kind-et, a minikube-ot és a felügyelt fürtöket, például az EKS-t, a GKE-t vagy az AKS-t.

## Másik démon vagy fürt használata

Ha feladatokat szeretne küldeni egy másik Docker-démonnak, állítsa be az `DOCKER_HOST` értéket, vagy váltson az `docker context use` segítségével. Másik Kubernetes-fürt használatához váltson az aktuális környezetre az `kubectl config use-context` segítségével. Az alkalmazás követi azt, amit a parancssor már használ, így nincs szükség további beállításokra az alkalmazáson belül.

## A fájlok beillesztési helyére

A Kubernetes esetében a mappa kétféleképpen csatolható. A helyi fejlesztési környezetek közvetlen gazdagépmappa-csatlakozást kapnak. Ez lefedi a `desktop`, `colima` vagy `orbstack` nevű kontextust, a `@desktop` végződésű kontextust, a `kind-`, `minikube` vagy `k3d-` kezdetű kontextust, valamint azt a kontextust, amelynek a neve tartalmazza a `docker-desktop`, `docker-for-desktop` vagy `rancher-desktop` szöveget. Minden más kontextus valódi fürtként kezelendő, és ehelyett állandó kötetigényt kap, mivel a valódi fürtcsomópont nem láthatja az asztali gépen lévő mappákat. Ha az `ORGANIZE_FILES_K8S_VOLUME_MODE` értéke `pvc` vagy `hostpath`, az minden kontextusnál felülírja ezt a választást.

## Hálózati mappák Windows rendszeren

Windows rendszeren a Docker Desktop nem tud hálózati elérési utat, például `\\server\share` csatolni egy Linux-tárolóhoz. A Windows látja a mappát, de a tárolót nem. Kétféleképpen kerülheti meg. Használjon egy mappát a helyi lemezen, vagy futtassa inkább a feladatot az alkalmazás céljával, amely magában az alkalmazásban végzi el a munkát. A megosztáshoz rendelt meghajtóbetűjel nem segít, mert az alkalmazás visszavezeti a hálózati elérési útra, és ugyanúgy elutasítja.

## Kész fájlok

A Linux parancssori csomagok `containers` mappájában kész fájlok vannak: egy Dockerfile, amely magából a csomagból készíti el a lemezképet, egy Compose-minta, Kubernetes Job-minták és a `containers/README.md`, mellette minden nyelvhez egy README.

# Konténerek és CLI workerek

## Ütemezett munkák — Docker és Kubernetes célpontok

Nyissa meg a **Feladatok** elemet a főablak oldalsávjáról. Kattintson az **Új munka** vagy a **Szerkesztés** lehetőségre egy meglévő kártyán. A **Cél** legördülő menüben válassza a **Docker parancs** vagy a **Kubernetes-feladat** lehetőséget.

1. Állítsa be a **Források** (gazdaútvonalak) és **Kimenet** (gazdagép elérési útja – már léteznie kell, mielőtt a job fut) értéket.
2. Válassza a **Mód** és a **Futtatási beállítások** lehetőséget, mint bármely más feladatnál.
3. A **Parancs előnézete** panelen pontosan az alkalmazandó `docker run` parancs vagy Kubernetes Job YAML látható.
4. **Mentse el** a munkát, és állítson be egy **Ütemezést**, vagy kattintson a **Futtatás most** lehetőségre a kártyán az azonnali kezdéshez.

Az alkalmazás automatikusan generálja a csatolási jelzőket és a kötet elérési útvonalait a mentett pillanatképből. A Docker démonnak vagy a "kubectl"-nek elérhetőnek kell lennie a gazdagépen. Az **Preflight** ellenőrzi a kapcsolatot, és minden hibát jelent a munkanaplóban a futtatás megkezdése előtt. A jóváhagyási folyamattal, a naplók lekérésével és a fej nélküli ütemezéssel kapcsolatban lásd: **Ütemezett feladatok**.

## A gazdagép terminálja (PowerShell / bash / cmd)

Igen — a gazdagépen indítsa az **OrganizeFiles.Cli** programot PowerShellből, bashből vagy cmd-ből. Ez a támogatott terminálos út. Az Avalonia asztali ablaka külön grafikus felület. Tegye közzé vagy telepítse a CLI-készletet az alkalmazás mellé (vagy a PATH útvonalra), majd adja át a **--source** (ismételhető), **--output** és **--mode** kapcsolókat. Kezdje inkább próbafuttatással. A **--execute** kapcsolót csak akkor tegye hozzá, amikor készen áll.

## Asztali felület és konténerek

Tárolók és automatizálás: az Avalonia asztali grafikus felhasználói felületet nem arra tervezték, hogy egy tipikus fej nélküli Linux-tárolóban fusson. Egy vagy több elszigetelt jobhoz, beleértve több párhuzamos dolgozót is, használja a OrganizeFiles.Cli kísérőt: minden tárolóba csak olvasható forrásmappákat kell felszerelni a próbafuttatásként futtatott előnézeti feladatokhoz. A **--execute** valódi áthelyezései írható forrás beillesztést igényelnek, mert a motor áthelyezi a fájlokat a forrásfából. Használjon dedikált olvasási/írási kimeneti kötetet, biztosítson érvényes tárolási vagy kiadói jogosultságot minden szervezési/javítási futtatáshoz (próbafuttatás és végrehajtás), adja át a **--source** (ismételhető), **--output** és **--mode** kódot. Minden párhuzamos dolgozónak szüksége van saját kimeneti gyökérre. A **Output** mappának már léteznie kell a gazdagépen, mielőtt a Docker- vagy Kubernetes-feladatok futnának (az előzetes ellenőrzés elutasítja a hiányzó célhelyet, és nem hozza létre azt). Példaútvonalak: containers/README.md és containers/docker-compose.sample.yml. A Jobs/JobAgent által generált `docker run` a forrásokat a `/in1`, `/in2`, … helyeken csatlakoztatja, a kimenetet pedig a `/out` helyen. A manuális, egyforrású példák használhatják a `/in` kódot (lásd: containers/README.md).
