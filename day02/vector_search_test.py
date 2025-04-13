import faiss
from sentence_transformers import SentenceTransformer
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(project_root, "data/sample.txt")

# 1. 加载段落
with open(data_path, "r", encoding="utf-8") as f:
    text = f.read()
paragraphs = [p.strip() for p in text.split("。") if p.strip()]

# 2. 加载 FAISS 向量库
index = faiss.read_index("day02/faiss_index.idx")

# 3. 加载模型
model = SentenceTransformer("all-MiniLM-L6-v2")

# 4. 输入问题
query = input("请输入你的问题：")
query_embedding = model.encode([query])

# 5. 向量搜索
k = 3
distances, indices = index.search(query_embedding, k)

# 6. 输出最相关段落
print("\n📚 与问题最相关的段落：")
for i, idx in enumerate(indices[0]):
    print(f"Top {i+1}: {paragraphs[idx]}  (距离: {distances[0][i]:.4f})")
