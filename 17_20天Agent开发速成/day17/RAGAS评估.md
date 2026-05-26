
---
name: RAGAS评估
description: RAGAS评估框架完整详解：核心指标、评估实践
type: knowledge
tags: ["RAGAS", "评估", "RAG"]
summary: RAGAS评估框架完整详解
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# RAGAS评估 📊

&gt; 🎯 **本章目标**：理解如何用RAGAS评估RAG系统  
&gt; ⏰ **预计时间**：60 分钟

---

## 一、RAGAS简介

### 什么是RAGAS？

RAGAS = RAG Assessment，专门用于评估RAG（检索增强生成）系统的框架。

---

## 二、核心指标

### RAGAS的4大核心指标

| 指标 | 说明 | 衡量什么 | 分数范围 |
|------|------|---------|---------|
| **Answer Relevancy** | 答案相关性 | 回答是否切题 | 0-1 |
| **Context Relevancy** | 上下文相关性 | 检索的上下文是否相关 | 0-1 |
| **Faithfulness** | 忠实度 | 回答是否基于上下文，不幻觉 | 0-1 |
| **Context Recall** | 上下文召回 | 关键信息是否都在上下文中 | 0-1 |

---

## 三、简化评估示例

### 1. 手动计算示例

```python
def evaluate_rag_sample(question, answer, contexts, ground_truth):
    """简化的RAG评估"""
    
    # 答案相关性（简化：关键词匹配）
    question_keywords = set(question.lower().split())
    answer_keywords = set(answer.lower().split())
    answer_relevancy = len(question_keywords &amp; answer_keywords) / max(len(question_keywords), 1)
    
    # 上下文相关性（简化：关键词匹配）
    context_text = " ".join(contexts).lower()
    context_keywords = set(context_text.split())
    context_relevancy = len(question_keywords &amp; context_keywords) / max(len(question_keywords), 1)
    
    # 忠实度（简化：答案是否来自上下文）
    answer_words = answer.lower().split()
    context_words = context_text.split()
    faithfulness = sum(1 for w in answer_words if w in context_words) / max(len(answer_words), 1)
    
    # 上下文召回（简化：标准答案是否在上下文中）
    ground_truth_words = ground_truth.lower().split()
    context_recall = sum(1 for w in ground_truth_words if w in context_words) / max(len(ground_truth_words), 1)
    
    return {
        "answer_relevancy": round(answer_relevancy, 2),
        "context_relevancy": round(context_relevancy, 2),
        "faithfulness": round(faithfulness, 2),
        "context_recall": round(context_recall, 2),
    }

# 示例
question = "什么是Python？"
answer = "Python是一种编程语言，由Guido van Rossum创建。"
contexts = [
    "Python是一种解释型、高级、通用的编程语言。",
    "Python由Guido van Rossum设计，于1991年首次发布。",
]
ground_truth = "Python是一种编程语言，由Guido van Rossum创建。"

result = evaluate_rag_sample(question, answer, contexts, ground_truth)
print("评估结果：")
for key, value in result.items():
    print(f"  {key}: {value}")
```

---

## 四、面试要点

### 高频面试题

1. **RAGAS的核心指标有哪些？**
   - Answer Relevancy：答案相关性
   - Context Relevancy：上下文相关性
   - Faithfulness：忠实度（不幻觉）
   - Context Recall：上下文召回

2. **Faithfulness衡量什么？**
   - 回答是否基于检索到的上下文
   - 是否有幻觉（编造信息）

3. **如何评估RAG系统？**
   - 准备测试集（问题、标准答案）
   - RAG系统生成回答和上下文
   - 用RAGAS计算各项指标
   - 分析弱点，优化系统

---

**🎉 本章完成！**
