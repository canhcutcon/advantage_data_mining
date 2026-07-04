# Slide Outline — Khai thác mẫu hiếm (Rare Pattern Mining)

- **Nguồn**: `bao_cao_rare_pattern_mining.md` (bài tập lớn môn Khai thác dữ liệu nâng cao)
- **Loại talk**: oral, 15 phút, 18 slides
- **Ngôn ngữ**: tiếng Việt — engine xelatex
- **Tỉ lệ**: 16:9 · **Màu**: NeurIPS (tím `#8B5CF6` / xanh `#2563EB`)
- **Hình**: `figures/mushroom_experiments.png`, `figures/mushroom_runtime.png`

| # | Slide | Thời lượng | Cộng dồn |
|---|-------|-----------|----------|
| 1 | Trang bìa | 0:15 | 0:15 |
| 2 | Nội dung trình bày | 0:20 | 0:35 |
| 3 | Động cơ: mẫu hiếm nhưng giá trị cao | 1:00 | 1:35 |
| 4 | Vấn đề: hạ minsup là không đủ | 1:00 | 2:35 |
| 5 | Ví dụ (4 giao dịch) | 0:45 | 3:20 |
| 6 | Toàn cảnh: dòng chảy bài toán trên ví dụ | 0:40 | 4:00 |
| 7 | Ba định nghĩa mẫu hiếm | 1:15 | 5:15 |
| 8 | AprioriRare: tìm biên hiếm tối thiểu | 1:15 | 6:30 |
| 9 | AprioriInverse: thu hẹp ngay từ đầu | 1:00 | 7:30 |
| 10 | Mẫu giả: phổ biến ≠ đáng tin | 0:45 | 8:15 |
| 11 | bond và all-confidence | 1:00 | 9:15 |
| 12 | Null-invariance: vì sao lift thất bại | 0:45 | 10:00 |
| 13 | CORI: hiếm + tương quan trong một lần duyệt | 1:15 | 11:15 |
| 14 | Cài đặt & kiểm chứng 100% | 1:00 | 12:15 |
| 15 | Exp A — Cái giá của việc đi xuyên vùng phổ biến | 1:00 | 13:15 |
| 16 | Exp B & C — PRI rẻ, CORI giàu ngữ nghĩa | 1:15 | 14:30 |
| 17 | Kết luận: ba đánh đổi | 0:50 | 15:20 |
| 18 | Cảm ơn & Hỏi đáp | 0:20 | 15:40 |

> Tổng 15:40 — nếu cần đúng 15:00: rút slide 6 còn 0:20 và slide 3 còn 0:40.

---

## Slide 1 — Trang bìa

- Tiêu đề: **Khai thác các mẫu hiếm (Rare Pattern Mining)**
- Phụ đề: Bài tập lớn môn Khai thác dữ liệu nâng cao
- Tác giả: [Họ tên — MSSV], Tháng 6/2026

**Nói**: Chờ giới thiệu, chào, nêu tên đề tài. *(0:15)*

## Slide 2 — Nội dung trình bày

- Bài toán & động cơ
- Ba định nghĩa mẫu hiếm
- Ba thuật toán: AprioriRare, AprioriInverse, CORI
- Độ đo tương quan & null-invariance
- Cài đặt, kiểm chứng, thực nghiệm Mushroom

**Nói**: Lướt nhanh 5 phần. *(0:20)*

## Slide 3 — Động cơ: mẫu hiếm nhưng giá trị cao

- Y tế: tổ hợp triệu chứng bệnh hiếm → giá trị chẩn đoán cao
- Công nghiệp: lỗi sản phẩm hiếm gặp = đối tượng cần phát hiện
- An ninh mạng: bất thường = hiếm theo định nghĩa
- **FIM truyền thống bỏ qua hoàn toàn các mẫu này**

**Nói**: Mở đầu bằng câu hỏi "điều thú vị nhất trong dữ liệu có phải là điều xảy ra thường xuyên nhất?". FIM ngầm coi phổ biến = đáng quan tâm — sai trong nhiều ứng dụng. *(1:00)*

## Slide 4 — Vấn đề: hạ minsup là không đủ

- Giải pháp ngây thơ: hạ thấp minsup
- Hệ quả 1: **bùng nổ tổ hợp** số itemset
- Hệ quả 2: nhiễu — nhiều "mẫu hiếm" có **sup = 0** (không tồn tại!)
- Cần: định nghĩa chặt chẽ + thuật toán riêng + độ đo lọc mẫu giả

**Nói**: Đặt vấn đề kỹ thuật. Đây là lý do lĩnh vực rare pattern mining ra đời. → "Trước hết, cần một ví dụ nhỏ để nói chuyện cụ thể." *(1:00)*

## Slide 5 — Ví dụ

- Bảng 4 giao dịch: T1 {pasta, lemon, bread, orange} … T4 {pasta, lemon, orange, cake}
- minsup = 2 → **11 itemset phổ biến**
- {bread} sup = 1; {bread, cake} sup = 0
- Dùng xuyên suốt để chạy tay & kiểm chứng cài đặt

**Nói**: Giới thiệu CSDL ví dụ của bài giảng — mọi thuật toán sau đều minh họa trên đây. *(0:45)*

## Slide 6 — Toàn cảnh: dòng chảy bài toán trên ví dụ

- Sơ đồ 4 khối: **CSDL giao dịch** —(minsup)→ **Khai thác mẫu hiếm** —(minbond)→ **Lọc tương quan** → **CORI**
- Dưới mỗi khối: kết quả cụ thể trên ví dụ (mRI/PRI; loại {pasta, cake}; {bread}, {cake}, {orange, cake})
- Mỗi khối = một phần tiếp theo của bài

**Nói**: Bản đồ toàn bài trên chính ví dụ 4 giao dịch — khán giả định vị được đang ở khối nào trong suốt phần còn lại. *(0:40)*

## Slide 7 — Ba định nghĩa mẫu hiếm

- **Infrequent**: sup < minsup — bùng nổ, chứa sup = 0
- **Minimal rare (mRI)**: hiếm, mọi tập con đều phổ biến — *biên dưới vùng hiếm*
- **Perfectly rare (PRI)**: minsup ≤ sup < maxsup, mọi item thành phần đều hiếm
- Ví dụ: mRI = {bread}, {lemon, cake} · PRI = {bread}

(Bảng so sánh 3 định nghĩa thu gọn, dùng `\pause` từng dòng)

**Nói**: Tâm điểm lý thuyết — nhấn hình ảnh "đường biên" trong dàn itemset. → "Mỗi định nghĩa có một thuật toán tương ứng." *(1:15)*

## Slide 8 — AprioriRare: tìm biên hiếm tối thiểu

- Duyệt theo mức như Apriori
- Ứng viên sống sót qua prune mà **không phổ biến → chính là mRI**
- Không dùng itemset hiếm để sinh ứng viên tiếp
- Ví dụ: mRI = **{bread}, {lemon, cake}** ✓ khớp bài giảng
- Nhược: phải duyệt **toàn bộ vùng phổ biến**

**Nói**: Giải thích điểm tinh tế: qua prune nghĩa là mọi tập con đều phổ biến → tự động là mRI. Gieo trước nhược điểm chi phí — Exp A sẽ định lượng. *(1:15)*

## Slide 9 — AprioriInverse: thu hẹp ngay từ đầu

- Hai ngưỡng (minsup, maxsup)
- **Loại mọi item phổ biến ngay bước khởi tạo**
- Đúng đắn: mọi item hiếm → mọi tập con hiếm (điều kiện PRI tự thoả)
- Đổi lại: bỏ sót mẫu lai {item hiếm + item phổ biến}
- Ví dụ (1.1, 3.1): 5 PRI ✓ khớp bài giảng

**Nói**: Đối lập với AprioriRare: không gian nhỏ hơn hẳn nhưng định nghĩa hẹp hơn. Ví dụ mẫu lai bị bỏ sót: {bệnh hiếm, triệu chứng phổ biến}. *(1:00)*

## Slide 10 — Mẫu giả: phổ biến ≠ đáng tin

- {pasta, cake} xuất hiện 50% giao dịch
- Nhưng pasta có mặt trong **mọi** giao dịch
- Đồng xuất hiện là tất yếu — **không có liên hệ thật** (spurious)
- Cần độ đo tương quan để lọc

**Nói**: Chuyển mạch sang nửa thứ hai của câu chuyện: hiếm thôi chưa đủ, còn cần "thật". *(0:45)*

## Slide 11 — bond và all-confidence

- **bond(X) = sup(X) / dsup(X)** — tỉ lệ giao dịch "liên quan" chứa toàn bộ X
- bond = 1: các mục **luôn** đi cùng nhau
- **allconf(X) = sup(X) / max sup(item)** — confidence nhỏ nhất của mọi luật từ X
- Cả hai: = 1 với itemset đơn, **anti-monotone** → cắt tỉa kiểu Apriori
- Ví dụ: bond({cake, bread}) = 0 · bond({pasta, orange}) = 3/4

**Nói**: Hai độ đo chính của bài giảng. Nhấn tính anti-monotone vì CORI sẽ dùng nó để cắt tỉa. *(1:00)*

## Slide 12 — Null-invariance: vì sao lift thất bại

- Null transaction: giao dịch không chứa mục nào của mẫu
- χ², lift bị **bóp méo** bởi hàng triệu giao dịch không liên quan
- bond, all-confidence, cosine, Kulczynski: **null-invariant**
- Mẫu hiếm ⊂ phần rất nhỏ dữ liệu → **bắt buộc dùng null-invariant**

**Nói**: Lý do sâu xa để chọn bond/allconf cho mẫu hiếm — dữ liệu thưa toàn null transactions. *(0:45)*

## Slide 13 — CORI: hiếm + tương quan trong một lần duyệt

- Rare correlated: **sup(X) < maxsup VÀ bond(X) ≥ minbond**
- Hai ràng buộc đối ngẫu: hiếm = monotone · bond = anti-monotone
- Duyệt kiểu Eclat, mỗi itemset giữ **TID-List + DTID-List**
- bond rớt ngưỡng → cắt cả nhánh; sup ≥ maxsup → chưa xuất nhưng vẫn mở rộng
- Ví dụ (3, 0.6): **{bread}, {cake}, {orange, cake}** ✓

**Nói**: Đỉnh lý thuyết của talk — hai dòng kỹ thuật hội tụ. Giải thích phép giao/hợp TID khi nối hai itemset. *(1:15)*

## Slide 14 — Cài đặt & kiểm chứng 100%

- Python 3.13, **chỉ thư viện chuẩn**; TID-set dùng chung cho cả 3 thuật toán
- **19 assert** đối chiếu từng con số kỳ vọng trên ví dụ — **100% ĐẠT**
- Phủ FIM, AprioriRare, AprioriInverse, CORI & các độ đo
- {pasta, cake}: lift = 1.0, bond = 0.5 → xác nhận mẫu giả bằng số

**Nói**: 19 assert phủ toàn bộ bảng FIM, ba thuật toán và các độ đo — tất cả khớp kết quả tính tay trên ví dụ minh họa. *(1:00)*

## Slide 15 — Exp A: cái giá của việc đi xuyên vùng phổ biến

- **Hình**: `mushroom_runtime.png` (≥60% slide)
- UCI Mushroom: 8 124 giao dịch, 118 item, dày
- minsup 0.6 → 0.2: #frequent tăng **~890×** (51 → 45 391)
- #mRI chỉ tăng **~8×** (122 → 986)

**Nói**: mRI là biểu diễn gọn, nhưng chi phí bị chi phối bởi vùng phổ biến — đúng như lý thuyết slide AprioriRare dự báo. *(1:00)*

## Slide 16 — Exp B & C: PRI rẻ, CORI giàu ngữ nghĩa

- **Hình**: `mushroom_experiments.png` (≥60% slide)
- AprioriInverse: **mili-giây** — alphabet hiếm rất nhỏ (không phải benchmark cùng điều kiện)
- CORI: kết quả **bão hòa** 90–104 mẫu khi nới minbond 0.95 → 0.5
- Mẫu kể chuyện: {odor=m, ring…} sup = 36 (0.44%), **bond = 1.0**

**Nói**: Mẫu bond = 1 trên Mushroom: 36 cây nấm mùi mốc *luôn* đồng thời không vòng cuống + cuống màu quế — loại tri thức FIM không bao giờ chạm tới. *(1:15)*

## Slide 17 — Kết luận: ba đánh đổi

- **mRI gọn nhưng đắt** — phải duyệt toàn vùng phổ biến
- **PRI rẻ nhưng hẹp** — bỏ sót mẫu lai
- **CORI cân bằng** — ràng buộc kép, kết quả nhỏ & giàu ngữ nghĩa
- Hướng 2021–2026: metaheuristic (MRI-CE), fuzzy, utility, **privacy**

**Nói**: Thông điệp mang về: không có định nghĩa hiếm "đúng" duy nhất — chỉ có đánh đổi; null-invariance là bắt buộc với dữ liệu thưa. *(0:50)*

## Slide 18 — Cảm ơn & Hỏi đáp

- Tóm tắt 1 dòng: 3 định nghĩa · 3 thuật toán · kiểm chứng 100% · Mushroom
- Mã nguồn & kết quả: `advantage_data_mining/code`, `results/`
- **Xin cảm ơn — mời thầy/cô và các bạn đặt câu hỏi**

**Nói**: Cảm ơn, mời câu hỏi. *(0:20)*
