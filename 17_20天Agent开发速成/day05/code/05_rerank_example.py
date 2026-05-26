
# -*- coding: utf-8 -*-
"""
Day05 Code 05: Rerank 重排序实战
"""

from sentence_transformers import SentenceTransformer, CrossEncoder, util

print("=" * 60)
print("Day05 - Rerank 重排序实战")
print("=" * 60)

# ===================== 1. 准备数据 =====================
documents = [
    "Go 语言由 Google 开发，擅长高并发场景，性能优异，是后端开发的热门选择。",
    "Python 是一种解释型语言，语法简洁，生态丰富，广泛用于 AI 和数据科学。",
    "Java 是编译型语言，运行在 JVM 上，企业级应用首选，稳定可靠。",
    "Rust 注重内存安全，系统级开发利器，性能接近 C++，学习曲线陡峭。",
    "JavaScript 主要用于网页前端开发，也可以用 Node.js 做后端。",
    "C++ 性能极高，游戏和系统开发常用，但复杂度高，容易出错。",
    "Kotlin 可以和 Java 互操作，Android 开发首选，简洁现代。",
    "TypeScript 是 JavaScript 的超集，类型安全，适合大型项目。",
    "PHP 是 Web 开发的老牌语言，WordPress 就是用 PHP 写的。",
    "Swift 是 Apple 的编程语言，用于 iOS 和 macOS 开发。"
]

query = "什么语言适合做高并发后端服务？"

print(f"\n文档数量: {len(documents)}")
print(f"查询: {query}")

# ===================== 2. 第一阶段：向量检索 =====================
print("\n" + "=" * 60)
print("第一阶段：向量检索（召回 Top 5）")
print("=" * 60)

embedding_model = SentenceTransformer('BAAI/bge-small-zh-v1.5')
doc_embeddings = embedding_model.encode(documents, convert_to_tensor=True)
query_embedding = embedding_model.encode(query, convert_to_tensor=True)

hits = util.semantic_search(query_embedding, doc_embeddings, top_k=5)[0]

print("\n向量检索结果:")
for i, hit in enumerate(hits, 1):
    print(f"{i}. (score: {hit['score']:.4f}) {documents[hit['corpus_id']][:50]}...")

# ===================== 3. 第二阶段：Rerank =====================
print("\n" + "=" * 60)
print("第二阶段：Rerank 重排序")
print("=" * 60)

print("\n加载 Rerank 模型...")
reranker = CrossEncoder('BAAI/bge-reranker-base')

# 取出候选文档
candidate_ids = [hit['corpus_id'] for hit in hits]
candidate_docs = [documents[i] for i in candidate_ids]

# 构造 pair
pairs = [[query, doc] for doc in candidate_docs]

# 计算 Rerank 分数
print("计算 Rerank 分数...")
rerank_scores = reranker.predict(pairs)

# 排序
rerank_results = sorted(zip(rerank_scores, candidate_ids, candidate_docs), key=lambda x: -x[0])

print("\nRerank 后结果:")
for i, (score, doc_id, doc) in enumerate(rerank_results, 1):
    print(f"{i}. (score: {score:.4f}) {doc[:60]}...")

# ===================== 4. 对比 =====================
print("\n" + "=" * 60)
print("对比：向量检索 vs +Rerank")
print("=" * 60)

print("\n向量检索第 1 名:")
print(f"  {documents[hits[0]['corpus_id']]}")

print("\nRerank 后第 1 名:")
print(f"  {rerank_results[0][2]}")

print("\n" + "=" * 60)
print("两阶段检索总结")
print("=" * 60)
print("""
第一阶段（召回）:
  - 方法: 向量检索
  - 目标: 尽可能召回相关文档
  - 速度: 极快

第二阶段（精排）:
  - 方法: Rerank
  - 目标: 把最相关的排到前面
  - 速度: 较慢，但更准

效果提升: 准确率通常从 70% 提升到 85%+
""")

print("\n" + "=" * 60)
print("✅ Rerank 演示完成！")
print("=" * 60)
