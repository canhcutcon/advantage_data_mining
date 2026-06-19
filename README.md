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

Hình thức làm và nộp bài:

- Làm tự luận ra giấy (viết tay không đánh máy) ra giấy. Chú ý, trên mỗi trang giấy ghi đầy đủ thông tin cá nhân và đánh số trang tương ứng

- Scan bài làm, đưa vào file .doc hoặc .pdf

- Nộp file lên LMS trong thời gian qui định

Database

┌─────┬───────────────┐
│ SID │ Sequence │
├─────┼───────────────┤
│ 1 │ ⟨(a b)(c)(a)⟩ │
├─────┼───────────────┤
│ 2 │ ⟨(a b)(b)(c)⟩ │
├─────┼───────────────┤
│ 3 │ ⟨(b)(c)(d)⟩ │
├─────┼───────────────┤
│ 4 │ ⟨(b)(a b)(c)⟩ │
└─────┴───────────────┘

minsup = 3 (a pattern must appear in ≥ 3 of the 4 sequences).

---

PHẦN 1 — THUẬT TOÁN GSP

▎ Cơ chế (slide GSP): Quét lần 1 tìm mẫu 1-phần tử → Lặp: Sinh ứng viên (Candidate Generation) → Cắt tỉa (Pruning) → Đếm support (Support Counting) → Loại bỏ (Elimination).

Bước 1 — Tìm mẫu độ dài 1 (quét CSDL lần 1)

Ứng viên ban đầu: ⟨a⟩, ⟨b⟩, ⟨c⟩, ⟨d⟩. Đếm support (chuỗi nào chứa item):

┌──────────┬─────┬─────┬─────┬─────┬─────┬───────────┐
│ Ứng viên │ S₁ │ S₂ │ S₃ │ S₄ │ sup │ Kết luận │
├──────────┼─────┼─────┼─────┼─────┼─────┼───────────┤
│ ⟨a⟩ │ ✓ │ ✓ │ ✗ │ ✓ │ 3 │ ≥3 ✓ │
├──────────┼─────┼─────┼─────┼─────┼─────┼───────────┤
│ ⟨b⟩ │ ✓ │ ✓ │ ✓ │ ✓ │ 4 │ ≥3 ✓ │
├──────────┼─────┼─────┼─────┼─────┼─────┼───────────┤
│ ⟨c⟩ │ ✓ │ ✓ │ ✓ │ ✓ │ 4 │ ≥3 ✓ │
├──────────┼─────┼─────┼─────┼─────┼─────┼───────────┤
│ ⟨d⟩ │ ✗ │ ✗ │ ✓ │ ✗ │ 1 │ <3 ✗ loại │
└──────────┴─────┴─────┴─────┴─────┴─────┴───────────┘

F₁ = { ⟨a⟩:3, ⟨b⟩:4, ⟨c⟩:4 } (loại d theo Apriori).

Bước 2 — Sinh ứng viên độ dài 2 (C₂)

Từ F₁ = {a, b, c}, theo slide "GSP: Generating Length-2 Candidates", ứng viên gồm 2 dạng:

- Cùng itemset ⟨(x y)⟩, x<y: (ab), (ac), (bc) → 3 ứng viên
- Khác itemset ⟨(x)(y)⟩, mọi cặp có thứ tự kể cả x=y: (a)(a),(a)(b),(a)(c),(b)(a),(b)(b),(b)(c),(c)(a),(c)(b),(c)(c) → 9 ứng viên

→ Tổng 12 ứng viên. Quét CSDL đếm support (ghi rõ chuỗi thỏa):

┌──────────┬───────────────────────────────────────┬─────┬─────┐
│ Ứng viên │ Chuỗi chứa │ sup │ │
├──────────┼───────────────────────────────────────┼─────┼─────┤
│ ⟨(ab)⟩ │ S₁,S₂,S₄ │ 3 │ ✓ │
├──────────┼───────────────────────────────────────┼─────┼─────┤
│ ⟨(ac)⟩ │ — (không itemset nào chứa cả a,c) │ 0 │ ✗ │
├──────────┼───────────────────────────────────────┼─────┼─────┤
│ ⟨(bc)⟩ │ — │ 0 │ ✗ │
├──────────┼───────────────────────────────────────┼─────┼─────┤
│ ⟨(a)(a)⟩ │ S₁ (a@1→a@3) │ 1 │ ✗ │
├──────────┼───────────────────────────────────────┼─────┼─────┤
│ ⟨(a)(b)⟩ │ S₂ (a@1→b@2) │ 1 │ ✗ │
├──────────┼───────────────────────────────────────┼─────┼─────┤
│ ⟨(a)(c)⟩ │ S₁(a@1→c@2), S₂(a@1→c@3), S₄(a@2→c@3) │ 3 │ ✓ │
├──────────┼───────────────────────────────────────┼─────┼─────┤
│ ⟨(b)(a)⟩ │ S₁(b@1→a@3), S₄(b@1→a@2) │ 2 │ ✗ │
├──────────┼───────────────────────────────────────┼─────┼─────┤
│ ⟨(b)(b)⟩ │ S₂, S₄ │ 2 │ ✗ │
├──────────┼───────────────────────────────────────┼─────┼─────┤
│ ⟨(b)(c)⟩ │ S₁,S₂,S₃,S₄ │ 4 │ ✓ │
├──────────┼───────────────────────────────────────┼─────┼─────┤
│ ⟨(c)(a)⟩ │ S₁ (c@2→a@3) │ 1 │ ✗ │
├──────────┼───────────────────────────────────────┼─────┼─────┤
│ ⟨(c)(b)⟩ │ — │ 0 │ ✗ │
├──────────┼───────────────────────────────────────┼─────┼─────┤
│ ⟨(c)(c)⟩ │ — (mỗi chuỗi chỉ 1 'c') │ 0 │ ✗ │
└──────────┴───────────────────────────────────────┴─────┴─────┘

F₂ = { ⟨(ab)⟩:3, ⟨(a)(c)⟩:3, ⟨(b)(c)⟩:4 }

Bước 3 — Sinh ứng viên độ dài 3 (C₃)

▎ Luật trộn (slide Candidate Generation): w₁ trộn được với w₂ nếu bỏ event ĐẦU của w₁ = bỏ event CUỐI của w₂. Ứng viên = w₁ nối thêm event cuối của w₂ (nếu 2 event cuối của w₂ cùng itemset → gộp itemset; ngược
▎ lại → itemset mới).

Tính phần "bỏ đầu / bỏ cuối" cho từng phần tử F₂:

┌──────────┬──────────────┬───────────────┐
│ w │ bỏ event đầu │ bỏ event cuối │
├──────────┼──────────────┼───────────────┤
│ ⟨(ab)⟩ │ ⟨(b)⟩ │ ⟨(a)⟩ │
├──────────┼──────────────┼───────────────┤
│ ⟨(a)(c)⟩ │ ⟨(c)⟩ │ ⟨(a)⟩ │
├──────────┼──────────────┼───────────────┤
│ ⟨(b)(c)⟩ │ ⟨(c)⟩ │ ⟨(b)⟩ │
└──────────┴──────────────┴───────────────┘

Dò các cặp (w₁, w₂) sao cho bỏ-đầu(w₁) = bỏ-cuối(w₂):

- w₁ = ⟨(ab)⟩ → bỏ-đầu = ⟨(b)⟩. Tìm w₂ có bỏ-cuối = ⟨(b)⟩ → w₂ = ⟨(b)(c)⟩. ✔
  Trộn: nối w₁ với event cuối của w₂ là c. Trong w₂ hai event cuối (b, c) khác itemset → c thành itemset mới → ⟨(ab)(c)⟩.
- w₁ = ⟨(a)(c)⟩ → bỏ-đầu = ⟨(c)⟩: không w₂ nào có bỏ-cuối = ⟨(c)⟩ → không trộn.
- w₁ = ⟨(b)(c)⟩ → bỏ-đầu = ⟨(c)⟩: tương tự không trộn.

→ C₃ = { ⟨(ab)(c)⟩ }

Cắt tỉa (Pruning): mọi chuỗi con độ dài 2 của ⟨(ab)(c)⟩ phải ∈ F₂:

- bỏ a → ⟨(b)(c)⟩ ✓ • bỏ b → ⟨(a)(c)⟩ ✓ • bỏ c → ⟨(ab)⟩ ✓ → giữ lại.

Đếm support ⟨(ab)(c)⟩ (itemset chứa {a,b} rồi sau đó có c):

┌────────┬───────────────┬───────────────┬───────────────────┬───────────────┐
│ │ S₁ │ S₂ │ S₃ │ S₄ │
├────────┼───────────────┼───────────────┼───────────────────┼───────────────┤
│ (ab)→c │ ✓ (ab@1, c@2) │ ✓ (ab@1, c@3) │ ✗ (không có (ab)) │ ✓ (ab@2, c@3) │
└────────┴───────────────┴───────────────┴───────────────────┴───────────────┘

→ sup = 3 ✓ → F₃ = { ⟨(ab)(c)⟩:3 }

Bước 4

Chỉ còn 1 phần tử trong F₃ → không trộn được C₄ → DỪNG.

✅ Kết quả GSP (7 mẫu)

┌───────────┬─────┐
│ Mẫu │ sup │
├───────────┼─────┤
│ ⟨a⟩ │ 3 │
├───────────┼─────┤
│ ⟨b⟩ │ 4 │
├───────────┼─────┤
│ ⟨c⟩ │ 4 │
├───────────┼─────┤
│ ⟨(ab)⟩ │ 3 │
├───────────┼─────┤
│ ⟨(a)(c)⟩ │ 3 │
├───────────┼─────┤
│ ⟨(b)(c)⟩ │ 4 │
├───────────┼─────┤
│ ⟨(ab)(c)⟩ │ 3 │
└───────────┴─────┘

---

PHẦN 2 — THUẬT TOÁN PrefixSpan

▎ Cơ chế (slide The Algorithm of PrefixSpan): tìm item-1 thường xuyên → với mỗi tiền tố α, chiếu CSDL (lấy hậu tố sau lần xuất hiện đầu tiên của α) → đệ quy PrefixSpan(α, l+1, S|α).
▎ Ký hiệu \_x (slide Prefix and Suffix): item x nằm cùng itemset với item cuối của tiền tố (mở rộng itemset, tạo dạng (…x)).

Bước 1 — Mẫu độ dài 1

Quét CSDL: ⟨a⟩:3, ⟨b⟩:4, ⟨c⟩:4, ⟨d⟩:1 → giữ ⟨a⟩, ⟨b⟩, ⟨c⟩ (loại d).

Chia không gian tìm kiếm thành 3 nhánh tiền tố: ⟨a⟩, ⟨b⟩, ⟨c⟩.

---

Nhánh tiền tố ⟨a⟩

CSDL chiếu S|⟨a⟩ (hậu tố sau 'a' đầu tiên; phần còn lại trong itemset ghi bằng \_):

┌─────────────────┬────────────────┬──────────────┐
│ Chuỗi │ Vị trí 'a' đầu │ Hậu tố chiếu │
├─────────────────┼────────────────┼──────────────┤
│ S₁ ⟨(ab)(c)(a)⟩ │ trong (ab) │ ⟨(\_b)(c)(a)⟩ │
├─────────────────┼────────────────┼──────────────┤
│ S₂ ⟨(ab)(b)(c)⟩ │ trong (ab) │ ⟨(\_b)(b)(c)⟩ │
├─────────────────┼────────────────┼──────────────┤
│ S₃ │ không có a │ — (loại) │
├─────────────────┼────────────────┼──────────────┤
│ S₄ ⟨(b)(ab)(c)⟩ │ trong (ab)@2 │ ⟨(\_b)(c)⟩ │
└─────────────────┴────────────────┴──────────────┘

Đếm item trong CSDL chiếu này:

┌─────────────────────────┬────────┬─────┬────────────┐
│ Item │ Có ở │ sup │ Tạo mẫu │
├─────────────────────────┼────────┼─────┼────────────┤
│ \_b (gộp itemset → (ab)) │ cả 3 │ 3 ✓ │ ⟨(ab)⟩:3 │
├─────────────────────────┼────────┼─────┼────────────┤
│ b (itemset riêng) │ chỉ S₂ │ 1 ✗ │ │
├─────────────────────────┼────────┼─────┼────────────┤
│ c │ cả 3 │ 3 ✓ │ ⟨(a)(c)⟩:3 │
├─────────────────────────┼────────┼─────┼────────────┤
│ a │ chỉ S₁ │ 1 ✗ │ │
└─────────────────────────┴────────┴─────┴────────────┘

→ Xuất ⟨(ab)⟩:3, ⟨(a)(c)⟩:3.

Nhánh con ⟨(ab)⟩ — CSDL chiếu S|⟨(ab)⟩ (hậu tố sau itemset chứa {a,b}):

┌─────┬──────────┐
│ │ hậu tố │
├─────┼──────────┤
│ S₁ │ ⟨(c)(a)⟩ │
├─────┼──────────┤
│ S₂ │ ⟨(b)(c)⟩ │
├─────┼──────────┤
│ S₄ │ ⟨(c)⟩ │
└─────┴──────────┘

Đếm: c → 3 ✓; a→1; b→1. → Xuất ⟨(ab)(c)⟩:3.

- Chiếu tiếp S|⟨(ab)(c)⟩: {⟨(a)⟩, ⟨⟩, ⟨⟩} → a:1 → không có item ≥3 → dừng.

Nhánh con ⟨(a)(c)⟩ — chiếu S|⟨(a)(c)⟩ (từ CSDL chiếu của ⟨a⟩, lấy hậu tố sau 'c' riêng):

{⟨(a)⟩, ⟨⟩, ⟨⟩} → a:1 → không có gì ≥3 → dừng.

---

Nhánh tiền tố ⟨b⟩

CSDL chiếu S|⟨b⟩ (sau 'b' đầu tiên; trong (ab), b đứng cuối itemset nên không có item \_ theo sau):

┌─────────────────┬────────────────┬──────────────┐
│ Chuỗi │ Vị trí 'b' đầu │ Hậu tố chiếu │
├─────────────────┼────────────────┼──────────────┤
│ S₁ ⟨(ab)(c)(a)⟩ │ (ab)@1 │ ⟨(c)(a)⟩ │
├─────────────────┼────────────────┼──────────────┤
│ S₂ ⟨(ab)(b)(c)⟩ │ (ab)@1 │ ⟨(b)(c)⟩ │
├─────────────────┼────────────────┼──────────────┤
│ S₃ ⟨(b)(c)(d)⟩ │ (b)@1 │ ⟨(c)(d)⟩ │
├─────────────────┼────────────────┼──────────────┤
│ S₄ ⟨(b)(ab)(c)⟩ │ (b)@1 │ ⟨(ab)(c)⟩ │
└─────────────────┴────────────────┴──────────────┘

Đếm item:

┌──────┬─────────────┬─────┬────────────┐
│ Item │ Có ở │ sup │ │
├──────┼─────────────┼─────┼────────────┤
│ c │ S₁,S₂,S₃,S₄ │ 4 ✓ │ ⟨(b)(c)⟩:4 │
├──────┼─────────────┼─────┼────────────┤
│ a │ S₁, S₄ │ 2 ✗ │ │
├──────┼─────────────┼─────┼────────────┤
│ b │ S₂, S₄ │ 2 ✗ │ │
├──────┼─────────────┼─────┼────────────┤
│ d │ S₃ │ 1 ✗ │ │
└──────┴─────────────┴─────┴────────────┘

→ Xuất ⟨(b)(c)⟩:4.

- Chiếu tiếp S|⟨(b)(c)⟩: {⟨(a)⟩, ⟨⟩, ⟨(d)⟩, ⟨⟩} → a:1, d:1 → không gì ≥3 → dừng.

---

Nhánh tiền tố ⟨c⟩

CSDL chiếu S|⟨c⟩: S₁→⟨(a)⟩, S₂→⟨⟩, S₃→⟨(d)⟩, S₄→⟨⟩.
Đếm: a:1, d:1 → không gì ≥3 → dừng (chỉ có ⟨c⟩ độ dài 1).

✅ Kết quả PrefixSpan (7 mẫu — trùng GSP)

⟨a⟩:3, ⟨b⟩:4, ⟨c⟩:4, ⟨(ab)⟩:3, ⟨(a)(c)⟩:3, ⟨(b)(c)⟩:4, ⟨(ab)(c)⟩:3.

---

KẾT LUẬN CHUNG

Cả hai thuật toán cho cùng 7 sequential patterns với minsup = 3:

┌─────┬───────────┬─────┬───────────────────────────┐
│ # │ Mẫu │ sup │ Diễn giải │
├─────┼───────────┼─────┼───────────────────────────┤
│ 1 │ ⟨a⟩ │ 3 │ a xuất hiện ở 3 chuỗi │
├─────┼───────────┼─────┼───────────────────────────┤
│ 2 │ ⟨b⟩ │ 4 │ b ở cả 4 chuỗi │
├─────┼───────────┼─────┼───────────────────────────┤
│ 3 │ ⟨c⟩ │ 4 │ c ở cả 4 chuỗi │
├─────┼───────────┼─────┼───────────────────────────┤
│ 4 │ ⟨(ab)⟩ │ 3 │ a và b cùng một itemset │
├─────┼───────────┼─────┼───────────────────────────┤
│ 5 │ ⟨(a)(c)⟩ │ 3 │ a rồi sau đó c │
├─────┼───────────┼─────┼───────────────────────────┤
│ 6 │ ⟨(b)(c)⟩ │ 4 │ b rồi sau đó c │
├─────┼───────────┼─────┼───────────────────────────┤
│ 7 │ ⟨(ab)(c)⟩ │ 3 │ itemset (ab) rồi sau đó c │
└─────┴───────────┴─────┴───────────────────────────┘

So sánh hai cách tiếp cận (theo slide):

- GSP (Apriori-based): sinh-rồi-kiểm tra, duyệt theo chiều rộng (BFS), quét CSDL nhiều lần, sinh nhiều ứng viên — kể cả ứng viên không có trong CSDL (vd ⟨(ac)⟩, ⟨(c)(b)⟩).
- PrefixSpan (pattern-growth): chỉ xét mẫu thực sự tồn tại trong CSDL nhờ chiếu theo tiền tố, duyệt theo chiều sâu (DFS), không sinh ứng viên thừa.
  → Hai bên ra cùng kết quả là một cách kiểm tra chéo rất tốt.
