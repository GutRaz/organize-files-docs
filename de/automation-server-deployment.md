# CLI, Docker und Kubernetes (Referenzlayout)

## CLI-Automatisierung

Dieses Kapitel folgt dem Microsoft/HashiCorp-Stil: Verwendungszeile, Flag-Tabelle (englische Token), dann Beispiele zum Kopieren und Einfügen.

CLI (OrganizeFiles.Cli)
  VERWENDUNG: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  VERWENDUNG: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Flagge (lang) | Bedeutung
  -------------------------|-------------
  --execute | Echte Bewegungen (Standard ist nur Probelauf).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | UTF-8 Fortsetzungsdatei mit B64| Linien.
  --delete-duplicates | Löschen Sie doppelte Kandidaten (erfordert --confirm-delete mit --execute).
  --delete-issues | Issue-Bucket-Kandidaten löschen (erfordert --confirm-delete mit --execute). Nicht auf Remote-Automatisierungszielen.
  --archive-after-organize | Nach dem Organisieren: Pro-Datei-Geschwister-ZIP, dann Originale löschen (erfordert --confirm-delete mit --execute). Überspringt bereits archivierte Erweiterungen.

  **Hinweis:** CLI `--mode models` wählt **CAD-/3D-Modelle** aus, keine KI-Artefakte. Verwenden Sie `--mode ai` oder `--mode models-ai` für AI/ML.

  Beispiel (Testlauf, alle Buckets): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Beispiel (nur Verschiebungen nach Unique, ausführen): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Erstellen: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Testlauf: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  Entfernen Sie für --execute :ro vom Quell-Mount. Siehe containers/README.md für Multi-Worker-Regeln (ein Ausgabestamm pro Worker).

Kubernetes (Referenzjob)
  Für Probelaufaufträge sind schreibgeschützte Quell-PVCs gültig. Echte Bewegungen mit --execute erfordern beschreibbare Quell-PVCs. Stellen Sie für alle Organisations-/Reparaturläufe (Probelauf und Ausführung) eine gültige Store- oder Publisher-Berechtigung bereit. Ein Pod pro Ausgabebaum. Ein minimales Muster ist in containers/README.md zusammen mit einem Beispielmanifest dokumentiert.

Auftragsfortschritt
  Das Aufträge-Fenster zeigt den Fortschritt für App-, CLI-, Docker- und Kubernetes-Läufe. Phasen mit bekanntem Gesamtwert zeigen einen Prozentsatz. Scans ohne Gesamtwert bleiben unbestimmt.
  Die Automatisierung startet den CLI-Worker mit ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 und entfernt diese Markierungszeilen aus dem sichtbaren Protokoll. Ein von Hand gestarteter CLI-Lauf gibt keine Markierungen aus, solange diese Variable nicht gesetzt ist.
  Docker- und Kubernetes-Worker erhalten dieselbe Variable, daher melden diese Läufe ebenfalls einen Prozentsatz. Der Wert wird aus dem Protokoll des Workers gelesen und erscheint, sobald der Container oder der Pod zu schreiben beginnt.
  --list-running und --show-run führen Fortschrittsfelder für aktive Aufträge, sobald der Lauf etwas gemeldet hat.

# Ausführungsbeispiele

## Grafische Benutzeroberfläche

Fügen Sie **Quellen** und den Ausgabeordner hinzu, wählen Sie den Ausführungsmodus, aktivieren Sie **Testlauf** für eine Vorschau und drücken Sie dann **Ausführen**. Lassen Sie **Testlauf** für echte Verschiebungen deaktiviert. Löschoptionen erfordern vor der Ausführung eine Bestätigung.

## CLI-Beispiele

CLI Testlauf: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
