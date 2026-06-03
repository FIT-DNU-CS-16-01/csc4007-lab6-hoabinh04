import pandas as pd
import json
import re

def extract_json(raw_text):
    try:
        # Tìm khối JSON nằm giữa cặp dấu { }
        match = re.search(r'\{.*\}', str(raw_text), re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return json.loads(str(raw_text))
    except:
        return None

# Đọc file kết quả Ollama vừa chạy
df = pd.read_csv("outputs/result_v1_ollama.csv")

parsed_data = []
invalid_json_count = 0

for idx, row in df.iterrows():
    raw_out = row.get('raw_output', '')
    js = extract_json(raw_out)
    
    if js and isinstance(js, dict):
        parsed_data.append({
            "review_id": row.get("review_id"),
            "gold_sentiment": row.get("gold_sentiment"),
            "llm_sentiment": js.get("sentiment", "N/A"),
            "llm_evidence": str(js.get("evidence", [])),
            "error_check": "Valid JSON"
        })
    else:
        invalid_json_count += 1
        parsed_data.append({
            "review_id": row.get("review_id"),
            "gold_sentiment": row.get("gold_sentiment"),
            "llm_sentiment": "ERROR",
            "llm_evidence": "[]",
            "error_check": "Invalid JSON"
        })

df_parsed = pd.DataFrame(parsed_data)
df_parsed.to_csv("outputs/result_v1_parsed.csv", index=False)
print(f"--- Đã parse xong! Số mẫu lỗi định dạng JSON: {invalid_json_count}/20 ---")