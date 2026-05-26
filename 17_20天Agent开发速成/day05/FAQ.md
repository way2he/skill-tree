
---
name: Day05 FAQ
description: Day05 常见问题解答
type: faq
tags: ["FAQ", "常见问题"]
summary: Day05 常见问题解答
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# Day05 常见问题 FAQ ❓

---

## RAG 相关

### Q1: RAG 和 Fine-tuning 怎么选？

| 维度 | RAG | Fine-tuning |
|------|-----|-------------|
| **知识更新** | 快（加文档就行） | 慢（重新训练） |
| **可追溯** | ✅ 可以溯源到文档 | ❌ 不行 |
| **幻觉** | 较少 | 可能有 |
| **成本** | 低（推理时成本） | 高（训练成本） |
| **适用场景** | 知识变化快、需要溯源 | 风格对齐、特定任务 |

---

### Q2: RAG 效果不好怎么办？

检查清单：
1. ✅ 文档分块合理吗？
2. ✅ Embedding 模型选对了吗？
3. ✅ Top-K 大小合适吗？
4. ✅ 加 Rerank 了吗？
5. ✅ 提示词写得好吗？

---

## Embedding 相关

### Q3: 中文 Embedding 选哪个？

**首选：BGE 系列**（BAAI/bge-small/medium/large-zh-v1.5）
- 效果最好
- 开源免费
- 社区活跃

---

## 向量数据库相关

### Q4: Chroma 和 Qdrant 怎么选？

| 场景 | 选择 |
|------|------|
| **开发/原型** | Chroma（简单） |
| **生产环境** | Qdrant（性能好） |
| **大规模** | Pinecone（托管）/ Milvus |

---

## 相似度相关

### Q5: 余弦相似度 0.8 算高吗？

- 0.9+：非常相似
- 0.7-0.9：比较相似
- 0.5-0.7：一般相似
- 0.5 以下：不太相似

---

## Rerank 相关

### Q6: Rerank 的 K 选多少？

- 通用：20-50
- 数据量小：10-20
- 数据量大：50-100

---

## NLP 相关

### Q7: 学 Agent 还要学传统 NLP 吗？

**不用系统学！**  
本计划已经把 NLP 必学内容融入对应天数了：
- 词向量 + Tokenizer → Day05
- 文本分类 + NER → Day06
- Transformer 深度 → Day07
- LoRA 微调 → Day14

---

## 面试相关

### Q8: 今天内容面试重点是什么？

**必背 3 题：**
1. RAG 完整流程
2. 向量数据库 vs 传统数据库
3. 余弦相似度 vs 欧氏距离

**进阶 3 题：**
4. 为什么需要 Rerank？
5. Word2Vec 的两种训练方式？
6. BPE 怎么工作？

---

## 其他

### Q9: 有推荐的 RAG 项目参考吗？

- LlamaIndex（GPT Index）
- LangChain RAG 模板
- OpenAGI
- 等等

---

**还有问题？请随时问！** 🙋
