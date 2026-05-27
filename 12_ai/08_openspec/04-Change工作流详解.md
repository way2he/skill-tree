---
name: OpenSpec Change 工作流详解
description: proposal/spec/design/tasks/archive 五阶段工作流深度解析
type: tutorial
tags: ["OpenSpec", "Change", "工作流", "proposal", "archive"]
summary: Day 4 学习内容，深挖 OpenSpec 核心工作流
created_at: 2026-05-27
updated_at: 2026-05-27
status: done
quality_score: 94
---

# 04 - Change 工作流详解

> Day 4 学习笔记 · 阶段 B 核心篇 · 对应 Day1 Demo A 完整流程
> 配套实例：Day1 Demo A 的 `add-parser` change 全程产物
## 🎯 什么是 Change？

Change = **一次独立、完整、可审查、可回滚的需求交付单元**。

等价于：
- JIRA 里的一个 Story
- PRD 里的一个 Feature
- 一次完整的 Feature 开发 PR
- OpenSpec 里的 `openspec new change <name>` 产物

**每个 Change 必须是原子的**：要么全做，要么不做，不能一半。

举几个例子：
✅ 是 Change：新增「导出 JSON 格式」能力
✅ 是 Change：修复「中文文件名解析失败」Bug
❌ 不是 Change：「随便改几个函数名」（没有明确的 spec，纯重构需单独管理）
❌ 不是 Change：「优化性能」（模糊不清，需明确是「解析速度提升 2 倍」这类可验证的要求）

## 📜 Change 五阶段全流程

```
    [proposal] → [specs] → [design] → [tasks] → [archive] → [合并到全局 specs]
        ↓          ↓          ↓          ↓          ↓
  为什么做？  做什么？    怎么实现？  分步走？    完成合并
```

OpenSpec 用 `status` 命令自动告诉你当前阶段和阻塞：
```
Change: add-export
Schema: spec-driven
Progress: 0/4 artifacts complete

[ ] proposal
[-] design (blocked by: proposal) ✅ 自动提示下一个阶段
[-] specs (blocked by: proposal)
[-] tasks (blocked by: design, specs)
```

## 🔍 各阶段深度拆解

### 阶段 1：Proposal（为什么做？）
**目标**：对齐“要不要做”的共识，不用写细节。

#### 模板（从 `openspec instructions proposal <change>` 导出）：
```markdown
## Why
1-2 句话讲清楚痛点、机会、业务价值。

## What Changes
- 新增/修改/删除什么能力？具体描述。

## Capabilities
### New Capabilities
- `能力名-小蛇形`：一句话说明是什么。

### Modified Capabilities
- `现有能力名`：要改什么。

## Impact
- 新增依赖？影响什么代码？会不会破坏现有功能？
```

#### 检查清单（✅ 必须全过）：
- [ ] 没有模糊的“优化”“增强”这类词
- [ ] Capabilities 列表清晰，每个对应 1 个 spec 文件
- [ ] 影响范围明确

**反例**：“Why：提升用户体验，What Changes：优化功能” — 全是废话。

---

### 阶段 2：Specs（做什么？）
**目标**：精确、可验证地定义“做什么”，不讲“怎么实现”。

#### 模板：
```markdown
## ADDED/MODIFIED/REMOVED Requirements

### Requirement: 需求名称
系统 SHALL/MUST 做什么。

#### Scenario: 场景名称
- **WHEN** 什么触发条件
- **THEN** 必须是什么结果
```

#### 核心规则：
1. **Requirement 必须用 SHALL/MUST**：没有“应该”“可能”这种模糊词
2. **每个 Requirement 至少 1 个 Scenario**：没有 Scenario 的不算数
3. **Scenario 用 WHEN/THEN 双段式**：明确输入输出，可直接转为测试用例
4. **禁止写实现细节**：不要出现“用正则表达式”这类内容，那是 Design 阶段的事

---

### 阶段 3：Design（怎么实现？）
**目标**：可选阶段。复杂变更、跨团队、涉架构变更才需要。

#### 何时写？
- 单变更代码量 > 500 行
- 会改到公共模块
- 跨团队依赖
- 会影响数据库或外部 API

#### 设计内容：架构图、接口定义、依赖选型、数据库变更、边界条件处理

---

### 阶段 4：Tasks（分步走？）
**目标**：拆成可执行、可检查的任务清单。

#### 模板：
```markdown
## 1. 模块名
- [ ] 1.1 做什么子任务
- [ ] 1.2 做什么子任务

## 3. 验收
- [ ] 3.1 什么验收条件
- [ ] 3.2 `openspec validate` 必须通过
```

**要求**：每个任务不超过 2 小时工作量，完成后可打勾。

---

### 阶段 5：Archive（合并归档）
**目标**：把 change 合并到全局 spec 库，归档变更历史。

#### 触发条件：
- 代码合并到主分支、测试通过、文档更新完毕、`validate` 通过

#### 自动执行：
1. 把 change 从 `changes/<name>` 移到 `changes/archive/YYYY-MM-DD-<name>`
2. ADDED 的 capability 合并到 `openspec/specs/<capability>/spec.md`这个文件会被创建
3. MODIFIED 的 capability 在现有 spec 文件里更新对应 Requirement
4. REMOVED 的 capability 在 spec 文件里标记废弃

#### 检查：
```
openspec list --specs   # 看新 capability 有没有出现在列表
openspec show <capability>  # 看合并后的全趌 spec
```

## 📖 Demo A `add-parser` 全程走读

### Step 1: Proposal—“Why + What + Capabilities + Impact”
示例产物 `proposal.md`：
```markdown
## Why
知识库每天产出大量 markdown 笔记，文中散落着 - [ ] TODO 但没有统一汇总工具。

## What Changes
- 新增 `mdtodo` Python 工具
- 提取所有 - [ ] 未完成项与 - [x] 已完成项
- 输出 JSON / 控制台表格两种格式

## Capabilities
### New Capabilities
- `todo-parser`：解析单个 markdown 文件中的 TODO 项

## Impact
- 仅 Python 标准库，不影响现有任何工具
```

### Step 2: Specs—“Requirement + Scenario”
示例产物 `specs/todo-parser/spec.md`：
```markdown
## ADDED Requirements

### Requirement: 解析 Markdown 文件提取 TODO 项
系统 SHALL 读取指定的 markdown 文件，提取所有形如 - [ ] 或 - [x] 的待办/已完成项。

#### Scenario: 文件含未完成 TODO
- **WHEN** 输入 markdown 包含 `- [ ] 写测试`
- **THEN** 返回项包含 `{status: "open", text: "写测试"}`
```

### Step 3: Tasks—“分步任务清单”
示例产物 `tasks.md`：
```markdown
## 1. 实现核心解析器
- [ ] 1.1 创建 `mdtodo/__init__.py`
- [ ] 1.2 实现 `parse_file(path: Path) -> list[TodoItem]`

## 2. 单元测试
- [ ] 2.1 创建 `tests/test_parser.py`
- [ ] 2.2 覆盖 spec 中 5 个 Scenario
```

### Step 4: Archive—合并
```
openspec archive add-parser --yes
```
此后：
- `openspec list` 插 add-parser 从活动列表消失
- `openspec list --specs` 出现 `todo-parser`
- `openspec show todo-parser` 看到完整 spec、不可再改

## 🔗 多 Change 依赖与冲突管理

### 依赖场景
Change A 新增 `user-auth` capability
Change B 依赖 `user-auth` 才能写 `user-profile`

### 推荐策略：**串行**
- B 的 proposal 明确说明“依赖 A 完成后才能开始”
- A 先 archive，再开始 B 的实现
- 避免同时修改同一个 capability

### 冲突场景
Change A 和 B 都修改 `user-auth`？

### 推荐策略：**合并为一个 change**
- 拆开修改同一 capability 会导致 archive 后覆盖问题
- 合并后统一 proposal、统一 review

### 多人并行场景
使用 git 分支，每个 change 一个分支：
```
branch add-export   → change add-export
branch add-stats    → change add-stats
```
archive 容易冲突的是 `openspec/specs/<capability>/spec.md`，质量门禁要求：**同一 capability 同一时间只能有一个 active change 在修改**。

## 🎯 Day 4 三大核心心得

### 心得 1：Change 原子性是生命线
拆得太大会让 review/rollback 都难。一个原则：**一个 change 能在 1-3 天完成**。超过的必须拆。

### 心得 2：Spec 禁止写“怎么实现”是铁律
Day1 我写 spec 时合不拢“用正则匹配”，被 `validate` 提醒改了。记住：spec 是契约，代码实现是契约的一种可能。

### 心得 3：Archive 是一道单向门
Archive 后的 change 不能再改，`show` 也查不到。要改只能新建一个 change 去修改 capability。**这个设计后果**是：阐述历史变化只能看 spec 里的 modification history，不是某个独立的 changelog。反过来鼓励在 spec 里加“变更原因”注释。

## 🔑 全流程一行流速查卡

```
openspec new change <name>             创建 change
openspec status --change <name>        看下一步
openspec instructions proposal --change <name>   拿 proposal 模板
# (手动写 proposal.md)
openspec instructions specs --change <name>      拿 specs 模板
# (手动写 specs/<cap>/spec.md）
openspec validate <name>                          验证依赖、结构、格式
# (写代码、跑测试、PR、合并代码)
openspec archive <name> --yes                     合并 spec + 归档 change
openspec list --specs                              验证合并成功
```

## 相关阅读
- [01-快速上手](./01-快速上手.md) ← 实际走过闭环
- [02-命令速查](./02-命令速查.md) ← 相关命令全集
- [03-SDD方法论](./03-SDD方法论.md) ← 为什么需要这套流程
- [FAQ](./FAQ.md)

---

**Day 4 检查表**：
- [x] 理解 Change 作为原子需求单元的重要性
- [x] 能独立完成五个阶段的产物写作
- [x] 掌握 SHALL/Scenario/Delta 的格式约束
- [x] 能区分何时写 Design、何时不写
- [x] 了解多 Change 依赖与冲突管理策略