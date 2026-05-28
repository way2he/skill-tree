---
name: Day 02 brainstorming 实战
description: 用 brainstorming 流程探索「知识库每日抽样质检脚本」需求
type: learning-note
day: 2
tags: ["superpowers", "brainstorming", "需求探索", "学习笔记"]
summary: brainstorming 不是头脑风暴，是结构化的需求挖掘——探索 user intent → propose 2-3 approaches → 写 spec → 用户审核 → 转 writing-plans
created_at: 2026-05-28
updated_at: 2026-05-28
---

# Day 02 — brainstorming：从想法到设计

> **核心铁律**：动手写代码 / scaffold 项目 / invoke 实现 skill 之前，**必须先 present design 并获得用户批准**。
> **Anti-pattern 反面**：「这个太简单不需要 design」——所有项目都要走，再小也要。

---

## 一、skill 精读笔记（1554 词）

### 1.1 brainstorming 是什么

不是「拍脑袋头脑风暴」，而是**一套有 9 步 checklist 的结构化需求挖掘流程**：

```
1. Explore project context（看文件、文档、最近 commit）
2. Offer Visual Companion（如涉及 UI，单独消息发出邀请）
3. Ask clarifying questions（一次问一个）
4. Propose 2-3 approaches（带 trade-off + 你的推荐）
5. Present design（按复杂度分节，每节后求批准）
6. Write design doc（到 docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md）
7. Spec self-review（placeholder / 矛盾 / 模糊点扫描）
8. User reviews written spec
9. Transition → invoke writing-plans
```

终态：**只能转到 writing-plans，不能跳进任何 implementation skill**。

### 1.2 关键原则

- **One question at a time**：一次只问一个问题，多选题优先
- **YAGNI ruthlessly**：删掉一切非必要功能
- **Incremental validation**：每节 design 都求批准
- **设计单元有清晰边界**：「能不看内部就明白它干啥吗？」

### 1.3 与其他 skill 的关系

```
brainstorming → writing-plans → executing-plans / subagent-driven-development
```

brainstorming 解决的是「该不该做、做什么」；writing-plans 解决「怎么做」；executing 解决「做」。

---

## 二、实战：给知识库加「每日抽样质检脚本」

### 2.1 探索项目上下文

我先扫了一遍现有质检相关资源：

| 文件/工具 | 现状 |
|-----------|------|
| `wiki_self_improve.py` | 已有，但是「全库扫描」非「每日抽样」 |
| `HEARTBEAT.md` | 描述了每日抽样 1-2 篇的 SOP |
| `WIKI-GOVERNANCE.md` | 定义了 5 维度 100 分质量评分 |
| `tools/scan_frontmatter_pollution.py` | 已有，但只检乱码 |

**结论**：HEARTBEAT 描述了需求但**没有专用脚本**，每日手工抽样靠 Agent 心情，不可靠。

### 2.2 澄清问题（一次一个）

**Q1（必问）**：抽样标准是「真随机」还是「优先抽未抽过的」？
- A：优先抽**最久没被检查过**的（按 `last_audited` 字段排序，无字段视为从未抽过）

**Q2（必问）**：评分模型是「沿用 wiki_self_improve 的 5 维度」还是「重新设计简化版」？
- A：沿用 5 维度，但**输出格式简化为单页 markdown 报告**

**Q3（必问）**：每天抽几篇？1 / 2 / 3 / 5？
- A：默认 2 篇（HEARTBEAT 上限），可命令行参数覆盖

**Q4（必问）**：低分文章（<70）的处理方式？
- A：**写入 `memory/quality-improvement-queue.md` 待改进队列**，超过 14 天未改触发告警

**Q5（必问）**：脚本是「独立 CLI」还是「被 heartbeat 自动调用」？
- A：**独立 CLI**，老板手动跑 / 也可被 heartbeat 调用，二者解耦

### 2.3 Propose 2-3 Approaches

#### 方案 A：Python 单文件脚本（推荐 ⭐）
- **位置**：`tools/daily_quality_sampling.py`
- **依赖**：仅标准库（os、re、json、frontmatter 已装）
- **核心逻辑**：
  1. 扫描 `wiki/**/*.md`，读 frontmatter 取 `last_audited` 字段
  2. 按 `last_audited` 升序排前 N 个（默认 2）
  3. 用 wiki_self_improve 的评分逻辑算分
  4. 写入 `memory/quality-audit-YYYY-MM-DD.md` 报告
  5. 低分 → 追加到 `memory/quality-improvement-queue.md`
  6. 更新被抽样文章的 `last_audited` 字段
- **优点**：与现有工具风格一致、零依赖、易测
- **缺点**：评分逻辑跟 wiki_self_improve 重复（需抽公共函数）

#### 方案 B：复用 wiki_self_improve 加 `--sample` 子命令
- 直接给现有工具加一个子命令 `python wiki_self_improve.py sample --count 2`
- **优点**：单一工具入口
- **缺点**：wiki_self_improve 已经做全库扫描，混合两种用途职责不清

#### 方案 C：用 LLM API 评分（非规则评分）
- 用 Claude API 对每篇做语义打分
- **优点**：评分更准
- **缺点**：成本（每天 2 篇 × 365 天 ≈ 多花钱）、需 API key、慢

**我的推荐：方案 A**。理由：
- 与现有规则化评分一致，无新依赖
- 评分逻辑抽公共模块 `tools/quality_score.py`，方案 A 与 wiki_self_improve 都引用
- 未来要加 LLM 评分也只需替换 quality_score.py 内部实现

### 2.4 Present Design（分节）

#### Section 1：架构

```
┌──────────────────────────────────────┐
│  tools/daily_quality_sampling.py     │  CLI 入口
└──────────────────────────────────────┘
              ↓ 调用
┌──────────────────────────────────────┐
│  tools/quality_score.py              │  评分公共模块
│  - score_article(path) -> dict       │  (新建，抽自 wiki_self_improve)
└──────────────────────────────────────┘
              ↓ 写入
┌──────────────────────────────────────┐
│  memory/quality-audit-YYYY-MM-DD.md  │  当日报告
│  memory/quality-improvement-queue.md │  待改进队列
└──────────────────────────────────────┘
              ↓ 更新
┌──────────────────────────────────────┐
│  wiki/**/*.md frontmatter            │  last_audited 字段
└──────────────────────────────────────┘
```

#### Section 2：数据流

1. 输入：无（自动扫描）或 `--count N`
2. 处理：扫 wiki → sort by last_audited → 取前 N → 评分
3. 输出：3 处（当日报告 + 待改进队列 + frontmatter 更新）

#### Section 3：错误处理

| 错误 | 处理 |
|------|------|
| frontmatter 缺失 | last_audited 视为 1970-01-01（最优先抽） |
| 评分异常 | 跳过该文件，报告里标 ERROR |
| memory/ 目录不存在 | mkdir -p |
| 编码错误 | 用 utf-8 errors='replace'（红线规则 1） |

#### Section 4：测试

| 测试用例 | 期望 |
|----------|------|
| 文章无 last_audited | 被选中 |
| 文章 last_audited 最旧 | 被选中 |
| --count 5 | 选 5 篇 |
| 评分 < 70 | 写入待改进队列 |
| 同日重跑 | 不会重复抽（last_audited 已更新） |

---

## 三、Spec self-review 结果

按 brainstorming 第 7 步要求检查：

| 检查项 | 结果 |
|--------|------|
| Placeholder（TBD/TODO） | ✅ 无 |
| 矛盾 | ✅ 无 |
| Scope | ✅ 单一文件，单一职责 |
| 模糊性 | ⚠️ "评分异常" 含义模糊 → 已补充：「Python 异常 catch 后跳过」 |

---

## 四、Day 2 反思

### 做对的事
- **真的忍住没直接给方案**，先问了 5 个澄清问题
- **YAGNI 砍掉了 LLM 方案**（方案 C），承认成本不划算
- **架构图分节呈现**，每节都可独立批准

### 差点犯的错
- 第一反应想直接「加到 wiki_self_improve.py」，被 brainstorming 流程拦住
- 差点跳过 spec self-review

### 比直觉的差别
- 直觉：「这么简单不用 brainstorm，10 行 Python 搞定」
- 实际：brainstorm 出来发现「公共评分模块」这件事，把单脚本设计成了**两文件解耦**架构，长期维护性更好

---

## 五、Day 2 自评

| 维度 | 评分 | 备注 |
|------|------|------|
| 澄清问题深度 | 5/5 | 5 个问题都挖到了「用户没明说但很重要」的点 |
| 方案对比质量 | 5/5 | 3 个方案 + 量化对比 |
| 分节呈现 | 5/5 | 4 节，每节可独立批准 |
| spec self-review | 5/5 | 真的扫到了模糊点并修 |
| YAGNI | 5/5 | 主动砍方案 C |

**总评：25/25** ✅ 满分通关

---

## 六、产出物

- ✅ design spec（已在本笔记 Section 1-4）
- ⏭️ Day 3 转入 writing-plans，把 spec 写成可执行 plan

---

> 相关：[Day01](./day01-overview.md) | [Day03](./day03-plan.md) | [学习计划](../学习计划.md)
