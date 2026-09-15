# AI सहायक (MCP)

लाइसेंस वाली टीमें **OrganizeFiles.Cli** को Claude Desktop, **Cursor**, VS Code Copilot या किसी अन्य Model Context Protocol क्लाइंट से जोड़ती हैं, जिसे नीचे MCP क्लाइंट कहा गया है। कनेक्टर Python पैकेज **organize-files-mcp** है। इसे github.com/GutRaz/organize-files-docs के `mcp/` फ़ोल्डर से मुफ़्त डाउनलोड किया जा सकता है।

**डेस्कटॉप ऐप में:** विकल्प कॉलम में **अनुप्रयोग और डेटा** के नीचे, या टूल मेनू से **MCP सेटअप...** खोलें। **MCP पहुंच** चुनें: **बंद**, **मॉनिटर** या **नियंत्रण**। फिर JSON स्निपेट कॉपी करें। हर बार स्तर बदलने के बाद AI ऐप में MCP फिर से लोड करें, क्योंकि **नियंत्रण** हर बार नया टोकन बनाता है।

**दस्तावेज़ सहायक से पूछें** "setup mcp" या "cum setez mcp", ताकि मौजूदा सिस्टम के चरण मिलें।

## MCP पहुंच स्तर, ऐप में सेट किए जाते हैं

स्तर तीन तरह के काम से मेल खाते हैं: **पढ़ना / पूर्वावलोकन / निष्पादन**।

| स्तर | काम का प्रकार | AI क्या कर सकता है |
|-------|--------|-------------------|
| **बंद** | — | केवल `organize_mcp_status`। कोई निदान नहीं और कार्यक्षेत्र तक कोई पहुंच नहीं। |
| **मॉनिटर** | **पढ़ना** | बंद की सभी सुविधाएँ, साथ में केवल पढ़ने वाला निदान, रन और कार्य इतिहास, लॉक, ऑडिट जांच, **`organize_capabilities`** और **`organize_workspace_snapshot`**। `organize_capabilities` रन मोड की सूची देता है, जिनमें **`ai`** भी है, साथ ही मूव स्कोप और लक्ष्य। `organize_workspace_snapshot` मुख्य विंडो में सहेजा गया कार्यक्षेत्र दिखाता है। कोई पूर्वावलोकन नहीं और कोई निष्पादन नहीं। |
| **नियंत्रण** | **पूर्वावलोकन** / **निष्पादन** | मॉनिटर की सभी सुविधाएँ, साथ में **`organize_create_job`**, **`organize_run_workspace`** और **`organize_remove_empty_organize_layout`**। इसके लिए MCP सेटिंग्स में **नियंत्रण टोकन** चाहिए, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`। **पूर्वावलोकन** का मतलब है `organize_run_workspace` जब सहेजे गए कार्यक्षेत्र में **ड्राई रन** चालू हो, इसलिए कुछ भी लिखा नहीं जाता। **निष्पादन** वही टूल है जब ड्राई रन बंद हो, इसलिए फ़ाइलें मूव होती हैं। जब तक कॉल `confirm_destructive=true` सेट न करे, कनेक्टर `--confirm-destructive` नहीं जोड़ता, और इस फ़्लैग के बिना कमांड लाइन `confirm_destructive_required` के साथ मना कर देती है। |

नियंत्रण फ़ाइल **`mcp-control.json`** है, जो ऐप के प्रोफ़ाइल फ़ोल्डर में `automation-jobs.json` के बगल में रहती है। कॉपी किया गया स्निपेट इस फ़ाइल का नाम नहीं लेता, क्योंकि कनेक्टर इसे डिफ़ॉल्ट प्रोफ़ाइल फ़ोल्डर में खुद ढूंढ लेता है। **`ORGANIZE_FILES_MCP_CONTROL_FILE`** केवल तब सेट करें जब फ़ाइल कहीं और हो। **नियंत्रण** पर स्निपेट **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`** भी सेट करता है।

**फ़ाइलें मूव करने और हटाने के लिए दूसरा, इंसानी चरण चाहिए।** सहायक अपनी पुष्टि खुद सेट करता है, इसलिए सहायक द्वारा पढ़ा गया पाठ सहायक को पुष्टि करने के लिए मना सकता है। इसलिए जो रन ड्राई रन नहीं है, उसे **MCP सेटअप** में खोली गई समय-सीमा भी चाहिए, और यह समय-सीमा 15 मिनट बाद अपने आप बंद हो जाती है। इस समय-सीमा के बाहर सहायक फिर भी रन तैयार कर सकता है और रन का पूर्वावलोकन कर सकता है, पर रन खुद अस्वीकार हो जाता है। नियंत्रण फ़ाइल और समय-सीमा दोनों इस इंस्टॉलेशन की रखी हुई कुंजी से हस्ताक्षरित होती हैं। हाथ से बदली गई या किसी दूसरे कंप्यूटर से कॉपी की गई नियंत्रण फ़ाइल बंद मानी जाती है।

## स्तर के अनुसार MCP टूल

**हमेशा, बंद पर भी:** `organize_mcp_status`

**मॉनिटर और नियंत्रण:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` और `organize_run_raw_cli`, जो केवल पढ़ने वाले कमांड स्वीकार करता है।

**मॉनिटर और नियंत्रण में यह भी:** `organize_capabilities`, जो AI और ML फ़ाइलों के लिए रन मोड **`ai`** की सूची देता है, और `organize_workspace_snapshot`।

**केवल नियंत्रण:** कार्यक्षेत्र से या कार्य JSON से `organize_create_job`, कार्यक्षेत्र के ड्राई रन के अनुसार पूर्वावलोकन या असली रन के लिए `organize_run_workspace`, और `organize_remove_empty_organize_layout`, जो किसी मौजूदा आउटपुट के अंदर खाली लेआउट फ़ोल्डर हटाता है और आउटपुट फ़ोल्डर खुद कभी नहीं बनाता।

फ़ाइलें मूव करने या हटाने वाले कमांड **नियंत्रण** स्तर के बाहर MCP से हमेशा रोके जाते हैं। कोई दूसरी सेटिंग इन कमांड की अनुमति नहीं देती।

## कनेक्टर जो कमांड लाइन फ़्लैग इस्तेमाल करता है

| फ़्लैग | स्तर | उद्देश्य |
|------|-------|---------|
| `--mcp-control-status` | कोई भी | स्तर, नियंत्रण फ़ाइल का पथ और मॉनिटर व नियंत्रण फ़्लैग वाला JSON |
| `--mcp-capabilities` | मॉनिटर और ऊपर | रन मोड की JSON सूची, जिनमें **`ai`** भी है, साथ ही मूव स्कोप और लक्ष्य |
| `--mcp-workspace-snapshot` | मॉनिटर और ऊपर | सहेजा गया कार्यक्षेत्र और कार्यक्षेत्र कार्य में कैसे बदलता है |
| `--mcp-create-job` | नियंत्रण | `--from-workspace` या `--mcp-job-json` से कार्य बनाएँ |
| `--mcp-run-workspace` | नियंत्रण | सहेजा गया कार्यक्षेत्र `--allow-app-target` और `--mcp-control-token` के साथ चलाएँ |
| `--remove-empty-organize-layout` | नियंत्रण | किसी मौजूदा `--output` के अंदर खाली लेआउट फ़ोल्डर हटाएँ |
| `--confirm-destructive` | नियंत्रण | मूव करने या हटाने वाले रन के लिए `--mcp-run-workspace` के साथ ज़रूरी। कनेक्टर इसे केवल `confirm_destructive=true` होने पर भेजता है |

## MCP क्लाइंट JSON में सेटिंग्स

| सेटिंग | कब |
|----------|------|
| `ORGANIZE_FILES_CLI` | OrganizeFiles.Cli का पथ |
| `ORGANIZE_FILES_JOBS_FILE` | `automation-jobs.json` का पथ |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | `mcp-control.json` का पथ, केवल तब जब फ़ाइल डिफ़ॉल्ट प्रोफ़ाइल फ़ोल्डर में न हो |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | केवल **नियंत्रण** स्तर, ऐप के स्निपेट से |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | **नियंत्रण** स्तर, सहेजे गए कार्यक्षेत्र के रन के लिए |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | वैकल्पिक। वही टोकन जो होस्ट पढ़ने के कार्यों के लिए इस्तेमाल करता है |

## Windows सेटअप

1. **Python 3.10 या नया** — PowerShell में `python -V` चलाएँ। अगर Python नहीं है या पुराना है, तो [python.org](https://www.python.org/downloads/) से इंस्टॉल करें और **Add python.exe to PATH** पर टिक करें।
2. **कनेक्टर डाउनलोड और इंस्टॉल करें** — github.com/GutRaz/organize-files-docs को ZIP के रूप में डाउनलोड करें, ZIP खोलें और `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1` चलाएँ। स्क्रिप्ट कनेक्टर के लिए अलग Python वातावरण बनाती है और AI ऐप के लिए कमांड दिखाती है।
3. **ऐप में:** **MCP सेटअप...**, **मॉनिटर** या **नियंत्रण** चुनें, फिर JSON कॉपी करें।
4. **पथ:** `%LocalAppData%\OrganizeFilesCrossPlatform\` में कार्य और `mcp-control.json` रहते हैं। Cursor: `%USERPROFILE%\.cursor\mcp.json`। Claude: `%APPDATA%\Claude\claude_desktop_config.json`। VS Code: `%USERPROFILE%\.vscode\mcp.json`।
5. **परीक्षण** — `organize_mcp_status` चलाएँ, फिर `organize_server_info`। `cliResolved` true होना चाहिए और `mcpLevel` ऐप से मेल खाना चाहिए।

## macOS सेटअप

वही चरण **python3** और `bash mcp/install-organize-files-mcp.sh` के साथ। अगर `python3 -V` 3.9 दिखाए या Python बिल्कुल न हो, तो पहले [python.org](https://www.python.org/downloads/macos/) से Python इंस्टॉल करें। पथ: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`।

## Linux सेटअप

वही चरण **python3** और `bash mcp/install-organize-files-mcp.sh` के साथ। Debian और Ubuntu पर पहले `sudo apt install python3-venv` चलाएँ। पथ: `~/.local/share/OrganizeFilesCrossPlatform/`, या सेट होने पर `$XDG_DATA_HOME`, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`।

## सुरक्षा

- MCP ऑपरेटिंग सिस्टम के **स्थानीय उपयोगकर्ता** के रूप में चलता है, उन्हीं अधिकारों के साथ जो हाथ से चलाई गई कमांड लाइन के होते हैं।
- **नियंत्रण टोकन** और **पढ़ने का टोकन** पासवर्ड की तरह गुप्त रखें। नियंत्रण चालू करने के बाद JSON फिर से कॉपी करें।
- **`organize_run_workspace`** ऐप के चलाएँ बटन से नहीं, कमांड लाइन में चलता है। एक ही आउटपुट फ़ोल्डर पर एक साथ दो कार्य न चलाएँ।
- उदाहरण: `mcp/examples/`।

## ऐसे रन जो मूव करते या हटाते हैं

`--mcp-run-workspace` को हर उस रन के लिए `--confirm-destructive` चाहिए जो ड्राई रन नहीं है, चाहे रन मूव करे, हटाए या आर्काइव करे। इस फ़्लैग के बिना कमांड लाइन `confirm_destructive_required` जवाब देती है। जब तक कॉल `confirm_destructive=true` सेट न करे, कनेक्टर यह फ़्लैग नहीं जोड़ता, और ऐसा केवल नियंत्रण स्तर कर सकता है। इसलिए डिफ़ॉल्ट रूप से कनेक्टर मना करता है।

## भाषाएँ

सेटअप के जवाब उसी अनुवादित गाइड से आते हैं जिससे दस्तावेज़ विंडो और मार्गदर्शक सहायक के जवाब आते हैं। `organize_capabilities` रन मोड और लक्ष्य बताता है, ऐप की थीम के नाम नहीं।
