---
name: OpenSpec 7 天学习计划
description: 由浅入深熟练掌握 OpenSpec 规范驱动开发框架的完整学习路径
type: index
tags: ["OpenSpec", "SDD", "规范驱动开发", "学习计划", "AI编程"]
summary: OpenSpec 7 天学习计划主入口，覆盖工具上手、方法论吃透、对比研究与实战集成三个阶段
created_at: 2026-05-27
updated_at: 2026-05-27
---

# 🚀 OpenSpec 7 天学习计划

> 由浅入深，从安装上手到方法论吃透，再到对比研究与实战集成。
>
> **设计文档**：`docs/superpowers/specs/2026-05-27-openspec-learning-plan-design.md`

---

## 🎯 学习目标

学完后能：
1. ✅ 独立使用 OpenSpec 管理任意项目的 change/spec/archive 全流程
2. ✅ 理解 SDD（规范驱动开发）思想，能向他人讲清「为什么需要」
3. ✅ 在 Claude Code / Cursor / Trae 等 AI 编辑器中配置并使用 OpenSpec
4. ✅ 对比 OpenSpec / Spec-Kit / 裸 prompt 三种方案，做出合理选型
5. ✅ 把 OpenSpec 集成进真实项目（demo：`kb_git_commit.py` 升级）

---

## 📅 7 天进度看板

| 天 | 阶段 | 笔记 | 状态 | 评分 |
|----|------|------|------|------|
| Day 1 | 🟢 A·上手 | [01-快速上手](./01-快速上手.md) | ⏳ 未开始 | — |
| Day 2 | 🟢 A·上手 | [02-命令速查](./02-命令速查.md) | ⏳ 未开始 | — |
| Day 3 | 🟡 B·方法论 | [03-SDD方法论](./03-SDD方法论.md) | ⏳ 未开始 | — |
| Day 4 | 🟡 B·方法论 | [04-Change工作流详解](./04-Change工作流详解.md) | ⏳ 未开始 | — |
| Day 5 | 🟡 B·方法论 | [05-AI工具集成](./05-AI工具集成.md) | ⏳ 未开始 | — |
| Day 6 | 🔴 C·对比 | [06-与SpecKit横评](./06-与SpecKit横评.md) | ⏳ 未开始 | — |
| Day 7 | 🔴 C·实战 | [07-实战集成案例](./07-实战集成案例.md) | ⏳ 未开始 | — |

**总耗时**：17.5 小时（可碎片化分摊 7 个工作日）

---

## 📖 内容地图

### 🟢 阶段 A：工具上手（Day 1-2）
- **[01-快速上手](./01-快速上手.md)** — 安装、init、目录结构、第一个 spec（含 Demo A 启动）
- **[02-命令速查](./02-命令速查.md)** — 全部 CLI 命令 + 工作流图 + 快捷键

### 🟡 阶段 B：方法论吃透（Day 3-5）
- **[03-SDD方法论](./03-SDD方法论.md)** — 规范驱动开发思想、与 TDD/DDD 关系、AI 时代价值
- **[04-Change工作流详解](./04-Change工作流详解.md)** — proposal/spec/design/tasks/archive 五阶段深挖
- **[05-AI工具集成](./05-AI工具集成.md)** — Claude Code/Cursor/Trae/Codex 集成对比

### 🔴 阶段 C：对比与实战（Day 6-7）
- **[06-与SpecKit横评](./06-与SpecKit横评.md)** — OpenSpec vs Spec-Kit vs 裸 prompt 对比矩阵
- **[07-实战集成案例](./07-实战集成案例.md)** — 集成进 `kb_git_commit.py` 实测

### 📚 配套资料
- [FAQ](./FAQ.md) — 10 个常见问题汇总
- [面试题](./面试题.md) — 8 道题（含答案）

---

## 🧪 配套 Demo

### Demo A：Markdown TODO 解析器
- 📁 `demo/markdown-todo-parser/`
- 🎯 ~200 行 Python 工具，完整走通 OpenSpec 4 个 change 流程
- 🚀 Day 1 启动，贯穿 Day 1-2

### Demo B：kb_git_commit.py 升级
- 📁 `demo/kb-git-commit-upgrade/`
- 🎯 用 OpenSpec 给现有工具规划 3 个 change（不强求实现）
- 🚀 Day 7 实战

---

## ✅ 验收标准

每篇笔记：
- Frontmatter 完整、至少 1 个代码示例 + 1 张流程图、末尾「相关阅读」、质量评分 ≥ 80

整体：
- 7 篇 + README + FAQ + 面试题全齐
- 2 个 demo 可运行
- 最终 commit 一次（`python kb_git_commit.py`）

---

## 🔗 相关阅读

- **设计文档**：`docs/superpowers/specs/2026-05-27-openspec-learning-plan-design.md`
- **同源参考**：`raw/skill-tree/17_20天Agent开发速成/` — 7 天结构灵感来源
- **OpenSpec 官方**：https://intent-driven.dev
- **GitHub Spec-Kit**：https://github.com/github/spec-kit
