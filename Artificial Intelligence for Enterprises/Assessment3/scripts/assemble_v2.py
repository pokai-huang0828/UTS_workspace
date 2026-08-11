# -*- coding: utf-8 -*-
"""由 notes/_v2_parts/ 三份分段檔機械重組 notes/04_十頁內容_v2.md,並用 Python 實算配時。

🔴 為什麼要有這支腳本(而不是每次臨時 inline 做):
   上一輪臨時寫的切法是 `re.sub(r"\\A.*?(?=\\n#\\s)", "", t)` —— 它刪掉「第一個 H1 之前的全部」,
   但 P08-11.md 的第一個 H1 之後緊接著就是 P8 的 H1(相距 7 行),
   非貪婪 `.*?` 會停在**第一個** `\\n#`,結果把分段標題連同 P8 整段一起吃掉。
   正解:找出所有 H1,從 **第 2 個**(第一個「單元」標題)切到檔尾 —— 分段標題(甲/乙/丙段)本身丟掉。

配時口徑(與 v2.2 起一致):
   口白字數 = 「## 口白逐字」區塊內的 **CJK + 英數字元**,不計標點與 markdown 記號。
   語速 4.4 字/秒。硬上限 600 秒。
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.normpath(os.path.join(HERE, "..", "notes"))
PARTS = [os.path.join(NOTES, "_v2_parts", n) for n in ("P01-04.md", "P05-07.md", "P08-11.md")]
OUT = os.path.join(NOTES, "04_十頁內容_v2.md")
VER = "v2.4"
RATE = 4.4
HARD_LIMIT = 600.0

H1 = re.compile(r"(?m)^#\s+(.+)$")
NARR = re.compile(r"(?m)^##\s*口白逐字\s*$")
NEXT_H = re.compile(r"(?m)^#{1,2}\s+")
COUNTABLE = re.compile(r"[一-鿿㐀-䶿 A-Za-z0-9]".replace(" ", ""))

# 🔴 舞台指示不是口白:整段被括號包住的錄影標記 / 交界移交註記,不唸出聲,不計配時。
#    這是本腳本第一版的實測瑕疵 —— 它把 P6/P7 三段括號註記算成口白,
#    憑空多出 210 字(+47.7 秒),讓 567.5 秒的片子看起來像 615.2 秒、假超時。
#    其中一段自己就寫著「口白不出聲」,另一段自己就寫著「不列入本頁 224 字」。
#    (?ms):^ $ 錨在行邊界而 . 可跨行,故多行括號註記能整段剝掉;.*? 非貪婪,連續兩段不會被併吃。
STAGE = re.compile(r"(?ms)^[ 	]*[*_]{0,2}[((].*?[))][*_]{0,2}[ 	]*$")

# 各單元「> 配時 … 口白 NNN 字」的自帶宣告值 —— 當回歸護欄用,避免同類瑕疵再無聲復發。
DECL = re.compile(r"(?m)^>\s*配時.*?口白\s*\*{0,2}\s*([0-9]+)\s*字")


def body_after_first_unit(text, path):
    """丟掉分段標題,從第一個單元標題切到檔尾。"""
    hs = list(H1.finditer(text))
    if len(hs) < 2:
        sys.exit(f"🔴 {os.path.basename(path)} 只有 {len(hs)} 個 H1,結構不符預期")
    return text[hs[1].start():].rstrip() + "\n"


def narration_chars(unit_text):
    """取出該單元「## 口白逐字」區塊的可計字元數。"""
    m = NARR.search(unit_text)
    if not m:
        return 0, ""
    rest = unit_text[m.end():]
    nxt = NEXT_H.search(rest)
    block = rest[:nxt.start()] if nxt else rest
    block = STAGE.sub("", block)          # 🔴 先剝掉舞台指示(錄影標記 / 交界移交)
    # 去掉引言區塊(> …)與 markdown 強調記號
    lines = [l for l in block.split("\n") if not l.lstrip().startswith(">")]
    plain = re.sub(r"[*_`~]", "", "\n".join(lines))
    return len(COUNTABLE.findall(plain)), plain.strip()


def main():
    bodies = [body_after_first_unit(open(p, encoding="utf-8").read(), p) for p in PARTS]
    merged = "\n\n".join(b.strip() for b in bodies) + "\n"

    # 逐單元配時
    units = list(H1.finditer(merged))
    rows, total = [], 0
    for i, m in enumerate(units):
        end = units[i + 1].start() if i + 1 < len(units) else len(merged)
        unit = merged[m.start():end]
        n, _ = narration_chars(unit)
        d = DECL.search(unit)
        if d and int(d.group(1)) != n:
            print(f"⚠ 護欄:{m.group(1).strip()[:28]} 實算 {n} 字 ≠ 自帶宣告 {d.group(1)} 字"
                  f" —— 先查是內容改了還是抽取歪了")
        rows.append((m.group(1).strip(), n, n / RATE))
        total += n
    secs = total / RATE

    hdr = [
        f"# A3 v4 · 十頁內容 {VER}(地端 VLM 事件判讀)",
        "",
        "> 由 `_v2_parts/` 三份分段檔經 `scripts/assemble_v2.py` 機械串接 —— "
        "**改內容請改分段檔,不要改本檔**。",
        "> 位階:`20_第四輪裁決`(本輪最高)> `19_Kenny第三批答覆` > `17_Codex異家族審查`",
        "> > `16_地端VLM方案升級` > `15_全案重算`(數字)> `13_參考文獻查證`(引用)",
        "> > `09_修訂裁決`(含 Codex 覆蓋層)> `06_修訂總則` > 本檔。",
        ">",
        "> **審查軌跡**:v1 → 第一路對抗 → 整合稽核 → 四鏡頭二路對抗 → 九條裁決 → v2",
        "> → **Codex 異家族(六 CLAIM,四 REFUTED)** → 六條覆蓋層 → v2.1 → 獨立複驗",
        "> → **Kenny 第二批答覆 → 全案重算(4.4→5.25 分)** → v2.2",
        "> → **方案升級為地端 VLM** → v2.3",
        "> → **Codex 二度異家族審查(六 CLAIM,四 REFUTED,判不可錄製)** → Kenny 第三批答覆",
        f"> → **裁決 P–V 八項落地** → **{VER}**(本版)",
        "",
        f"## 配時(本表由 `assemble_v2.py` 實算,非 agent 自報)",
        "",
        f"| 單位 | 口白字數 | 秒({RATE} 字/秒) |",
        "|---|---:|---:|",
    ]
    for name, n, s in rows:
        hdr.append(f"| {name} | {n} | {s:.1f} |")
    hdr += [
        f"| **合計** | **{total}** | **{secs:.1f} 秒 = {int(secs // 60)}:{int(secs % 60):02d}** |",
        "",
        (f"距 {HARD_LIMIT:.0f} 秒硬上限餘裕 **{HARD_LIMIT - secs:.1f} 秒**。"
         if secs <= HARD_LIMIT else
         f"🔴 **超出硬上限 {secs - HARD_LIMIT:.1f} 秒 —— 必須砍字**。"),
        "",
        "---",
        "",
    ]
    open(OUT, "w", encoding="utf-8", newline="").write("\n".join(hdr) + merged)

    print(f"✅ 重組完成 → {os.path.basename(OUT)}  ({len(merged):,} 字元內容 + 檔頭)")
    print(f"\n{'單位':44}{'字數':>6}{'秒':>8}")
    for name, n, s in rows:
        print(f"  {name[:42]:42}{n:6}{s:8.1f}")
    print(f"  {'合計':42}{total:6}{secs:8.1f}  = {int(secs//60)}:{int(secs%60):02d}")
    if secs > HARD_LIMIT:
        print(f"\n🔴 超出 600 秒硬上限 {secs - HARD_LIMIT:.1f} 秒")
    else:
        print(f"\n✅ 餘裕 {HARD_LIMIT - secs:.1f} 秒")
    return 0 if secs <= HARD_LIMIT else 1


if __name__ == "__main__":
    sys.exit(main())
