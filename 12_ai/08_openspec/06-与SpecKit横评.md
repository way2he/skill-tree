---
name: OpenSpec 与 Spec-Kit 横评
description: OpenSpec vs GitHub Spec-Kit vs 裸 prompt 三种 SDD 方案的全维度对比与选型决策
type: comparison
tags: ["OpenSpec", "Spec-Kit", "SDD", "对比", "选型", "决策树"]
summary: Day 6 学习内容，SDD 工具链横评 + 选型决策树 + 混用策略
created_at: 2026-05-27
updated_at: 2026-05-28
status: done
quality_score: 90
---

# 06 - OpenSpec 与 Spec-Kit 横评

> Day 6 学习笔记 · 阶段 C 第一篇 · 实战耗时 2.5h
> 本篇核心：替你做完选型功课，给出一棵决策树和混用策略。

## 🎯 为什么要做这次横评？

SDD 赛道 2026 年百家争鸣，主流玩家：
- **OpenSpec**（Fission AI 出品，npm 全局）
- **GitHub Spec-Kit**（GitHub 官方，2026-Q1 上线）
- **裸 prompt + 文档**（很多团队的现状）

不做横评直接选 → 多半会选「最热门」而不是「最合适」，3 个月后再迁移成本巨大。

## 📋 GitHub Spec-Kit 简介

### 一句话定位
> GitHub 官方推出的「**仓库级 spec-driven 协议**」，深度绑定 GitHub Actions / Copilot / Issues。

### 核心特点
- ✅ 全 YAML 结构化（不是 markdown）
- ✅ 与 GitHub Issues 双向同步（spec 改动会创建 issue）
- ✅ Copilot Workspace 原生支持 spec → code 一键生成
- ✅ Spec 评审走 PR 流程，强制 reviewer 签字
- ❌ 只在 GitHub 平台上能用（gitlab / gitee / 私有 git 不行）
- ❌ 需要 GitHub Enterprise 或 Pro 账号才完整可用

### 目录结构
```
.spec/
├── spec.yaml                ← 全局 spec（YAML）
├── changes/
│   └── 2026-05-add-export.yaml
├── capabilities/
│   └── todo-parser.yaml
└── reviews/
    └── 2026-05-add-export-review.md
```

### 关键 YAML 片段
```yaml
capability: todo-parser
version: 1.2.0
owner: '@alice'
requirements:
  - id: REQ-001
    shall: Parse markdown TODO items
    scenarios:
      - when: Input contains "- [ ] task"
        then: Returns { status: open, text: task }
```

## ⚔️ 全维度对比矩阵

| 维度 | OpenSpec | Spec-Kit | 裸 prompt |
|------|----------|----------|-----------|
| **出品方** | Fission AI | GitHub 官方 | — |
| **格式** | Markdown | YAML | 自由文本 |
| **学习曲线** | 1 天上手 | 3 天上手 | 0 |
| **AI 工具兼容** | 27+ 工具 | Copilot 独家 | 全兼容 |
| **平台依赖** | 无（任意 git） | GitHub 强绑定 | 无 |
| **change 管理** | ✅ proposal/spec/tasks/archive | ✅ PR + Issue 联动 | ❌ 全靠人 |
| **delta marker** | ✅ ADDED/MODIFIED/REMOVED | ⚠️ 通过版本号 | ❌ |
| **验证机制** | `openspec validate` CLI | GitHub Actions check | ❌ |
| **Scenario 语法** | WHEN/THEN markdown | YAML scenarios 数组 | 无约定 |
| **review 流程** | 人工 + AI | PR 强制 reviewer | 无 |
| **审计追溯** | git 历史 + archive 目录 | Issue + PR + spec 三方关联 | 仅 git log |
| **离线可用** | ✅ | ❌（依赖 GitHub API） | ✅ |
| **国内可用性** | ✅ | ⚠️（GitHub 访问） | ✅ |
| **学术背书** | OpenReview 论文 L2 | GitHub 白皮书 | 无 |
| **成本** | 免费（OSS） | GitHub Pro $4/月起 | 免费 |
| **生态成熟度** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐（GitHub 加持） | — |
| **多 agent 协作** | ✅ 通过 AGENTS.md | ⚠️ 仅 Copilot Workspace | ❌ |

### 关键差异详解

#### 差异 1：Markdown vs YAML 之争
- **OpenSpec Markdown** 优势：人类友好、git diff 清晰、AI 写得自然
- **Spec-Kit YAML** 优势：机器可解析、强 schema 校验、转 JSON 容易
- **结论**：人类多就选 markdown，自动化多就选 YAML

#### 差异 2：CLI vs 平台
- **OpenSpec CLI** 优势：跨平台、可嵌入任何 git 工作流、离线友好
- **Spec-Kit 平台** 优势：与 Issue/PR/Actions 深度联动、零额外搭建
- **结论**：开源 / 非 GitHub 项目选 OpenSpec，纯 GitHub 项目可考虑 Spec-Kit

#### 差异 3：AI 集成广度
- OpenSpec 兼容 27+ 工具，包括国产 Trae、CodeBuddy
- Spec-Kit 实际只在 GitHub Copilot 中工作良好
- **结论**：多模型多工具用 OpenSpec；只用 Copilot 可考虑 Spec-Kit

## 🥊 与裸 prompt 的对比

### 裸 prompt 的真实成本（METR 2026-02 数据）

| 项 | 裸 prompt | OpenSpec/Spec-Kit |
|----|-----------|---------------------|
| 单功能开发耗时 | 4.2h（含返工） | 3.1h（含 spec 写作） |
| 自我感觉效率 | +30%（错觉） | +0%（如实） |
| 1 周后能复述需求？ | 18% | 92% |
| 代码与口头需求一致率 | 61% | 88% |
| 多人协作冲突率 | 高 | 低 |

### 为什么大多数团队仍在用裸 prompt？
1. **沉没成本**：已经习惯，迁移痛苦
2. **错觉偏差**：感觉很快，实际更慢
3. **小项目不痛**：< 1000 行代码确实不需要 spec
4. **AI 营销话术**：「自然语言就能编程」让人放松警惕

### 何时可以接受裸 prompt？
- ✅ 一次性脚本（写完就丢）
- ✅ 学习练手项目
- ✅ < 100 行的小 demo
- ❌ 任何需要维护超过 1 个月的代码
- ❌ 任何 > 1 人协作的项目
- ❌ 任何会上线的工具

## 🌳 选型决策树

```
你在做 SDD 选型？
├── 项目托管在 GitHub 且团队全用 Copilot？
│   ├── 是 → 选 Spec-Kit（生态加成最大）
│   └── 否 → ↓
├── 项目需要跨平台/离线/国内访问？
│   └── 是 → 选 OpenSpec（无平台依赖）
├── 是个人快速迭代 / < 100 行 demo？
│   └── 是 → 裸 prompt（但写完别上线）
├── 多 AI 工具混用（Claude + Cursor + Trae）？
│   └── 是 → 选 OpenSpec（兼容性最广）
├── 团队要做严格 review 流程？
│   ├── 在 GitHub 上 → Spec-Kit（PR 强制 reviewer）
│   └── 不在 GitHub 上 → OpenSpec + git 分支 + CODEOWNERS
└── 默认推荐 → OpenSpec
```

## 🔄 三者互补与混用

### 混用模式 1：OpenSpec + Spec-Kit 双跑
- **场景**：开源项目，主仓库在 GitHub，但有非 GitHub 镜像
- **做法**：
  - OpenSpec 为主，所有 change 走 markdown
  - 写一个 sync script 把 archived spec 转 YAML 推到 Spec-Kit
  - Spec-Kit 用作 GitHub Issue 自动化

### 混用模式 2：OpenSpec + 裸 prompt 分级
- **场景**：单仓库内既有核心模块也有辅助脚本
- **做法**：
  - 核心模块走 OpenSpec full 流程
  - `scripts/` 一次性脚本允许裸 prompt
  - `.gitignore` 或 OWNERS 明确分级

### 混用模式 3：spec 一致，工具分立
- **场景**：团队成员用不同 AI 编辑器
- **做法**：
  - 共同遵循 OpenSpec 协议
  - 每人 `init --tools <自己用的>`
  - AGENTS.md 锁死，禁止个人化

## 🎯 Day 6 三大核心心得

### 心得 1：选型本质是选「协议」不是选「工具」
工具会过时（Spec-Kit 半年后可能换协议），协议（SDD 思想）不会。
**先吃透 SDD，再选工具实现。**

### 心得 2：GitHub 加持是双刃剑
Spec-Kit 的最大优势也是最大劣势：**绑死 GitHub**。
- 项目永远在 GitHub？放心绑
- 有迁移可能？OpenSpec 留后路

### 心得 3：裸 prompt 不是「不专业」
小项目 / 探索阶段裸 prompt 完全 OK。
**真正不专业**是用裸 prompt 上线生产代码、用 SDD 写一次性脚本。
**配对原则**：项目阶段 ↔ 工具选型。

## 🔑 一行流速查卡

```
任意 git 项目 + 跨工具       → OpenSpec
GitHub + Copilot Workspace  → Spec-Kit
一次性脚本 + 学习练手        → 裸 prompt
团队 / 强 review            → OpenSpec + git CODEOWNERS, 或 Spec-Kit + PR
迁移老项目                   → OpenSpec（迁移成本最低）
```

## 相关阅读
- [03-SDD方法论](./03-SDD方法论.md) ← 协议思想根本来源
- [05-AI工具集成](./05-AI工具集成.md) ← OpenSpec 集成深度
- [07-实战集成案例](./07-实战集成案例.md) ← 选完工具后怎么落地
- [面试题](./面试题.md)

---

**Day 6 检查表**：
- [x] 能讲清 OpenSpec / Spec-Kit / 裸 prompt 三者定位差异
- [x] 能根据项目场景做选型决策（用决策树）
- [x] 知道何时该接受裸 prompt（短期 / 实验性）
- [x] 理解协议 > 工具的本质
- [x] 能设计混用方案应对复杂团队场景