# Kết quả thực nghiệm trên UCI Mushroom

## Thống kê dữ liệu

- Số giao dịch: **8124**
- Số item phân biệt (thuộc_tính=giá_trị): **118**
- Độ dài giao dịch trung bình: **22.69**

## Exp A — AprioriRare

| minsup (tỉ lệ) | minsup (abs) | #Frequent | #mRI | Thời gian (s) |
|---|---|---|---|---|
| 0.6 | 4874 | 51 | 122 | 0.005 |
| 0.5 | 4062 | 153 | 153 | 0.013 |
| 0.4 | 3249 | 565 | 258 | 0.043 |
| 0.3 | 2437 | 2733 | 389 | 0.197 |
| 0.25 | 2031 | 5511 | 623 | 0.411 |
| 0.2 | 1624 | 45391 | 986 | 2.912 |

## Exp B — AprioriInverse

| minsup | maxsup | #PRI | Kích thước max | Thời gian (s) |
|---|---|---|---|---|
| 0.01 | 0.05 | 71 | 4 | 0.001 |
| 0.02 | 0.05 | 22 | 3 | 0.001 |
| 0.01 | 0.1 | 153 | 4 | 0.004 |
| 0.02 | 0.1 | 52 | 3 | 0.003 |
| 0.05 | 0.1 | 17 | 1 | 0.001 |
| 0.01 | 0.2 | 533 | 5 | 0.012 |
| 0.02 | 0.2 | 189 | 4 | 0.009 |
| 0.05 | 0.2 | 46 | 2 | 0.004 |

## Exp C — CORI (maxsup = 0.1, max_size = 4)

| minbond | #Rare correlated | Kích thước max | Thời gian (s) |
|---|---|---|---|
| 0.95 | 90 | 4 | 0.544 |
| 0.9 | 93 | 4 | 0.538 |
| 0.8 | 93 | 4 | 0.549 |
| 0.7 | 93 | 4 | 0.719 |
| 0.6 | 94 | 4 | 0.731 |
| 0.5 | 104 | 4 | 0.969 |

## 10 mẫu hiếm tương quan tiêu biểu (|X| ≥ 2, minbond = 0.9)

| Itemset | sup | bond |
|---|---|---|
| {stalk-color-above-ring=y, veil-color=y} | 8 | 1.000 |
| {odor=m, ring-number=n} | 36 | 1.000 |
| {odor=m, ring-number=n, ring-type=n} | 36 | 1.000 |
| {odor=m, ring-number=n, ring-type=n, stalk-color-above-ring=c} | 36 | 1.000 |
| {odor=m, ring-number=n, ring-type=n, stalk-color-below-ring=c} | 36 | 1.000 |
| {odor=m, ring-number=n, stalk-color-above-ring=c} | 36 | 1.000 |
| {odor=m, ring-number=n, stalk-color-above-ring=c, stalk-color-below-ring=c} | 36 | 1.000 |
| {odor=m, ring-number=n, stalk-color-below-ring=c} | 36 | 1.000 |
| {odor=m, ring-type=n} | 36 | 1.000 |
| {odor=m, ring-type=n, stalk-color-above-ring=c} | 36 | 1.000 |
