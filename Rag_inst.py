import json
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.docstore.document import Document

# --- PostgreSQL 连接 ---
CONNECTION_STRING = "postgresql+psycopg2://admin:admin123@localhost:5432/vectordb"
COLLECTION_NAME = "products"

# --- 本地 embedding 模型 ---
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")

# --- 加载 JSON 数据 ---
with open("merged.json", "r", encoding="utf-8") as f:
    products = json.load(f)

docs = []
for p in products:
    parts = [p.get("original_name", "")]
    desc = p.get("description", {})
    if "main_description" in desc:
        parts.append(desc["main_description"])
    if "key_features" in desc:
        parts.extend(desc["key_features"])
    specs = p.get("specifications", {})
    for k, v in specs.items():
        parts.append(f"{k}: {v}")
    text = "\n".join(parts)

    docs.append(Document(
        page_content=text,
        metadata={
            "product_id": p["product_id"],
            "original_name": p["original_name"],
            "original_url": p["original_url"],
            "specifications": p["specifications"]
        }
    ))

# --- 写入 PGVector ---
vectorstore = PGVector.from_documents(
    documents=docs,
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
)

print("✅ 全部商品已用本地 embedding 写入 PGVector!")