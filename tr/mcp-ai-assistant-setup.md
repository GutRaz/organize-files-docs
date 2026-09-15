# Yapay zeka asistanı (MCP)

Lisanslı ekipler **OrganizeFiles.Cli** aracını Claude Desktop, **Cursor**, VS Code Copilot veya başka bir Model Context Protocol istemcisine bağlar, aşağıda buna MCP istemcisi denir. Bağlayıcı, **organize-files-mcp** Python paketidir. github.com/GutRaz/organize-files-docs adresinden, `mcp/` klasöründen ücretsiz indirilir.

**Masaüstü uygulamasında:** seçenekler sütununda **Uygulama ve veriler** altındaki veya araçlar menüsündeki **MCP kurulumu…** öğesini açın. **MCP erişimi** için bir düzey seçin: **Kapalı**, **Monitör** veya **Denetim**. Ardından JSON parçasını kopyalayın. Her düzey değişikliğinden sonra yapay zeka uygulamasında MCP'yi yeniden yükleyin, çünkü **Denetim** her seferinde yeni bir belirteç oluşturur.

**Dokümantasyon asistanına** geçerli sistemdeki adımlar için "setup mcp" veya "cum setez mcp" diye sorun.

## Uygulamada ayarlanan MCP erişim düzeyleri

Düzeyler üç tür işe karşılık gelir: **okuma / önizleme / yürütme**.

| Düzey | İş türü | Yapay zekanın yapabildikleri |
|-------|--------|-------------------|
| **Kapalı** | — | Yalnızca `organize_mcp_status`. Tanılama yok ve çalışma alanına erişim yok. |
| **Monitör** | **Okuma** | Kapalı düzeyindeki her şey, ayrıca salt okunur tanılama, çalıştırma ve görev geçmişi, kilitler, denetim kontrolleri, **`organize_capabilities`** ve **`organize_workspace_snapshot`**. `organize_capabilities` çalıştırma kiplerini, aralarında **`ai`** olmak üzere, taşıma kapsamlarını ve hedefleri listeler. `organize_workspace_snapshot` ana pencerede kaydedilen çalışma alanını gösterir. Önizleme ve yürütme yok. |
| **Denetim** | **Önizleme** / **Yürütme** | Monitör düzeyindeki her şey, ayrıca **`organize_create_job`**, **`organize_run_workspace`** ve **`organize_remove_empty_organize_layout`**. MCP ayarlarında bir **denetim belirteci** gerekir, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **Önizleme**, kaydedilen çalışma alanında **Deneme çalıştırması** açıkken `organize_run_workspace` demektir, bu yüzden hiçbir şey yazılmaz. **Yürütme**, Deneme çalıştırması kapalıyken aynı araçtır, bu yüzden dosyalar taşınır. Bağlayıcı, çağrı `confirm_destructive=true` ayarlamadıkça `--confirm-destructive` eklemez ve bu bayrak olmadan komut satırı `confirm_destructive_required` ile reddeder. |

Denetim dosyası **`mcp-control.json`** dosyasıdır ve uygulamanın profil klasöründe `automation-jobs.json` dosyasının yanındadır. Kopyalanan parça bu dosyanın adını vermez, çünkü bağlayıcı dosyayı varsayılan profil klasöründe kendisi bulur. **`ORGANIZE_FILES_MCP_CONTROL_FILE`** değerini yalnızca dosya başka bir yerdeyse ayarlayın. **Denetim** düzeyinde parça ayrıca **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`** ayarlar.

**Taşıma ve silme, insan tarafından atılan ikinci bir adım gerektirir.** Asistan onayını kendisi verir, bu yüzden okuduğu bir metin asistanı onaylamaya ikna edebilir. Bu nedenle deneme olmayan bir çalıştırma, **MCP kurulumu** içinde açılan bir zaman aralığı da gerektirir ve bu aralık 15 dakika sonra kendiliğinden kapanır. Aralığın dışında asistan yine de bir çalıştırmayı hazırlayıp önizleyebilir, ancak çalıştırmanın kendisi reddedilir. Hem denetim dosyası hem de aralık bu kurulumun sakladığı bir anahtarla imzalanır. Elle değiştirilmiş veya başka bir bilgisayardan kopyalanmış bir denetim dosyası Kapalı sayılır.

## Düzeylere göre MCP araçları

**Her zaman, Kapalı düzeyinde de:** `organize_mcp_status`

**Monitör ve Denetim:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` ve yalnızca okuma komutlarını kabul eden `organize_run_raw_cli`.

**Yine Monitör ve Denetim düzeyinde:** yapay zeka ve makine öğrenmesi dosyaları için **`ai`** çalıştırma kipini listeleyen `organize_capabilities` ve `organize_workspace_snapshot`.

**Yalnızca Denetim:** çalışma alanından veya görev JSON'undan `organize_create_job`, çalışma alanındaki Deneme çalıştırması ayarına göre önizleme veya gerçek çalıştırma için `organize_run_workspace` ve var olan bir çıktının içindeki boş yerleşim klasörlerini kaldıran, çıktı klasörünün kendisini asla oluşturmayan `organize_remove_empty_organize_layout`.

Dosyaları taşıyan veya silen komutlar, **Denetim** düzeyi dışında MCP üzerinden her zaman engellenir. Başka hiçbir ayar bunlara izin vermez.

## Bağlayıcının kullandığı komut satırı bayrakları

| Bayrak | Düzey | Amaç |
|------|-------|---------|
| `--mcp-control-status` | herhangi | Düzeyi, denetim dosyasının yolunu ve Monitör ile Denetim işaretlerini içeren JSON |
| `--mcp-capabilities` | Monitör ve üstü | Aralarında **`ai`** olan çalıştırma kiplerinin, taşıma kapsamlarının ve hedeflerin JSON listesi |
| `--mcp-workspace-snapshot` | Monitör ve üstü | Kaydedilen çalışma alanı ve bir göreve nasıl dönüştüğü |
| `--mcp-create-job` | Denetim | `--from-workspace` veya `--mcp-job-json` ile görev oluşturma |
| `--mcp-run-workspace` | Denetim | Kaydedilen çalışma alanını `--allow-app-target` ve `--mcp-control-token` ile çalıştırma |
| `--remove-empty-organize-layout` | Denetim | Var olan bir `--output` içindeki boş yerleşim klasörlerini kaldırma |
| `--confirm-destructive` | Denetim | Taşıyan veya silen bir çalıştırma için `--mcp-run-workspace` ile gerekir. Bağlayıcı bunu yalnızca `confirm_destructive=true` olduğunda iletir |

## MCP istemcisi JSON'undaki ayarlar

| Ayar | Ne zaman |
|----------|------|
| `ORGANIZE_FILES_CLI` | OrganizeFiles.Cli yolu |
| `ORGANIZE_FILES_JOBS_FILE` | `automation-jobs.json` yolu |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | `mcp-control.json` yolu, yalnızca dosya varsayılan profil klasöründe değilse |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | Yalnızca **Denetim** düzeyi, uygulamanın parçasından |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | **Denetim** düzeyi, kaydedilen çalışma alanının çalıştırmaları için |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | İsteğe bağlı. Ana makinenin okuma işlemleri için kullandığı belirtecin aynısı |

## Windows kurulumu

1. **Python 3.10 veya daha yenisi** — PowerShell'de `python -V` çalıştırın. Python yoksa veya daha eskiyse [python.org](https://www.python.org/downloads/) adresinden yükleyin ve **Add python.exe to PATH** kutusunu işaretleyin.
2. **Bağlayıcıyı indirin ve kurun** — github.com/GutRaz/organize-files-docs deposunu ZIP olarak indirin, açın ve `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1` çalıştırın. Betik, bağlayıcı için ayrı bir Python ortamı oluşturur ve yapay zeka uygulaması için komutu yazdırır.
3. **Uygulamada:** **MCP kurulumu…**, **Monitör** veya **Denetim** seçin, sonra JSON'u kopyalayın.
4. **Yollar:** `%LocalAppData%\OrganizeFilesCrossPlatform\` görevleri ve `mcp-control.json` dosyasını tutar. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **Test** — `organize_mcp_status`, ardından `organize_server_info` çalıştırın. `cliResolved` true olmalı ve `mcpLevel` uygulamayla aynı olmalıdır.

## macOS kurulumu

**python3** ve `bash mcp/install-organize-files-mcp.sh` ile aynı adımlar. `python3 -V` 3.9 gösteriyorsa veya hiç Python yoksa önce [python.org](https://www.python.org/downloads/macos/) adresinden Python yükleyin. Yollar: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Linux kurulumu

**python3** ve `bash mcp/install-organize-files-mcp.sh` ile aynı adımlar. Debian ve Ubuntu'da önce `sudo apt install python3-venv` çalıştırın. Yollar: `~/.local/share/OrganizeFilesCrossPlatform/` veya ayarlıysa `$XDG_DATA_HOME`, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Güvenlik

- MCP, işletim sisteminin **yerel kullanıcısı** olarak, elle çalıştırılan komut satırıyla aynı haklarla çalışır.
- **Denetim belirtecini** ve **okuma belirtecini** parolalar gibi gizli tutun. Denetim düzeyini açtıktan sonra JSON'u yeniden kopyalayın.
- **`organize_run_workspace`**, uygulamanın Çalıştır düğmesiyle değil, komut satırında çalışır. Aynı çıktı klasöründe aynı anda iki görev çalıştırmayın.
- Örnekler: `mcp/examples/`.

## Taşıyan veya silen çalıştırmalar

`--mcp-run-workspace`, deneme olmayan her çalıştırma için `--confirm-destructive` ister, çalıştırma taşısa, silse veya arşivlese de. Bu bayrak olmadan komut satırı `confirm_destructive_required` yanıtını verir. Bağlayıcı, çağrı `confirm_destructive=true` ayarlamadıkça bayrağı eklemez ve bunu yalnızca Denetim düzeyi yapabilir. Bu yüzden bağlayıcı varsayılan olarak reddeder.

## Diller

Kurulum yanıtları, Dokümantasyon penceresi ve Rehber asistanı ile aynı çevrilmiş kılavuzdan gelir. `organize_capabilities` uygulamadaki tema adlarını değil, çalıştırma kiplerini ve hedefleri bildirir.
