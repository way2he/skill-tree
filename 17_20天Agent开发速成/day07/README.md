
---
name: Day07-LangGraph框架入门
description: Day07完整学习资料：LangGraph核心概念、ML基础、Transformer深度精讲
type: learning-material
tags: ["LangGraph", "Agent", "Transformer", "梯度下降"]
summary: LangGraph框架入门，包含核心概念、ML基础、Transformer深度精讲
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# Day07：LangGraph 框架入门 🚀

&gt; 📅 **学习日期**：2026-05-26  
&gt; ⏰ **总时长**：8 小时  
&gt; 🎯 **验收标准**：能从零搭一个带条件跳转的 LangGraph，能说清 Transformer 核心原理

---

## 📋 今日学习内容清单

| 时间 | 学习内容 | 时长 | 对应文档 |
|------|---------|------|---------|
| **09:00-10:00** | LangGraph 核心概念：State/Node/Edge/Graph | 1h | `LangGraph核心概念.md` |
| **10:00-11:00** | State 设计最佳实践 | 1h | `LangGraph核心概念.md` |
| **11:00-12:00** | 节点编写：纯函数 vs 带副作用 | 1h | `LangGraph核心概念.md` |
| **14:00-15:00** | ML基础：梯度下降+反向传播+激活函数 | 1h | `ML基础-梯度下降与激活函数.md` |
| **15:00-16:00** | ML基础：损失函数（CE/MSE/Contrastive） | 1h | `ML基础-梯度下降与激活函数.md` |
| **16:00-17:00** | NLP核心：Transformer深度精讲 | 1h | `Transformer深度精讲.md` |
| **19:00-20:00** | 面试题专项（Day07） | 1h | `面试题.md` + `面试题_标准答案.md` |
| **20:00-21:00** | 复盘 + 整理面试话术 | 1h | `今日串讲.md` |

---

## 🎯 今日验收标准

### 理论验收（面试必答）
- ✅ 能说清 LangGraph 和 LangChain 的区别
- ✅ 能说清 Transformer 完整架构（Self-Attention、Multi-Head、LayerNorm 等）
- ✅ 能解释为什么用 LayerNorm 而不是 BatchNorm
- ✅ 能解释梯度下降三种变体（SGD/Momentum/Adam）

### 代码验收（手写代码）
- ✅ 能从零写一个带条件跳转的 LangGraph
- ✅ 能画出 Transformer 架构图

---

## 📚 今日核心知识点

### LangGraph 核心概念

| 概念 | 说明 |
|------|------|
| **State** | Agent 的状态（对话历史、中间结果等） |
| **Node** | 节点（执行单元，纯函数或带副作用） |
| **Edge** | 边（连接节点，条件跳转） |
| **Graph** | 完整的图（State + Nodes + Edges） |

### Transformer 核心组件

| 组件 | 作用 |
|------|------|
| **Self-Attention** | 自注意力，计算词之间的关系 |
| **Multi-Head Attention** | 多头注意力，多个子空间并行 |
| **Position Encoding** | 位置编码，加入位置信息 |
| **LayerNorm** | 层归一化，稳定训练 |
| **Feed Forward** | 前馈网络，非线性变换 |

---

## 💻 今日代码实战

### 代码文件清单
- `code/01_simple_langgraph.py` - 最简单的 LangGraph
- `code/02_conditional_edge.py` - 带条件跳转的 LangGraph
- `code/03_ml_gradient_descent.py` - 梯度下降演示
- `code/04_activation_functions.py` - 激活函数对比

---

## 📌 今日面试考点（5 道）

### 基础题（2 道）
1. LangChain 和 LangGraph 的区别是什么？为什么要用 LangGraph？
2. 梯度下降三种变体（SGD/Momentum/Adam）的区别？

### 进阶题（3 道）
3. Transformer 的完整架构是什么？请详细说明每个组件。
4. 为什么 Transformer 用 LayerNorm 而不是 BatchNorm？
5. Self-Attention 的公式推导和计算过程？

---

## 🔗 相关资料链接

- 官方文档
  - 📖 [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
  - 📖 [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

---

## 📝 今日学习计划（建议）

### 上午（3 小时）
1. LangGraph 核心概念（State/Node/Edge/Graph）
2. State 设计最佳实践
3. 节点编写（纯函数 vs 带副作用）

### 下午（3 小时）
1. ML 基础：梯度下降 + 反向传播 + 激活函数
2. ML 基础：损失函数
3. NLP 核心：Transformer 深度精讲

### 晚上（2 小时）
1. 5 道面试题 + 标准答案
2. 复盘整理

---

**🚀 让我们开始 Day07 的学习！**
