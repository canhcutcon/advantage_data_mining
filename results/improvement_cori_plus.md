# Thực nghiệm cải tiến — CORI+ (cận trên all-confidence)

Kiểm chứng: với MỌI minbond khảo sát, `cori_plus` cho kết quả TRÙNG KHỚP `cori` (assert pass) — cải tiến chỉ thay đổi chi phí, không đổi kết quả.

Dữ liệu: UCI Mushroom (8124 giao dịch), maxsup = 0.1, max_size = 4. Thời gian là trung vị 5 lần chạy.

| minbond | #Kết quả | #Hợp DTID đã làm | #Hợp né được | % né | CORI (ms) | CORI+ (ms) | Tăng tốc |
|---|---|---|---|---|---|---|---|
| 0.95 | 90 | 149 | 9145 | 98.4 | 592.9 | 110.7 | x5.35 |
| 0.9 | 93 | 156 | 9383 | 98.4 | 602.9 | 111.8 | x5.39 |
| 0.8 | 93 | 170 | 9378 | 98.2 | 599.1 | 114.3 | x5.24 |
| 0.7 | 93 | 188 | 9489 | 98.1 | 617.5 | 119.7 | x5.16 |
| 0.6 | 94 | 248 | 9722 | 97.5 | 661.2 | 136.8 | x4.83 |
| 0.5 | 104 | 441 | 10939 | 96.1 | 794.7 | 189.4 | x4.2 |
