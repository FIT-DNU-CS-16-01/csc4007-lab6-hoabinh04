import argparse
import csv
import json
import os
import time
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="Script chạy đánh giá Prompt LLM")
    parser.add_argument("--input", type=str, required=True, help="Đường dẫn file CSV testset")
    parser.add_argument("--prompt", type=str, required=True, help="Đường dẫn file text chứa prompt")
    parser.add_argument("--output", type=str, required=True, help="Đường dẫn file CSV kết quả")
    parser.add_argument("--provider", type=str, choices=["gemini", "groq", "ollama"], required=True, help="Chọn API provider")
    return parser.parse_args()

def call_gemini(prompt_text):
    import google.generativeai as genai
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Vui lòng set biến môi trường GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    # Cập nhật sang gemini-2.0-flash do 2.5-flash đã hết quota 20 lượt/ngày
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt_text)
    return response.text

def call_groq(prompt_text):
    from groq import Groq
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Vui lòng set biến môi trường GROQ_API_KEY")
    client = Groq(api_key=api_key)
    # Llama 3 8b rất nhanh trên Groq
    completion = client.chat.completions.create(
        model="llama3-8b-8192", 
        messages=[{"role": "user", "content": prompt_text}],
        temperature=0.0
    )
    return completion.choices[0].message.content

def call_ollama(prompt_text, model="qwen2.5:7b"):
    import urllib.request
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt_text,
        "stream": False,
        "options": {
            "temperature": 0.0
        }
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("response", "")
    except Exception as e:
        raise RuntimeError(f"Lỗi nối Ollama (Hãy chắc chắn Ollama đang chạy tại localhost:11434 và đã tải model {model}): {e}")

def parse_json_safely(raw_text: str):
    """Xử lý output của LLM phòng trường hợp có bọc mã Markdown ```json ... ```"""
    clean_text = raw_text.strip()
    if clean_text.startswith("```json"):
        clean_text = clean_text[7:]
    elif clean_text.startswith("```"):
        clean_text = clean_text[3:]
    if clean_text.endswith("```"):
        clean_text = clean_text[:-3]
    clean_text = clean_text.strip()
    
    try:
        return json.loads(clean_text), 1
    except json.JSONDecodeError:
        return {}, 0

def extract_pred_sentiment(parsed_output: dict) -> str:
    sentiment = parsed_output.get("sentiment", "")
    if isinstance(sentiment, str):
        sentiment = sentiment.strip().lower()
    return sentiment if sentiment in {"positive", "negative", "neutral", "mixed"} else ""

def main():
    args = parse_args()
    
    input_path = Path(args.input)
    prompt_path = Path(args.prompt)
    output_path = Path(args.output)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    prompt_template = prompt_path.read_text(encoding="utf-8")
    
    with input_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    outputs = []
    print(f"Bắt đầu chạy đánh giá bằng {args.provider.upper()}...")
    
    for idx, row in enumerate(rows):
        print(f"Đang xử lý mẫu {idx+1}/{len(rows)} - Review ID: {row['review_id']}")
        prompt = prompt_template.replace("{review_text}", row["review_text"])
        
        try:
            if args.provider == "gemini":
                llm_output = call_gemini(prompt)
                time.sleep(15) # Nghỉ 15 giây để qua mặt giới hạn 5 requests/phút của API miễn phí
            elif args.provider == "groq":
                llm_output = call_groq(prompt)
                time.sleep(1)
            elif args.provider == "ollama":
                llm_output = call_ollama(prompt)
                time.sleep(0.1)
        except Exception as e:
            print(f"Lỗi khi gọi API: {e}")
            llm_output = f'{{"error": "{str(e)}"}}'
            
        parsed_output, valid_json = parse_json_safely(llm_output)
        pred_sentiment = extract_pred_sentiment(parsed_output)
        
        # Lấy evidence ra string nếu đang là list
        evidence = parsed_output.get("evidence", "")
        if isinstance(evidence, list):
            evidence = " | ".join([str(e) for e in evidence])
            
        outputs.append({
            "review_id": row["review_id"],
            "gold_sentiment": row["gold_sentiment"],
            "llm_sentiment": pred_sentiment,
            "llm_evidence": evidence,
            "raw_output": llm_output,
            "valid_json": valid_json
        })
        
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["review_id", "gold_sentiment", "llm_sentiment", "llm_evidence", "raw_output", "valid_json"],
        )
        writer.writeheader()
        writer.writerows(outputs)
        
    print(f"\n=> Đã xử lý xong! Lưu kết quả tại: {output_path}")

if __name__ == "__main__":
    main()
    
