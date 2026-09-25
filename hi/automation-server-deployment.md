# CLI, Docker और Kubernetes (संदर्भ लेआउट)

## CLI स्वचालन

यह अध्याय Microsoft/HashiCorp शैली का अनुसरण करता है: उपयोग पंक्ति, ध्वज तालिका (अंग्रेजी टोकन), फिर उदाहरणों को कॉपी-पेस्ट करें।

CLI (OrganizeFiles.Cli)
  उपयोग: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  उपयोग: OrganizeFiles.Cli --output <dir> --mode repair [options]

  झंडा (लंबा) | मतलब
  --------------------------------|------------------------------------------------
  --execute | वास्तविक चालें (डिफ़ॉल्ट केवल ड्राई-रन है)।
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | B64| के साथ UTF-8 रीज़्यूम स्थिति फ़ाइल पंक्तियाँ.
  --delete-duplicates | डुप्लिकेट उम्मीदवारों को हटाएं (--execute के साथ --confirm-delete की आवश्यकता है)।
  --delete-issues | समस्या-बकेट उम्मीदवारों को हटाएं (--execute के साथ --confirm-delete की आवश्यकता है)। दूरस्थ स्वचालन लक्ष्य पर नहीं.
  --archive-after-organize | व्यवस्थित करने के बाद: प्रति-फ़ाइल सिबलिंग ZIP फिर मूल हटाएं (--execute के साथ --confirm-delete की आवश्यकता है)। पहले से संग्रहित एक्सटेंशन को छोड़ देता है।

  **ध्यान दें:** CLI `--mode models` **CAD/3D मॉडल** का चयन करता है, AI कलाकृतियों का नहीं। AI/ML के लिए `--mode ai` या `--mode models-ai` का उपयोग करें।

  उदाहरण (ड्राई-रन, सभी बकेट): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  उदाहरण (केवल अद्वितीय चालें, निष्पादित करें): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  बिल्ड: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  ड्राई-रन: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  --execute के लिए, स्रोत माउंट से :ro हटा दें। मल्टी-वर्कर नियमों (प्रति वर्कर एक आउटपुट रूट) के लिए containers/README.md देखें।

Kubernetes (संदर्भ कार्य)
  ड्राई-रन कार्यों के लिए रीड-ओनली सोर्स PVC मान्य हैं। --execute के साथ वास्तविक चालों के लिए लिखने योग्य स्रोत PVC की आवश्यकता होती है। सभी व्यवस्थित/मरम्मत रन (ड्राई-रन और निष्पादन) के लिए वैध स्टोर या प्रकाशक पात्रता प्रदान करें। प्रति आउटपुट ट्री एक पॉड। एक नमूना मैनिफ़ेस्ट के साथ containers/README.md में एक न्यूनतम पैटर्न प्रलेखित किया गया है।

कार्य प्रगति
  कार्य विंडो App, CLI, Docker और Kubernetes रन की प्रगति दिखाती है। ज्ञात कुल वाले चरण प्रतिशत दिखाते हैं। बिना कुल वाली स्कैन अनिश्चित रहती हैं।
  स्वचालन CLI वर्कर को ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 के साथ शुरू करता है और उन चिह्न पंक्तियों को दृश्य लॉग से हटा देता है। हाथ से शुरू किया गया CLI रन तब तक कोई चिह्न नहीं भेजता जब तक वह चर सेट न हो।
  Docker और Kubernetes वर्कर को वही चर मिलता है, इसलिए ये रन भी प्रतिशत बताते हैं। यह आँकड़ा वर्कर के लॉग से पढ़ा जाता है, इसलिए यह तब दिखता है जब कंटेनर या पॉड लिखना शुरू करता है।
  --list-running और --show-run सक्रिय कार्यों के लिए प्रगति फ़ील्ड रखते हैं, जब रन ने कुछ बताया हो।

# रन के उदाहरण

## Graphical UI

**सूत्रों का कहना है** और आउटपुट फ़ोल्डर जोड़ें, रन मोड चुनें, पूर्वावलोकन के लिए **ड्राई रन** चालू करें, फिर **चलाएँ** दबाएँ। वास्तविक स्थानांतरण के लिए **ड्राई रन** बंद रहने दें। विलोपन विकल्प निष्पादन से पहले पुष्टि माँगते हैं।

## CLI उदाहरण

CLI ड्राई रन: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
