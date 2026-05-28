---
name: 14 个 superpowers skill 速查表
description: superpowers 体系 14 个 skill 的一页纸速查
type: cheatsheet
tags: ["superpowers", "速查", "cheatsheet"]
summary: 14 个 superpowers skill 的触发场景、核心要点、红线一页纸速查
created_at: 2026-05-28
updated_at: 2026-05-28
---

# 14 个 superpowers skill 速查表

> 每个 skill 一段：**触发场景 + 核心步骤 + 红线**

---

## A 类：元元技能

### 1. using-superpowers
- **触发**：每次对话开始
- **核心**：在任何 response（含澄清问题）之前，先 invoke 相关 skill
- **红线**：「这是简单问题不用 skill」「我记得这个 skill 内容」都是借口

### 2. writing-skills
- **触发**：创建/编辑/验证 skill
- **核心**：description 要让 agent 主动 invoke；包含 trigger、步骤、红线
- **红线**：description 写成「skill 是干啥的」而不是「什么时候用」

---

## B 类：任务流程三段式

### 3. brainstorming
- **触发**：创造性工作（新功能、新组件、行为修改）前
- **核心**：探索 user intent → requirements → design 三层
- **红线**：跳过直接写代码；走过场不深挖

### 4. writing-plans
- **触发**：有 spec/需求要做多步任务，**且 brainstorm 已完成**
- **核心**：结构化 plan（步骤 + 依赖 + 验证点 + 回滚）
- **红线**：没 brainstorm 就开始写 plan

### 5. executing-plans
- **触发**：手上有一份 written plan 要执行
- **核心**：跨 session 执行 + checkpoint review
- **红线**：跳过 checkpoint 一路狂奔

---

## C 类：工程质量四件套

### 6. test-driven-development
- **触发**：实现任何 feature 或 bugfix
- **核心**：红（失败测试）→ 绿（最小通过）→ 重构
- **红线**：先写实现再补测试；测试粒度太粗

### 7. systematic-debugging
- **触发**：遇到 bug、test 失败、非预期行为
- **核心**：观察 → 假设 → 实验 → 修正，假设必须可证伪
- **红线**：试错碰运气；不写假设直接改代码

### 8. verification-before-completion
- **触发**：准备说「完成了」「修好了」「测试通过」之前
- **核心**：先跑命令拿到证据，再做断言
- **红线**：「应该是好了」「我估计 OK」

### 9. finishing-a-development-branch
- **触发**：实现完成 + 测试通过，需要决定怎么整合
- **核心**：结构化呈现选项（merge / PR / cleanup），让用户决策
- **红线**：未询问就直接 merge

---

## D 类：并行协作

### 10. dispatching-parallel-agents
- **触发**：面对 2+ 独立任务（无共享状态、无顺序依赖）
- **核心**：并行派发，避免串行苦干
- **红线**：把有依赖的任务硬塞并行

### 11. subagent-driven-development
- **触发**：当前 session 内执行有独立任务的 plan
- **核心**：写好任务简报（objective/output/scope/verification）
- **红线**：任务简报模糊；subagent 越权改文件

### 12. using-git-worktrees
- **触发**：feature 工作需要隔离当前 workspace
- **核心**：用 native tools 或 worktree 创建独立工作空间
- **红线**：直接在主分支改大改动

---

## E 类：Code Review

### 13. requesting-code-review
- **触发**：任务完成、major feature、merge 前
- **核心**：主动请求 review 验证是否满足需求
- **红线**：自己审自己不算 review

### 14. receiving-code-review
- **触发**：收到 review 反馈，开始实现建议之前
- **核心**：技术性博弈 — 验证、不盲从、不抗拒
- **红线**：表演性赞同；不验证就改；情绪化反驳

---

## 🎯 三大决策框架

### 框架 1：开工前问自己
1. 是创造性工作吗？→ brainstorming
2. 有 plan 吗？→ writing-plans 或 executing-plans
3. 涉及代码实现？→ test-driven-development
4. 多个独立子任务？→ dispatching-parallel-agents

### 框架 2：遇阻时问自己
1. 是 bug / 异常？→ systematic-debugging
2. 不确定对错？→ verification-before-completion
3. 主分支太杂？→ using-git-worktrees

### 框架 3：收尾前问自己
1. 真的完成了？→ verification-before-completion
2. 要请 review？→ requesting-code-review
3. 怎么 merge？→ finishing-a-development-branch

---

## 📌 优先级口诀

```
User > superpowers > 默认系统
Process > Implementation
Brainstorm > Plan > Execute
Test > Code > Verify > Merge
```

---

*"会用 14 个 skill 不是目标，是 Agent 的基本配置。"*
