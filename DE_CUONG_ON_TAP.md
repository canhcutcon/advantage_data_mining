# ĐỀ CƯƠNG ÔN TẬP — ADVANCED DATA MINING
### (Khai phá mẫu tuần tự & Khai phá tập mục phổ biến + mở rộng)

> Nguồn: các slide trong `advantage_data_mining/doc/`. Ký hiệu thống nhất theo slide:
> chuỗi `⟨…⟩`, itemset trong `()` hoặc `{}`, `sup(X)` = số chuỗi/giao dịch chứa X, `minsup` = ngưỡng hỗ trợ tối thiểu.

---

# CẤU TRÚC ÔN TẬP (theo yêu cầu)

| Chủ đề | Trọng tâm |
|---|---|
| **A. Mẫu tuần tự (Chuỗi)** | Lý thuyết + **ưu/nhược điểm** + **2 thuật toán** (GSP, PrefixSpan) + dạng bài "tìm TẤT CẢ sequential patterns" |
| **B. Tập mục phổ biến** | **Apriori + thuật toán cải tiến** (FP-Growth / Eclat) |
| **C. Các bài toán mở rộng** | Tập **đóng** (closed), tập **tối đại** (maximal), tập **hiếm** (rare), tập **hữu ích cao** (high utility) — *(Bỏ tập tương đồng / correlated)* |

---

# PHẦN A — KHAI PHÁ MẪU TUẦN TỰ (Sequential Pattern Mining)

## A.1. Khái niệm cốt lõi (PHẢI thuộc định nghĩa)

- **Sequence (chuỗi):** danh sách CÓ THỨ TỰ các phần tử (element/transaction): `s = ⟨e₁ e₂ e₃ …⟩`.
- **Element (phần tử):** một itemset `eᵢ = {i₁, i₂, …, iₖ}` (tập item xảy ra CÙNG lúc). Trong itemset thứ tự **không quan trọng** (ghi theo bảng chữ cái).
- **Item (event):** một ký hiệu/sản phẩm.
- **k-sequence:** chuỗi chứa tổng cộng **k item** (đếm cả lặp). VD `⟨a(abc)(ac)d(cf)⟩` là 9-sequence (5 phần tử, 9 item).
- **Thứ tự GIỮA các phần tử có ý nghĩa, trong cùng phần tử thì không:**
  `⟨a(abc)…⟩ = ⟨a(cba)…⟩` nhưng `⟨a(abc)…⟩ ≠ ⟨a(ac)(abc)…⟩`.
- **Subsequence α ⊑ β:** α=⟨a₁…aₙ⟩ là chuỗi con của β nếu tồn tại `j₁<j₂<…<jₙ` sao cho `a₁⊆b_{j1}, …, aₙ⊆b_{jn}`.
- **Support:** `sup(Sₐ) = |{ S | S ∈ D và Sₐ ⊑ S }|` (đếm theo SỐ CHUỖI, không đếm số lần lặp trong 1 chuỗi).
- **Sequential pattern:** chuỗi con S với `sup(S) ≥ minsup`. Input = CSDL chuỗi + minsup; Output = TẤT CẢ sequential patterns.
- **Tính chất Apriori:** nếu S không phổ biến thì mọi siêu-chuỗi (super-sequence) của S đều không phổ biến. VD `⟨hb⟩` hiếm ⟹ `⟨hab⟩`, `⟨(ah)b⟩` cũng hiếm.

> ⚠️ Phân biệt support cho ví dụ: `sup(⟨{a},{b}⟩)` (a TRƯỚC b, khác phần tử) **≠** `sup(⟨{a,b}⟩)` (a,b CÙNG phần tử).

## A.2. Hai thuật toán (TRỌNG TÂM — phải làm được bằng tay)

### (1) GSP — Generalized Sequential Pattern (Apriori-based, Srikant & Agrawal 1995)
Quy trình: **quét tạo L₁ → lặp { Sinh ứng viên → Cắt tỉa → Đếm support → Loại bỏ }**.

- **Sinh ứng viên độ dài 2:** từ items {x,y,…} tạo cả `⟨(xy)⟩` (cùng itemset, x<y) và `⟨(x)(y)⟩` (mọi cặp có thứ tự, kể cả x=y).
- **Sinh ứng viên độ dài k (k>2) — luật trộn:** trộn w₁ với w₂ nếu **(bỏ event ĐẦU của w₁) = (bỏ event CUỐI của w₂)**. Ứng viên = w₁ nối thêm event cuối của w₂:
  - nếu 2 event cuối của w₂ cùng itemset → gộp vào itemset cuối của w₁;
  - ngược lại → thêm thành itemset mới.
- **Cắt tỉa (Apriori):** loại ứng viên nếu có chuỗi con (k-1) không phổ biến.
- **Đếm support:** quét lại CSDL.

### (2) PrefixSpan — Prefix-Projected Pattern Growth (Pei et al. 2001/2004)
- **Ý tưởng:** chia không gian theo **tiền tố (prefix)**, với mỗi tiền tố α dựng **CSDL chiếu S|α** (lấy hậu tố/suffix sau lần xuất hiện ĐẦU TIÊN của α), rồi đệ quy.
- **Ký hiệu `_x`:** item x nằm CÙNG itemset với item cuối của tiền tố (mở rộng itemset → dạng `(…x)`).
- **Pseudocode:** `PrefixSpan(α, l, S|α)`:
  1. Quét S|α 1 lần, tìm item b tần suất ≥ minsup mà: (a) ghép vào itemset cuối của α, hoặc (b) nối ⟨b⟩ vào sau α.
  2. Mỗi b → tạo α' (xuất α'), 
  3. Dựng S|α' và gọi `PrefixSpan(α', l+1, S|α')`.

### (Tham khảo) SPADE — vertical format, dùng danh sách `⟨SID, EID⟩`, growth bằng phép giao (join) các id-list.

## A.3. ƯU / NHƯỢC ĐIỂM (câu hỏi lý thuyết hay ra)

| Thuật toán | Ưu điểm | Nhược điểm |
|---|---|---|
| **GSP** | Đơn giản, dễ hiểu, dễ cài; tận dụng tính chất Apriori cắt tỉa | Sinh **rất nhiều ứng viên** (nhất là độ dài 2); **quét CSDL nhiều lần** (mỗi vòng độ dài tăng 1); sinh cả ứng viên **không tồn tại** trong CSDL; kém hiệu quả với mẫu dài (BFS) |
| **PrefixSpan** | **Không sinh ứng viên thừa** — chỉ xét mẫu thực sự có trong CSDL; DFS, chuỗi co lại nhanh; ít vòng quét hơn | Chi phí **xây dựng CSDL chiếu** lớn (bộ nhớ/thời gian) nếu không dùng pseudo-projection; không phải nhanh nhất nhưng đơn giản & dễ mở rộng |
| **SPADE** | Định dạng dọc, dùng giao id-list nhanh; ít quét CSDL | Tốn bộ nhớ lưu id-list; vẫn sinh ứng viên (Apriori-style) |

**Bottleneck chung của GSP/SPADE:** số ứng viên độ dài 2 bùng nổ (vd 1000 item-1 ⟹ ~1.499.500 ứng viên-2); mẫu dài cần số ứng viên ngắn theo cấp số mũ.

## A.4. DẠNG BÀI: "Tìm TẤT CẢ sequential patterns thỏa minsup"
Trình tự làm tay (nên trình bày cả 2 thuật toán để đối chiếu):
1. Liệt kê CSDL, xác định minsup.
2. Tìm L₁ (đếm từng item theo SỐ CHUỖI), loại item < minsup.
3. **GSP:** sinh C₂ (cả dạng (xy) và (x)(y)) → đếm → L₂ → trộn C₃ → cắt tỉa → đếm → L₃ → … đến khi rỗng.
4. **PrefixSpan:** với mỗi tiền tố trong L₁, dựng CSDL chiếu, đếm item (`_x` và x), đệ quy.
5. Tổng hợp danh sách patterns + support; hai thuật toán phải **ra cùng kết quả**.

> Ví dụ mẫu đã giải (CSDL ⟨(ab)(c)(a)⟩, ⟨(ab)(b)(c)⟩, ⟨(b)(c)(d)⟩, ⟨(b)(ab)(c)⟩, minsup=3):
> 7 patterns ⟹ ⟨a⟩:3, ⟨b⟩:4, ⟨c⟩:4, ⟨(ab)⟩:3, ⟨(a)(c)⟩:3, ⟨(b)(c)⟩:4, ⟨(ab)(c)⟩:3.

---

# PHẦN B — KHAI PHÁ TẬP MỤC PHỔ BIẾN (Frequent Itemset Mining)

## B.1. Khái niệm
- **I** = tập tất cả item; **transaction** Tₐ ⊆ I (một itemset, KHÔNG thứ tự, mỗi item ≤ 1 lần); **CSDL giao dịch** D = {T₁,…,Tᵣ}.
- Có thể xem D như **ma trận nhị phân** (thuộc tính nhị phân **bất đối xứng**: 1 quan trọng hơn 0).
- **k-itemset:** itemset có k item. Với |I|=n có `2ⁿ − 1` itemset khác rỗng → **search space = lattice (Hasse diagram)**.
- **Support:** `sup(X) = |{ T | X ⊆ T ∧ T ∈ D }|` (đếm hoặc tỉ lệ %).
- **FIM:** tìm mọi X với `sup(X) ≥ minsup`. minsup cao → ít itemset, nhanh, ít bộ nhớ.
- **Cách ngây thơ (naïve):** đếm hết 2ⁿ−1 itemset → quá tốn → cần (1) đếm support hiệu quả, (2) thu hẹp không gian tìm kiếm.

## B.2. Thuật toán 1 — APRIORI (Agrawal & Srikant 1993/1994)
**Hai tính chất nền tảng:**
- **Apriori property (anti-monotonic):** nếu `X ⊂ Y` thì `sup(Y) ≤ sup(X)`.
- **Property 2:** nếu tồn tại `X ⊂ Y` mà X không phổ biến ⟹ Y không phổ biến (⟹ mọi superset của item hiếm đều hiếm → cắt nhánh).

**Quy trình:** L₁ → (sinh ứng viên Cₖ bằng nối Lₖ₋₁ + cắt tỉa các tập con (k-1) không phổ biến) → quét đếm → Lₖ → lặp.

**Ưu điểm:** nổi tiếng, đơn giản, truyền cảm hứng nhiều thuật toán, tính chất Apriori giảm mạnh không gian (vd 31 → 18 itemset).

**Nhược điểm (Problems of Apriori):**
- Sinh **nhiều ứng viên** (đặc biệt 2-itemset).
- **Quét CSDL nhiều lần** (mỗi vòng độ dài +1).
- Ứng viên có thể **không tồn tại** trong CSDL.

**Yếu tố ảnh hưởng độ phức tạp:** minsup; số item (dimensionality); kích thước CSDL; độ rộng trung bình giao dịch.

**Tối ưu hóa Apriori (advanced):**
1. Mã hoá item thành **số nguyên** (so sánh nhanh, ít bộ nhớ).
2. **Sắp xếp giao dịch theo độ dài tăng** → tính sup itemset size k chỉ dùng giao dịch độ dài ≥ k.
3. Gộp các giao dịch trùng nhau thành 1 (kèm **trọng số**).
4. **Sắp item theo thứ tự toàn phần + tìm kiếm nhị phân** để kiểm tra item ∈ giao dịch.
5. Lưu ứng viên trong **hash tree** để đếm support nhanh.
→ Giải pháp tổng quát giảm số lượng: **Concise representation** = mine **closed** & **maximal** patterns (xem Phần C).

## B.3. Thuật toán cải tiến (cái "??" trong đề) — Pattern-Growth / Vertical

> Các thuật toán FIM khác nêu trong slide: **Apriori, AprioriTID, Eclat, FPGrowth, Hmine, LCM**.
> Cặp đôi kinh điển với Apriori thường là **FP-Growth** (và **Eclat**). Học cả hai để chắc chắn.

### (a) FP-Growth (Han et al.) — Pattern-Growth, KHÔNG sinh ứng viên
- Quét CSDL **2 lần**: lần 1 đếm item & loại item hiếm, sắp theo support giảm dần; lần 2 nén CSDL vào **FP-tree** (cây tiền tố nén).
- Khai thác **đệ quy** bằng **conditional pattern base + conditional FP-tree** (chia để trị, không sinh-kiểm-tra ứng viên).
- **Ưu:** chỉ 2 lần quét, không sinh ứng viên, rất nhanh với CSDL dày (dense). **Nhược:** cây có thể lớn, cài đặt phức tạp; CSDL thưa/rời rạc thì FP-tree kém hiệu quả.

### (b) Eclat (Zaki) — định dạng DỌC (vertical)
- Mỗi item lưu **TID-set** (tập giao dịch chứa nó); `sup(XY) = |TIDset(X) ∩ TIDset(Y)|`.
- Khai thác theo DFS bằng **giao TID-set** (dClat dùng diffset để tiết kiệm).
- **Ưu:** đếm support bằng phép giao nhanh, ít quét CSDL. **Nhược:** TID-set có thể rất lớn (tốn bộ nhớ) với item phổ biến.

### So sánh nhanh
| | Quét CSDL | Sinh ứng viên | Mạnh khi |
|---|---|---|---|
| Apriori | nhiều lần | có (nhiều) | minsup cao, CSDL nhỏ |
| FP-Growth | 2 lần | không | CSDL dày, mẫu dài |
| Eclat | ít | có (giao TID) | CSDL thưa vừa phải |

---

# PHẦN C — CÁC BÀI TOÁN MỞ RỘNG

> **Vấn đề chung:** số frequent itemset thường **rất lớn** và **dư thừa** → cần biểu diễn cô đọng (concise representation): **closed** và **maximal**.

## C.1. Tập đóng (Closed Frequent Itemsets) — Pasquier 1999
- **Định nghĩa:** itemset X **đóng** nếu KHÔNG tồn tại Y mà `X ⊂ Y` và `sup(X) = sup(Y)`.
- **Closure c(X):** closed itemset NHỎ NHẤT chứa X; bằng **giao các giao dịch** chứa X. Các itemset cùng closure → cùng support, cùng xuất hiện trong cùng tập giao dịch (cùng *equivalence class*).
- **Khôi phục:** từ closed itemsets + support, lấy mọi tập con → ra mọi frequent itemset; `sup(X) = sup(c(X))`.
- **Tính cô đọng:** Chess minsup=0.4: 6.439.702 FI → 1.361.157 closed (không mất thông tin support).
- **Thuật toán:** naïve (post-processing — kém); hiệu quả: **Charm, AprioriClose/A-Close, LCMClosed, FPClose**.

## C.2. Tập tối đại (Maximal Frequent Itemsets)
- **Định nghĩa:** X **maximal** nếu X phổ biến và KHÔNG có siêu tập trực tiếp nào phổ biến (X là FI "lớn nhất").
- **Công dụng:** biết maximal ⟹ suy ra mọi FI (lấy tập con) — RẤT cô đọng. Chess minsup=0.4: 6.439.702 FI → chỉ **38.050 maximal** (nhỏ hơn ~168 lần).
- ⚠️ **Mất support:** maximal KHÔNG giữ support của các tập con (khác với closed).
- **Thuật toán:** naïve post-processing (kém); hiệu quả: **GenMax** (cải tiến Eclat), **FPMax** (cải tiến FP-Growth), **LCMMax**.
  - GenMax dùng **Combine-Set** + đệ quy backtrack (`MFI-backtrack`, `FI-combine`), cắt nhánh khi `I∪P` đã có superset trong MFI.

## C.3. Quan hệ phân cấp (PHẢI nhớ — hay hỏi)
```
Maximal FI  ⊆  Closed FI  ⊆  Frequent Itemsets
```
- Maximal: ít nhất, suy ra được **tập** FI nhưng **mất support**.
- Closed: nhiều hơn maximal, suy ra được FI **và** support đầy đủ (không mất mát).

## C.4. Tập hiếm (Rare Itemsets)
Lý do: nhiều mẫu thú vị lại HIẾM (gian lận, bệnh hiếm…), FIM bỏ sót.

- **Định nghĩa 1 — infrequent:** `sup(X) < minsup`. → Vấn đề: **quá nhiều**, gồm cả tập **support = 0** (không tồn tại) → vô dụng.
- **Định nghĩa 2 — Minimal Rare Itemset (MRI):** `sup(X) < minsup` NHƯNG **mọi tập con thực sự đều phổ biến** (`∀ Y ⊂ X: sup(Y) ≥ minsup`). → "đường biên" giữa frequent và rare, gọn.
  - **Thuật toán AprioriRare (2007):** giống Apriori sinh theo tầng, NHƯNG: khi gặp itemset size k **không phổ biến** mà mọi tập con phổ biến → đó là MRI; **không** dùng itemset không phổ biến để sinh tiếp.
  - VD (minsup=2): trong các cặp, `{lemon, cake}` sup=1 (<2) còn {lemon}, {cake} đều phổ biến ⟹ là MRI.
- **Định nghĩa 3 — Perfectly Rare Itemset (2 ngưỡng minsup < maxsup):** X là **frequent** nếu `sup ≥ maxsup`; X là **perfectly rare** nếu `minsup ≤ sup(X) < maxsup` VÀ mọi tập con không rỗng `Y ⊂ X` có `sup(Y) < maxsup`.
  - **Thuật toán AprioriInverse (2005):** ban đầu **loại bỏ item có sup ≥ maxsup**, rồi chạy như Apriori trên phần còn lại để tìm itemset có sup ≥ minsup → tìm "sporadic rules".

## C.5. Tập hữu ích cao (High Utility Itemset Mining — HUIM)
> ⚠️ *Slide HUIM trong thư mục bị trùng nội dung Rare — phần dưới theo lý thuyết chuẩn HUI-Miner, hãy ĐỐI CHIẾU lại slide gốc (gợi ý từ tên file: `minutil=30`, thứ tự item a,b,c,d,e).*

Động cơ: support coi mọi item như nhau (mua 1 hay 10, rẻ hay đắt đều như nhau). HUIM thêm **số lượng (quantity)** và **lợi nhuận/đơn giá (profit)**.

- **Internal utility** q(i,T): số lượng item i trong giao dịch T.
- **External utility** p(i): lợi nhuận/đơn vị của item i (bảng profit).
- **Utility của item trong T:** `u(i,T) = q(i,T) × p(i)`.
- **Utility của itemset X trong T:** `u(X,T) = Σ_{i∈X} u(i,T)`.
- **Utility của X:** `u(X) = Σ_{T⊇X} u(X,T)`.
- **High Utility Itemset:** `u(X) ≥ minutil`.
- **Khó khăn:** utility **KHÔNG anti-monotonic** (tập lớn hơn có thể utility cao hơn hoặc thấp hơn) → không cắt nhánh trực tiếp như Apriori.
- **Giải pháp — TWU (Transaction-Weighted Utilization):**
  - `TU(T) = Σ_{i∈T} u(i,T)` (utility cả giao dịch).
  - `TWU(X) = Σ_{T⊇X} TU(T)`.
  - **Tính chất TWU (anti-monotonic, overestimate):** `TWU(X) ≥ u(X)`; nếu `TWU(X) < minutil` thì X và mọi superset đều KHÔNG phải HUI → cắt nhánh.
- **Thuật toán:**
  - **Two-Phase (2005):** Pha 1 dùng TWU (kiểu Apriori) tìm ứng viên HTWUI; Pha 2 quét lại tính utility thật, giữ X có `u(X) ≥ minutil`.
  - **HUI-Miner (2012):** dùng cấu trúc **utility-list** (utility + remaining utility), không sinh ứng viên 2 pha; cắt nhánh bằng tổng `iutil + rutil`.
  - **FHM, EFIM…** cải tiến tốc độ.
- **Dạng bài (theo tên file):** cho bảng giao dịch + số lượng + bảng profit, `minutil=30`, thứ tự xử lý item a<b<c<d<e → tính `u`, `TU`, `TWU`, liệt kê HUI. *(Đối chiếu slide gốc để dùng đúng dữ liệu.)*

---

# PHẦN D — BẢNG HỆ THỐNG HOÁ & CÂU HỎI ÔN

## D.1. Bảng "bài toán → định nghĩa lõi → thuật toán"
| Bài toán | Điều kiện cốt lõi | Thuật toán tiêu biểu |
|---|---|---|
| Frequent itemset | `sup ≥ minsup` | Apriori, FP-Growth, Eclat |
| Closed FI | FI & không superset cùng support | Charm, AprioriClose, FPClose |
| Maximal FI | FI & không superset phổ biến | GenMax, FPMax, LCMMax |
| Minimal rare | `sup < minsup` & mọi tập con phổ biến | AprioriRare |
| Perfectly rare | `minsup ≤ sup < maxsup` & con < maxsup | AprioriInverse |
| High utility | `u(X) ≥ minutil` (cắt bằng TWU) | Two-Phase, HUI-Miner, FHM |
| Sequential pattern | `sup ≥ minsup` (có thứ tự) | GSP, PrefixSpan, SPADE |

## D.2. Câu hỏi lý thuyết hay gặp
1. Phát biểu & chứng minh tính chất Apriori (anti-monotonic). Vai trò trong cắt không gian tìm kiếm?
2. So sánh GSP vs PrefixSpan: cơ chế, ưu/nhược, vì sao PrefixSpan không sinh ứng viên thừa?
3. Phân biệt **closed** vs **maximal**: cái nào giữ được support? Vẽ quan hệ bao hàm.
4. Vì sao infrequent itemset "thô" vô dụng? Minimal rare khắc phục thế nào?
5. Vì sao utility KHÔNG anti-monotonic? TWU giúp cắt nhánh ra sao (overestimation)?
6. Các kỹ thuật tối ưu Apriori (5 cái) — giải thích mục đích từng cái.

## D.3. Dạng bài tập tính toán (luyện tay)
- **B1:** Cho CSDL chuỗi + minsup → tìm **tất cả** sequential patterns bằng **GSP** và **PrefixSpan** (đối chiếu).
- **B2:** Cho CSDL giao dịch + minsup → tìm **frequent / closed / maximal** itemsets; chỉ ra cái nào closed, cái nào maximal, tính closure.
- **B3:** Cùng CSDL → tìm **minimal rare** (AprioriRare) và **perfectly rare** (AprioriInverse, cho minsup & maxsup).
- **B4:** Cho bảng số lượng + profit, minutil=30 → tính `u(X)`, `TU`, `TWU`, liệt kê **High Utility Itemsets**.

---
*Ghi chú: FP-Growth/Eclat và HUIM được bổ sung theo kiến thức chuẩn vì slide trong thư mục chủ yếu trình bày Apriori (FIM) và file HUIM bị trùng nội dung Rare. Khi ôn, ưu tiên đối chiếu slide gốc của thầy/cô cho phần ví dụ số liệu.*
