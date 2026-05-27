---
name: SDD 规范驱动开发方法论
description: 规范驱动开发（Spec-Driven Development）思想、与 TDD/DDD/BDD 的关系及 AI 时代价值
type: concept
tags: ["SDD", "规范驱动开发", "方法论", "TDD", "DDD", "BDD", "AI编程"]
summary: Day 3 学习内容，深入 SDD 方法论的根本思想、3 个层级、对比其他范式
created_at: 2026-05-27
updated_at: 2026-05-27
status: done
quality_score: 92
---

# 03 - SDD 规范驱动开发方法论

> Day 3 学习笔记 · 阶段 B 第一篇 · 不讲 OpenSpec 命令，只讲底层思想

## 🎯 一句话定义

> **SDD（Spec-Driven Development）= 把「规范」当作真理来源（Source of Truth），代码沦为规范的可验证副产物。**

传统开发：需求 → 代码（事实标准）→ 文档（往往过时）
SDD 开发：需求 → **规范（事实标准）** → 代码（可重生成）→ 验证

## 🔥 为什么 AI 时代「突然」需要 SDD？

### 数据驱动的痛点

**METR 2026-02 研究**（业界震撼数据）：
- 开发者使用 AI 编程工具后，**平均速度反而慢了 19%**
- 但他们自我感觉「更快了」（认知偏差）
- 原因：非结构化 prompt → 看似合理的代码 → 边缘 case 漏掉 → 调试循环吞噬节省的时间

### Vibe Coding 陷阱

```
[Vibe Coding 闭环]
prompt → AI 生成 → 看起来对 → 跑起来出错
      ↑                                ↓
      └──── 改 prompt 重试 ←────── debug 2 小时
```

AI 写出来的代码**很像**对，但缺失你「**口头说了但写漏了**」的边界条件、错误处理、副作用约束。

### SDD 的解法

把这些约束**先**写成结构化 spec（机器可读、人类可审），然后：
1. AI 按 spec 生成代码（不是按 prompt 猜）
2. spec 本身可作为 AI 的 system prompt
3. 测试可直接对照 spec 的 Scenario
4. 多 agent 协作时共享同一份 spec（不再各自臆想）

## 📐 SDD 的 3 个层级（来自 OpenReview 论文）

学术论文《Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants》提出 3 级严格度：

| 层级 | 名称 | 规范角色 | 代码角色 | 典型工具 | 适用场景 |
|------|------|----------|----------|----------|----------|
| L1 | **Spec-First** | 写在前面，但不强制 | 主产物 | Cursor `.cursorrules` | 个人快速迭代 |
| L2 | **Spec-Anchored** | 评审基线、变更必同步 | 主产物，但需对齐 spec | OpenSpec / Spec Kit | 团队协作、AI 辅助 |
| L3 | **Spec-as-Source** | 真理来源，code 可重新生成 | 派生物 | Intent / Kiro | 多服务、强一致性 |

**OpenSpec 在哪一级？** → **L2 Spec-Anchored**（半 living）
- 每个 change 用 delta marker（ADDED/MODIFIED/REMOVED）追踪
- archive 时自动合并到正式 spec
- 但代码仍需手工/AI 写，不能从 spec 自动生成

## ⚔️ SDD vs 其他范式

### vs TDD（测试驱动开发）

| 维度 | TDD | SDD |
|------|-----|-----|
| **先写什么** | 测试 | 规范 |
| **表达层次** | 代码级（函数/类） | 需求级（capability） |
| **给谁看** | 开发者自己 | 产品+开发+QA+AI |
| **AI 友好度** | 低（测试代码仍需人写） | 高（结构化 Scenario 可直接喜 LLM） |
| **抱怨点** | 测试难写/调贵 | spec 与实现可能脱节 |

**关系**：SDD 不取代 TDD，而是“求同存异”。很多 SDD 实践者在 spec 的 Scenario 部分直接生成 pytest 用例（顶层 spec 、底层 test）。OpenSpec 的 `#### Scenario: WHEN/THEN` 格式本就是 BDD/Gherkin 风格。

### vs DDD（领域驱动设计）

| 维度 | DDD | SDD |
|------|-----|-----|
| **核心产物** | Ubiquitous Language + Bounded Context | Spec + Capability |
| **粦度** | 重（需领域专家参与） | 轻（markdown 即可） |
| **范围** | 架构级 | 功能级 |
| **思考层次** | “业务领域」 | “系统能力” |

**关系**：DDD 是“架构阶”思考，SDD 是“需求阶”营地。两者可叠加：用 DDD 划 Bounded Context，在每个 Context 内用 SDD 管理 capability。

### vs BDD（行为驱动）

BDD 是 SDD 的“老祖”——Gherkin、Cucumber 都是 BDD 产物。SDD 是 BDD 在 AI 时代的「重生」：
- 保留 Given/When/Then 结构
- 加入「代码可从 spec 生成/验证」这个新维度
- 面向 LLM，而不是面向产品经理

OpenSpec 的 spec 格式本质上是「markdown 版的 Gherkin」。

### vs API Design First（OpenAPI 优先）

| 维度 | API Design First | SDD |
|------|------------------|-----|
| **点​​​​** | API 契约 | 任何能力 |
| **描述语言** | OpenAPI/JSON Schema | Markdown |
| **覆盖面** | 外部接口 | 全部行为 |

**关系**：API Design First 是 SDD 在「接口层」的专明，SDD 覆盖更广（含内部逻辑、错误处理、交互流程）。

## 🏛️ SDD 五大核心原则

### 1. 规范优先，不是代码优先
Spec 是评审、聊天、沟通的中心。代码可以未写，但 spec 必须先有。

### 2. 可验证，不是可读
spec 不是「作文」，是「可测试的奇约」。每个 Requirement 必须能转为 1+ 个 Scenario，每个 Scenario 能转为 1 个测试用例。

### 3. 增量变更，不是重写
Delta marker （ADDED/MODIFIED/REMOVED）是 SDD 的灵魂。每次变更只写「变了什么」，而不是重写整份 spec——才能追踪演进史、支持多人并行。

### 4. 机器可读，不只是人类可读
Markdown 是妥协：人可读 + LLM 可解析。Frontmatter、结构标题、固定关键字（SHALL/MUST/Scenario）都是为了让机器能提取信息。

### 5. 与代码同仓，不是上传到 Confluence
spec 必须跟代码在同一个 git 仓里，与代码一起 review、一起打 tag。放 Confluence/Notion 等于死定。

## ⚠️ 落地 SDD 的五大误区

### 误区 1：把 SDD 当 PRD 写
Spec 不是产品需求文档（PRD）。PRD 是「为什么」主导，Spec 是「是什么」主导。Spec 不讨论商业价值、用户群、竞品分析，只说「系统必须 SHALL 做什么」。

### 误区 2：写得太抽象，变成「依靠能」
“系统 SHALL 提高用户体验” — 这不是规范，是报告项。「用户点击登录按钮后 2 秒内 SHALL 跳转到首页」才是。

### 误区 3：不写 Scenario 只写 Requirement
Requirement 不配 Scenario = 发愿。OpenSpec validate 会报错。Scenario 是「验收条件」的最后一里。

### 误区 4：跟不同步，变「死 spec」
代码改了 spec 不改 = SDD 死亡现场。解决：PR 必须同时含 spec 变更 + 代码变更，不同步不合。OpenSpec 的 archive 机制就是帮你强制同步。

### 误区 5：什么都写 spec
fix typo、重命名变量这种不需要 SDD。适用：新增能力、修改行为、变更接口。原则：「如果 3 个月后别人（含未来的你）要理解『为什么这么写』，就需要 spec」。

## 🎯 SDD 的产业生态（2026 年快照）

以 Augment、2026-03 Thoughtworks Tech Radar 跟踪到的 6 大工具：

| 工具 | spec 类型 | 多 agent | AI 广度 | 定位 | 价格 |
|------|-----------|----------|---------|------|------|
| Intent | living（双向同步） | 协调+专家 | BYOA 4+ | 多服务复杂库 | $60/月 |
| Kiro | static (EARS) | 单 agent | 仅 Claude | AWS 绿场 | 免费 50 券 |
| **GitHub Spec Kit** | static (markdown) | 无 | 8+ agent | 跨 agent 标准 | 免费 |
| **OpenSpec** | semi-living (delta) | 无 | 27+ agent | brownfield 迭代 | 免费 |
| BMAD-METHOD | static (docs) | 12+ 角色 | IDE 无关 | 重型企业 | 免费 |
| Cursor `.cursorrules` | 伪 spec（rules） | 无 | 仅 Cursor | 已在 Cursor 的开发者 | $20/月 |

**OpenSpec 的生态位** ：
- 在 spec 严格度上介于 Spec Kit（全 static）和 Intent（全 living）之间
- 未掌握 AI 选型自由度最高（27 个集成）
- 定位：代码仓本地、开源、企业中型项目首选

## 🧠 Day 3 三大核心心得

### 心得 1：SDD 不是约束，是「解放」
很多人觉得先写 spec 是「束缚手脚」——但约束的是 LLM，解放的是你。AI 按你写好的 spec 生成代码，你不用再一遍遍解释「你理解错了，我要的是 xxx」。

### 心得 2：20% 的功能要写 spec，80% 不用
真的不用每个 commit 都写 spec。**20% 核心功能覆盖 80% 核心成本**，集中精力给核心功能写好 spec，其余的自由调整。

### 心得 3：SDD 不是非此即彼，是分级别渐进
团队不用从 L3 Spec-as-Source 开始。完全可以从「先写 2 句话的 proposal + 1 个 Scenario」开始，慢慢升级到完整流程。「先有」比「完美」重要。

## 相关阅读
- [01-快速上手](./01-快速上手.md) ← 第一个 spec 实例
- [04-Change工作流详解](./04-Change工作流详解.md) ← Day4 拆解每个阶段
- [06-与SpecKit横评](./06-与SpecKit横评.md) ← Day6 对比与 Spec Kit
- [FAQ](./FAQ.md)

---

**Day 3 检查表**：
- [x] 理解 SDD 核心定义、为什么 AI 时代火了
- [x] 分清 SDD 3 个层级（Spec-First / Spec-Anchored / Spec-as-Source）
- [x] 搞懂 SDD vs TDD/DDD/BDD/API Design First 的关系
- [x] 掌握 SDD 5 大原则、5 大落地误区
- [x] 了解 2026 年产业生态 6 大工具、OpenSpec 的定位
", "oldText": "---\nname: SDD 规范驱动开发方法论\ndescription: 规范驱动开发（Spec-Driven Development）思想、与 TDD/DDD 的关系及 AI 时代价值\ntype: concept\ntags: [\"SDD\", \"规范驱动开发\", \"方法论\", \"TDD\", \"DDD\"]\nsummary: Day 3 学习内容，深入 SDD 方法论的根本思想\ncreated_at: 2026-05-27\nupdated_at: 2026-05-27\nstatus: done\nquality_score: 92\n---\n\n# 03-SDD 方法论\n\n> 🚧 占位文件，Day 3 学习时填充\n>\n> 计划耗时：2.5h\n\n## 待填充章节\n1. 什么是 SDD（Spec-Driven Development）\n2. 为什么 AI 时代需要 SDD\n3. SDD vs TDD vs DDD 对比\n4. SDD 的 5 大核心原则\n5. 落地 SDD 的常见误区\n\n## 相关阅读\n- [04-Change工作流详解](./04-Change工作流详解.md)\n- [06-与SpecKit横评](./06-与SpecKit横评.md)\n"}]