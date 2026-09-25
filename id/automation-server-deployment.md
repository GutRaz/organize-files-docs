# CLI, Docker, dan Kubernetes (tata letak referensi)

## Otomatisasi CLI

Bab ini mengikuti gaya Microsoft/HashiCorp: baris penggunaan, tabel bendera (token bahasa Inggris), lalu contoh salin-tempel.

CLI (OrganizeFiles.Cli)
  PENGGUNAAN: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  PENGGUNAAN: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Bendera (panjang) | Artinya
  -------------------------|----------------------------------------
  --execute | Pergerakan nyata (defaultnya hanya simulasi).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | File resume UTF-8 dengan B64| garis.
  --delete-duplicates | Hapus kandidat duplikat (membutuhkan --confirm-delete dengan --execute).
  --delete-issues | Hapus kandidat keranjang masalah (membutuhkan --confirm-delete dengan --execute). Bukan pada target otomatisasi jarak jauh.
  --archive-after-organize | Setelah mengatur: per file saudara ZIP lalu hapus yang asli (membutuhkan --confirm-delete dengan --execute). Melewati ekstensi yang sudah diarsipkan.

  **Catatan:** CLI `--mode models` memilih **model CAD / 3D**, bukan artefak AI. Gunakan `--mode ai` atau `--mode models-ai` untuk AI / ML.

  Contoh (simulasi, semua bucket): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Contoh (hanya gerakan unik, jalankan): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Membangun: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Simulasi: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  Untuk --execute, hapus :ro dari mount sumber. Lihat containers/README.md untuk aturan multi-worker (satu root keluaran per worker).

Kubernetes (referensi Pekerjaan)
  PVC sumber read-only berlaku untuk pekerjaan simulasi. Pergerakan nyata dengan --execute memerlukan PVC sumber yang dapat ditulis. Memberikan hak penyimpanan atau penerbit yang valid untuk semua proses pengorganisasian/perbaikan (simulasi dan eksekusi). Satu Pod per pohon keluaran. Pola minimal didokumentasikan di containers/README.md bersama dengan contoh manifes.

Kemajuan tugas
  Jendela Tugas menampilkan kemajuan untuk proses App, CLI, Docker, dan Kubernetes. Tahap dengan total yang diketahui menampilkan persentase. Pemindaian tanpa total tetap tidak tentu.
  Otomatisasi memulai worker CLI dengan ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 dan menghapus baris penanda itu dari log yang terlihat. Proses CLI yang dimulai secara manual tidak mengirim penanda kecuali variabel itu disetel.
  Worker Docker dan Kubernetes menerima variabel yang sama, sehingga proses tersebut juga melaporkan persentase. Angka dibaca dari log worker, sehingga muncul begitu kontainer atau pod mulai menulis.
  --list-running dan --show-run membawa bidang kemajuan untuk tugas aktif ketika proses telah melaporkan sesuatu.

# Contoh proses

## UI Grafis

Tambahkan **Sumber** dan folder keluaran, pilih mode jalan, aktifkan **Simulasi** untuk pratinjau, lalu tekan **Jalankan**. Biarkan **Simulasi** mati untuk pemindahan sebenarnya. Opsi hapus meminta konfirmasi sebelum dijalankan.

## Contoh CLI

CLI Simulasi: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
