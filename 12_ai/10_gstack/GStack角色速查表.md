---
name: GStack 角色速查表
description: GStack 常用角色、触发场景、核心流程与交付物速查
type: cheatsheet
tags: ["GStack", "角色", "速查表", "AI Agent"]
summary: 本速查表整理 GStack 角色化软件工厂中的核心角色，包括 Office Hours、CEO Review、工程评审、设计评审、代码审查、QA、发布、监控、安全防护等。
created_at: 2026-05-28
updated_at: 2026-05-28
---

# GStack 角色速查表

## 一、产品与方向层

### `/office-hours` — YC 导师

**什么时候用**：用户有一个想法、需求模糊、想确认是否值得做。

**核心流程**：

1. 判断目标：startup / internal / learning / hackathon / fun；
2. Startup mode 走 YC 六问；Builder mode 找 delight 与最快可展示版本；
3. 挑战前提；
4. 生成 2-3 个方案；
5. 产出 DESIGN.md。

**交付物**：产品设计文档、下一步 assignment。

### `/plan-ceo-review` — CEO / Founder 评审

**什么时候用**：已有 plan，需要挑战方向、范围、10 星愿景。

**核心流程**：

1. Nuclear Scope Challenge；
2. 2-3 个替代方案；
3. 选择四种模式之一：扩张、选择性扩张、保持、缩减；
4. 按 11 个 section 完整审查；
5. 输出 CEO Review Summary。

**交付物**：范围决策、挑战清单、in/out/deferred scope。

---

## 二、规划与设计层

### `/plan-eng-review` — 工程经理

**什么时候用**：要检查技术方案、架构、数据流、测试覆盖。

**关注点**：

1. 架构边界；
2. 数据流；
3. 状态机；
4. 错误边界；
5. 测试矩阵；
6. 隐含假设。

**交付物**：工程评审报告、P0/P1/P2 风险清单。

### `/plan-design-review` — 高级设计师

**什么时候用**：需要评审 UI/UX 方案是否达到可用与美观标准。

**8 个评分维度**：

1. 视觉层级；
2. 一致性；
3. 可用性；
4. 响应式；
5. 无障碍；
6. 加载体验；
7. 错误状态；
8. AI Slop 检测。

**交付物**：设计评分报告、每项改进建议。

### `/design-consultation` — 设计合伙人

**什么时候用**：从 0 到 1 设计产品或页面。

**核心流程**：竞品调研 → 创意风险评估 → 设计系统 → DESIGN.md。

**交付物**：设计系统与产品设计文档。

---

## 三、构建与调试层

### `/review` — Staff Engineer 代码审查

**什么时候用**：提交前、PR 前、重大改动后。

**问题分级**：

- P0：会导致 CI 失败或生产事故；
- P1：性能、安全、内存、可维护性隐患；
- P2：命名、重复、可读性改进。

**交付物**：代码审查报告、自动修复的明确问题。

### `/investigate` — 调试专家

**什么时候用**：bug、报错、行为异常。

**流程**：信息收集 → 假设排列 → 逐一验证 → 定位根因 → 修复 → 防回归。

**硬规则**：同一问题修复失败超过 3 次后停手，汇报卡点。

---

## 四、质量与发布层

### `/qa` — QA 负责人

**什么时候用**：功能完成后，需要完整测试并允许自动修复。

**覆盖范围**：Happy path、error path、edge cases。

**交付物**：QA 报告、修复代码、回归测试用例。

### `/qa-only` — QA 报告员

**什么时候用**：只想知道问题，不希望自动改代码。

**交付物**：缺陷报告、复现步骤、严重程度。

### `/ship` — 发布工程师

**什么时候用**：准备推 PR 或发布。

**流程**：同步主干 → 跑测试 → 检查覆盖率 → 推分支 → 创建 PR。

### `/land-and-deploy` — 合并并部署

**什么时候用**：PR 已准备好上线。

**流程**：合并 PR → 等 CI → 部署 → 烟雾测试 → 必要时 revert。

### `/canary` — SRE 监控

**什么时候用**：部署后观察生产环境是否正常。

**观察项**：console 错误、性能指标、关键页面截图、异常告警。

### `/benchmark` — 性能工程师

**什么时候用**：比较 PR 前后性能。

**指标**：FCP、LCP、CLS、TTI、Bundle Size、Lighthouse Score。

---

## 五、文档、复盘与安全层

### `/document-release` — 技术写作

**用途**：同步 README、ARCHITECTURE、CONTRIBUTING、CHANGELOG、AGENTS/CLAUDE 指南。

### `/retro` — 工程经理复盘

**用途**：周度交付统计、质量趋势、学习总结、下周重点。

### `/careful` — 危险命令警告

**用途**：拦截 `rm -rf`、`DROP TABLE`、`git reset --hard`、`terraform destroy` 等破坏性命令。

### `/freeze` — 编辑锁

**用途**：只允许修改指定目录，防止越界。

### `/guard` — 全面防护

**用途**：同时启用 `/careful` 和 `/freeze`。

---

## 六、典型工作流

### 新功能开发

```text
/office-hours
  → /plan-ceo-review
  → /plan-eng-review
  → /plan-design-review
  → 开发
  → /review
  → /qa
  → /ship
```

### 紧急修复

```text
/guard
  → /investigate
  → /review
  → /qa-only
  → /ship
```

### 设计优化

```text
/design-consultation
  → 实现
  → /design-review
  → /benchmark
```
