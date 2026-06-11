# Sanity check — đối chiếu cài đặt với slide bài giảng

Dataset: T1{pasta, lemon, bread, orange}, T2{pasta, lemon}, T3{pasta, orange, cake}, T4{pasta, lemon, orange, cake}

## 1. Frequent itemsets (minsup = 2) — khớp lattice slide tr.2

⚠️ Danh sách chữ ở slide tr.18 bỏ sót {pasta, orange, cake} (sup = 2, thuộc T3 và T4); hình lattice tr.2 vẽ đúng node `poc` là itemset phổ biến. Kết quả đúng: **11** itemset phổ biến.

| Itemset | Support |
|---|---|
| {cake} | 2 |
| {lemon} | 3 |
| {orange} | 3 |
| {pasta} | 4 |
| {cake, orange} | 2 |
| {cake, pasta} | 2 |
| {lemon, orange} | 2 |
| {lemon, pasta} | 3 |
| {orange, pasta} | 3 |
| {cake, orange, pasta} | 2 |
| {lemon, orange, pasta} | 2 |

## 2. AprioriRare — minimal rare itemsets (minsup = 2) — khớp slide tr.5–11

| mRI | Support |
|---|---|
| {bread} | 1 |
| {cake, lemon} | 1 |

## 3. AprioriInverse — perfectly rare itemsets (minsup = 1, maxsup = 1.9) — khớp slide tr.12

| PRI | Support |
|---|---|
| {bread} | 1 |

Biến thể (minsup = 1.1, maxsup = 3.1):

| PRI | Support |
|---|---|
| {cake} | 2 |
| {lemon} | 3 |
| {orange} | 3 |
| {cake, orange} | 2 |
| {lemon, orange} | 2 |

## 4. Độ đo bond — khớp slide tr.24–29 (kể cả Property 1: bond(item đơn) = 1)

| Itemset | bond |
|---|---|
| {pasta, orange} | 0.75 |
| {cake, bread} | 0 |
| {lemon, bread} | 0.3333 |
| {lemon, orange} | 0.5 |
| {pasta, lemon} | 0.75 |
| {pasta, lemon, orange} | 0.5 |

## 5. All-confidence — khớp slide tr.42–45

| Itemset | allconf |
|---|---|
| {pasta, orange} | 0.75 |
| {lemon, orange, cake} | 0.3333 |
| {pasta, lemon, orange} | 0.5 |

## 6. Correlated frequent itemsets (minsup = 2, minbond = 0.75) — khớp slide tr.31

| Itemset | sup | bond |
|---|---|---|
| {cake} | 2 | 1.00 |
| {lemon} | 3 | 1.00 |
| {orange} | 3 | 1.00 |
| {pasta} | 4 | 1.00 |
| {lemon, pasta} | 3 | 0.75 |
| {orange, pasta} | 3 | 0.75 |

## 7. CORI — rare correlated itemsets (maxsup = 3, minbond = 0.6) — khớp slide tr.33

| Itemset | sup | bond |
|---|---|---|
| {bread} | 1 | 1.00 |
| {cake} | 2 | 1.00 |
| {orange, cake} | 2 | 0.66 |

## 8. TID-List / DTID-List — khớp slide tr.36–39

| Itemset | TID-List | sup | DTID-List | dsup |
|---|---|---|---|---|
| {pasta} | T1 T2 T3 T4 | 4 | T1 T2 T3 T4 | 4 |
| {pasta, lemon} | T1 T2 T4 | 3 | T1 T2 T3 T4 | 4 |
| {bread, orange} | T1 | 1 | T1 T3 T4 | 3 |

## 9. Các độ đo khác cho cặp minh hoạ {pasta, cake} (khung Wu et al. 2010)

| Độ đo | Giá trị |
|---|---|
| sup | 2 |
| chi2 | 0 |
| lift | 1 |
| allconf | 0.5 |
| coherence(bond) | 0.5 |
| cosine | 0.7071 |
| kulc | 0.75 |
| maxconf | 1 |

→ lift({pasta, cake}) = 1.0: dù xuất hiện ở 50% giao dịch, cặp này KHÔNG tương quan (pasta có mặt ở mọi giao dịch) — đúng nhận xét 'spurious pattern' ở slide tr.21–22.

**KẾT LUẬN: 100% phép đối chiếu với slide ĐẠT (assert pass).**
