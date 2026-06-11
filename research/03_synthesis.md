# Tổng hợp tài liệu (Research Synthesis) — Rare Pattern Mining

> **Stage 1 — RESEARCH.** Tổng hợp từ slide gốc (50 trang) + 22 nguồn đã xác minh
> trong `02_bibliography.md`. Ký hiệu [S#]/[R#] tham chiếu danh mục tài liệu.

## 1. Ba định nghĩa "mẫu hiếm" (trả lời RQ1)

Bài toán nền: cho CSDL giao dịch *D* và ngưỡng *minsup*, FIM liệt kê mọi itemset X có
sup(X) ≥ minsup [S1]. Mẫu hiếm là phần bù của không gian này, nhưng "phần bù thô" không
dùng được trực tiếp — ba định nghĩa tinh chế dần:

| Định nghĩa | Phát biểu | Vấn đề giải quyết | Hạn chế |
|---|---|---|---|
| **Infrequent itemset** | sup(X) < minsup | Đơn giản, trực tiếp | Bùng nổ tổ hợp; chứa cả itemset sup = 0 (không tồn tại trong dữ liệu) |
| **Minimal rare itemset (mRI)** [S5] | sup(X) < minsup **và** mọi tập con thực sự của X đều phổ biến | Biên dưới gọn của vùng hiếm (biên kề ngay trên vùng phổ biến trong lattice) | Vẫn cần duyệt qua toàn bộ vùng phổ biến để chạm tới biên |
| **Perfectly rare itemset** [S4] | minsup ≤ sup(X) < maxsup **và** mọi tập con khác rỗng Y ⊂ X có sup(Y) < maxsup | Loại nhiễu hai phía: vừa đủ hiếm (dưới maxsup) vừa không phải nhiễu ngẫu nhiên (trên minsup); mọi mục thành phần cũng hiếm | Bỏ sót mẫu hiếm chứa mục phổ biến (vd. {bệnh hiếm, triệu chứng phổ biến}) |

Nhận xét cấu trúc quan trọng (từ lattice trong slide): vùng phổ biến và vùng hiếm tách nhau
bởi một **biên (border)**; mRI chính là biên dưới của vùng hiếm. Taxonomy đầy đủ về các biến
thể định nghĩa được hệ thống hóa trong khảo sát [S8].

## 2. Thuật toán khai thác mẫu hiếm (trả lời RQ2)

### 2.1 AprioriRare (2007) [S5]
- Nền tảng Apriori [S1]: sinh ứng viên theo mức (level-wise), mức k từ mức k−1.
- **Hai khác biệt:** (1) gặp itemset k-phần tử *infrequent* → kiểm tra mọi tập con
  (k−1) có phổ biến không; nếu có → đó là **minimal rare itemset**; (2) **không** dùng
  itemset infrequent để sinh ứng viên lớn hơn (vẫn cắt tỉa như Apriori).
- Ví dụ trong slide (T1–T4, minsup = 2): mRI = {bread} (sup 1), {lemon, cake} (sup 1).
- Chi phí ~ Apriori: phải duyệt hết vùng phổ biến. Cải tiến gần đây: tìm mRI bằng
  cross-entropy (MRI-CE) tránh duyệt vét cạn [R12], khai thác bitwise theo chiều dọc [R10].

### 2.2 AprioriInverse (2005) [S4]
- Dùng cho perfectly rare itemsets với 2 ngưỡng (minsup, maxsup).
- **Khác biệt cốt lõi:** bước khởi tạo **loại bỏ mọi mục x có sup(x) ≥ maxsup**; sau đó
  chạy như Apriori trên các mục còn lại với ngưỡng dưới minsup. Nhờ mọi tập con của
  perfectly rare itemset cũng hiếm (tính chất đóng), việc loại mục phổ biến từ đầu
  không làm mất nghiệm.
- Hệ quả: không gian tìm kiếm nhỏ hơn hẳn AprioriRare, nhưng định nghĩa hẹp hơn.

### 2.3 CORI (2015) [S7] — mẫu hiếm **tương quan**
- Bài toán: tìm X sao cho **sup(X) < maxsup** (hiếm) **và bond(X) ≥ minbond** (các mục
  thực sự đi cùng nhau). Kết hợp một ràng buộc monotone và một anti-monotone.
- Nền tảng Eclat [S2]: mỗi itemset giữ **TID-list** (giao dịch chứa X) và
  **DTID-list** (giao dịch chứa ≥ 1 mục của X); khi nối X ∪ Y:
  TIDLIST(Z) = TIDLIST(X) ∩ TIDLIST(Y); DTIDLIST(Z) = DTIDLIST(X) ∪ DTIDLIST(Y);
  bond(Z) = |TIDLIST(Z)| / |DTIDLIST(Z)|.
- Cắt tỉa: bond anti-monotone (Property 2) → bond(Z) < minbond thì bỏ mọi superset của Z.
- Ví dụ slide (maxsup = 3, minbond = 0.6): {bread} (sup 1, bond 1), {cake} (sup 2, bond 1),
  {orange, cake} (sup 2, bond 0.66).
- Hướng nối tiếp: khai thác luật kết hợp hiếm-tương quan-mạch lạc CLS-MMS [R4].

## 3. Độ đo tương quan và tính null-invariance (trả lời RQ3)

Vấn đề "mẫu giả": itemset phổ biến có thể gồm các mục **tương quan yếu** — vd. {pasta, cake}
xuất hiện 50% giao dịch chỉ vì pasta có mặt ở *mọi* giao dịch. Ba hướng xử lý nêu trong slide:
(1) độ đo tương quan (bond, all-confidence) [S3]; (2) kiểm định thống kê; (3) chuyển sang
loại mẫu khác (luật kết hợp).

- **bond(X) = sup(X) / dsup(X)** ∈ [0,1]; bond của mục đơn = 1; anti-monotone [S3, S7].
- **allconf(X) = sup(X) / max{sup(i) | i ∈ X}** ∈ [0,1]; cũng anti-monotone; chỉ cần
  support các mục đơn nên dễ tích hợp vào Apriori/Eclat [S3].
- Khung thống nhất của Wu et al. [S6]: χ² và lift **không null-invariant** (bị méo bởi
  các giao dịch không chứa mục nào của X — null transactions); allconf, coherence
  (= bond), cosine, kulc, maxconf **null-invariant** — phù hợp dữ liệu thưa, lệch phân bố,
  đúng bối cảnh mẫu hiếm.

## 4. Hiện trạng nghiên cứu 2021–2026 (trả lời RQ5)

Bốn dòng chính nổi lên từ các nguồn ≥ 2021:

1. **Mở rộng biểu diễn dữ liệu:** fuzzy rare itemset mining trên dữ liệu định lượng
   (FRI-Miner) [R2]; dữ liệu tăng trưởng theo thời gian với cấu trúc cây vòng đời
   (incremental, time-sensitive) [R5]; cấu trúc cây FR-Tree cho dữ liệu lớn [R3];
   khai thác bitwise/vertical hiệu năng cao [R10].
2. **Mẫu hiếm + tiện ích/mục tiêu:** rare high-utility patterns có định hướng mục tiêu
   (targeted) [R7] — hợp lưu của rare mining và utility mining.
3. **Quyền riêng tư:** privacy-preserving rare itemset mining — che giấu mẫu hiếm nhạy cảm
   trong khi vẫn công bố dữ liệu [R11, R14] (Information Sciences 2024–2025, dòng rất mới).
4. **Ứng dụng:** chẩn đoán yếu tố bệnh tim bằng luật kết hợp hiếm [R13]; lỗi hiếm trong
   công nghiệp ô tô (ERIM) [R6]; phát hiện outlier trên data stream bằng minimum rare
   patterns [R8]; tổng quan ứng dụng và thách thức [R1, R9].

**Khoảng trống/cơ hội** (định vị cho phần kết luận của báo cáo): các thuật toán nền
(AprioriRare/AprioriInverse) vẫn là baseline trong các công bố mới [R10, R12]; tối ưu
metaheuristic (cross-entropy [R12]) và ràng buộc kép kiểu CORI là hướng hiện đại;
chưa có chuẩn benchmark thống nhất cho rare mining (các bài dùng dataset khác nhau).

## 5. Thiết kế thực nghiệm rút ra cho Chương 4 (trả lời RQ4)

1. **Kiểm chứng đúng đắn (sanity check):** chạy 3 thuật toán trên dataset slide
   (T1{pasta,lemon,bread,orange}, T2{pasta,lemon}, T3{pasta,orange,cake},
   T4{pasta,lemon,orange,cake}); đối chiếu từng con số với slide:
   - minsup=2 → mRI = {bread}, {lemon,cake}
   - (minsup=1, maxsup=2) → perfectly rare: {bread}; (maxsup=1.9, minsup=1) theo slide
   - maxsup=3, minbond=0.6 → rare correlated: {bread}, {cake}, {orange,cake}
   - bond({pasta,orange}) = 0.75; allconf({lemon,orange,cake}) = 1/3…
2. **Dataset chuẩn:** 1 dataset từ kho SPMF/UCI (vd. Mushroom — dày, hoặc retail — thưa);
   khảo sát: số mẫu tìm được & thời gian chạy theo minsup/maxsup/minbond.
3. **Trực quan:** biểu đồ số itemset theo ngưỡng; bảng so sánh 3 thuật toán.
