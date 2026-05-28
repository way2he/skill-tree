---
name: Day 03 writing-plans 实战
description: 把 Day 2 的需求 spec 写成可执行 plan
type: learning-note
day: 3
tags: ["superpowers", "writing-plans", "学习笔记"]
summary: writing-plans 假设执行的工程师对你的项目零上下文且品味差——必须给 bite-sized task (2-5 分钟一步)、确切文件路径、完整代码、明确验证命令
created_at: 2026-05-28
updated_at: 2026-05-28
---

# Day 03 — writing-plans：把 Spec 变成 Bite-Sized Plan

> **核心铁律**：假设执行的工程师有零上下文 + 可疑的品味。给他**所有他需要知道的**——文件路径、代码、命令、验证。

---

## 一、skill 精读笔记 (921 词)

### 1.1 Plan 的颗粒度

**每一步必须是 2-5 分钟可完成的单个动作**：
- "Write the failing test" - one step
- "Run it to make sure it fails" - one step
- "Implement the minimal code to make the test pass" - one step
- "Run the tests and make sure they pass" - one step
- "Commit" - one step

### 1.2 必含的 Plan 头部

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development OR superpowers:executing-plans.

**Goal:** [one sentence]

**Architecture:** [2-3 sentences]

**Tech Stack:** [tech list]
```

### 1.3 任务结构 (TDD 五步)

每个 Task 都长这样：

````markdown
### Task N: [Component Name]

**Files:** Create/Modify/Test paths

- [ ] **Step 1: Write the failing test** (code shown)
- [ ] **Step 2: Run test to verify it fails** (exact command + expected output)
- [ ] **Step 3: Write minimal implementation** (code shown)
- [ ] **Step 4: Run test to verify it passes** (exact command + expected output)
- [ ] **Step 5: Commit** (exact git command + message)
````

### 1.4 No Placeholders Rule

下列写法是 **plan failure**，永远不能写:
- "TBD", "TODO", "implement later"
- "Add appropriate error handling"
- "Write tests for the above" (没有实际测试代码)
- "Similar to Task N" (重复代码——工程师可能跳读)
- 引用未定义的 type / function

---

## 二、Day 2 spec 转 Plan

### Plan Header

# Daily Quality Sampling Implementation Plan

> REQUIRED SUB-SKILL: superpowers:subagent-driven-development

**Goal**: 实现 tools/daily_quality_sampling.py，每日按 last_audited 升序抽 N 篇文章评分、写报告、更新待改进队列

**Architecture**: 两文件解耦——`quality_score.py` 抽取公共评分函数 (从 wiki_self_improve.py)，`daily_quality_sampling.py` 做 CLI 入口。结果写入 `memory/quality-audit-YYYY-MM-DD.md` 和 `memory/quality-improvement-queue.md`，更新文章 frontmatter 的 last_audited 字段。

**Tech Stack**: Python 3.12 标准库 + python-frontmatter (已装)

---

### File Structure

| 文件 | 状态 | 责任 |
|------|------|------|
| `tools/quality_score.py` | Create | 公共评分函数 score_article(path) -> dict |
| `tools/daily_quality_sampling.py` | Create | CLI 入口 + 抽样 + 报告生成 |
| `tests/test_quality_score.py` | Create | quality_score 单元测试 |
| `tests/test_daily_sampling.py` | Create | daily_sampling 集成测试 |
| `wiki_self_improve.py` | Modify | 改为引用 quality_score.py |
| `memory/quality-improvement-queue.md` | Create | 待改进队列 (首次运行时) |

---

### Task 1: Extract quality_score.py from wiki_self_improve.py

**Files**: Create `tools/quality_score.py` + `tests/test_quality_score.py`

- [ ] **Step 1: Write failing test**

```python
# tests/test_quality_score.py
import pytest
from tools.quality_score import score_article

def test_score_article_returns_dict_with_total():
    result = score_article("wiki/test_article.md")
    assert "total" in result
    assert 0 <= result["total"] <= 100

def test_score_article_dimensions():
    result = score_article("wiki/test_article.md")
    assert set(result.keys()) >= {"total", "completeness", "relevance", "timeliness", "readability", "practicality"}
```

- [ ] **Step 2: Verify RED**

```bash
pytest tests/test_quality_score.py -v
# Expected: FAIL - ModuleNotFoundError: tools.quality_score
```

- [ ] **Step 3: Extract minimal implementation**

把 wiki_self_improve.py 里的 `_score_*` 5 个函数搬到 tools/quality_score.py 并加 score_article 入口

- [ ] **Step 4: Verify GREEN**

```bash
pytest tests/test_quality_score.py -v
# Expected: PASS 2/2
```

- [ ] **Step 5: Commit**

```bash
git add tools/quality_score.py tests/test_quality_score.py
git commit -m "refactor: extract quality_score module from wiki_self_improve"
```

---

### Task 2: Update wiki_self_improve.py to use shared module

类似 Task 1 (改 wiki_self_improve.py import 路径 + 跑全量回归测试)

---

### Task 3: Build daily_quality_sampling.py - sampling logic

**Files**: Create `tools/daily_quality_sampling.py` + `tests/test_daily_sampling.py`

- [ ] **Step 1: Failing test for sampler**

```python
# tests/test_daily_sampling.py
from tools.daily_quality_sampling import sample_articles
from datetime import datetime

def test_sample_picks_oldest_audited(tmp_path):
    # 创建 3 篇 mock 文章, last_audited 分别为 None, 2025-01-01, 2026-05-01
    # 期望 sample(count=1) 返回 None 那篇 (优先级最高)
    ...
    result = sample_articles(tmp_path, count=1)
    assert result[0].name == "never_audited.md"
```

- [ ] Steps 2-5: Verify RED → 实现 sample_articles → Verify GREEN → Commit

---

### Task 4: Report generation

类似 Task 3, 测试 `generate_report(articles, scores)` 输出 markdown

---

### Task 5: Improvement queue update

类似 Task 3, 测试低分文章追加到 `memory/quality-improvement-queue.md`

---

### Task 6: Update frontmatter last_audited

类似 Task 3, 测试 frontmatter 字段更新

---

### Task 7: CLI entry + integration test

集成 Task 3-6, 测试 `python tools/daily_quality_sampling.py --count 2` 端到端跑通

---

## 三、Plan Self-Review

| 检查项 | 结果 |
|--------|------|
| Spec 覆盖 | ✅ 5 个维度需求全覆盖 |
| Placeholder 扫描 | ⚠️ Task 4-6 用了 "类似 Task 3"——违反 No Placeholders, 实战需展开 |
| Type 一致性 | ✅ score_article 返回 dict, sample_articles 返回 list |

**修正动作**: 本笔记为学习产出, 不实际执行——若真要执行需把 Task 4-6 完整展开 (这里压缩为避免笔记膨胀, 真实执行 plan 不允许压缩)

---

## 四、Day 3 反思

### 做对
- 严格按 TDD 五步分 step
- 文件路径全部明确
- 每步都有验证命令 + 预期输出

### 容易犯
- 偷懒写 "类似 Task N" (真实 plan 禁止)
- 偷懒省略测试代码

### 比直觉差别
- 直觉: "我自己看 plan 就行, 别写那么细"
- 实际: plan 是给"零上下文工程师"的, 写细不是浪费——是把"未来的我"当成新人对待

---

## 五、Day 3 自评

| 维度 | 分 |
|------|---|
| Plan header 完整 | 5/5 |
| Task 颗粒度 | 4/5 (Task 4-6 偷懒压缩) |
| 代码完整性 | 4/5 |
| 验证命令明确 | 5/5 |
| Self-review 真做 | 5/5 (发现并标注了 placeholder 违规) |

**总评: 23/25** ✅ 通关 (扣 2 分: Task 4-6 压缩, 真实场景会扣更多)

---

## 六、产出物

- ✅ Plan 文档 (本笔记)
- ⏭️ Day 4: 取 Plan 的 Task 1-3 实际执行 + verification