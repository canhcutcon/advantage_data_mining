# Báo cáo kiểm tra toàn vẹn — Stage 2.5 (INTEGRITY, pre-review)

> Ngày kiểm: 2026-06-11 · Đối tượng: `bao_cao_rare_pattern_mining.md` (sau Stage 2)
> Kết luận: **PASS** (sau 3 sửa lỗi được phát hiện và khắc phục trong phiên kiểm)

## Pha 1 — Xác minh tài liệu tham khảo (21 DOI + 1 nguồn không DOI)

- Phương pháp: gọi CrossRef API cho từng DOI, đối chiếu **title / năm / tác giả đầu**
  với mục tương ứng trong báo cáo.
- Kết quả: **21/21 DOI hợp lệ và đúng bài báo**. [1] (VLDB 1994) không có DOI
  (đặc thù kỷ yếu VLDB), đã ghi URL bản gốc chính thức.
- **2 lỗi metadata phát hiện và đã sửa:**
  | Ref | Lỗi | Đã sửa thành |
  |---|---|---|
  | [12] CLS-MMS | ghi "vol. 65, no. 12, 2022" | **The Computer Journal 66(2), 342–359, 2023 (online 2021)** |
  | [14] ERIM | ghi "vol. 39, no. 10, 2022" | **Expert Systems 41(6), e13122, 2024 (online 2022)** |
- Ghi chú chính sách: 8 nguồn > 5 năm đều gắn cờ `[SEMINAL — định nghĩa]` và chỉ được
  trích cho định nghĩa gốc; mọi nhận định hiện trạng đều dẫn nguồn 2021–2026. ✅
- Hạng Q/CORE: không có API công khai để xác minh tự động → đã thêm chú thích
  "mang tính tham khảo" vào phần Tài liệu tham khảo (xử lý minh bạch thay vì khẳng định chắc).

## Pha 2 — Đối chiếu trích dẫn trong ngữ cảnh (citation context)

Rà 22 vị trí trích dẫn trong thân bài: mỗi citation đỡ đúng nhận định nó được gắn
(vd. [20] chỉ dẫn cho MRI-CE/cross-entropy; [19], [22] chỉ dẫn cho privacy-preserving;
[5] chỉ dẫn cho mRI/AprioriRare). Không phát hiện trích dẫn lạc ngữ cảnh. ✅

## Pha 3 — Xác minh số liệu thống kê

- Script đối chiếu tự động: **mọi con số** trong Bảng 4.1, 4.2, 4.3 khớp 100% với
  `results/expA|expB|expC_*.csv` (sinh trực tiếp từ code). ✅
- Thống kê dữ liệu (8 124 giao dịch, 118 item, độ dài TB 22.69) khớp output. ✅
- Các khẳng định dẫn xuất: "tăng ~890 lần" (45 391/51 = 890.0), "~8 lần" (986/122 = 8.08),
  "0.44%" (36/8 124 = 0.443%) — đúng. ✅
- **1 lỗi phát hiện và đã sửa:** báo cáo viết "11 + 14 phép kiểm" trong khi code có
  **19 câu lệnh assert** — đã sửa lại mô tả cho chính xác.

## Pha 4 — Tính nguyên gốc

Toàn bộ văn bản viết mới bằng tiếng Việt; giả mã viết lại theo mô tả thuật toán gốc;
không sao chép nguyên văn từ slide hay bài báo. Ví dụ chạy tay lấy từ slide bài giảng
(được phép — tài liệu môn học) và có ghi nguồn. ✅

## Pha 5 — Kiểm chứng khẳng định (claims)

Khẳng định mạnh nhất của báo cáo — "slide tr.18 bỏ sót {pasta, orange, cake}" — được
kiểm chứng độc lập: sup({pasta, orange, cake}) = 2 ≥ minsup = 2 trên CSDL T1–T4
(thuộc T3, T4), và node `poc` trong hình lattice tr.2 của slide được vẽ là frequent.
Khẳng định đúng và được trình bày thận trọng ("thiếu sót nhỏ"). ✅

## Checklist 7 chế độ thất bại nghiên cứu AI (AI Research Failure Modes)

| # | Chế độ | Kết luận | Bằng chứng |
|---|--------|----------|------------|
| 1 | Citation hallucination | **CLEAR** | 21/21 DOI xác minh qua CrossRef API (Pha 1) |
| 2 | Implementation bugs | **CLEAR** | 19 assert đối chiếu với slide: 100% PASS; phát hiện và sửa 1 expected-value sai trong chính bộ test (slide thiếu itemset) |
| 3 | Hallucinated results | **CLEAR** | Script đối chiếu tự động báo cáo ↔ CSV: PASS toàn bộ (Pha 3) |
| 4 | Shortcut reliance | **CLEAR** | Không có mô hình học máy/đánh giá dự đoán; thuật toán tổ hợp tất định |
| 5 | Bug-as-insight | **CLEAR** | Phát hiện "slide bỏ sót itemset" được xác nhận bằng tính tay độc lập, không phải artifact của code |
| 6 | Methodology fabrication | **CLEAR** | Phương pháp mô tả trong báo cáo khớp đúng code thực tế (cùng repo, có hướng dẫn tái lập) |
| 7 | Pipeline frame-lock | **CLEAR** | Phạm vi bám đề bài (slide môn học); các quyết định mở rộng (Mushroom, dải ngưỡng) đều nêu lý do |

**Không có mode nào SUSPECTED → không kích hoạt block.**

## Kết luận Stage 2.5

**PASS.** Ba lỗi phát hiện trong phiên kiểm ([12], [14], số phép assert) đã được sửa
ngay; tài liệu sẵn sàng chuyển sang Stage 3 (REVIEW).
