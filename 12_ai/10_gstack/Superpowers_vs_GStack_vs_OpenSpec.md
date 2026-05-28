---
name: Superpowers vs GStack vs OpenSpec 对比
description: 三套 AI 开发方法论的定位、边界与组合方式
type: case-study
tags: ["GStack", "Superpowers", "OpenSpec", "方法论对比"]
summary: 本文对比 Superpowers、GStack、OpenSpec 三套方法论：GStack 负责战略与角色协作，Superpowers 负责执行纪律与验证，OpenSpec 负责规格治理与变更追踪。
created_at: 2026-05-28
updated_at: 2026-05-28
---

# Superpowers vs GStack vs OpenSpec 对比

## 一句话定位

- **GStack**：AI 虚拟软件工厂，负责「想清楚做什么、谁来评审、如何交付」。
- **Superpowers**：资深工程师纪律系统，负责「怎么高质量执行」。
- **OpenSpec**：规格治理系统，负责「需求和变更如何被记录、审查、追踪」。

---

## 一、三层模型

```text
战略 / 角色层：GStack
  - Office Hours
  - CEO Review
  - Engineering / Design / QA / Ship 角色

规格 / 治理层：OpenSpec
  - Proposal
  - Spec
  - Tasks
  - Archive

执行 / 质量层：Superpowers
  - Brainstorming
  - TDD
  - Systematic Debugging
  - Verification Before Completion
```

**推荐顺序**：

```text
GStack 定方向
  → OpenSpec 固化范围与变更
  → Superpowers 执行与验证
  → GStack QA / Ship / Retro 收尾
```

---

## 二、适用场景对比

### GStack 更适合

1. 需求模糊，需要从 0 到 1 想清楚；
2. 需要 CEO / PM / 工程 / 设计 / QA 多角色视角；
3. 想做产品而不只是写代码；
4. 需要从想法到发布的完整交付链；
5. 独立开发者需要一个「虚拟团队」。

### Superpowers 更适合

1. 已经知道要做什么，需要稳定落地；
2. 需要 TDD、验证、系统性调试；
3. 需要强制纪律防止 Agent 自作聪明；
4. 工程质量比速度更重要；
5. 需要明确的执行流程和红线。

### OpenSpec 更适合

1. 需求变更频繁；
2. 多人/多 Agent 协作需要共享 spec；
3. 需要知道某个变更为什么发生；
4. 需要 proposal → tasks → archive 的治理链；
5. 希望防止实现和需求腐烂。

---

## 三、优缺点对比

### GStack

**优点**：

1. 角色清晰，能覆盖产品、设计、工程、QA、发布；
2. 对模糊需求特别有效；
3. CEO Review 能主动挑战范围和前提；
4. 适合做 demo、产品、创业型项目。

**缺点**：

1. 若没有工程纪律配合，容易停留在评审和建议；
2. 角色多，初学者可能不知道什么时候用哪个；
3. 对纯底层技术问题可能显得过重。

### Superpowers

**优点**：

1. 纪律强，尤其是 TDD、debugging、verification；
2. 防止「没验证就说完成」；
3. 每个 skill 都有清晰触发条件和红线；
4. 适合严肃工程交付。

**缺点**：

1. 产品方向和商业判断不是重点；
2. 缺少完整角色团队感；
3. 对从 0 到 1 的创意阶段支持不如 GStack。

### OpenSpec

**优点**：

1. 变更可追溯；
2. 适合长期维护；
3. 能把需求、任务、实现关联起来；
4. 对团队协作友好。

**缺点**：

1. 不是角色框架；
2. 不直接提供 TDD / QA / 发布纪律；
3. 小任务可能略显流程重。

---

## 四、组合工作流示例

### 工作流 1：新产品功能

```text
GStack /office-hours：确认真实问题
GStack /plan-ceo-review：挑战范围与 10 星愿景
OpenSpec：写 proposal / spec / tasks
Superpowers writing-plans：生成实施计划
Superpowers TDD + verification：执行
GStack /qa + /ship：交付
```

### 工作流 2：紧急 bug 修复

```text
GStack /guard：开启安全防护
Superpowers systematic-debugging：根因分析
GStack /investigate：补充调查报告与防回归
Superpowers verification-before-completion：验证修复
GStack /qa-only：确认缺陷关闭
```

### 工作流 3：知识库专题建设

```text
GStack /office-hours：确定专题目标与受众
GStack /plan-ceo-review：决定范围扩大或缩减
OpenSpec：记录专题结构和任务
Superpowers writing-plans：拆解为每日学习计划
GStack /retro：复盘学习效果
```

---

## 五、选择口诀

- **还不知道做什么**：先 GStack。
- **已经知道做什么，但怕做歪**：OpenSpec。
- **已经知道怎么做，但怕质量差**：Superpowers。
- **准备上线/发布/复盘**：回到 GStack。

最终组合：

> **GStack 管方向，OpenSpec 管边界，Superpowers 管执行。**
