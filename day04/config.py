# config.py - Day 4 中央配置模块

import os

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(PROJECT_ROOT)

# 数据目录
DATA_DIR = os.path.join(PARENT_DIR, "data")
TEXT_EXTENSIONS = [".txt", ".md"]

# 文件路径
INDEX_PATH = os.path.join(DATA_DIR, "paragraphs.index")
META_PATH = os.path.join(DATA_DIR, "paragraphs.json")

# 模型配置
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
LLM_MODEL_NAME = "llama3"
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# 返回 top-k 段落
TOP_K = 3