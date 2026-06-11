# Danh mục tài liệu đã xác minh — Rare Pattern Mining

> **Stage 1 — RESEARCH.** Mọi mục dưới đây đã được xác minh qua **CrossRef API / OpenAlex API**
> ngày 2026-06-11 (metadata: tác giả, năm, venue, DOI). Cột **Hạng** ghi xếp hạng venue
> (Q-rank SCIE/Scopus hoặc CORE rank); hạng đánh dấu `*` là theo tri thức phổ biến về venue,
> chưa tra trực tiếp từ cổng xếp hạng — sẽ rà lại ở Stage 2.5 (INTEGRITY).
> Cờ `[SEMINAL — định nghĩa]`: nguồn > 5 năm, **chỉ** được trích cho định nghĩa gốc
> khái niệm/thuật toán, không dùng làm bằng chứng hiện trạng nghiên cứu.

## A. Nguồn nền tảng (SEMINAL — chỉ dùng cho định nghĩa)

| # | Tài liệu | Năm | Loại nguồn | Hạng | DOI / URL | Cờ |
|---|----------|-----|-----------|------|-----------|-----|
| S1 | Agrawal, R., Srikant, R. *Fast Algorithms for Mining Association Rules in Large Databases.* Proc. VLDB 1994, 487–499. | 1994 | Hội nghị (VLDB) | CORE A* | Không có DOI (kỷ yếu VLDB '94); bản gốc: https://www.vldb.org/conf/1994/P487.PDF | [SEMINAL — định nghĩa Apriori/FIM] |
| S2 | Zaki, M. J. *Scalable Algorithms for Association Mining.* IEEE Transactions on Knowledge and Data Engineering 12(3), 372–390. | 2000 | Tạp chí (TKDE) | Q1 SCIE | 10.1109/69.846291 | [SEMINAL — định nghĩa Eclat/TID-list] |
| S3 | Omiecinski, E. R. *Alternative Interest Measures for Mining Associations in Databases.* IEEE Transactions on Knowledge and Data Engineering 15(1), 57–69. | 2003 | Tạp chí (TKDE) | Q1 SCIE | 10.1109/TKDE.2003.1161582 | [SEMINAL — định nghĩa bond, all-confidence] |
| S4 | Koh, Y. S., Rountree, N. *Finding Sporadic Rules Using Apriori-Inverse.* Proc. PAKDD 2005, LNCS 3518, 97–106. | 2005 | Hội nghị (PAKDD) | CORE A* | 10.1007/11430919_13 | [SEMINAL — định nghĩa perfectly rare itemset, AprioriInverse] |
| S5 | Szathmary, L., Napoli, A., Valtchev, P. *Towards Rare Itemset Mining.* Proc. 19th IEEE ICTAI 2007, 305–312. | 2007 | Hội nghị (IEEE ICTAI) | CORE B* | 10.1109/ICTAI.2007.30 | [SEMINAL — định nghĩa minimal rare itemset, AprioriRare] |
| S6 | Wu, T., Chen, Y., Han, J. *Re-examination of Interestingness Measures in Pattern Mining: A Unified Framework.* Data Mining and Knowledge Discovery 21, 371–397. | 2010 | Tạp chí (DMKD) | Q1 SCIE | 10.1007/s10618-009-0161-2 | [SEMINAL — khung thống nhất độ đo, null-invariance] |
| S7 | Bouasker, S., Ben Yahia, S. *Key Correlation Mining by Simultaneous Monotone and Anti-monotone Constraints Checking.* Proc. 30th ACM SAC 2015, 851–856. | 2015 | Hội nghị (ACM SAC) | CORE B* | 10.1145/2695664.2695802 | [SEMINAL — thuật toán CORI] |
| S8 | Koh, Y. S., Ravana, S. D. *Unsupervised Rare Pattern Mining: A Survey.* ACM Transactions on Knowledge Discovery from Data 10(4), Article 45. | 2016 | Tạp chí (ACM TKDD) | Q1 SCIE | 10.1145/2898359 | [SEMINAL — taxonomy/định nghĩa phân loại mẫu hiếm] |

## B. Nguồn ≤ 5 năm (2021–2026) — dùng cho tổng quan, so sánh, hiện trạng

| # | Tài liệu | Năm | Loại nguồn | Hạng | DOI |
|---|----------|-----|-----------|------|-----|
| R1 | Darrab, S., Broneske, D., Saake, G. *Modern Applications and Challenges for Rare Itemset Mining.* International Journal of Machine Learning and Computing 11(3), 208–218. | 2021 | Tạp chí (survey) | Scopus (đã ngừng chỉ mục từ 2021 — dùng thận trọng)* | 10.18178/ijmlc.2021.11.3.1037 |
| R2 | Cui, Y., Gan, W., Lin, H., Zheng, W. *FRI-Miner: Fuzzy Rare Itemset Mining.* Applied Intelligence 52, 3387–3402. | 2021 | Tạp chí | Q2 SCIE* | 10.1007/s10489-021-02574-1 |
| R3 | Mahdi, M. A., Hosny, K. M., El-Henawy, I. *FR-Tree: A Novel Rare Association Rule for Big Data Problem.* Expert Systems with Applications 187, 115898. | 2021 | Tạp chí | Q1 SCIE | 10.1016/j.eswa.2021.115898 |
| R4 | Datta, S., Mali, K., Ghosh, U., Bose, S., Das, S., Ghosh, S. *Rare Correlated Coherent Association Rule Mining with CLS-MMS.* The Computer Journal 66(2), 342–359 (print 2023, online 2021). | 2021 | Tạp chí | Q2/Q3 SCIE* | 10.1093/comjnl/bxab164 |
| R5 | Hu, K., Qiu, L., Zhang, S., Wang, Z., Fang, N. *An Incremental Rare Association Rule Mining Approach with a Life Cycle Tree Structure Considering Time-Sensitive Data.* Applied Intelligence 53, 9442–9466. | 2022 | Tạp chí | Q2 SCIE* | 10.1007/s10489-022-03978-3 |
| R6 | Akdaş, D. N., Birant, D., Yıldırım Taşer, P. *ERIM: An Ensemble of Rare Itemset Mining and Its Application in the Automotive Industry.* Expert Systems 41(6), e13122 (print 2024, online 2022). | 2022 | Tạp chí | Q2/Q3 SCIE* | 10.1111/exsy.13122 |
| R7 | Zhang, P., Chen, J., Wan, S., Gan, W. *Targeted Mining of Rare High-Utility Patterns.* Proc. IEEE International Conference on Big Data 2022, 6271–6280. | 2022 | Hội nghị (IEEE BigData) | CORE B* | 10.1109/BigData55660.2022.10020226 |
| R8 | Li, Y., Cai, S. *Detecting Outliers in Data Streams Based on Minimum Rare Pattern Mining and Pattern Matching.* Information Technology and Control 51(2), 268–282. | 2022 | Tạp chí | Q3/Q4 SCIE* | 10.5755/j01.itc.51.2.30524 |
| R9 | Biswas, S., Saha, D., Pandit, R. *A State-of-the-Art Association Rule Mining Survey and Its Rare Application, Challenges.* International Journal on Artificial Intelligence Tools 32(6). | 2022 | Tạp chí (survey) | Q4 SCIE* | 10.1142/S0218213023500215 |
| R10 | Capillar, E., Ishmam, C. A. M., Leung, C. K., Pazdor, A. G. M., et al. *Bitwise Vertical Mining of Minimal Rare Patterns.* Proc. DaWaK 2023, LNCS 14148, 197–213. | 2023 | Hội nghị (DaWaK) | CORE B* | 10.1007/978-3-031-39831-5_13 |
| R11 | Gui, Y., Gan, W., Wu, Y., Yu, P. S. *Privacy Preserving Rare Itemset Mining.* Information Sciences 662, 120262. | 2024 | Tạp chí | Q1 SCIE | 10.1016/j.ins.2024.120262 |
| R12 | Song, W., Sun, Z., Fournier-Viger, P., Wu, Y. *MRI-CE: Minimal Rare Itemset Discovery Using the Cross-Entropy Method.* Information Sciences 670, 120392. | 2024 | Tạp chí | Q1 SCIE | 10.1016/j.ins.2024.120392 |
| R13 | Darrab, S., Broneske, D., Saake, G. *Exploring the Predictive Factors of Heart Disease Using Rare Association Rule Mining.* Scientific Reports 14, 18178. | 2024 | Tạp chí | Q1 SCIE | 10.1038/s41598-024-69071-6 |
| R14 | Chen, C.-M., Li, W., Lv, J., Kumari, S. *Rare yet Critical: Algorithms for Privacy Preserving Rare Itemset Mining.* Information Sciences (in press, available online 2025), 122572. | 2025 | Tạp chí | Q1 SCIE | 10.1016/j.ins.2025.122572 |

## C. Ghi chú tuân thủ Chính sách trích dẫn

- **Độ mới:** 14/22 nguồn thuộc giai đoạn 2021–2026 — dùng cho tổng quan/so sánh/hiện trạng.
  8 nguồn seminal chỉ dùng cho định nghĩa gốc, có gắn cờ.
- **Cấp học thuật:** toàn bộ là tạp chí peer-reviewed có chỉ mục hoặc kỷ yếu hội nghị
  quốc tế (IEEE/ACM/Springer). Không có blog/Wikipedia/nguồn phổ thông.
- **Xác minh:** 21/22 mục có DOI xác minh qua API; S1 (VLDB 1994) không có DOI
  (đặc thù kỷ yếu VLDB thời kỳ đó) — đã ghi URL bản gốc chính thức.
- **Mục cần rà lại ở Stage 2.5:** các hạng đánh dấu `*`; tình trạng chỉ mục Scopus của
  IJMLC (R1) — nếu không đạt, hạ vai trò R1 xuống nguồn phụ và thay bằng R9/S8 cho các
  nhận định tổng quan.
