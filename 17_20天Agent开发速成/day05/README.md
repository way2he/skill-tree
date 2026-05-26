
---
name: Day05-RAG检索增强(上)-基础篇
description: Day05完整学习资料：RAG完整流程、Embedding模型对比、向量数据库、相似度检索、重排序、词向量与Tokenizer
type: learning-material
tags: ["RAG", "Agent开发", "向量数据库", "Embedding", "NLP"]
summary: RAG基础篇完整学习资料，包含完整流程、模型对比、向量库、重排序、词向量、Tokenizer及配套代码
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# Day05：RAG 检索增强（上）- 基础篇 🚀

&gt; 📅 **学习日期**：2026-05-26  
&gt; ⏰ **总时长**：8 小时  
&gt; 🎯 **验收标准**：能从零搭建一个完整的 RAG 问答系统，能说清楚每个环节的原理

---

## 📋 本日学习内容清单

| 时间 | 学习内容 | 时长 | 对应文档 |
|------|---------|------|---------|
| **09:00-10:00** | RAG 完整流程：文档 → 分块 → 向量化 → 检索 → 增强 → 生成 | 1h | [RAG完整流程详解.md](./RAG完整流程详解.md) |
| **10:00-11:00** | Embedding 模型对比：OpenAI、BGE、M3E、GTE | 1h | [Embedding模型对比与选型.md](./Embedding模型对比与选型.md) |
| **11:00-12:00** | 向量数据库基础：Chroma、Qdrant 对比 + 实战 | 1h | [向量数据库基础实战.md](./向量数据库基础实战.md) |
| **14:00-15:00** | 相似度检索原理：余弦相似度、欧氏距离、内积 | 1h | [相似度检索原理.md](./相似度检索原理.md) |
| **15:00-16:00** | 重排序 Rerank 原理 + 实战：BGE-Reranker、ColBERT | 1h | [重排序Rerank实战.md](./重排序Rerank实战.md) |
| **16:00-17:00** | 【NLP核心】词向量 Word2Vec/GloVe + Tokenizer | 1h | [词向量与Tokenizer.md](./词向量与Tokenizer.md) |
| **19:00-20:00** | 【面试题专项】Day05 6 道 RAG 基础面试题 | 1h | [面试题.md](./面试题.md) + [面试题_标准答案.md](./面试题_标准答案.md) |
| **20:00-21:00** | 复盘 + 整理面试话术 | 1h | [今日串讲.md](./今日串讲.md) |

---

## 🎯 本日验收标准

### 理论验收（面试必答）
- ✅ 能完整画出 RAG 的完整流程
- ✅ 能说出 3 个以上 Embedding 模型的优缺点
- ✅ 能解释余弦相似度和欧氏距离的区别
- ✅ 能讲清楚为什么需要重排序
- ✅ 能说清 Word2Vec 的两种训练方式和 BPE 的工作原理

### 代码验收（手写代码）
- ✅ 能从零手写一个最简单的 RAG 问答系统
- ✅ 能使用 Chroma/Qdrant 完成向量存储和检索
- ✅ 能实现带重排序的 RAG 流程

---

## 📚 本日核心知识点

### RAG 完整流程 🔄
```
文档 → 分块 → 向量化 → 向量存储 → 用户查询 → 向量化 → 相似度检索 → 重排序 → 增强 → 生成回答
```

### 关键概念速查
| 概念 | 一句话说明 |
|------|-----------|
| **RAG** | Retrieval-Augmented Generation，用检索到的知识增强大模型生成 |
| **Embedding** | 把文本变成高维向量，衡量语义相似度 |
| **向量数据库** | 专门存向量、做相似度检索的数据库 |
| **余弦相似度** | 用两个向量的夹角大小衡量相似程度 |
| **Rerank** | 用更精准的模型对初筛结果重排，提升准确率 |
| **Word2Vec** | 经典的词向量训练方法，CBOW 和 Skip-gram 两种方式 |
| **BPE** | Byte-Pair Encoding，大模型通用的 Tokenization 算法 |

---

## 💻 本日代码实战

### 代码文件清单
- [code/01_simple_rag.py](./code/01_simple_rag.py) - 最简单的 RAG 系统
- [code/02_chroma_quickstart.py](./code/02_chroma_quickstart.py) - Chroma 快速入门
- [code/03_qdrant_quickstart.py](./code/03_qdrant_quickstart.py) - Qdrant 快速入门
- [code/04_similarity_comparison.py](./code/04_similarity_comparison.py) - 相似度算法对比
- [code/05_rerank_example.py](./code/05_rerank_example.py) - 重排序实战
- [code/06_tokenizer_demo.py](./code/06_tokenizer_demo.py) - Tokenizer 演示

### 快速启动
```bash
# 安装依赖
pip install chromadb qdrant-client sentence-transformers scikit-learn numpy

# 运行最简 RAG
python code/01_simple_rag.py
```

---

## 📌 本日面试考点（6 道题）

### 基础题（3 道）
1. RAG 的完整流程是什么？每个环节的作用是什么？
2. 向量数据库和传统数据库的区别是什么？
3. 余弦相似度和欧氏距离的区别？什么时候用哪个？

### 进阶题（3 道）
4. 为什么需要重排序？直接用向量检索不行吗？
5. Word2Vec 的两种训练方式是什么？各自有什么优缺点？
6. BPE 是怎么工作的？为什么大模型都用 BPE 做 Tokenization？

&gt; 💡 **答案详见**：[面试题_标准答案.md](./面试题_标准答案.md)

---

## 🔗 相关资料链接

- 官方文档
  - 📖 [Chroma 官方文档](https://docs.trychroma.com/)
  - 📖 [Qdrant 官方文档](https://qdrant.tech/documentation/)
  - 📖 [Sentence-Transformers 文档](https://www.sbert.net/)

- 经典论文
  - 📄 RAG: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
  - 📄 Efficient and Effective Passage Search via Contextualized Late Interaction
  - 📄 ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction

---

## 📝 今日学习计划（建议）

### 上午（3小时）
1. **09:00-10:00**：看 RAG 完整流程，理解每个环节
2. **10:00-11:00**：对比 Embedding 模型，了解选型思路
3. **11:00-12:00**：跑通 Chroma 和 Qdrant 的代码示例

### 下午（3小时）
1. **14:00-15:00**：理解相似度算法的区别
2. **15:00-16:00**：实现重排序，看 RAG 效果提升
3. **16:00-17:00**：学习 NLP 核心：词向量 + Tokenizer

### 晚上（2小时）
1. **19:00-20:00**：做 6 道面试题，对照标准答案
2. **20:00-21:00**：复盘整理，准备 Day06

---

**🚀 让我们开始 Day05 的学习吧！先从 RAG 完整流程开始！**

---
