# Nadzór za pomocą Prometheus i Grafana

## Co obejmują liczniki

Zaplanowane zadania prowadzą niewielki zestaw liczników i wskaźników Prometheus. Każda nazwa zaczyna się od `organize_files_automation_`, a cały zestaw jest publikowany jako tekst Prometheus. Wszystkie trzy hosty uruchamiające zadania publikują ten sam zestaw: aplikacja na pulpicie, usługa `OrganizeFiles.JobAgent` oraz host wiersza poleceń używany w kontenerach.

Liczniki opisują harmonogram, a nie pliki. Liczone są przebiegi, wyniki zadań, zatwierdzenia, dostarczanie webhooków i porządkowanie historii. O plikach, które zadanie przenosi, nie liczy się nic.

## Eksport do pliku, bez otwartego portu

`automation-metrics.prom` zapisywany jest w folderze danych automatyzacji, obok `automation-jobs.json`, i odświeżany po każdym należnym przebiegu oraz przy każdym odczycie. Układ jest taki, jaki czyta kolektor textfile narzędzia `node_exporter`, więc maszyna, na której `node_exporter` już działa, jest objęta bez nasłuchującego portu, bez tokenu i bez reguły zapory. Plik jest podmieniany atomowo, a dowiązanie symboliczne pozostawione w jego miejscu zatrzymuje zapis, zamiast zostać podążone.

## Punkt odczytu

Punkt odczytu istnieje tylko wtedy, gdy `ORGANIZE_FILES_METRICS_HTTP_PORT` zawiera port z przedziału od 1 do 65535. Bez tej zmiennej nic nie nasłuchuje.

| Zmienna | Skutek |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | Port nasłuchu. Jeśli go brakuje lub leży poza zakresem, punkt odczytu w ogóle nie istnieje. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Adres nasłuchu. Domyślnie `127.0.0.1`. Wartości `0.0.0.0`, `+` i `*` oznaczają wszystkie adresy, a cokolwiek innego wraca do `127.0.0.1`. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | Token bearer wymagany na `/metrics` i na `/ready`. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` pozwala `/ready` odpowiadać bez tego tokenu, na potrzeby sond klastra. Ścieżki hosta są wtedy pomijane w odpowiedzi. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | Rozdzielone przecinkami kody wyjścia, przy których `/ready` zgłasza brak gotowości. Zastępuje listę wbudowaną. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` pomija kod wyjścia ostatniego przebiegu, a także stan sprzed zakończenia pierwszego przebiegu. |
| `ORGANIZE_FILES_READY_JSON` | `1` wymusza odpowiedź JSON na `/ready`, nawet dla wywołującego, który poprosił o czysty tekst. |

Adres spoza pętli lokalnej jest odrzucany przed otwarciem nasłuchu, o ile nie ustawiono tokenu bearer. Odmowa trafia na wyjście błędów i jest wysyłana jako zdarzenie webhooka, ponieważ takie połączenie oddałoby liczniki całej sieci.

## Obsługiwane ścieżki

- `/metrics` — liczniki jako tekst Prometheus. Żądanie do `/` zwraca tę samą treść.
- `/ready` — gotowość dla orkiestratora. Odpowiedź brzmi `200`, gdy folder automatyzacji przyjmie zapis próbny, plik zadań daje się otworzyć, folder historii rozwiązuje się wewnątrz katalogu danych, a ostatni należny przebieg zakończył się kodem wyjścia, który nie blokuje. W przeciwnym razie odpowiedzią jest `503` z krótkim powodem, takim jak `due_pass_not_completed` lub `last_due_pass_license_failed`.
- `/health` — tylko znak życia. Ta ścieżka pozostaje anonimowa nawet przy ustawionym tokenie, ponieważ odpowiada `ok` i nic więcej.

Kody wyjścia `3` dla błędu licencji, `8` dla zablokowanego drzewa wyjściowego, `10` dla nigdy niepotwierdzonego usunięcia i `11` dla konfliktu zastrzeżenia domyślnie blokują gotowość. Treść na `/ready` to JSON, chyba że wywołujący wyśle `Accept: text/plain` albo doda `?format=text`.

## Liczniki

| Nazwa | Zawartość |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Należne przebiegi rozpoczęte przez harmonogram. |
| `organize_files_automation_jobs_started_total` | Uruchomienia zadań, które osiągnęły stan działania. |
| `organize_files_automation_jobs_skipped_total` | Pominięte zadania: środowisko Docker lub Kubernetes, które nie jest gotowe, zadanie wymierzone w aplikację na hoście bez ekranu, zajęty katalog wyjściowy, albo zadanie odrzucone przez orkiestratora. |
| `organize_files_automation_jobs_failed_total` | Uruchomienia zadań zakończone niepowodzeniem. |
| `organize_files_automation_jobs_awaiting_approval_total` | Prawdziwe uruchomienia wstrzymane do zatwierdzenia. |
| `organize_files_automation_execute_approvals_total` | Zatwierdzenia udzielone prawdziwemu uruchomieniu. |
| `organize_files_automation_execute_approvals_expired_total` | Zatwierdzenia, którym upłynął termin przed użyciem. |
| `organize_files_automation_claim_conflicts_total` | Przypadki, gdy inny host trzymał już zastrzeżenie katalogu wyjściowego. |
| `organize_files_automation_runs_orphaned_total` | Uruchomienia odzyskane jako osierocone, pozostawione przez host, który się zatrzymał. |
| `organize_files_automation_job_events_total` | Jeden licznik na zdarzenie, z etykietami `event`, `job_id`, `target` i `jobs_file`. |
| `organize_files_automation_webhook_posts_succeeded_total` | Przyjęte dostarczenia webhooków. |
| `organize_files_automation_webhook_posts_failed_total` | Odrzucone lub nieosiągalne dostarczenia webhooków. |
| `organize_files_automation_webhook_dead_letter_depth` | Wiersze czekające w tej chwili w pliku niedostarczonych webhooków. |
| `organize_files_automation_log_retention_pruned_total` | Dzienniki uruchomień usunięte przez zasady przechowywania. |
| `organize_files_automation_runs_index_compacted_total` | Wiersze wycofane z indeksu uruchomień przy zagęszczaniu. |
| `organize_files_automation_last_due_pass_exit_code` | Kod wyjścia ostatnio zakończonego przebiegu. `0` oznacza przebieg czysty. |
| `organize_files_automation_last_due_pass_completed_utc` | Czas Unix w sekundach ostatnio zakończonego przebiegu, a `0` przed pierwszym. |

## Pulpit i reguły alarmów

Gotowy pulpit Grafana publikowany jest wraz z plikami wdrożeniowymi jako `grafana-organize-files-automation.json`, pod tytułem **OrganizeFiles Automation**. Jego dziesięć paneli pokazuje należne przebiegi, zadania rozpoczęte i nieudane, konflikty zastrzeżenia, przepustowość zadań w ciągu godziny, ostatni kod wyjścia, głębokość niedostarczonych wiadomości, błędy webhooków w ciągu doby, zadania czekające na zatwierdzenie i zdarzenia zadań według stanu. Każdy panel nazywa swoje źródło danych symbolem zastępczym `${DS_PROMETHEUS}`.

Odpowiadające reguły alarmów to `alerts-organize-files-automation.yaml`, z `prometheus-rule-automation.yaml` jako powłoką Kubernetes dla `kube-prometheus-stack`. Ostatni kod wyjścia różny od zera ostrzega po pięciu minutach, błąd licencji jest krytyczny po jednej minucie, a pozostałe reguły obejmują nieudane zadania, konflikty zastrzeżenia, błędy webhooków, zator niedostarczonych wiadomości i zatwierdzenia czekające dobę. Oba pliki są sprawdzane przy każdej kompilacji, więc powyższe nazwy dotrzymują kroku licznikom.

# Wyjście przebiegu i metryki

## Wiersz stanu

Obszar **Wyjście przebiegu** pokazuje:

- Bieżący stan aplikacji i postęp silnika.
- **CPU** i dwie wartości **pamięci** tylko dla tego procesu.
- Wiersze **GPU**, w systemie Windows: udział tego procesu w każdej karcie graficznej, a nie cała karta.

Ten sam kompaktowy pasek zasobów jest ponownie wykorzystywany w oknach narzędzi dodatkowych, takich jak eksploracja plików, zaplanowane zadania i naprawa plików.

## Etykiety pamięci

- **Prywatne bajty / zatwierdzenie** — prywatna pamięć wirtualna zarezerwowana przez proces.
- **Zestaw roboczy / pamięć** — rezydentna pamięć RAM aktualnie przechowywana przez ten proces. Może różnić się od monitora innego systemu operacyjnego, ponieważ każdy system operacyjny i środowisko graficzne przetwarzają pamięć inaczej.

## Uruchom puls JSON (opcjonalnie)

Włącz opcję **Zapis pulsu JSON** w obszarze **Zaawansowane / Diagnostyka**. Silnik zapisuje `Organize.Files.run.json` pod `Output\_OrganizeMediaLogs` (ten sam folder, w którym znajduje się domyślny plik wznawiania organizacji).

- **Ścieżka** — aktualizowana atomowo podczas porządkowania i naprawy.
- **Odstępy czasu** — podczas przeglądania źródeł plik jest przepisywany co 10 000 obejrzanych plików, co 5000 dopasowań i mniej więcej co 15 sekund, dopóki przeglądanie trwa, więc duże drzewo sieciowe, które wolno się listuje, i tak pokazuje, że uruchomienie żyje. Podczas sprawdzania, haszowania i przenoszenia jest przepisywany po każdych 1000 plikach, najwyżej co 5 sekund. Zapis na początku i na końcu nadal następuje, gdy uruchomienie się zaczyna i kończy.
- **Postęp** — dopóki liczba plików wciąż rośnie, główny pasek postępu pokazuje pliki obejrzane do tej pory zamiast 100%, dopóki etap nie pozna swojej sumy.
- **Pola** — `schema`, `mode`, `phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`), `runState` (`active` / `completed` / `failed` / `cancelled`), `utc` (ISO-8601), `dryRun`, `outputRoot`, `validateMedia`, Liczniki `deepVideoValidate`, `gpuDeviceCount`, `hwaccel`, opcjonalnie `correlationId`, zagnieżdżone liczniki `progress`.
- **Log** — panel wyjściowy wydruku drukuje pełną ścieżkę na początku i na końcu po zapisaniu pliku. Użyj opcji **Otwórz folder dziennika pulsu** / **Pokaż plik JSON pulsu** w obszarze Zaawansowane / Diagnostyka.
- **CLI** — `--heartbeat-json` na OrganizeFiles.Cli. Anuluj i krytyczne błędy powłoki zapisz `cancelled` / `failed` `runState`, gdy są włączone.
