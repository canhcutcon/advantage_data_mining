"""run_experiments.py — Thực nghiệm cho báo cáo Rare Pattern Mining.

Phần 1 (SANITY CHECK): chạy mọi thuật toán trên dataset 4 giao dịch trong slide
và ĐỐI CHIẾU TỰ ĐỘNG (assert) với từng con số in trong slide. Nếu một phép
đối chiếu sai, script dừng với AssertionError — bảo đảm cài đặt đúng lý thuyết.

Phần 2 (UCI MUSHROOM): khảo sát hành vi 3 thuật toán theo ngưỡng trên dữ liệu
thực (8124 giao dịch, 23 thuộc tính → item dạng "thuộc_tính=giá_trị"):
  - Exp A: AprioriRare  — số itemset phổ biến / số mRI / thời gian theo minsup
  - Exp B: AprioriInverse — số PRI / thời gian theo (minsup, maxsup)
  - Exp C: CORI         — số rare correlated itemset / thời gian theo minbond

Kết quả ghi vào ../results/ (CSV + Markdown + PNG).
Chạy:  python3 run_experiments.py
"""

from __future__ import annotations

import csv
import os
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from rare_mining import (
    TransactionDB, apriori, apriori_rare, apriori_inverse, cori,
    bond, all_confidence, pair_measures, load_uci_mushroom, slide_example_db,
)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
RESULTS = os.path.join(HERE, "..", "results")
os.makedirs(RESULTS, exist_ok=True)


def fs(itemset) -> str:
    return "{" + ", ".join(itemset) + "}"


# ===========================================================================
# PHẦN 1 — SANITY CHECK trên dataset trong slide
# ===========================================================================

def part1_sanity() -> list[str]:
    db = slide_example_db()
    lines = ["# Sanity check — đối chiếu cài đặt với slide bài giảng",
             "",
             "Dataset: T1{pasta, lemon, bread, orange}, T2{pasta, lemon}, "
             "T3{pasta, orange, cake}, T4{pasta, lemon, orange, cake}", ""]

    # --- 1. FIM (slide tr.18): minsup = 2 --------------------------------------
    # LƯU Ý: danh sách chữ ở slide tr.18 liệt kê 10 itemset và BỎ SÓT
    # {pasta, orange, cake} (sup = 2, có mặt trong T3 và T4). Hình lattice ở
    # tr.2 của chính slide lại vẽ node "poc" là itemset PHỔ BIẾN (màu trắng),
    # nhất quán với kết quả tính toán. Đây là thiếu sót nhỏ của slide;
    # kết quả đúng là 11 itemset phổ biến.
    freq = apriori(db, minsup=2)
    expected_freq = {
        ("lemon",): 3, ("pasta",): 4, ("orange",): 3, ("cake",): 2,
        ("lemon", "pasta"): 3, ("lemon", "orange"): 2, ("orange", "pasta"): 3,
        ("cake", "pasta"): 2, ("cake", "orange"): 2,
        ("lemon", "orange", "pasta"): 2, ("cake", "orange", "pasta"): 2,
    }
    assert freq == expected_freq, f"FIM sai: {freq}"
    lines += ["## 1. Frequent itemsets (minsup = 2) — khớp lattice slide tr.2",
              "",
              "⚠️ Danh sách chữ ở slide tr.18 bỏ sót {pasta, orange, cake} "
              "(sup = 2, thuộc T3 và T4); hình lattice tr.2 vẽ đúng node `poc` "
              "là itemset phổ biến. Kết quả đúng: **11** itemset phổ biến.",
              "", "| Itemset | Support |", "|---|---|"]
    lines += [f"| {fs(k)} | {v} |" for k, v in sorted(freq.items(), key=lambda x: (len(x[0]), x[0]))]
    lines.append("")

    # --- 2. AprioriRare (slide tr.4-11): minsup = 2 → mRI ---------------------
    _, mri = apriori_rare(db, minsup=2)
    expected_mri = {("bread",): 1, ("cake", "lemon"): 1}
    assert mri == expected_mri, f"mRI sai: {mri}"
    lines += ["## 2. AprioriRare — minimal rare itemsets (minsup = 2) — khớp slide tr.5–11",
              "", "| mRI | Support |", "|---|---|"]
    lines += [f"| {fs(k)} | {v} |" for k, v in sorted(mri.items())]
    lines.append("")

    # --- 3. AprioriInverse (slide tr.12): maxsup = 1.9, minsup = 1 → {bread} --
    pri = apriori_inverse(db, minsup=1, maxsup=1.9)
    assert pri == {("bread",): 1}, f"PRI sai: {pri}"
    lines += ["## 3. AprioriInverse — perfectly rare itemsets (minsup = 1, maxsup = 1.9) — khớp slide tr.12",
              "", "| PRI | Support |", "|---|---|",
              f"| {fs(('bread',))} | 1 |", ""]

    # (biến thể slide tr.13–14: maxsup = 3.1, minsup = 1.1)
    pri2 = apriori_inverse(db, minsup=1.1, maxsup=3.1)
    expected_pri2 = {("lemon",): 3, ("orange",): 3, ("cake",): 2,
                     ("lemon", "orange"): 2, ("cake", "orange"): 2}
    assert pri2 == expected_pri2, f"PRI2 sai: {pri2}"
    lines += ["Biến thể (minsup = 1.1, maxsup = 3.1):",
              "", "| PRI | Support |", "|---|---|"]
    lines += [f"| {fs(k)} | {v} |" for k, v in sorted(pri2.items(), key=lambda x: (len(x[0]), x[0]))]
    lines.append("")

    # --- 4. bond (slide tr.24-28) ---------------------------------------------
    checks_bond = {
        ("pasta", "orange"): 0.75,      # tr.24: 3/4
        ("cake", "bread"): 0.0,         # tr.27: 0/3
        ("lemon", "bread"): 1 / 3,      # tr.27
        ("lemon", "orange"): 0.5,       # tr.27: 2/4
        ("pasta", "lemon"): 0.75,       # tr.27: 3/4
    }
    for pair_, exp in checks_bond.items():
        got = bond(db, pair_)
        assert abs(got - exp) < 1e-9, f"bond{pair_} = {got} ≠ {exp}"
    assert all(abs(bond(db, [i]) - 1.0) < 1e-9 for i in db.items)  # Property 1
    assert abs(bond(db, ["pasta", "lemon", "orange"]) - 0.5) < 1e-9  # tr.29: 2/4
    lines += ["## 4. Độ đo bond — khớp slide tr.24–29 (kể cả Property 1: bond(item đơn) = 1)",
              "", "| Itemset | bond |", "|---|---|"]
    lines += [f"| {fs(k)} | {v:.4g} |" for k, v in checks_bond.items()]
    lines += [f"| {fs(('pasta', 'lemon', 'orange'))} | 0.5 |", ""]

    # --- 5. all-confidence (slide tr.42-45) ------------------------------------
    assert abs(all_confidence(db, ["pasta", "orange"]) - 0.75) < 1e-9       # tr.42
    assert abs(all_confidence(db, ["lemon", "orange", "cake"]) - 1 / 3) < 1e-9  # tr.43
    assert abs(all_confidence(db, ["pasta", "lemon", "orange"]) - 0.5) < 1e-9   # tr.45
    lines += ["## 5. All-confidence — khớp slide tr.42–45", "",
              "| Itemset | allconf |", "|---|---|",
              "| {pasta, orange} | 0.75 |",
              "| {lemon, orange, cake} | 0.3333 |",
              "| {pasta, lemon, orange} | 0.5 |", ""]

    # --- 6. Correlated frequent itemsets bằng bond (slide tr.31) ---------------
    freq2 = apriori(db, minsup=2)
    corr_freq = {k: (v, bond(db, k)) for k, v in freq2.items()
                 if bond(db, k) >= 0.75}
    expected_cf = {("lemon",), ("pasta",), ("orange",), ("cake",),
                   ("lemon", "pasta"), ("orange", "pasta")}
    assert set(corr_freq) == expected_cf, f"correlated frequent sai: {corr_freq}"
    lines += ["## 6. Correlated frequent itemsets (minsup = 2, minbond = 0.75) — khớp slide tr.31",
              "", "| Itemset | sup | bond |", "|---|---|---|"]
    lines += [f"| {fs(k)} | {s} | {b:.2f} |" for k, (s, b) in sorted(corr_freq.items(), key=lambda x: (len(x[0]), x[0]))]
    lines.append("")

    # --- 7. CORI — rare correlated itemsets (slide tr.33) ----------------------
    rc = cori(db, maxsup=3, minbond=0.6)
    expected_rc = {("bread",): (1, 1.0), ("cake",): (2, 1.0)}
    got_oc = rc.get(("cake", "orange"))
    assert got_oc and got_oc[0] == 2 and abs(got_oc[1] - 2 / 3) < 1e-9
    rest = {k: v for k, v in rc.items() if k != ("cake", "orange")}
    assert rest == expected_rc, f"CORI sai: {rc}"
    lines += ["## 7. CORI — rare correlated itemsets (maxsup = 3, minbond = 0.6) — khớp slide tr.33",
              "", "| Itemset | sup | bond |", "|---|---|---|",
              "| {bread} | 1 | 1.00 |", "| {cake} | 2 | 1.00 |",
              "| {orange, cake} | 2 | 0.66 |", ""]

    # --- 8. TID-List / DTID-List (slide tr.36-39) -------------------------------
    assert db.tidset(["pasta"]) == frozenset({0, 1, 2, 3})
    assert db.tidset(["pasta", "lemon"]) == frozenset({0, 1, 3})
    assert db.tidset(["bread", "orange"]) == frozenset({0})
    assert db.dtidset(["pasta"]) == frozenset({0, 1, 2, 3})
    assert db.dtidset(["pasta", "lemon"]) == frozenset({0, 1, 2, 3})
    assert db.dtidset(["bread", "orange"]) == frozenset({0, 2, 3})
    lines += ["## 8. TID-List / DTID-List — khớp slide tr.36–39", "",
              "| Itemset | TID-List | sup | DTID-List | dsup |", "|---|---|---|---|---|",
              "| {pasta} | T1 T2 T3 T4 | 4 | T1 T2 T3 T4 | 4 |",
              "| {pasta, lemon} | T1 T2 T4 | 3 | T1 T2 T3 T4 | 4 |",
              "| {bread, orange} | T1 | 1 | T1 T3 T4 | 3 |", ""]

    # --- 9. Bảng độ đo cặp (Wu et al. 2010) ------------------------------------
    pm = pair_measures(db, "pasta", "cake")
    lines += ["## 9. Các độ đo khác cho cặp minh hoạ {pasta, cake} (khung Wu et al. 2010)",
              "", "| Độ đo | Giá trị |", "|---|---|"]
    lines += [f"| {m} | {v:.4g} |" for m, v in pm.items()]
    lines += ["", "→ lift({pasta, cake}) = 1.0: dù xuất hiện ở 50% giao dịch, "
              "cặp này KHÔNG tương quan (pasta có mặt ở mọi giao dịch) — đúng "
              "nhận xét 'spurious pattern' ở slide tr.21–22.", ""]

    lines.append("**KẾT LUẬN: 100% phép đối chiếu với slide ĐẠT (assert pass).**")
    return lines


# ===========================================================================
# PHẦN 2 — UCI MUSHROOM
# ===========================================================================

def part2_mushroom() -> None:
    db = load_uci_mushroom(os.path.join(DATA, "agaricus-lepiota.data"))
    n = db.n
    n_items = len(db.items)
    avg_len = sum(len(t) for t in db.transactions) / n
    print(f"[mushroom] n={n}, |items|={n_items}, avg_len={avg_len:.2f}")

    stats = [f"- Số giao dịch: **{n}**",
             f"- Số item phân biệt (thuộc_tính=giá_trị): **{n_items}**",
             f"- Độ dài giao dịch trung bình: **{avg_len:.2f}**"]

    # --- Exp A: AprioriRare theo minsup ---------------------------------------
    rows_a = []
    for rel in (0.6, 0.5, 0.4, 0.3, 0.25, 0.2):
        ms = rel * n
        t0 = time.perf_counter()
        freq, mri = apriori_rare(db, minsup=ms)
        dt = time.perf_counter() - t0
        rows_a.append({"minsup_rel": rel, "minsup_abs": int(ms),
                       "n_frequent": len(freq), "n_mri": len(mri),
                       "time_s": round(dt, 3)})
        print(f"[A] minsup={rel:.2f} -> freq={len(freq)}, mRI={len(mri)}, {dt:.2f}s")

    # --- Exp B: AprioriInverse theo (minsup, maxsup) ----------------------------
    rows_b = []
    for max_rel in (0.05, 0.10, 0.20):
        for min_rel in (0.01, 0.02, 0.05):
            if min_rel >= max_rel:
                continue
            t0 = time.perf_counter()
            pri = apriori_inverse(db, minsup=min_rel * n, maxsup=max_rel * n)
            dt = time.perf_counter() - t0
            max_size = max((len(k) for k in pri), default=0)
            rows_b.append({"minsup_rel": min_rel, "maxsup_rel": max_rel,
                           "n_pri": len(pri), "max_size": max_size,
                           "time_s": round(dt, 3)})
            print(f"[B] minsup={min_rel}, maxsup={max_rel} -> PRI={len(pri)} "
                  f"(max size {max_size}), {dt:.2f}s")

    # --- Exp C: CORI theo minbond ------------------------------------------------
    rows_c = []
    for minbond in (0.95, 0.9, 0.8, 0.7, 0.6, 0.5):
        t0 = time.perf_counter()
        rc = cori(db, maxsup=0.1 * n, minbond=minbond, max_size=4)
        dt = time.perf_counter() - t0
        max_size = max((len(k) for k in rc), default=0)
        rows_c.append({"maxsup_rel": 0.1, "minbond": minbond,
                       "n_rare_corr": len(rc), "max_size": max_size,
                       "time_s": round(dt, 3)})
        print(f"[C] minbond={minbond} -> rare-corr={len(rc)} "
              f"(max size {max_size}), {dt:.2f}s")

    # ví dụ mẫu hiếm tương quan tiêu biểu (bond cao, support thấp)
    rc = cori(db, maxsup=0.1 * n, minbond=0.9, max_size=4)
    top = sorted(((k, v) for k, v in rc.items() if len(k) >= 2),
                 key=lambda x: (-x[1][1], x[1][0]))[:10]

    # --- ghi CSV -----------------------------------------------------------------
    for name, rows in (("expA_apriorirare", rows_a),
                       ("expB_aprioriinverse", rows_b),
                       ("expC_cori", rows_c)):
        with open(os.path.join(RESULTS, f"{name}.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    # --- vẽ hình -------------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    ax = axes[0]
    xs = [r["minsup_rel"] for r in rows_a]
    ax.plot(xs, [r["n_frequent"] for r in rows_a], "o-", label="Frequent itemsets")
    ax.plot(xs, [r["n_mri"] for r in rows_a], "s-", label="Minimal rare itemsets")
    ax.set_yscale("log"); ax.invert_xaxis()
    ax.set_xlabel("minsup (tỉ lệ)"); ax.set_ylabel("Số itemset (log)")
    ax.set_title("Exp A — AprioriRare (Mushroom)"); ax.legend(); ax.grid(alpha=.3)

    ax = axes[1]
    for max_rel in (0.05, 0.10, 0.20):
        sub = [r for r in rows_b if r["maxsup_rel"] == max_rel]
        ax.plot([r["minsup_rel"] for r in sub], [r["n_pri"] for r in sub],
                "o-", label=f"maxsup={max_rel}")
    ax.set_yscale("log"); ax.invert_xaxis()
    ax.set_xlabel("minsup (tỉ lệ)"); ax.set_ylabel("Số PRI (log)")
    ax.set_title("Exp B — AprioriInverse (Mushroom)"); ax.legend(); ax.grid(alpha=.3)

    ax = axes[2]
    ax.plot([r["minbond"] for r in rows_c], [r["n_rare_corr"] for r in rows_c], "o-",
            color="tab:red")
    ax.set_yscale("log"); ax.invert_xaxis()
    ax.set_xlabel("minbond"); ax.set_ylabel("Số rare correlated itemset (log)")
    ax.set_title("Exp C — CORI (Mushroom, maxsup = 0.1)"); ax.grid(alpha=.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS, "mushroom_experiments.png"), dpi=150)

    # hình thời gian chạy
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.plot(xs, [r["time_s"] for r in rows_a], "o-", label="AprioriRare")
    ax2.invert_xaxis(); ax2.set_xlabel("minsup (tỉ lệ)")
    ax2.set_ylabel("Thời gian (giây)"); ax2.grid(alpha=.3)
    ax2.set_title("Thời gian chạy AprioriRare theo minsup (Mushroom)")
    ax2.legend(); fig2.tight_layout()
    fig2.savefig(os.path.join(RESULTS, "mushroom_runtime.png"), dpi=150)

    # --- Markdown tổng hợp ----------------------------------------------------------
    md = ["# Kết quả thực nghiệm trên UCI Mushroom", "", "## Thống kê dữ liệu", ""]
    md += stats + ["",
        "## Exp A — AprioriRare", "",
        "| minsup (tỉ lệ) | minsup (abs) | #Frequent | #mRI | Thời gian (s) |",
        "|---|---|---|---|---|"]
    md += [f"| {r['minsup_rel']} | {r['minsup_abs']} | {r['n_frequent']} | "
           f"{r['n_mri']} | {r['time_s']} |" for r in rows_a]
    md += ["", "## Exp B — AprioriInverse", "",
        "| minsup | maxsup | #PRI | Kích thước max | Thời gian (s) |",
        "|---|---|---|---|---|"]
    md += [f"| {r['minsup_rel']} | {r['maxsup_rel']} | {r['n_pri']} | "
           f"{r['max_size']} | {r['time_s']} |" for r in rows_b]
    md += ["", "## Exp C — CORI (maxsup = 0.1, max_size = 4)", "",
        "| minbond | #Rare correlated | Kích thước max | Thời gian (s) |",
        "|---|---|---|---|"]
    md += [f"| {r['minbond']} | {r['n_rare_corr']} | {r['max_size']} | "
           f"{r['time_s']} |" for r in rows_c]
    md += ["", "## 10 mẫu hiếm tương quan tiêu biểu (|X| ≥ 2, minbond = 0.9)", "",
           "| Itemset | sup | bond |", "|---|---|---|"]
    md += [f"| {fs(k)} | {s} | {b:.3f} |" for k, (s, b) in top]
    with open(os.path.join(RESULTS, "mushroom_results.md"), "w") as f:
        f.write("\n".join(md) + "\n")


if __name__ == "__main__":
    t0 = time.perf_counter()
    lines = part1_sanity()
    with open(os.path.join(RESULTS, "sanity_check.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("[sanity] 100% assert PASS — ghi results/sanity_check.md")
    part2_mushroom()
    print(f"[done] tổng thời gian {time.perf_counter() - t0:.1f}s — "
          f"kết quả trong results/")
