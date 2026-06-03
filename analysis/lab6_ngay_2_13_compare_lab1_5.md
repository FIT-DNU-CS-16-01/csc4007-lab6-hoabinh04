# 2.13 So sánh LLM prompting với các mô hình Lab 1–Lab 5 (gợi ý)

## Bảng tổng hợp ngắn

| Cách tiếp cận | Đầu vào | Có huấn luyện trong lab? | Nhận xét |
|---|---|---:|---|
| LogReg / SVM (TF‑IDF) | Bag-of-words / TF‑IDF | Có (training trên train split) | Baseline nhanh, dễ giải thích theo trọng số từ khóa. |
| RNN / LSTM / GRU | Chuỗi token | Có | Học thứ tự từ tốt hơn TF‑IDF, nhưng phụ thuộc huấn luyện, dễ khó tối ưu. |
| Transformer fine-tuning | Tokenized input | Có | Mạnh hơn nhờ pretraining + fine-tune; hiệu quả cao nhưng tốn tài nguyên và dễ overfit nếu dữ liệu ít. |
| LLM prompting | Prompt + review text (zero/few-shot) | Không (thường) | Linh hoạt trong việc tạo giải thích/evidence; cần kiểm soát lỗi (format, hallucination) và đánh giá độ tin cậy. |

## Nhận xét (7–10 dòng)
- LLM prompting cho ưu điểm so với classifier truyền thống ở chỗ: nó có thể **tạo cấu trúc output** (sentiment, aspects, evidence) và **giải thích kèm dẫn chứng** từ văn bản đầu vào.
- Khi được ràng buộc đúng prompt, LLM giúp nhóm lỗi rõ ràng hơn: bỏ sót cue, mâu thuẫn sentiment, hoặc trích evidence không khớp.
- Rủi ro lớn là LLM có thể **hallucinate evidence**, suy diễn ngoài review, hoặc trả **JSON sai format**; nếu không có kiểm tra/đánh giá thì hệ thống dễ mất tin cậy.
- Nếu mục tiêu chỉ là dự đoán nhãn nhanh với dữ liệu dồi dào và yêu cầu ổn định, **model đã train/fine-tune** (Lab 3–5) thường đáng tin hơn vì ít “biến thiên” output.
- LLM prompting phù hợp khi bạn cần **tính diễn giải**, trích dẫn bằng chứng, hoặc muốn nhanh chóng thử nhiều chiến lược prompt cho các test case khó.
- Với IMDB, LLM có thể giúp hiểu lỗi bằng cách chỉ ra evidence/nhãn quan hệ với nội dung, từ đó cải tiến prompt (như tăng ràng buộc evidence exactness).
- Tuy vậy, IMDB có nhiều đoạn mơ hồ/ẩn dụ, nên LLM vẫn cần rubric + error buckets để biết khi nào nó “đáng tin” và khi nào nên fallback sang mô hình train sẵn.

