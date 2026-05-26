
---
name: 词向量与Tokenizer
description: NLP核心：词向量Word2Vec/GloVe和Tokenizer(BPE/WordPiece/SentencePiece)详解
type: learning-material
tags: ["NLP", "词向量", "Word2Vec", "Tokenizer", "BPE"]
summary: NLP核心：词向量和Tokenizer详解，包含Word2Vec两种训练方式、BPE原理和代码示例
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# 词向量与 Tokenizer 📖

&gt; 📖 **本讲学习目标**：理解词向量的意义、Word2Vec 的两种训练方式、Tokenizer 的原理（特别是 BPE）  
&gt; ⏰ **预计学习时间**：1 小时  
&gt; 🎯 **面试考点**：高频！

---

## 第一部分：词向量

### 什么是词向量？

#### 问题：计算机怎么理解词？
```
"猫" → ???
```

#### 答案：用向量表示！

```
"猫" → [0.1, 0.2, -0.3, ...]  (100维向量)
"狗" → [0.15, 0.25, -0.28, ...]  (接近"猫")
"车" → [0.8, -0.5, 0.1, ...]  (离"猫"很远)
```

### 为什么需要词向量？

| 表示方法 | 问题 | 词向量的优势 |
|---------|------|-------------|
| One-Hot | 维度太高，没语义 | 低维，有语义 |
| 离散符号 | 无法计算相似度 | 可以计算相似度 |

---

## Word2Vec（经典词向量方法）

### 两种训练方式 🔥

| 方式 | 全称 | 目标 |
|------|------|------|
| **CBOW** | Continuous Bag of Words | 用上下文预测中心词 |
| **Skip-gram** | - | 用中心词预测上下文 |

---

### 1. CBOW（Continuous Bag of Words）

#### 直观理解
```
句子: "我 喜欢 吃 苹果"
        ↑    ↑    ↑
     上下文(我,吃) → 预测中心词(喜欢)
```

#### 优点
- ✅ 训练快
- ✅ 对常见词效果好

#### 缺点
- ❌ 对稀有词效果一般

---

### 2. Skip-gram

#### 直观理解
```
句子: "我 喜欢 吃 苹果"
           ↑
        中心词(喜欢) → 预测上下文(我,吃,苹果)
```

#### 优点
- ✅ 对稀有词效果好
- ✅ 总体效果通常更好

#### 缺点
- ❌ 训练慢一点

---

### Word2Vec 代码实战

```python
# -*- coding: utf-8 -*-
import numpy as np

# 简化的 Skip-gram 示例
corpus = [
    "我 喜欢 吃 苹果",
    "我 喜欢 吃 香蕉",
    "猫 喜欢 吃 鱼",
    "狗 喜欢 吃 肉"
]

# 1. 构建词表
vocab = set()
for sentence in corpus:
    for word in sentence.split():
        vocab.add(word)
vocab = sorted(vocab)
word2id = {word: i for i, word in enumerate(vocab)}
id2word = {i: word for word, i in word2id.items()}

print("词表:", vocab)
print("\nword2id:", word2id)

# 2. 生成训练数据（中心词 -> 上下文）
window_size = 1
training_data = []

for sentence in corpus:
    words = sentence.split()
    for i, center_word in enumerate(words):
        center_id = word2id[center_word]
        # 上下文
        for j in range(max(0, i-window_size), min(len(words), i+window_size+1)):
            if i != j:
                context_word = words[j]
                context_id = word2id[context_word]
                training_data.append((center_id, context_id))

print("\n训练数据条数:", len(training_data))
print("前5条:", training_data[:5])
```

---

## 第二部分：Tokenizer（分词器）

### 什么是 Tokenization？

把句子切成更小的单元（Token）

```
"我喜欢编程" 
    ↓
["我", "喜欢", "编程"]
```

### 为什么需要 Tokenization？
- 大模型的输入是 Token 序列
- 减少词表大小
- 处理未登录词（OOV）

---

## 主流 Tokenization 算法

| 算法 | 说明 | 代表模型 |
|------|------|---------|
| **BPE** | Byte-Pair Encoding | GPT 系列、LLaMA |
| **WordPiece** | - | BERT 系列 |
| **SentencePiece** | - | T5、多语言模型 |

---

## BPE（Byte-Pair Encoding）详解 🔥

### BPE 核心思想
**高频出现的字符组合合并成一个 Token**

### BPE 完整训练过程

#### Step 1: 初始词表（单个字符）
```
词表: a, b, c, d, e, ...
```

#### Step 2: 统计字符对出现频率
```
low: l-o-w → 出现 100 次
new: n-e-w → 出现 50 次
...
```

#### Step 3: 合并最高频的对
```
假设 e-r 出现最多，合并成 "er"
词表新增: er
```

#### Step 4: 重复直到词表大小达标

---

### BPE 示例（超简化版）

```python
# -*- coding: utf-8 -*-
"""
BPE 简化演示
"""

# 初始词汇（都是单个字符）
vocab = set("abcdefghijklmnopqrstuvwxyz ")

# 训练数据
corpus = [
    "low low low low low",
    "new new new new new",
    "year year year year",
    "lowest lowest lowest",
    "newest newest newest",
    "wider wider wider",
    "widest widest widest"
]

print("=" * 60)
print("BPE 训练过程（简化版）")
print("=" * 60)

# 统计字符对频率（简化演示）
print("\nStep 1: 初始词表:", sorted(vocab))
print("Step 2: 假设 'e' 和 'r' 一起出现最多，合并成 'er'")
print("Step 3: 假设 'er' 和 'e' 一起出现最多，合并成 'ere'")
print("...")
print("Step N: 最终词表包含常见组合")

print("\n最终词表示例:")
print("['e', 'er', 'ere', 'ew', 'low', 'new', 'year', 'wide', 'est', ...]")
```

---

## Tokenizer 实战（HuggingFace）

```python
# -*- coding: utf-8 -*-
from transformers import AutoTokenizer

# 加载 BERT 的 Tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")

# 测试句子
text = "我喜欢用 Python 编程"

print("=" * 60)
print("Tokenizer 演示")
print("=" * 60)

# 1. 分词
tokens = tokenizer.tokenize(text)
print(f"\n原始句子: {text}")
print(f"分词结果: {tokens}")

# 2. 转成 ID
input_ids = tokenizer.encode(text)
print(f"\nToken IDs: {input_ids}")

# 3. 完整输出
output = tokenizer(text)
print(f"\n完整输出:")
for k, v in output.items():
    print(f"  {k}: {v}")

# 4. 解码
decoded = tokenizer.decode(input_ids)
print(f"\n解码回文本: {decoded}")
```

---

## 面试必考点 🔥

### Q1: Word2Vec 的两种训练方式是什么？区别是什么？
**答案**：
- **CBOW**：用上下文预测中心词，训练快，常见词好
- **Skip-gram**：用中心词预测上下文，稀有词好，整体效果好

### Q2: BPE 的工作原理是什么？
**答案**：
1. 初始词表是单个字符
2. 统计字符对出现频率
3. 合并最高频的对
4. 重复直到词表大小达标

### Q3: 为什么大模型都用 BPE/子词分词？
**答案**：
- 词表大小可控
- 可以处理未登录词（拆成子词）
- 平衡词汇量和语义

---

## 本讲小结 ✅

### 词向量部分
- 词向量：词 → 向量，有语义
- Word2Vec：CBOW（上下文→中心词）、Skip-gram（中心词→上下文）

### Tokenizer 部分
- Tokenization：句子 → Token 序列
- BPE：核心是合并高频字符对
- 面试必考题！

---

**Day05 全部内容结束！接下来是面试题和串讲！** 🎉
