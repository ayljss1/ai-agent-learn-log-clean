import re
from sentence_transformers import SentenceTransformer
import faiss
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(project_root, "data/sample.txt")

# 1. 读取文本
with open(data_path, "r", encoding="utf-8") as f:
    text = f.read()
print("原始文本内容：", repr(text))

# 2. 切分段落（更通用）
paragraphs = [p.strip() for p in re.split(r'[。.!?]', text) if p.strip()]
print("段落列表：", paragraphs)

# 3. 向量化
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(paragraphs)

# 4. 构建向量库
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# ✅ 5. 保存向量库
index_path = os.path.join(project_root, "day02/faiss_index.idx")
faiss.write_index(index, index_path)
print(f"✅ 向量库已保存到 {index_path}")