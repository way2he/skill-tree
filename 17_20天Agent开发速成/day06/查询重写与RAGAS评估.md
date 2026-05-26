
---
name: 查询重写与RAGAS评估
description: 查询重写方法详解、RAGAS评估指标与实战
type: learning-material
tags: ["查询重写", "RAGAS", "评估"]
summary: 查询重写与RAGAS评估详解，包含5个核心评估指标
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# 查询重写与 RAGAS 评估 📊

&gt; 📖 **本讲学习目标**：掌握查询重写方法，能用 RAGAS 评估 RAG 系统  
&gt; ⏰ **预计学习时间**：2 小时

---

## 第一部分：查询重写

### 为什么要查询重写？

#### 用户查询的问题
- 太口语化："咋弄这个？"
- 太长太啰嗦
- 缺少上下文
- 表达不清楚

#### 解决方法
用 LLM 把用户查询**重写**成更适合检索的形式！

---

### 常见查询重写方法

#### 方法 1：查询精简（Query Simplification）

把啰嗦的查询变简洁。

**例子**
```
用户: "我想知道怎么在 Python 里面写代码去调用 OpenAI 的 API，能不能给我一个简单的例子？"
重写后: "Python 调用 OpenAI API 示例"
```

**提示词模板**
```
把用户查询改写成简洁明了的形式，适合做向量检索，不要丢失关键信息。

用户查询: {query}
重写后:
```

---

#### 方法 2：查询扩展（Query Expansion）

扩展查询，增加相关关键词。

**例子**
```
用户: "Python 异步"
重写后: "Python asyncio aiohttp async await 异步编程"
```

---

#### 方法 3：查询拆解（Query Decomposition）

复杂问题拆成多个子问题。

**例子**
```
用户: "Python 和 Java 对比，哪个适合做后端？"
重写后:
1. Python 做后端的优缺点
2. Java 做后端的优缺点
3. Python vs Java 后端对比
```

---

#### 方法 4：多查询生成（Multi-Query Generation）

生成多个不同表达的查询，一起检索。

**例子**
```
用户: "Python 怎么学？"
重写后:
1. Python 学习路线
2. Python 入门教程
3. Python 学习资源推荐
4. 如何系统学习 Python
```

---

### 查询重写代码示例

```python
# -*- coding: utf-8 -*-
"""
查询重写示例
"""

# 简单的查询重写提示词模板
QUERY_REWRITE_TEMPLATE = """
你是一个查询重写助手，把用户查询改写成更适合做向量检索的形式。

要求:
1. 简洁明了，保留关键信息
2. 可以适当扩展相关关键词
3. 输出 3-5 种不同的查询表达

用户查询: {query}

重写后的查询（每行一个）:
"""

# 例子
query = "我想知道怎么系统地学习 Python，有没有推荐的路线？"

print("=" * 60)
print("原查询:")
print(query)
print("\n重写后的查询:")
print("1. Python 系统学习路线")
print("2. Python 学习路径推荐")
print("3. 如何系统学习 Python")
print("4. Python 入门到精通学习路线")
print("5. Python 学习规划")

print("\n" + "=" * 60)
print("为什么要多查询生成？")
print("=" * 60)
print("""
不同表达的查询可以召回不同但相关的文档
然后合并结果，提升召回率！
""")
```

---

## 第二部分：RAGAS 评估

### 什么是 RAGAS？

RAGAS（RAG Assessment）是专门评估 RAG 系统的框架。

### 为什么需要 RAGAS？

你做了一个 RAG 系统，怎么量化它好不好？
- 回答准确吗？
- 基于检索到的上下文吗？
- 上下文相关吗？

---

### RAGAS 的 5 个核心评估指标

#### 1. Faithfulness（忠实度）⭐⭐⭐⭐⭐

**衡量什么**：答案是否只基于检索到的上下文，有没有幻觉。

**例子**
```
上下文: "Python 由 Guido van Rossum 于 1991 年创建。"

好答案: "Python 由 Guido van Rossum 于 1991 年创建。" → Faithfulness = 1.0

坏答案: "Python 由 Bill Gates 于 1990 年创建。" → Faithfulness = 0.0
```

---

#### 2. Answer Relevance（答案相关性）⭐⭐⭐⭐⭐

**衡量什么**：答案是否和用户问题相关。

**例子**
```
用户问题: "Python 怎么学？"

好答案: "Python 可以通过在线课程、书籍、项目实战学习。" → 相关 = 1.0

坏答案: "今天天气真好。" → 相关 = 0.0
```

---

#### 3. Context Precision（上下文精准度）

**衡量什么**：检索到的上下文是否精准，有没有不相关的。

---

#### 4. Context Recall（上下文召回率）

**衡量什么**：应该检索到的文档有没有都检索到。

---

#### 5. Context Relevance（上下文相关性）

**衡量什么**：检索到的上下文是否和用户问题相关。

---

### RAGAS 评估指标总结

| 指标 | 衡量什么 | 目标 |
|------|---------|------|
| **Faithfulness** | 答案忠实于上下文吗？ | 越高越好 |
| **Answer Relevance** | 答案和问题相关吗？ | 越高越好 |
| **Context Precision** | 检索到的上下文精准吗？ | 越高越好 |
| **Context Recall** | 该召回的文档都召回了吗？ | 越高越好 |
| **Context Relevance** | 检索到的上下文相关吗？ | 越高越好 |

---

### RAGAS 快速入门

```python
# -*- coding: utf-8 -*-
"""
RAGAS 评估示例
"""

print("=" * 60)
print("RAGAS 评估示例")
print("=" * 60)

# RAGAS 需要的评估数据格式
sample_data = {
    "question": "Python 是谁创建的？",
    "answer": "Python 由 Guido van Rossum 于 1991 年创建。",
    "contexts": [
        "Python 是一种解释型语言，由 Guido van Rossum 于 1991 年首次发布。",
        "Python 的设计哲学强调代码可读性。"
    ],
    "ground_truth": "Python 由 Guido van Rossum 创建，发布于 1991 年。"
}

print("\n评估数据格式:")
print(f"  question: {sample_data['question']}")
print(f"  answer: {sample_data['answer']}")
print(f"  contexts: {len(sample_data['contexts'])} 个")
print(f"  ground_truth: {sample_data['ground_truth']}")

print("\n" + "=" * 60)
print("RAGAS 核心指标")
print("=" * 60)
print("""
1. Faithfulness: 答案是否忠实于上下文？
2. Answer Relevance: 答案是否相关？
3. Context Precision: 上下文精准度？
4. Context Recall: 上下文召回率？
5. Context Relevance: 上下文相关性？
""")

print("\n" + "=" * 60)
print("安装 RAGAS:")
print("  pip install ragas")
print("=" * 60)
```

---

## 本讲小结 ✅

### 查询重写
1. **查询精简**：变简洁
2. **查询扩展**：加关键词
3. **查询拆解**：拆成子问题
4. **多查询生成**：生成多个查询

### RAGAS 评估
- **Faithfulness**：忠实度
- **Answer Relevance**：答案相关性
- **Context Precision/Recall/Relevance**：上下文评估

### 下讲预告
文本分类与 NER 实战
