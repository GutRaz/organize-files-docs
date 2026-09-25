# Lanjutan / Diagnostik

## Atur penyetelan

Tingkat Lanjut / Diagnostik menampilkan opsi **OrganizeFilesEngine** tanpa mengacaukan panel utama.

Mode pengorganisasian dapat menyetel dedupe, indeks tujuan, aturan tanggal unik, threading pemindahan dan enumerasi, suplemen BFS, file resume, dan akar Unik tambahan.

Perbaikan hanya mempertahankan waktu percobaan ulang jaringan dan penuh disk, jalur perangkat keras grafis yang terdeteksi untuk pemeriksaan video penuh opsional, buffer baca hash, dan detak jantung JSON. Bidang lain terlihat untuk konteks tetapi dinonaktifkan.

Ketika sumber atau keluaran aktif di jalur NAS atau UNC, turunkan paralelisme, tetap aktifkan percobaan ulang jaringan, biarkan suplemen BFS aktif untuk pohon SMB ganjil, dan coba buffer hash 8 MiB jika hashing lambat.

# Lanjutan / Diagnostik — setiap opsi

## Tentang bab ini

Kontrol ini adalah opsi mesin. Desktop (Windows, macOS, Linux), Android, iOS, dan alat baris perintah membaca nilai yang sama.

Mode **Atur** menggunakan setiap kontrol di bawah kecuali antarmuka membuatnya abu-abu. **Perbaikan** hanya menggunakan percobaan ulang jaringan, percobaan ulang saat disk penuh, jalur perangkat keras grafis yang terdeteksi (dengan pemeriksaan video lengkap), buffer baca hash, JSON detak jantung, **File status lanjutan** dan **Mulai baru (potong file status lanjutan)**. Bidang lainnya tetap terlihat tetapi diabaikan selama perbaikan.

## Sumber jaringan (NAS / UNC)

Ketika Sumber atau Output berada pada share SMB/CIFS, volume NAS, atau drive yang dipetakan, tinjau bagian ini dengan cermat.

- **Mengapa menyetel** — Jumlah thread yang berfungsi pada SSD lokal dapat menghentikan atau membebani filer secara berlebihan.
- **Apa yang harus dicoba** — Terus aktifkan percobaan ulang jaringan. Turunkan thread perpindahan dan enum maks paralel pada batas waktu. Biarkan suplemen BFS aktif kecuali jumlah penuh telah diverifikasi tanpanya. Coba buffer hash 8 MiB ketika hashing lambat melalui jaringan.
- **Nonaktifkan tunggu jaringan** — Gagal dengan cepat pada kesalahan jaringan sementara. Berisiko pada Wi-Fi atau berbagi yang sibuk.

## Mode dedupe

Bagaimana mesin memutuskan dua file adalah duplikat.

| Modus | Apa fungsinya | Kapan menggunakan | Pertukaran |
| ---- | ------------ | ----------- | --------- |
| **Hash (SHA-256)** | Membaca dan melakukan hashing pada konten lengkap setiap file sumber yang disertakan, lalu mengelompokkan byte yang identik. | Mode praktis terkuat. Hash (SHA-256) wajib untuk penghapusan di tempat (duplikat dan berkas bermasalah). | Paling lambat di pohon besar atau NAS. Tidak ada algoritma yang dapat dijadikan sebagai jaminan mutlak. |
| **Ukuran + waktu + nama** | Kunci = ukuran, tanda centang penulisan terakhir UTC, nama dengan huruf kecil, lalu verifikasi lengkap SHA-256. | Mode kompatibilitas konservatif untuk tata letak folder media lama. | Dapat melewatkan duplikat yang diganti namanya. Jangan pernah gunakan dengan penghapusan duplikat atau berkas bermasalah. |
| **Tidak ada** | Tidak ada dedupe lintas file. | Hanya penyortiran, bukan pembersihan duplikat. | Duplikat tetap berada di sumber. |

## Lewati indeks tujuan

- **Mati (default)** — Memindai keluaran **Unik** yang ada dan mengindeksnya sebelum melakukan hashing. Lebih aman ketika menggunakan kembali folder keluaran yang sama.
- **On** — Melewati pemindaian itu.
- **Manfaat** — Lebih cepat pada pohon keluaran besar.
- **Risiko** — Lebih banyak konten duplikat dapat masuk ke dalam Unique.

## Tahun min. Unik

Tahun kalender minimum untuk folder tanggal pada **Unik** dalam tata letak media. **Mengapa** — Menghindari penyebaran file yang sangat lama ke folder tahun ganjil jika metadatanya salah.

## Pindahkan thread

Pemindahan file paralel setelah tujuan dicadangkan.

- **Lebih Tinggi** — Lebih cepat pada SSD lokal.
- **Lebih Rendah** — Lebih aman pada drive yang dipetakan NAS, USB, atau Wi-Fi.

## Utas klasifikasi dan hash

Pekerja paralel selama pemindaian sumber dan deduplikasi SHA-256.

- **Utas klasifikasi** — Penemuan dan klasifikasi berkas. CLI: `--classify-threads <n>`.
- **Utas hash** — Pekerja hashing konten. CLI: `--hash-threads <n>`.
- **Penggantian** — Nilai manual menggantikan bawaan profil (`--profile`).

## Enum paralel maks

Enum untuk daftar direktori paralel selama pemindaian.

- **0** = mesin otomatis.
- **Lebih Rendah** — Mengurangi tekanan pada SMB ketika banyak folder dicantumkan sekaligus.

## Tambahan pass direktori

- **Nyala (bawaan)** — Satu penelusuran tambahan yang dangkal, melebar dahulu.
- **Mengapa** — Sebagian jalur NAS atau pohon yang dalam tampak belum lengkap setelah penelusuran pertama.
- **Mati** — Hanya setelah jumlah berkas yang utuh terbukti tanpa itu.
- **CLI** — `--no-bfs` mematikan penelusuran ini.

## File status lanjut status

Jalur UTF-8 opsional. Pergerakan yang berhasil menambahkan baris `B64|` sehingga proses pengorganisasian berikutnya dapat melewati sumber yang sudah selesai.

- **Mengapa** — Melanjutkan pekerjaan yang panjang setelah berhenti atau mogok.
- **Jalur default** — Saat kolom kosong saat run time, mesin akan menggunakan `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt`. Tanpa Output, ia menggunakan `sessions\<id>\resume\OrganizeFiles.resume.txt` di bawah profil aplikasi.
- **Desktop UI** — Daftar jalur baca-saja untuk pemilihan dan penyalinan mouse. Ketika file resume sudah ada di lokasi default, jalurnya muncul secara otomatis. **Jelajahi** pilih folder log dan tambahkan `OrganizeFiles.resume.txt`. **Hapus** membersihkan jalur. Jika kosong, petunjuk menunjukkan jalur yang digunakan saat run time.

## Mulai baru

Memotong file resume ketika proses pengorganisasian **sebenarnya** dimulai (simulasi tidak terpotong). Dengan **Simpan kemajuan & ruang kerja**, juga menghapus snapshot UI yang disimpan saat proses dimulai. **Mengapa** — Memaksa penghitungan ulang secara penuh alih-alih melanjutkan log resume lama.

## Akar pemindaian Ekstra Unik

Satu folder per baris: pohon **Unik** ekstra untuk diindeks (tata letak lama, volume lain).

- **Mengapa** — Dedupe dapat melihat file yang sudah diatur di tempat lain tanpa memindahkannya lagi.
- **Desktop UI** — Daftar hanya baca untuk salinan per baris. **Tambahkan** menambahkan folder yang dipilih. **Hapus** menghapus baris yang dipilih (misalnya pohon `Uniques` lama di NAS).

## Coba ulang jaringan (detik) / Nonaktifkan tunggu jaringan

Detik untuk mencoba lagi I/O jaringan sementara.

- **Mengapa** — Pelapor UKM menghentikan sesi menganggur. Digunakan untuk mengatur dan memperbaiki.
- **Nonaktifkan tunggu jaringan** — Berhenti menunggu dan gagal.

## Disk full retry

(detik) / Nonaktifkan disk-full wait

Pola yang sama ketika volume keluaran kehabisan ruang. **Mengapa** — Saatnya mengosongkan disk saat dijalankan dalam waktu lama.

## Jalur kartu grafis

Hanya ketika **pemeriksaan video penuh** bawaan menyala dan **Gunakan kartu grafis yang terdeteksi** juga menyala. Nilai di atas **0** menetapkan jumlah jalur yang pasti untuk pemeriksaan sejajar di antara pabrikan yang terdeteksi (NVIDIA, AMD, Intel, Apple, seluler). **0** berarti jumlah jalur dicari sendiri. Itu bukan berarti hanya prosesor. Untuk pencuplikan hanya pada prosesor, pilih **Hanya CPU** pada daftar kartu grafis. Penanda jalur merencanakan pemeriksaan aliran bit pada prosesor. Penanda itu tidak memanggil pengurai video perangkat keras sistem.

- **Prasetel baris perintah** — `--hwaccel <value>` memilih prasetel jalur pemeriksaan (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`) ketika pemeriksaan video penuh berjalan.

## Buffer baca hash

Buffer baca per pekerja saat melakukan hashing (512 KiB, 1 MiB, 8 MiB). **Mengapa** — Buffer yang lebih besar membantu ketika NAS atau berbagi dengan latensi tinggi lambat merespons.

## Rekam jurnal urungkan

Jurnal JSONL opsional atas pemindahan di bawah akar keluaran untuk proses ini.

- **Untuk apa** — Memungkinkan pembatalan lewat CLI setelah proses nyata.
- **Arsip** — Pengarsipan setelah penataan tetap mati selama jurnal aktif.
- **CLI** — `--record-undo-journal` (sama dengan kotak centang di jendela utama).

## Tulis jalankan detak jantung

Menulis berkas opsional `Organize.Files.run.json` di bawah `Output\_OrganizeMediaLogs`.

- **Mengapa** — Perkakas luar dapat membaca pencacah hidup (ditelusuri, direncanakan, selesai) selagi menata atau memperbaiki.
- **Selang waktu** — Setiap 10.000 berkas terlihat, setiap 5.000 kecocokan, dan kira-kira setiap 15 detik selama penelusuran sumber, setiap 1.000 berkas dan paling sering sekali setiap 5 detik selama validasi, hashing, dan pemindahan, dan pada setiap tahap besar.
