# BÀI TẬP CÓ LỜI GIẢI CHI TIẾT — ADVANCED DATA MINING
### (Phụ lục minh hoạ cho `DE_CUONG_ON_TAP.md`)

> Ký hiệu: chuỗi `⟨…⟩`, itemset `()`/`{}`, `sup(X)` đếm theo số chuỗi/giao dịch, `_x` = item cùng itemset với item cuối của tiền tố (PrefixSpan).

---

# BÀI 1 — MẪU TUẦN TỰ: tìm TẤT CẢ sequential patterns (GSP & PrefixSpan)

## Đề
| SID | Chuỗi |
|---|---|
| 1 | S₁ = ⟨(a b)(c)(a)⟩ |
| 2 | S₂ = ⟨(a b)(b)(c)⟩ |
| 3 | S₃ = ⟨(b)(c)(d)⟩ |
| 4 | S₄ = ⟨(b)(a b)(c)⟩ |

**minsup = 3.**

## Lời giải bằng GSP

**Bước 1 — L₁ (đếm theo số chuỗi chứa item):**

| item | chuỗi chứa | sup | |
|---|---|---|---|
| a | S₁,S₂,S₄ | 3 | ✓ |
| b | S₁,S₂,S₃,S₄ | 4 | ✓ |
| c | S₁,S₂,S₃,S₄ | 4 | ✓ |
| d | S₃ | 1 | ✗ loại |

→ **L₁ = {⟨a⟩:3, ⟨b⟩:4, ⟨c⟩:4}**

**Bước 2 — C₂ → L₂.** Ứng viên gồm `(xy)` (cùng itemset) và `(x)(y)` (khác itemset):

| Ứng viên | chuỗi thỏa | sup | | Ứng viên | sup | |
|---|---|---|---|---|---|---|
| ⟨(ab)⟩ | S₁,S₂,S₄ | **3** | ✓ | ⟨(b)(a)⟩ | 2 | ✗ |
| ⟨(ac)⟩ | – | 0 | ✗ | ⟨(b)(b)⟩ | 2 | ✗ |
| ⟨(bc)⟩ | – | 0 | ✗ | ⟨(b)(c)⟩ | **4** | ✓ |
| ⟨(a)(a)⟩ | S₁ | 1 | ✗ | ⟨(c)(a)⟩ | 1 | ✗ |
| ⟨(a)(b)⟩ | S₂ | 1 | ✗ | ⟨(c)(b)⟩ | 0 | ✗ |
| ⟨(a)(c)⟩ | S₁,S₂,S₄ | **3** | ✓ | ⟨(c)(c)⟩ | 0 | ✗ |

→ **L₂ = {⟨(ab)⟩:3, ⟨(a)(c)⟩:3, ⟨(b)(c)⟩:4}**

**Bước 3 — C₃ (luật trộn: bỏ-đầu(w₁) = bỏ-cuối(w₂)):**

| w | bỏ event đầu | bỏ event cuối |
|---|---|---|
| ⟨(ab)⟩ | ⟨(b)⟩ | ⟨(a)⟩ |
| ⟨(a)(c)⟩ | ⟨(c)⟩ | ⟨(a)⟩ |
| ⟨(b)(c)⟩ | ⟨(c)⟩ | ⟨(b)⟩ |

Khớp: bỏ-đầu⟨(ab)⟩=⟨(b)⟩ = bỏ-cuối⟨(b)(c)⟩ ⟹ nối `c` (khác itemset) ⟹ **⟨(ab)(c)⟩**.

Cắt tỉa: con độ-dài-2 {⟨(ab)⟩, ⟨(a)(c)⟩, ⟨(b)(c)⟩} đều ∈ L₂ ✓.
Đếm: (ab)→c có ở S₁,S₂,S₄ ⟹ **sup=3** ✓ → **L₃ = {⟨(ab)(c)⟩:3}**. Không sinh được C₄ → **dừng**.

## Lời giải bằng PrefixSpan (đối chiếu)

**Tiền tố ⟨a⟩** → CSDL chiếu: `⟨(_b)(c)(a)⟩, ⟨(_b)(b)(c)⟩, ⟨(_b)(c)⟩`
- `_b`:3 → **⟨(ab)⟩:3**; `c`:3 → **⟨(a)(c)⟩:3**; `b`(riêng):1✗; `a`:1✗.
  - ⟨(ab)⟩ → chiếu `⟨(c)(a)⟩,⟨(b)(c)⟩,⟨(c)⟩` → `c`:3 → **⟨(ab)(c)⟩:3** → chiếu `⟨(a)⟩,⟨⟩,⟨⟩` → dừng.
  - ⟨(a)(c)⟩ → chiếu `⟨(a)⟩,⟨⟩,⟨⟩` → dừng.

**Tiền tố ⟨b⟩** → CSDL chiếu: `⟨(c)(a)⟩,⟨(b)(c)⟩,⟨(c)(d)⟩,⟨(ab)(c)⟩`
- `c`:4 → **⟨(b)(c)⟩:4**; a:2✗; b:2✗; d:1✗. → ⟨(b)(c)⟩ chiếu `⟨(a)⟩,⟨⟩,⟨(d)⟩,⟨⟩` → dừng.

**Tiền tố ⟨c⟩** → chiếu `⟨(a)⟩,⟨⟩,⟨(d)⟩,⟨⟩` → a:1,d:1 → dừng.

## ✅ Kết quả (cả hai thuật toán ra GIỐNG NHAU — 7 patterns)
⟨a⟩:3, ⟨b⟩:4, ⟨c⟩:4, ⟨(ab)⟩:3, ⟨(a)(c)⟩:3, ⟨(b)(c)⟩:4, ⟨(ab)(c)⟩:3.

---

# BÀI 2 — TẬP PHỔ BIẾN / ĐÓNG / TỐI ĐẠI (Apriori + closed + maximal)

## Đề (CSDL trong slide)
| TID | Items |
|---|---|
| T1 | {pasta, lemon, bread, orange} |
| T2 | {pasta, lemon} |
| T3 | {pasta, orange, cake} |
| T4 | {pasta, lemon, orange, cake} |

**minsup = 2.** (viết tắt p=pasta, l=lemon, b=bread, o=orange, c=cake)

## (a) Frequent itemsets bằng Apriori

**L₁** (đếm support):

| item | sup | |
|---|---|---|
| p | 4 | ✓ |
| l | 3 | ✓ |
| o | 3 | ✓ |
| c | 2 | ✓ |
| b | 1 | ✗ loại |

**C₂ → L₂** (chỉ ghép {p,l,o,c}):

| cặp | giao dịch | sup | |
|---|---|---|---|
| {p,l} | T1,T2,T4 | 3 | ✓ |
| {p,o} | T1,T3,T4 | 3 | ✓ |
| {p,c} | T3,T4 | 2 | ✓ |
| {l,o} | T1,T4 | 2 | ✓ |
| {l,c} | T4 | 1 | ✗ |
| {o,c} | T3,T4 | 2 | ✓ |

→ L₂ = {pl:3, po:3, pc:2, lo:2, oc:2}

**C₃ → L₃** (cắt tỉa nếu có tập con ∉ L₂):
- {p,l,o}: con {pl,po,lo} đều ∈L₂ → giữ; giao dịch T1,T4 → **sup=2** ✓
- {p,l,c}: con {l,c}∉L₂ → **cắt tỉa**
- {p,o,c}: con {po,pc,oc}∈L₂ → giữ; T3,T4 → **sup=2** ✓
- {l,o,c}: con {l,c}∉L₂ → **cắt tỉa**

→ L₃ = {plo:2, poc:2}

**C₄:** {p,l,o,c} có con {l,o,c} (chứa {l,c} hiếm) → cắt tỉa → **L₄ = ∅. Dừng.**

→ **11 frequent itemsets**: p:4, l:3, o:3, c:2, pl:3, po:3, pc:2, lo:2, oc:2, plo:2, poc:2.

## (b) Closed itemsets (X đóng nếu không có superset cùng support)

| Itemset | sup | Có superset cùng sup? | Closed? |
|---|---|---|---|
| {p} | 4 | pl=3,po=3,pc=2 (đều <4) | ✓ **closed** |
| {l} | 3 | {p,l}=3 (=) | ✗ |
| {o} | 3 | {p,o}=3 (=) | ✗ |
| {c} | 2 | {p,c}=2 (=) | ✗ |
| {p,l} | 3 | {p,l,o}=2 (<3) | ✓ **closed** |
| {p,o} | 3 | plo=2, poc=2 (<3) | ✓ **closed** |
| {p,c} | 2 | {p,o,c}=2 (=) | ✗ |
| {l,o} | 2 | {p,l,o}=2 (=) | ✗ |
| {o,c} | 2 | {p,o,c}=2 (=) | ✗ |
| {p,l,o} | 2 | không superset phổ biến | ✓ **closed** |
| {p,o,c} | 2 | không superset phổ biến | ✓ **closed** |

→ **5 closed itemsets**: {p}:4, {p,l}:3, {p,o}:3, {p,l,o}:2, {p,o,c}:2.

*Minh hoạ closure:* `c({cake}) = giao(T3,T4) = {pasta,orange,cake}` ⟹ sup({cake}) = sup({p,o,c}) = 2.

## (c) Maximal itemsets (không có superset phổ biến)
Chỉ {p,l,o}:2 và {p,o,c}:2 (mọi tập 4 đã bị loại) → **2 maximal itemsets**.

## Quan hệ kiểm chứng
`Maximal {plo, poc} (2) ⊆ Closed (5) ⊆ Frequent (11)`. Closed giữ đủ support; Maximal chỉ giúp suy ra **tập** FI (mất support).

---

# BÀI 3 — TẬP HIẾM (Minimal Rare & Perfectly Rare)

## Dùng lại CSDL Bài 2.

## (a) Minimal Rare Itemset — AprioriRare (minsup = 2)
**Định nghĩa:** sup(X) < 2 NHƯNG mọi tập con thực sự đều phổ biến.

- Xét size-1: chỉ {bread}:1 < 2. Tập con thực sự = ∅ (luôn phổ biến) ⟹ **{bread} là MRI**.
- Xét size-2 không phổ biến mà mọi con phổ biến:
  - {lemon, cake}: sup=1<2; con {lemon}:3 ✓, {cake}:2 ✓ → **{lemon, cake} là MRI**.
  - Các cặp chứa bread (vd {p,b}…) có con {bread} hiếm → **không** phải minimal.

→ **Minimal rare = { {bread}:1 , {lemon,cake}:1 }**

## (b) Perfectly Rare Itemset — AprioriInverse (minsup = 1, maxsup = 3)
**Định nghĩa:** X perfectly rare nếu `1 ≤ sup(X) < 3` và mọi tập con không rỗng `Y⊂X` có `sup(Y) < 3`.
**AprioriInverse:** loại trước các item có `sup ≥ maxsup = 3`.

- Loại p(4), l(3), o(3) (vì ≥3). Còn lại: cake:2, bread:1 (đều <3).
- Sinh itemset từ {cake, bread} có sup ≥ minsup=1:
  - {cake}: sup=2 ∈[1,3) ✓ → **perfectly rare**
  - {bread}: sup=1 ∈[1,3) ✓ → **perfectly rare**
  - {bread,cake}: không giao dịch nào chứa cả hai (bread∈T1; cake∈T3,T4) → sup=0 <1 → loại.

→ **Perfectly rare = { {cake}:2 , {bread}:1 }**

---

# BÀI 4 — TẬP HỮU ÍCH CAO (High Utility Itemset Mining)

> ⚠️ Slide HUIM gốc bị thiếu (file trùng nội dung Rare). Dưới đây dùng **bộ dữ liệu minh hoạ tự xây**;
> chọn **minutil = 40** để liệt kê gọn (phương pháp y hệt cho mọi minutil, kể cả 30).

## Đề
**Bảng lợi nhuận (external utility / đơn vị):** a=5, b=2, c=4, d=3, e=1

**CSDL giao dịch (item : số lượng):**
| TID | Nội dung |
|---|---|
| T1 | a:1, c:1, d:1 |
| T2 | a:2, c:6, e:2 |
| T3 | a:1, b:2, c:1, d:6, e:1 |
| T4 | b:4, c:3, d:3, e:1 |
| T5 | b:2, c:2, e:1 |

**minutil = 40.** Thứ tự xử lý item: a < b < c < d < e.

## Bước 1 — Utility từng item trong mỗi giao dịch & Transaction Utility (TU)
`u(i,T) = q(i,T) × p(i)`; `TU(T) = Σ u(i,T)`.

| TID | u(a) | u(b) | u(c) | u(d) | u(e) | **TU** |
|---|---|---|---|---|---|---|
| T1 | 5 | – | 4 | 3 | – | **12** |
| T2 | 10 | – | 24 | – | 2 | **36** |
| T3 | 5 | 4 | 4 | 18 | 1 | **32** |
| T4 | – | 8 | 12 | 9 | 1 | **30** |
| T5 | – | 4 | 8 | – | 1 | **13** |

*(VD: T2: a=2×5=10, c=6×4=24, e=2×1=2 → TU=36.)*

## Bước 2 — Utility & TWU của từng item (1-itemset)
`u(i) = Σ_{T⊇i} u(i,T)`; `TWU(i) = Σ_{T⊇i} TU(T)`.

| item | u(i) | TWU(i) | u ≥ 40? | TWU ≥ 40? (giữ để mở rộng) |
|---|---|---|---|---|
| a | 5+10+5 = **20** | 12+36+32 = 80 | ✗ | ✓ |
| b | 4+8+4 = **16** | 32+30+13 = 75 | ✗ | ✓ |
| c | 4+24+4+12+8 = **52** | 123 | ✓ **HUI** | ✓ |
| d | 3+18+9 = **30** | 12+32+30 = 74 | ✗ | ✓ |
| e | 2+1+1+1 = **5** | 36+32+30+13 = 111 | ✗ | ✓ |

→ Mọi item đều có **TWU ≥ minutil** ⟹ không cắt được item nào ở bước này (đều "có triển vọng"). HUI size-1: **{c}=52**.

> **Vì sao cần TWU:** utility KHÔNG anti-monotonic (vd u(e)=5 nhưng u(ce)=53 lớn hơn) → không thể cắt nhánh trực tiếp. TWU thoả `TWU(X) ≥ u(X)` và anti-monotonic ⟹ nếu `TWU(X) < minutil` thì X và mọi superset chắc chắn không phải HUI.

## Bước 3 — Utility các 2-itemset
`u(X,T)=Σ_{i∈X} u(i,T)`, chỉ xét giao dịch chứa ĐỦ X.

| Cặp | Tính | u | HUI? |
|---|---|---|---|
| a,c | T1(5+4)+T2(10+24)+T3(5+4)=9+34+9 | **52** | ✓ |
| c,d | T1(4+3)+T3(4+18)+T4(12+9)=7+22+21 | **50** | ✓ |
| c,e | T2(24+2)+T3(4+1)+T4(12+1)+T5(8+1)=26+5+13+9 | **53** | ✓ |
| b,c | T3(4+4)+T4(8+12)+T5(4+8)=8+20+12 | **40** | ✓ |
| a,d | T1(5+3)+T3(5+18)=8+23 | 31 | ✗ |
| b,d | T3(4+18)+T4(8+9)=22+17 | 39 | ✗ |
| d,e | T3(18+1)+T4(9+1)=19+10 | 29 | ✗ |
| a,e | T2(10+2)+T3(5+1)=12+6 | 18 | ✗ |
| b,e | T3(4+1)+T4(8+1)+T5(4+1)=5+9+5 | 19 | ✗ |
| a,b | T3(5+4) | 9 | ✗ |

→ HUI size-2: **{a,c}=52, {c,d}=50, {c,e}=53, {b,c}=40**.

## Bước 4 — Utility các 3-itemset (chỉ xét tổ hợp có triển vọng)

| Bộ ba | Tính | u | HUI? |
|---|---|---|---|
| a,c,e | T2(10+24+2)+T3(5+4+1)=36+10 | **46** | ✓ |
| b,c,d | T3(4+4+18)+T4(8+12+9)=26+29 | **55** | ✓ |
| b,c,e | T3(4+4+1)+T4(8+12+1)+T5(4+8+1)=9+21+13 | **43** | ✓ |
| c,d,e | T3(4+18+1)+T4(12+9+1)=23+22 | **45** | ✓ |
| a,c,d | T1(5+4+3)+T3(5+4+18)=12+27 | 39 | ✗ |
| a,b,c | T3(5+4+4) | 13 | ✗ |
| b,d,e | T3(4+18+1)+T4(8+9+1)=23+18 | 41 | (✓)* |

\* {b,d,e}=41 ≥40 → cũng là HUI. (Lưu ý kiểm đủ các bộ ba!)

→ HUI size-3: **{a,c,e}=46, {b,c,d}=55, {b,c,e}=43, {c,d,e}=45, {b,d,e}=41**.

## Bước 5 — 4-itemset & 5-itemset

| Bộ | Tính | u | HUI? |
|---|---|---|---|
| b,c,d,e | T3(4+4+18+1)+T4(8+12+9+1)=27+30 | **57** | ✓ |
| a,c,d,e | T3(5+4+18+1)=28 | 28 | ✗ |
| a,b,c,d | T3(5+4+4+18)=31 | 31 | ✗ |
| a,b,c,e | T3(5+4+4+1)=14 | 14 | ✗ |
| a,b,c,d,e | T3(5+4+4+18+1)=32 | 32 | ✗ |

→ HUI size-4: **{b,c,d,e}=57**.

## ✅ Kết quả: tất cả High Utility Itemsets (minutil = 40)
| Size | HUIs (utility) |
|---|---|
| 1 | {c}=52 |
| 2 | {a,c}=52, {b,c}=40, {c,d}=50, {c,e}=53 |
| 3 | {a,c,e}=46, {b,c,d}=55, {b,c,e}=43, {b,d,e}=41, {c,d,e}=45 |
| 4 | {b,c,d,e}=57 |

**Tổng: 11 high-utility itemsets.**

---

# GHI NHỚ NHANH KHI ĐI THI
- **Sequential:** đếm support theo **số chuỗi**; GSP sinh cả `(xy)` & `(x)(y)`; PrefixSpan dùng `_x`.
- **Apriori:** cắt tỉa bằng "mọi tập con phải phổ biến".
- **Closed:** không superset **cùng support** (giữ support). **Maximal:** không superset **phổ biến** (mất support). `Maximal ⊆ Closed ⊆ Frequent`.
- **Minimal rare:** hiếm nhưng mọi con phổ biến. **Perfectly rare:** 2 ngưỡng, loại trước item ≥ maxsup.
- **HUIM:** `u = Σ q×p`; utility **không** anti-monotonic → cắt nhánh bằng **TWU** (`TWU ≥ u`, anti-monotonic).
