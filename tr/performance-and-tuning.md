# Gelişmiş / Teşhis

## Ayarlamayı organize edin

Gelişmiş / Tanılama, ana paneli karmaşıklaştırmadan **OrganizeFilesEngine** seçeneklerini ortaya çıkarır.

Düzenleme modları tekilleştirmeyi, hedef dizini, Benzersiz tarih kurallarını, taşıma ve numaralandırma iş parçacığını, BFS ekini, devam durumu dosyasını ve ekstra Benzersiz kökleri ayarlayabilir.

Onarım, yalnızca ağ ve disk dolu yeniden deneme zamanlamasını, isteğe bağlı tam video kontrolü için algılanan grafik donanım hatlarını, karma okuma arabelleğini ve JSON kalp atışını korur. Diğer alanlar bağlam açısından görünür ancak devre dışıdır.

Kaynaklar veya çıktı NAS veya UNC yollarında yayınlandığında, paralelliği azaltın, ağı yeniden denemeyi etkin tutun, tek SMB ağaçları için BFS ekini açık bırakın ve karma işlemi yavaşsa 8 MiB karma arabelleğini deneyin.

# Gelişmiş / Teşhis — her seçenek

## Bu bölüm hakkında

Bu denetimler motor seçenekleridir. Masaüstü (Windows, macOS, Linux), Android, iOS ve komut satırı aracı aynı değerleri okur.

**Organize Et** modları, kullanıcı arayüzü soluklaştırmadığı sürece aşağıdaki tüm denetimleri kullanır. **Onarım** yalnızca ağ yeniden denemesini, disk dolduğunda yeniden denemeyi, algılanan grafik donanımı hatlarını (tam video denetimiyle), karma okuma arabelleğini, heartbeat JSON'unu, **Devam durumu dosyası** ve **Yeni başla (devam durumu dosyasını kısalt)** kullanır. Diğer alanlar görünür kalır ancak onarım sırasında yok sayılır.

## Ağ kaynakları (NAS / UNC)

Kaynaklar veya Çıkış SMB/CIFS paylaşımlarında, NAS birimlerinde veya eşlenen sürücülerde olduğunda bu bölümü dikkatlice inceleyin.

- **Neden ayarlama** — Yerel bir SSD'de çalışan iş parçacığı sayımları, dosyalayıcıyı durdurabilir veya aşırı yükleyebilir.
- **Ne denenmeli** — Ağ yeniden denemeyi açık tutun. Zaman aşımlarında iş parçacıklarını azaltın ve paralel maksimumu numaralandırın. Tam sayım onsuz doğrulanmadığı sürece BFS ekini açık bırakın. Ağ üzerinde karma işlemi yavaş olduğunda 8 MiB karma arabelleğini deneyin.
- **Ağ beklemeyi devre dışı bırak** — Geçici ağ hatalarında hızlı bir şekilde başarısız olur. Wi-Fi veya meşgul paylaşımlarda riskli.

## Tekilleştirme modu

Motorun iki dosyanın kopya olduğuna nasıl karar verdiği.

| Modu | Ne işe yarar | Ne zaman kullanılır | Takas |
| ---- | ------------ | ----------- | --------- |
| **Karma (SHA-256)** | Dahil edilen her kaynak dosyanın tam içeriğini okur ve karma hale getirir, ardından aynı baytları gruplandırır. | En güçlü pratik mod. Kaynakta silme için Hash (SHA-256) zorunludur (kopyalar ve sorunlu dosyalar). | Büyük ağaçlarda veya NAS'te en yavaş. Hiçbir algoritma mutlak garanti olarak sunulmamalıdır. |
| **Boyut + zaman + ad** | Anahtar = boyut, UTC son yazma işaretleri, küçük harfli ad, ardından tam SHA-256 doğrulaması. | Eski medya klasörü düzenleri için muhafazakar uyumluluk modu. | Yeniden adlandırılan kopyaları kaçırabilir. Kopyaları veya sorunlu dosyaları silme işlemiyle asla kullanmayın. |
| **Yok** | Dosyalar arası tekilleştirme yok. | Yalnızca sıralama, yinelenen temizleme değil. | Kopyalar kaynaklarda kalır. |

## Hedef dizinini atla

- **Kapalı (varsayılan)** — Mevcut **Benzersiz** çıktıyı tarar ve karma işleminden önce dizine ekler. Aynı çıktı klasörünü yeniden kullanırken daha güvenli.
- **Açık** — Bu taramayı atlar.
- **Avantaj** — Büyük çıktı ağaçlarında daha hızlı.
- **Risk** — Benzersiz'in içine daha fazla yinelenen içerik gelebilir.

## Benzersiz için min. yıl

Medya düzenlerinde **Benzersiz** altındaki tarih klasörleri için minimum takvim yılı. **Neden** — Meta veriler yanlış olduğunda çok eski dosyaların tek yıllık klasörlere dağılmasını önler.

## Konuları taşı

Hedefler ayrıldıktan sonra paralel dosya taşınır.

- **Daha yüksek** — Yerel SSD'de daha hızlı.
- **Daha düşük** — NAS, USB veya Wi-Fi eşlemeli sürücülerde daha güvenli.

## Sınıflandırma ve hash iş parçacıkları

Kaynak taraması ve SHA-256 yinelenen ayıklaması sırasındaki paralel işçiler.

- **Sınıflandırma iş parçacıkları** — Dosya keşfi ve sınıflandırma. CLI: `--classify-threads <n>`.
- **Hash iş parçacıkları** — İçerik hash işçileri. CLI: `--hash-threads <n>`.
- **Geçersiz kılmalar** — Elle girilen değerler profil varsayılanlarını geçersiz kılar (`--profile`).

## Maksimum paralel numaralandırma

Tarama sırasında paralel dizin listelemesi için üst sınır.

- **0** = motor otomatik.
- **Daha düşük** — Aynı anda birçok klasör listelendiğinde SMB üzerinde daha az baskı olur.

## Ek BFS dizin geçişi

- **Açık (öntanımlı)** — Fazladan bir sığ, önce genişlik taraması.
- **Neden** — Bazı NAS yolları ya da derin ağaçlar ilk taramadan sonra eksik görünür.
- **Kapalı** — Ancak onsuz tam bir dosya sayımı doğrulandıktan sonra.
- **CLI** — `--no-bfs` bu taramayı kapatır.

## Durum dosyasını sürdürün

İsteğe bağlı UTF-8 yolu. Başarılı hamleler `B64|` satırlarını ekler, böylece bir sonraki düzenleme çalıştırması bitmiş kaynakları atlayabilir.

- **Neden** — Durma veya çarpma sonrasında uzun işlere devam edin.
- **Varsayılan yol** — Çalışma zamanında alan boş olduğunda motor `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt`i kullanır. Çıkış olmadan uygulama profili altında `sessions\<id>\resume\OrganizeFiles.resume.txt` kullanılır.
- **Masaüstü kullanıcı arayüzü** — Fare seçimi ve kopyalama için salt okunur yol listesi. Varsayılan konumda bir devam durumu dosyası zaten mevcut olduğunda yol otomatik olarak görünür. **Gözat** bir günlük klasörü seçer ve sonuna `OrganizeFiles.resume.txt` ifadesini ekler. **Kaldır** yolu temizler. Boş olduğunda ipucu, çalışma zamanında kullanılan yolu gösterir.

## Yeni başlat

**gerçek** bir düzenleme çalıştırması başladığında devam durumu dosyasını kısaltır (prova çalıştırma kesilmez). **İlerleme durumunu ve çalışma alanını kaydet** seçeneği, çalıştırma başlangıcında kaydedilen kullanıcı arayüzü anlık görüntüsünü de temizler. **Neden** — Eski bir devam dosyası günlüğüne devam etmek yerine tam bir yeniden sayımı zorunlu kılın.

## Ekstra Benzersiz tarama kökleri

Satır başına bir klasör: dizine eklenecek ekstra **Benzersiz** ağaçlar (eski düzen, diğer cilt).

- **Neden** — Tekilleştirme, başka bir yerde düzenlenmiş olan dosyaları tekrar taşımadan görebilir.
- **Masaüstü kullanıcı arayüzü** — Satır başına kopyalama için salt okunur liste. **Ekle** seçilen bir klasörü ekler. **Kaldır** seçilen satırı siler (örneğin, NAS'teki eski bir `Uniques` ağacı).

## Ağı yeniden dene (saniye) / Ağ beklemeyi devre dışı bırak

Geçici ağ G/Ç'sini yeniden denemek için saniyeler.

- **Neden** — SMB dosya sunucuları boşta kalan oturumları bırakır. Düzenlemek ve onarmak için kullanılır.
- **Ağ beklemeyi devre dışı bırak** — Beklemeyi bırakın ve bunun yerine başarısız olun.

## Disk dolu yeniden deneme

(saniye) / Disk dolu beklemeyi devre dışı bırak

Çıkış biriminde yer kalmadığında aynı model. **Neden** — Uzun çalıştırmalar sırasında diski boşaltma zamanı.

## Ekran kartı şeritleri

Yalnızca gömülü **tam video denetimi** açıkken ve **Bulunan ekran kartını kullan** da açıkken geçerlidir. **0** üzerindeki bir değer, bulunan üreticiler (NVIDIA, AMD, Intel, Apple, taşınabilir) arasında koşut denetim için belirli bir şerit sayısı belirler. **0**, şerit sayısının kendiliğinden bulunması demektir, yalnızca işlemci demek değildir. Yalnızca işlemcide örnekleme için ekran kartı listesinden **Yalnızca CPU** seçeneğini seçin. Şerit etiketleri işlemcide bit akışı denetimini planlar. İşletim sisteminin donanımla video çözmesini çağırmaz.

- **Komut satırı ön ayarı** — Tam video denetimi çalışırken `--hwaccel <value>`, denetim şeritleri için bir ön ayar (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`) seçer.

## Karma okuma arabelleği

Karma oluşturma sırasında çalışan başına okuma arabelleği (512 KiB, 1 MiB, 8 MiB). **Neden** — Daha büyük arabellekler, NAS'in yavaşlamasına ve yüksek gecikme süreli paylaşımlara yardımcı olur.

## Geri alma günlüğünü kaydet

Çalıştırma için çıktı kökü altındaki taşımaların isteğe bağlı JSONL günlüğü.

- **Neden** — Gerçek bir çalıştırmadan sonra CLI ile geri almayı sağlar.
- **Arşiv** — Günlük etkinken düzenleme sonrası arşivleme kapalı kalır.
- **CLI** — `--record-undo-journal` (ana penceredeki onay kutusuyla aynı).

## Yazma çalıştırma sinyali JSON

İsteğe bağlı `Organize.Files.run.json` dosyasını `Output\_OrganizeMediaLogs` altına yazar.

- **Neden** — Dış araçlar, düzenleme ya da onarım sürerken canlı sayaçları (taranan, planlanan, tamamlanan) okuyabilir.
- **Yazma aralığı** — Kaynak taramaları boyunca görülen her 10.000 dosyada, her 5.000 eşleşmede ve yaklaşık 15 saniyede bir, doğrulama, karma alma ve taşıma sırasında her 1.000 dosyadan sonra en fazla 5 saniyede bir ve her büyük aşamada.
