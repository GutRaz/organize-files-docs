# CLI, Docker และ Kubernetes (เค้าโครงอ้างอิง)

## CLI อัตโนมัติ

บทนี้เป็นไปตามสไตล์ของ Microsoft/HashiCorp: บรรทัดการใช้งาน ตารางสถานะ (โทเค็นภาษาอังกฤษ) จากนั้นคัดลอกและวางตัวอย่าง

คลี (OrganizeFiles.Cli)
  การใช้งาน: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  การใช้งาน: OrganizeFiles.Cli --output <dir> --mode repair [options]

  ธง (ยาว) | ความหมาย
  ------------------------------|--------------------------------------------
  --execute | การเคลื่อนไหวจริง (ค่าเริ่มต้นคือการทดลองรันเท่านั้น)
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | ไฟล์ประวัติ UTF-8 ที่มี B64| เส้น
  --delete-duplicates | ลบผู้สมัครที่ซ้ำกัน (ต้องการ --confirm-delete พร้อมด้วย --execute)
  --delete-issues | ลบผู้สมัครกลุ่มปัญหา (ต้องการ --confirm-delete พร้อมด้วย --execute) ไม่อยู่ในเป้าหมายอัตโนมัติระยะไกล
  --archive-after-organize | หลังจากการจัดระเบียบ: ต่อไฟล์ ZIP พี่น้อง จากนั้นลบต้นฉบับ (ต้องการ --confirm-delete พร้อม --execute) ข้ามส่วนขยายที่เก็บถาวรแล้ว

  **หมายเหตุ:** CLI `--mode models` เลือก **โมเดล CAD / 3D** ไม่ใช่สิ่งประดิษฐ์ AI ใช้ `--mode ai` หรือ `--mode models-ai` สำหรับ AI / ML

  ตัวอย่าง (ทดลองรัน บัคเก็ตทั้งหมด): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  ตัวอย่าง (เฉพาะการเคลื่อนไหวที่ไม่ซ้ำเท่านั้น, ดำเนินการ): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  สร้าง: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  การทดลองรัน: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  สำหรับ --execute ให้ลบ :ro ออกจากซอร์สเมาท์ ดู containers/README.md สำหรับกฎของผู้ปฏิบัติงานหลายคน (หนึ่งเอาต์พุตรูทต่อผู้ปฏิบัติงาน)

Kubernetes (งานอ้างอิง)
  PVC แหล่งที่มาแบบอ่านอย่างเดียวใช้ได้กับงานทดลองรัน การเคลื่อนไหวจริงด้วย --execute จำเป็นต้องมี PVC ที่สามารถเขียนได้ ให้สิทธิ์ร้านค้าหรือผู้จัดพิมพ์ที่ถูกต้องสำหรับการจัดระเบียบ/ซ่อมแซมทั้งหมด (ทดลองเรียกใช้และดำเนินการ) หนึ่งฝักต่อต้นไม้ออก รูปแบบขั้นต่ำสุดได้รับการบันทึกไว้ใน containers/README.md ควบคู่ไปกับรายการตัวอย่าง

ความคืบหน้าของงาน
  หน้าต่างงานแสดงความคืบหน้าสำหรับการรัน App, CLI, Docker และ Kubernetes ขั้นตอนที่ทราบยอดรวมจะแสดงเปอร์เซ็นต์ การสแกนที่ไม่มียอดรวมจะยังไม่กำหนด
  ระบบอัตโนมัติเริ่มตัวทำงาน CLI ด้วย ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 และตัดบรรทัดเครื่องหมายเหล่านั้นออกจากบันทึกที่มองเห็น การรัน CLI ที่เริ่มด้วยมือจะไม่ส่งเครื่องหมายเว้นแต่จะตั้งค่าตัวแปรนั้น
  ตัวทำงาน Docker และ Kubernetes ได้รับตัวแปรเดียวกัน การรันเหล่านั้นจึงรายงานเปอร์เซ็นต์ด้วย ตัวเลขนี้อ่านจากบันทึกของตัวทำงาน จึงเริ่มแสดงเมื่อคอนเทนเนอร์หรือพอดเริ่มเขียน
  --list-running และ --show-run มีช่องความคืบหน้าสำหรับงานที่ทำงานอยู่ เมื่อการรันได้รายงานบางอย่างแล้ว

# ตัวอย่างการทำงาน

## UI แบบกราฟิก

เพิ่ม **แหล่งที่มา** และโฟลเดอร์เอาต์พุต เลือกโหมดการทำงาน เปิด **ทดลองรัน** เพื่อดูตัวอย่าง แล้วกด **เรียกใช้** ปล่อยให้ **ทดลองรัน** ปิดอยู่เพื่อย้ายไฟล์จริง ตัวเลือกการลบจะขอการยืนยันก่อนดำเนินการ

## ตัวอย่าง CLI

CLI การทดลองรัน: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
