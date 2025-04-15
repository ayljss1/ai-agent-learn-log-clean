# rag_api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from rag_utils import load_paragraphs, embed_paragraphs, search_similar, build_prompt
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(project_root, "data/sample.txt")

app = FastAPI()

# 1. 初始化模型与数据
MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_MODEL = SentenceTransformer(MODEL_NAME)
DATA_PATH = data_path

# 读取段落并向量化
paragraphs = load_paragraphs(DATA_PATH)
faiss_index, embeddings = embed_paragraphs(EMBEDDING_MODEL, paragraphs)


# 2. 定义 API 输入格式
class QuestionRequest(BaseModel):
    question: str


# 3. 定义 API 路由
@app.post("/ask")
def ask_question(req: QuestionRequest):
    try:
        # 向量化用户问题
        question_vector = EMBEDDING_MODEL.encode([req.question])

        # 检索相关段落
        distances, indices = search_similar(faiss_index, question_vector, top_k=3)
        related_paragraphs = [paragraphs[idx] for idx in indices]

        # 拼接 prompt
        prompt = build_prompt(related_paragraphs, req.question)

        # 调用本地 LLM（Ollama llama3）
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
        )
        result = response.json()
        return {"answer": result["response"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
