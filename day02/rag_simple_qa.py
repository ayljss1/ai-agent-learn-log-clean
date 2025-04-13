# rag_simple_qa.py
import faiss
import requests
from sentence_transformers import SentenceTransformer

# 1. 加载段落
with open("data/sample.txt", "r", encoding="utf-8") as f:
    text = f.read()
paragraphs = [p.strip() for p in text.split("。") if p.strip()]

# 2. 加载向量库
index = faiss.read_index("day02/faiss_index.idx")

# 3. 加载嵌入模型
model = SentenceTransformer("all-MiniLM-L6-v2")

# 4. 用户输入问题
question = input("请输入你的问题：")
query_vec = model.encode([question])

# 5. 向量搜索
top_k = 3
D, I = index.search(query_vec, top_k)

# 6. 构造上下文
retrieved_context = "\n".join([paragraphs[idx] for idx in I[0]])

# 7. 拼接 prompt
prompt = f"""你是一个专业的文档问答助手，请根据以下内容回答用户问题。

【文档内容】
{retrieved_context}

【用户问题】
{question}

【回答】
"""
print(prompt)
# 8. 调用本地 LLM (Ollama)
response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "llama3", 
          "prompt": prompt, 
          "stream": False
    }
)

answer = response.json()["response"]
print("\n🤖 回答：\n", answer)
