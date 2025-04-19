# 📝 CHANGELOG - AI Agent 学习日志项目

## 📅 2025-04-16 - Day 4
- 🔁 增加 `/rebuild` 接口用于热重建向量索引
- 📄 支持多文档 `.txt/.md` 自动嵌入与段落切分
- 🧠 打印用户提问 + 检索段落日志，方便调试
- ⚙️ 添加 `config.py` 管理模型路径、数据路径、接口配置
- ✅ 索引文件与段落原文保存至本地 `data/`，可持久化加载
- 🧪 项目结构全面模块化，适配后续 UI / 多轮问答扩展

## 📅 2025-04-15 - Day 3
- 🚀 构建第一个 RAG 问答 API，基于 FastAPI + Ollama 本地模型
- 🧩 完成段落向量生成、FAISS 建库、拼接 prompt 并调用 llama3
- ✅ 成功接通本地大模型推理流程，问答逻辑可用
- 📂 开始模块拆分为 `rag_utils.py` + `rag_api.py`
- 🧪 使用 `curl` 和 Swagger 文档测试 API

## 📅 2025-04-14 - Day 2
- 📄 编写嵌入脚本，将 sample.txt 切分段落并嵌入向量
- 💾 构建 FAISS 向量数据库并实现向量搜索匹配
- 🔍 实现根据问题查找 Top-K 段落的语义检索功能
- 🤖 拼接 prompt 并发送给本地 llama3 模型回答
- ✅ 成功完成第一个 Retrieval + Generate 的 RAG 流程

## 📅 2025-04-13 - Day 1
- ✅ 完成环境配置，成功运行 Ollama + LLaMA3 本地模型
- 🛠️ 创建 Python 脚本 `chat_local_llm.py` 调用模型
- 🔗 成功连接 Ollama API：`http://localhost:11434/api/generate`
- 🔄 提交第一份 Git commit 并推送至 GitHub 仓库
