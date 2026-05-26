
# -*- coding: utf-8 -*-
"""
Day05 Code 01: 最简 RAG 系统
"""

import numpy as np
from sentence_transformers import SentenceTransformer, util

# ===================== 1. 准备文档 =====================
documents = [
    "Python 是一种解释型、高级、通用的编程语言，由 Guido van Rossum 于 1991 年首次发布。",
    "Python 的设计哲学强调代码的可读性，使用显著的缩进。",
    "Python 支持多种编程范式，包括面向对象、命令式、函数式和过程式编程。",
    "Python 的标准库提供了丰富的功能，被称为'电池包括'哲学。",
    "Python 广泛应用于 Web 开发、数据分析、人工智能、科学计算等领域。",
    "JavaScript 主要用于网页前端开发，可以和 HTML/CSS 配合。",
    "Java 是编译型语言，运行在 JVM 上，企业级应用首选。",
    "Go 语言擅长高并发场景，性能优异。"
]

print("=" * 60)
print("Day05 - 最简 RAG 系统")
print("=" * 60)
print(f"\n文档数量: {len(documents)}")

# ===================== 2. 加载 Embedding 模型 =====================
print("\n加载模型...")
model = SentenceTransformer('BAAI/bge-small-zh-v1.5')

# ===================== 3. 文档向量化 =====================
print("文档向量化...")
doc_embeddings = model.encode(documents, convert_to_tensor=True)
print(f"向量维度: {doc_embeddings.shape}")

# ===================== 4. 用户查询 =====================
query = "Python 是谁创建的？"
print(f"\n用户查询: {query}")

# 查询向量化
query_embedding = model.encode(query, convert_to_tensor=True)

# ===================== 5. 相似度检索 =====================
print("\n相似度检索...")
hits = util.semantic_search(query_embedding, doc_embeddings, top_k=3)[0]

print("\n" + "=" * 60)
print("检索结果 (Top 3)")
print("=" * 60)
for i, hit in enumerate(hits, 1):
    print(f"\n--- Top {i} (相似度: {hit['score']:.4f}) ---")
    print(documents[hit['corpus_id']])

# ===================== 6. 构建增强提示词 =====================
print("\n" + "=" * 60)
print("构建增强提示词")
print("=" * 60)

context = "\n\n".join([
    f"[资料 {i+1}] {documents[hit['corpus_id']]}"
    for i, hit in enumerate(hits)
])

prompt = f"""你是一个问答助手，只基于下面提供的参考资料回答用户问题。
如果参考资料里没有答案，请说"抱歉，我在提供的资料里找不到答案"。

【参考资料】
{context}

【用户问题】
{query}

【回答要求】
1. 只使用参考资料里的信息
2. 回答要简洁准确
3. 请标注答案来源

【回答】"""

print(prompt)

print("\n" + "=" * 60)
print("✅ 最简 RAG 演示完成！")
print("=" * 60)
