# Lab 5 Recap
- Model used: `distilbert-base-uncased` (Full fine-tuning)
- Tokenizer/max_length: 256
- Test accuracy: 0.9095
- Test macro-F1: 0.9095
- Typical errors:
1. Mixed sentiment (Nửa khen nửa chê làm mô hình bối rối, ví dụ khen diễn viên nhưng chê kịch bản).
2. Sarcasm / Mỉa mai (Dùng từ tiêu cực cực đoan để nói đùa rồi chốt hạ khen phim).
3. Câu chốt cảm xúc nằm quá xa ở cuối câu (bị cắt mất ngữ cảnh do max_length).
4. Phủ định nhiều tầng hoặc trích dẫn lại lời của người khác (quote những nhận xét xấu).