import requests
import time

prompt = "请用中文且通俗的语言解释一下什么是 Embedding。"

start_time = time.time()

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3",       # 模型名，与你用 ollama run 的一致
        "prompt": prompt,
        "stream": False
    }
)

end_time = time.time()

print("answer: \n", response.json()["response"])

# 打印耗时（单位：秒）
print(f"⏱️ 回答用时：{end_time - start_time:.2f} 秒")