# CLI, Docker y Kubernetes (diseño de referencia)

## Automatización CLI

Este capítulo sigue el estilo de Microsoft/HashiCorp: línea de uso, tabla de indicadores (tokens en inglés) y luego ejemplos de copiar y pegar.

CLI (OrganizeFiles.Cli)
  USO: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  USO: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Bandera (larga) | Significado
  -------------------------|----------------------------------------
  --execute | Movimientos reales (el valor predeterminado es solo ejecución de prueba).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | UTF-8 archivo de reanudación con B64| pauta.
  --delete-duplicates | Elimine candidatos duplicados (necesita --confirm-delete con --execute).
  --delete-issues | Elimine los candidatos al depósito de problemas (necesita --confirm-delete con --execute). No en objetivos de automatización remota.
  --archive-after-organize | Después de organizar: ZIP hermano por archivo, luego elimine los originales (necesita --confirm-delete con --execute). Omite las extensiones que ya están archivadas.

  **Nota:** CLI `--mode models` selecciona **modelos CAD/3D**, no artefactos de IA. Utilice `--mode ai` o `--mode models-ai` para AI/ML.

  Ejemplo (ejecución de prueba, todos los depósitos): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Ejemplo (solo traslados a Unique, ejecutar): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Compilación: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Ejecución de prueba: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  Para --execute, elimine :ro del montaje de origen. Consulte containers/README.md para conocer las reglas para varios workers (una raíz de salida por worker).

Kubernetes (trabajo de referencia)
  Los PVC de origen de sólo lectura son válidos para trabajos de prueba. Los movimientos reales con --execute necesitan PVC de fuente grabable. Proporcione un derecho válido de tienda o editor para todas las ejecuciones de organización/reparación (ejecución de prueba y ejecución). Un Pod por árbol de salida. Un patrón mínimo está documentado en containers/README.md junto con un manifiesto de muestra.

Progreso de trabajos
  La ventana Trabajos muestra el progreso de las ejecuciones App, CLI, Docker y Kubernetes. Las etapas con un total conocido muestran un porcentaje. Los escaneos sin total permanecen indeterminados.
  La automatización inicia el proceso de trabajo CLI con ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 y elimina esas líneas de marca del registro visible. Una ejecución CLI iniciada a mano no emite marcas a menos que esa variable esté definida.
  Los procesos de trabajo de Docker y Kubernetes reciben la misma variable, por lo que esas ejecuciones también informan un porcentaje. La cifra se lee del registro del proceso de trabajo, así que aparece en cuanto el contenedor o el pod empieza a escribir.
  --list-running y --show-run llevan campos de progreso para los trabajos activos cuando la ejecución ha informado algo.

# Ejemplos de ejecución

## Interfaz de usuario gráfica

Añade **Orígenes** y la carpeta de salida, elige el modo de ejecución, activa **Ejecución de prueba** para una vista previa y pulsa **Ejecutar**. Deja **Ejecución de prueba** sin marcar para mover de verdad. Las opciones de borrado piden confirmación antes de ejecutarse.

## Ejemplos de CLI

CLI Simulación: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
