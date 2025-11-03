# RAG_iPhone

## 简介（中文）
这是一个基于本地 embedding 与本地 LLM 的 RAG（Retrieval-Augmented Generation）示例项目，目标是对爬取的手机商品数据（`merged.json`）建立向量索引（PGVector），并通过检索+生成的方式回答问题。

## Description (English)
This is a small RAG (Retrieval-Augmented Generation) demo that uses locally computed embeddings and a local LLM. It builds a vector index (PGVector) from scraped phone product data (`merged.json`) and answers questions by retrieving related documents and generating answers.

---

## 文件说明 / Files

- `merged.json` — 爬取并整理的商品数据（JSON 数组）。
- `Rag_inst.py` — 将 `merged.json` 中的商品文本构造成 `Document` 并写入 PGVector 向量集合的脚本（用于向量索引构建/更新）。
- `answer.py` — 基于 LangChain 的 RetrievalQA 示例，使用本地 Ollama 模型（通过 `ChatOllama`）和 PGVector 检索器做问答并返回来源文档。

---

## 依赖 / Requirements

观测到的主要依赖：

- Python 3.10+
- PostgreSQL（需要 pgvector 扩展）
- Python 包：`langchain`, `langchain_community`, `langchain_ollama`, `psycopg2-binary`, `sentence-transformers` / `transformers`（用于本地 embedding）

建议安装命令（示例）：

```bash
# 在 macOS / zsh 下示例
python -m pip install --upgrade pip
python -m pip install langchain langchain_community langchain_ollama psycopg2-binary sentence-transformers
```

如果你用 virtualenv / venv，请先创建并激活环境。

---

## 数据库与 pgvector

脚本中使用的连接字符串示例：

```python
CONNECTION_STRING = "postgresql+psycopg2://admin:admin123@localhost:5432/vectordb"
COLLECTION_NAME = "products"
```

你需要在 PostgreSQL 中创建数据库并启用 pgvector：

```sql
-- 在 psql 中
CREATE DATABASE vectordb;
\c vectordb
CREATE EXTENSION IF NOT EXISTS vector;
```

（如果使用托管服务或不同用户名/密码，请相应修改脚本中的连接字符串或把连接信息放到环境变量中。）

---

## 使用方法 / Usage

1) 构建向量索引（把 `merged.json` 写入 PGVector）

```bash
python Rag_inst.py
```

该脚本会：
- 从 `merged.json` 读取商品条目
- 用 `HuggingFaceEmbeddings`（代码里是 `BAAI/bge-large-en-v1.5`）生成 embedding
- 用 `PGVector.from_documents(...)` 将文档写入名为 `products` 的集合

2) 运行问答示例

```bash
python answer.py
```

`answer.py` 会：
- 使用相同的 embedding 与 PGVector 检索器构建 retriever
- 使用 `ChatOllama`（本地 Ollama）作为 LLM（示例模型 `gpt-oss:20b`）
- 调用 `RetrievalQA` 执行检索与生成，并打印回答与来源文档

注意：运行 `answer.py` 前请确保：
- PostgreSQL + pgvector 可用，且集合已写入（已运行 `Rag_inst.py`）
- 本地 Ollama 服务可用（或将 `ChatOllama` 的模型名替换为你可用的模型）

---

## 配置要点 / Configuration highlights

- 在两个脚本中，修改 `CONNECTION_STRING` 与 `COLLECTION_NAME` 来匹配你的数据库环境。
- Embedding 模型名可在 `HuggingFaceEmbeddings(model_name=...)` 中更改；若内存/显存不足，可换成更小的 embedding 模型。
- LLM 模型在 `ChatOllama(model=...)` 中配置，或替换为你自己的 LLM 接入方式（API Key / 本地服务）。

---

## 注意事项 / Notes

- `merged.json` 看起来是从公开零售页面爬取的产品描述（包含规格与功能点）。在公开或商业化使用这些数据前，请确认数据来源与版权许可。
- 切勿在代码中硬编码生产数据库凭据。建议使用环境变量或机密管理工具。
- 如果本地 embedding 模型或 Ollama 模型需要大量显存/磁盘资源，请在有足够资源的机器上运行或使用小模型调试。

---

## 贡献 / Contributing

欢迎提交 issues 或 PR：

- 如果希望我为仓库补充 `requirements.txt`、`.env.example` 或演示 notebook，我可以帮你添加。

---

## 联系 / Contact

作者仓库：请在该仓库打开 issue 或直接通过 Git 提交 PR。

---

## 完成情况 / What I added

已生成本文件 `README.md`，包含中英文对照的项目说明与使用步骤。如需更改译文风格（并列对照表格或两栏展示），或需要我顺手添加 `requirements.txt` / 简单示例 notebook，请告诉我。
