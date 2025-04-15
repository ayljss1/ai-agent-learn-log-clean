# 📘 Day 3：构建本地 RAG 问答 API（FastAPI + Ollama）

## ✅ 今天完成的内容

- 新建 `day03/` 文件夹用于封装 RAG 问答服务
- 编写 `rag_utils.py`：
  - 封装了加载段落、向量化、向量搜索、构建 prompt 的函数
- 编写 `rag_api.py`：
  - 用 FastAPI 构建了 POST 接口 `/ask`，接收用户提问
  - 接口会自动调用 embedding + FAISS 检索 + 拼接 prompt 并请求本地 llama3 模型
- 使用 Swagger 页面成功访问 API
- 编写 `sample.json`，并通过 `curl` 成功测试 API 调用
- 完成了一个可运行的本地文档问答系统（RAG 全流程）

---

## 🌐 FastAPI 使用步骤

1. 启动服务（需在 day03/ 目录下）

```bash
uvicorn rag_api:app --reload

2. 打开浏览器访问：

bash

http://localhost:8000/docs

3.展开 /ask 接口，点击 Try it out

4.在 JSON 输入框中输入问题，例如：

json

{
  "question": "什么是向量数据库？"
}

5.点击 Execute，查看模型返回的答案

🧪 用 curl 测试接口（可选）

curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d @sample.json
确保你当前位于 sample.json 所在目录（如 day03/）

🔁 模型接口说明（Ollama）
使用的模型服务为本地启动的 llama3：

bash

ollama run llama3
FastAPI 会向该地址发送请求：

bash

http://localhost:11434/api/generate