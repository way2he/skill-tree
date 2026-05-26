
# -*- coding: utf-8 -*-
"""
Day05 Code 04: 相似度算法对比
"""

import numpy as np
from sentence_transformers import SentenceTransformer, util

print("=" * 60)
print("Day05 - 相似度算法对比")
print("=" * 60)

# ===================== 1. 准备数据 =====================
sentences = [
    "我喜欢吃苹果",
    "我爱吃苹果",
    "我喜欢吃香蕉",
    "我喜欢吃水果",
    "今天天气真好",
    "Python 是编程语言",
    "机器学习是人工智能的分支"
]

print(f"\n句子数量: {len(sentences)}")
for i, s in enumerate(sentences):
    print(f"  {i}. {s}")

# ===================== 2. 加载模型 =====================
print("\n加载模型...")
model = SentenceTransformer('BAAI/bge-small-zh-v1.5')

# ===================== 3. 向量化 =====================
print("向量化...")
embeddings = model.encode(sentences, convert_to_tensor=True)

# ===================== 4. 余弦相似度矩阵 =====================
print("\n" + "=" * 60)
print("余弦相似度矩阵")
print("=" * 60)
cosine_matrix = util.cos_sim(embeddings, embeddings)
for i in range(len(sentences)):
    for j in range(len(sentences)):
        print(f"{cosine_matrix[i][j]:.3f}", end="  ")
    print()

# ===================== 5. 查询示例 =====================
query = "我喜欢吃什么水果？"
print(f"\n\n查询: {query}")
query_embedding = model.encode(query, convert_to_tensor=True)

print("\n" + "=" * 60)
print("余弦相似度检索结果")
print("=" * 60)
cosine_hits = util.semantic_search(query_embedding, embeddings, top_k=5)[0]
for i, hit in enumerate(cosine_hits, 1):
    print(f"{i}. (score: {hit['score']:.4f}) {sentences[hit['corpus_id']]}")

# ===================== 6. 欧氏距离对比 =====================
from sklearn.metrics.pairwise import euclidean_distances

print("\n" + "=" * 60)
print("欧氏距离结果")
print("=" * 60)
euclidean_matrix = euclidean_distances(embeddings, [query_embedding])
# 从小到大排序
sorted_idx = np.argsort(euclidean_matrix.flatten())
for i, idx in enumerate(sorted_idx[:5]):
    print(f"{i+1}. (distance: {euclidean_matrix[idx][0]:.4f}) {sentences[idx]}")

# ===================== 7. 直观对比 =====================
print("\n" + "=" * 60)
print("算法对比总结")
print("=" * 60)
print("""
余弦相似度:
  - 看向量夹角
  - 范围 [-1, 1]
  - 文本相似度首选

欧氏距离:
  - 看直线距离
  - 范围 [0, ∞)
  - 低维空间用

内积:
  - 归一化后 = 余弦
  - 最快
""")

print("\n" + "=" * 60)
print("✅ 相似度对比演示完成！")
print("=" * 60)
