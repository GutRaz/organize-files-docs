# 容器 — 设置

## 需要什么

只有 `docker` 或 `kubectl` 程序必须在运行作业的计算机上可访问。不需要其他任何东西。 Docker Desktop 不是必需的。 Linux 上的 Docker Engine、Rancher Desktop、colima 和具有 docker 兼容命令的 Podman 都以相同的方式工作，因为应用程序只是运行它在系统路径上找到的命令。

Kubernetes 的工作原理是一样的。支持可通过 `kubectl` 访问的任何集群，包括 k3s、kind、minikube 和托管集群（例如 EKS、GKE 或 AKS）。

## 使用不同的守护进程或集群

要将作业发送到另一个 Docker 守护进程，请设置 `DOCKER_HOST` 或使用 `docker context use` 进行切换。要使用另一个 Kubernetes 集群，请使用 `kubectl config use-context` 切换当前上下文。该应用程序遵循命令行已使用的任何内容，因此应用程序内部不需要额外的设置。

## 文件挂载的位置

对于 Kubernetes，该文件夹通过两种方式之一附加。本地开发上下文可以直接安装主机文件夹。其中涵盖名为 `desktop`、`colima` 或 `orbstack` 的上下文、以 `@desktop` 结尾的上下文、以 `kind-`、`minikube` 或 `k3d-` 开头的上下文，以及名称包含 `docker-desktop`、`docker-for-desktop` 或 `rancher-desktop` 的上下文。每个其他上下文都被视为真正的集群，并获得持久卷声明，因为真正的集群节点无法看到桌面计算机上的文件夹。将 `ORGANIZE_FILES_K8S_VOLUME_MODE` 设置为 `pvc` 或 `hostpath` 会覆盖所有上下文的这一选择。

## Windows 上的网络文件夹

Windows 上的 Docker Desktop 无法将 `\\server\share` 等网络路径附加到 Linux 容器。 Windows 可以看到该文件夹，但容器看不到。有两种方法可以解决这个问题。使用本地磁盘上的文件夹，或者改用应用程序目标运行作业，这会在应用程序本身中完成工作。映射到该共享的驱动器号也无济于事，因为应用程序会顺着它找回网络路径，并同样拒绝它。

## 现成的文件

Linux 命令行工具包的 `containers` 文件夹中带有现成的文件：一个直接用工具包本身构建镜像的 Dockerfile、一个 Compose 示例、若干 Kubernetes Job 示例，以及 `containers/README.md`，旁边还有每种语言的 README。

# 容器和 CLI 工作人员

## 计划作业 — Docker 和 Kubernetes 目标

从主窗口侧边栏打开**作业**。单击现有卡上的“**新任务**”或“**编辑**”。在 **目标** 下拉列表中选择 **Docker 命令** 或 **Kubernetes 作业**。

1. 设置 **来源**（主机路径）和 **Output**（主机路径 — 在作业运行之前必须已存在）。
2. 与任何其他作业一样，选择 **模式** 和 **运行选项**。
3. **命令预览**面板显示将应用的确切“docker run”命令或 Kubernetes 作业 YAML。
4. **保存**作业并设置**时间表**，或单击卡上的**立即运行**以立即开始。

该应用程序从保存的快照自动生成安装标志和卷路径。 Docker 守护进程或“kubectl”必须在主机上可访问。 **预检** 在运行开始之前检查连接并在作业日志中报告任何错误。有关审批流程、日志检索和无头调度，请参阅**计划作业**。

## 宿主机终端 (PowerShell / bash / cmd)

可以——在宿主机上通过 PowerShell、bash 或 cmd 运行 **OrganizeFiles.Cli**，这是受支持的终端路径。Avalonia 桌面窗口是另一套图形界面。把 CLI 套件发布或安装在应用旁边（或放进 PATH），然后传入 **--source**（可重复）、**--output** 和 **--mode**。建议先做试运行，准备妥当后再加上 **--execute**。

## 桌面图形界面与容器

容器和自动化：Avalonia 桌面 GUI 并不意味着在典型的无头 Linux 容器内运行。对于一项或多项独立作业（包括多个并行工作程序），请使用 OrganizeFiles.Cli 配套工具：在每个容器中以只读方式安装源文件夹，以用于试运行预览作业。 **--execute** 的实际移动需要可写的源安装，因为引擎会将文件从源树中重新定位。使用专用的读/写输出卷，确保所有整理/修复运行（试运行和执行）的有效存储或发布者权利，传递**--source**（可重复）、**--output**和**--mode**。每个并发工作线程都需要自己的输出根。在 Docker 或 Kubernetes 作业运行之前，**Output** 文件夹必须已存在于主机上（预检会拒绝丢失的目标，并且不会创建它）。示例路径：containers/README.md 和 containers/docker-compose.sample.yml。 Jobs/JobAgent生成的`docker run`将源安装在`/in1`，`/in2`，...并在`/out`输出。手动单源示例可以使用`/in`（请参阅containers/README.md）。
