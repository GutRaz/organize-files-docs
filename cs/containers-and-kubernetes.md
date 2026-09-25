# Kontejnery — nastavení

## Co je požadováno

Pouze program `docker` nebo `kubectl` musí být dostupný na stroji, který spouští úlohu. Nic jiného není potřeba. Docker Desktop není podmínkou. Docker Engine na Linuxu, Rancher Desktop, colima a Podman s příkazem kompatibilním s dockerem fungují stejně, protože aplikace jednoduše spustí příkaz, který najde na systémové cestě.

Kubernetes funguje stejně. Je podporován jakýkoli cluster dosažitelný prostřednictvím `kubectl`, včetně k3s, kind, minikube a spravovaných clusterů, jako jsou EKS, GKE nebo AKS.

## Použití jiného démona nebo clusteru

Chcete-li odeslat úlohy jinému démonovi Docker, nastavte `DOCKER_HOST` nebo přepněte pomocí `docker context use`. Chcete-li použít jiný cluster Kubernetes, přepněte aktuální kontext pomocí `kubectl config use-context`. Aplikace se řídí tím, co již používá příkazový řádek, takže v aplikaci není potřeba žádné další nastavení.

## Kde jsou připojeny soubory

U Kubernetes je složka připojena jedním ze dvou způsobů. Místní vývojové kontexty získávají přímé připojení hostitelské složky. To zahrnuje kontext nazvaný `desktop`, `colima` nebo `orbstack`, kontext končící na `@desktop`, kontext začínající na `kind-`, `minikube` nebo `k3d-` a kontext, jehož název obsahuje `docker-desktop`, `docker-for-desktop` nebo `rancher-desktop`. S každým dalším kontextem se zachází jako se skutečným clusterem a místo toho získává trvalý nárok na svazek, protože skutečný uzel clusteru nevidí složky na stolním počítači. Nastavení `ORGANIZE_FILES_K8S_VOLUME_MODE` na `pvc` nebo `hostpath` tuto volbu přepíše pro každý kontext.

## Síťové složky v systému Windows

Docker Desktop v systému Windows nemůže připojit síťovou cestu, jako je `\\server\share`, ke kontejneru Linux. Windows vidí složku, ale kontejner ne. Obejít to lze dvěma způsoby. Použijte složku na místním disku, nebo místo toho spusťte úlohu s cílem aplikace, který provede práci přímo v aplikaci. Písmeno jednotky namapované na sdílenou složku nepomůže, protože aplikace ho dohledá zpět až k síťové cestě a odmítne ho stejně.

## Hotové soubory

Sady příkazového řádku pro Linux obsahují ve složce `containers` hotové soubory: Dockerfile, který sestaví obraz přímo ze sady, ukázku pro Compose, ukázky Job pro Kubernetes a `containers/README.md` a vedle něj README pro každý jazyk.

# Kontejnery a workery CLI

## Naplánované úlohy – cíle Docker a Kubernetes

Otevřete **Úlohy** z postranního panelu hlavního okna. Klikněte na **Nová úloha** nebo **Upravit** na existující kartě. V rozevíracím seznamu **Cíl** vyberte **Příkaz Docker** nebo **Úloha Kubernetes**.

1. Nastavte **Zdroje** (cesty hostitele) a **Output** (cesta hostitele – musí existovat před spuštěním úlohy).
2. Vyberte **Režim** a **Možnosti spuštění** jako u jakékoli jiné úlohy.
3. Panel **Náhled příkazu** zobrazuje přesný příkaz `docker run` nebo Kubernetes Job YAML, který bude použit.
4. **Uložte** úlohu a nastavte **Plán**, nebo klikněte na **Spustit nyní** na kartě a začněte okamžitě.

Aplikace generuje příznaky připojení a cesty svazku automaticky z uloženého snímku. Démon Docker nebo `kubectl` musí být dosažitelný na hostitelském počítači. **Preflight** zkontroluje konektivitu a před zahájením běhu hlásí všechny chyby v protokolu úlohy. Postup schvalování, načítání protokolů a headless plánování naleznete v části **Naplánované úlohy**.

## Terminál hostitele (PowerShell / bash / cmd)

Ano — na hostitelském počítači spusťte **OrganizeFiles.Cli** z PowerShellu, bashe nebo cmd. To je podporovaná cesta přes terminál. Okno Avalonia na ploše je samostatné grafické rozhraní. Publikujte nebo nainstalujte sadu CLI vedle aplikace (nebo do PATH) a pak předejte **--source** (lze opakovat), **--output** a **--mode**. Nejprve raději zkušební běh. **--execute** přidejte, až budete připraveni.

## Grafické rozhraní na ploše a kontejnery

Kontejnery a automatizace: Avalonia desktop GUI nemá běžet v typickém headless linuxovém kontejneru. Pro jednu nebo více izolovaných úloh, včetně několika paralelních pracovníků, použijte doprovod OrganizeFiles.Cli: v každém kontejneru připojte zdrojové složky pouze pro čtení pro úlohy náhledu nanečisto. Skutečné pohyby s **--execute** vyžadují připojení zapisovatelného zdroje, protože engine přemístí soubory mimo zdrojový strom. Použijte vyhrazený výstupní svazek pro čtení/zápis, zajistěte platné oprávnění k ukládání nebo vydavateli pro všechny běhy organizování/oprav (zkušební běh a provádění), předejte **--source** (opakovatelné), **--output** a **--mode**. Každý souběžný pracovník potřebuje svůj vlastní výstupní kořen. Složka **Output** již musí na hostiteli existovat před spuštěním úloh Docker nebo Kubernetes (preflight odmítne chybějící cíl a nevytvoří jej). Příklady cest: containers/README.md a containers/docker-compose.sample.yml. Jobs/JobAgent generované `docker run` připojí zdroje na `/in1`, `/in2`, … a výstup na `/out`. Manuální příklady z jednoho zdroje mohou používat `/in` (viz containers/README.md).
