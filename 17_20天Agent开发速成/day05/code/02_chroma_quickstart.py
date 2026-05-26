
# -*- coding: utf-8 -*-
"""
Day05 Code 02: Chroma 快速入门
"""

import chromadb

# ===================== 1. 初始化客户端 =====================
print("=" * 60)
print("Day05 - Chroma 快速入门")
print("=" * 60)

client = chromadb.PersistentClient(path="./chroma_db_demo")

# ===================== 2. 创建集合 =====================
collection_name = "programming_languages"

# 先删除旧集合（如果存在）
try:
    client.delete_collection(collection_name)
    print(f"\n已删除旧集合: {collection_name}")
except Exception:
    pass

collection = client.create_collection(
    name=collection_name,
    metadata={"description": "编程语言知识库"}
)

print(f"\n✅ 创建集合: {collection_name}")

# ===================== 3. 准备文档 =====================
documents = [
    "Python 是一种解释型、高级、通用的编程语言，由 Guido van Rossum 于 1991 年发布。",
    "JavaScript 主要用于网页前端开发，是 Web 的三大核心技术之一。",
    "Java 是编译型语言，运行在 JVM 上，适合企业级应用开发。",
    "Go 语言由 Google 开发，擅长高并发场景，性能优异。",
    "Rust 注重内存安全，适合系统级开发，性能接近 C++。",
    "TypeScript 是 JavaScript 的超集，提供了类型安全和更好的工具支持。"
]

metadatas = [
    {"category": "programming", "year": 1991, "author": "Guido van Rossum"},
    {"category": "programming", "year": 1995, "domain": "web"},
    {"category": "programming", "year": 1995, "domain": "enterprise"},
    {"category": "programming", "year": 2009, "domain": "concurrency"},
    {"category": "programming", "year": 2010, "domain": "system"},
    {"category": "programming", "year": 2012, "domain": "web"}
]

ids = [f"doc_{i}" for i in range(len(documents))]

# ===================== 4. 添加文档 =====================
print("\n添加文档...")
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)
print(f"✅ 添加了 {len(documents)} 个文档")

# ===================== 5. 查询 =====================
query_text = "什么语言适合做高并发？"
print(f"\n查询: {query_text}")

results = collection.query(
    query_texts=[query_text],
    n_results=3
)

print("\n" + "=" * 60)
print("查询结果")
print("=" * 60)
for i in range(len(results['ids'][0])):
    print(f"\n--- 结果 {i+1} ---")
    print(f"ID: {results['ids'][0][i]}")
    print(f"距离: {results['distances'][0][i]:.4f}")
    print(f"内容: {results['documents'][0][i]}")
    print(f"元数据: {results['metadatas'][0][i]}")

# ===================== 6. 其他操作演示 =====================
print("\n" + "=" * 60)
print("其他操作")
print("=" * 60)

# 查看所有集合
print(f"\n所有集合: {client.list_collections()}")

# 获取集合信息
print(f"\n集合中的文档数: {collection.count()}")

# 更新文档
print("\n更新 doc_0 ...")
collection.update(
    ids=["doc_0"],
    documents=["Python 是一种解释型、高级、通用的编程语言，由 Guido van Rossum 于 1991 年首次发布，广泛应用于 AI、数据科学和 Web 开发。"]
)
print("✅ 更新完成")

print("\n" + "=" * 60)
print("✅ Chroma 快速入门完成！")
print("=" * 60)
