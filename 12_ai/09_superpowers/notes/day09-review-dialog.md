---
name: Day 09 Code Review 博弈
description: requesting + receiving code review 一次完整循环 — 含技术性反驳实例
type: learning-note
day: 9
tags: ["superpowers", "requesting-code-review", "receiving-code-review", "code-review", "学习笔记"]
summary: 接 review 不是表演同意——是技术性博弈. 禁止 "You are absolutely right" / "Thanks"; 必须 verify 后才能 implement; 错就 push back, 对就直接修
created_at: 2026-05-28
updated_at: 2026-05-28
---

# Day 09 — Code Review 博弈

## 一、双 skill 核心

### 1.1 requesting-code-review

**何时请求** (mandatory):
- 每个 task 完成后 (SDD)
- major feature 完成后
- merge 到 main 前

**怎么请求** (subagent dispatch):
1. 拿 BASE_SHA / HEAD_SHA
2. dispatch reviewer subagent (general-purpose), 填模板:
   - DESCRIPTION (一句话总结建了什么)
   - PLAN_OR_REQUIREMENTS (应该做什么)
   - BASE_SHA / HEAD_SHA
3. 拿反馈后处理:
   - Critical → 立即修
   - Important → proceed 前修
   - Minor → 记录待办
   - reviewer 错 → 带技术理由 push back

### 1.2 receiving-code-review (重头戏)

**Response Pattern**:
```
1. READ: 看完, 不立即反应
2. UNDERSTAND: 用自己的话复述要求 (或问)
3. VERIFY: 对照代码现实检查
4. EVALUATE: 对这个码库技术上对吗?
5. RESPOND: 技术性 ack 或 reasoned push back
6. IMPLEMENT: 一次一项, 每项测试
```

#### 禁止用语 (CLAUDE.md 红线)

- ❌ "You are absolutely right!"
- ❌ "Great point!" / "Excellent feedback!"
- ❌ "Let me implement that now" (verify 前)
- ❌ "Thanks for [anything]" — 任何感谢

**Why no thanks**: Actions speak. Just fix it.

#### 正确姿势

- ✅ "Fixed. [brief 描述]"
- ✅ "Good catch — [specific issue]. Fixed in [location]."
- ✅ [直接展示修后的代码]

#### Unclear feedback 处理

```
IF any item unclear:
  STOP — do not implement anything yet
  ASK for clarification on unclear items
```

理由: items 可能相关, 部分理解 = 错实现.

#### Push back 何时

- 建议会破坏现有功能
- reviewer 缺上下文
- 违反 YAGNI (无用功能)
- 技术上对 stack 错
- 有 legacy 兼容理由
- 跟 partner 架构决策冲突

**怎么 push**: 技术理由, 非防御性. 引证 test/code. 架构层面 → 拉 partner.

#### YAGNI check
reviewer 说 "implement properly" → 先 grep 看有没人调用 → 没调用就建议删 (YAGNI).

---

## 二、实战: Review Day 5 frontmatter_validator

### 我请求 review (模拟)

dispatch subagent prompt:
```
DESCRIPTION: 实现 frontmatter validator 校验 name/description/type 三个必填字段, 90 行 Python
PLAN_OR_REQUIREMENTS:
  - 缺字段返回 error list
  - 完整 frontmatter 返回 []
  - 严格 TDD 三 commit
BASE_SHA: <commit before tests>
HEAD_SHA: <last refactor commit>
```

### Reviewer 返回 (模拟生成, 含真实可能反馈)

```
Strengths:
- 严格 TDD, 三 commit 分明
- 类型提示完整 (ValidationError TypedDict)
- helper 抽取后可读性好

Issues:
[Important] 1. 正则 `^---\n(.*?)\n---` 在 Windows CRLF 文件上会失败
[Important] 2. 没有处理 frontmatter 中 value 含 ":" 的情况 (e.g., "summary: x: y" 会截断)
[Important] 3. 没测试 edge case: 空 frontmatter, 多个 frontmatter, 缩进 yaml
[Minor] 4. REQUIRED_FIELDS 应该可配置 (不同项目要求不同)
[Suggestion] 5. 用 python-frontmatter lib 替代手写正则

Assessment: 修 1-3 后可 merge
```

### 我的回应 (技术性博弈, 不是表演)

#### Item 1 (Important): CRLF — VERIFIED
```python
import re
PATTERN = re.compile(r"^---\r?\n(.*?)\r?\n---", re.DOTALL)
```
对, Windows 文件常 CRLF, 当前正则 fail. 修.

Response: "Fixed. 加 `\r?\n` 兼容 CRLF."

#### Item 2 (Important): value 含 ":" — VERIFIED
```python
def test_value_with_colon():
    c = "---\nname: x\nsummary: hello: world\ndescription: y\ntype: doc\n---"
    assert validate(c) == []  # 当前实现会把 "summary" "hello" "world" 都当 key
```
跑 → ✅ 复现. 当前 `split(":")` 错. 改 `split(":", 1)`.

Response: "Good catch — fixed by using `split(':', 1)`. Added test_value_with_colon."

#### Item 3 (Important): edge cases — VERIFIED 一部分
- 空 frontmatter `^---\n---` → 当前实现返回所有 required missing → ✅ 正确行为, 不用修
- 多个 frontmatter → 题外话, 实际 markdown 只允许一个, 不修
- 缩进 yaml → 当前不支持嵌套, 但需求里也不需要 → YAGNI 不修

Response: "Verified — 空 frontmatter 当前行为已正确 (返回所有 missing). 多 frontmatter 和缩进 yaml 属 YAGNI, 当前需求不需要. 如需支持请明确."

#### Item 4 (Minor): 可配置 — PUSH BACK
```bash
grep -r "REQUIRED_FIELDS" .
# 只本文件用一次, 没其他调用
```
YAGNI. 没有 caller 要求可配置.

Response: "Pushed back — grep shows 只此一处用, 没有可配置需求 (YAGNI). 如未来出现需求再加."

#### Item 5 (Suggestion): 用 python-frontmatter lib — PUSH BACK
查依赖: 工作空间已有 python-frontmatter. 但用 lib 会让模块只做 "check required keys", 失去独立性 (需依赖).

Response: "Considered — python-frontmatter 会引入依赖换 30 行手写正则. 当前 90 行模块独立性高于 lib 依赖收益. 暂不改, 如未来用法增加再考虑."

### Reviewer 第二轮

```
- Item 1, 2 fixed ✅
- Item 3 你解释清楚了, 接受 ✅
- Item 4 YAGNI 合理, 接受 ✅
- Item 5 push back 合理, 接受 ✅
Approved.
```

---

## 三、回应 4 大类示例统计

| 反馈 | 我的回应 | 类型 |
|------|---------|------|
| Item 1 CRLF | Fixed | 接受 |
| Item 2 colon | Fixed | 接受 |
| Item 3 edge | 部分接受 + 解释 | 部分接受 |
| Item 4 configurable | Pushed back | 拒绝 (YAGNI) |
| Item 5 use lib | Pushed back | 拒绝 (技术理由) |

**没出现的禁止用语**: "Thanks", "Great point", "Excellent", "You are right". ✅

---

## 四、Day 9 反思

### 最难做到的
**不写 "Thanks" / "Great catch"**. 这是社交本能, 但 superpowers 强制用 "Fixed." 替代. 第一次写时手指都僵, 但读起来其实更专业.

### Push back 时的心理障碍
心里会想 "怕得罪 reviewer", 但 receiving-code-review 反复强调 "technical correctness > social comfort". 老板 + reviewer 都向同一个目标交付, push back 不是对抗, 是协作.

### YAGNI check 的真实价值
Item 4 / 5 都是 reviewer 想做更"专业"的事, 但 grep 一下发现没人用, 立刻砍掉. 这一动作平均省 30+ 行代码 + 后续维护.

---

## 五、Day 9 自评

| 维度 | 分 |
|------|---|
| 5 项反馈都 verify | 5/5 |
| 至少 1 个 push back (带技术理由) | 5/5 (有 2 个) |
| 至少 1 个 partial accept | 5/5 |
| 至少 1 个 direct fix | 5/5 |
| 零禁止用语 | 5/5 |

**总评: 25/25** ✅ 满分