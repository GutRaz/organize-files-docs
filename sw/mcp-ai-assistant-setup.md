# Msaidizi wa AI (MCP)

Timu zenye leseni huunganisha **OrganizeFiles.Cli** na Claude Desktop, **Cursor**, VS Code Copilot au mteja mwingine wa Model Context Protocol, unaoitwa mteja wa MCP hapa chini. Kiunganishi ni kifurushi cha Python **organize-files-mcp**. Kinapakuliwa bure kutoka github.com/GutRaz/organize-files-docs, kwenye folda yake ya `mcp/`.

**Katika programu ya kompyuta:** fungua **Mpangilio wa MCP...** chini ya **Programu na data** kwenye safu ya chaguo, au kutoka kwenye menyu ya zana. Chagua **ufikiaji wa MCP**: **Imezimwa**, **Ufuatiliaji** au **Udhibiti**. Kisha nakili kijisehemu cha JSON. Pakia upya MCP katika programu ya AI baada ya kila badiliko la kiwango, kwa sababu **Udhibiti** hutengeneza tokeni mpya kila mara.

**Uliza msaidizi wa nyaraka** “setup mcp” au “cum setez mcp” ili kupata hatua za mfumo wa sasa.

## Viwango vya ufikiaji wa MCP, vinavyowekwa katika programu

Viwango vinalingana na aina tatu za kazi: **kusoma / onyesho la awali / utekelezaji**.

| Kiwango | Aina ya kazi | Kile AI inaweza kufanya |
|-------|--------|-------------------|
| **Imezimwa** | — | `organize_mcp_status` pekee. Hakuna uchunguzi na hakuna ufikiaji wa nafasi ya kazi. |
| **Ufuatiliaji** | **Kusoma** | Kila kitu cha Imezimwa, pamoja na uchunguzi wa kusoma pekee, historia ya uendeshaji na ya kazi, kufuli, ukaguzi wa rekodi, **`organize_capabilities`** na **`organize_workspace_snapshot`**. `organize_capabilities` huorodhesha njia za uendeshaji, ikiwemo **`ai`**, maeneo ya kuhamisha na malengo. `organize_workspace_snapshot` huonyesha nafasi ya kazi iliyohifadhiwa katika dirisha kuu. Hakuna onyesho la awali na hakuna utekelezaji. |
| **Udhibiti** | **Onyesho la awali** / **Utekelezaji** | Kila kitu cha Ufuatiliaji, pamoja na **`organize_create_job`**, **`organize_run_workspace`** na **`organize_remove_empty_organize_layout`**. Kiwango hiki kinahitaji **tokeni ya udhibiti** katika mipangilio ya MCP, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **Onyesho la awali** ni `organize_run_workspace` wakati nafasi ya kazi iliyohifadhiwa ina **Uendeshaji wa majaribio** umewashwa, kwa hiyo hakuna kinachoandikwa. **Utekelezaji** ni zana hiyo hiyo wakati Uendeshaji wa majaribio umezimwa, kwa hiyo faili huhamishwa. Kiunganishi huacha `--confirm-destructive` isipokuwa mwito uweke `confirm_destructive=true`, na bila bendera hiyo mstari wa amri hukataa kwa `confirm_destructive_required`. |

Faili ya udhibiti ni **`mcp-control.json`**, kando ya `automation-jobs.json` katika folda ya wasifu wa programu. Kijisehemu kilichonakiliwa hakitaji faili hiyo, kwa sababu kiunganishi huipata katika folda ya wasifu ya chaguo-msingi. Weka **`ORGANIZE_FILES_MCP_CONTROL_FILE`** tu wakati faili iko mahali pengine. Katika **Udhibiti**, kijisehemu pia huweka **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`**.

**Kuhamisha na kufuta kunahitaji hatua ya pili, inayofanywa na binadamu.** Msaidizi huweka uthibitisho wake mwenyewe, kwa hiyo maandishi ambayo msaidizi anasoma yanaweza kumshawishi kuthibitisha. Kwa hiyo uendeshaji ambao si wa majaribio unahitaji pia dirisha la muda linalofunguliwa katika **Mpangilio wa MCP**, na dirisha hilo hujifunga lenyewe baada ya dakika 15. Nje ya dirisha hilo msaidizi bado anaweza kuandaa na kuonyesha uendeshaji, lakini uendeshaji wenyewe hukataliwa. Faili ya udhibiti na dirisha vyote vimetiwa saini kwa ufunguo unaohifadhiwa na usakinishaji huu. Faili ya udhibiti iliyobadilishwa kwa mkono au kunakiliwa kutoka kompyuta nyingine huhesabiwa kama Imezimwa.

## Zana za MCP kwa kiwango

**Daima, pia katika Imezimwa:** `organize_mcp_status`

**Ufuatiliaji na Udhibiti:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` na `organize_run_raw_cli`, inayokubali amri za kusoma pekee.

**Pia katika Ufuatiliaji na Udhibiti:** `organize_capabilities`, inayoorodhesha njia ya uendeshaji **`ai`** kwa faili za AI na ML, na `organize_workspace_snapshot`.

**Udhibiti pekee:** `organize_create_job` kutoka kwenye nafasi ya kazi au kutoka JSON ya kazi, `organize_run_workspace` kwa onyesho la awali au uendeshaji halisi kulingana na Uendeshaji wa majaribio wa nafasi ya kazi, na `organize_remove_empty_organize_layout`, inayoondoa folda tupu za mpangilio ndani ya pato lililopo na haiundi kamwe folda ya pato yenyewe.

Amri zinazohamisha au kufuta faili huzuiwa daima kupitia MCP nje ya kiwango cha **Udhibiti**. Hakuna mpangilio mwingine unaoziruhusu.

## Bendera za mstari wa amri ambazo kiunganishi hutumia

| Bendera | Kiwango | Kusudi |
|------|-------|---------|
| `--mcp-control-status` | chochote | JSON yenye kiwango, njia ya faili ya udhibiti na alama za Ufuatiliaji na Udhibiti |
| `--mcp-capabilities` | Ufuatiliaji na juu | Orodha ya JSON ya njia za uendeshaji, ikiwemo **`ai`**, maeneo ya kuhamisha na malengo |
| `--mcp-workspace-snapshot` | Ufuatiliaji na juu | Nafasi ya kazi iliyohifadhiwa na jinsi inavyokuwa kazi |
| `--mcp-create-job` | Udhibiti | Kuunda kazi kwa `--from-workspace` au `--mcp-job-json` |
| `--mcp-run-workspace` | Udhibiti | Kuendesha nafasi ya kazi iliyohifadhiwa, kwa `--allow-app-target` na `--mcp-control-token` |
| `--remove-empty-organize-layout` | Udhibiti | Kuondoa folda tupu za mpangilio ndani ya `--output` iliyopo |
| `--confirm-destructive` | Udhibiti | Inahitajika pamoja na `--mcp-run-workspace` kwa uendeshaji unaohamisha au kufuta. Kiunganishi huipitisha tu wakati `confirm_destructive=true` |

## Mipangilio katika JSON ya mteja wa MCP

| Mpangilio | Lini |
|----------|------|
| `ORGANIZE_FILES_CLI` | Njia ya OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | Njia ya `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | Njia ya `mcp-control.json`, tu wakati faili haipo katika folda ya wasifu ya chaguo-msingi |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | Kiwango cha **Udhibiti** pekee, kutoka kwenye kijisehemu cha programu |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | Kiwango cha **Udhibiti**, kwa uendeshaji wa nafasi ya kazi iliyohifadhiwa |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | Hiari. Tokeni ile ile ambayo seva hutumia kwa shughuli za kusoma |

## Mpangilio wa Windows

1. **Python 3.10 au mpya zaidi** — endesha `python -V` katika PowerShell. Ikiwa Python haipo au ni ya zamani zaidi, isakinishe kutoka [python.org](https://www.python.org/downloads/) na uweke alama kwenye **Add python.exe to PATH**.
2. **Pakua na usakinishe kiunganishi** — pakua github.com/GutRaz/organize-files-docs kama ZIP, ifungue na uendeshe `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1`. Hati hiyo huunda mazingira ya Python ya kiunganishi pekee na huchapisha amri ya programu ya AI.
3. **Katika programu:** **Mpangilio wa MCP...**, chagua **Ufuatiliaji** au **Udhibiti**, kisha nakili JSON.
4. **Njia:** `%LocalAppData%\OrganizeFilesCrossPlatform\` huhifadhi kazi na `mcp-control.json`. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **Jaribio** — endesha `organize_mcp_status`, kisha `organize_server_info`. `cliResolved` lazima iwe true na `mcpLevel` lazima ilingane na programu.

## Mpangilio wa macOS

Hatua zile zile kwa **python3** na `bash mcp/install-organize-files-mcp.sh`. Ikiwa `python3 -V` inaonyesha 3.9 au hakuna Python kabisa, kwanza sakinisha Python kutoka [python.org](https://www.python.org/downloads/macos/). Njia: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Mpangilio wa Linux

Hatua zile zile kwa **python3** na `bash mcp/install-organize-files-mcp.sh`. Kwenye Debian na Ubuntu, kwanza endesha `sudo apt install python3-venv`. Njia: `~/.local/share/OrganizeFilesCrossPlatform/`, au `$XDG_DATA_HOME` ikiwa imewekwa, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Usalama

- MCP huendeshwa kama **mtumiaji wa ndani** wa mfumo wa uendeshaji, kwa haki zile zile kama mstari wa amri unaoendeshwa kwa mkono.
- Weka siri **tokeni ya udhibiti** na **tokeni ya kusoma**, kama nywila. Nakili JSON tena baada ya kuwasha Udhibiti.
- **`organize_run_workspace`** huendeshwa katika mstari wa amri, si kupitia kitufe cha Endesha cha programu. Usiendeshe kazi mbili kwenye folda ile ile ya pato kwa wakati mmoja.
- Mifano: `mcp/examples/`.

## Uendeshaji unaohamisha au kufuta

`--mcp-run-workspace` inahitaji `--confirm-destructive` kwa kila uendeshaji ambao si wa majaribio, uwe unahamisha, unafuta au unahifadhi kwenye kumbukumbu. Bila bendera hiyo, mstari wa amri hujibu `confirm_destructive_required`. Kiunganishi huacha bendera hiyo isipokuwa mwito uweke `confirm_destructive=true`, na hilo linawezekana tu katika kiwango cha Udhibiti. Kwa hiyo, kwa chaguo-msingi, kiunganishi hukataa.

## Lugha

Majibu ya mpangilio yanatoka kwenye mwongozo ule ule uliotafsiriwa kama dirisha la Nyaraka na Msaidizi wa mwongozo. `organize_capabilities` huripoti njia za uendeshaji na malengo, si majina ya mandhari ya programu.
