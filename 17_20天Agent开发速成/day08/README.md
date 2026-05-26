
---
name: Day08-LangGraph精通与预训练模型
description: Day08完整学习资料：LangGraph图编译、Checkpoint、流式输出、Human-in-the-loop、BERT/GPT/T5三大家族
type: learning-material
tags: ["LangGraph", "Agent开发", "LLM", "预训练模型"]
summary: Day08完整学习资料，LangGraph高级特性与预训练模型三大家族详解
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# Day08：LangGraph 精通与预训练模型三大家族 🚀

&gt; 📅 **学习日期**：2026-05-26  
&gt; ⏰ **总时长**：8 小时  
&gt; 🎯 **验收标准**：能实现生产级 LangGraph 应用，讲清楚三大预训练模型家族的区别

---

## 📋 本日学习内容清单

| 时间 | 学习内容 | 时长 | 对应文档 |
|------|---------|------|---------|
| **09:00-10:00** | LangGraph 图编译原理与高级 API | 1h | LangGraph图编译原理.md |
| **10:00-11:00** | Checkpoint 机制与状态持久化 | 1h | Checkpoint与状态持久化.md |
| **11:00-12:00** | 流式输出与实时交互 | 1h | 流式输出与Human-in-the-loop.md |
| **14:00-15:00** | Human-in-the-loop 设计模式 | 1h | 流式输出与Human-in-the-loop.md |
| **15:00-16:00** | 预训练模型三大家族：BERT 系 | 1h | 预训练模型三大家族.md |
| **16:00-17:00** | 预训练模型三大家族：GPT 系 + T5 系 | 1h | 预训练模型三大家族.md |
| **19:00-20:00** | 【面试题专项】Day08 6 道面试题 | 1h | 面试题.md + 面试题_标准答案.md |
| **20:00-21:00** | 复盘 + 整理面试话术 | 1h | 今日串讲.md |

---

## 🎯 本日验收标准

### 理论验收（面试必答）
- ✅ 能讲清楚 LangGraph 的图编译原理和优势
- ✅ 能解释 Checkpoint 机制的设计思想和应用场景
- ✅ 能实现流式输出和 Human-in-the-loop 交互
- ✅ 能对比 BERT、GPT、T5 三大模型家族的区别
- ✅ 能说出每个模型家族的适用场景

### 代码验收（手写代码）
- ✅ 能实现带 Checkpoint 的 LangGraph 应用
- ✅ 能实现流式输出的 Agent
- ✅ 能实现 Human-in-the-loop 交互流程

---

## 📚 本日核心知识点

### LangGraph 高级特性 🔄
- **图编译**：将状态机编译为高效执行图
- **Checkpoint**：状态持久化，支持中断恢复
- **流式输出**：Token 级实时输出
- **Human-in-the-loop**：人机协作模式

### 预训练模型三大家族
| 家族 | 特点 | 代表模型 | 适用场景 |
|------|------|---------|---------|
| **BERT** | 双向编码器，理解能力强 | BERT、RoBERTa、ALBERT | 分类、NER、抽取 |
| **GPT** | 自回归解码器，生成能力强 | GPT-2/3/4、LLaMA | 文本生成、对话 |
| **T5** | 统一 Seq2Seq 架构 | T5、FLAN-T5 | 翻译、摘要、问答 |

---

## 💻 本日代码实战

### 代码文件清单
- code/01_graph_compile.py - LangGraph 图编译示例
- code/02_checkpoint_example.py - Checkpoint 机制
- code/03_streaming_output.py - 流式输出
- code/04_human_in_the_loop.py - 人机交互
- code/05_model_family_comparison.py - 模型家族对比

---

## 📌 本日面试考点（6 道题）

### 基础题（3 道）
1. LangGraph 的图编译原理是什么？相比普通状态机有什么优势？
2. Checkpoint 机制的作用是什么？在什么场景下使用？
3. BERT、GPT、T5 三大模型家族的核心区别是什么？

### 进阶题（3 道）
4. 如何实现流式输出？有哪些注意事项？
5. Human-in-the-loop 的设计模式有哪些？如何优雅地实现？
6. 为什么 T5 采用统一的 Seq2Seq 架构？这种设计的优势是什么？

---

**🚀 让我们开始 Day08 的学习吧！**

---
