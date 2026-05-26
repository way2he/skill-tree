
---
name: Day07 FAQ
description: Day07 常见问题解答
type: faq
tags: ["FAQ", "常见问题"]
summary: Day07 常见问题解答
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# Day07 常见问题 FAQ ❓

---

## LangGraph 相关

### Q1：LangGraph 学习路径？

**建议**：
1. 先学 LangChain 基础（概念：LLM、Prompt、Chain）
2. 再学 LangGraph：核心概念 → 简单示例 → 条件边 → Checkpoint
3. 实战：ReAct Agent → 多 Agent 协作

---

### Q2：State 里应该存什么？不要存什么？

**应该存**：
- 对话历史（messages）
- 中间结果（retrieved_docs、tool_results）
- 任务状态（step、is_done、intent）

**不要存**：
- 全局配置（config 单独存）
- 大文件（存路径或 id）
- 冗余字段（能算出来的不要存）

---

## Transformer 相关

### Q3：Transformer 太复杂，背不下来怎么办？

**记忆技巧**：
1. 先记整体架构图
2. 再记每个组件一句话
3. 最后记 3 个高频面试题：
   - Self-Attention 公式
   - 为什么用 LayerNorm
   - Encoder/Decoder 区别

---

### Q4：GPT、BERT、T5 有什么区别？

| 架构 | 代表 | 适用任务 |
|------|------|---------|
| Encoder-only | BERT、ERNIE | 理解类（分类、NER、QA） |
| Decoder-only | GPT、Llama | 生成类（文本生成） |
| Encoder-Decoder | T5、BART | 翻译、摘要 |

---

## ML 基础相关

### Q5：激活函数怎么选？

**建议**：
- 默认 GELU
- 快一点选 ReLU
- 二分类最后一层用 Sigmoid
- 多分类最后一层用 Softmax

---

## 其他

### Q6：Day01-Day07 学完了，Agent 应该掌握到什么程度？

**验收标准**：
1. ✅ 能搭带条件跳转的 LangGraph
2. ✅ 能说清 Transformer 核心组件
3. ✅ 能回答 Day01-Day07 的面试题

---

**还有问题？请随时问！** 🙋
