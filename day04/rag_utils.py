# rag_utils.py（Day 4 加强版）

import re
import os
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from config import TEXT_EXTENSIONS

# 读取单个文件并分段
def load_paragraphs_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return [p.strip() for p in re.split(r"[\n\u3002.!?]", text) if p.strip()]

# 批量读取目录下所有 .txt/.md 文件
def load_all_paragraphs_from_folder(folder_path):
    all_paragraphs = []
    for fname in os.listdir(folder_path):
        if any(fname.endswith(ext) for ext in TEXT_EXTENSIONS):
            all_paragraphs += load_paragraphs_from_file(os.path.join(folder_path, fname))
    return all_paragraphs

# 向量化
def embed_paragraphs(model, paragraphs):
    return model.encode(paragraphs)

# FAISS 构建 + 保存
def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index

def save_faiss_index(index, path):
    faiss.write_index(index, path)

def load_faiss_index(path):
    return faiss.read_index(path)

# 段落元数据保存 (JSON)
def save_paragraphs(paragraphs, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(paragraphs, f, ensure_ascii=False, indent=2)

def load_paragraphs_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# FAISS 搜索
def search_similar(index, query_vector, top_k=3):
    distances, indices = index.search(query_vector, top_k)
    return distances[0], indices[0]

# prompt 构造
def build_prompt(top_paragraphs, question):
    context = "\n".join(f"- {p}" for p in top_paragraphs)
    return f"""你是一个专业的文档问答助手，请根据以下内容回答问题：\n\n{context}\n\n问题：{question}\n回答："""
