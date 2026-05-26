
---
name: 重排序Rerank实战
description: Rerank重排序实战教程：BGE-Reranker、ColBERT的使用和效果对比
type: learning-material
tags: ["Rerank", "重排序", "BGE-Reranker", "ColBERT"]
summary: Rerank重排序实战教程，包含BGE-Reranker的使用和效果对比
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# 重排序 Rerank 实战 📋

&gt; 📖 **本讲学习目标**：理解为什么需要重排序，学会使用 BGE-Reranker，能看到 Rerank 带来的效果提升  
&gt; ⏰ **预计学习时间**：1 小时

---

## 为什么需要重排序？

### 向量检索的问题
向量检索是**快**，但**不够准**

```
向量检索返回 Top 20
    (快，召回率高，但可能混进去不相关的)
        ↓
    Rerank 重排 → 返回 Top 3
        (慢，但准确率高)
```

### 两阶段检索

| 阶段 | 方法 | 目标 | 速度 |
|------|------|------|------|
| **第一阶段（召回）** | 向量检索 | 尽可能找到所有相关的 | ⚡ 极快 |
| **第二阶段（精排）** | Rerank | 把最相关的排到前面 | 🐢 较慢 |

### 效果对比
| 方法 | 准确率 | 速度 |
|------|--------|------|
| 向量检索 | 70% | ⚡⚡⚡⚡⚡ |
| + Rerank | 85% | ⚡⚡ |

---

## 主流 Rerank 模型

| 模型 | 厂商 | 中文 | 速度 | 效果 | 推荐 |
|------|------|------|------|------|------|
| **BGE-Reranker** | 智源 | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 首选 |
| **ColBERT** | Stanford | ⭐⭐⭐ | ⚡⚡ | ⭐⭐⭐⭐ | 英文 |
| **Cross-Encoder** | Sentence-Transformers | ⭐⭐⭐ | ⚡⚡ | ⭐⭐⭐⭐ | 通用 |

---

## 实战：BGE-Reranker 🔥

### 1. 安装
```bash
pip install sentence-transformers flagembedding
```

### 2. 最简示例
```python
# -*- coding: utf-8 -*-
from sentence_transformers import CrossEncoder

# 加载模型
model = CrossEncoder('BAAI/bge-reranker-base')

# 查询和文档
query = "什么语言适合高并发？"
documents = [
    "Go 语言擅长高并发场景",
    "Python 是解释型语言",
    "Java 运行在 JVM 上",
    "Rust 注重内存安全",
    "JavaScript 用于网页开发"
]

# 构造 pair 对
pairs = [[query, doc] for doc in documents]

# 计算分数
scores = model.predict(pairs)

print("=" * 50)
print(f"查询: {query}")
print("=" * 50)

# 排序输出
results = sorted(zip(scores, documents), key=lambda x: -x[0])
for score, doc in results:
    print(f"\n分数: {score:.4f}")
    print(f"文档: {doc}")
```

---

## 完整实战：向量检索 vs 向量检索+Rerank

```python
# -*- coding: utf-8 -*-
from sentence_transformers import SentenceTransformer, CrossEncoder, util

# 1. 准备数据
documents = [
    "Go 语言由 Google 开发，擅长高并发场景，性能优异",
    "Python 是一种解释型语言，语法简洁，生态丰富",
    "Java 是编译型语言，运行在 JVM 上，企业级应用首选",
    "Rust 注重内存安全，系统级开发利器",
    "JavaScript 主要用于网页前端开发，也可以做后端（Node.js）",
    "C++ 性能极高，游戏和系统开发常用",
    "Kotlin 可以和 Java 互操作，Android 开发首选",
    "TypeScript 是 JavaScript 的超集，类型安全"
]

query = "什么语言适合做高并发服务？"

# 2. 第一阶段：向量检索
print("=" * 60)
print("第一阶段：向量检索（召回）")
print("=" * 60)

embedding_model = SentenceTransformer('BAAI/bge-small-zh-v1.5')
doc_embeddings = embedding_model.encode(documents, convert_to_tensor=True)
query_embedding = embedding_model.encode(query, convert_to_tensor=True)

hits = util.semantic_search(query_embedding, doc_embeddings, top_k=5)[0]

print("\n向量检索 Top 5:")
for i, hit in enumerate(hits, 1):
    print(f"{i}. (score: {hit['score']:.3f}) {documents[hit['corpus_id']]}")

# 3. 第二阶段：Rerank 重排
print("\n" + "=" * 60)
print("第二阶段：Rerank 重排（精排）")
print("=" * 60)

reranker = CrossEncoder('BAAI/bge-reranker-base')

# 取出向量检索的 Top 5 做重排
candidate_docs = [documents[hit['corpus_id']] for hit in hits]
pairs = [[query, doc] for doc in candidate_docs]

rerank_scores = reranker.predict(pairs)

# 重排序
rerank_results = sorted(zip(rerank_scores, candidate_docs), key=lambda x: -x[0])

print("\nRerank 后结果:")
for i, (score, doc) in enumerate(rerank_results, 1):
    print(f"{i}. (score: {score:.4f}) {doc}")

# 4. 对比
print("\n" + "=" * 60)
print("对比：向量检索 vs +Rerank")
print("=" * 60)
print(f"\n向量检索第1: {documents[hits[0]['corpus_id']]}")
print(f"+Rerank 后第1: {rerank_results[0][1]}")
```

---

## Rerank 最佳实践

### 1. K 值怎么选？
| 场景 | 建议 K |
|------|--------|
| **通用** | 20-50 |
| **数据量小** | 10-20 |
| **数据量大** | 50-100 |

### 2. 速度优化
- 向量检索用小模型（BGE-small）
- Rerank 也用小模型（BGE-reranker-base）
- 可以用 ONNX 加速 Rerank

### 3. 什么时候用 Rerank？
- ✅ 对准确率要求高
- ✅ 计算资源充足
- ✅ 数据量大

---

## 本讲小结 ✅

### 核心要点
1. Rerank 是两阶段检索的第二阶段（精排）
2. 向量检索快但不够准，Rerank 准但慢
3. BGE-Reranker 是中文首选

### 下讲预告
下一讲：【NLP 核心】词向量 Word2Vec/GloVe + Tokenizer

---
