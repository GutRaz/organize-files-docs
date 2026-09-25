# Prometheus ve Grafana ile izleme

## Sayaçların kapsamı

Planlanmış işler küçük bir Prometheus sayaç ve gösterge kümesi tutar. Her ad `organize_files_automation_` ile başlar ve kümenin tamamı Prometheus metni olarak yayımlanır. İş çalıştıran üç makinenin üçü de aynı kümeyi yayımlar: masaüstü uygulaması, `OrganizeFiles.JobAgent` hizmeti ve kapsayıcılarda kullanılan komut satırı makinesi.

Sayaçlar dosyaları değil, zamanlayıcıyı anlatır. Geçişler, iş sonuçları, onaylar, webhook teslimi ve geçmiş bakımı sayılır. Bir işin taşıdığı dosyalar hakkında hiçbir şey sayılmaz.

## Bağlantı noktası açmadan dosyaya aktarma

`automation-metrics.prom`, otomasyon veri klasörüne `automation-jobs.json` yanına yazılır ve her vadesi gelen geçişten sonra ve her okumada tazelenir. Biçim, `node_exporter` içindeki textfile toplayıcısının okuduğu biçimdir, dolayısıyla `node_exporter` zaten çalışan bir makine dinleyen bağlantı noktası olmadan, belirteç olmadan ve güvenlik duvarı kuralı olmadan kapsanır. Dosya atomik olarak değiştirilir ve yerine bırakılan simgesel bağ, izlenmek yerine yazmayı durdurur.

## Okuma uç noktası

Uç nokta yalnızca `ORGANIZE_FILES_METRICS_HTTP_PORT` 1 ile 65535 arasında bir bağlantı noktası tuttuğunda vardır. Bu değişken olmadan hiçbir şey dinlemez.

| Değişken | Etki |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | Dinlenecek bağlantı noktası. Yoksa veya aralık dışındaysa hiçbir uç nokta oluşmaz. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Dinleme adresi. Varsayılan `127.0.0.1` değeridir. `0.0.0.0`, `+` ve `*` değerleri tüm adresleri anlatır, başka her şey `127.0.0.1` değerine döner. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | `/metrics` ve `/ready` üzerinde istenen bearer belirteci. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1`, küme yoklamaları için `/ready` yolunun o belirteç olmadan yanıt vermesine izin verir. Makine yolları o durumda yanıtın dışında kalır. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | `/ready` yolunun hazır değil bildirmesine yol açan, virgülle ayrılmış çıkış kodları. Yerleşik listenin yerini alır. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1`, son geçişin çıkış kodunu ve ilk geçiş bitmeden önceki durumu da yok sayar. |
| `ORGANIZE_FILES_READY_JSON` | `1`, düz metin isteyen bir çağıran için bile `/ready` üzerinde JSON gövdesini zorunlu kılar. |

Geri döngü dışındaki bir adres, bir bearer belirteci ayarlanmadıysa dinleyici açılmadan önce geri çevrilir. Geri çevirme hata çıktısına yazılır ve webhook olayı olarak gönderilir, çünkü bu birleşim sayaçları tüm ağa verirdi.

## Sunulan yollar

- `/metrics` — Prometheus metni olarak sayaçlar. `/` yoluna gelen bir istek aynı içeriği döndürür.
- `/ready` — bir düzenleyici için hazırlık. Otomasyon klasörü deneme yazmasını kabul ettiğinde, iş dosyası açıldığında, geçmiş klasörü veri kökü içinde çözüldüğünde ve vadesi gelen son geçiş engellemeyen bir çıkış koduyla bittiğinde yanıt `200` olur. Aksi durumda yanıt `503` olur ve `due_pass_not_completed` ya da `last_due_pass_license_failed` gibi kısa bir gerekçe gelir.
- `/health` — yalnızca yaşam işareti. Bir belirteç ayarlıyken bile bu yol anonim kalır, çünkü `ok` yanıtını verir ve başka bir şey vermez.

Lisans hatası için `3`, kilitli çıktı ağacı için `8`, hiç onaylanmamış bir silme için `10` ve talep çakışması için `11` çıkış kodları hazırlığı varsayılan olarak engeller. `/ready` gövdesi, çağıran `Accept: text/plain` göndermedikçe veya `?format=text` eklemedikçe JSON olur.

## Sayaçlar

| Ad | İçerik |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Zamanlayıcının başlattığı, vadesi gelen geçişler. |
| `organize_files_automation_jobs_started_total` | Çalışır duruma ulaşan iş çalıştırmaları. |
| `organize_files_automation_jobs_skipped_total` | Atlanan işler: hazır olmayan bir Docker veya Kubernetes ortamı, ekransız bir makinede uygulamayı hedefleyen iş, dolu bir çıktı kökü ya da düzenleyicinin geri çevirdiği iş. |
| `organize_files_automation_jobs_failed_total` | Başarısızlıkla biten iş çalıştırmaları. |
| `organize_files_automation_jobs_awaiting_approval_total` | Onay için bekletilen gerçek çalıştırmalar. |
| `organize_files_automation_execute_approvals_total` | Gerçek bir çalıştırmaya verilen onaylar. |
| `organize_files_automation_execute_approvals_expired_total` | Kullanılmadan önce süresi dolan onaylar. |
| `organize_files_automation_claim_conflicts_total` | Başka bir makinenin çıktı kökü üzerindeki talebi zaten elinde tuttuğu durumlar. |
| `organize_files_automation_runs_orphaned_total` | Duran bir makinenin geride bıraktığı, öksüz olarak kurtarılan çalıştırmalar. |
| `organize_files_automation_job_events_total` | Olay başına bir sayaç, `event`, `job_id`, `target` ve `jobs_file` etiketleriyle. |
| `organize_files_automation_webhook_posts_succeeded_total` | Kabul edilen webhook teslimleri. |
| `organize_files_automation_webhook_posts_failed_total` | Geri çevrilen veya ulaşılamayan webhook teslimleri. |
| `organize_files_automation_webhook_dead_letter_depth` | Teslim edilemeyen webhook dosyasında şu anda bekleyen satırlar. |
| `organize_files_automation_log_retention_pruned_total` | Saklama süresinin kaldırdığı çalıştırma günlükleri. |
| `organize_files_automation_runs_index_compacted_total` | Sıkıştırma sırasında çalıştırma dizininden çıkarılan satırlar. |
| `organize_files_automation_last_due_pass_exit_code` | En son biten geçişin çıkış kodu. `0` temiz bir geçiştir. |
| `organize_files_automation_last_due_pass_completed_utc` | En son biten geçişin saniye cinsinden Unix zamanı, ilkinden önce ise `0`. |

## Gösterge tablosu ve uyarı kuralları

Hazır bir Grafana gösterge tablosu, dağıtım dosyalarıyla birlikte `grafana-organize-files-automation.json` adıyla ve **OrganizeFiles Automation** başlığıyla yayımlanır. On paneli vadesi gelen geçişleri, başlatılan ve başarısız işleri, talep çakışmalarını, bir saatlik iş akışını, son çıkış kodunu, teslim edilemeyen ileti derinliğini, bir günlük webhook hatalarını, onay bekleyen işleri ve duruma göre iş olaylarını gösterir. Her panel veri kaynağını `${DS_PROMETHEUS}` yer tutucusuyla adlandırır.

Karşılık gelen uyarı kuralları `alerts-organize-files-automation.yaml` dosyasındadır, `prometheus-rule-automation.yaml` ise `kube-prometheus-stack` için Kubernetes kabuğudur. Sıfırdan farklı bir son çıkış kodu beş dakika sonra uyarır, lisans hatası bir dakika sonra kritiktir, kalan kurallar ise başarısız işleri, talep çakışmalarını, webhook hatalarını, teslim edilemeyen ileti yığılmasını ve bir gündür bekleyen onayları kapsar. Her iki dosya da her derlemede doğrulanır, böylece yukarıdaki adlar sayaçlarla aynı adımda kalır.

# Çalıştırma çıktısı ve ölçümler

## Durum satırı

**Çalıştırma çıktısı** alanı şunu gösterir:

- Uygulamanın mevcut durumu ve motorun ilerlemesi.
- **CPU** ve yalnızca bu işlem için iki **bellek** değeri.
- **GPU** satırları, Windows'ta: bu işlemin her ekran kartındaki payı, kartın tamamı değil.

Aynı kompakt kaynak çubuğu, dosya keşfi, zamanlanmış işler ve dosya onarımı gibi ikincil araç pencerelerinde yeniden kullanılır.

## Bellek etiketleri

- **Özel bayt/taahhüt** — işlem tarafından ayrılan özel sanal bellek.
- **Çalışma seti/bellek** — bu işlem tarafından halihazırda tutulan yerleşik RAM. Her işletim sistemi ve masaüstü ortamı etiketi belleği farklı şekilde işlediğinden, başka bir işletim sistemi monitöründen farklı olabilir.

## Heartbeat JSON'u çalıştır (isteğe bağlı)

**Gelişmiş / Teşhis** altında **Çalıştırma kalp atışı JSON'unu yaz** seçeneğini etkinleştirin. Motor, `Output\_OrganizeMediaLogs` altına (varsayılan organize devam durumu dosyasıyla aynı klasör) `Organize.Files.run.json` yazar.

- **Yol** — düzenleme ve onarım çalışmaları sırasında atomik olarak güncellenir.
- **Yazma aralığı** — kaynaklar taranırken dosya, görülen her 10.000 dosyada, her 5.000 eşleşmede ve tarama sürdükçe yaklaşık 15 saniyede bir yeniden yazılır. Böylece listelenmesi yavaş büyük bir ağ ağacında bile çalıştırmanın canlı olduğu görülür. Doğrulama, karma alma ve taşıma sırasında her 1.000 dosyadan sonra, en fazla 5 saniyede bir yeniden yazılır. Başlangıç ve bitiş yazımları, bir çalıştırma başlarken ve biterken yine gerçekleşir.
- **İlerleme** — dosya sayıları hâlâ artarken ana ilerleme çubuğu %100 yerine o ana dek görülen dosyaları gösterir, ta ki bir aşamanın toplamı bilinene kadar.
- **Alanlar** — `schema`, `mode`, `phase` (örneğin `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`), `runState` (`active` / `completed` / `failed` / `cancelled`), `utc` (ISO-8601), `dryRun`, `outputRoot`, `validateMedia`, `deepVideoValidate`, `gpuDeviceCount`, `hwaccel`, isteğe bağlı `correlationId`, iç içe geçmiş `progress` sayaçları.
- **Günlük** — çalıştırma çıktı paneli başlangıçta ve dosyanın sonunda kaydedildiğinde tam yolu yazdırır. Gelişmiş / Teşhis altında **Kalp atışı günlük klasörünü aç** / **Kalp atışı JSON dosyasını göster** seçeneğini kullanın.
- **CLI** — OrganizeFiles.Cli üzerinde `--heartbeat-json`. İptal ve ölümcül kabuk hataları, etkinleştirildiğinde `cancelled` / `failed` `runState` yazın.
