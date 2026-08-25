# ENV.md —— 逐機器環境紀錄

> **為什麼要逐機器分開**:2026-08-09 踩過一次 ——
> TODO.md 有一張「本機環境」表(2026-08-02 建置),但那張表**沒有標是哪一台**。
> 後來在 MSI 上發現 `gh` / `ffmpeg` / `yt-dlp` 都叫不到,我就下結論「那張表是另一台的」。
> **結果只對三分之一**:`ffmpeg` 本來就裝在 MSI(winget 有記錄,只是不在 PATH),
> `gh` 與 `yt-dlp` 才是真的沒裝。
>
> 🔑 **教訓:「叫不到」有兩種原因 —— 沒裝、或裝了但不在 PATH。**
> 兩者的處置完全不同,而且不能靠 `Get-Command` 一個指令分辨。
> **正確診斷順序**:①`winget list --id <id>` 或 `pip show <pkg>` 查有沒有裝
> ②有裝就去 `%LOCALAPPDATA%\Microsoft\WinGet\Packages\` 底下找 exe ③再決定是補 PATH 還是安裝。

---

## 🖥️ MSI(`$env:COMPUTERNAME` = **MSI**,Micro-Star Raider 18 HX AI A2XWIG)

**最後實查:2026-08-09**(jupyter / ML 套件 / yt-dlp 三列 2026-08-25 複查)

| 工具 | 狀態 | 路徑 / 版本 |
|---|---|---|
| git | ✅ PATH OK | 2.55.0.3 |
| python | ✅ PATH OK | 3.11.9 |
| node / npm | ✅ PATH OK | v24.18.1 / 12.x |
| **codex** | ✅ PATH OK | **0.147.0**(2026-08-09 由 0.144.5 升級)<br>`%APPDATA%\npm\codex.cmd` |
| code(VS Code) | ✅ PATH OK | |
| **ffmpeg / ffprobe** | ⚠️ **裝了但預設不在 PATH**<br>2026-08-09 已加進 User PATH | **9.0-full_build**<br>`C:\Users\kenny\AppData\Local\Microsoft\WinGet\Packages\`<br>`Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\`<br>`ffmpeg-9.0-full_build\bin` |
| **gh** | 🔴 **沒裝**(winget 查無) | 要用:`winget install --id GitHub.cli -e` |
| **yt-dlp** | ✅ **2026-08-25 已裝** | **2026.08.19**,`C:\Users\kenny\AppData\Local\Programs\Python\Python311\Scripts\yt-dlp.exe`<br>零相依安裝(乾跑顯示僅 `Would install yt-dlp-2026.8.19` 一項),**不影響 pycaret 鎖住的 pandas/numpy/scipy**<br>⚠️ **YouTube 一定要加 `--js-runtimes node`**,否則警告 "No supported JavaScript runtime" 且部分格式抓不到(預設只認 deno;本機有 node v24.18.1) |
| **影片來源實測**(2026-08-25) | 見右 | **YouTube** ✅ 標題/時長/自動字幕全可(含 zh-TW);實測 `OhCzX0iLnOc` 抽出 1,659 字逐字稿<br>**bilibili** ⚠️ 影片可下載,但**只有 danmaku 彈幕,沒有字幕軌** → 要逐字稿得下載影片再跑 Whisper<br>**ted.com / embed.ted.com** 🔴 抽取失敗(`JSON object must be str...`)→ 改用 `ytsearch1:` 找 YouTube 版本(TED-Ed 那支 = `RzkD_rTEBYs`) |
| jupyter(CLI) | 🔴 CLI 沒裝 —— **但不影響跑 .ipynb** | 2026-08-25 複查:VS Code 擴充 `ms-toolsai.jupyter` + `ipykernel 7.1.0` 已裝,**在 VS Code 直接開 .ipynb 選 Python 3.11.9 kernel 即可**,不需要 `jupyter notebook` 伺服器,也不需要 Anaconda(conda 未裝且不需裝) |
| **ML 課套件**(2026-08-25 實查) | ✅ 兩情境全齊 | sklearn 1.4.2 · xgboost 3.2.0 · lightgbm 4.6.0 · pandas 2.1.4 · numpy 1.26.4 · scipy 1.11.4 · matplotlib 3.7.5 · seaborn 0.13.2 · openpyxl 3.1.5<br>tensorflow 2.20.0 · keras 3.13.2 · torch 2.10.0 · torchvision 0.25.0 · pillow 12.0.0 |
| Word / PowerPoint COM | ✅ 可用 | 組版的逐頁 PNG 導出靠它 |
| **Google Workspace MCP** | 🔴 **不能用** | `~/.workspace-mcp/client_secret.json` 不存在,`GOOGLE_OAUTH_CLIENT_ID` / `_SECRET` 也沒設。<br>→ 要寫 Google Sheet 只能走 **Chrome 擴充功能**(內建瀏覽器沒登入 Google,而我不能代輸入密碼) |

### MSI 專屬注意

- **ffmpeg 的路徑很長且帶 winget 的雜湊目錄名**,升版之後路徑會變
  (`ffmpeg-9.0-full_build` → `ffmpeg-X.Y-full_build`)。
  升版後 User PATH 那筆會失效,要重新指。
  → **穩健的做法**:腳本裡不要寫死路徑,用
  `Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Filter ffmpeg.exe -Recurse -Depth 6`
  動態找,或每次在 session 裡把 bin 前置到 `$env:Path`。
- ⚠️ **另有一支 SteelSeries 附帶的 ffmpeg**
  (`C:\Program Files\SteelSeries\GG\apps\moments\ffmpeg.exe`)——
  版本不明、功能可能被裁,**不要用它**。

---

## 🖥️ 另一台(2026-08-02「新機建置」那台,主機名未記錄)

⚠️ **這一段的可信度低** —— 來源是 TODO.md 的舊表,而那張表沒標機器,
且其中至少兩項(gh / yt-dlp)在 MSI 上不成立。**接手時一律重新實查,不要照抄。**

TODO 舊表聲稱:git 2.55.0.3 · gh 2.97.0 · pip 26.2 · npm 12.0.2 ·
Python 3.11.9 + A2b 全部相依 · JupyterLab 4.6.2 / notebook 7.6.1 / nbconvert 7.17.1 ·
Node v24.18.1 · Codex 0.146.0 · ffmpeg 8.1.2-full · yt-dlp 2026.07.04

→ 其中 **Codex 實際是 0.144.5 不是 0.146.0**(2026-08-08 handoff 已記),
**ffmpeg 在 MSI 上是 9.0 不是 8.1.2**。這張表整體需要重新驗。

---

## 跨機器都成立的坑

- **持久化 PATH 是對的,但「行程過期」不是 PATH 沒設** ——
  安裝**之前**就已啟動的行程(Claude Code session 本身、已開的終端機 / VS Code)
  拿的是舊環境區塊。解法是**重開那些視窗**,或在該 session 內重讀 registry:
  ```
  $env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' +
              [Environment]::GetEnvironmentVariable('Path','User')
  ```
  🚫 **不要再 append 一次** —— 那只會疊出重複路徑。
- **Codex 預設 `reasoning effort: none`**,每趟都要加 `-c model_reasoning_effort="xhigh"`。
- **PowerShell 會把多行 prompt 拆成多個引數** → 餵 Codex 一律用 `Get-Content x.txt -Raw |` 管道。
- **不要對原生 exe 用 `2>&1`** —— PowerShell 5.1 會把 stderr 包成 ErrorRecord 並讓 `$?` 變 false。
- **Python 套件被 `pycaret 3.3.2` 鎖在 2024 年**(scipy/numpy/matplotlib/pandas/sklearn 五個上限貼死)。
  `pip install --upgrade` 不會警告,照跑會讓 Business Analytics 靜默壞掉。
  正解是**隔離不是升級**:AI for Enterprises 另開 venv。
