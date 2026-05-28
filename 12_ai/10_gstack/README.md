---
name: GStack 学习专题
description: GStack 综合学习入口，覆盖使用者、方法论、开发者三个视角
type: skill-tree
tags: ["GStack", "AI Agent", "软件工厂", "学习计划"]
summary: 本专题围绕 GStack 构建 10 天标准学习路径，学习 YC Office Hours、CEO Review、工程/设计/QA/发布角色流，并横向比较 Superpowers 与 OpenSpec。
created_at: 2026-05-28
updated_at: 2026-05-28
---

# GStack 学习专题

> **定位**：GStack 是一套「AI 虚拟软件工厂」方法论，把软件交付拆成 CEO、YC 导师、工程经理、设计师、Staff Engineer、QA、发布工程师、SRE 等专职角色。

---

## 一、学习目标

本专题采用 **10 天标准综合版**，覆盖三个视角：

### 1. 使用者视角

学会什么时候调用 GStack 的不同角色：

- `/office-hours`：需求拷问，产出设计文档
- `/plan-ceo-review`：CEO/Founder 视角，挑战范围与 10 星愿景
- `/plan-eng-review`：工程评审，检查架构、数据流、错误边界、测试矩阵
- `/plan-design-review` / `/design-review`：设计评分与视觉还原
- `/review` / `/investigate`：代码审查与根因分析
- `/qa` / `/ship` / `/canary`：质量、发布与部署后监控

### 2. 方法论视角

理解 GStack 与其他框架的分工：

- **GStack**：战略层 / 管理层 / 角色团队 / 产品交付
- **Superpowers**：执行层 / 工程纪律 / TDD / 验证
- **OpenSpec**：规格层 / 需求变更治理 / 可追溯 spec

### 3. 开发者视角

学会拆解 GStack skill 的写法，最终能写一个自己的 GStack 风格角色 skill。

---

## 二、核心心智模型

GStack 不是单一工具，而是一套「角色化交付流水线」。

```text
想法 / 模糊需求
  → Office Hours：逼问真实问题与目标用户
  → CEO Review：挑战范围、寻找 10 星产品
  → Engineering / Design Review：把方向变成可执行设计
  → Review / Investigate：构建过程中的质量控制
  → QA / Ship / Canary：交付、发布、监控
  → Retro / Document-release：复盘与知识沉淀
```

一句话：

> **GStack 负责把一个想法变成一支 AI 团队协作交付的流程。**

---

## 三、推荐学习顺序

1. 先读 [学习计划.md](./学习计划.md)
2. 再看 [GStack角色速查表.md](./GStack角色速查表.md)
3. 对比 [Superpowers_vs_GStack_vs_OpenSpec.md](./Superpowers_vs_GStack_vs_OpenSpec.md)
4. 按 [实战练习清单.md](./实战练习清单.md) 做练习
5. 用 [资源索引.md](./资源索引.md) 回到源文件精读

---

## 四、与 09_superpowers 的关系

本专题建议接在 `09_superpowers` 后学习：

- 先用 Superpowers 建立工程纪律；
- 再用 GStack 建立产品与团队角色视角；
- 最后用 OpenSpec / GStack / Superpowers 组合成完整 AI 开发方法论。

推荐组合：

```text
GStack 想清楚做什么
  → OpenSpec 固化变更与边界
  → Superpowers 高质量执行
  → GStack QA / Ship / Retro 完成交付闭环
```
