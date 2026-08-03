# -*- coding: utf-8 -*-
"""A2b 交件前的 notebook 清理 —— 每次重跑 Restart & Run All 之後都要跑一次。

清掉三種「執行環境留下、但不該出現在交件檔裡」的東西:

  1. cell metadata 裡的 `execution` 時間戳(iopub.execute_input / status.busy / status.idle)
     `nbconvert --execute` 會寫進去,內容是 UTC 時間,會與宣稱的繳交日對不上。
  2. stderr 輸出 —— 目前只有 joblib 找不到實體核心數的 UserWarning,
     內含 1200+ 字元 traceback 與 c:\\Users\\kenny\\... 本機絕對路徑,交件檔不需要。
  3. VS Code Data Wrangler 的專屬 payload
     (application/vnd.microsoft.datawrangler.viewer.v0+json)——
     只有裝了該擴充的 VS Code 認得,標準 Jupyter 用不到,純粹讓檔案變大。

**只動 outputs 與 metadata,不動任何 source。** 可重複執行。

用法:
    python "Artificial Intelligence for Enterprises/notes/practice/a2b_clean_outputs.py"
"""
import os
import sys

import nbformat

NB = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "Assessment2b",
    "Huang_26254793_421104_Assessment 2b.ipynb",
)
DW = "application/vnd.microsoft.datawrangler.viewer.v0+json"


def main():
    if not os.path.exists(NB):
        print("找不到 notebook:%s" % NB)
        return 1

    nb = nbformat.read(NB, as_version=4)

    n_exec = n_err = n_dw = 0
    for c in nb.cells:
        if "execution" in c.get("metadata", {}):
            del c.metadata["execution"]
            n_exec += 1
        if c.cell_type != "code":
            continue
        keep = []
        for o in c.get("outputs", []):
            if o.get("output_type") == "stream" and o.get("name") == "stderr":
                n_err += 1
                continue
            if DW in o.get("data", {}):
                del o["data"][DW]
                n_dw += 1
            keep.append(o)
        c.outputs = keep

    if n_exec or n_err or n_dw:
        nbformat.write(nb, NB)
        print("已清除:execution metadata %d 組 / stderr %d 筆 / Data Wrangler payload %d 個"
              % (n_exec, n_err, n_dw))
    else:
        print("乾淨,無需清理")

    codes = [c for c in nb.cells if c.cell_type == "code"]
    ec = [c.execution_count for c in codes]
    print("結構:%d cells / %d code,執行序 %s"
          % (len(nb.cells), len(codes),
             "連續 1→%d" % len(ec) if ec == list(range(1, len(ec) + 1)) else str(ec)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
