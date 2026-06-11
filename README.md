# Bài tập lớn — Khai thác các mẫu hiếm (Rare Pattern Mining)

Môn: Khai thác dữ liệu nâng cao. Dựa trên slide
`AdvancedDataMining_02_RareItemset Techniques.pdf`.

## Cấu trúc

```
advantage_data_mining/
├── bao_cao_rare_pattern_mining.md   # Báo cáo chính (tiếng Việt)
├── research/                        # Stage 1 — nghiên cứu
│   ├── 01_rq_brief.md               #   câu hỏi nghiên cứu, phạm vi, phương pháp
│   ├── 02_bibliography.md           #   22 nguồn đã xác minh DOI (CrossRef/OpenAlex)
│   └── 03_synthesis.md              #   tổng hợp tài liệu
├── code/
│   ├── rare_mining.py               # AprioriRare, AprioriInverse, CORI, bond, allconf…
│   └── run_experiments.py           # sanity check (assert với slide) + UCI Mushroom
├── data/
│   └── agaricus-lepiota.data        # UCI Mushroom (8124 giao dịch)
└── results/                         # sanity_check.md, bảng CSV/MD, hình PNG
```

## Chạy lại thực nghiệm

```bash
cd code && python3 run_experiments.py
```
