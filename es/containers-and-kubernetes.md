# Contenedores — configuración

## ¿Qué se requiere?

Sólo el programa `docker` o `kubectl` debe ser accesible en la máquina que ejecuta el trabajo. No se necesita nada más. Docker Desktop no es un requisito. Docker Engine en Linux, Rancher Desktop, colima y Podman con un comando compatible con Docker funcionan de la misma manera, porque la aplicación simplemente ejecuta el comando que encuentra en la ruta del sistema.

Kubernetes funciona igual. Se admite cualquier clúster al que se pueda acceder a través de `kubectl`, incluidos k3s, kind, minikube y clústeres administrados como EKS, GKE o AKS.

## Usando un demonio o clúster diferente

Para enviar trabajos a otro demonio Docker, configure `DOCKER_HOST` o cambie con `docker context use`. Para utilizar otro clúster de Kubernetes, cambie el contexto actual con `kubectl config use-context`. La aplicación sigue lo que ya usa la línea de comando, por lo que no se necesita ninguna configuración adicional dentro de la aplicación.

## Dónde se montan los archivos

Para Kubernetes, la carpeta se adjunta de dos maneras. Los contextos de desarrollo local obtienen un montaje directo de la carpeta del host. Esto cubre un contexto denominado `desktop`, `colima` o `orbstack`, uno que termina en `@desktop`, uno que comienza con `kind-`, `minikube` o `k3d-`, y uno cuyo nombre contiene `docker-desktop`, `docker-for-desktop` o `rancher-desktop`. Cualquier otro contexto se trata como un clúster real y, en su lugar, obtiene una reclamación de volumen persistente, porque un nodo de clúster real no puede ver las carpetas en la máquina de escritorio. Establecer `ORGANIZE_FILES_K8S_VOLUME_MODE` en `pvc` o `hostpath` anula esa elección para cada contexto.

## Carpetas de red en Windows

Docker Desktop en Windows no puede adjuntar una ruta de red como `\\server\share` a un contenedor de Linux. Windows ve la carpeta, pero el contenedor no. Hay dos maneras de evitarlo. Utilice una carpeta en un disco local, o ejecute el trabajo con el destino de la aplicación, que hace el trabajo en la propia aplicación. Una letra de unidad asignada al recurso compartido no sirve, porque la aplicación la sigue hasta la ruta de red y la rechaza igual.

## Archivos listos para usar

Los kits de línea de comandos para Linux traen archivos listos en su carpeta `containers`: un Dockerfile que crea la imagen a partir del propio kit, un ejemplo de Compose, ejemplos de Job de Kubernetes y `containers/README.md`, con un README para cada idioma al lado.

# Contenedores y workers CLI

## Trabajos programados: objetivos de Docker y Kubernetes

Abra **Trabajos** desde la barra lateral de la ventana principal. Haga clic en **Nueva tarea** o **Editar** en una tarjeta existente. En el menú desplegable **Destino**, seleccione **Comando Docker** o **trabajo de Kubernetes**.

1. Configure **Orígenes** (rutas de host) y **Salida** (ruta de host, que ya debe existir antes de que se ejecute el trabajo).
2. Elija **Modo** y **Opciones de ejecución** como para cualquier otro trabajo.
3. El panel **Vista previa del comando** muestra el comando exacto `docker run` o el trabajo YAML de Kubernetes que se aplicará.
4. **Guarde** el trabajo y establezca una **Programación**, o haga clic en **Ejecutar ahora** en la tarjeta para comenzar de inmediato.

La aplicación genera automáticamente los indicadores de montaje y las rutas de volumen a partir de la instantánea guardada. Se debe poder acceder al demonio Docker o `kubectl` en la máquina host. **Comprobación previa** comprueba la conectividad e informa cualquier error en el registro del trabajo antes de que comience la ejecución. Para conocer el flujo de aprobación, la recuperación de registros y la programación autónoma, consulte **Tareas programadas**.

## Terminal del equipo anfitrión (PowerShell / bash / cmd)

Sí — en el equipo anfitrión ejecute **OrganizeFiles.Cli** desde PowerShell, bash o cmd. Esa es la vía de terminal admitida. La ventana de escritorio de Avalonia es una interfaz gráfica aparte. Publique o instale el kit de la CLI junto a la aplicación (o en PATH) y pase **--source** (repetible), **--output** y **--mode**. Conviene empezar con una simulación. Añada **--execute** solo cuando esté listo.

## Interfaz de escritorio y contenedores

Contenedores y automatización: la GUI de escritorio de Avalonia no está diseñada para ejecutarse dentro de un contenedor típico de Linux headless. Para uno o más trabajos aislados, incluidos varios trabajadores paralelos, utilice el complemento OrganizeFiles.Cli: en cada contenedor, monte las carpetas de origen de solo lectura para trabajos de vista previa de prueba. Los movimientos reales con **--execute** requieren un montaje de fuente grabable porque el motor reubica archivos fuera del árbol de fuentes. Utilice un volumen de salida de lectura/escritura dedicado, garantice un derecho válido de tienda o editor para todas las ejecuciones de organización/reparación (ejecución de prueba y ejecución), pase **--source** (repetible), **--output** y **--mode**. Cada trabajador concurrente necesita su propia raíz de salida. La carpeta **Output** ya debe existir en el host antes de que se ejecuten los trabajos de Docker o Kubernetes (la verificación previa rechaza un destino faltante y no lo crea). Rutas de ejemplo: containers/README.md y containers/docker-compose.sample.yml. Jobs/JobAgent generado `docker run` monta fuentes en `/in1`, `/in2`,… y salida en `/out`. Los ejemplos manuales de fuente única pueden usar `/in` (ver containers/README.md).
