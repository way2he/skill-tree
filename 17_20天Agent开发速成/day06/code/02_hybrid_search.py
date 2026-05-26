
# -*- coding: utf-8 -*-
"""
Day06 Code 02：混合检索（BM25 + 向量）
"""

print("=" * 60)
print("Day06 - 混合检索演示")
print("=" * 60)

# 1. 准备数据
documents = [
    "iPhone 15 价格 5999 元起，A17 芯片",
    "iPhone 14 降价促销，A15 芯片，现在买很划算",
    "苹果手机新品发布会，iPhone 15 正式亮相",
    "华为 Mate 60 Pro 发布，麒麟芯片回归",
    "小米 14 系列，骁龙 8 Gen 3，性能强劲",
    "vivo X100 拍照手机，蔡司镜头，影像能力强"
]

query = "iPhone 15 价格"

print(f"\n文档数: {len(documents)}")
print(f"查询: {query}")

# 2. BM25 检索
try:
    from rank_bm25 import BM25Okapi
    print("\n" + "=" * 60)
    print("BM25 检索结果（关键词匹配）")
    print("=" * 60)
    tokenized_docs = [doc.split() for doc in documents]
    bm25 = BM25Okapi(tokenized_docs)
    bm25_scores = bm25.get_scores(query.split())
    bm25_results = sorted(zip(bm25_scores, documents), key=lambda x: -x[0])[:3]
    for i, (score, doc) in enumerate(bm25_results, 1):
        print(f"{i}. (score: {score:.4f}) {doc}")
except ImportError:
    print("\n请安装: pip install rank-bm25")

# 3. 向量检索
print("\n" + "=" * 60)
print("向量检索结果（语义匹配）")
print("=" * 60)
try:
    from sentence_transformers import SentenceTransformer, util
    model = SentenceTransformer('BAAI/bge-small-zh-v1.5')
    doc_embeddings = model.encode(documents, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)
    vec_hits = util.semantic_search(query_embedding, doc_embeddings, top_k=3)[0]
    for i, hit in enumerate(vec_hits, 1):
        print(f"{i}. (score: {hit['score']:.4f}) {documents[hit['corpus_id']]}")
except ImportError:
    print("\n请安装: pip install sentence-transformers")

# 4. 混合检索结果
print("\n" + "=" * 60)
print("混合检索 = BM25 + 向量（召回率更高）")
print("=" * 60)
print("""
BM25 优势: 关键词精确匹配（如 'iPhone 15 价格'）
向量优势: 语义匹配（如 '苹果手机' = 'iPhone'）
混合: 两者结合，召回率更高！
""")
