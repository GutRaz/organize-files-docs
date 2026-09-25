# Kontenery — konfiguracja

## Co jest wymagane

Tylko program `docker` lub `kubectl` musi być osiągalny na komputerze, na którym wykonuje się zadanie. Nic więcej nie jest potrzebne. Docker Desktop nie jest wymogiem. Docker Engine w systemie Linux, Rancher Desktop, colima i Podman z poleceniem zgodnym z Dockerem działają w ten sam sposób, ponieważ aplikacja po prostu uruchamia polecenie znalezione w ścieżce systemowej.

Kubernetes działa tak samo. Obsługiwany jest dowolny klaster osiągalny za pośrednictwem `kubectl`, w tym k3s, kind, minikube i klastry zarządzane, takie jak EKS, GKE lub AKS.

## Używanie innego demona lub klastra

Aby wysłać zadania do innego demona Dockera, ustaw `DOCKER_HOST` lub przełącz za pomocą `docker context use`. Aby użyć innego klastra Kubernetes, przełącz bieżący kontekst za pomocą `kubectl config use-context`. Aplikacja działa zgodnie z tym, czego używa już linia poleceń, więc nie są potrzebne żadne dodatkowe ustawienia w aplikacji.

## Miejsce zamontowania plików

W przypadku Kubernetes folder jest dołączany na jeden z dwóch sposobów. Lokalne konteksty programistyczne są montowane bezpośrednio w folderze hosta. Obejmuje to kontekst o nazwie `desktop`, `colima` lub `orbstack`, kontekst kończący się na `@desktop`, kontekst zaczynający się od `kind-`, `minikube` lub `k3d-` oraz kontekst, którego nazwa zawiera `docker-desktop`, `docker-for-desktop` lub `rancher-desktop`. Każdy inny kontekst jest traktowany jak prawdziwy klaster i zamiast tego otrzymuje trwałe żądanie woluminu, ponieważ prawdziwy węzeł klastra nie widzi folderów na komputerze stacjonarnym. Ustawienie `ORGANIZE_FILES_K8S_VOLUME_MODE` na `pvc` lub `hostpath` zastępuje ten wybór dla każdego kontekstu.

## Foldery sieciowe w systemie Windows

Docker Desktop w systemie Windows nie może dołączyć ścieżki sieciowej, takiej jak `\\server\share`, do kontenera systemu Linux. System Windows widzi folder, ale kontener nie. Można to obejść na dwa sposoby. Użyj folderu na dysku lokalnym albo zamiast tego uruchom zadanie z elementem docelowym aplikacji, co spowoduje wykonanie pracy w samej aplikacji. Litera dysku zmapowana na udział nie pomoże, bo aplikacja śledzi ją z powrotem do ścieżki sieciowej i odrzuca tak samo.

## Gotowe pliki

Zestawy wiersza poleceń dla Linuksa zawierają w folderze `containers` gotowe pliki: Dockerfile budujący obraz z samego zestawu, przykład Compose, przykłady Job dla Kubernetes oraz `containers/README.md`, a obok niego README dla każdego języka.

# Kontenery i workery CLI

## Zaplanowane zadania — cele Dockera i Kubernetesa

Otwórz **Praca** na pasku bocznym okna głównego. Kliknij **Nowa praca** lub **Edytuj** na istniejącej karcie. Z menu **Cel** wybierz **Polecenie Docker** lub **Zadanie Kubernetes**.

1. Ustaw **Źródła** (ścieżki hosta) i **Wyjście** (ścieżka hosta — musi już istnieć przed uruchomieniem zadania).
2. Wybierz **Tryb** i **Opcje uruchamiania**, tak jak w przypadku każdego innego zadania.
3. Panel **Podgląd poleceń** pokazuje dokładnie polecenie „uruchamianie dokera” lub YAML zadania Kubernetes, które zostanie zastosowane.
4. **Zapisz** zadanie i ustaw **Harmonogram** lub kliknij **Uruchom teraz** na karcie, aby rozpocząć natychmiast.

Aplikacja automatycznie generuje flagi montowania i ścieżki woluminów na podstawie zapisanej migawki. Demon Dockera lub „kubectl” musi być osiągalny na komputerze hosta. **Preflight** sprawdza łączność i zgłasza wszelkie błędy w protokole zadania przed rozpoczęciem przebiegu. Aby zapoznać się z procesem zatwierdzania, pobieraniem dzienników i planowaniem headless, zobacz **Zaplanowane zadania**.

## Terminal komputera gospodarza (PowerShell / bash / cmd)

Tak — na komputerze gospodarza uruchom **OrganizeFiles.Cli** z programu PowerShell, bash lub cmd. To jest wspierana droga przez terminal. Okno pulpitu Avalonia to osobny interfejs graficzny. Opublikuj albo zainstaluj zestaw CLI obok aplikacji (lub w PATH), a następnie przekaż **--source** (można powtarzać), **--output** i **--mode**. Lepiej zacząć od uruchomienia próbnego. **--execute** dodaj dopiero wtedy, gdy wszystko jest gotowe.

## Interfejs pulpitu i kontenery

Kontenery i automatyzacja: graficzny interfejs użytkownika Avalonia na komputery stacjonarne nie jest przeznaczony do działania w typowym, headless kontenerze Linuksa. W przypadku jednego lub większej liczby izolowanych zadań, w tym kilku równoległych procesów roboczych, użyj towarzysza OrganizeFiles.Cli: w każdym kontenerze montuj foldery źródłowe tylko do odczytu dla zadań podglądu próbnego. Prawdziwe ruchy za pomocą **--execute** wymagają zapisywalnego montowania źródła, ponieważ silnik przenosi pliki poza drzewo źródłowe. Użyj dedykowanego woluminu wyjściowego do odczytu/zapisu, upewnij się, że masz ważne uprawnienia sklepu lub wydawcy do wszystkich przebiegów organizowania/naprawy (przebieg próbny i wykonanie), przekaż **--source** (powtarzalne), **--output** i **--mode**. Każdy współbieżny proces roboczy potrzebuje własnego katalogu głównego wyjściowego. Folder **Output** musi już istnieć na hoście, zanim zostaną uruchomione zadania Dockera lub Kubernetesa (inspekcja wstępna odrzuca brakujące miejsce docelowe i go nie tworzy). Przykładowe ścieżki: containers/README.md i containers/docker-compose.sample.yml. Wygenerowane przez Jobs/JobAgent `docker run` montuje źródła w `/in1`, `/in2`, … i wyjście w `/out`. W przykładach podręczników z jednego źródła można używać `/in` (patrz containers/README.md).
