# Biên bản review — Stage 3 (hội đồng mô phỏng 5 người)

> Đối tượng: `bao_cao_rare_pattern_mining.md` (bản sau Stage 2.5)
> Ngày review: 2026-06-11

## Reviewer 1 — Trưởng ban biên tập (EIC), góc nhìn tổng thể

Báo cáo có cấu trúc mạch lạc, bám sát khung bài giảng, phần thực nghiệm tự kiểm chứng
là điểm cộng hiếm thấy ở bài tập lớn. Hai vấn đề cần xử lý:

- **R1.1 (P1 — lỗi nội dung).** Bảng 2.2, hàng "Chứa mẫu sup = 0?", cột mRI ghi
  "Không¹". **Sai về mặt lý thuyết**: một mRI hoàn toàn có thể có support bằng 0 —
  ví dụ hai item đều phổ biến nhưng không bao giờ đồng xuất hiện thì cặp của chúng có
  sup = 0 và mọi tập con đều phổ biến, thoả Định nghĩa 2.5. Chú thích ¹ hiện tại cũng
  diễn đạt rối. Cần sửa thành "Có thể" kèm giải thích đúng.
- **R1.2 (P1 — thiếu thành phần).** Báo cáo thiếu phần **Tóm tắt** ở đầu — thành phần
  chuẩn của báo cáo học thuật, giúp người chấm nắm nhanh đóng góp.

## Reviewer 2 — Chuyên gia thực nghiệm

- **R2.1 (P2 — so sánh chưa công bằng).** Mục 4.3/4.4 viết AprioriInverse "nhanh hơn
  AprioriRare 2–3 bậc". Hai thuật toán giải **hai bài toán khác nhau** với bộ ngưỡng
  khác nhau (minsup cao vs cặp minsup/maxsup thấp); so sánh thời gian trực tiếp dễ gây
  hiểu lầm là cùng một bài toán. Cần thêm mệnh đề làm rõ đây là so sánh *chi phí đặc
  trưng của từng bài toán*, không phải benchmark cùng điều kiện.
- **R2.2 (P2 — minh bạch giới hạn).** Bảng 4.3 (Exp C) dùng giới hạn kích thước
  itemset ≤ 4; cột "kích thước max = 4" trong dữ liệu gốc vì vậy là **giá trị chạm
  trần**, không phải kích thước tự nhiên lớn nhất. Mục 4.4 có nhắc nhưng nên nói rõ
  ngay tại Exp C để người đọc không suy diễn sai.
- **R2.3 (P3 — gợi ý).** Nên ghi cấu hình máy chạy thực nghiệm (CPU, RAM) để con số
  thời gian có ngữ cảnh. Không bắt buộc với bài tập lớn.

## Reviewer 3 — Chuyên gia lý thuyết / related work

- **R3.1 (P3 — chính xác hoá).** Mục 2.2.2 viết "mọi itemset hiếm khác đều là tập cha
  của một mRI nào đó" — đúng, nhưng nên thêm điều kiện "mọi itemset hiếm *khác rỗng*"
  cho chặt (tập rỗng luôn phổ biến nên không ảnh hưởng, phát biểu hiện tại chấp nhận được).
- **R3.2 (P3).** Bảng 3.1: nên nhấn mạnh các công thức viết cho **cặp mục (a, b)**
  theo đúng [6], còn bond/all-confidence tổng quát hoá cho itemset bất kỳ — báo cáo có
  ghi ở chú thích bảng nhưng có thể người đọc bỏ qua. Hiện trạng chấp nhận được.
- **R3.3 (khen).** Việc chỉ ra coherence ≡ bond qua nguyên lý bao hàm–loại trừ là điểm
  tinh tế, thể hiện hiểu sâu.

## Reviewer 4 — Người hướng dẫn thực hành (reproducibility)

- **R4.1 (khen).** 19 assert đối chiếu với slide + script đối chiếu báo cáo↔CSV là
  thực hành tốt; Phụ lục A đủ để tái lập.
- **R4.2 (P3 — gợi ý).** `run_experiments.py` cố định ngưỡng trong code; nếu thêm
  argparse sẽ tiện khảo sát thêm. Không bắt buộc.

## Reviewer 5 — Devil's Advocate

- **D5.1.** "Phát hiện slide bỏ sót {pasta, orange, cake}" — đã kiểm tính tay độc lập
  (T3, T4 đều chứa), khẳng định đứng vững và trình bày đúng mực. Không phản đối.
- **D5.2 (P2 — câu chữ).** Mở đầu viết FIM "mặc định rằng phổ biến đồng nghĩa với đáng
  quan tâm" — hơi nặng tay; FIM chỉ là công cụ liệt kê theo ngưỡng, "giả định" nằm ở
  cách dùng. Đề nghị làm mềm câu này.
- **D5.3.** Kết quả Exp C "bão hòa 90–104" có thể là artifact của giới hạn max_size = 4
  và maxsup = 0.1 — yêu cầu báo cáo thừa nhận khả năng này (liên quan R2.2). 

## Quyết định biên tập (Editorial Decision)

**MINOR REVISION.** Không có lỗi phương pháp hay số liệu; 2 mục P1 (một lỗi nội dung
ở Bảng 2.2, một thiếu Tóm tắt), 3 mục P2 về diễn đạt/minh bạch, còn lại P3 tùy chọn.

## Lộ trình chỉnh sửa (Revision Roadmap)

| # | Nguồn | Ưu tiên | Việc cần làm | Trạng thái |
|---|-------|---------|--------------|------------|
| 1 | R1.1 | P1 | Sửa Bảng 2.2: mRI "Có thể chứa sup = 0", viết lại chú thích ¹ | bắt buộc |
| 2 | R1.2 | P1 | Thêm mục **Tóm tắt** đầu báo cáo | bắt buộc |
| 3 | R2.1 | P2 | Làm rõ so sánh thời gian AprioriInverse vs AprioriRare là khác bài toán | bắt buộc |
| 4 | R2.2 + D5.3 | P2 | Ghi rõ tại Exp C: max_size = 4 là trần; "bão hòa" có thể do trần + maxsup | bắt buộc |
| 5 | D5.2 | P2 | Làm mềm câu "FIM mặc định..." ở mở đầu | bắt buộc |
| 6 | R2.3 | P3 | Thêm cấu hình máy | tùy chọn — sẽ làm (1 dòng) |
| 7 | R3.1 | P3 | Thêm "khác rỗng" | tùy chọn — sẽ làm |
| 8 | R4.2 | P3 | argparse cho script | tùy chọn — KHÔNG làm (ngoài phạm vi, ghi nhận hạn chế) |
