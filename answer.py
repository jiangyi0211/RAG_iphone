from langchain_ollama import ChatOllama
from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

# === 基本配置 ===
CONNECTION_STRING = "postgresql+psycopg2://admin:admin123@localhost:5432/vectordb"
COLLECTION_NAME = "products"

# === 加载本地 embedding 模型 ===
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")

# === 从已有集合加载 PGVector ===
vectorstore = PGVector.from_existing_index(
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
)

# === 构建检索器 ===
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# === 使用本地 gpt-oss:20b ===
llm = ChatOllama(model="gpt-oss:20b", temperature=0.3)

# === 构建 RAG 问答链 ===
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# === 示例查询 ===
query = "哪款 iPhone 17 最便宜？"
result = qa.invoke(query)

print("🔍 问题:", query)
print("💡 回答:", result["result"])
print("📂 来源:")
for doc in result["source_documents"]:
    print("-", doc.metadata["original_name"])