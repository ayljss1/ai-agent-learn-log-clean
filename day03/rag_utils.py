import re
from sentence_transformers import SentenceTransformer
import faiss

# 1. 文本读取与分段
def load_paragraphs(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    paragraphs = [p.strip() for p in re.split(r"[。！？.!?]", text) if p.strip()]
    return paragraphs

# 2. 嵌入段落并构建向量库
def embed_paragraphs(model, paragraphs):
    embeddings = model.encode(paragraphs)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index, embeddings

# 3. 搜索相似段落（返回 index 和距离）
def search_similar(index, query_vector, top_k=3):
    distances, indices = index.search(query_vector, top_k)
    return distances[0], indices[0]

# 4. 构建 prompt 给 LLM 用
def build_prompt(top_paragraphs, question):
    context = "\n".join(f"- {p}" for p in top_paragraphs)
    prompt = f"""你是一个专业的文档问答助手，请根据以下段落内容回答问题：

{context}

问题：{question}
请用简洁、通俗的语言回答。
"""
    return prompt
