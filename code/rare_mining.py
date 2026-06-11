"""rare_mining.py — Cài đặt các thuật toán khai thác mẫu hiếm (Rare Pattern Mining).

Bài tập lớn môn Khai thác dữ liệu nâng cao.
Cài đặt theo slide "AdvancedDataMining_02_RareItemset Techniques" và các bài báo gốc:

- Apriori                : Agrawal & Srikant, VLDB 1994 (nền tảng, để so sánh)
- AprioriRare            : Szathmary, Napoli, Valtchev, ICTAI 2007
                           (minimal rare itemsets — mRI)
- AprioriInverse         : Koh & Rountree, PAKDD 2005
                           (perfectly rare itemsets — PRI)
- CORI                   : Bouasker & Ben Yahia, ACM SAC 2015
                           (rare correlated itemsets, độ đo bond, nền Eclat)
- Độ đo tương quan        : bond, all-confidence (Omiecinski, TKDE 2003);
                           lift, cosine, kulc, maxconf, chi2 (Wu et al., DMKD 2010)

Chỉ dùng thư viện chuẩn Python. Support tính bằng SỐ GIAO DỊCH (absolute count);
các ngưỡng minsup/maxsup chấp nhận số thực (vd. maxsup = 1.9 như ví dụ trong slide).
"""

from __future__ import annotations

from itertools import combinations
from typing import Iterable


Itemset = tuple[str, ...]  # itemset chuẩn hoá: tuple các item đã sort


# ---------------------------------------------------------------------------
# Cơ sở dữ liệu giao dịch
# ---------------------------------------------------------------------------

class TransactionDB:
    """CSDL giao dịch với chỉ mục dọc (vertical layout).

    Mỗi item giữ một TID-set: tập chỉ số các giao dịch chứa item đó.
    Đây chính là biểu diễn TID-List của Eclat (Zaki, TKDE 2000) mà CORI kế thừa.
    """

    def __init__(self, transactions: Iterable[Iterable[str]]):
        self.transactions: list[frozenset[str]] = [frozenset(t) for t in transactions]
        self.n: int = len(self.transactions)
        item_tids: dict[str, set[int]] = {}
        for tid, t in enumerate(self.transactions):
            for item in t:
                item_tids.setdefault(item, set()).add(tid)
        self.item_tids: dict[str, frozenset[int]] = {
            i: frozenset(s) for i, s in item_tids.items()
        }
        self.items: list[str] = sorted(self.item_tids)

    # --- support hội (conjunctive) & tuyển (disjunctive) -------------------
    def tidset(self, itemset: Iterable[str]) -> frozenset[int]:
        """TID-List: các giao dịch chứa TẤT CẢ item của itemset."""
        its = list(itemset)
        result = self.item_tids[its[0]]
        for i in its[1:]:
            result = result & self.item_tids[i]
        return result

    def dtidset(self, itemset: Iterable[str]) -> frozenset[int]:
        """DTID-List: các giao dịch chứa ÍT NHẤT MỘT item của itemset."""
        result: frozenset[int] = frozenset()
        for i in itemset:
            result = result | self.item_tids[i]
        return result

    def sup(self, itemset: Iterable[str]) -> int:
        """Support hội: sup(X) = |{T | X ⊆ T}|."""
        return len(self.tidset(itemset))

    def dsup(self, itemset: Iterable[str]) -> int:
        """Support tuyển: dsup(X) = |{T | X ∩ T ≠ ∅}|."""
        return len(self.dtidset(itemset))


# ---------------------------------------------------------------------------
# Độ đo tương quan
# ---------------------------------------------------------------------------

def bond(db: TransactionDB, itemset: Iterable[str]) -> float:
    """bond(X) = sup(X) / dsup(X)  (Omiecinski 2003). Null-invariant, anti-monotone."""
    d = db.dsup(itemset)
    return db.sup(itemset) / d if d else 0.0


def all_confidence(db: TransactionDB, itemset: Iterable[str]) -> float:
    """allconf(X) = sup(X) / max{sup(i) | i ∈ X}  (Omiecinski 2003)."""
    items = list(itemset)
    m = max(len(db.item_tids[i]) for i in items)
    return db.sup(items) / m if m else 0.0


def pair_measures(db: TransactionDB, a: str, b: str) -> dict[str, float]:
    """Các độ đo cho cặp item (a, b) theo bảng của Wu et al. (DMKD 2010)."""
    n = db.n
    sa, sb = len(db.item_tids[a]), len(db.item_tids[b])
    sab = db.sup([a, b])
    # bảng tiếp liên 2x2 cho chi2
    o = {
        (1, 1): sab,
        (1, 0): sa - sab,
        (0, 1): sb - sab,
        (0, 0): n - sa - sb + sab,
    }
    chi2 = 0.0
    for (i, j), obs in o.items():
        pa = sa / n if i == 1 else 1 - sa / n
        pb = sb / n if j == 1 else 1 - sb / n
        exp = n * pa * pb
        if exp > 0:
            chi2 += (obs - exp) ** 2 / exp
    return {
        "sup": sab,
        "chi2": chi2,
        "lift": (sab / n) / ((sa / n) * (sb / n)) if sa and sb else 0.0,
        "allconf": sab / max(sa, sb),
        "coherence(bond)": bond(db, [a, b]),
        "cosine": sab / (sa * sb) ** 0.5 if sa and sb else 0.0,
        "kulc": (sab / 2) * (1 / sa + 1 / sb) if sa and sb else 0.0,
        "maxconf": max(sab / sa if sa else 0.0, sab / sb if sb else 0.0),
    }


# ---------------------------------------------------------------------------
# Apriori (baseline) — sinh ứng viên theo mức với TID-set
# ---------------------------------------------------------------------------

def _join_candidates(prev_level: dict[Itemset, frozenset[int]], k: int
                     ) -> list[tuple[Itemset, frozenset[int], frozenset[int]]]:
    """Bước join của Apriori: nối hai (k-1)-itemset chung tiền tố (k-2).

    Trả về [(ứng viên k item, tidset cha 1, tidset cha 2)].
    """
    keys = sorted(prev_level)
    out = []
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            x, y = keys[i], keys[j]
            if x[: k - 2] != y[: k - 2]:
                break  # keys đã sort theo tiền tố — hết nhóm chung tiền tố
            cand = x + (y[-1],)
            out.append((cand, prev_level[x], prev_level[y]))
    return out


def _subsets_all_in(cand: Itemset, level: dict[Itemset, frozenset[int]]) -> bool:
    """Bước prune của Apriori: mọi tập con (k-1) phải nằm trong mức trước."""
    return all(cand[:i] + cand[i + 1:] in level for i in range(len(cand)))


def apriori(db: TransactionDB, minsup: float) -> dict[Itemset, int]:
    """Apriori chuẩn: trả về mọi itemset phổ biến {itemset: support}."""
    frequent: dict[Itemset, int] = {}
    level: dict[Itemset, frozenset[int]] = {}
    for item, tids in db.item_tids.items():
        if len(tids) >= minsup:
            level[(item,)] = tids
            frequent[(item,)] = len(tids)
    k = 2
    while level:
        next_level: dict[Itemset, frozenset[int]] = {}
        for cand, t1, t2 in _join_candidates(level, k):
            if not _subsets_all_in(cand, level):
                continue
            tids = t1 & t2
            if len(tids) >= minsup:
                next_level[cand] = tids
                frequent[cand] = len(tids)
        level = next_level
        k += 1
    return frequent


# ---------------------------------------------------------------------------
# AprioriRare (Szathmary et al., ICTAI 2007) — minimal rare itemsets
# ---------------------------------------------------------------------------

def apriori_rare(db: TransactionDB, minsup: float
                 ) -> tuple[dict[Itemset, int], dict[Itemset, int]]:
    """AprioriRare: duyệt theo mức như Apriori với HAI khác biệt (đúng slide):

    1. Ứng viên k item KHÔNG phổ biến nhưng mọi tập con (k-1) đều phổ biến
       → là MINIMAL RARE ITEMSET (mRI), được thu thập.
    2. Itemset không phổ biến KHÔNG được dùng để sinh ứng viên lớn hơn.

    Trả về (frequent itemsets, minimal rare itemsets).
    """
    frequent: dict[Itemset, int] = {}
    minimal_rare: dict[Itemset, int] = {}

    # Mức 1: tập rỗng luôn phổ biến (sup = n ≥ minsup), nên mọi item đơn
    # không phổ biến đều là mRI.
    level: dict[Itemset, frozenset[int]] = {}
    for item, tids in db.item_tids.items():
        if len(tids) >= minsup:
            level[(item,)] = tids
            frequent[(item,)] = len(tids)
        else:
            minimal_rare[(item,)] = len(tids)

    k = 2
    while level:
        next_level: dict[Itemset, frozenset[int]] = {}
        for cand, t1, t2 in _join_candidates(level, k):
            if not _subsets_all_in(cand, level):
                # có tập con không phổ biến → cand không phải mRI, bỏ hẳn
                continue
            tids = t1 & t2
            if len(tids) >= minsup:
                next_level[cand] = tids
                frequent[cand] = len(tids)
            else:
                # mọi tập con (k-1) phổ biến (đã qua prune) → mRI
                minimal_rare[cand] = len(tids)
        level = next_level
        k += 1
    return frequent, minimal_rare


# ---------------------------------------------------------------------------
# AprioriInverse (Koh & Rountree, PAKDD 2005) — perfectly rare itemsets
# ---------------------------------------------------------------------------

def apriori_inverse(db: TransactionDB, minsup: float, maxsup: float
                    ) -> dict[Itemset, int]:
    """AprioriInverse: tìm mọi PERFECTLY RARE ITEMSET (PRI).

    PRI: minsup ≤ sup(X) < maxsup và mọi tập con khác rỗng Y ⊂ X có
    sup(Y) < maxsup. Vì sup(Y) ≤ min{sup(i) | i ∈ Y}, điều kiện tập con
    tương đương: MỌI ITEM của X đều có sup < maxsup.

    Khác biệt cốt lõi so với Apriori (đúng slide): bước đầu LOẠI BỎ mọi item
    có sup(x) ≥ maxsup, sau đó khai thác như Apriori trên các item còn lại
    với ngưỡng dưới minsup.
    """
    pri: dict[Itemset, int] = {}
    level: dict[Itemset, frozenset[int]] = {}
    for item, tids in db.item_tids.items():
        if len(tids) >= maxsup:
            continue  # loại item phổ biến ngay từ đầu
        if len(tids) >= minsup:
            level[(item,)] = tids
            pri[(item,)] = len(tids)
    k = 2
    while level:
        next_level: dict[Itemset, frozenset[int]] = {}
        for cand, t1, t2 in _join_candidates(level, k):
            if not _subsets_all_in(cand, level):
                continue
            tids = t1 & t2
            if len(tids) >= minsup:  # sup < maxsup tự thoả (mọi item < maxsup)
                next_level[cand] = tids
                pri[cand] = len(tids)
        level = next_level
        k += 1
    return pri


# ---------------------------------------------------------------------------
# CORI (Bouasker & Ben Yahia, ACM SAC 2015) — rare correlated itemsets
# ---------------------------------------------------------------------------

def cori(db: TransactionDB, maxsup: float, minbond: float,
         max_size: int | None = None) -> dict[Itemset, tuple[int, float]]:
    """CORI: tìm mọi itemset X (|X| ≥ 1) thoả ĐỒNG THỜI hai ràng buộc:

        sup(X)  <  maxsup   (ràng buộc HIẾM   — monotone theo hướng mở rộng)
        bond(X) ≥  minbond  (ràng buộc TƯƠNG QUAN — anti-monotone)

    Cài đặt kiểu Eclat (DFS): mỗi itemset giữ cặp (TID-List, DTID-List);
    khi nối Z = X ∪ Y:
        TIDLIST(Z)  = TIDLIST(X)  ∩ TIDLIST(Y)
        DTIDLIST(Z) = DTIDLIST(X) ∪ DTIDLIST(Y)
        bond(Z)     = |TIDLIST(Z)| / |DTIDLIST(Z)|
    Cắt tỉa: bond(Z) < minbond → bỏ mọi superset của Z (anti-monotone).
    Nút có sup ≥ maxsup KHÔNG được xuất nhưng vẫn phải mở rộng tiếp,
    vì superset của nó có thể tụt xuống dưới maxsup (monotone).

    Trả về {itemset: (support, bond)}.
    """
    result: dict[Itemset, tuple[int, float]] = {}
    # sắp item theo support tăng dần (thứ tự chuẩn của Eclat cho dữ liệu thưa)
    items = sorted(db.items, key=lambda i: len(db.item_tids[i]))

    def expand(prefix: Itemset, tids: frozenset[int], dtids: frozenset[int],
               start: int) -> None:
        for idx in range(start, len(items)):
            item = items[idx]
            new_tids = tids & db.item_tids[item] if prefix else db.item_tids[item]
            new_dtids = dtids | db.item_tids[item]
            b = len(new_tids) / len(new_dtids) if new_dtids else 0.0
            if b < minbond:
                continue  # cắt tỉa anti-monotone: mọi superset cũng bị loại
            new_prefix = prefix + (item,)
            if len(new_tids) < maxsup:
                result[tuple(sorted(new_prefix))] = (len(new_tids), b)
            if max_size is None or len(new_prefix) < max_size:
                expand(new_prefix, new_tids, new_dtids, idx + 1)

    expand((), frozenset(), frozenset(), 0)
    return result


# ---------------------------------------------------------------------------
# Đọc dữ liệu
# ---------------------------------------------------------------------------

MUSHROOM_ATTRS = [
    "class", "cap-shape", "cap-surface", "cap-color", "bruises", "odor",
    "gill-attachment", "gill-spacing", "gill-size", "gill-color",
    "stalk-shape", "stalk-root", "stalk-surface-above-ring",
    "stalk-surface-below-ring", "stalk-color-above-ring",
    "stalk-color-below-ring", "veil-type", "veil-color", "ring-number",
    "ring-type", "spore-print-color", "population", "habitat",
]


def load_uci_mushroom(path: str) -> TransactionDB:
    """Đọc UCI Mushroom (agaricus-lepiota.data, CSV 23 cột) thành CSDL giao dịch.

    Mỗi dòng → một giao dịch gồm 23 item dạng "thuộc_tính=giá_trị".
    Giá trị thiếu "?" (ở cột stalk-root) bị bỏ qua.
    """
    transactions = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            vals = line.strip().split(",")
            if len(vals) != len(MUSHROOM_ATTRS):
                continue
            transactions.append(
                f"{a}={v}" for a, v in zip(MUSHROOM_ATTRS, vals) if v != "?"
            )
    return TransactionDB(transactions)


def slide_example_db() -> TransactionDB:
    """Dataset 4 giao dịch dùng xuyên suốt slide bài giảng."""
    return TransactionDB([
        {"pasta", "lemon", "bread", "orange"},   # T1
        {"pasta", "lemon"},                       # T2
        {"pasta", "orange", "cake"},              # T3
        {"pasta", "lemon", "orange", "cake"},     # T4
    ])
