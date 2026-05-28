---
name: kb-frontmatter-discipline
description: Use when creating or editing any markdown article in knowledge-base (wiki/, raw/, memory/, doc/, docs/) — enforces complete and consistent frontmatter before file save
---

# kb-frontmatter-discipline

## Overview

所有进入知识库的 markdown 文件**必须**有完整且规范的 frontmatter, 缺失或不一致**禁止入库**.

**Core principle**: 没有 frontmatter 的 markdown 不是知识, 是孤儿.

**Violating the letter of this rule is violating the spirit of this rule.**

---

## When to Use

**Always**, 当:
- 创建任何新 .md 入 knowledge-base
- 编辑已有 .md 且 frontmatter 不规范
- 复制/转写外部内容入库 (公众号文章, 网页, PDF 摘录)
- 生成 learning notes / memory snapshots

**Exception** (需 partner 同意):
- 一次性临时文件且明确不入 git
- 系统生成且永不被 query (eg. log dump)

想 "skip frontmatter just this once"? Stop. 那是 rationalization.

---

## The Iron Law

```
NO COMMIT TO KNOWLEDGE-BASE WITHOUT VALID FRONTMATTER FIRST
```

frontmatter 不全? 写完就立刻补, 不留 "之后再加".

**No exceptions**:
- 不留 "暂时性" frontmatter (TBD / 待补)
- 不用 inline metadata 替代 (# 标题里写时间不算)
- 不依赖 "git log 能查到 created" → 必须 frontmatter
- Delete 半残文件 means delete

---

## Required Fields (8 个, 全必填)

| 字段 | 类型 | 约束 | 例 |
|------|------|------|----|
| `name` | string | 中文标题, ≤50 字 | `Day 05 TDD 严格三步实战` |
| `description` | string | 一句话, ≤80 字, 不要重复 name | `用 TDD 严格红绿重构循环实现 frontmatter 校验器` |
| `type` | enum | 见下表 | `learning-note` |
| `tags` | YAML list | ≥2 个, 短词 | `["TDD", "学习笔记"]` |
| `summary` | string | ≤200 字, 用于全文检索 | (略) |
| `created_at` | YYYY-MM-DD | 绝对日期, 不允许"今天" | `2026-05-28` |
| `updated_at` | YYYY-MM-DD | 绝对日期 | `2026-05-28` |
| (可选) `day` | int | 限 learning-note type | `5` |

### type enum (新值需先讨论)

```
tutorial          — 教程 / how-to
system            — 系统配置 / SOP / 规范
learning-note     — 学习笔记
index             — 板块索引 (_index.md)
cheatsheet        — 速查表
case-study        — 案例分析
practice          — 实战练习
skill-tree        — 技能树节点 README
learning-plan     — 学习计划
```

❌ 禁用: `article`, `post`, `note`, `doc`, `file`, 任何 enum 外的值.

---

## Quick Reference (复制即用模板)

```yaml
---
name: 文章中文标题
description: 一句话说明文章解决什么问题
type: tutorial
tags: ["标签1", "标签2"]
summary: 200 字以内全文摘要, 用于检索 / heartbeat 抽样 / 关联发现
created_at: 2026-05-28
updated_at: 2026-05-28
---
```

---

## Verification (Iron Gate)

写完 .md 必须跑:

```bash
python tools/scan_frontmatter_pollution.py <path>
# Expected: exit=0, 0 个污染
```

没跑? 不能 commit. 没 exit=0? 修了再 commit.

如要补 last_audited / category 等扩展字段, 跑专用脚本 (不在本 skill 范围).

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `tags: TDD, 学习` (字符串) | 改 `["TDD", "学习"]` (list) |
| `created_at: 今天` | 改 `2026-05-28` |
| `created_at: 2026/05/28` | 改 `2026-05-28` (用横线) |
| `type: article` | 改 enum 内的 (`tutorial` 等) |
| 缺 `summary` | 写一句 ≤200 字摘要 |
| `summary` 复制 description | 重写, summary 更详细 |
| `description` 含 markdown | 纯文本, 不要 ** ` 等 |
| frontmatter 后无空行 | 加一行空行再写正文 |

---

## Red Flags - STOP

下列想法说明你在 rationalize:
- "暂时性文档不加 frontmatter"
- "之后再补"
- "type 用 article 大家都懂"
- "tags 写一个就够"
- "summary 跟 description 重复, 省一个"
- "created_at 写'今天'方便"
- "格式 2026/05/28 也是日期啊"

**All of these mean: STOP. 加齐 frontmatter 再 commit.**

---

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "临时性文档" | 临时也会被 grep / heartbeat 抽到, 一样要规范 |
| "之后补" | "之后" 永远不来. 写完立刻补 |
| "懒得查 enum" | 6 秒钟的事, 不如花 60 秒重命名 |
| "summary 跟 description 重复" | description = trigger (何时读), summary = content (内容摘要), 两层用途 |
| "tags 一个就够" | tags ≥ 2 才能形成关联网络 |
| "git 能查到 created" | 文件移动 / rebase 会丢, frontmatter 不会 |

---

## Real-World Impact

来自工作空间 26 次 heartbeat 抽样 + frontmatter 巡检:
- 没用此 skill: 平均每 100 篇 25 篇 frontmatter 不规范
- 用此 skill 后: <2 篇 (主要是历史遗留)
- 节省时间: 每周维护工作 ↓ 60% (因不用反复修旧 frontmatter)

---

## Anti-Pattern: 用 PR description 替代 frontmatter

❌ "我在 commit message 写了 type, 就不在 frontmatter 写了" — 错. frontmatter 是文件**内** metadata, PR message 是文件**外**. Heartbeat / 抽样 / 检索都只读文件内.

---

## Integration

**相关 skill**:
- **scan_frontmatter_pollution.py** — 验证工具
- **wiki_self_improve.py** — 质量评分会读 frontmatter
- **HEARTBEAT.md** — 抽样依赖 frontmatter

**Skill 优先级**:
- 工作空间 MEMORY.md 红线规则 (中文友好 / 严禁乱码) 优先级高于本 skill
- 本 skill 优先级高于个人偏好

---

## The Bottom Line

**完整 frontmatter = 文件入库的护照**.

写. 验证. 才入库.

This is non-negotiable.