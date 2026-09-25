# Zaawansowane / Diagnostyka

## Organizuj strojenie

Zaawansowane/Diagnostyka udostępnia opcje **OrganizeFilesEngine** bez zaśmiecania głównego panelu.

Tryby organizacji umożliwiają dostrajanie deduplikacji, indeksu docelowego, unikalnych reguł dat, wątków przenoszenia i wyliczania, uzupełniania BFS, pliku wznawiania i dodatkowych unikalnych korzeni.

Naprawa utrzymuje tylko czas ponownych prób zapełnienia sieci i dysku, wykryte ścieżki sprzętu graficznego na potrzeby opcjonalnej pełnej kontroli wideo, bufor odczytu skrótu i puls JSON. Inne pola są widoczne dla kontekstu, ale wyłączone.

Gdy źródła lub dane wyjściowe znajdują się na ścieżkach NAS lub UNC, zmniejsz równoległość, włącz ponawianie sieci, pozostaw dodatek BFS włączony dla nieparzystych drzew SMB i wypróbuj bufor mieszający 8 MiB, jeśli mieszanie jest wolne.

# Zaawansowane / Diagnostyka – każda opcja

## Informacje o tym rozdziale

Te elementy sterujące to opcje silnika. Aplikacja desktopowa (Windows, macOS, Linux), Android, iOS i narzędzie wiersza poleceń odczytują te same wartości.

Tryby **Organizuj** korzystają ze wszystkich poniższych elementów sterujących, o ile interfejs ich nie wyszarzy. **Naprawa** korzysta tylko z ponawiania prób sieciowych, ponawiania przy zapełnionym dysku, wykrytych linii sprzętu graficznego (z pełną kontrolą wideo), bufora odczytu skrótu, pulsu JSON, **Plik stanu wznowienia** i **Zacznij od nowa (skróć plik wznawiania)**. Pozostałe pola są nadal widoczne, ale podczas naprawy są ignorowane.

## Źródła sieciowe (NAS / UNC)

Jeśli źródła lub dane wyjściowe znajdują się na udziałach SMB/CIFS, woluminach NAS lub zmapowanych dyskach, przejrzyj uważnie tę sekcję.

- **Po co dostrajać** — Liczba wątków działających na lokalnym dysku SSD może spowodować zatrzymanie lub przeciążenie modułu filer.
- **Co spróbować** — Włącz ponawianie połączeń sieciowych. Niższe przenoszenie wątków i wyliczanie równoległe maksymalnie w przypadku przekroczenia limitu czasu. Pozostaw dodatek BFS włączony, chyba że bez niego zweryfikowano pełne zliczenie. Wypróbuj bufor mieszający 8 MiB, gdy mieszanie w sieci jest powolne.
- **Wyłącz oczekiwanie na sieć** — szybko kończy się niepowodzeniem w przypadku przejściowych błędów sieci. Ryzykowne w przypadku Wi-Fi lub zajętych akcji.

## Tryb dedupe

W jaki sposób silnik decyduje, że dwa pliki są duplikatami.

| Tryb | Co to robi | Kiedy używać | Kompromis |
| ---- | ------------ | ----------- | --------- |
| **Skrót (SHA-256)** | Odczytuje i miesza pełną zawartość każdego dołączonego pliku źródłowego, a następnie grupuje identyczne bajty. | Najsilniejszy tryb praktyczny. Hash (SHA-256) jest wymagany do usuwania w miejscu (duplikaty i pliki problematyczne). | Najwolniej na dużych drzewach lub NAS. Żaden algorytm nie powinien być przedstawiany jako absolutna gwarancja. |
| **Rozmiar + czas + nazwa** | Klucz = rozmiar, znaczniki ostatniego zapisu UTC, nazwa pisana małymi literami, a następnie pełna weryfikacja SHA-256. | Konserwatywny tryb zgodności dla starszych układów folderów multimediów. | Można pominąć duplikaty o zmienionych nazwach. Nigdy nie używaj przy usuwaniu duplikatów ani plików problematycznych. |
| **Brak** | Brak deduplikacji między plikami. | Tylko sortowanie, a nie czyszczenie duplikatów. | Duplikaty pozostają w źródłach. |

## Pomiń indeks miejsca docelowego

- **Wyłączone (domyślnie)** — Skanuje istniejące dane wyjściowe **Unikalne** i indeksuje je przed mieszaniem. Bezpieczniejsze przy ponownym użyciu tego samego folderu wyjściowego.
- **Włącz** — pomija to skanowanie.
- **Korzyść** — Szybciej na ogromnych drzewach wyjściowych.
- **Ryzyko** — W Unique może pojawić się więcej zduplikowanych treści.

## Min. rok dla Unikalne

Minimalny rok kalendarzowy dla folderów z datami w obszarze **Unikalny** w układach multimediów. **Dlaczego** — pozwala uniknąć rozrzucania bardzo starych plików do folderów z rokiem nieparzystym, gdy metadane są nieprawidłowe.

## Przenieś wątki

Równoległe przeniesienie pliku po zarezerwowaniu miejsc docelowych.

- **Wyższy** — Szybciej na lokalnym dysku SSD.
- **Niższy** — bezpieczniejszy na dyskach NAS, USB lub mapowanych przez Wi-Fi.

## Wątki klasyfikacji i haszowania

Równoległe wątki podczas skanowania źródeł i deduplikacji SHA-256.

- **Wątki klasyfikacji** — Wykrywanie i klasyfikacja plików. CLI: `--classify-threads <n>`.
- **Hashowe wątki** — Wątki haszujące zawartość. CLI: `--hash-threads <n>`.
- **Nadpisania** — Wartości ręczne nadpisują domyślne ustawienia profilu (`--profile`).

## Wyliczenie równoległe maks

Maksymalny limit wyświetlania katalogów równoległych podczas skanowania.

- **0** = silnik automatyczny.
- **Niższy** — Mniejsze obciążenie SMB w przypadku jednoczesnego wyświetlania wielu folderów.

## Dodatek BFS przepustka do katalogu

- **Włączone (domyślnie)** — Dodatkowe płytkie przejście wszerz.
- **Dlaczego** — Niektóre ścieżki NAS albo głębokie drzewa po pierwszym przejściu wyglądają na niepełne.
- **Wyłączone** — Dopiero po potwierdzeniu pełnej liczby plików bez niego.
- **CLI** — `--no-bfs` wyłącza to przejście.

## Wznów plik stanu

Opcjonalna ścieżka UTF-8. Pomyślne ruchy dołączają linie `B64|`, aby następne uruchomienie organizacyjne mogło pominąć gotowe źródła.

- **Dlaczego** — Kontynuuj długie zadania po zatrzymaniu lub awarii.
- **Ścieżka domyślna** — Gdy w czasie wykonywania pole jest puste, silnik używa `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt`. Bez danych wyjściowych używa `sessions\<id>\resume\OrganizeFiles.resume.txt` w profilu aplikacji.
- **Interfejs pulpitu** — Lista ścieżek tylko do odczytu do wybierania i kopiowania za pomocą myszy. Jeśli plik wznawiania już istnieje w domyślnej lokalizacji, ścieżka pojawi się automatycznie. **Przeglądaj** wybiera folder dziennika i dołącza `OrganizeFiles.resume.txt`. **Usuń** oczyszcza ścieżkę. Gdy jest pusty, wskazówka pokazuje ścieżkę używaną w czasie wykonywania.

## Rozpocznij od nowa

Obcina plik wznawiania po rozpoczęciu **prawdziwego** przebiegu organizacyjnego (przebieg próbny nie jest obcinany). Opcja **Zapisz postęp i obszar roboczy** czyści również zapisaną migawkę interfejsu użytkownika przy uruchomieniu. **Dlaczego** — Wymuś pełne przeliczenie zamiast kontynuować stary dziennik plik wznawiania.

## Dodatkowe unikalne korzenie

Jeden folder w wierszu: dodatkowe drzewa **Unique** do zaindeksowania (stary układ, inny wolumin).

- **Dlaczego** — Usuwanie duplikatów widzi pliki już uporządkowane gdzie indziej, nie przenosząc ich ponownie.
- **Interfejs pulpitu** — Lista tylko do odczytu, do kopiowania wiersz po wierszu. **Dodaj** dopisuje wskazany folder. **Usuń** kasuje zaznaczony wiersz (na przykład stare drzewo `Uniques` na NAS).

## Ponowna próba sieci (sekundy)

Sekundy, przez które ponawiać przejściowe operacje sieciowe.

- **Dlaczego** — Serwery SMB zrywają bezczynne sesje. Używane przy porządkowaniu i naprawie.
- **Wyłącz czekanie na sieć** — Przestań czekać i zamiast tego zgłoś błąd.

## Ponowna próba zapełnienia dysku

(sekundy) /

Wyłącz oczekiwanie na zapełnienie dysku

Ten sam schemat, gdy na woluminie wyjściowym zabraknie miejsca. **Dlaczego** — Czas zwolnić dysk podczas długich uruchomień.

## Pasma karty graficznej

Tylko wtedy, gdy wbudowane **pełne sprawdzanie wideo** jest włączone i **Użyj wykrytej karty graficznej** także. Wartość powyżej **0** ustala jawną liczbę pasm do równoległego sprawdzania wśród wykrytych producentów (NVIDIA, AMD, Intel, Apple, urządzenia przenośne). **0** oznacza, że liczba pasm ustala się sama. Nie oznacza to tylko procesora. Aby próbkować wyłącznie na procesorze, wybierz **Tylko CPU** na liście kart graficznych. Oznaczenia pasm planują sprawdzanie strumienia bitów na procesorze. Nie wywołują sprzętowego dekodowania wideo w systemie.

- **Ustawienie w wierszu poleceń** — `--hwaccel <value>` wybiera gotowe ustawienie pasm sprawdzania (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`), gdy trwa pełne sprawdzanie wideo.

## Bufor odczytu skrótu

Bufor odczytu przypadający na pracownika podczas mieszania (512 KiB, 1 MiB, 8 MiB). **Dlaczego** — Większe bufory pomagają, gdy NAS lub udostępnianie o dużym opóźnieniu powoli odpowiada.

## Zapisz dziennik cofania

Opcjonalny dziennik JSONL przeniesień w katalogu wyjściowym przebiegu.

- **Po co** — Umożliwia cofnięcie z poziomu CLI po rzeczywistym przebiegu.
- **Archiwum** — Archiwizacja po uporządkowaniu pozostaje wyłączona, gdy dziennik jest aktywny.
- **CLI** — `--record-undo-journal` (to samo co pole wyboru w oknie głównym).

## Zapis pulsu JSON

Zapisuje opcjonalny plik `Organize.Files.run.json` w `Output\_OrganizeMediaLogs`.

- **Dlaczego** — Zewnętrzne narzędzia mogą w trakcie porządkowania lub naprawy czytać żywe liczniki (przejrzane, zaplanowane, ukończone).
- **Odstępy czasu** — Co 10 000 obejrzanych plików, co 5000 dopasowań i mniej więcej co 15 sekund podczas przeglądania źródeł, po każdych 1000 plikach i najwyżej co 5 sekund podczas sprawdzania, haszowania i przenoszenia oraz przy każdym większym etapie.
