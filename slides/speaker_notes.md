# Speaker Notes — Khai thác các mẫu hiếm (15 phút, 17 slides)

### việc chọn đúng 3 thuật toán và bộ độ đo này không phải ngẫu nhiên —

### Lý do học thuật: 3 thuật toán ↔ 3 định nghĩa, không thừa không thiếu

Đây là điểm mạnh nhất để bảo vệ. Mỗi thuật toán là đại diện chính tắc (canonical) cho một định nghĩa hình thức của mẫu hiếm — chúng tạo thành một hệ thống khép kín chứ không phải 3 lựa chọn tùy ý:

Định nghĩa Thuật toán chính tắc Vai trò trong "câu chuyện"

- Minimal rare itemset (mRI) AprioriRare (Szathmary 2007) Biên dưới vùng hiếm — gọn nhưng đắt (phải duyệt hết vùng phổ biến)
- Perfectly rare itemset (PRI) AprioriInverse (Koh & Rountree 2005) Hiếm "thuần khiết" — rẻ nhưng hẹp (bỏ sót mẫu lai)
- Rare correlated itemset CORI (Bouasker 2015) Hiếm + gắn kết thật — cân bằng chất lượng, loại mẫu giả

  Ba thuật toán này thể hiện đúng trục đánh đổi biểu đạt–chi phí mà Chương 4 định lượng được trên Mushroom (45 391 itemset phổ biến để tìm 986 mRI, so với mili-giây của AprioriInverse). Thay một trong ba bằng thuật toán khác sẽ phá vỡ sự tương ứng 1-1 định nghĩa ↔ thuật toán.

Báo cáo được xây dựng theo bài giảng "Rare Itemset Techniques" của môn Khai thác dữ liệu nâng cao — phạm vi đề tài là tái hiện, cài đặt và kiểm chứng đúng nội dung đó (toàn bộ 19 assert ở Chương 4 đối chiếu với từng con số trong slide). Chọn thuật toán khác sẽ lệch phạm vi bài tập lớn.

3. Vì sao bond + all-confidence + null-invariance (mà không phải lift, χ²)?
   Mẫu hiếm theo định nghĩa chỉ xuất hiện trong phần rất nhỏ dữ liệu → phần còn lại là null transactions. Lift và χ² không null-invariant: hàng nghìn giao dịch không liên quan thổi phồng/bóp méo giá trị của chúng (mục 3.5). Vậy với rare mining, chỉ nhóm độ đo null-invariant là hợp lệ — đây là lập luận của khung Wu et al. [6].
   Trong nhóm null-invariant (bond, all-confidence, cosine, Kulczynski, max-confidence — bảng 3.1 vẫn trình bày đủ cả 7 độ đo để so sánh), báo cáo đi sâu vào bond và all-confidence vì hai lý do: (i) cả hai anti-monotone, nên cắt tỉa được kiểu Apriori/Eclat — cosine và Kulczynski không có tính chất này nên không nhúng được vào thuật toán khai thác; (ii) bond chính là ràng buộc lõi của CORI — TID-List/DTID-List của CORI được thiết kế riêng để tính bond tăng dần. Nói cách khác, độ đo được chọn vì nó vận hành được trong thuật toán, không chỉ để đánh giá hậu kiểm.

4. Vì sao không chọn thuật toán "mới hơn"?
   Mục 2.4 đã chặn trước câu hỏi này: các công bố 2023–2024 ([18] bitwise vertical mining, [20] MRI-CE cross-entropy) vẫn dùng AprioriRare/AprioriInverse làm baseline — tức muốn hiểu và đánh giá các phương pháp mới thì phải nắm vững các thuật toán kinh điển trước.
   Các hướng mới (FP-tree-based như RP-Tree, metaheuristic, fuzzy, high-utility) được xếp vào tổng quan 2021–2026 và hướng phát triển (mục 5.2) thay vì phân tích sâu, vì chúng nằm ngoài phạm vi bài giảng và đòi hỏi nền tảng chính là 3 thuật toán này.

Một câu tóm tắt nếu bị hỏi trực tiếp: "Ba thuật toán được chọn vì mỗi cái là thuật toán gốc tương ứng với một trong ba định nghĩa hình thức của mẫu hiếm, tạo thành phổ đánh đổi đầy đủ (gọn-nhưng-đắt / rẻ-nhưng-hẹp / cân bằng-chất-lượng); bond và all-confidence được chọn vì chúng vừa null-invariant — bắt buộc với dữ liệu hiếm/thưa — vừa anti-monotone nên nhúng được vào cơ chế cắt tỉa, trong đó bond là ràng buộc lõi của CORI."
