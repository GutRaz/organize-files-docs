# Containers — setup

## What is required

Only the `docker` or `kubectl` program has to be reachable on the machine that runs the job. Nothing else is needed. Docker Desktop is not a requirement. Docker Engine on Linux, Rancher Desktop, colima, and Podman with a docker-compatible command all work the same way, because the app simply runs the command it finds on the system path.

Kubernetes works the same. Any cluster reachable through `kubectl` is supported, including k3s, kind, minikube, and managed clusters such as EKS, GKE, or AKS.

## Using a different daemon or cluster

To send jobs to another Docker daemon, set `DOCKER_HOST` or switch with `docker context use`. To use another Kubernetes cluster, switch the current context with `kubectl config use-context`. The app follows whatever the command line already uses, so no extra setting is needed inside the app.

## Where files are mounted

For Kubernetes, the folder is attached in one of two ways. Local development contexts get a direct host folder mount. That covers a context named `desktop`, `colima` or `orbstack`, one ending in `@desktop`, one starting with `kind-`, `minikube` or `k3d-`, and one whose name contains `docker-desktop`, `docker-for-desktop` or `rancher-desktop`. Every other context is treated as a real cluster and gets a persistent volume claim instead, because a real cluster node cannot see the folders on the desktop machine. Setting `ORGANIZE_FILES_K8S_VOLUME_MODE` to `pvc` or `hostpath` overrides that choice for every context.

## Network folders on Windows

Docker Desktop on Windows cannot attach a network path such as `\\server\share` to a Linux container. Windows sees the folder, but the container does not. There are two ways around it. Use a folder on a local disk, or run the job with the App target instead, which does the work in the app itself. A drive letter mapped to the share does not help, because the app follows it back to the network path and refuses it the same way.

## Ready-made files

The Linux command-line kits carry ready-made files in their `containers` folder: a Dockerfile that builds the image from the kit itself, a Compose sample, Kubernetes Job samples, and `containers/README.md`, with a README in each language next to it.

# Containers and CLI workers

## Scheduled jobs — Docker and Kubernetes targets

Open **Jobs** from the main window sidebar. Click **New job** or **Edit** on an existing card. In the **Target** dropdown select **Docker command** or **Kubernetes job**.

1. Set **Sources** (host paths) and **Output** (host path — must already exist before the job runs).
2. Choose **Mode** and **Run options** as for any other job.
3. The **Command preview** panel shows the exact docker run command or Kubernetes Job YAML that will be applied.
4. **Save** the job and set a **Schedule**, or click **Run now** on the card to start immediately.

The app generates the mount flags and volume paths automatically from the saved snapshot. Docker daemon or kubectl must be reachable on the host machine. **Preflight** checks connectivity and reports any errors in the job log before the run starts. For the approval flow, log retrieval, and headless scheduling, see **Scheduled jobs**.

## Host terminal (PowerShell / bash / cmd)

Yes — on the host computer run **OrganizeFiles.Cli** from PowerShell, bash, or cmd. That is the supported terminal path. The Avalonia desktop window is a separate GUI. Publish or install the CLI kit next to the app (or on PATH), then pass **--source** (repeatable), **--output**, and **--mode**. Prefer a dry run first. Add **--execute** only when ready.

## Desktop GUI and containers

Containers and automation: the Avalonia desktop GUI is not meant to run inside a typical headless Linux container. For one or more isolated jobs, including several parallel workers, use the OrganizeFiles.Cli companion: in each container mount source folders read-only only for dry-run preview jobs. Real moves with **--execute** require a writable source mount because the engine relocates files out of the source tree. Use a dedicated read/write output volume, ensure valid store or publisher entitlement for all organize/repair runs (dry run and execute), pass **--source** (repeatable), **--output**, and **--mode**. Each concurrent worker needs its own output root. The **Output** folder must already exist on the host before Docker or Kubernetes jobs run (preflight refuses a missing destination and does not create it). Example paths: containers/README.md and containers/docker-compose.sample.yml. Jobs/JobAgent generated `docker run` mounts sources at `/in1`, `/in2`, … and output at `/out`. Manual single-source examples may use `/in`, as containers/README.md shows.
