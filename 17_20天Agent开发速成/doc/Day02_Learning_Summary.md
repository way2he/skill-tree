# Day 02 学习总结 - 20天Agent开发速成

**学习日期**: 2026年5月20日  
**学习时长**: 约2-3小时  
**状态**: ✅ 已完成

---

## 📚 今日学习内容

### 1. Prompt 工程核心知识点

#### 角色设定 (Role Prompting)
- 通过角色设定激活大模型的领域知识
- 示例：资深软件架构师、数据结构化专家
- 关键：明确角色背景、职责、专业领域

#### 思维链 (Chain of Thought, CoT)
- 让模型"说出"思考过程，提高推理准确性
- Zero-shot CoT: "请一步步思考"
- Few-shot CoT: 提供思考示例

#### Few-shot 学习
- 给模型几个示例，让它学习模式和格式
- 适用于：格式控制、风格模仿、任务理解

### 2. 注意力机制深度解析

#### 多头注意力 (Multi-Head Attention)
- Q/K/V 机制：Query查什么，Key标签，Value内容
- 多头并行：不同头关注不同语义关系
- 公式：`Attention(Q,K,V) = softmax(QK^T/√d_k) × V`

#### FlashAttention
- 问题：标准注意力 O(N²) 内存复杂度
- 解决：分块计算 + 重计算策略
- 效果：支持 100K+ 长上下文

#### 位置编码
- **RoPE**: 旋转位置编码，外推性好
- **ALiBi**: 线性偏置，训练稳定，外推性极强

### 3. 实战任务完成情况

| 任务 | 状态 | 产出 |
|------|------|------|
| 代码审查 Agent | ✅ | `Day02_CodeReview_Agent.py` |
| JSON 输出控制 | ✅ | `Day02_JSON_Output_Control.py` |
| 提示注入防护 | ✅ | `Day02_Prompt_Injection.py` |

### 4. 配套知识

#### 过拟合与正则化在 Agent 中的应用
| ML概念 | Agent对应 | 解决方案 |
|--------|-----------|---------|
| 过拟合 | Prompt过度优化特定场景 | 多样化测试用例 |
| L1正则 | 精简Prompt | 只保留核心指令 |
| L2正则 | 平滑Prompt | 使用温和措辞 |
| Dropout | 增强鲁棒性 | 测试时移除部分约束 |

### 5. 算法热身

**Leetcode 125. 验证回文串**
- 双指针法：O(n)时间，O(1)空间
- Pythonic法：过滤后比较
- 核心技能：字符串处理（Prompt工程天天用）

---

## 🎯 今日收获

### 核心技能
1. ✅ 能写出高质量的系统提示词
2. ✅ 能控制大模型稳定输出JSON
3. ✅ 理解5种提示注入攻击及防护
4. ✅ 理解注意力机制原理

### 代码产出
- 代码审查 Agent 完整实现
- JSON输出控制工具类
- 提示注入检测与防护工具
- 回文判断算法（双指针）

### 理论提升
- 理解Transformer注意力机制
- 了解长上下文处理技术
- 掌握Prompt安全防护策略

---

## 🤔 遇到的问题与解决

### 问题1: 提示词中的特殊字符导致Python语法错误
**解决**: 避免在字符串中使用可能引起混淆的特殊字符组合，使用转义或替换表述

### 问题2: JSON输出格式不稳定
**解决**: 
- 明确的角色设定
- 详细的Schema定义
- Few-shot示例
- 输出验证机制

---

## 📁 今日产出文件

```
knowledge-base/
├── Day02_CodeReview_Agent.py      # 代码审查Agent
├── Day02_code_review_result.json   # 审查结果示例
├── Day02_JSON_Output_Control.py    # JSON输出控制
├── Day02_json_prompts.json         # 提示词模板
├── Day02_Prompt_Injection.py       # 提示注入攻防
├── Day02_Leetcode_125.py           # 算法热身
└── Day02_Learning_Summary.md       # 本总结
```

---

## 🚀 明日预告

**Day 03: 大模型 API 深度使用 + MCP 协议 + 模型微调入门**

- OpenAI API 完整使用指南
- 国产模型对比（DeepSeek/Qwen/通义千问）
- Token 计费与成本估算
- MCP (Model Control Protocol) 入门
- 模型微调基础：SFT、LoRA

---

## 💡 学习心得

> Prompt 工程是 Agent 开发的核心技能，好的提示词能让模型性能提升数倍。
> 
> 今天的学习让我理解了：
> 1. 为什么角色设定如此重要 - 它激活了模型的特定知识领域
> 2. 为什么需要 Few-shot - 它让模型理解期望的输出格式
> 3. 安全防护的重要性 - Agent 上线必须考虑提示注入攻击
> 
> 注意力机制的学习让我对大模型的工作原理有了更深的理解，
> 特别是 FlashAttention 如何解决长上下文问题。

---

**打卡完成！** 🎉
