# RQ Brief — Khai thác các mẫu hiếm (Rare Pattern Mining)

> **Stage 1 — RESEARCH (academic-pipeline) · Bài tập lớn môn Khai thác dữ liệu nâng cao**
> Nguồn gốc đề tài: slide bài giảng `AdvancedDataMining_02_RareItemset Techniques.pdf` (50 trang).
> Ngày lập: 2026-06-11

## 1. Bối cảnh và động cơ nghiên cứu

Khai thác tập mục phổ biến (Frequent Itemset Mining — FIM) chỉ tìm các mẫu có support ≥ *minsup*,
do đó **bỏ sót các mẫu hiếm** — những mẫu xuất hiện ít nhưng mang giá trị cao trong thực tế
(chẩn đoán bệnh hiếm, phát hiện gian lận, phát hiện bất thường mạng, lỗi sản phẩm hiếm gặp).
Ngược lại, nếu hạ *minsup* xuống quá thấp, số lượng itemset bùng nổ tổ hợp và nhiều mẫu
"hiếm" thực chất là nhiễu (support = 0 hoặc các mục chỉ tình cờ đi cùng nhau).

Bài toán đặt ra: **định nghĩa thế nào là "mẫu hiếm có ý nghĩa"** và **thiết kế thuật toán
khai thác hiệu quả** khi tính chất anti-monotone của support không còn trợ giúp việc cắt tỉa
theo hướng tìm mẫu hiếm.

## 2. Câu hỏi nghiên cứu (Research Questions)

| # | Câu hỏi | Phạm vi trả lời |
|---|---------|-----------------|
| **RQ1** | Các định nghĩa hình thức của "mẫu hiếm" khác nhau như thế nào (infrequent / minimal rare / perfectly rare itemset) và hệ quả của từng định nghĩa lên không gian tìm kiếm? | Cơ sở lý thuyết (Chương 2) |
| **RQ2** | Các thuật toán kinh điển AprioriRare, AprioriInverse và CORI hoạt động ra sao; khác biệt cốt lõi so với Apriori/Eclat gốc là gì? | Thuật toán (Chương 3) |
| **RQ3** | Các độ đo tương quan (bond, all-confidence, χ², lift, cosine, kulc, maxconf) lọc mẫu giả (spurious patterns) như thế nào, và tính null-invariance ảnh hưởng gì đến việc chọn độ đo? | Độ đo (Chương 3) |
| **RQ4** | Kết quả cài đặt thực nghiệm AprioriRare, AprioriInverse, CORI trên dữ liệu ví dụ và dữ liệu chuẩn có khớp lý thuyết không; hành vi của các thuật toán thay đổi thế nào theo ngưỡng (minsup/maxsup/minbond)? | Thực nghiệm (Chương 4) |
| **RQ5** | Hướng nghiên cứu 5 năm gần đây (2021–2026) của rare pattern mining là gì (fuzzy, privacy-preserving, high-utility, incremental, ứng dụng y tế/công nghiệp)? | Tổng quan & hướng phát triển (Chương 2, 5) |

## 3. Phạm vi (Scope)

**Trong phạm vi:**
- Itemset hiếm trên CSDL giao dịch (transactional database) — đúng phạm vi slide gốc.
- 3 định nghĩa: infrequent, minimal rare, perfectly rare itemsets.
- 2 thuật toán khai thác mẫu hiếm: AprioriRare (2007), AprioriInverse (2005).
- Mẫu tương quan: bond, all-confidence; thuật toán CORI (2015); bảng độ đo của Wu et al. (2010).
- Cài đặt Python + thực nghiệm trên dataset ví dụ trong slide (4 giao dịch) và 1 dataset chuẩn.

**Ngoài phạm vi (chỉ điểm qua ở related work):** rare sequential patterns, rare high-utility
patterns (chỉ giới thiệu), khai thác trên data stream, dữ liệu không chắc chắn (uncertain data).

## 4. Phương pháp (Methodology)

1. **Tổng quan tài liệu có xác minh:** mọi citation xác minh qua CrossRef/OpenAlex API
   (DOI + năm + venue). Nguồn so sánh/tổng quan **≥ 2021**; nguồn cũ hơn chỉ dùng cho
   định nghĩa gốc và gắn cờ `[SEMINAL — định nghĩa]` (theo Chính sách trích dẫn workspace).
2. **Phân tích thuật toán:** trình bày giả mã, ví dụ chạy tay từng bước trên dataset
   T1–T4 của slide (pasta, lemon, bread, orange, cake), phân tích độ phức tạp và
   tính chất cắt tỉa (anti-monotonicity).
3. **Thực nghiệm:** cài đặt AprioriRare, AprioriInverse, CORI và các độ đo bằng Python
   (chuẩn thư viện: chỉ stdlib + pandas/matplotlib cho trình bày). Kiểm chứng output
   khớp 100% kết quả tính tay trong slide; sau đó chạy trên dataset chuẩn
   (vd. Mushroom/retail từ SPMF hoặc UCI) và khảo sát độ nhạy theo ngưỡng.
4. **Tổng hợp:** so sánh ưu/nhược các tiếp cận, liên hệ hướng nghiên cứu 2021–2026.

## 5. Sản phẩm dự kiến (Deliverables)

| Sản phẩm | File |
|----------|------|
| RQ Brief (file này) | `research/01_rq_brief.md` |
| Danh mục tài liệu đã xác minh | `research/02_bibliography.md` |
| Tổng hợp tài liệu (synthesis) | `research/03_synthesis.md` |
| Mã nguồn thực nghiệm | `code/rare_mining.py`, `code/run_experiments.py` |
| Kết quả thực nghiệm | `results/` (bảng + hình) |
| Báo cáo bài tập lớn (tiếng Việt) | `bao_cao_rare_pattern_mining.md` → `.docx` + `.pdf` |
