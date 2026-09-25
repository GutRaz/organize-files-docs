# Kontainer — penyiapan

## Apa yang diperlukan

Hanya program `docker` atau `kubectl` yang harus dapat dijangkau di mesin yang menjalankan pekerjaan tersebut. Tidak ada lagi yang diperlukan. Docker Desktop bukanlah suatu keharusan. Docker Engine di Linux, Rancher Desktop, colima, dan Podman dengan perintah yang kompatibel dengan Docker semuanya bekerja dengan cara yang sama, karena aplikasi hanya menjalankan perintah yang ditemukan di jalur sistem.

Kubernetes bekerja dengan cara yang sama. Semua cluster yang dapat dijangkau melalui `kubectl` didukung, termasuk k3s, kind, minikube, dan cluster terkelola seperti EKS, GKE, atau AKS.

## Menggunakan daemon atau cluster yang berbeda

Untuk mengirim pekerjaan ke daemon Docker lain, atur `DOCKER_HOST` atau ganti dengan `docker context use`. Untuk menggunakan cluster Kubernetes lain, alihkan konteks saat ini dengan `kubectl config use-context`. Aplikasi ini mengikuti apa pun yang sudah digunakan baris perintah, jadi tidak diperlukan pengaturan tambahan di dalam aplikasi.

## Tempat file dipasang

Untuk Kubernetes, folder dilampirkan dengan salah satu dari dua cara berikut. Konteks pengembangan lokal mendapatkan pemasangan folder host langsung. Itu mencakup konteks bernama `desktop`, `colima`, atau `orbstack`, konteks yang berakhir dengan `@desktop`, konteks yang dimulai dengan `kind-`, `minikube`, atau `k3d-`, dan konteks yang namanya mengandung `docker-desktop`, `docker-for-desktop`, atau `rancher-desktop`. Setiap konteks lainnya diperlakukan sebagai cluster nyata dan mendapat klaim volume persisten, karena node cluster nyata tidak dapat melihat folder di mesin desktop. Mengatur `ORGANIZE_FILES_K8S_VOLUME_MODE` ke `pvc` atau `hostpath` menimpa pilihan itu untuk setiap konteks.

## Folder jaringan di Windows

Docker Desktop di Windows tidak dapat melampirkan jalur jaringan seperti `\\server\share` ke container Linux. Windows melihat foldernya, tetapi wadahnya tidak. Ada dua cara untuk mengatasinya. Gunakan folder di disk lokal, atau jalankan pekerjaan dengan target Aplikasi, yang melakukan pekerjaan di aplikasi itu sendiri. Huruf drive yang dipetakan ke folder bersama itu tidak membantu, karena aplikasi menelusurinya kembali ke jalur jaringan dan menolaknya dengan cara yang sama.

## File siap pakai

Kit baris perintah Linux menyertakan file siap pakai di folder `containers`: sebuah Dockerfile yang membuat image dari kit itu sendiri, contoh Compose, contoh Job Kubernetes, dan `containers/README.md`, dengan README untuk setiap bahasa di sebelahnya.

# Kontainer dan worker CLI

## Pekerjaan terjadwal — Target Docker dan Kubernetes

Buka **Pekerjaan** dari sidebar jendela utama. Klik **Pekerjaan baru** atau **Ubah** pada kartu yang ada. Di tarik-turun **Sasaran** pilih **Perintah Docker** atau **Pekerjaan Kubernetes**.

1. Tetapkan **Sumber** (jalur host) dan **Output** (jalur host — harus sudah ada sebelum pekerjaan dijalankan).
2. Pilih **Mode** dan **Opsi proses** seperti untuk pekerjaan lainnya.
3. Panel **Pratinjau perintah** menampilkan perintah `docker run` atau Kubernetes Job YAML yang akan diterapkan.
4. **Simpan** pekerjaan dan tetapkan **Jadwal**, atau klik **Jalankan sekarang** pada kartu untuk segera memulai.

Aplikasi ini menghasilkan tanda pemasangan dan jalur volume secara otomatis dari snapshot yang disimpan. Daemon Docker atau `kubectl` harus dapat dijangkau di mesin host. **Preflight** memeriksa konektivitas dan melaporkan kesalahan apa pun di log pekerjaan sebelum proses dimulai. Untuk alur persetujuan, pengambilan log, dan penjadwalan headless, lihat **Tugas terjadwal**.

## Terminal mesin induk (PowerShell / bash / cmd)

Ya — pada mesin induk jalankan **OrganizeFiles.Cli** dari PowerShell, bash, atau cmd. Itulah jalur terminal yang didukung. Jendela desktop Avalonia adalah antarmuka grafis tersendiri. Terbitkan atau pasang perangkat CLI di samping aplikasi (atau pada PATH), lalu berikan **--source** (boleh berulang), **--output**, dan **--mode**. Sebaiknya mulai dengan simulasi. Tambahkan **--execute** hanya bila sudah siap.

## Antarmuka desktop dan kontainer

Kontainer dan otomatisasi: GUI desktop Avalonia tidak dimaksudkan untuk dijalankan di dalam kontainer Linux headless pada umumnya. Untuk satu atau lebih pekerjaan terisolasi, termasuk beberapa pekerja paralel, gunakan pendamping OrganizeFiles.Cli: di setiap kontainer pasang folder sumber hanya-baca untuk pekerjaan pratinjau simulasi. Perpindahan nyata dengan **--execute** memerlukan pemasangan sumber yang dapat ditulis karena mesin memindahkan file keluar dari pohon sumber. Gunakan volume keluaran baca/tulis khusus, pastikan hak penyimpanan atau penerbit yang valid untuk semua proses pengorganisasian/perbaikan (simulasi dan eksekusi), berikan **--source** (dapat diulang), **--output**, dan **--mode**. Setiap pekerja secara bersamaan membutuhkan akar keluarannya sendiri. Folder **Output** harus sudah ada di host sebelum pekerjaan Docker atau Kubernetes dijalankan (preflight menolak tujuan yang hilang dan tidak membuatnya). Contoh jalur: containers/README.md dan containers/docker-compose.sample.yml. Jobs/JobAgent menghasilkan `docker run` memasang sumber di `/in1`, `/in2`, … dan keluaran di `/out`. Contoh sumber tunggal manual mungkin menggunakan `/in` (lihat containers/README.md).
