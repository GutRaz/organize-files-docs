# CLI, Docker ve Kubernetes (referans düzeni)

## CLI otomasyonu

Bu bölüm Microsoft/HashiCorp stilini takip etmektedir: kullanım satırı, bayrak tablosu (İngilizce belirteçler), ardından kopyala-yapıştır örnekleri.

CLI (OrganizeFiles.Cli)
  KULLANIM: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  KULLANIM: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Bayrak (uzun) | Anlamı
  --------------------------|----------------------------
  --execute | Gerçek hareketler (varsayılan yalnızca provadır).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | B64| ile UTF-8 devam durumu dosyası çizgiler.
  --delete-duplicates | Yinelenen adayları silin (--confirm-delete ile --execute gerekir).
  --delete-issues | Sorun grubu adaylarını silin (--execute ile --confirm-delete gerekir). Uzak otomasyon hedeflerinde değil.
  --archive-after-organize | Düzenlemeden sonra: dosya başına kardeş ZIP'i, ardından orijinalleri silin (--execute ile --confirm-delete gerekir). Zaten arşivlenmiş olan uzantıları atlar.

  **Not:** CLI `--mode models` AI yapıtlarını değil **CAD / 3D modelleri** seçer. AI / ML için `--mode ai` veya `--mode models-ai` kullanın.

  Örnek (deneme çalıştırması, tüm kovalar): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Örnek (yalnızca Benzersiz hareketler, yürütme): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Derleme: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Deneme çalışması: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  --execute için, :ro'yu kaynak montajından kaldırın. Çok workerli kurallar için bkz. containers/README.md (worker başına bir çıkış kökü).

Kubernetes (referans İşi)
  Salt okunur kaynak PVC'ler deneme çalıştırması işleri için geçerlidir. --execute ile gerçek hareketler yazılabilir kaynak PVC'lere ihtiyaç duyar. Tüm düzenleme/onarım işlemleri (prova çalıştırma ve yürütme) için geçerli mağaza veya yayıncı yetkisi sağlayın. Çıkış ağacı başına bir Pod. Minimal bir model, örnek bildirimin yanı sıra containers/README.md'te belgelenmiştir.

İş ilerlemesi
  İşler penceresi App, CLI, Docker ve Kubernetes çalıştırmaları için ilerleme gösterir. Toplamı bilinen aşamalar yüzde gösterir. Toplamı olmayan taramalar belirsiz kalır.
  Otomasyon, CLI worker'ını ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 ile başlatır ve o işaret satırlarını görünen günlükten çıkarır. Elle başlatılan bir CLI çalıştırması, o değişken ayarlanmadıkça işaret yaymaz.
  Docker ve Kubernetes worker'ları aynı değişkeni alır, bu yüzden o çalıştırmalar da yüzde bildirir. Rakam, worker'ın günlüğünden okunur, bu yüzden konteyner veya pod yazmaya başladığında görünür.
  --list-running ve --show-run, çalıştırma bir şey bildirdiğinde etkin işler için ilerleme alanları taşır.

# Çalıştırma örnekleri

## Grafiksel kullanıcı arayüzü

**Kaynaklar** ve çıktı klasörünü ekleyin, çalıştırma modunu seçin, önizleme için **Deneme çalıştırması** seçeneğini açın ve ardından **Çalıştır** düğmesine basın. Gerçek taşımalar için **Deneme çalıştırması** seçeneğini kapalı bırakın. Silme seçenekleri çalıştırmadan önce onay ister.

## CLI örnekleri

CLI Deneme çalıştırması: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
