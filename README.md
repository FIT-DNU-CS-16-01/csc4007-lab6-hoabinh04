# Lab 6 - CineSense Prompt Engineering on IMDB

## Giới thiệu
Lab 6 dùng LLM để phân loại sentiment review phim IMDB và đánh giá độ tin cậy của prompt bằng vòng lặp: **prompt → chạy thử → đo lường → phân tích lỗi → cải tiến prompt**.

## LLM setup
- Provider: Ollama (local HTTP)
- Model: qwen2.5:7b
- Temperature: 0.0
- Test set size: 20 reviews
- Run date: 2026-06-03 17:33:43
- Lưu ý chạy thủ công: Không có. Kết quả được lấy từ các file CSV sinh sẵn trong `outputs/`.

## Prompt versions
- prompt_v1.txt: baseline prompt (`prompts/prompt_v1.txt`)
- prompt_v2.txt: improved prompt sau phân tích lỗi (`prompts/prompt_template_v2.txt`)

## Dữ liệu & output chính
- Kết quả prompt v1: `outputs/result_v1_ollama.csv`
- Kết quả prompt v2: `outputs/result_v2.csv`

## Kết quả chính (main finding)
- Prompt v2 cải thiện sentiment accuracy so với prompt v1.
- Valid JSON rate: v1 = 1.00, v2 = 1.00.
- Sentiment accuracy: v1 = 0.75, v2 = 0.90.

## Tài liệu/biểu mẫu liên quan
- Error buckets (Prompt v1): `analysis/error_buckets.md`
- Metric comparison (v2 vs v1): `analysis/prompt_v2_vs_v1_metrics.md`
- So sánh Lab 1–Lab 5 và đặt Lab 6 vào mạch học: `analysis/lab6_ngay_2_13_compare_lab1_5.md`


