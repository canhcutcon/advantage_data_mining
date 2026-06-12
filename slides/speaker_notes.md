# Speaker Notes — Khai thác các mẫu hiếm (15 phút, 17 slides)

## Slide 1: Trang bìa
[Chờ giới thiệu] "Em xin chào thầy/cô và các bạn. Hôm nay em trình bày đề tài Khai thác các mẫu hiếm — Rare Pattern Mining."
[Thời lượng: 0:15]

## Slide 2: Nội dung trình bày
"Bài trình bày gồm 5 phần: bài toán và động cơ, ba định nghĩa mẫu hiếm, ba thuật toán, các độ đo tương quan, và cuối cùng là phần cài đặt — kiểm chứng — thực nghiệm."
→ Chuyển: "Bắt đầu từ câu hỏi vì sao cần mẫu hiếm."
[Thời lượng: 0:20]

## Slide 3: Động cơ
"Điều thú vị nhất trong dữ liệu có phải là điều xảy ra thường xuyên nhất không? Trong y tế, tổ hợp triệu chứng bệnh hiếm mới mang giá trị chẩn đoán; trong công nghiệp, lỗi hiếm mới là thứ cần phát hiện. FIM truyền thống bỏ qua hoàn toàn các mẫu này."
→ Chuyển: "Vậy sao không hạ thấp ngưỡng hỗ trợ?"
[Thời lượng: 1:00]

## Slide 4: Vấn đề
"Hạ minsup gây hai hệ quả: bùng nổ tổ hợp, và nhiễu — nhiều mẫu 'hiếm' có support bằng 0, tức không hề tồn tại trong dữ liệu. Cần cả ba mảnh ghép: định nghĩa chặt, thuật toán riêng, độ đo lọc mẫu giả."
→ Chuyển: "Để nói chuyện cụ thể, em dùng một ví dụ nhỏ."
[Thời lượng: 1:00]

## Slide 5: Ví dụ chạy xuyên suốt
"Bốn giao dịch theo bài giảng. Chú ý: pasta có mặt trong mọi giao dịch — chi tiết này sẽ quay lại ở phần mẫu giả. Với minsup = 2 có đúng 11 itemset phổ biến."
→ Chuyển: "Trên ví dụ này, 'hiếm' nghĩa là gì?"
[Thời lượng: 0:45]

## Slide 6: Ba định nghĩa (có \pause — bấm 3 lần)
"Infrequent là phần bù thô của FIM — bùng nổ và chứa cả sup = 0. mRI là các điểm hiếm 'đầu tiên' ngay khi vượt qua biên vùng phổ biến — nhỏ gọn mà đại diện được mọi mẫu hiếm. PRI thêm ngưỡng dưới để loại nhiễu và đòi mọi item thành phần cũng hiếm."
→ Chuyển: "Mỗi định nghĩa có một thuật toán tương ứng."
[Thời lượng: 1:15]

## Slide 7: AprioriRare
"Duyệt theo mức như Apriori. Điểm tinh tế: ứng viên đã qua bước prune nghĩa là mọi tập con đều phổ biến — nên hễ nó không phổ biến là tự động thành mRI. Nhược điểm: phải đi xuyên toàn bộ vùng phổ biến — em sẽ định lượng ở thực nghiệm A."
→ Chuyển: "Thuật toán thứ hai đi theo hướng ngược lại."
[Thời lượng: 1:15]

## Slide 8: AprioriInverse
"Loại mọi item phổ biến ngay từ đầu — đúng đắn vì mọi item hiếm thì mọi tập con cũng hiếm. Không gian nhỏ hơn hẳn, nhưng cái giá là bỏ sót mẫu lai, ví dụ {bệnh hiếm + triệu chứng phổ biến}."
→ Chuyển: "Hiếm thôi chưa đủ — mẫu tìm được có đáng tin không?"
[Thời lượng: 1:00]

## Slide 9: Mẫu giả
"{pasta, cake} xuất hiện ở một nửa giao dịch, nhưng pasta có mặt khắp nơi nên đi cùng bất cứ thứ gì — support cao không nói lên mối liên hệ nào. Đây là mẫu giả."
→ Chuyển: "Bài giảng giới thiệu hai độ đo chính."
[Thời lượng: 0:45]

## Slide 10: bond & all-confidence
"bond chia support hội cho support tuyển — tỉ lệ giao dịch liên quan thực sự chứa toàn bộ mẫu. All-confidence là confidence nhỏ nhất của mọi luật sinh từ mẫu. Cả hai đều anti-monotone — CORI sẽ dùng tính chất này để cắt tỉa."
→ Chuyển: "Vì sao không dùng lift hay chi bình phương quen thuộc?"
[Thời lượng: 1:00]

## Slide 11: Null-invariance
"Mẫu hiếm theo định nghĩa chỉ chạm một phần rất nhỏ dữ liệu — phần còn lại toàn null transactions. Lift và chi bình phương nhạy với chúng nên bị bóp méo trên dữ liệu thưa. Vì vậy bắt buộc dùng độ đo null-invariant."
→ Chuyển: "Hai dòng kỹ thuật — hiếm và tương quan — hội tụ ở CORI."
[Thời lượng: 0:45]

## Slide 12: CORI
"CORI tìm itemset vừa hiếm vừa gắn kết. Hai ràng buộc đối ngẫu nhau: hiếm là monotone, bond là anti-monotone. Mỗi itemset giữ hai danh sách TID — khi nối, lấy giao và hợp, support và bond tính ngay không cần quét lại CSDL. Chú ý: nút chưa hiếm vẫn phải mở rộng vì tập cha có thể hiếm."
→ Chuyển: "Toàn bộ lý thuyết trên được em cài đặt lại và kiểm chứng tự động."
[Thời lượng: 1:15]

## Slide 13: Cài đặt & kiểm chứng
"Cài đặt thuần Python, chỉ thư viện chuẩn. 19 câu lệnh assert đối chiếu từng con số bài giảng — đạt 100%. Thú vị nhất: quá trình này bắt được lỗi của chính slide gốc — danh sách FIM thiếu một itemset mà hình lattice lại vẽ đúng."
→ Chuyển: "Trên dữ liệu thật thì các đánh đổi lý thuyết hiện ra thế nào?"
[Thời lượng: 1:00]

## Slide 14: Exp A
"Trên Mushroom 8 124 giao dịch: khi minsup giảm từ 0.6 xuống 0.2, số itemset phổ biến phải duyệt tăng 890 lần, trong khi số mRI chỉ tăng 8 lần. mRI gọn — nhưng chi phí bị chi phối bởi vùng phổ biến, đúng như dự báo."
[Thời lượng: 1:00]

## Slide 15: Exp B & C
"AprioriInverse chạy ở mức mili-giây — nhưng nhấn mạnh đây là bài toán khác, không phải benchmark cùng điều kiện. Mẫu đắt giá nhất của CORI: 36 cây nấm mùi mốc luôn đồng thời không vòng cuống và cuống màu quế — bond bằng 1 tuyệt đối. Đây là loại tri thức FIM không bao giờ chạm tới."
→ Chuyển: "Ba thực nghiệm chốt lại ba đánh đổi."
[Thời lượng: 1:15]

## Slide 16: Kết luận
"Không có định nghĩa hiếm 'đúng' duy nhất — chỉ có đánh đổi: mRI gọn nhưng đắt, PRI rẻ nhưng hẹp, CORI cân bằng. Và trên dữ liệu thưa, null-invariance là bắt buộc. Hướng nổi bật 2021–2026 là privacy: chính vì hiếm, mẫu hiếm dễ định danh cá nhân."
[Thời lượng: 0:50]

## Slide 17: Cảm ơn & Hỏi đáp
"Em xin tóm tắt: ba định nghĩa, ba thuật toán, kiểm chứng tự động 100%, thực nghiệm Mushroom. Em xin cảm ơn và mời thầy/cô đặt câu hỏi."
[Thời lượng: 0:20]
