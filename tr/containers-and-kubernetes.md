# Kapsayıcılar — kurulum

## Ne gerekli?

İşi çalıştıran makinede yalnızca `docker` veya `kubectl` programının erişilebilir olması gerekir. Başka hiçbir şeye gerek yok. Docker Masaüstü bir gereklilik değildir. Linux'ta Docker Engine, Rancher Desktop, colima ve docker uyumlu komuta sahip Podman'ın tümü aynı şekilde çalışır, çünkü uygulama yalnızca sistem yolunda bulduğu komutu çalıştırır.

Kubernetes aynı şekilde çalışır. K3s, kind, minikube ve EKS, GKE veya AKS gibi yönetilen kümeler dahil olmak üzere `kubectl` aracılığıyla erişilebilen tüm kümeler desteklenir.

## Farklı bir arka plan programı veya küme kullanma

İşleri başka bir Docker arka plan programına göndermek için `DOCKER_HOST` ayarlayın veya `docker context use` ile geçiş yapın. Başka bir Kubernetes kümesi kullanmak için geçerli bağlamı `kubectl config use-context` ile değiştirin. Uygulama, komut satırının halihazırda kullandığı her şeyi takip eder, dolayısıyla uygulamanın içinde ekstra bir ayar yapılmasına gerek yoktur.

## Dosyaların bağlandığı yer

Kubernetes için klasör iki yoldan biriyle eklenir. Yerel geliştirme bağlamları doğrudan ana bilgisayar klasörüne bağlanır. Bu, `desktop`, `colima` veya `orbstack` adlı bir bağlamı, `@desktop` ile biten bir bağlamı, `kind-`, `minikube` veya `k3d-` ile başlayan bir bağlamı ve adında `docker-desktop`, `docker-for-desktop` veya `rancher-desktop` geçen bir bağlamı kapsar. Gerçek bir küme düğümü masaüstü makinedeki klasörleri göremediği için diğer tüm bağlamlar gerçek bir küme olarak ele alınır ve bunun yerine kalıcı bir birim talebi alır. `ORGANIZE_FILES_K8S_VOLUME_MODE` değerini `pvc` veya `hostpath` yapmak bu seçimi her bağlam için geçersiz kılar.

## Windows'ta ağ klasörleri

Windows'taki Docker Desktop, bir Linux kapsayıcısına `\\server\share` gibi bir ağ yolu ekleyemez. Windows klasörü görüyor ancak kapsayıcı görmüyor. Bunu aşmanın iki yolu var. Yerel diskteki bir klasörü kullanın veya işi, çalışmayı uygulamanın kendisinde yapan Uygulama hedefiyle çalıştırın. Paylaşıma eşlenmiş bir sürücü harfi işe yaramaz, çünkü uygulama onu ağ yoluna kadar izler ve aynı şekilde reddeder.

## Hazır dosyalar

Linux komut satırı setleri, `containers` klasöründe hazır dosyalar içerir: imajı doğrudan setin kendisinden derleyen bir Dockerfile, bir Compose örneği, Kubernetes Job örnekleri ve yanında her dil için bir README bulunan `containers/README.md`.

# Konteynerler ve CLI worker'ları

## Zamanlanmış işler — Docker ve Kubernetes hedefleri

Ana pencere kenar çubuğundan **İşler**'i açın. Mevcut bir kartta **Yeni görev** veya **Düzenle**'yi tıklayın. **Hedef** açılır menüsünde **Docker komutunu** veya **Kubernetes işini** seçin.

1. **Kaynaklar** (ana bilgisayar yolları) ve **Çıktı**'yı (ana bilgisayar yolu — iş çalıştırılmadan önce mevcut olmalıdır) ayarlayın.
2. Diğer işlerde olduğu gibi **Mod** ve **Çalıştırma seçeneklerini** seçin.
3. **Komut önizlemesi** paneli, uygulanacak tam "docker run" komutunu veya Kubernetes İş YAML'sini gösterir.
4. İşi **kaydedin** ve bir **Zamanlama** ayarlayın veya hemen başlamak için kartta **Şimdi çalıştır** seçeneğini tıklayın.

Uygulama, kaydedilen anlık görüntüden otomatik olarak bağlama işaretlerini ve birim yollarını oluşturur. Docker arka plan programı veya "kubectl" ana makinede erişilebilir olmalıdır. **Ön kontrol** bağlantıyı kontrol eder ve çalıştırma başlamadan önce iş günlüğündeki hataları bildirir. Onay akışı, günlük alımı ve arayüzsüz planlama için **Zamanlanan işler**'e bakın.

## Ana makinenin uçbirimi (PowerShell / bash / cmd)

Evet — ana makinede **OrganizeFiles.Cli** uygulamasını PowerShell, bash ya da cmd üzerinden çalıştırın. Desteklenen uçbirim yolu budur. Avalonia masaüstü penceresi ayrı bir grafik arayüzdür. CLI takımını uygulamanın yanına (ya da PATH üzerine) yayımlayın veya kurun, ardından **--source** (yinelenebilir), **--output** ve **--mode** değerlerini geçirin. Önce deneme çalıştırması yapmak yerinde olur. **--execute** seçeneğini ancak hazır olduğunuzda ekleyin.

## Masaüstü arayüzü ve kapsayıcılar

Konteynerler ve otomasyon: Avalonia masaüstü GUI'sinin tipik bir headless Linux konteynerinde çalışması amaçlanmamıştır. Birkaç paralel çalışan da dahil olmak üzere bir veya daha fazla yalıtılmış iş için OrganizeFiles.Cli tamamlayıcısını kullanın: her kapsayıcıda, prova önizleme işleri için salt okunur kaynak klasörleri bağlayın. **--execute** ile yapılan gerçek hareketler, yazılabilir bir kaynak bağlantısı gerektirir çünkü motor, dosyaları kaynak ağacın dışına taşır. Özel bir okuma/yazma çıkış birimi kullanın, tüm düzenleme/onarım işlemleri (deneme çalıştırması ve yürütme) için geçerli mağaza veya yayıncı yetkisine sahip olduğunuzdan emin olun, **--source** (tekrarlanabilir), **--output** ve **--mode**'yi iletin. Her eşzamanlı çalışanın kendi çıkış köküne ihtiyacı vardır. Docker veya Kubernetes işleri çalıştırılmadan önce **Output** klasörünün ana bilgisayarda zaten mevcut olması gerekir (ön kontrol, eksik bir hedefi reddeder ve onu oluşturmaz). Örnek yollar: containers/README.md ve containers/docker-compose.sample.yml. Jobs/JobAgent oluşturulan `docker run`, kaynakları `/in1`, `/in2`, …'ye bağlar ve `/out`'de çıktı verir. Manuel tek kaynaklı örneklerde `/in` kullanılabilir (bkz. containers/README.md).
