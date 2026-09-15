# مساعد الذكاء الاصطناعي (MCP)

تربط الفرق المرخّصة **OrganizeFiles.Cli** بـ Claude Desktop أو **Cursor** أو VS Code Copilot أو عميل آخر لـ Model Context Protocol، ويُسمّى أدناه عميل MCP. الموصّل هو حزمة Python باسم **organize-files-mcp**. ويمكن تنزيله مجانًا من github.com/GutRaz/organize-files-docs، من المجلد `mcp/`.

**في تطبيق سطح المكتب:** افتح **إعداد MCP…** ضمن **التطبيق والبيانات** في عمود الخيارات، أو من قائمة الأدوات. اختر **وصول MCP**: **إيقاف** أو **المراقبة** أو **التحكم**. ثم انسخ مقتطف JSON. أعد تحميل MCP في تطبيق الذكاء الاصطناعي بعد كل تغيير في المستوى، لأن **التحكم** ينشئ رمزًا مميزًا جديدًا في كل مرة.

**اسأل مساعد التوثيق** "setup mcp" أو "cum setez mcp" لمعرفة الخطوات على النظام الحالي.

## مستويات وصول MCP، تُضبط في التطبيق

تطابق المستويات ثلاثة أنواع من العمل: **قراءة / معاينة / تنفيذ**.

| المستوى | نوع العمل | ما يمكن للذكاء الاصطناعي فعله |
|-------|--------|-------------------|
| **إيقاف** | — | فقط `organize_mcp_status`. لا تشخيص ولا وصول إلى مساحة العمل. |
| **المراقبة** | **قراءة** | كل ما في إيقاف، إضافة إلى تشخيصات للقراءة فقط، وسجل التشغيلات والمهام، والأقفال، وفحوص التدقيق، و **`organize_capabilities`** و **`organize_workspace_snapshot`**. تسرد `organize_capabilities` أوضاع التشغيل، ومنها **`ai`**، ونطاقات النقل والأهداف. وتعرض `organize_workspace_snapshot` مساحة العمل المحفوظة في النافذة الرئيسية. لا معاينة ولا تنفيذ. |
| **التحكم** | **معاينة** / **تنفيذ** | كل ما في المراقبة، إضافة إلى **`organize_create_job`** و **`organize_run_workspace`** و **`organize_remove_empty_organize_layout`**. يتطلب **رمز تحكم** في إعدادات MCP، وهو `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **المعاينة** هي `organize_run_workspace` عندما يكون **تشغيل تجريبي** مفعّلًا في مساحة العمل المحفوظة، فلا يُكتب شيء. **التنفيذ** هو الأداة نفسها عندما يكون تشغيل تجريبي متوقفًا، فتُنقل الملفات. لا يضيف الموصّل `--confirm-destructive` ما لم يضبط الاستدعاء `confirm_destructive=true`، ومن دون هذا الخيار يرفض سطر الأوامر بـ `confirm_destructive_required`. |

ملف التحكم هو **`mcp-control.json`**، بجوار `automation-jobs.json` في مجلد ملف التعريف الخاص بالتطبيق. لا يذكر المقتطف المنسوخ هذا الملف، لأن الموصّل يجده في مجلد ملف التعريف الافتراضي. اضبط **`ORGANIZE_FILES_MCP_CONTROL_FILE`** فقط عندما يكون الملف في مكان آخر. في **التحكم**، يضبط المقتطف أيضًا **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`**.

**يتطلب النقل والحذف خطوة ثانية يقوم بها إنسان.** يضبط المساعد تأكيده بنفسه، لذا قد يقنع نصٌّ يقرؤه المساعدُ المساعدَ بالتأكيد. لذلك يحتاج التشغيل الذي ليس تجريبيًا أيضًا إلى نافذة زمنية تُفتح من **إعداد MCP**، وتُغلق هذه النافذة من تلقاء نفسها بعد 15 دقيقة. وخارج هذه النافذة يظل بإمكان المساعد تحضير تشغيل ومعاينته، لكن التشغيل نفسه يُرفض. ملف التحكم والنافذة كلاهما موقّع بمفتاح تحتفظ به هذه النسخة المثبتة. ملف التحكم الذي عُدِّل يدويًا أو نُسخ من جهاز آخر يُعدّ في مستوى إيقاف.

## أدوات MCP حسب المستوى

**دائمًا، حتى في إيقاف:** `organize_mcp_status`

**المراقبة والتحكم:** `organize_server_info`، `organize_cli_help`، `organize_query_runs`، `organize_show_run`، `organize_list_running`، `organize_query_jobs`، `organize_due_pass_lock_status`، `organize_output_lock_status`، `organize_verify_audit`، `organize_exit_code_guide`، و `organize_run_raw_cli` التي لا تقبل إلا أوامر القراءة.

**أيضًا في المراقبة والتحكم:** `organize_capabilities` التي تسرد وضع التشغيل **`ai`** لملفات الذكاء الاصطناعي وتعلّم الآلة، و `organize_workspace_snapshot`.

**التحكم فقط:** `organize_create_job` من مساحة العمل أو من JSON لمهمة، و `organize_run_workspace` لمعاينة أو تشغيل حقيقي بحسب إعداد تشغيل تجريبي في مساحة العمل، و `organize_remove_empty_organize_layout` التي تزيل مجلدات التخطيط الفارغة داخل مخرج موجود ولا تنشئ مجلد المخرج نفسه أبدًا.

الأوامر التي تنقل الملفات أو تحذفها محظورة دائمًا عبر MCP خارج مستوى **التحكم**. ولا يسمح بها أي إعداد آخر.

## خيارات سطر الأوامر التي يستخدمها الموصّل

| الخيار | المستوى | الغرض |
|------|-------|---------|
| `--mcp-control-status` | أي مستوى | JSON فيه المستوى ومسار ملف التحكم وعلامتا المراقبة والتحكم |
| `--mcp-capabilities` | المراقبة فما فوق | قائمة JSON بأوضاع التشغيل، ومنها **`ai`**، ونطاقات النقل والأهداف |
| `--mcp-workspace-snapshot` | المراقبة فما فوق | مساحة العمل المحفوظة وكيف تصبح مهمة |
| `--mcp-create-job` | التحكم | إنشاء مهمة بـ `--from-workspace` أو `--mcp-job-json` |
| `--mcp-run-workspace` | التحكم | تشغيل مساحة العمل المحفوظة مع `--allow-app-target` و `--mcp-control-token` |
| `--remove-empty-organize-layout` | التحكم | إزالة مجلدات التخطيط الفارغة داخل `--output` موجود |
| `--confirm-destructive` | التحكم | مطلوب مع `--mcp-run-workspace` لتشغيل ينقل أو يحذف. لا يمرّره الموصّل إلا عند `confirm_destructive=true` |

## الإعدادات في JSON عميل MCP

| الإعداد | متى |
|----------|------|
| `ORGANIZE_FILES_CLI` | مسار OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | مسار `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | مسار `mcp-control.json`، فقط عندما لا يكون الملف في مجلد ملف التعريف الافتراضي |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | مستوى **التحكم** فقط، من مقتطف التطبيق |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | مستوى **التحكم**، لتشغيلات مساحة العمل المحفوظة |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | اختياري. الرمز نفسه الذي يستخدمه المضيف لعمليات القراءة |

## الإعداد على Windows

1. **Python 3.10 أو أحدث** — شغّل `python -V` في PowerShell. إذا لم يكن Python موجودًا أو كان أقدم، فثبّته من [python.org](https://www.python.org/downloads/) وحدّد **Add python.exe to PATH**.
2. **نزّل الموصّل وثبّته** — نزّل github.com/GutRaz/organize-files-docs كملف ZIP، وفك ضغطه، وشغّل `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1`. ينشئ السكربت بيئة Python خاصة بالموصّل ويطبع الأمر لتطبيق الذكاء الاصطناعي.
3. **في التطبيق:** **إعداد MCP…**، اختر **المراقبة** أو **التحكم**، ثم انسخ JSON.
4. **المسارات:** يحتوي `%LocalAppData%\OrganizeFilesCrossPlatform\` على المهام و `mcp-control.json`. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **الاختبار** — شغّل `organize_mcp_status`، ثم `organize_server_info`. يجب أن تكون قيمة `cliResolved` هي true، وأن يطابق `mcpLevel` التطبيق.

## الإعداد على macOS

الخطوات نفسها مع **python3** و `bash mcp/install-organize-files-mcp.sh`. إذا أظهر `python3 -V` الإصدار 3.9 أو لم يوجد Python إطلاقًا، فثبّت Python أولًا من [python.org](https://www.python.org/downloads/macos/). المسارات: `~/Library/Application Support/OrganizeFilesCrossPlatform/`، `~/.cursor/mcp.json`، Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## الإعداد على Linux

الخطوات نفسها مع **python3** و `bash mcp/install-organize-files-mcp.sh`. على Debian و Ubuntu، شغّل أولًا `sudo apt install python3-venv`. المسارات: `~/.local/share/OrganizeFilesCrossPlatform/`، أو `$XDG_DATA_HOME` عند ضبطه، `~/.cursor/mcp.json`، Claude `~/.config/Claude/claude_desktop_config.json`.

## الأمان

- يعمل MCP باسم **المستخدم المحلي** لنظام التشغيل، وبالصلاحيات نفسها التي لسطر الأوامر عند تشغيله يدويًا.
- احتفظ بسرية **رمز التحكم** و **رمز القراءة** مثل كلمات المرور. انسخ JSON من جديد بعد تشغيل التحكم.
- يعمل **`organize_run_workspace`** في سطر الأوامر، لا عبر زر تشغيل في التطبيق. لا تشغّل مهمتين على مجلد المخرج نفسه في الوقت نفسه.
- أمثلة: `mcp/examples/`.

## التشغيلات التي تنقل أو تحذف

يتطلب `--mcp-run-workspace` الخيار `--confirm-destructive` لكل تشغيل ليس تجريبيًا، سواء نقل أو حذف أو أرشف. ومن دون هذا الخيار يجيب سطر الأوامر بـ `confirm_destructive_required`. لا يضيف الموصّل هذا الخيار ما لم يضبط الاستدعاء `confirm_destructive=true`، ولا يستطيع ذلك إلا مستوى التحكم. لذلك يرفض الموصّل افتراضيًا.

## اللغات

تأتي إجابات الإعداد من الدليل المترجم نفسه الذي تستخدمه نافذة التوثيق و مساعد الدليل. يُبلغ `organize_capabilities` عن أوضاع التشغيل والأهداف، لا عن أسماء سمات التطبيق.
