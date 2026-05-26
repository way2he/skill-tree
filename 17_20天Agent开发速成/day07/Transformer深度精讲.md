
---
name: Transformer深度精讲
description: NLP核心：Transformer架构深度精讲（面试必背！）
type: learning-material
tags: ["NLP", "Transformer", "Self-Attention", "Multi-Head", "LayerNorm"]
summary: Transformer架构深度精讲，包含Self-Attention、Multi-Head、LayerNorm、Position Encoding
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# Transformer 深度精讲 🔥（面试必背！）

&gt; 📖 **本讲学习目标**：完全理解 Transformer 架构，能说出每个组件的作用，能解释为什么用 LayerNorm  
&gt; ⏰ **预计学习时间**：1 小时  
&gt; 🎯 **面试必考**：100% 会问！

---

## Transformer 整体架构

```
输入 → Embedding + Position Encoding
         ↓
    Encoder Stack × N
         ↓
    Decoder Stack × N
         ↓
    Linear + Softmax → 输出
```

---

## 核心组件详解

### 1. Self-Attention（自注意力）⭐⭐⭐⭐⭐

**一句话**：计算每个词和其他所有词的关系。

**公式**（记下来！面试会推！）
```
Attention(Q, K, V) = softmax(Q·K^T / √d_k) · V
```

**Q/K/V 是什么？**
- Q（Query）：当前词"问"其他词
- K（Key）：其他词的"钥匙"
- V（Value）：其他词的"值"

**为什么除以 √d_k？**
- 防止 Q·K^T 太大，softmax 梯度消失

---

### 2. Multi-Head Attention（多头注意力）⭐⭐⭐⭐⭐

**一句话**：把 Q/K/V 分成多个头，并行关注不同子空间。

**为什么多头？**
- 每个头可以关注不同模式（语法/语义/局部/全局）
- 并行计算，快

---

### 3. Position Encoding（位置编码）⭐⭐⭐⭐⭐

**一句话**：给 Embedding 加入位置信息（Attention 本身不知道位置）。

**两种方案**
1. **正弦/余弦位置编码**（原 Transformer）
2. **可学习位置编码**（GPT/BERT 常用）

---

### 4. LayerNorm vs BatchNorm ⭐⭐⭐⭐⭐（必考！）

**为什么 Transformer 用 LayerNorm 而不是 BatchNorm？**

| 维度 | LayerNorm | BatchNorm |
|------|-----------|-----------|
| 归一化方向 | 每个样本内部归一化 | 每个特征在 batch 内部归一化 |
| 序列长度 | 可变长度没问题 | batch 内序列长度要一致 |
| batch size | 不敏感 | batch size 小效果差 |

**答案**：
1. 序列长度可变，BatchNorm 不好处理
2. batch size 小时，LayerNorm 更稳
3. 每个样本独立，推理时也能正常计算

---

### 5. Residual Connection（残差连接）⭐⭐⭐⭐⭐

**一句话**：x + F(x)，解决深层网络梯度消失问题。

---

### 6. Feed Forward Network（前馈网络）⭐⭐⭐⭐

**结构**
```
Linear → GELU → Linear
```

**作用**：引入非线性，拟合复杂函数。

---

## Encoder vs Decoder

| 组件 | Encoder | Decoder |
|------|---------|---------|
| Self-Attention | ✅ | ✅（Masked） |
| Cross-Attention | ❌ | ✅（Attend to Encoder） |
| Feed Forward | ✅ | ✅ |
| 输入 | 原文 | 已生成的词 |

---

## Transformer 三个重要分支

| 分支 | 架构 | 代表 | 适用任务 |
|------|------|------|---------|
| **Encoder-only** | 只有 Encoder | BERT、ERNIE | 理解类（分类、NER、QA） |
| **Decoder-only** | 只有 Decoder | GPT、Llama | 生成类（文本生成） |
| **Encoder-Decoder** | 都有 | T5、BART | 翻译、摘要 |

---

## 本讲小结 ✅

### Transformer 核心组件（面试必背！）
1. **Self-Attention**：Q/K/V，公式要会推
2. **Multi-Head**：多头并行，关注不同子空间
3. **Position Encoding**：加入位置信息
4. **LayerNorm vs BatchNorm**：必考！要讲清楚区别
5. **Residual**：x + F(x)，防梯度消失
6. **FFN**：前馈网络，非线性

---

**Day07 理论部分完成！接下来是面试题！** 🎉
