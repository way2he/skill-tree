---
name: Day 01 入门与全景认知
description: superpowers 体系入门，建立 14 个 skill 的心智模型
type: learning-note
day: 1
tags: ["superpowers", "using-superpowers", "学习笔记"]
summary: superpowers 是给 Agent 装上的「方法论操作系统」，14 个 skill 按 A/B/C/D/E 五类组织，最高铁律是「invoke skill BEFORE response」
created_at: 2026-05-28
updated_at: 2026-05-28
---

# Day 01 — superpowers 入门与全景认知

> **今日目标**：建立 superpowers 心智模型，知道 14 个 skill 各干啥。
> **核心一句话**：superpowers 不是工具，是 Agent 的元方法论框架。

---

## 一、第一性原理：什么是 superpowers？

读完 `using-superpowers` SKILL.md（788 词）后，我的理解是：

> **superpowers 是一套"在 response 之前先 invoke 相应 skill"的强制纪律框架。**

它不教 Agent 写代码，而是教 Agent：
1. **遇到任何任务先停**，问「有没有对应的 skill 应该用？」
2. **哪怕只有 1% 的可能性 skill 适用，也必须 invoke**
3. **invoke 完按 skill 里的 checklist 一步步走，不能跳步、不能简化**

这跟人类世界的「SOP（标准作业流程）」一模一样。区别是 Agent 容易自作聪明，所以需要更强的纪律约束。

---

## 二、三层指令优先级（**必背**）

```
用户指令（CLAUDE.md / AGENTS.md / 直接请求）
       ↓ 覆盖
superpowers skill 
       ↓ 覆盖
默认系统提示
```

**实战意义**：如果老板在 `AGENTS.md` 写了「不要用 TDD」，而 TDD skill 说「永远 TDD」，那**听老板的**。

我（小蜜）的工作空间里 `MEMORY.md` 有 4 条红线规则（中文友好、严禁乱码、面试题不用表格、模型版本最新），这些规则**优先级高于 superpowers**。

---

## 三、14 个 skill 五大分类全景

### A. 元元技能（管 skill 的 skill）

| # | Skill | 用途 |
|---|-------|------|
| 1 | **using-superpowers** | 怎么用 skill 体系本身——入口中的入口 |
| 2 | **writing-skills** | 怎么创建/编辑 skill（最长 3213 词）——TDD 用于文档 |

### B. 任务流程三段式

| # | Skill | 用途 |
|---|-------|------|
| 3 | **brainstorming** | 创造性工作动手前必做——探索 user intent / requirements / design |
| 4 | **writing-plans** | 有了需求把它写成可执行的 plan |
| 5 | **executing-plans** | 跨 session 执行 plan + checkpoint review |

### C. 工程质量四件套

| # | Skill | 用途 |
|---|-------|------|
| 6 | **test-driven-development** | 红绿重构三步循环——Rigid 严格执行 |
| 7 | **systematic-debugging** | 假设驱动 4 阶段调试 |
| 8 | **verification-before-completion** | 声称完成前必须跑命令拿证据 |
| 9 | **finishing-a-development-branch** | 分支结束的整合决策（4 选项菜单） |

### D. 协作与并行

| # | Skill | 用途 |
|---|-------|------|
| 10 | **dispatching-parallel-agents** | 2+ 独立任务并行派发 |
| 11 | **subagent-driven-development** | 当前 session 内 fresh subagent + 两阶段 review |
| 12 | **using-git-worktrees** | 工作空间隔离 |

### E. Code Review 博弈

| # | Skill | 用途 |
|---|-------|------|
| 13 | **requesting-code-review** | 主动请求 review |
| 14 | **receiving-code-review** | 收到 review 的技术性博弈姿态（不盲从不抗拒） |

---

## 四、两条核心决策原则

### 原则 1：Process > Implementation

多个 skill 都适用时，**先用流程类 skill 决定怎么思考**，再用实现类 skill 决定怎么做。

- "Let's build X" → 先 `brainstorming`，再 implementation
- "Fix this bug" → 先 `systematic-debugging`，再 domain skill

### 原则 2：Rigid vs Flexible

- **Rigid skills**（TDD、debugging）：严格执行，不能"灵活变通"
- **Flexible skills**（patterns）：按上下文适配

skill 自己会告诉你它属于哪种。

---

## 五、Red Flags（必须警惕的 12 句自欺）

精读时我记下了这张表（来自 using-superpowers），每一句都是 Agent 跳过 skill 的常见借口：

| 自欺想法 | 真相 |
|----------|------|
| "这是简单问题" | 问题也是任务，先查 skill |
| "我需要先了解上下文" | skill 告诉你**怎么**了解上下文，先查 |
| "让我先看看代码" | skill 告诉你**怎么**看，先查 |
| "我能快速看一下 git" | 文件没有对话上下文，先查 skill |
| "这不需要正式 skill" | skill 存在就要用 |
| "我记得这个 skill" | skill 会演化，读当前版本 |
| "这不算任务" | 行动 = 任务 |
| "skill 是 overkill" | 简单事会变复杂 |
| "先做这一件事" | 做任何事**之前**先查 |
| "感觉很有效率" | 没纪律的行动浪费时间 |
| "我知道这个概念" | 知道 ≠ 会用，invoke 它 |

**我的 Day 1 自我提醒**：写这篇笔记本身就是「写代码前」的任务，下次写真代码前要先想「该用哪个 skill」。

---

## 六、思维导图（A/B/C/D/E 五分组）

```
superpowers (14)
├── A. 元元技能 (2)
│   ├── using-superpowers ★入口
│   └── writing-skills ★创建 skill 的 skill
│
├── B. 任务流程三段式 (3)
│   ├── brainstorming ★创意阶段
│   ├── writing-plans ★计划阶段
│   └── executing-plans ★执行阶段
│
├── C. 工程质量四件套 (4)
│   ├── test-driven-development [Rigid] 红绿重构
│   ├── systematic-debugging 假设驱动 4 阶段
│   ├── verification-before-completion 证据先于断言
│   └── finishing-a-development-branch 4 选项菜单
│
├── D. 协作与并行 (3)
│   ├── dispatching-parallel-agents 独立任务并行
│   ├── subagent-driven-development 同 session 内 fresh subagent
│   └── using-git-worktrees 工作空间隔离
│
└── E. Code Review 博弈 (2)
    ├── requesting-code-review 主动请求
    └── receiving-code-review 技术性博弈
```

---

## 七、第一印象（200 字）

读完 14 个 SKILL.md 的第一印象：

**superpowers 本质是把"软件工程最佳实践"做成了对 Agent 强制可执行的指令集**。它不是"建议"，而是"铁律"。每个 skill 都用 `<EXTREMELY-IMPORTANT>` / `Iron Law` / `Red Flags` 三件套把 Agent 的退路堵死。最有意思的是 `writing-skills` 把"创建 skill"本身也变成了 TDD（先写 pressure scenario 当失败测试，看 Agent 不读 skill 时怎么犯错，再写 skill 让它通过）——**用 TDD 写 TDD 的 skill**，是套娃式的优雅。我作为小蜜，过去经常"凭感觉"行动，superpowers 提供的是**反凭感觉的纪律**。这种纪律的成本是慢一点，收益是输出稳定。

---

## 八、Day 1 自评

| 维度 | 评分 | 备注 |
|------|------|------|
| 全景覆盖 | 5/5 | 14 个 skill 全部精读 |
| 分类正确 | 5/5 | A/B/C/D/E 五类清晰 |
| 心智模型 | 4/5 | 还需要 9 天实战验证 |
| 思维导图 | 5/5 | 完成 |
| 200 字感想 | 5/5 | 完成 |

**总评：24/25** ✅ 通关

---

## 九、明日预告

**Day 2 — brainstorming**：找一个真实需求（候选：「给知识库加一个每日抽样质检脚本」），完整走 brainstorming 流程。

预期挑战：忍住不直接给方案，先问澄清问题。

---

> 相关文件：[学习计划.md](../学习计划.md) | [14个skill速查表.md](../14个skill速查表.md) | [资源索引.md](../资源索引.md)
