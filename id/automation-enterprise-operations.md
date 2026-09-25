# Pemantauan dengan Prometheus dan Grafana

## Cakupan penghitung

Pekerjaan terjadwal menyimpan sekumpulan kecil penghitung dan pengukur Prometheus. Setiap nama diawali `organize_files_automation_`, dan seluruh kumpulan diterbitkan sebagai teks Prometheus. Ketiga inang yang menjalankan pekerjaan menerbitkan kumpulan yang sama: aplikasi destop, layanan `OrganizeFiles.JobAgent`, dan inang baris perintah yang dipakai di dalam kontainer.

Penghitung menggambarkan penjadwal, bukan berkas. Yang dihitung adalah lintasan, hasil pekerjaan, persetujuan, pengiriman webhook, dan perapian riwayat. Tidak ada yang dihitung tentang berkas yang dipindahkan sebuah pekerjaan.

## Ekspor ke berkas, tanpa membuka porta

`automation-metrics.prom` ditulis ke folder data otomatisasi, di samping `automation-jobs.json`, dan disegarkan setelah setiap lintasan yang jatuh tempo dan pada setiap pembacaan. Tata letaknya adalah yang dibaca pengumpul textfile milik `node_exporter`, sehingga mesin yang sudah menjalankan `node_exporter` tercakup tanpa porta yang mendengarkan, tanpa token, dan tanpa aturan tembok api. Berkas diganti secara atomik, dan tautan simbolis yang ditinggalkan di tempatnya menghentikan penulisan alih-alih diikuti.

## Titik pembacaan

Titik pembacaan hanya ada bila `ORGANIZE_FILES_METRICS_HTTP_PORT` memuat porta antara 1 dan 65535. Tanpa variabel itu tidak ada yang mendengarkan.

| Variabel | Akibat |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | Porta yang didengarkan. Bila hilang atau di luar rentang, tidak ada titik pembacaan sama sekali. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Alamat pendengaran. Bawaannya `127.0.0.1`. Nilai `0.0.0.0`, `+` dan `*` berarti semua alamat, dan nilai lain kembali ke `127.0.0.1`. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | Token bearer yang diminta pada `/metrics` dan pada `/ready`. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` membiarkan `/ready` menjawab tanpa token itu, untuk penyelidik gugus. Jalur inang lalu ditinggalkan di luar jawaban. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | Kode keluar yang dipisah koma yang membuat `/ready` melaporkan belum siap. Menggantikan daftar bawaan. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` mengabaikan kode keluar lintasan terakhir, dan juga keadaan sebelum lintasan pertama selesai. |
| `ORGANIZE_FILES_READY_JSON` | `1` memaksa badan JSON pada `/ready`, bahkan untuk pemanggil yang meminta teks biasa. |

Alamat di luar loopback ditolak sebelum pendengar dibuka bila tidak ada token bearer yang disetel. Penolakan dituliskan ke keluaran galat dan dikirim sebagai peristiwa webhook, sebab gabungan itu akan menyerahkan penghitung kepada seluruh jaringan.

## Jalur yang dilayani

- `/metrics` — penghitung sebagai teks Prometheus. Permintaan ke `/` mengembalikan isi yang sama.
- `/ready` — kesiapan bagi pengatur. Jawabannya `200` begitu folder otomatisasi menerima penulisan uji, berkas pekerjaan terbuka, folder riwayat terpecahkan di dalam akar data, dan lintasan jatuh tempo terakhir berakhir pada kode keluar yang tidak menghalangi. Selain itu jawabannya `503` dengan alasan singkat seperti `due_pass_not_completed` atau `last_due_pass_license_failed`.
- `/health` — hanya tanda hidup. Jalur itu tetap tanpa nama walau token disetel, karena menjawab `ok` dan tidak lebih.

Kode keluar `3` untuk kegagalan lisensi, `8` untuk pohon keluaran terkunci, `10` untuk penghapusan yang tak pernah ditegaskan, dan `11` untuk benturan klaim menghalangi kesiapan secara bawaan. Badan `/ready` berupa JSON kecuali pemanggil mengirim `Accept: text/plain` atau menambahkan `?format=text`.

## Penghitungnya

| Nama | Isi |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Lintasan jatuh tempo yang dimulai penjadwal. |
| `organize_files_automation_jobs_started_total` | Jalannya pekerjaan yang mencapai keadaan berjalan. |
| `organize_files_automation_jobs_skipped_total` | Pekerjaan yang dilewati: lingkungan Docker atau Kubernetes yang belum siap, pekerjaan yang menyasar aplikasi pada inang tanpa layar, akar keluaran sedang sibuk, atau pekerjaan yang ditolak pengatur. |
| `organize_files_automation_jobs_failed_total` | Jalannya pekerjaan yang berakhir gagal. |
| `organize_files_automation_jobs_awaiting_approval_total` | Jalannya pekerjaan sungguhan yang ditahan menunggu persetujuan. |
| `organize_files_automation_execute_approvals_total` | Persetujuan yang diberikan untuk jalannya pekerjaan sungguhan. |
| `organize_files_automation_execute_approvals_expired_total` | Persetujuan yang tenggatnya habis sebelum dipakai. |
| `organize_files_automation_claim_conflicts_total` | Saat inang lain sudah memegang klaim atas akar keluaran. |
| `organize_files_automation_runs_orphaned_total` | Jalannya pekerjaan yang dipulihkan sebagai yatim, ditinggalkan oleh inang yang berhenti. |
| `organize_files_automation_job_events_total` | Satu penghitung per peristiwa, dengan label `event`, `job_id`, `target` dan `jobs_file`. |
| `organize_files_automation_webhook_posts_succeeded_total` | Pengiriman webhook yang diterima. |
| `organize_files_automation_webhook_posts_failed_total` | Pengiriman webhook yang ditolak atau tak terjangkau. |
| `organize_files_automation_webhook_dead_letter_depth` | Baris yang menunggu saat ini di berkas webhook yang tidak terkirim. |
| `organize_files_automation_log_retention_pruned_total` | Catatan jalannya pekerjaan yang dihapus oleh aturan penyimpanan. |
| `organize_files_automation_runs_index_compacted_total` | Baris yang dikeluarkan dari indeks jalannya pekerjaan saat pemadatan. |
| `organize_files_automation_last_due_pass_exit_code` | Kode keluar lintasan terakhir yang selesai. `0` berarti lintasan bersih. |
| `organize_files_automation_last_due_pass_completed_utc` | Waktu Unix dalam detik dari lintasan terakhir yang selesai, dan `0` sebelum yang pertama. |

## Dasbor dan aturan peringatan

Dasbor Grafana siap pakai diterbitkan bersama berkas penggelaran sebagai `grafana-organize-files-automation.json`, dengan judul **OrganizeFiles Automation**. Sepuluh panelnya menampilkan lintasan jatuh tempo, pekerjaan yang dimulai dan gagal, benturan klaim, laju pekerjaan selama satu jam, kode keluar terakhir, kedalaman pesan tak terkirim, kegagalan webhook selama sehari, pekerjaan yang menunggu persetujuan, dan peristiwa pekerjaan menurut keadaan. Setiap panel menyebut sumber datanya lewat penanda `${DS_PROMETHEUS}`.

Aturan peringatan yang sepadan ada di `alerts-organize-files-automation.yaml`, dengan `prometheus-rule-automation.yaml` sebagai selubung Kubernetes untuk `kube-prometheus-stack`. Kode keluar terakhir yang bukan nol memberi peringatan setelah lima menit, kegagalan lisensi menjadi genting setelah satu menit, dan sisa aturannya mencakup pekerjaan gagal, benturan klaim, kegagalan webhook, tumpukan pesan tak terkirim, dan persetujuan yang dibiarkan menunggu sehari. Kedua berkas diperiksa pada setiap pembangunan, sehingga nama di atas tetap sejalan dengan penghitung.

# Keluaran proses dan metrik

## Baris status

Area **Keluaran proses** menunjukkan:

- Status aplikasi saat ini dan kemajuan mesin.
- **CPU** dan dua nilai **memori** hanya untuk proses ini.
- Baris **GPU**, di Windows: bagian proses ini dari setiap kartu grafis, bukan seluruh kartu.

Bilah sumber daya ringkas yang sama digunakan kembali di jendela alat sekunder seperti eksplorasi file, pekerjaan terjadwal, dan perbaikan file.

## Label memori

- **Byte pribadi / komit** — memori virtual pribadi yang dicadangkan oleh proses.
- **Working set / memory** — RAM residen yang saat ini disimpan oleh proses ini. Ini dapat berbeda dari monitor sistem operasi lain karena setiap OS dan lingkungan desktop memberi label proses memori secara berbeda.

## Jalankan detak jantung JSON (opsional)

Aktifkan **Write run detak jantung JSON** di bawah **Lanjutan / Diagnostik**. Mesin menulis `Organize.Files.run.json` di bawah `Output\_OrganizeMediaLogs` (folder yang sama dengan file resume pengaturan default).

- **Jalur** — diperbarui secara atom selama proses pengorganisasian dan perbaikan.
- **Selang waktu** — selagi sumber ditelusuri, berkas ditulis ulang setiap 10.000 berkas terlihat, setiap 5.000 kecocokan, dan kira-kira setiap 15 detik selama penelusuran masih berjalan, sehingga pohon jaringan besar yang lambat didaftar tetap menunjukkan bahwa eksekusi masih hidup. Selama validasi, hashing, dan pemindahan, berkas ditulis ulang setiap 1.000 berkas, paling sering sekali setiap 5 detik. Penulisan di awal dan di akhir tetap terjadi ketika sebuah eksekusi dimulai dan selesai.
- **Kemajuan** — selama jumlah berkas masih bertambah, bilah kemajuan utama menampilkan berkas yang sudah terlihat alih-alih 100%, sampai suatu tahap punya total yang diketahui.
- **Bidang** — `schema`, `mode`, `phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`), `runState` (`active` / `completed` / `failed` / `cancelled`), `utc` (ISO-8601), `dryRun`, `outputRoot`, `validateMedia`, `deepVideoValidate`, `gpuDeviceCount`, `hwaccel`, opsional `correlationId`, penghitung `progress` bertumpuk.
- **Log** — panel keluaran proses mencetak jalur lengkap saat awal dan saat file disimpan di akhir. Gunakan **Buka folder log detak jantung** / **Tampilkan file JSON detak jantung** di bagian Tingkat Lanjut/Diagnostik.
- **CLI** — `--heartbeat-json` di OrganizeFiles.Cli. Pembatalan dan kesalahan shell yang fatal tulis `cancelled` / `failed` `runState` saat diaktifkan.
