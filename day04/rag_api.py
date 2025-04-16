# rag_api.py（Day 4 改进版 + config + rebuild 支持 + 日志）

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from config import DATA_DIR, INDEX_PATH, META_PATH, EMBEDDING_MODEL_NAME, LLM_MODEL_NAME, OLLAMA_API_URL, TOP_K
from rag_utils import (
    load_all_paragraphs_from_folder,
    embed_paragraphs,
    build_faiss_index,
    save_faiss_index,
    load_faiss_index,
    save_paragraphs,
    load_paragraphs_json,
    search_similar,
    build_prompt
)

# 应用
app = FastAPI()
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# 全局数据
index = None
paragraphs = []

def build_or_load_index(force_rebuild=False):
    global index, paragraphs
    if not force_rebuild and os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
        print("📂 正在加载已有索引...")
        index = load_faiss_index(INDEX_PATH)
        paragraphs = load_paragraphs_json(META_PATH)
    else:
        print("🔧 正在重新构建索引...")
        paragraphs = load_all_paragraphs_from_folder(DATA_DIR)
        print(f"📃 加载段落数：{len(paragraphs)}")
        embeddings = embed_paragraphs(model, paragraphs)
        index = build_faiss_index(embeddings)
        save_faiss_index(index, INDEX_PATH)
        save_paragraphs(paragraphs, META_PATH)
        print("✅ 索引构建并保存成功！")

# 初始化一次
build_or_load_index()

# 接口模型
class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask(req: QuestionRequest):
    try:
        q_vector = model.encode([req.question])
        distances, indices = search_similar(index, q_vector, top_k=TOP_K)
        top_context = [paragraphs[i] for i in indices]
        prompt = build_prompt(top_context, req.question)

        print("\n💬 提问：", req.question)
        print("📚 检索段落：")
        for i, p in enumerate(top_context):
            print(f"Top {i+1}: {p}")

        response = requests.post(OLLAMA_API_URL, json={
            "model": LLM_MODEL_NAME,
            "prompt": prompt,
            "stream": False
        })
        result = response.json()
        return {"answer": result["response"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rebuild")
def rebuild():
    try:
        build_or_load_index(force_rebuild=True)
        return {"message": f"索引已成功重建，段落数量：{len(paragraphs)}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"重建失败: {str(e)}")