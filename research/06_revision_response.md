# Phản hồi chỉnh sửa (Response to Reviewers) — Stage 4 + biên bản re-review Stage 3'

> Ngày: 2026-06-11 · Bản chỉnh sửa: `bao_cao_rare_pattern_mining.md`

## Bảng đối chiếu từng ý kiến (R&R Traceability)

| # | Ý kiến | Ưu tiên | Xử lý | Vị trí trong báo cáo |
|---|--------|---------|-------|----------------------|
| 1 | R1.1 — Bảng 2.2 sai: mRI "Không chứa sup = 0" | P1 | **ĐÃ SỬA**: đổi thành "Có thể¹", viết lại chú thích ¹ với phản ví dụ đúng (hai item phổ biến không bao giờ đồng xuất hiện); cột PRI bổ sung lý do "vì sup ≥ minsup" | Bảng 2.2 |
| 2 | R1.2 — Thiếu Tóm tắt | P1 | **ĐÃ THÊM**: mục Tóm tắt + từ khóa ở đầu báo cáo | Trước Chương 1 |
| 3 | R2.1 — So sánh thời gian 2 thuật toán dễ hiểu lầm | P2 | **ĐÃ SỬA**: thêm mệnh đề "không phải benchmark cùng điều kiện… chi phí đặc trưng của từng bài toán" | Mục 4.3 Exp B |
| 4 | R2.2 + D5.3 — max_size = 4 là trần; "bão hòa" có thể là artifact | P2 | **ĐÃ SỬA**: chú thích Bảng 4.3 ghi rõ trần kích thước; nhận xét thêm câu "dưới hai ràng buộc khảo sát… nới ràng buộc có thể làm số mẫu tăng trở lại" | Bảng 4.3 + nhận xét Exp C |
| 5 | D5.2 — "FIM mặc định…" nặng tay | P2 | **ĐÃ SỬA**: đổi thành "khi dùng FIM người ta thường ngầm coi…" — chuyển "giả định" từ công cụ sang cách dùng | Mục 1.1 |
| 6 | R2.3 — Cấu hình máy | P3 | **ĐÃ THÊM**: "Apple M3, RAM 16 GB, macOS 15.5" | Mục 4.1 |
| 7 | R3.1 — "khác rỗng" | P3 | **ĐÃ THÊM** | Mục 2.2.2 |
| 8 | R4.2 — argparse cho script | P3 | **KHÔNG LÀM** (ngoài phạm vi bài tập; ngưỡng đã ghi rõ trong code và báo cáo; hướng dẫn tái lập ở Phụ lục A đủ dùng) | — |

8/8 ý kiến được giải trình; 7 thực hiện, 1 từ chối có lý do.

## Biên bản re-review — Stage 3' (verification review)

Kiểm tra từng mục roadmap trên bản chỉnh sửa:

- ✅ Mục 1: Bảng 2.2 nay đúng lý thuyết; phản ví dụ trong chú thích chính xác
  (cặp item phổ biến disjoint → sup = 0, mọi tập con phổ biến → là mRI).
- ✅ Mục 2: Tóm tắt ~180 từ, đủ 4 thành phần (bối cảnh — phương pháp — kết quả — kết
  luận), có từ khóa; các con số trong Tóm tắt (19 assert, 8 124, 45 391, 986, 0.2)
  khớp thân bài.
- ✅ Mục 3, 4, 5, 6, 7: đã vào đúng vị trí, văn phong nhất quán với phần còn lại.
- ✅ Mục 8: từ chối có lý do hợp lệ, ghi nhận trong bảng đối chiếu.
- Kiểm tra hồi quy (regression): các chỉnh sửa không đụng tới bảng số liệu 4.1–4.3 và
  danh mục tài liệu; không phát sinh nhận định mới cần trích dẫn.

**Kết luận Stage 3': ACCEPT** — đủ điều kiện chuyển Stage 4.5 (FINAL INTEGRITY).
Không còn vấn đề tồn đọng (residual issues: none).
