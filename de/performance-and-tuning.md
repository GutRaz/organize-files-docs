# Erweitert / Diagnose

## Tuning organisieren

Erweitert/Diagnose stellt **OrganizeFilesEngine**-Optionen bereit, ohne das Hauptfenster zu überladen.

Mit den Organisationsmodi können Deduplizierung, Zielindex, eindeutige Datumsregeln, Verschiebungs- und Aufzählungsthreading, BFS-Ergänzung, Fortsetzungsdatei und zusätzliche eindeutige Wurzeln optimiert werden.

Bei der Reparatur bleiben nur das Netzwerk- und Festplatten-Voll-Wiederholungs-Timing, erkannte Grafik-Hardware-Lanes für optionale vollständige Videoprüfung, Hash-Lesepuffer und JSON-Heartbeat erhalten. Andere Felder sind für den Kontext sichtbar, aber deaktiviert.

Wenn Quellen oder Ausgaben auf den Pfaden NAS oder UNC aktiv sind, verringern Sie die Parallelität, lassen Sie die Netzwerkwiederholung aktiviert, lassen Sie die Ergänzung BFS für ungerade SMB-Bäume aktiviert und versuchen Sie den 8-MiB-Hash-Puffer, wenn das Hashing langsam ist.

# Erweitert/Diagnose – jede Option

## Über dieses Kapitel

Diese Steuerelemente sind Optionen der Engine. Desktop (Windows, macOS, Linux), Android, iOS und das Befehlszeilentool lesen dieselben Werte.

**Organisieren**-Modi verwenden alle unten aufgeführten Steuerelemente, sofern sie in der Benutzeroberfläche nicht ausgegraut sind. **Reparatur** verwendet nur Netzwerkwiederholung, Wiederholungsversuch bei voller Festplatte, erkannte Grafik-Hardware-Lanes (mit vollständiger Videoprüfung), Hash-Lesepuffer, Heartbeat-JSON, **Fortsetzungsdatei** und **Neu beginnen (Fortsetzungsdatei abschneiden)**. Andere Felder bleiben sichtbar, werden aber bei der Reparatur ignoriert.

## Netzwerkquellen (NAS / UNC)

Wenn sich Quellen oder Ausgaben auf SMB/CIFS-Freigaben, NAS-Volumes oder zugeordneten Laufwerken befinden, lesen Sie diesen Abschnitt sorgfältig durch.

- **Warum optimieren** – Thread-Anzahlen, die auf einer lokalen SSD funktionieren, können einen Filer blockieren oder überlasten.
- **Was Sie versuchen sollten** – Lassen Sie die Netzwerkwiederholung aktiviert. Verringern Sie die maximale Anzahl an Zeitüberschreitungen für das Verschieben von Threads und die Enumeration paralleler Threads. Lassen Sie den Zusatz BFS aktiviert, es sei denn, eine vollständige Zählung wurde ohne diesen Zusatz verifiziert. Probieren Sie den 8-MiB-Hash-Puffer aus, wenn das Hashing über das Netzwerk langsam ist.
- **Netzwerkwartezeit deaktivieren** – Schlägt bei vorübergehenden Netzwerkfehlern schnell fehl. Riskant bei WLAN oder stark beanspruchten Freigaben.

## Dedupe-Modus

Wie die Engine entscheidet, dass es sich bei zwei Dateien um Duplikate handelt.

| Modus | Was es tut | Wann zu verwenden | Kompromiss |
| ---- | ------------ | ----------- | --------- |
| **Hash (SHA-256)** | Liest und hasht den gesamten Inhalt jeder enthaltenen Quelldatei und gruppiert dann identische Bytes. | Stärkster praktischer Modus. Hash (SHA-256) ist für das Löschen an der Quelle erforderlich (Duplikate und problematische Dateien). | Am langsamsten bei großen Bäumen oder NAS. Kein Algorithmus sollte als absolute Garantie dargestellt werden. |
| **Größe + Zeit + Name** | Schlüssel = Größe, UTC-Ticks für den letzten Schreibvorgang, Name in Kleinbuchstaben, dann vollständige SHA-256-Überprüfung. | Konservativer Kompatibilitätsmodus für ältere Medienordner-Layouts. | Umbenannte Duplikate können übersehen werden. Niemals mit dem Löschen von Duplikaten oder problematischen Dateien verwenden. |
| **Keine** | Keine dateiübergreifende Deduplizierung. | Nur Sortieren, keine Duplikatbereinigung. | Duplikate bleiben in den Quellen. |

## Zielindex überspringen

- **Aus (Standard)** – Scannt die vorhandene **Eindeutige**-Ausgabe und indiziert sie vor dem Hashing. Sicherer bei Wiederverwendung desselben Ausgabeordners.
- **Ein** – Überspringt diesen Scan.
- **Vorteil** – Schneller bei großen Ausgabebäumen.
- **Risiko** – Bei Unique können mehr doppelte Inhalte landen.

## Min. Jahr für Eindeutige

Mindestkalenderjahr für Datumsordner unter **Unique** in Medienlayouts. **Warum** – Verhindert die Verteilung sehr alter Dateien in Ordner mit ungeraden Jahren, wenn die Metadaten falsch sind.

## Threads verschieben

Parallele Dateiverschiebungen, nachdem Ziele reserviert wurden.

- **Höher** – Schneller auf lokaler SSD.
- **Niedriger** – Sicherer auf NAS-, USB- oder Wi-Fi-zugeordneten Laufwerken.

## Klassifizierungs- und Hash-Threads

Parallele Worker beim Quell-Scan und beim SHA-256-Dedupe.

- **Klassifizierungs-Threads** — Dateisuche und Klassifizierung. CLI: `--classify-threads <n>`.
- **Hash-Threads** — Worker für das Hashen von Inhalten. CLI: `--hash-threads <n>`.
- **Überschreibungen** — Manuelle Werte überschreiben die Vorgaben des Organisationsprofils (`--profile`).

## Max. parallele Aufzählung

Limit für die parallele Verzeichnisauflistung während des Scans.

- **0** = Motor automatisch.
- **Niedriger** – Weniger Druck auf KMU, wenn viele Ordner gleichzeitig aufgelistet werden.

## Ergänzung BFS-Verzeichnisdurchlauf

- **Ein (Standard)** — Ein zusätzlicher flacher Durchlauf in die Breite.
- **Warum** — Manche NAS-Pfade oder tiefe Bäume wirken nach dem ersten Durchlauf unvollständig.
- **Aus** — Erst nachdem eine vollständige Dateizahl ohne ihn bestätigt wurde.
- **CLI** — `--no-bfs` schaltet diesen Durchlauf ab.

## Statusdatei fortsetzen Optionaler

UTF-8-Pfad. Erfolgreiche Verschiebungen hängen `B64|`-Zeilen an, sodass beim nächsten Organisationslauf fertige Quellen übersprungen werden können.

- **Warum** – Setzen Sie lange Jobs nach einem Stopp oder Absturz fort.
- **Standardpfad** – Wenn das Feld zur Laufzeit leer ist, verwendet die Engine `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt`. Ohne Ausgabe wird `sessions\<id>\resume\OrganizeFiles.resume.txt` unter dem App-Profil verwendet.
- **Desktop-Benutzeroberfläche** – Schreibgeschützte Pfadliste für Mausauswahl und Kopieren. Wenn am Standardspeicherort bereits eine Fortsetzungsdatei vorhanden ist, wird der Pfad automatisch angezeigt. **Durchsuchen** wählt einen Protokollordner aus und hängt `OrganizeFiles.resume.txt` an. **Entfernen** löscht den Pfad. Wenn der Hinweis leer ist, wird der zur Laufzeit verwendete Pfad angezeigt.

## Neu starten

Schneidet die Fortsetzungsdatei ab, wenn ein **echter** Organisationslauf startet (der Probelauf wird nicht abgeschnitten). Mit **Fortschritt und Arbeitsbereich speichern** wird auch der gespeicherte UI-Snapshot beim Start der Ausführung gelöscht. **Warum** – Erzwingen Sie eine vollständige Neuzählung, anstatt ein altes Fortsetzungsdateiprotokoll fortzusetzen.

## Zusätzliche eindeutige

Ein Ordner je Zeile: zusätzliche **Unique**-Bäume zum Indexieren (altes Layout, anderer Datenträger).

- **Warum** — Das Dedupe sieht Dateien, die anderswo bereits geordnet wurden, ohne sie erneut zu verschieben.
- **Desktopoberfläche** — Schreibgeschützte Liste zum zeilenweisen Kopieren. **Hinzufügen** hängt einen gewählten Ordner an. **Entfernen** löscht die gewählte Zeile (etwa einen alten `Uniques`-Baum auf einem NAS).

## Netzwerkwiederholung (Sekunden) /

Netzwerkwartezeit deaktivieren Sekunden, um vorübergehende Netzwerk-E/A erneut zu versuchen.

- **Warum** – SMB-Filer brechen Leerlaufsitzungen ab. Wird zum Organisieren und Reparieren verwendet.
- **Netzwerkwartezeit deaktivieren** – Hören Sie auf zu warten und schlagen Sie stattdessen fehl.

## Wiederholungsversuch „Festplatte voll“

(Sekunden) / Warten auf

„Festplatte voll“ deaktivieren. Gleiches Muster, wenn auf dem Ausgabevolume nicht mehr genügend Speicherplatz vorhanden ist. **Warum** – Zeit, bei langen Läufen Speicherplatz freizugeben.

## Spuren der Grafikhardware

Nur wenn die eingebaute **vollständige Videoprüfung** eingeschaltet ist und **Erkannte Grafikhardware verwenden** ebenfalls. Ein Wert über **0** setzt eine feste Spurenzahl für die gleichzeitige Prüfung über die erkannten Hersteller hinweg (NVIDIA, AMD, Intel, Apple, mobil). **0** heißt, die Spurenzahl wird selbst ermittelt. Es heißt nicht nur Prozessor. Für Stichproben allein auf dem Prozessor wählen Sie in der Liste der Grafikkarten **Nur Prozessor**. Spurenmarken planen die Bitstromprüfung auf dem Prozessor. Sie rufen die Hardware-Videodekodierung des Betriebssystems nicht auf.

- **Voreinstellung auf der Befehlszeile** — `--hwaccel <value>` wählt eine Voreinstellung für Prüfspuren (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`), wenn die vollständige Videoprüfung läuft.

## Hash-Lesepuffer

Pro-Worker-Lesepuffer beim Hashing (512 KiB, 1 MiB, 8 MiB). **Warum** – Größere Puffer helfen, wenn ein NAS oder eine Freigabe mit hoher Latenz langsam antwortet.

## Rückgängig-Journal aufzeichnen

Optionales JSONL-Journal der Verschiebungen unter dem Ausgabestamm für den Lauf.

- **Warum** — Ermöglicht das CLI-Rückgängigmachen nach einem echten Organisationslauf.
- **Archiv** — Das Archiv nach dem Organisieren bleibt aus, solange das Rückgängig-Journal aktiv ist.
- **CLI** — `--record-undo-journal` (entspricht dem Kontrollkästchen im Hauptfenster).

## Laufendes JSON zum Lauf schreiben

Schreibt die optionale Datei `Organize.Files.run.json` unter `Output\_OrganizeMediaLogs`.

- **Warum** — Fremde Werkzeuge können während des Organisierens oder Reparierens laufende Zähler lesen (durchsucht, geplant, fertig).
- **Zeitabstände** — Nach je 10.000 gesehenen Dateien, je 5.000 Treffern und etwa alle 15 Sekunden beim Quelldurchlauf, nach je 1.000 Dateien und höchstens alle 5 Sekunden bei Prüfung, Hashing und Verschiebungen und bei jeder großen Phase.
