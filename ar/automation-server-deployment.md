# CLI وDocker وKubernetes (التخطيط المرجعي)

## أتمتة سطر الأوامر

يتبع هذا الفصل أسلوب Microsoft/HashiCorp: سطر الاستخدام، وجدول العلامات (الرموز الإنجليزية)، ثم أمثلة النسخ واللصق.

سطر الأوامر (OrganizeFiles.Cli)
  الاستخدام: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  الاستخدام: OrganizeFiles.Cli --output <dir> --mode repair [options]

  علم (طويل) | معنى
  -------------------------|----------------------------------------
  --execute | التحركات الحقيقية (الافتراضي هو التشغيل التجريبي فقط).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | ملف حالة الاستئناف UTF-8 مع B64| خطوط.
  --delete-duplicates | احذف المرشحين المكررين (يحتاج إلى --confirm-delete مع --execute).
  --delete-issues | احذف مجموعة الإصدارات المرشحة (يحتاج إلى --confirm-delete مع --execute). ليس على أهداف الأتمتة عن بعد.
  --archive-after-organize | بعد التنظيم: لكل ملف ZIP للأخ، ثم احذف النسخ الأصلية (يحتاج إلى --confirm-delete مع --execute). يتخطى ملحقات الأرشيف بالفعل.

  **ملاحظة:** يحدد CLI `--mode models` **نماذج CAD / ثلاثية الأبعاد**، وليس عناصر الذكاء الاصطناعي. استخدم `--mode ai` أو `--mode models-ai` لـ AI / ML.

  مثال (التشغيل التجريبي، جميع الجرافات): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  مثال (فقط الحركات الفريدة، التنفيذ): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  البناء: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  التشغيل التجريبي: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  بالنسبة إلى --execute ، قم بإزالة :ro من قاعدة التثبيت المصدر. راجع containers/README.md لمعرفة قواعد تعدد workers (جذر إخراج واحد لكل worker).

Kubernetes (الوظيفة المرجعية)
  تعد PVCs المصدر للقراءة فقط صالحة للمهام التجريبية. تحتاج الحركات الحقيقية مع --execute إلى مصدر PVC قابل للكتابة. قم بتوفير استحقاق صالح للمتجر أو الناشر لجميع عمليات التنظيم/الإصلاح (التشغيل التجريبي والتنفيذ). جراب واحد لكل شجرة إخراج. تم توثيق الحد الأدنى من النموذج في containers/README.md جنبًا إلى جنب مع نموذج البيان.

تقدم المهام
  تعرض نافذة المهام التقدم لعمليات التشغيل App وCLI وDocker وKubernetes. المراحل ذات الإجمالي المعروف تعرض نسبة مئوية. الفحوصات بلا إجمالي تبقى غير محددة.
  تبدأ الأتمتة worker CLI بالمتغير ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 وتزيل أسطر العلامات تلك من السجل المرئي. عملية CLI التي تبدأ يدويًا لا تصدر أي علامات ما لم يُضبط ذلك المتغير.
  يتلقى workers Docker وKubernetes المتغير نفسه، لذلك تعرض تلك العمليات نسبة مئوية أيضًا. يُقرأ الرقم من سجل الـworker، لذلك يظهر بمجرد أن تبدأ الحاوية أو الـpod في الكتابة.
  يحمل --list-running و--show-run حقول تقدم للمهام النشطة عندما تكون العملية قد أبلغت عن شيء.

# تشغيل الأمثلة

## واجهة المستخدم الرسومية

أضف **مصادر** ومجلد الإخراج، واختر وضع التشغيل، وفعّل **التشغيل التجريبي** للمعاينة، ثم اضغط **تشغيل**. اترك **التشغيل التجريبي** معطّلاً لتنفيذ النقل الفعلي. تطلب خيارات الحذف تأكيداً قبل التنفيذ.

## أمثلة CLI

CLI تشغيل تجريبي: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
