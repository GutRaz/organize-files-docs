# Container – Einrichtung

## Was ist erforderlich

Nur das Programm `docker` oder `kubectl` muss auf dem Computer erreichbar sein, auf dem der Job ausgeführt wird. Es ist nichts anderes nötig. Docker Desktop ist keine Voraussetzung. Docker Engine unter Linux, Rancher Desktop, Colima und Podman mit einem Docker-kompatiblen Befehl funktionieren alle auf die gleiche Weise, da die App einfach den Befehl ausführt, den sie im Systempfad findet.

Kubernetes funktioniert genauso. Jeder über `kubectl` erreichbare Cluster wird unterstützt, einschließlich k3s, kind, minikube und verwalteter Cluster wie EKS, GKE oder AKS.

## Verwendung eines anderen Daemons oder Clusters

Um Jobs an einen anderen Docker-Daemon zu senden, legen Sie `DOCKER_HOST` fest oder wechseln Sie mit `docker context use`. Um einen anderen Kubernetes-Cluster zu verwenden, wechseln Sie den aktuellen Kontext mit `kubectl config use-context`. Die App folgt allem, was die Befehlszeile bereits verwendet, sodass keine zusätzlichen Einstellungen innerhalb der App erforderlich sind.

## Wo Dateien gemountet werden

Für Kubernetes wird der Ordner auf zwei Arten angehängt. Lokale Entwicklungskontexte erhalten eine direkte Bereitstellung des Hostordners. Das umfasst einen Kontext mit dem Namen `desktop`, `colima` oder `orbstack`, einen, der auf `@desktop` endet, einen, der mit `kind-`, `minikube` oder `k3d-` beginnt, und einen, dessen Name `docker-desktop`, `docker-for-desktop` oder `rancher-desktop` enthält. Jeder andere Kontext wird als echter Cluster behandelt und erhält stattdessen einen dauerhaften Volume-Anspruch, da ein echter Clusterknoten die Ordner auf dem Desktop-Computer nicht sehen kann. Wird `ORGANIZE_FILES_K8S_VOLUME_MODE` auf `pvc` oder `hostpath` gesetzt, ersetzt das diese Wahl für jeden Kontext.

## Netzwerkordner unter Windows

Docker Desktop unter Windows kann einen Netzwerkpfad wie `\\server\share` nicht an einen Linux-Container anhängen. Windows erkennt den Ordner, der Container jedoch nicht. Es gibt zwei Möglichkeiten, dies zu umgehen. Verwenden Sie einen Ordner auf einer lokalen Festplatte oder führen Sie den Job stattdessen mit dem App-Ziel aus, das die Arbeit in der App selbst erledigt. Ein Laufwerksbuchstabe, der mit der Freigabe verbunden ist, hilft nicht, denn die App verfolgt ihn bis zum Netzwerkpfad zurück und lehnt ihn genauso ab.

## Vorgefertigte Dateien

Die Linux-Befehlszeilen-Kits enthalten im Ordner `containers` fertige Dateien: ein Dockerfile, das das Image aus dem Kit selbst baut, ein Compose-Beispiel, Kubernetes-Job-Beispiele und `containers/README.md`, daneben eine README für jede Sprache.

# Container und CLI-Worker

## Geplante Aufgaben – Docker- und Kubernetes-Ziele

Öffnen Sie **Aufgaben** in der Seitenleiste des Hauptfensters. Klicken Sie auf einer vorhandenen Karte auf **Neue Aufgabe** oder **Bearbeiten**. Wählen Sie im Dropdown-Menü **Ziel** den **Docker-Befehl** oder **Kubernetes-Job** aus.

1. Legen Sie **Quellen** (Hostpfade) und **Ausgabe** (Hostpfad – muss bereits vorhanden sein, bevor die Aufgabe ausgeführt wird) fest.
2. Wählen Sie **Modus** und **Ausführungsoptionen** wie bei jeder anderen Aufgabe.
3. Im Bereich **Befehlsvorschau** wird der genaue „Docker Run“-Befehl oder Kubernetes-Job-YAML angezeigt, der angewendet wird.
4. **Speichern** Sie die Aufgabe und legen Sie einen **Zeitplan** fest oder klicken Sie auf der Karte auf **Jetzt ausführen**, um sofort zu starten.

Die App generiert die Mount-Flags und Volume-Pfade automatisch aus dem gespeicherten Snapshot. Der Docker-Daemon oder „kubectl“ muss auf dem Host-Computer erreichbar sein. **Preflight** prüft die Konnektivität und meldet etwaige Fehler im Jobprotokoll, bevor die Ausführung beginnt. Informationen zum Genehmigungsablauf, zum Protokollabruf und zur Headless-Planung finden Sie unter **Geplante Aufgaben**.

## Terminal des Hostrechners (PowerShell / bash / cmd)

Ja — auf dem Hostrechner **OrganizeFiles.Cli** aus PowerShell, bash oder cmd starten. Das ist der unterstützte Weg über ein Terminal. Das Avalonia-Desktopfenster ist eine eigene grafische Oberfläche. Veröffentlichen oder installieren Sie das CLI-Paket neben der Anwendung (oder in PATH) und übergeben Sie dann **--source** (wiederholbar), **--output** und **--mode**. Beginnen Sie besser mit einem Testlauf. **--execute** erst hinzufügen, wenn alles bereit ist.

## Desktop-GUI und Container

Container und Automatisierung: Die Avalonia-Desktop-GUI ist nicht für die Ausführung in einem typischen Headless-Linux-Container gedacht. Verwenden Sie für einen oder mehrere isolierte Jobs, einschließlich mehrerer paralleler Worker, den OrganizeFiles.Cli-Begleiter: Mounten Sie in jedem Container Quellordner, die nur für Probelauf-Vorschaujobs schreibgeschützt sind. Echte Verschiebungen mit **--execute** erfordern einen beschreibbaren Quell-Mount, da die Engine Dateien aus dem Quellbaum verschiebt. Verwenden Sie ein dediziertes Lese-/Schreib-Ausgabe-Volume, stellen Sie sicher, dass für alle Organisations-/Reparaturläufe (Probelauf und Ausführung) eine gültige Speicher- oder Herausgeberberechtigung vorliegt, übergeben Sie **--source** (wiederholbar), **--output** und **--mode**. Jeder gleichzeitig arbeitende Arbeiter benötigt seinen eigenen Ausgabestamm. Der Ordner **Output** muss bereits auf dem Host vorhanden sein, bevor Docker- oder Kubernetes-Jobs ausgeführt werden (Preflight lehnt ein fehlendes Ziel ab und erstellt es nicht). Beispielpfade: containers/README.md und containers/docker-compose.sample.yml. Jobs/JobAgent generiert `docker run` mountet Quellen bei `/in1`, `/in2`, … und gibt bei `/out` aus. Manuelle Single-Source-Beispiele können `/in` verwenden (siehe containers/README.md).
