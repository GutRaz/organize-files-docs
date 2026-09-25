# Advanced / Diagnostics

## Organize tuning

Advanced / Diagnostics exposes **OrganizeFilesEngine** options without cluttering the main panel.

Organize modes can tune dedupe, destination index, Unique date rules, move and enumeration threading, BFS supplement, resume file, and extra Unique roots.

Repair keeps only network and disk-full retry timing, detected graphics hardware lanes for optional full video check, hash read buffer, and JSON heartbeat. Other fields are visible for context but disabled.

When sources or output live on NAS or UNC paths, lower parallelism, keep network retry enabled, leave supplement BFS on for odd SMB trees, and try the 8 MiB hash buffer if hashing is slow.

# Advanced / Diagnostics — each option

## About this chapter

These controls are engine options. Desktop (Windows, macOS, Linux), Android, iOS and the command-line tool read the same values.

**Organize** modes use every control below unless the UI grays it out. **Repair** uses only network retry, disk-full retry, detected graphics hardware lanes (with full video check), hash read buffer, heartbeat JSON, **Resume state file** and **Start fresh (truncate resume file)**. Other fields stay visible but are ignored during repair.

## Network sources (NAS / UNC)

When **Sources** or **Output** are on SMB/CIFS shares, NAS volumes, or mapped drives, review this section carefully.

- **Why tune** — Thread counts that work on a local SSD can stall or overload a filer.
- **What to try** — Keep network retry on. Lower move threads and enum parallel max on timeouts. Leave supplement BFS on unless a full count was verified without it. Try the 8 MiB hash buffer when hashing is slow over the network.
- **Disable network wait** — Fails fast on transient network errors. Risky on Wi-Fi or busy shares.

## Dedupe mode

How the engine decides two files are duplicates.

| Mode | What it does | When to use | Trade-off |
| ---- | ------------ | ----------- | --------- |
| **Hash (SHA-256)** | Reads and hashes the full content of every included source file, then groups identical bytes. | Strongest practical mode. Required for in-place deletion (duplicates and problematic files). | Slowest on large trees or NAS. No algorithm should be presented as an absolute guarantee. |
| **Size + time + name** | Key = size, UTC last-write ticks, lowercased name, then full SHA-256 verification. | Conservative compatibility mode for older media folder layouts. | Can miss renamed duplicates. Never use with Delete duplicates or Delete problematic files. |
| **None** | No cross-file dedupe. | Sorting only, not duplicate cleanup. | Duplicates stay in sources. |

## Skip destination index

- **Off (default)** — Scans existing **Unique** output and indexes it before hashing. Safer when reusing the same output folder.
- **On** — Skips that scan.
- **Benefit** — Faster on huge output trees.
- **Risk** — More duplicate content can land inside **Unique**.

## Unique min year

Minimum calendar year for date folders under **Unique** in media layouts.

**Why** — Avoids scattering very old files into odd year folders when metadata is wrong.

## Move threads

Parallel file moves after destinations are reserved.

- **Higher** — Faster on local SSD.
- **Lower** — Safer on NAS, USB, or Wi-Fi mapped drives.

## Classify and hash threads

Parallel workers during source scan and SHA-256 dedupe.

- **Classify threads** — File discovery and classification. CLI: `--classify-threads <n>`.
- **Hash threads** — Content hashing workers. CLI: `--hash-threads <n>`.
- **Overrides** — Manual counts override organize profile defaults (`--profile`).

## Enum parallel max

Limit for parallel directory listing during scan.

- **0** = engine auto.
- **Lower** — Less pressure on SMB when many folders list at once.

## Supplement BFS directory pass

- **On (default)** — Extra shallow breadth-first listing pass.
- **Why** — Some NAS paths or deep trees look incomplete on the first pass.
- **Off** — Only after verifying a complete file count without it.
- **CLI** — `--no-bfs` turns off this pass.

## Resume state file

Optional UTF-8 path. Successful moves append `B64|` lines so the next organize run can skip finished sources.

- **Why** — Continue long jobs after stop or crash.
- **Default path** — When the field is empty at run time, the engine uses `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt`. Without **Output**, it uses `sessions\<id>\resume\OrganizeFiles.resume.txt` under the app profile.
- **Desktop UI** — Read-only path list for mouse selection and copy. When a resume file already exists at the default location, the path appears automatically. **Browse** picks a log folder and appends `OrganizeFiles.resume.txt`. **Remove** clears the path. When empty, the hint shows the path used at run time.

## Start fresh

Truncates the resume file when a **real** organize run starts (dry run does not truncate). With **Save progress & workspace**, also clears the saved UI snapshot at run start.

**Why** — Force a full recount instead of continuing an old resume log.

## Extra Unique scan roots

One folder per line: extra **Unique** trees to index (legacy layout, other volume).

- **Why** — Dedupe can see files already organized elsewhere without moving them again.
- **Desktop UI** — Read-only list for per-line copy. **Add** appends a picked folder. **Remove** deletes the selected line (for example an old `Uniques` tree on NAS).

## Network retry (seconds) / Disable network wait

Seconds to retry transient network I/O.

- **Why** — SMB filers drop idle sessions. Used by organize and repair.
- **Disable network wait** — Stop waiting and fail instead.

## Disk full retry (seconds) / Disable disk-full wait

Same pattern when the output volume runs out of space.

**Why** — Time to free disk during long runs.

## Graphics hardware lanes

Only when integrated **full video check** is enabled and **Use detected graphics hardware** is on. A value above **0** sets an explicit lane count for validation parallelism across detected vendors (NVIDIA, AMD, Intel, Apple, mobile). **0** means auto-detect hybrid lane count. It does not mean CPU-only. Select **CPU only** in the graphics-card list for CPU-only sampling. Lane tags plan CPU bitstream validation. They do not invoke OS hardware video decode.

- **CLI preset** — `--hwaccel <value>` selects a validation lane preset (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`) when full video check runs.

## Hash read buffer

Per-worker read buffer while hashing (512 KiB, 1 MiB, 8 MiB).

**Why** — Larger buffers help when a NAS or a high-latency share is slow to answer.

## Record undo journal

Opt-in JSONL journal of moves under the output root for the run.

- **Why** — Supports CLI undo replay after a real organize run.
- **Archive** — Post-organize archive stays off while undo journal is active.
- **CLI** — `--record-undo-journal` (same as the Main checkbox).

## Write run heartbeat JSON

Writes optional `Organize.Files.run.json` under `Output\_OrganizeMediaLogs`.

- **Why** — External tools can read live counters (scanned, planned, completed) during organize or repair.
- **Timing** — Every 10,000 files seen, every 5,000 matches and about every 15 seconds during source scans, after every 1,000 files and at most every 5 seconds during validation, hashing and moves, and at each major phase.
