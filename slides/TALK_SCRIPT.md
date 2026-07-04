# Kịch bản thuyết trình: Khai thác các mẫu hiếm (Rare Pattern Mining)

**Hình thức**: thuyết trình bài tập lớn, 15 phút, 18 slides
**Nguồn**: `bao_cao_rare_pattern_mining.md`
**Lưu ý thời gian**: kịch bản đầy đủ chạy 15:40. Nếu bị giới hạn đúng 15:00, rút slide 6 (Toàn cảnh) xuống 0:20 — chỉ vào sơ đồ và đọc 4 khối — và lướt nhanh slide 3 còn 0:40.

## Slide 1: Trang bìa [0:00 – 0:15]

_[Chờ thầy/cô mời lên]_

"Em xin chào thầy/cô và các bạn. Em là [Họ tên], MSSV [.....]. Hôm nay em xin trình bày đề tài **Khai thác các mẫu hiếm — Rare Pattern Mining**, bài tập lớn môn Khai thác dữ liệu nâng cao."

---

## Slide 2: Nội dung trình bày [0:15 – 0:35]

"Bài trình bày của em gồm năm phần: thứ nhất là bài toán và động cơ; thứ hai, ba định nghĩa hình thức của mẫu hiếm; thứ ba, ba thuật toán AprioriRare, AprioriInverse và CORI; thứ tư, các độ đo tương quan và tính null-invariance; và cuối cùng là phần em tự cài đặt, kiểm chứng tự động và thực nghiệm trên dữ liệu thật."

→ _Chuyển_: "Em xin bắt đầu từ câu hỏi: vì sao cần quan tâm mẫu hiếm?"

---

## Slide 3: Động cơ [0:35 – 1:35]

"Thưa thầy/cô, điều thú vị nhất trong dữ liệu **có phải là điều xảy ra thường xuyên nhất** không? Khai thác tập mục phổ biến — FIM — ngầm trả lời 'có': nó chỉ giữ lại những gì vượt ngưỡng hỗ trợ.

Nhưng trong nhiều ứng dụng, câu trả lời là 'không'. Trong y tế, tổ hợp triệu chứng của bệnh hiếm xuất hiện rất ít nhưng mang giá trị chẩn đoán cao. Trong công nghiệp, lỗi sản phẩm hiếm gặp mới chính là thứ cần phát hiện. Trong an ninh mạng, hành vi bất thường — theo định nghĩa — là hành vi hiếm.

Tất cả các mẫu này bị FIM truyền thống **bỏ qua hoàn toàn**."

→ _Chuyển_: "Phản xạ đầu tiên là: vậy hạ thấp ngưỡng hỗ trợ xuống là xong?"

---

## Slide 4: Vấn đề [1:35 – 2:35]

"Đáng tiếc là không. Hạ thấp minsup gây ra hai hệ quả. Một là **bùng nổ tổ hợp**: ngưỡng càng thấp thì càng nhiều tập mục vượt qua được, số lượng tăng theo cấp mũ — máy không xử lý nổi và người cũng không đọc nổi kết quả. Hai là **nhiễu**: rất nhiều 'mẫu hiếm' thu được có support bằng 0 — tức là chúng **chưa từng xuất hiện** trong dữ liệu. Ví dụ hai mặt hàng chưa ai mua cùng nhau bao giờ: cặp này 'hiếm' theo nghĩa đen, nhưng hoàn toàn vô nghĩa.

Vì vậy lĩnh vực rare pattern mining cần cả ba mảnh ghép: định nghĩa chặt chẽ hơn về 'hiếm có ý nghĩa', thuật toán khai thác riêng, và độ đo tương quan để lọc mẫu giả. Đó cũng là cấu trúc phần còn lại của bài."

→ _Chuyển_: "Để nói chuyện cụ thể, em dùng một ví dụ nhỏ xuyên suốt."

---

## Slide 5: Ví dụ [2:35 – 3:20]

"Đây là cơ sở dữ liệu 4 giao dịch theo bài giảng. Support của một tập mục đơn giản là **số giao dịch chứa đủ mọi mục trong tập đó** — ví dụ {pasta, lemon} có support 3 vì xuất hiện cùng nhau ở T1, T2 và T4.

Em xin lưu ý một chi tiết: **pasta có mặt trong cả bốn giao dịch** — chi tiết này sẽ quay lại ở phần mẫu giả.

Với minsup bằng 2, có đúng **11 itemset phổ biến**. Còn {bread} chỉ xuất hiện một lần, và {bread, cake} không xuất hiện lần nào — support bằng 0. Mọi thuật toán phía sau đều được em chạy tay trên ví dụ này và dùng nó để kiểm chứng cài đặt."

→ _Chuyển_: "Trước khi đi vào chi tiết, em xin đưa toàn cảnh dòng chảy bài toán trên chính ví dụ này."

---

## Slide 6: Toàn cảnh — dòng chảy bài toán trên ví dụ [3:20 – 4:00]

_[Chỉ theo sơ đồ, lần lượt từng khối từ trái sang phải]_

"Đây là bản đồ của toàn bộ bài toán, chạy trên chính 4 giao dịch vừa rồi.

Xuất phát từ **cơ sở dữ liệu thô**. Bước một, dùng ngưỡng minsup để trả lời 'thế nào là hiếm' và **khai thác mẫu hiếm**: AprioriRare tìm ra các mẫu hiếm tối thiểu {bread} và {lemon, cake}; AprioriInverse tìm các mẫu hiếm 'thuần khiết' như {bread}.

Nhưng hiếm thôi chưa đủ. Bước hai, dùng độ đo tương quan để **lọc mẫu giả**: cặp {pasta, cake} tuy xuất hiện ở nửa số giao dịch nhưng bond chỉ 0.5 và lift đúng bằng 1 — chúng đi cùng nhau chỉ vì pasta có mặt khắp nơi, không phải vì có liên hệ thật.

Cuối cùng, **CORI** gộp cả hai điều kiện — vừa hiếm vừa gắn kết — và cho ra đúng ba mẫu: {bread}, {cake}, {orange, cake}.

Mỗi khối trên sơ đồ tương ứng một phần tiếp theo của bài, nên thầy/cô và các bạn có thể định vị mình đang ở đâu."

→ _Chuyển_: "Em bắt đầu từ khối đầu tiên: 'hiếm' chính xác nghĩa là gì? Có ba câu trả lời."

---

## Slide 7: Ba định nghĩa mẫu hiếm [4:00 – 5:15]

_[Bấm từng `\pause`]_

"Định nghĩa thứ nhất, **infrequent**: cứ support dưới ngưỡng là hiếm. Đơn giản nhưng vô dụng — kết quả bùng nổ và chứa cả các mẫu support bằng 0 chưa từng tồn tại.

_[bấm]_ Định nghĩa thứ hai, **minimal rare itemset — mRI**: itemset hiếm mà **mọi tập con thực sự của nó đều phổ biến**. Trên ví dụ: {lemon, cake} có support 1 — hiếm; nhưng {lemon} support 3 và {cake} support 2 — đều phổ biến. Vậy {lemon, cake} là điểm 'vừa mới vượt biên' từ vùng phổ biến sang vùng hiếm. Hình dung dàn itemset chia hai vùng — mRI chính là **đường biên dưới của vùng hiếm**. Tập mRI nhỏ gọn, nhưng mọi mẫu hiếm đều là tập cha của một mRI nào đó, nên nắm được biên là nắm được cả vùng.

_[bấm]_ Định nghĩa thứ ba, **perfectly rare itemset — PRI**: dùng hai ngưỡng — support nằm giữa minsup và maxsup — và thêm điều kiện **từng item thành phần cũng phải hiếm**. Ngưỡng dưới loại bỏ nhiễu quá hiếm; điều kiện thứ hai cho mẫu hiếm 'thuần khiết', không dính item phổ biến.

_[bấm]_ Tổng kết trên ví dụ với minsup 2: mRI gồm {bread} và {lemon, cake}; PRI chỉ có {bread} — vì bread vừa hiếm, vừa là item hiếm duy nhất."

→ _Chuyển_: "Mỗi định nghĩa có một thuật toán tương ứng."

---

## Slide 8: AprioriRare [5:15 – 6:30]

"AprioriRare tìm toàn bộ mRI. Nó duyệt theo tầng đúng như Apriori: tầng một đếm support từng item, tầng hai ghép các item phổ biến thành cặp, và cứ thế đi lên.

Chạy cụ thể trên ví dụ: tầng một, bread có support 1 — hiếm ngay từ đầu — nên {bread} là mRI. Tầng hai, chỉ ghép các item phổ biến với nhau; cặp {lemon, cake} đếm ra support 1 — hiếm — thành mRI thứ hai. Kết quả đúng {bread} và {lemon, cake}, khớp bài giảng.

Điểm tinh tế nhất nằm ở đây: một ứng viên đã **sống sót qua bước prune** nghĩa là mọi tập con của nó đều phổ biến. Vì vậy hễ đếm ra nó không phổ biến thì nó **tự động là một mRI** — không cần kiểm tra gì thêm.

Nhược điểm cố hữu: biên hiếm nằm phía trên vùng phổ biến, nên muốn chạm tới nó thuật toán phải **đi xuyên qua và đếm toàn bộ vùng phổ biến** trước. Em sẽ định lượng cái giá này ở thực nghiệm A."

→ _Chuyển_: "Thuật toán thứ hai chọn hướng ngược lại."

---

## Slide 9: AprioriInverse [6:30 – 7:30]

"AprioriInverse tìm PRI, và khác biệt nằm ngay bước khởi tạo: **vứt bỏ mọi item phổ biến trước khi bắt đầu**. Trên ví dụ, pasta xuất hiện ở cả 4 giao dịch nên bị loại ngay từ vòng gửi xe — mọi tổ hợp về sau không bao giờ chứa pasta.

Vì sao làm vậy vẫn đúng? Vì support của một tập không bao giờ vượt quá support của item yếu nhất trong nó — nếu mọi item đều hiếm thì mọi tổ hợp của chúng cũng hiếm, điều kiện PRI tự được thoả. Không gian tìm kiếm nhờ đó nhỏ hơn hẳn.

Cái giá phải trả: các **mẫu lai** — trộn item hiếm với item phổ biến, ví dụ {bệnh hiếm, triệu chứng phổ biến} trong y tế — nằm ngoài tầm với vĩnh viễn, vì item phổ biến đã bị vứt từ đầu.

Chạy trên ví dụ với hai ngưỡng 1.1 và 3.1 cho đúng 5 PRI như bài giảng."

→ _Chuyển_: "Đến đây ta đã tìm được mẫu hiếm. Nhưng hiếm thôi chưa đủ — mẫu đó có đáng tin không?"

---

## Slide 10: Mẫu giả [7:30 – 8:15]

"Quay lại chi tiết em đã gửi gắm ở slide ví dụ. Cặp {pasta, cake} xuất hiện ở 2 trên 4 giao dịch — support 50%, nghe có vẻ là mẫu tốt.

Nhưng để ý: pasta có mặt trong **mọi** giao dịch. Nghĩa là hễ giao dịch nào có cake thì đương nhiên có pasta — hai thứ 'đi cùng nhau' chỉ vì pasta đi cùng **tất cả mọi thứ**. Sự đồng xuất hiện này là tất yếu, **không nói lên bất kỳ mối liên hệ nào** giữa pasta và cake. Đây gọi là mẫu giả — spurious pattern.

Support không phân biệt được 'đi cùng nhau vì có liên hệ' với 'đi cùng nhau vì một bên có mặt khắp nơi'. Ta cần độ đo tương quan để làm việc đó."

→ _Chuyển_: "Bài giảng giới thiệu hai độ đo chính."

---

## Slide 11: bond và all-confidence [8:15 – 9:15]

"**Bond** lấy support hội chia cho support tuyển. Nói dễ hiểu: trong số các giao dịch *có dính dáng* tới mẫu — chứa ít nhất một mục của nó — bao nhiêu phần chứa *trọn vẹn* mẫu?

Tính cụ thể: bond của {pasta, orange}. Giao dịch chứa ít nhất một trong hai là cả 4 giao dịch; giao dịch chứa cả hai là T1, T3, T4 — vậy bond bằng 3/4: khá gắn kết. Còn {cake, bread}: không giao dịch nào chứa cả hai — bond bằng 0. Bond bằng 1 nghĩa là hai mục **luôn luôn** đi cùng nhau, không bao giờ xuất hiện lẻ.

**All-confidence** lấy support của mẫu chia cho support của item mạnh nhất trong mẫu — và nó chính là **confidence nhỏ nhất** trong mọi luật kết hợp sinh từ mẫu: kịch bản bi quan nhất vẫn đạt bao nhiêu.

Cả hai có chung tính chất quan trọng: **anti-monotone** — thêm mục vào mẫu thì giá trị chỉ giảm hoặc giữ nguyên. Nhờ đó có thể cắt tỉa kiểu Apriori: một mẫu đã rớt ngưỡng thì mọi mẫu lớn hơn chứa nó cũng rớt — CORI sẽ khai thác triệt để điều này."

→ _Chuyển_: "Một câu hỏi tự nhiên: sao không dùng lift hay chi bình phương quen thuộc?"

---

## Slide 12: Null-invariance [9:15 – 10:00]

"Câu trả lời nằm ở khái niệm **null transaction** — giao dịch không chứa mục nào của mẫu đang xét.

Hình dung một siêu thị có một triệu giao dịch, trong đó cặp mặt hàng ta quan tâm chỉ liên quan tới vài trăm giao dịch. Lift và chi bình phương được tính trên **toàn bộ** một triệu giao dịch — nên chín trăm chín mươi mấy nghìn giao dịch chẳng liên quan gì vẫn tham gia vào công thức và có thể thổi phồng hoặc dìm giá trị độ đo. Bond và all-confidence thì chỉ nhìn vào các giao dịch có dính dáng tới mẫu — thêm bao nhiêu giao dịch không liên quan giá trị cũng **không đổi**. Đó gọi là tính null-invariant.

Mẫu hiếm — theo đúng định nghĩa — chỉ chạm một phần rất nhỏ dữ liệu; phần còn lại toàn null transactions. Vì vậy với mẫu hiếm, dùng độ đo null-invariant là **bắt buộc**, không phải tuỳ chọn."

→ _Chuyển_: "Hai dòng kỹ thuật — hiếm và tương quan — hội tụ ở thuật toán cuối cùng: CORI."

---

## Slide 13: CORI [10:00 – 11:15]

"CORI tìm các itemset **vừa hiếm vừa thực sự gắn kết**: support dưới maxsup _và_ bond từ minbond trở lên.

Điều đẹp ở đây là hai ràng buộc có bản chất **đối ngẫu**: đã hiếm thì mọi tập cha đều hiếm — tính monotone; còn bond đã rớt ngưỡng thì mọi tập cha đều rớt — tính anti-monotone. CORI khai thác đồng thời cả hai trong một lần duyệt kiểu Eclat.

Cơ chế cụ thể: mỗi itemset mang theo hai danh sách — **TID-List** là các giao dịch chứa *trọn vẹn* nó, **DTID-List** là các giao dịch chứa *ít nhất một* mục của nó. Khi ghép {orange} với {cake}: TID-List lấy **giao** — orange có ở T1, T3, T4, cake ở T3, T4, giao lại còn T3, T4, tức support 2; DTID-List lấy **hợp** — T1, T3, T4, tức 3 giao dịch. Bond bằng 2/3, vượt ngưỡng 0.6 — giữ lại. Mọi thứ tính ngay trên hai danh sách, **không cần quét lại cơ sở dữ liệu**.

Một chi tiết thiết kế đáng chú ý: nút có support còn cao — chưa hiếm — **vẫn phải mở rộng tiếp**, vì tập cha của nó có thể hiếm. Đây là điểm khác hẳn cắt tỉa support truyền thống.

Chạy trên ví dụ với maxsup 3 và minbond 0.6 cho đúng ba kết quả {bread}, {cake}, {orange, cake} — khớp bài giảng."

→ _Chuyển_: "Toàn bộ lý thuyết trên được em cài đặt lại từ đầu và kiểm chứng tự động."

---

## Slide 14: Cài đặt & kiểm chứng [11:15 – 12:15]

"Em cài đặt cả ba thuật toán bằng Python thuần, **chỉ dùng thư viện chuẩn**, trên cùng một biểu diễn TID-set — support của ứng viên tính bằng phép giao hai TID-set của cha thay vì quét lại dữ liệu.

Về kiểm chứng: em viết **19 câu lệnh assert**. Assert giống như bài kiểm tra tự chấm: em tính tay từng con số kỳ vọng trên ví dụ minh họa — bao nhiêu itemset phổ biến, mRI gồm những gì, bond từng cặp bằng bao nhiêu — rồi để chương trình tự đối chiếu; chỉ cần lệch một con số là chương trình dừng và báo sai ngay. Kết quả: **19 trên 19 đạt, 100%**, phủ toàn bộ FIM, AprioriRare, AprioriInverse, CORI và các độ đo.

Và bảng độ đo cặp xác nhận bằng số trực giác mẫu giả: {pasta, cake} có lift đúng bằng 1.0 và bond 0.5 — không hề tương quan."

→ _Chuyển_: "Trên dữ liệu thật, các đánh đổi lý thuyết hiện ra thế nào?"

---

## Slide 15: Exp A [12:15 – 13:15]

_[Hình runtime — chỉ vào biểu đồ]_

"Em thực nghiệm trên bộ UCI Mushroom: 8 124 giao dịch, mỗi giao dịch là một cây nấm mô tả bằng 118 thuộc tính-giá trị — dữ liệu rất dày.

Cách đọc biểu đồ: trục hoành là minsup giảm dần từ 0.6 về 0.2; trục tung là thời gian chạy AprioriRare. Đường gần như nằm ngang cho đến khoảng 0.3, rồi **vọt dựng đứng** ở 0.2 — lên khoảng 3 giây.

Vì sao? Khi minsup giảm, vùng phổ biến phình ra: số itemset phổ biến phải đếm tăng khoảng **890 lần** — từ 51 lên hơn 45 nghìn. Trong khi đó thứ ta thực sự cần — số mRI — chỉ tăng khoảng **8 lần**, từ 122 lên 986. Tức là thuật toán phải lội qua cả cánh đồng chỉ để chạm tới hàng rào ở mép.

Kết luận: mRI quả thực là biểu diễn biên rất gọn, nhưng **chi phí tính nó bị quyết định bởi kích thước vùng phổ biến** — đúng như dự báo lý thuyết ở slide AprioriRare. Đây là lý do các nghiên cứu gần đây tìm cách né duyệt vét cạn bằng metaheuristic hoặc biểu diễn bit dọc."

---

## Slide 16: Exp B & C [13:15 – 14:30]

_[Hình experiments]_

"Thực nghiệm B với AprioriInverse: thời gian chạy ở mức **mili-giây** — nhanh hơn AprioriRare hai đến ba bậc. Lý do rất trực quan: bước loại item phổ biến vứt bỏ phần lớn trong số 118 item ngay từ đầu, bài toán co lại chỉ còn một nhóm item hiếm nhỏ. Nhưng em xin nhấn mạnh: đây **không phải benchmark cùng điều kiện** — hai thuật toán giải hai bài toán khác nhau với bộ ngưỡng khác nhau, nên các con số chỉ nói lên chi phí đặc trưng của từng bài toán, không nói thuật toán nào 'giỏi hơn'.

Thực nghiệm C với CORI cho một hiện tượng thú vị: khi em **nới lỏng** ngưỡng bond từ 0.95 xuống tận 0.5 — tức là dễ tính hơn hẳn — số mẫu tìm được chỉ nhích từ khoảng 90 lên 104, gần như **bão hòa**. Điều này nói lên đặc điểm của dữ liệu: các nhóm thuộc tính của cây nấm hoặc gắn kết rất chặt với bond sát 1, hoặc rời rạc hẳn — hầu như không có trường hợp lưng chừng ở giữa để 'vớt' thêm khi nới ngưỡng.

Và đây là mẫu em thích nhất: 36 cây nấm có mùi mốc — chỉ chiếm 0.44% dữ liệu — và cả 36 cây này **luôn luôn** đồng thời không có vòng cuống và có cuống màu quế. Bond đúng bằng 1: hễ thấy một trong ba đặc điểm ấy là chắc chắn thấy đủ cả ba. Với minsup thông thường, FIM đã vứt mẫu này từ vòng đầu — đây chính xác là loại tri thức mà chỉ khai thác mẫu hiếm mới chạm tới."

→ _Chuyển_: "Ba thực nghiệm chốt lại ba đánh đổi."

---

## Slide 17: Kết luận [14:30 – 15:20]

"Kết luận của em gồm ba đánh đổi: **mRI gọn nhưng đắt** — phải duyệt toàn vùng phổ biến; **PRI rẻ nhưng hẹp** — bỏ sót mẫu lai; **CORI cân bằng** — ràng buộc kép cho kết quả nhỏ và giàu ngữ nghĩa.

Thông điệp em muốn gửi: không có định nghĩa hiếm 'đúng' duy nhất — chỉ có đánh đổi phù hợp với từng bài toán; và trên dữ liệu thưa, null-invariance là bắt buộc.

Về hướng phát triển 2021–2026: metaheuristic cho dữ liệu lớn, mở rộng fuzzy và utility, và đặc biệt thời sự là **privacy** — chính vì hiếm, mẫu hiếm dễ định danh cá nhân hơn mẫu phổ biến."

---

## Slide 18: Cảm ơn & Hỏi đáp [15:20 – 15:40]

"Tóm lại, em đã trình bày ba định nghĩa, ba thuật toán, cài đặt kiểm chứng tự động 100% và thực nghiệm trên UCI Mushroom. Em xin cảm ơn thầy/cô và các bạn đã lắng nghe — em sẵn sàng nhận câu hỏi ạ."

---

## Bảng thời gian

| Slide | Chủ đề               | Thời lượng | Cộng dồn |
| :---: | -------------------- | :--------: | :------: |
|   1   | Trang bìa            |    0:15    |   0:15   |
|   2   | Nội dung             |    0:20    |   0:35   |
|   3   | Động cơ              |    1:00    |   1:35   |
|   4   | Vấn đề               |    1:00    |   2:35   |
|   5   | Ví dụ                |    0:45    |   3:20   |
|   6   | Toàn cảnh dòng chảy  |    0:40    |   4:00   |
|   7   | Ba định nghĩa        |    1:15    |   5:15   |
|   8   | AprioriRare          |    1:15    |   6:30   |
|   9   | AprioriInverse       |    1:00    |   7:30   |
|  10   | Mẫu giả              |    0:45    |   8:15   |
|  11   | bond / allconf       |    1:00    |   9:15   |
|  12   | Null-invariance      |    0:45    |  10:00   |
|  13   | CORI                 |    1:15    |  11:15   |
|  14   | Cài đặt & kiểm chứng |    1:00    |  12:15   |
|  15   | Exp A                |    1:00    |  13:15   |
|  16   | Exp B & C            |    1:15    |  14:30   |
|  17   | Kết luận             |    0:50    |  15:20   |
|  18   | Cảm ơn               |    0:20    |  15:40   |

**Tổng**: 15:40 — nếu cần đúng 15:00: rút slide 6 còn 0:20 và slide 3 còn 0:40.

---

## Q&A dự kiến

### Q1: AprioriRare và AprioriInverse — khi nào dùng cái nào?

**A**: "Trả lời ngắn: cần **đủ mọi mẫu hiếm** thì dùng AprioriRare; chỉ cần mẫu mà **mọi thành phần đều hiếm** thì dùng AprioriInverse.

Cụ thể hơn: chỉ AprioriRare mới bắt được mẫu lai — mẫu trộn item hiếm với item phổ biến, ví dụ {bệnh hiếm, triệu chứng phổ biến}: bệnh thì hiếm nhưng triệu chứng như sốt lại rất phổ biến. AprioriInverse không bao giờ thấy mẫu này vì nó vứt item phổ biến từ đầu — đổi lại nó nhanh hơn hai đến ba bậc trên Mushroom. Tóm lại là đánh đổi giữa độ phủ và tốc độ."

### Q2: Vì sao không so sánh trực tiếp thời gian chạy hai thuật toán?

**A**: "Vì hai thuật toán giải **hai đề bài khác nhau** với bộ ngưỡng khác nhau — giống như so thời gian của một người dọn cả kho hàng với một người chỉ dọn một góc kho: người sau xong sớm hơn không phải vì giỏi hơn, mà vì việc ít hơn. Tìm PRI vốn dĩ rẻ vì alphabet bị thu hẹp ngay từ đầu; tìm mRI buộc phải đếm hết vùng phổ biến. Nên các con số chỉ nên đọc là 'chi phí đặc trưng của từng bài toán'."

### Q3: Vì sao CORI giới hạn kích thước itemset ≤ 4?

**A**: "Đó là giới hạn **do em đặt cho phần khảo sát**, không phải giới hạn của thuật toán. Mỗi giao dịch Mushroom có trung bình gần 23 item — nếu không chặn kích thước, số tổ hợp con cần xét lên tới hàng triệu và thời gian chạy vượt khỏi phạm vi bài tập. Trong kết quả, 'kích thước lớn nhất bằng 4' chính là giá trị chạm trần này; nếu nới trần, số mẫu có thể tăng thêm — em đã ghi rõ điều đó trong báo cáo."

### Q4: Hiện tượng bão hòa ở Exp C nói lên điều gì?

**A**: "Nó nói lên rằng dữ liệu Mushroom phân thành **hai cực rõ rệt**. Em nới ngưỡng bond từ 0.95 xuống 0.5 — tức là hạ tiêu chuẩn gần một nửa — mà chỉ thêm được khoảng 14 mẫu. Nghĩa là các nhóm thuộc tính hoặc gắn kết rất chặt với bond sát 1 và đã được bắt từ đầu, hoặc rời rạc hẳn với bond dưới 0.5 — hầu như không có mẫu 'lưng chừng' để vớt thêm. Một hệ quả phụ: cắt tỉa theo bond rất hiệu quả, thời gian chạy chỉ tăng nhẹ khi nới ngưỡng."

### Q5: Một mRI có thể có support bằng 0 không?

**A**: "Có. Ví dụ dễ hình dung: sữa và bột giặt đều bán rất chạy — hai item phổ biến — nhưng giả sử chưa khách nào mua cả hai trong cùng một lần. Cặp {sữa, bột giặt} có support 0 — hiếm — trong khi mọi tập con của nó đều phổ biến — thoả đúng định nghĩa mRI. Khác với định nghĩa infrequent thô cho ra vô số mẫu support 0, tập mRI chỉ chứa đúng vài mẫu như vậy nằm trên biên. Riêng PRI thì không bao giờ có support 0, vì nó có ngưỡng dưới minsup chặn lại."

### Q6: Vì sao lift của {pasta, cake} đúng bằng 1?

**A**: "Lift bằng 1 nghĩa là hai mục **độc lập thống kê** — biết giao dịch có pasta không giúp đoán thêm gì về cake. Tính cụ thể: pasta có trong 100% giao dịch, nên xác suất 'có cả pasta lẫn cake' đúng bằng xác suất 'có cake'. Thay vào công thức lift = P(pasta, cake) / [P(pasta) × P(cake)] = P(cake) / [1 × P(cake)] = 1. Đây là minh họa đẹp cho mẫu giả: support tới 50% nhưng về mặt thống kê là không có liên hệ nào."

### Q7: Cài đặt có tối ưu không? Có thể nhanh hơn?

**A**: "Chưa tối ưu ạ — em cài bằng Python thuần, chưa dùng bitset hay chạy song song, nên các con số thời gian chỉ nên đọc theo nghĩa **so sánh tương đối** giữa các thuật toán, không phải hiệu năng tuyệt đối. Nếu cần nhanh hơn, văn liệu đã có hai hướng sẵn: biểu diễn bit dọc như Capillar 2023 — thay tập giao dịch bằng dãy bit để phép giao thành phép AND cực nhanh — hoặc bỏ hẳn vét cạn, dùng tối ưu hoá cross-entropy như MRI-CE 2024."

### Q8: Hướng phát triển nào em thấy tiềm năng nhất?

**A**: "Privacy-preserving rare itemset mining — dòng nghiên cứu 2024–2025 trên Information Sciences. Lý do rất trực quan từ chính kết quả của em: mẫu bond bằng 1 ở Exp C chỉ khớp với 36 trên 8 124 bản ghi. Nếu đây là hồ sơ bệnh án thay vì cây nấm, một mẫu hiếm như vậy gần như **chỉ mặt được từng cá nhân** — rủi ro riêng tư cao hơn hẳn mẫu phổ biến. Với dữ liệu Việt Nam, em muốn thử luật kết hợp hiếm trên hồ sơ bệnh án theo phương pháp luận của Darrab 2024 trên Scientific Reports."
