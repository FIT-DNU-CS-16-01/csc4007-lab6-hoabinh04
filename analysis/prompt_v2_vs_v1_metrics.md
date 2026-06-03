# 2.12 Prompt v2 vs Prompt v1 — Metric comparison

## Dữ liệu đầu vào
- Prompt v1: `outputs/result_v1_ollama.csv`
- Prompt v2: `outputs/result_v2_ollama.csv`

## Tổng quan metrics (Ollama)
Tính từ 20 review (valid_json = 1 cho cả hai):

| Metric | Prompt v1 | Prompt v2 |
|---|---:|---:|
| Sentiment accuracy (`gold_sentiment` == `llm_sentiment`) | 0.75 | 0.90 |
| Valid JSON rate (`valid_json`) | 1.00 | 1.00 |
| #samples | 20 | 20 |

## Nhận xét nhanh
- Prompt v2 cải thiện sentiment accuracy đáng kể: **+0.15** (0.75 → 0.90), trong khi cả hai đều giữ tỷ lệ JSON hợp lệ **100%**.
- V2 (theo format prompt template v2) có xu hướng trả `aspects`/`confidence` rõ ràng hơn, giúp giảm các lỗi “định dạng” và tăng ổn định ra nhãn sentiment.

## Gợi ý cho phần Error analysis tiếp theo
Với accuracy v2 cao hơn, các lỗi còn lại thường sẽ nằm ở:
- các review “mơ hồ/đa nghĩa” (dễ bị lệch sang polarity sai);
- evidence không khớp hoàn toàn với review (đặc biệt khi LLM paraphrase hoặc tự suy diễn).

