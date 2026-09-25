# CLI, Docker i Kubernetes (układ referencyjny)

## Automatyzacja CLI

W tym rozdziale zastosowano styl Microsoft/HashiCorp: linia użycia, tabela flag (tokeny angielskie), a następnie przykłady typu „kopiuj i wklej”.

Interfejs wiersza polecenia (OrganizeFiles.Cli)
  ZASTOSOWANIE: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  ZASTOSOWANIE: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Flaga (długa) | Znaczenie
  ------------------------|------------------------------------------------------
  --execute | Prawdziwe ruchy (domyślnie jest to tylko próba próbna).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | Plik wznawiania UTF-8 z wierszami B64|.
  --delete-duplicates | Usuń zduplikowanych kandydatów (wymaga --confirm-delete z --execute).
  --delete-issues | Usuń kandydatów z zasobnika problemów (wymaga --confirm-delete z --execute). Nie w przypadku zdalnych celów automatyzacji.
  --archive-after-organize | Po uporządkowaniu: plik ZIP rodzeństwa dla poszczególnych plików, następnie usuń oryginały (wymaga --confirm-delete z --execute). Pomija już archiwalne rozszerzenia.

  **Uwaga:** CLI `--mode models` wybiera **modele CAD/3D**, a nie artefakty AI. Użyj `--mode ai` lub `--mode models-ai` dla AI / ML.

  Przykład (przebieg próbny, wszystkie kategorie): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Przykład (tylko przeniesienia do Unique, wykonanie): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Kompilacja: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Przebieg próbny: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  W przypadku --execute usuń :ro z uchwytu źródłowego. Zobacz containers/README.md, aby poznać reguły dotyczące wielu procesów roboczych (jeden element główny wyjściowy na proces roboczy).

Kubernetes (zadanie referencyjne)
  Źródłowe PVC tylko do odczytu są ważne w przypadku zadań próbnych. Prawdziwe ruchy z --execute wymagają zapisywalnych źródłowych PVC. Podaj ważne uprawnienia sklepu lub wydawcy dla wszystkich przebiegów organizowania/naprawy (pracy próbnej i wykonywania). Jeden Pod na drzewo wyjściowe. Minimalny wzorzec jest udokumentowany w containers/README.md wraz z przykładowym manifestem.

Postęp zadań
  Okno Zadania pokazuje postęp dla uruchomień App, CLI, Docker i Kubernetes. Etapy o znanej sumie pokazują procent. Skanowania bez sumy pozostają nieokreślone.
  Automatyzacja uruchamia proces roboczy CLI z ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 i usuwa te wiersze znaczników z widocznego dziennika. Uruchomienie CLI wykonane ręcznie nie wysyła znaczników, o ile ta zmienna nie jest ustawiona.
  Procesy robocze Docker i Kubernetes otrzymują tę samą zmienną, więc te uruchomienia również podają procent. Wartość jest odczytywana z dziennika procesu roboczego, więc pojawia się, gdy kontener lub pod zacznie zapisywać.
  --list-running i --show-run niosą pola postępu dla aktywnych zadań, gdy uruchomienie coś zgłosiło.

# Przykłady uruchomień

## Graficzny interfejs użytkownika

Dodaj **Źródła** i folder wyjściowy, wybierz tryb uruchomienia, włącz opcję **Przebieg próbny**, aby zobaczyć podgląd, a następnie naciśnij **Uruchom**. Pozostaw **Przebieg próbny** wyłączoną, aby wykonać rzeczywiste przeniesienia. Opcje usuwania wymagają potwierdzenia przed wykonaniem.

## Przykłady CLI

CLI Przebieg próbny: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
