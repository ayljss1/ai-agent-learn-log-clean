初次启动 → 嵌入 + 保存索引 → 保存段落 → serve
下次启动 → 加载索引 + 段落 → serve

day4项目结构和说明
day04/
├── rag_utils.py          # 加强版工具模块
├── rag_api.py            # 启动前检查并加载缓存
├── config.py             # 可选配置集中管理
├── sample.json
└── README.md

✅ 今日完成内容概览
将数据处理、模型路径、索引路径集中到 config.py

对 rag_utils.py 添加多文档读取、向量保存、索引加载等函数

对 rag_api.py 进行结构优化，实现：

启动时判断是否加载已有索引或重新生成

日志打印加载段落总数

日志打印用户提问和被检索段落

加入 /rebuild 接口强制重建 FAISS 索引

在 data/ 中添加多个 .txt 文档，覆盖 AI、Embedding、LLM 等主题

支持自动读取多个文档、热重载、不重启服务即可更新问答内容

🔧 技术细节优化

项目	优化说明
配置管理	config.py 中统一管理路径和模型名
多文档支持	加入 load_all_paragraphs_from_folder() 实现多文件处理
索引管理	支持 .index 文件保存与加载，避免重复向量化
快速重建	新增 /rebuild 接口，无需重启即可热更新
Debug 日志	控制台打印提问、检索段落、加载数量等信息
🌐 接口说明
POST /ask
发送 JSON 问题，获取基于文档的回答：

json
{
  "question": "什么是向量数据库？"
}
POST /rebuild
强制重新构建 FAISS 索引，用于新增或更新 data/ 下的文档。

响应：

json
{
  "message": "索引已成功重建，段落数量：12"
}