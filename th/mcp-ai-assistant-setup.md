# ผู้ช่วย AI (MCP)

ทีมที่มีใบอนุญาตเชื่อมต่อ **OrganizeFiles.Cli** กับ Claude Desktop, **Cursor**, VS Code Copilot หรือไคลเอนต์ Model Context Protocol อื่น ซึ่งด้านล่างเรียกว่าไคลเอนต์ MCP ตัวเชื่อมต่อคือแพ็กเกจ Python ชื่อ **organize-files-mcp** ดาวน์โหลดได้ฟรีจาก github.com/GutRaz/organize-files-docs ในโฟลเดอร์ `mcp/`

**ในแอปเดสก์ท็อป:** เปิด **การตั้งค่า MCP...** ใต้ **แอปพลิเคชันและข้อมูล** ในคอลัมน์ตัวเลือก หรือจากเมนูเครื่องมือ เลือก **การเข้าถึง MCP** เป็น **ปิด**, **การเฝ้าติดตาม** หรือ **การควบคุม** จากนั้นคัดลอกส่วน JSON โหลด MCP ใหม่ในแอป AI ทุกครั้งที่เปลี่ยนระดับ เพราะ **การควบคุม** สร้างโทเค็นใหม่ทุกครั้ง

**ถามผู้ช่วยเอกสาร** “setup mcp” หรือ “cum setez mcp” เพื่อดูขั้นตอนบนระบบปัจจุบัน

## ระดับการเข้าถึง MCP ที่ตั้งค่าในแอป

ระดับต่าง ๆ ตรงกับงานสามแบบ: **อ่าน / ดูตัวอย่าง / ดำเนินการ**

| ระดับ | ประเภทงาน | สิ่งที่ AI ทำได้ |
|-------|--------|-------------------|
| **ปิด** | — | เฉพาะ `organize_mcp_status` ไม่มีการวินิจฉัยและไม่มีการเข้าถึงพื้นที่ทำงาน |
| **การเฝ้าติดตาม** | **อ่าน** | ทุกอย่างของระดับปิด รวมกับการวินิจฉัยแบบอ่านอย่างเดียว ประวัติการรันและงาน ล็อก การตรวจสอบบันทึก **`organize_capabilities`** และ **`organize_workspace_snapshot`** โดย `organize_capabilities` แสดงรายการโหมดการรัน ซึ่งมี **`ai`** อยู่ด้วย ขอบเขตการย้าย และเป้าหมาย ส่วน `organize_workspace_snapshot` แสดงพื้นที่ทำงานที่บันทึกไว้ในหน้าต่างหลัก ไม่มีการดูตัวอย่างและไม่มีการดำเนินการ |
| **การควบคุม** | **ดูตัวอย่าง** / **ดำเนินการ** | ทุกอย่างของระดับการเฝ้าติดตาม รวมกับ **`organize_create_job`**, **`organize_run_workspace`** และ **`organize_remove_empty_organize_layout`** ต้องมี **โทเค็นควบคุม** ในการตั้งค่า MCP คือ `ORGANIZE_FILES_MCP_CONTROL_TOKEN` **ดูตัวอย่าง** คือ `organize_run_workspace` เมื่อพื้นที่ทำงานที่บันทึกไว้เปิด **การทดลองรัน** อยู่ จึงไม่มีการเขียนสิ่งใด **ดำเนินการ** คือเครื่องมือเดียวกันเมื่อปิดการทดลองรัน จึงมีการย้ายไฟล์ ตัวเชื่อมต่อจะไม่ใส่ `--confirm-destructive` เว้นแต่การเรียกจะตั้ง `confirm_destructive=true` และถ้าไม่มีแฟล็กนี้ บรรทัดคำสั่งจะปฏิเสธด้วย `confirm_destructive_required` |

ไฟล์ควบคุมคือ **`mcp-control.json`** อยู่ข้าง `automation-jobs.json` ในโฟลเดอร์โปรไฟล์ของแอป ส่วนที่คัดลอกไม่ได้ระบุชื่อไฟล์นี้ เพราะตัวเชื่อมต่อหาไฟล์นี้เองในโฟลเดอร์โปรไฟล์เริ่มต้น ให้ตั้ง **`ORGANIZE_FILES_MCP_CONTROL_FILE`** เฉพาะเมื่อไฟล์อยู่ที่อื่น ที่ระดับ **การควบคุม** ส่วนที่คัดลอกจะตั้ง **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`** ด้วย

**การย้ายและการลบต้องมีขั้นตอนที่สองซึ่งทำโดยคน** ผู้ช่วยตั้งการยืนยันเอง ข้อความที่ผู้ช่วยอ่านจึงอาจชักจูงให้ผู้ช่วยยืนยันได้ ดังนั้นการรันที่ไม่ใช่การทดลองรันจึงต้องมีช่วงเวลาที่เปิดไว้ใน **การตั้งค่า MCP** ด้วย และช่วงเวลานั้นจะปิดเองหลังผ่านไป 15 นาที นอกช่วงเวลาดังกล่าว ผู้ช่วยยังเตรียมและดูตัวอย่างการรันได้ แต่ตัวการรันจะถูกปฏิเสธ ทั้งไฟล์ควบคุมและช่วงเวลานี้ลงลายเซ็นด้วยกุญแจที่การติดตั้งนี้เก็บไว้ ไฟล์ควบคุมที่ถูกแก้ด้วยมือหรือคัดลอกมาจากคอมพิวเตอร์เครื่องอื่นจะนับเป็นระดับปิด

## เครื่องมือ MCP ตามระดับ

**เสมอ รวมถึงที่ระดับปิด:** `organize_mcp_status`

**การเฝ้าติดตามและการควบคุม:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` และ `organize_run_raw_cli` ซึ่งรับเฉพาะคำสั่งแบบอ่าน

**ในระดับการเฝ้าติดตามและการควบคุมยังมี:** `organize_capabilities` ซึ่งแสดงโหมดการรัน **`ai`** สำหรับไฟล์ AI และ ML และ `organize_workspace_snapshot`

**เฉพาะการควบคุม:** `organize_create_job` จากพื้นที่ทำงานหรือจาก JSON ของงาน, `organize_run_workspace` สำหรับการดูตัวอย่างหรือการรันจริงตามการตั้งค่าการทดลองรันของพื้นที่ทำงาน และ `organize_remove_empty_organize_layout` ซึ่งลบโฟลเดอร์เลย์เอาต์ที่ว่างภายในเอาต์พุตที่มีอยู่ และไม่สร้างโฟลเดอร์เอาต์พุตเองเลย

คำสั่งที่ย้ายหรือลบไฟล์จะถูกบล็อกผ่าน MCP เสมอเมื่ออยู่นอกระดับ **การควบคุม** ไม่มีการตั้งค่าอื่นใดที่อนุญาตคำสั่งเหล่านี้

## แฟล็กบรรทัดคำสั่งที่ตัวเชื่อมต่อใช้

| แฟล็ก | ระดับ | จุดประสงค์ |
|------|-------|---------|
| `--mcp-control-status` | ทุกระดับ | JSON ที่มีระดับ เส้นทางไฟล์ควบคุม และแฟล็กของการเฝ้าติดตามและการควบคุม |
| `--mcp-capabilities` | การเฝ้าติดตามขึ้นไป | รายการ JSON ของโหมดการรัน ซึ่งมี **`ai`** อยู่ด้วย ขอบเขตการย้าย และเป้าหมาย |
| `--mcp-workspace-snapshot` | การเฝ้าติดตามขึ้นไป | พื้นที่ทำงานที่บันทึกไว้ และวิธีที่พื้นที่ทำงานนั้นกลายเป็นงาน |
| `--mcp-create-job` | การควบคุม | สร้างงานด้วย `--from-workspace` หรือ `--mcp-job-json` |
| `--mcp-run-workspace` | การควบคุม | รันพื้นที่ทำงานที่บันทึกไว้ด้วย `--allow-app-target` และ `--mcp-control-token` |
| `--remove-empty-organize-layout` | การควบคุม | ลบโฟลเดอร์เลย์เอาต์ที่ว่างภายใน `--output` ที่มีอยู่ |
| `--confirm-destructive` | การควบคุม | จำเป็นร่วมกับ `--mcp-run-workspace` สำหรับการรันที่ย้ายหรือลบ ตัวเชื่อมต่อส่งแฟล็กนี้เฉพาะเมื่อ `confirm_destructive=true` |

## การตั้งค่าใน JSON ของไคลเอนต์ MCP

| การตั้งค่า | เมื่อใด |
|----------|------|
| `ORGANIZE_FILES_CLI` | เส้นทางไปยัง OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | เส้นทางไปยัง `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | เส้นทางไปยัง `mcp-control.json` เฉพาะเมื่อไฟล์ไม่ได้อยู่ในโฟลเดอร์โปรไฟล์เริ่มต้น |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | เฉพาะระดับ **การควบคุม** จากส่วนที่แอปให้คัดลอก |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | ระดับ **การควบคุม** สำหรับการรันพื้นที่ทำงานที่บันทึกไว้ |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | ไม่บังคับ โทเค็นเดียวกับที่โฮสต์ใช้สำหรับการอ่าน |

## การตั้งค่าบน Windows

1. **Python 3.10 หรือใหม่กว่า** — รัน `python -V` ใน PowerShell ถ้าไม่มี Python หรือเป็นรุ่นเก่ากว่า ให้ติดตั้งจาก [python.org](https://www.python.org/downloads/) และเลือก **Add python.exe to PATH**
2. **ดาวน์โหลดและติดตั้งตัวเชื่อมต่อ** — ดาวน์โหลด github.com/GutRaz/organize-files-docs เป็น ZIP แตกไฟล์ แล้วรัน `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1` สคริปต์จะสร้างสภาพแวดล้อม Python เฉพาะสำหรับตัวเชื่อมต่อ และแสดงคำสั่งสำหรับแอป AI
3. **ในแอป:** **การตั้งค่า MCP...** เลือก **การเฝ้าติดตาม** หรือ **การควบคุม** แล้วคัดลอก JSON
4. **เส้นทาง:** `%LocalAppData%\OrganizeFilesCrossPlatform\` เก็บงานและ `mcp-control.json` Cursor: `%USERPROFILE%\.cursor\mcp.json` Claude: `%APPDATA%\Claude\claude_desktop_config.json` VS Code: `%USERPROFILE%\.vscode\mcp.json`
5. **ทดสอบ** — รัน `organize_mcp_status` แล้วรัน `organize_server_info` ค่า `cliResolved` ต้องเป็น true และ `mcpLevel` ต้องตรงกับแอป

## การตั้งค่าบน macOS

ขั้นตอนเดียวกันกับ **python3** และ `bash mcp/install-organize-files-mcp.sh` ถ้า `python3 -V` แสดง 3.9 หรือไม่มี Python เลย ให้ติดตั้ง Python จาก [python.org](https://www.python.org/downloads/macos/) ก่อน เส้นทาง: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`

## การตั้งค่าบน Linux

ขั้นตอนเดียวกันกับ **python3** และ `bash mcp/install-organize-files-mcp.sh` บน Debian และ Ubuntu ให้รัน `sudo apt install python3-venv` ก่อน เส้นทาง: `~/.local/share/OrganizeFilesCrossPlatform/` หรือ `$XDG_DATA_HOME` เมื่อมีการตั้งค่าไว้, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`

## ความปลอดภัย

- MCP ทำงานในฐานะ **ผู้ใช้ภายในเครื่อง** ของระบบปฏิบัติการ ด้วยสิทธิ์เดียวกับบรรทัดคำสั่งที่รันด้วยมือ
- เก็บ **โทเค็นควบคุม** และ **โทเค็นอ่าน** เป็นความลับเหมือนรหัสผ่าน คัดลอก JSON อีกครั้งหลังเปิดการควบคุม
- **`organize_run_workspace`** ทำงานในบรรทัดคำสั่ง ไม่ได้ผ่านปุ่มเรียกใช้ของแอป อย่ารันงานสองงานบนโฟลเดอร์เอาต์พุตเดียวกันพร้อมกัน
- ตัวอย่าง: `mcp/examples/`

## การรันที่ย้ายหรือลบ

`--mcp-run-workspace` ต้องใช้ `--confirm-destructive` สำหรับทุกการรันที่ไม่ใช่การทดลองรัน ไม่ว่าจะย้าย ลบ หรือเก็บถาวร ถ้าไม่มีแฟล็กนี้ บรรทัดคำสั่งจะตอบ `confirm_destructive_required` ตัวเชื่อมต่อจะไม่ใส่แฟล็กนี้เว้นแต่การเรียกจะตั้ง `confirm_destructive=true` ซึ่งทำได้เฉพาะระดับการควบคุม ดังนั้นโดยค่าเริ่มต้น ตัวเชื่อมต่อจะปฏิเสธ

## ภาษา

คำตอบเรื่องการตั้งค่ามาจากคู่มือที่แปลแล้วชุดเดียวกับหน้าต่างเอกสารประกอบและผู้ช่วยคู่มือ `organize_capabilities` รายงานโหมดการรันและเป้าหมาย ไม่ใช่ชื่อธีมของแอป
