"""run_improvement.py — Thực nghiệm ĐỀ XUẤT CẢI TIẾN: CORI+ vs CORI.

CORI+ cắt tỉa bằng cận trên all-confidence của bond (bond ≤ allconf), nhờ đó
né phần lớn phép hợp DTID-List tốn kém trên dữ liệu dày, MÀ cho kết quả đồng
nhất với CORI gốc.

Script này:
  1. KIỂM CHỨNG ĐÚNG ĐẮN: cori_plus cho kết quả TRÙNG KHỚP cori (assert), cả
     trên ví dụ slide lẫn trên UCI Mushroom ở nhiều ngưỡng.
  2. ĐO HIỆU NĂNG: thời gian CORI vs CORI+ và tỉ lệ phép hợp DTID né được,
     theo minbond, trên UCI Mushroom.

Kết quả ghi vào ../results/ (CSV + Markdown + PNG). Chạy: python3 run_improvement.py
"""

from __future__ import annotations

import csv
import os
import statistics
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from rare_mining import (
    TransactionDB, cori, cori_plus, load_uci_mushroom, slide_example_db,
)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
RESULTS = os.path.join(HERE, "..", "results")
os.makedirs(RESULTS, exist_ok=True)

REPEAT = 5  # lặp mỗi cấu hình để lấy trung vị thời gian (giảm nhiễu đo)


def time_median(fn, repeat: int = REPEAT) -> float:
    ts = []
    for _ in range(repeat):
        t0 = time.perf_counter()
        fn()
        ts.append(time.perf_counter() - t0)
    return statistics.median(ts)


def main() -> None:
    # --- 0. Kiểm chứng đúng đắn trên ví dụ slide --------------------------------
    db_ex = slide_example_db()
    r_old = cori(db_ex, maxsup=3, minbond=0.6)
    r_new, _ = cori_plus(db_ex, maxsup=3, minbond=0.6)
    assert r_old == r_new, f"CORI+ khác CORI trên ví dụ slide: {r_new} vs {r_old}"

    # --- 1. UCI Mushroom --------------------------------------------------------
    db = load_uci_mushroom(os.path.join(DATA, "agaricus-lepiota.data"))
    maxsup = 0.1 * db.n
    minbonds = (0.95, 0.9, 0.8, 0.7, 0.6, 0.5)

    rows = []
    for mb in minbonds:
        # kiểm chứng đồng nhất kết quả trên dữ liệu thực
        res_old = cori(db, maxsup=maxsup, minbond=mb, max_size=4)
        res_new, stats = cori_plus(db, maxsup=maxsup, minbond=mb, max_size=4)
        assert res_old == res_new, f"CORI+ khác CORI tại minbond={mb}"

        t_old = time_median(lambda: cori(db, maxsup=maxsup, minbond=mb, max_size=4))
        t_new = time_median(lambda: cori_plus(db, maxsup=maxsup, minbond=mb, max_size=4))

        cand = stats["union_done"] + stats["union_skipped"]
        pct_skip = 100.0 * stats["union_skipped"] / cand if cand else 0.0
        speedup = t_old / t_new if t_new else float("nan")
        rows.append({
            "minbond": mb,
            "n_result": len(res_new),
            "union_done": stats["union_done"],
            "union_skipped": stats["union_skipped"],
            "pct_union_skipped": round(pct_skip, 1),
            "time_cori_ms": round(t_old * 1000, 1),
            "time_cori_plus_ms": round(t_new * 1000, 1),
            "speedup": round(speedup, 2),
        })
        print(f"[minbond={mb}] |result|={len(res_new)} (trùng CORI) | "
              f"union né={pct_skip:.1f}% | CORI {t_old*1000:.1f}ms -> "
              f"CORI+ {t_new*1000:.1f}ms | x{speedup:.2f}")

    # --- ghi CSV ----------------------------------------------------------------
    with open(os.path.join(RESULTS, "improvement_cori_plus.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # --- vẽ hình ----------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    xs = [r["minbond"] for r in rows]
    ax1.plot(xs, [r["time_cori_ms"] for r in rows], "o-", label="CORI (gốc)")
    ax1.plot(xs, [r["time_cori_plus_ms"] for r in rows], "s-", label="CORI+ (cải tiến)")
    ax1.invert_xaxis()
    ax1.set_xlabel("minbond"); ax1.set_ylabel("Thời gian (ms, trung vị 5 lần)")
    ax1.set_title("Thời gian chạy: CORI vs CORI+ (Mushroom)")
    ax1.legend(); ax1.grid(alpha=.3)

    ax2.plot(xs, [r["pct_union_skipped"] for r in rows], "^-", color="tab:green")
    ax2.invert_xaxis()
    ax2.set_xlabel("minbond"); ax2.set_ylabel("% phép hợp DTID né được")
    ax2.set_title("Cận trên all-confidence né bao nhiêu phép hợp")
    ax2.grid(alpha=.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS, "improvement_cori_plus.png"), dpi=150)

    # --- Markdown ---------------------------------------------------------------
    md = ["# Thực nghiệm cải tiến — CORI+ (cận trên all-confidence)", "",
          "Kiểm chứng: với MỌI minbond khảo sát, `cori_plus` cho kết quả TRÙNG "
          "KHỚP `cori` (assert pass) — cải tiến chỉ thay đổi chi phí, không đổi "
          "kết quả.", "",
          f"Dữ liệu: UCI Mushroom ({db.n} giao dịch), maxsup = 0.1, max_size = 4. "
          f"Thời gian là trung vị {REPEAT} lần chạy.", "",
          "| minbond | #Kết quả | #Hợp DTID đã làm | #Hợp né được | % né | "
          "CORI (ms) | CORI+ (ms) | Tăng tốc |",
          "|---|---|---|---|---|---|---|---|"]
    md += [f"| {r['minbond']} | {r['n_result']} | {r['union_done']} | "
           f"{r['union_skipped']} | {r['pct_union_skipped']} | "
           f"{r['time_cori_ms']} | {r['time_cori_plus_ms']} | x{r['speedup']} |"
           for r in rows]
    with open(os.path.join(RESULTS, "improvement_cori_plus.md"), "w") as f:
        f.write("\n".join(md) + "\n")
    print("[done] ghi results/improvement_cori_plus.{csv,md,png}")


if __name__ == "__main__":
    main()
