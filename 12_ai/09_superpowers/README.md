---
name: superpowers 学习专区
description: Obra/Jesse Han superpowers 元技能体系学习计划与资源索引
type: skill-tree
tags: ["superpowers", "agent", "方法论", "学习计划"]
summary: superpowers 是一套面向 AI Agent 的元技能框架，包含 14 个核心 skill，本目录是 10 天速成学习计划 + 实战练习 + 资源索引
created_at: 2026-05-28
updated_at: 2026-05-28
---

# superpowers 学习专区

> **superpowers 是什么？**
> Obra（Jesse Han）开源的一套面向 AI Agent 的「元技能（meta-skill）」体系。
> 它不教你写代码，而是教 Agent **如何思考、如何拆解任务、如何 TDD、如何 debug、如何复盘**。
> 相当于给 Agent 装上「方法论操作系统」。

---

## 🎯 为什么要学

| 维度 | 学完之前 | 学完之后 |
|------|----------|----------|
| **任务拆解** | 一拍脑袋开干 | brainstorming → writing-plans → executing-plans 三段式 |
| **代码质量** | 边写边调 | TDD 红绿循环 + verification-before-completion |
| **Debug 效率** | 试错碰运气 | systematic-debugging 假设驱动 |
| **多任务协作** | 串行苦干 | dispatching-parallel-agents + subagent-driven-development |
| **Code Review** | 全盘接受 / 抗拒 | requesting/receiving-code-review 技术性博弈 |

---

## 📚 14 个核心 skill 全景图

### A. 元元技能（必读，2 个）
1. **using-superpowers** — 怎么用 skill 体系本身（入口）
2. **writing-skills** — 怎么创建/编辑 skill（最复杂，3213 词）

### B. 任务流程三段式（核心，3 个）
3. **brainstorming** — 创意/需求探索（动手前必做）
4. **writing-plans** — 把需求写成可执行计划
5. **executing-plans** — 跨 session 执行计划 + checkpoint

### C. 工程质量四件套（核心，4 个）
6. **test-driven-development** — TDD 红绿重构
7. **systematic-debugging** — 假设驱动的 debug
8. **verification-before-completion** — 声称完成前必须验证
9. **finishing-a-development-branch** — 分支结束时的整合决策

### D. 协作与并行（进阶，3 个）
10. **dispatching-parallel-agents** — 并行派发独立任务
11. **subagent-driven-development** — 当前 session 内用 subagent 执行
12. **using-git-worktrees** — 用 worktree 做工作空间隔离

### E. Code Review 博弈（进阶，2 个）
13. **requesting-code-review** — 主动请求 review
14. **receiving-code-review** — 收到 review 的处理姿态

---

## 🗓️ 10 天速成计划

> 每天 **1-2 个 skill**，配套实战练习，节奏可调。

| Day | 主题 | 学习内容 | 实战练习 |
|-----|------|----------|----------|
| **Day 1** | 入门 | using-superpowers + 全景认知 | 阅读 14 个 SKILL.md 描述行，画思维导图 |
| **Day 2** | 创意阶段 | brainstorming | 拿一个真实需求走完整 brainstorming 流程 |
| **Day 3** | 计划阶段 | writing-plans | 把 Day2 的需求写成完整 plan |
| **Day 4** | 执行阶段 | executing-plans + verification-before-completion | 用 Day3 的 plan 执行一次小迭代 |
| **Day 5** | TDD | test-driven-development | 写一个小函数，严格红绿重构三步 |
| **Day 6** | Debug | systematic-debugging | 复盘最近一次踩坑，用假设驱动法重做 |
| **Day 7** | 协作并行 | dispatching-parallel-agents + subagent-driven-development | 派发 3 个独立子任务并行处理 |
| **Day 8** | 隔离工作空间 | using-git-worktrees + finishing-a-development-branch | 用 worktree 开一条分支并完整结束 |
| **Day 9** | Code Review | requesting-code-review + receiving-code-review | 给自己代码做一次正式 review |
| **Day 10** | 元能力 | writing-skills + 综合复盘 | 创建一个自己的 skill 并验证 |

---

## 📁 目录结构

```
09_superpowers/
├── README.md                   # 本文件（学习总览）
├── 学习计划.md                 # 10 天详细日程
├── 14个skill速查表.md          # 每个 skill 一页纸速查
├── 实战练习清单.md             # 配套练习与判分标准
└── 资源索引.md                 # 指向本机源文件 + 外部链接
```

---

## 🔗 本机资源位置

| 资源 | 路径 |
|------|------|
| **源 SKILL.md（权威）** | `C:\Users\robotAi\Documents\repo\skill-repo\superpowers\skills\` |
| **knowledge-base 镜像** | `~\Documents\ClawWorksapce\knowledge-base\skills\superpowers-*` |
| **OpenClaw 集成版** | `~\Documents\ClawWorksapce\knowledge-base\skills\using-superpowers` 等 |

---

## ⚙️ 学习方法论

1. **读 + 用** — 每个 skill 必须当天找一个真实场景用一次，光读不算学会
2. **三遍法** — 第一遍速读、第二遍精读边读边记问题、第三遍带着问题查源码
3. **输出倒逼输入** — 每天写一篇「学习笔记 + 实战记录」入库到本目录
4. **复盘机制** — Day10 必须做完整复盘，对照 14 个 skill 评估自己掌握度（0-5 分）

---

## 🎯 学完产出

- [ ] 14 个 skill 速查表（自己整理一份）
- [ ] 10 篇学习笔记 + 实战记录
- [ ] 至少 1 个自创 skill（验证 writing-skills 掌握度）
- [ ] 一次完整的「brainstorm → plan → execute → review → finish」端到端流程实战

---

*"superpowers 不是工具，是给 Agent 装上的肌肉记忆。"*
