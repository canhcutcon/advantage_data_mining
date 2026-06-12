# Kịch bản thuyết trình: Khai thác các mẫu hiếm (Rare Pattern Mining)

**Hình thức**: thuyết trình bài tập lớn, 15 phút, 17 slides
**Nguồn**: `bao_cao_rare_pattern_mining.md`

---

## Slide 1: Trang bìa [0:00 – 0:15]

*[Chờ thầy/cô mời lên]*

"Em xin chào thầy/cô và các bạn. Em là [Họ tên], MSSV [.....]. Hôm nay em xin trình bày đề tài **Khai thác các mẫu hiếm — Rare Pattern Mining**, bài tập lớn môn Khai thác dữ liệu nâng cao."

---

## Slide 2: Nội dung trình bày [0:15 – 0:35]

"Bài trình bày của em gồm năm phần: thứ nhất là bài toán và động cơ; thứ hai, ba định nghĩa hình thức của mẫu hiếm; thứ ba, ba thuật toán AprioriRare, AprioriInverse và CORI; thứ tư, các độ đo tương quan và tính null-invariance; và cuối cùng là phần em tự cài đặt, kiểm chứng tự động và thực nghiệm trên dữ liệu thật."

→ *Chuyển*: "Em xin bắt đầu từ câu hỏi: vì sao cần quan tâm mẫu hiếm?"

---

## Slide 3: Động cơ [0:35 – 1:35]

"Thưa thầy/cô, điều thú vị nhất trong dữ liệu **có phải là điều xảy ra thường xuyên nhất** không? Khai thác tập mục phổ biến — FIM — ngầm trả lời 'có': nó chỉ giữ lại những gì vượt ngưỡng hỗ trợ.

Nhưng trong nhiều ứng dụng, câu trả lời là 'không'. Trong y tế, tổ hợp triệu chứng của bệnh hiếm xuất hiện rất ít nhưng mang giá trị chẩn đoán cao. Trong công nghiệp, lỗi sản phẩm hiếm gặp mới chính là thứ cần phát hiện. Trong an ninh mạng, hành vi bất thường — theo định nghĩa — là hành vi hiếm.

Tất cả các mẫu này bị FIM truyền thống **bỏ qua hoàn toàn**."

→ *Chuyển*: "Phản xạ đầu tiên là: vậy hạ thấp ngưỡng hỗ trợ xuống là xong?"

---

## Slide 4: Vấn đề [1:35 – 2:35]

"Đáng tiếc là không. Hạ thấp minsup gây ra hai hệ quả. Một là **bùng nổ tổ hợp**: số itemset thoả ngưỡng tăng theo cấp mũ. Hai là **nhiễu**: rất nhiều 'mẫu hiếm' thu được có support bằng 0 — tức là chúng không hề xuất hiện trong dữ liệu, ví dụ tổ hợp hai mặt hàng chưa ai từng mua cùng nhau.

Vì vậy lĩnh vực rare pattern mining cần cả ba mảnh ghép: định nghĩa chặt chẽ hơn về 'hiếm có ý nghĩa', thuật toán khai thác riêng, và độ đo tương quan để lọc mẫu giả. Đó cũng là cấu trúc phần còn lại của bài."

→ *Chuyển*: "Để nói chuyện cụ thể, em dùng một ví dụ nhỏ xuyên suốt."

---

## Slide 5: Ví dụ [2:35 – 3:20]

"Đây là cơ sở dữ liệu 4 giao dịch theo bài giảng. Em xin lưu ý một chi tiết: **pasta có mặt trong cả bốn giao dịch** — chi tiết này sẽ quay lại ở phần mẫu giả.

Với minsup bằng 2, có đúng **11 itemset phổ biến**. Còn {bread} chỉ xuất hiện một lần, và {bread, cake} không xuất hiện lần nào — support bằng 0. Mọi thuật toán phía sau đều được em chạy tay trên ví dụ này và dùng nó để kiểm chứng cài đặt."

→ *Chuyển*: "Trên ví dụ này, 'hiếm' chính xác nghĩa là gì? Có ba câu trả lời."

---

## Slide 6: Ba định nghĩa mẫu hiếm [3:20 – 4:35]

*[Bấm từng `\pause`]*

"Định nghĩa thứ nhất, **infrequent**: mọi itemset có support dưới ngưỡng. Đơn giản nhưng vô dụng — kết quả bùng nổ và chứa cả các mẫu support bằng 0.

*[bấm]* Định nghĩa thứ hai, **minimal rare itemset — mRI**: itemset hiếm mà mọi tập con thực sự đều phổ biến. Hình dung dàn itemset chia làm hai vùng bởi một đường biên — mRI chính là **biên dưới của vùng hiếm**, các điểm hiếm 'đầu tiên' ngay khi vượt qua vùng phổ biến. Nhỏ gọn, nhưng mọi mẫu hiếm đều là tập cha của một mRI nào đó.

*[bấm]* Định nghĩa thứ ba, **perfectly rare itemset — PRI**: dùng hai ngưỡng — support nằm giữa minsup và maxsup, và **mọi item thành phần cũng phải hiếm**. Ngưỡng dưới loại nhiễu quá hiếm, điều kiện thứ hai cho mẫu hiếm 'thuần khiết'.

*[bấm]* Trên ví dụ: mRI gồm {bread} và {lemon, cake}; PRI chỉ có {bread}."

→ *Chuyển*: "Mỗi định nghĩa có một thuật toán tương ứng."

---

## Slide 7: AprioriRare [4:35 – 5:50]

"AprioriRare tìm toàn bộ mRI, duyệt theo mức đúng như Apriori. Điểm khác biệt nằm ở cách xử lý ứng viên không phổ biến.

Điểm tinh tế nhất: một ứng viên đã **sống sót qua bước prune** nghĩa là mọi tập con kích thước k trừ 1 của nó đều phổ biến — và theo tính anti-monotone, mọi tập con nhỏ hơn cũng phổ biến. Vì vậy hễ ứng viên đó không phổ biến thì nó **tự động là một mRI**, không cần kiểm tra gì thêm.

Chạy trên ví dụ cho đúng {bread} và {lemon, cake} — khớp bài giảng.

Nhược điểm cố hữu: muốn chạm tới biên hiếm, thuật toán phải **đi xuyên toàn bộ vùng phổ biến**. Em sẽ định lượng cái giá này ở thực nghiệm A."

→ *Chuyển*: "Thuật toán thứ hai chọn hướng ngược lại."

---

## Slide 8: AprioriInverse [5:50 – 6:50]

"AprioriInverse tìm PRI, và khác biệt nằm ngay bước khởi tạo: **loại bỏ mọi item phổ biến trước khi bắt đầu**.

Vì sao đúng đắn? Vì support của itemset không vượt quá support của item nhỏ nhất trong nó — nếu mọi item đều hiếm thì mọi tập con cũng hiếm, điều kiện của PRI tự được thoả. Không gian tìm kiếm nhờ đó nhỏ hơn hẳn.

Cái giá phải trả: các **mẫu lai** — ví dụ tổ hợp {bệnh hiếm, triệu chứng phổ biến} — nằm ngoài tầm với, vì item phổ biến đã bị vứt từ đầu.

Chạy trên ví dụ với hai ngưỡng 1.1 và 3.1 cho đúng 5 PRI như bài giảng."

→ *Chuyển*: "Đến đây ta đã tìm được mẫu hiếm. Nhưng hiếm thôi chưa đủ — mẫu đó có đáng tin không?"

---

## Slide 9: Mẫu giả [6:50 – 7:35]

"Quay lại chi tiết em đã gửi gắm ở slide ví dụ: {pasta, cake} xuất hiện ở 50% giao dịch — nghe có vẻ là mẫu tốt. Nhưng pasta có mặt trong **mọi** giao dịch, nên nó đi cùng bất cứ thứ gì — sự đồng xuất hiện này là tất yếu, **không nói lên mối liên hệ nào** giữa pasta và cake. Đây gọi là mẫu giả — spurious pattern.

Ta cần độ đo tương quan để lọc chúng."

→ *Chuyển*: "Bài giảng giới thiệu hai độ đo chính."

---

## Slide 10: bond và all-confidence [7:35 – 8:35]

"**Bond** chia support hội cho support tuyển — tức trong số các giao dịch *có liên quan* tới mẫu, bao nhiêu phần chứa *toàn bộ* mẫu. Bond bằng 1 nghĩa là các mục luôn đi cùng nhau; bằng 0 nghĩa là không bao giờ.

**All-confidence** chia support cho support của item phổ biến nhất — và nó chính là **confidence nhỏ nhất** của mọi luật kết hợp sinh từ mẫu.

Cả hai có chung hai tính chất: bằng 1 với itemset đơn, và **anti-monotone** — thêm mục vào thì chỉ giảm. Tính chất thứ hai cho phép cắt tỉa kiểu Apriori, và CORI sẽ khai thác triệt để.

Trên ví dụ: bond của {cake, bread} bằng 0; của {pasta, orange} bằng 3/4."

→ *Chuyển*: "Một câu hỏi tự nhiên: sao không dùng lift hay chi bình phương quen thuộc?"

---

## Slide 11: Null-invariance [8:35 – 9:20]

"Câu trả lời nằm ở khái niệm **null transaction** — giao dịch không chứa mục nào của mẫu đang xét. Lift và chi bình phương **nhạy cảm** với chúng: trên dữ liệu thưa, hàng triệu giao dịch không liên quan có thể thổi phồng hoặc bóp méo giá trị độ đo.

Mẫu hiếm — theo đúng định nghĩa — chỉ chạm một phần rất nhỏ dữ liệu; phần còn lại toàn null transactions. Vì vậy với mẫu hiếm, dùng độ đo **null-invariant** như bond, all-confidence, cosine hay Kulczynski là **bắt buộc**, không phải tuỳ chọn."

→ *Chuyển*: "Hai dòng kỹ thuật — hiếm và tương quan — hội tụ ở thuật toán cuối cùng: CORI."

---

## Slide 12: CORI [9:20 – 10:35]

"CORI tìm các itemset **vừa hiếm vừa thực sự gắn kết**: support dưới maxsup *và* bond từ minbond trở lên.

Điều đẹp ở đây là hai ràng buộc có bản chất **đối ngẫu**: ràng buộc hiếm là monotone — đã hiếm thì mọi tập cha đều hiếm; ràng buộc bond là anti-monotone — đã rớt ngưỡng thì mọi tập cha đều rớt. CORI khai thác đồng thời cả hai trong một lần duyệt kiểu Eclat.

Mỗi itemset giữ hai cấu trúc: TID-List cho support hội và DTID-List cho support tuyển. Khi nối hai itemset, TID-List lấy **giao**, DTID-List lấy **hợp** — support và bond của itemset mới tính ngay, không cần quét lại cơ sở dữ liệu.

Một chi tiết thiết kế đáng chú ý: nút có support còn cao — chưa hiếm — **vẫn phải mở rộng tiếp**, vì tập cha của nó có thể hiếm. Đây là điểm khác hẳn cắt tỉa support truyền thống.

Chạy trên ví dụ cho đúng ba kết quả {bread}, {cake}, {orange, cake} — khớp bài giảng."

→ *Chuyển*: "Toàn bộ lý thuyết trên được em cài đặt lại từ đầu và kiểm chứng tự động."

---

## Slide 13: Cài đặt & kiểm chứng [10:35 – 11:35]

"Em cài đặt cả ba thuật toán bằng Python thuần, **chỉ dùng thư viện chuẩn**, trên cùng một biểu diễn TID-set — support của ứng viên tính bằng giao hai TID-set của cha thay vì quét lại dữ liệu.

Về kiểm chứng: em viết **19 câu lệnh assert** đối chiếu **từng con số** kỳ vọng đã tính tay trên ví dụ minh họa — phủ toàn bộ FIM, AprioriRare, AprioriInverse, CORI, bond, all-confidence. Kết quả: **100% đạt**.

Và bảng độ đo cặp xác nhận bằng số trực giác mẫu giả: {pasta, cake} có lift đúng bằng 1.0 và bond 0.5 — không tương quan."

→ *Chuyển*: "Trên dữ liệu thật, các đánh đổi lý thuyết hiện ra thế nào?"

---

## Slide 14: Exp A [11:35 – 12:35]

*[Hình runtime — chỉ vào biểu đồ]*

"Em thực nghiệm trên bộ UCI Mushroom: 8 124 giao dịch, 118 item, dữ liệu dày.

Kết quả thực nghiệm A: khi minsup giảm từ 0.6 xuống 0.2, số itemset phổ biến mà AprioriRare phải duyệt tăng khoảng **890 lần** — từ 51 lên hơn 45 nghìn — trong khi số mRI chỉ tăng khoảng **8 lần**, từ 122 lên 986.

Kết luận: tập mRI quả thực là biểu diễn biên rất gọn, nhưng **chi phí tính nó bị chi phối bởi kích thước vùng phổ biến** — đúng như dự báo lý thuyết ở slide AprioriRare, và đó là lý do các nghiên cứu gần đây tìm cách né duyệt vét cạn bằng metaheuristic hoặc biểu diễn bit dọc."

---

## Slide 15: Exp B & C [12:35 – 13:50]

*[Hình experiments]*

"Thực nghiệm B: AprioriInverse chạy ở mức **mili-giây** — nhanh hơn hai đến ba bậc. Nhưng em xin nhấn mạnh: đây **không phải benchmark cùng điều kiện** — hai thuật toán giải hai bài toán khác nhau; PRI vốn rẻ vì bước loại item phổ biến đã vứt bỏ phần lớn alphabet ngay từ đầu.

Thực nghiệm C với CORI: số mẫu hiếm tương quan gần như **bão hòa** quanh 90 đến 104 dù nới minbond từ 0.95 xuống 0.5 — trên dữ liệu này các nhóm thuộc tính hoặc gắn kết rất chặt hoặc rời hẳn.

Và đây là mẫu em thích nhất: 36 cây nấm mùi mốc — chỉ 0.44% dữ liệu — **luôn luôn** đồng thời không có vòng cuống và có cuống màu quế, bond đúng bằng 1. Đây chính xác là loại tri thức mà FIM với ngưỡng thông thường **không bao giờ chạm tới**."

→ *Chuyển*: "Ba thực nghiệm chốt lại ba đánh đổi."

---

## Slide 16: Kết luận [13:50 – 14:40]

"Kết luận của em gồm ba đánh đổi: **mRI gọn nhưng đắt** — phải duyệt toàn vùng phổ biến; **PRI rẻ nhưng hẹp** — bỏ sót mẫu lai; **CORI cân bằng** — ràng buộc kép cho kết quả nhỏ và giàu ngữ nghĩa.

Thông điệp em muốn gửi: không có định nghĩa hiếm 'đúng' duy nhất — chỉ có đánh đổi phù hợp với từng bài toán; và trên dữ liệu thưa, null-invariance là bắt buộc.

Về hướng phát triển 2021–2026: metaheuristic cho dữ liệu lớn, mở rộng fuzzy và utility, và đặc biệt thời sự là **privacy** — chính vì hiếm, mẫu hiếm dễ định danh cá nhân hơn mẫu phổ biến."

---

## Slide 17: Cảm ơn & Hỏi đáp [14:40 – 15:00]

"Tóm lại, em đã trình bày ba định nghĩa, ba thuật toán, cài đặt kiểm chứng tự động 100% và thực nghiệm trên UCI Mushroom. Em xin cảm ơn thầy/cô và các bạn đã lắng nghe — em sẵn sàng nhận câu hỏi ạ."

---

## Bảng thời gian

| Slide | Chủ đề | Thời lượng | Cộng dồn |
|:-----:|--------|:----------:|:--------:|
| 1 | Trang bìa | 0:15 | 0:15 |
| 2 | Nội dung | 0:20 | 0:35 |
| 3 | Động cơ | 1:00 | 1:35 |
| 4 | Vấn đề | 1:00 | 2:35 |
| 5 | Ví dụ | 0:45 | 3:20 |
| 6 | Ba định nghĩa | 1:15 | 4:35 |
| 7 | AprioriRare | 1:15 | 5:50 |
| 8 | AprioriInverse | 1:00 | 6:50 |
| 9 | Mẫu giả | 0:45 | 7:35 |
| 10 | bond / allconf | 1:00 | 8:35 |
| 11 | Null-invariance | 0:45 | 9:20 |
| 12 | CORI | 1:15 | 10:35 |
| 13 | Cài đặt & kiểm chứng | 1:00 | 11:35 |
| 14 | Exp A | 1:00 | 12:35 |
| 15 | Exp B & C | 1:15 | 13:50 |
| 16 | Kết luận | 0:50 | 14:40 |
| 17 | Cảm ơn | 0:20 | 15:00 |

**Tổng**: 15:00 (mục tiêu: 15 phút)

---

## Q&A dự kiến

### Q1: AprioriRare và AprioriInverse — khi nào dùng cái nào?
**A**: "Tuỳ định nghĩa hiếm mình cần. Nếu cần *mọi* mẫu hiếm kể cả mẫu lai chứa item phổ biến — ví dụ {bệnh hiếm, triệu chứng phổ biến} — thì phải dùng AprioriRare và chấp nhận chi phí duyệt vùng phổ biến. Nếu chỉ cần mẫu hiếm 'thuần khiết' mà mọi thành phần đều hiếm, AprioriInverse nhanh hơn hai đến ba bậc trên Mushroom."

### Q2: Vì sao không so sánh trực tiếp thời gian chạy hai thuật toán?
**A**: "Vì chúng giải hai bài toán khác nhau với bộ ngưỡng khác nhau — không phải benchmark cùng điều kiện. Con số phản ánh *chi phí đặc trưng của từng bài toán*: tìm PRI vốn rẻ vì alphabet bị thu hẹp từ đầu, còn tìm mRI buộc phải duyệt vùng phổ biến."

### Q3: Vì sao CORI giới hạn kích thước itemset ≤ 4?
**A**: "Để kiểm soát không gian duyệt trên dữ liệu dày như Mushroom — giao dịch trung bình 22.69 item. Đây là ràng buộc khảo sát, không phải của thuật toán; 'kích thước max = 4' trong kết quả là giá trị chạm trần. Nới trần này số mẫu có thể tăng trở lại — em đã ghi rõ trong báo cáo."

### Q4: Hiện tượng bão hòa ở Exp C nói lên điều gì?
**A**: "Trong phạm vi khảo sát — maxsup 0.1, kích thước ≤ 4 — các nhóm thuộc tính của Mushroom hoặc gắn kết rất chặt với bond gần 1, hoặc rời rạc hẳn, ít trường hợp lưng chừng. Nó cũng cho thấy cắt tỉa theo bond rất hiệu quả: thời gian chỉ tăng nhẹ khi nới ngưỡng."

### Q5: Một mRI có thể có support bằng 0 không?
**A**: "Có — ví dụ hai item đều phổ biến nhưng không bao giờ đồng xuất hiện: cặp của chúng có support 0 mà mọi tập con đều phổ biến, thoả định nghĩa mRI. Khác với định nghĩa infrequent thô, tập mRI chỉ chứa số rất nhỏ các mẫu như vậy — đúng các điểm trên biên. PRI thì không bao giờ, vì có ngưỡng dưới minsup."

### Q6: Vì sao lift của {pasta, cake} đúng bằng 1?
**A**: "Vì pasta xuất hiện trong 100% giao dịch nên P(pasta, cake) = P(cake), do đó lift = P(cake)/(P(pasta)·P(cake)) = 1/P(pasta) = 1 — độc lập thống kê hoàn hảo. Đây là minh họa đẹp cho mẫu giả: support 50% nhưng không có liên hệ nào."

### Q7: Cài đặt có tối ưu không? Có thể nhanh hơn?
**A**: "Cài đặt thuần Python chưa tối ưu hằng số — chưa dùng bitset hay song song hóa. Các con số thời gian nên đọc theo nghĩa so sánh tương đối giữa các thuật toán. Hướng tăng tốc có cơ sở từ văn liệu: biểu diễn bit dọc của Capillar 2023, hoặc thay vét cạn bằng cross-entropy như MRI-CE 2024."

### Q8: Hướng phát triển nào em thấy tiềm năng nhất?
**A**: "Privacy-preserving rare itemset mining — dòng 2024–2025 trên Information Sciences. Lý do: chính vì hiếm, các mẫu này dễ định danh cá nhân hơn mẫu phổ biến nên rủi ro riêng tư cao hơn. Với dữ liệu Việt Nam, em muốn thử luật kết hợp hiếm trên hồ sơ bệnh án theo phương pháp luận của Darrab 2024 trên Scientific Reports."
