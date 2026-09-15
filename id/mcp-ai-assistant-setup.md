# Asisten AI (MCP)

Tim berlisensi menghubungkan **OrganizeFiles.Cli** ke Claude Desktop, **Cursor**, VS Code Copilot, atau klien Model Context Protocol lain, yang di bawah ini disebut klien MCP. Konektornya adalah paket Python **organize-files-mcp**. Paket ini dapat diunduh gratis dari github.com/GutRaz/organize-files-docs, di folder `mcp/`.

**Di aplikasi desktop:** buka **Penyiapan MCP…** di bawah **Aplikasi & data** di kolom opsi, atau dari menu alat. Pilih **akses MCP**: **Mati**, **Monitor**, atau **Kontrol**. Lalu salin cuplikan JSON. Muat ulang MCP di aplikasi AI setiap kali tingkat diubah, karena **Kontrol** membuat token baru setiap kali.

**Tanyakan kepada asisten dokumentasi** “setup mcp” atau “cum setez mcp” untuk langkah-langkah pada sistem saat ini.

## Tingkat akses MCP, diatur di aplikasi

Tingkat ini sesuai dengan tiga jenis pekerjaan: **baca / pratinjau / eksekusi**.

| Tingkat | Jenis pekerjaan | Apa yang dapat dilakukan AI |
|-------|--------|-------------------|
| **Mati** | — | Hanya `organize_mcp_status`. Tanpa diagnostik dan tanpa akses ke ruang kerja. |
| **Monitor** | **Baca** | Semua yang ada di Mati, ditambah diagnostik hanya baca, riwayat proses dan tugas, kunci, pemeriksaan audit, **`organize_capabilities`** dan **`organize_workspace_snapshot`**. `organize_capabilities` mencantumkan mode proses, termasuk **`ai`**, cakupan pemindahan, dan target. `organize_workspace_snapshot` menampilkan ruang kerja yang disimpan di jendela utama. Tanpa pratinjau dan tanpa eksekusi. |
| **Kontrol** | **Pratinjau** / **Eksekusi** | Semua yang ada di Monitor, ditambah **`organize_create_job`**, **`organize_run_workspace`**, dan **`organize_remove_empty_organize_layout`**. Tingkat ini memerlukan **token kontrol** di pengaturan MCP, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **Pratinjau** adalah `organize_run_workspace` saat ruang kerja tersimpan mengaktifkan **Simulasi**, jadi tidak ada yang ditulis. **Eksekusi** adalah alat yang sama dengan Simulasi mati, jadi file dipindahkan. Konektor tidak menyertakan `--confirm-destructive` kecuali panggilan menetapkan `confirm_destructive=true`, dan tanpa opsi itu baris perintah menolak dengan `confirm_destructive_required`. |

File kontrol adalah **`mcp-control.json`**, di samping `automation-jobs.json` di folder profil aplikasi. Cuplikan yang disalin tidak menyebut file ini, karena konektor menemukannya di folder profil bawaan. Tetapkan **`ORGANIZE_FILES_MCP_CONTROL_FILE`** hanya jika file berada di tempat lain. Pada **Kontrol**, cuplikan juga menetapkan **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`**.

**Memindahkan dan menghapus memerlukan langkah kedua oleh manusia.** Asisten menetapkan konfirmasinya sendiri, sehingga teks yang dibaca asisten bisa membujuknya untuk mengonfirmasi. Karena itu, proses yang bukan simulasi juga memerlukan jendela yang dibuka di **Penyiapan MCP**, dan jendela itu menutup sendiri setelah 15 menit. Di luar jendela itu asisten masih dapat menyiapkan proses dan menampilkan pratinjaunya, tetapi prosesnya sendiri ditolak. File kontrol dan jendela itu sama-sama ditandatangani dengan kunci yang disimpan instalasi ini. File kontrol yang diubah secara manual atau disalin dari komputer lain dihitung sebagai Mati.

## Alat MCP menurut tingkat

**Selalu, juga pada Mati:** `organize_mcp_status`

**Monitor dan Kontrol:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide`, dan `organize_run_raw_cli`, yang hanya menerima perintah baca saja.

**Juga di Monitor dan Kontrol:** `organize_capabilities`, yang mencantumkan mode proses **`ai`** untuk file AI dan ML, dan `organize_workspace_snapshot`.

**Hanya Kontrol:** `organize_create_job` dari ruang kerja atau dari JSON tugas, `organize_run_workspace` untuk pratinjau atau proses sungguhan sesuai Simulasi ruang kerja, dan `organize_remove_empty_organize_layout`, yang menghapus folder tata letak kosong di dalam output yang sudah ada dan tidak pernah membuat folder output itu sendiri.

Perintah yang memindahkan atau menghapus file selalu diblokir melalui MCP di luar tingkat **Kontrol**. Tidak ada pengaturan lain yang mengizinkannya.

## Opsi baris perintah yang digunakan konektor

| Opsi | Tingkat | Tujuan |
|------|-------|---------|
| `--mcp-control-status` | apa pun | JSON berisi tingkat, jalur file kontrol, dan penanda Monitor dan Kontrol |
| `--mcp-capabilities` | Monitor ke atas | Daftar JSON mode proses, termasuk **`ai`**, cakupan pemindahan, dan target |
| `--mcp-workspace-snapshot` | Monitor ke atas | Ruang kerja yang disimpan dan cara ruang kerja itu menjadi tugas |
| `--mcp-create-job` | Kontrol | Membuat tugas dengan `--from-workspace` atau `--mcp-job-json` |
| `--mcp-run-workspace` | Kontrol | Menjalankan ruang kerja yang disimpan, dengan `--allow-app-target` dan `--mcp-control-token` |
| `--remove-empty-organize-layout` | Kontrol | Menghapus folder tata letak kosong di dalam `--output` yang sudah ada |
| `--confirm-destructive` | Kontrol | Diperlukan bersama `--mcp-run-workspace` untuk proses yang memindahkan atau menghapus. Konektor hanya meneruskan opsi ini jika `confirm_destructive=true` |

## Pengaturan dalam JSON klien MCP

| Pengaturan | Kapan |
|----------|------|
| `ORGANIZE_FILES_CLI` | Jalur ke OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | Jalur ke `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | Jalur ke `mcp-control.json`, hanya jika file tidak ada di folder profil bawaan |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | Hanya tingkat **Kontrol**, dari cuplikan aplikasi |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | Tingkat **Kontrol**, untuk proses ruang kerja yang disimpan |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | Opsional. Token yang sama dengan yang digunakan host untuk operasi baca |

## Penyiapan di Windows

1. **Python 3.10 atau lebih baru** — jalankan `python -V` di PowerShell. Jika Python tidak ada atau versinya lebih lama, instal Python dari [python.org](https://www.python.org/downloads/) dan centang **Add python.exe to PATH**.
2. **Unduh dan instal konektor** — unduh github.com/GutRaz/organize-files-docs sebagai ZIP, ekstrak, lalu jalankan `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1`. Skrip membuat lingkungan Python khusus untuk konektor dan menampilkan perintah untuk aplikasi AI.
3. **Di aplikasi:** **Penyiapan MCP…**, pilih **Monitor** atau **Kontrol**, lalu salin JSON.
4. **Jalur:** `%LocalAppData%\OrganizeFilesCrossPlatform\` berisi tugas dan `mcp-control.json`. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **Uji** — jalankan `organize_mcp_status`, lalu `organize_server_info`. `cliResolved` harus true dan `mcpLevel` harus sesuai dengan aplikasi.

## Penyiapan di macOS

Langkah yang sama dengan **python3** dan `bash mcp/install-organize-files-mcp.sh`. Jika `python3 -V` menampilkan 3.9 atau tidak ada Python sama sekali, instal Python terlebih dahulu dari [python.org](https://www.python.org/downloads/macos/). Jalur: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Penyiapan di Linux

Langkah yang sama dengan **python3** dan `bash mcp/install-organize-files-mcp.sh`. Di Debian dan Ubuntu, jalankan dahulu `sudo apt install python3-venv`. Jalur: `~/.local/share/OrganizeFilesCrossPlatform/`, atau `$XDG_DATA_HOME` jika sudah ditetapkan, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Keamanan

- MCP berjalan sebagai **pengguna lokal** sistem operasi, dengan hak yang sama seperti baris perintah yang dijalankan secara manual.
- Rahasiakan **token kontrol** dan **token baca**, seperti kata sandi. Salin JSON lagi setelah Kontrol diaktifkan.
- **`organize_run_workspace`** berjalan di baris perintah, bukan melalui tombol Jalankan di aplikasi. Jangan menjalankan dua tugas pada folder output yang sama secara bersamaan.
- Contoh: `mcp/examples/`.

## Proses yang memindahkan atau menghapus

`--mcp-run-workspace` memerlukan `--confirm-destructive` untuk setiap proses yang bukan simulasi, baik memindahkan, menghapus, maupun mengarsipkan. Tanpa opsi itu baris perintah menjawab `confirm_destructive_required`. Konektor tidak menyertakan opsi itu kecuali panggilan menetapkan `confirm_destructive=true`, dan hanya tingkat Kontrol yang dapat melakukannya. Jadi secara bawaan konektor menolak.

## Bahasa

Jawaban penyiapan berasal dari panduan terjemahan yang sama dengan jendela Dokumentasi dan Asisten panduan. `organize_capabilities` melaporkan mode proses dan target, bukan nama tema di aplikasi.
