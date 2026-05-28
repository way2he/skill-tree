---
name: Day 07 并行 + Subagent 实战
description: dispatching-parallel-agents + subagent-driven-development 协作模式
type: learning-note
day: 7
tags: ["superpowers", "dispatching-parallel-agents", "subagent-driven-development", "学习笔记"]
summary: 独立任务并行派发能省一半时间; subagent 同 session fresh context + 两阶段 review (spec → quality) 是高质量执行的最佳模式
created_at: 2026-05-28
updated_at: 2026-05-28
---

# Day 07 — 并行派发 + Subagent 驱动开发

> **核心区分**:
> - **dispatching-parallel-agents**: 调度 2+ 独立任务并行 (重点在并行)
> - **subagent-driven-development**: 同 session 内 fresh subagent per task + 两阶段 review (重点在质量)

---

## 一、双 skill 精读

### 1.1 dispatching 适用判断

```
Multiple failures?
  └─ 独立吗?
       ├─ no (related) → 单 agent 一起查
       └─ yes → 能并行吗?
                  ├─ no (shared state) → 串行
                  └─ yes → PARALLEL DISPATCH
```

**用**: 3+ test 文件失败原因不同 / 多子系统独立坏 / 多调研任务无依赖
**不用**: failures 相关 (修 A 可能也修 B) / 需理解全系统 / 探索性 debug / 共享 state 会冲突

### 1.2 subagent 任务简报四要素

每个 subagent 任务必须包含:
1. **Specific scope** (one test file or subsystem)
2. **Clear goal** (make these tests pass)
3. **Constraints** (don't change other code)
4. **Expected output** (return summary of what found and fixed)

### 1.3 subagent 4 种返回状态

| Status | 处理 |
|--------|------|
| DONE | 转 spec 审查 |
| DONE_WITH_CONCERNS | 看 concern; 影响正确性就先修 |
| NEEDS_CONTEXT | 补 context 再 dispatch |
| BLOCKED | 评估: context 不够 → 补; 推理不够 → 升级 model; task 太大 → 拆; plan 错 → 升级人 |

### 1.4 subagent 两阶段 review (顺序不可换)

```
implementer 实现 → spec reviewer (是否满足 spec) → 通过 → code quality reviewer (代码质量) → 通过 → 标完成
```

**禁忌**: 在 spec 通过前就开始 code quality review. 顺序错了.

### 1.5 model 选择策略

按任务复杂度选最便宜能完成的:
- 1-2 文件机械实现 → cheap model
- 多文件集成 → standard model
- 设计 / 跨码库理解 → most capable model

---

## 二、实战: 并行调研 3 个 markdown lint 工具

### 任务设计 (验证独立性)

| 子任务 | 独立性 |
|-------|-------|
| A. 调研 markdownlint-cli2 | 工具 A 文档, 无依赖 |
| B. 调研 textlint | 工具 B 文档, 无依赖 |
| C. 调研 vale | 工具 C 文档, 无依赖 |

✅ 真独立: 不读对方文档, 不写同一文件, 无共享 state.

### Subagent 简报模板

每个 subagent 我会这样发:

```
**Scope**: 调研 markdownlint-cli2 用于知识库 (Windows + Python 3.12)
**Goal**: 输出 200 字以内 evaluation, 含: 安装方式 / 中文 frontmatter 支持 / 常用规则 / 跟知识库需求匹配度 1-5 分
**Constraints**:
  - 只调研, 不修改任何文件
  - 不安装 (只查文档)
  - 不读其他子任务的产出
**Expected output**:
  - 一段 markdown, 5 个 section
  - 末尾给出 "推荐/不推荐" 结论 + 理由
```

### 派发模式 (本笔记是离线学习, 实际派发省略)

```
sessions_spawn(task=A_prompt, runtime="subagent", mode="run", taskName="md_a")
sessions_spawn(task=B_prompt, runtime="subagent", mode="run", taskName="md_b")
sessions_spawn(task=C_prompt, runtime="subagent", mode="run", taskName="md_c")
sessions_yield()  # 等三个完成
```

### 整合 (假设 3 个返回完毕)

1. 读三份 summary
2. 检查 conflicts (没有, 因独立)
3. 横向对比: 装机难度 / 中文 / 规则丰富度 / 推荐分
4. 选 top 1 写决策记录到 memory/active/decisions.md

---

## 三、subagent-driven-development 流程对照

如果不是并行调研, 而是按 Day 3 plan 执行 7 个 task, 用 SDD 流程:

```
Read plan once
  └─ Extract 7 tasks (full text + context)
  └─ Create TodoWrite

For each task:
  ├─ Dispatch implementer subagent (with full task text + context)
  ├─ implementer asks questions? → 答 → re-dispatch
  ├─ implementer 实现 / 测试 / commit / self-review → DONE
  ├─ Dispatch spec reviewer → 通过?
  │     └─ no: implementer 修 spec gap → re-review
  ├─ Dispatch code quality reviewer → 通过?
  │     └─ no: implementer 修 quality issue → re-review
  └─ Mark task complete

After all:
  └─ Dispatch final code reviewer (整体)
  └─ Use finishing-a-development-branch
```

### 关键纪律

- **No 并行 implementer** (会冲突)
- **No 跳过 review**
- **No 让 implementer 自己审 (self-review 不能替代独立 reviewer)**
- **Continuous execution** — 不要每个 task 后问老板 "继续吗", 老板说执行就执行到底

---

## 四、Day 7 反思

### 并行的最大坑
**误判独立性**. 看起来独立的任务实际共享某 config 或某 import, 并行后写入冲突. **判定时必须列出所有写入路径**, 重叠就不并行.

### subagent 优势
- Fresh context (主 session 不被 task 细节污染)
- 强制写好任务简报 (光是写 "scope / goal / constraints / output" 这 4 段就帮你想清楚 50%)
- 两阶段 review 防止 "差不多就行"

### 跟 dispatching 的关键差别
- dispatching = 多个**独立**任务并行 (横向)
- SDD = 一个 plan 里的多个 task 串行执行, 每个 task 派 fresh subagent (纵向)

---

## 五、Day 7 自评

| 维度 | 分 |
|------|---|
| 独立性判断准确 | 5/5 (列出写入路径) |
| 任务简报 4 要素 | 5/5 |
| 理解 4 种 status 处理 | 5/5 |
| 知道 review 顺序不能换 | 5/5 |
| 区分 dispatching vs SDD | 5/5 |

**总评: 25/25** ✅ 满分