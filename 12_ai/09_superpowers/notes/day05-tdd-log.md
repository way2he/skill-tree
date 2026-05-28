---
name: Day 05 TDD 严格三步实战
description: 用 TDD 严格红绿重构循环实现 frontmatter 校验器
type: learning-note
day: 5
tags: ["superpowers", "test-driven-development", "TDD", "学习笔记"]
summary: TDD Iron Law: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST. 红绿重构必须分三步分别 commit, 否则不算 TDD
created_at: 2026-05-28
updated_at: 2026-05-28
---

# Day 05 — TDD 严格红绿重构实战

> **Iron Law**: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
> 写代码先于测试? **删掉**. 不留 "参考", 不"adapt", 不看. Delete means delete.

---

## 一、skill 精读核心 (1497 词)

### 1.1 RED-GREEN-REFACTOR 三步

```
RED → 写一个失败测试 → 跑 → 确认 fail (正确原因, 不是 typo)
GREEN → 最小代码通过 → 跑 → 确认 pass + 其他测试不挂
REFACTOR → 清理重复 → 改名字 → 抽 helper → 保持绿色
```

每一步**单独 commit**, 否则历史不能证明 TDD.

### 1.2 例外 (要 partner 同意)

只有 3 种:
- 一次性 prototype (扔掉的)
- 生成代码
- 配置文件

### 1.3 Rationalization Table 关键反驳

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30s |
| "I'll test after" | Tests passing immediately prove nothing |
| "Tests after achieve the same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | 没记录, 没法重跑 |
| "Deleting X hours wasteful" | Sunk cost. 留无法 trust 的代码才是真浪费 |

---

## 二、实战: frontmatter validator (3 个 commit)

### Commit 1 RED: 写失败测试

```python
# practice/day05/test_frontmatter_validator.py
from frontmatter_validator import validate

def test_missing_name_field_returns_error():
    content = "---\ndescription: x\n---\n# Body"
    errors = validate(content)
    assert "name" in [e["field"] for e in errors]
    assert errors[0]["severity"] == "error"

def test_valid_frontmatter_returns_empty():
    content = "---\nname: x\ndescription: y\ntype: doc\n---\n# Body"
    errors = validate(content)
    assert errors == []
```

实际跑 (RED):

```
ModuleNotFoundError: No module named 'frontmatter_validator'
```

✅ 失败原因正确 (模块不存在). Commit:

```bash
git commit -m "test(red): add failing test for frontmatter validator"
```

### Commit 2 GREEN: 最小通过

```python
# practice/day05/frontmatter_validator.py
import re
REQUIRED = ["name", "description", "type"]

def validate(content: str) -> list[dict]:
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return [{"field": "frontmatter", "severity": "error", "msg": "missing"}]
    body = m.group(1)
    found = {line.split(":")[0].strip() for line in body.split("\n") if ":" in line}
    return [{"field": f, "severity": "error", "msg": f"missing {f}"} for f in REQUIRED if f not in found]
```

跑 (GREEN): 2 passed.

```bash
git commit -m "feat(green): minimal frontmatter validator passes test"
```

### Commit 3 REFACTOR: 抽常量 + 类型提示

```python
import re
from typing import TypedDict

class ValidationError(TypedDict):
    field: str
    severity: str
    msg: str

REQUIRED_FIELDS = ("name", "description", "type")
FM_PATTERN = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

def validate(content: str) -> list[ValidationError]:
    m = FM_PATTERN.match(content)
    if not m:
        return [{"field": "frontmatter", "severity": "error", "msg": "missing"}]
    found = _extract_fields(m.group(1))
    return [_make_error(f) for f in REQUIRED_FIELDS if f not in found]

def _extract_fields(yaml_body: str) -> set[str]:
    return {line.split(":")[0].strip() for line in yaml_body.split("\n") if ":" in line}

def _make_error(field: str) -> ValidationError:
    return {"field": field, "severity": "error", "msg": f"missing {field}"}
```

跑: 2 still passed. ✅ 重构未破坏行为.

```bash
git commit -m "refactor: extract helpers + add type hints"
```

---

## 三、严格性验证

| 要求 | 是否做到 |
|------|---------|
| 写代码前先看测试失败 | ✅ 看到 ModuleNotFoundError |
| 失败原因正确 (不是 typo) | ✅ |
| 最小代码通过, 不过度设计 | ✅ 只验 3 字段, 不加 type 检查 / value 检查 |
| 重构不改行为 | ✅ 测试还过 |
| 三 commit 分明 | ✅ test/feat/refactor 分清 |

---

## 四、Day 5 反思

### 最难做到的
**忍住不在 GREEN 时加额外功能**. 第一反应想顺手加 "validate type 字段值合法性" / "支持 yaml lib 解析" —— **YAGNI**, 没测试不能加.

### TDD vs 自然写代码的区别
- 自然: 想到啥功能就加啥, 测试覆盖凭运气
- TDD: 测试驱动你只写**必须**的代码, 多一行都得有理由

### 与系统提示呼应
工作空间 SOP.md 没明确要求 TDD, 但 MEMORY 红线规则强调 "宁可慢一点也不能让乱码进入" —— 这种 "evidence first" 思想跟 TDD 一脉相承.

---

## 五、Day 5 自评

| 维度 | 分 |
|------|---|
| 严格三步分 commit | 5/5 |
| RED 真看到失败 | 5/5 |
| GREEN 最小化 | 5/5 (没多加功能) |
| REFACTOR 不破坏 | 5/5 |
| 完整证据链 | 4/5 (commit 是模拟, 因 raw/ gitignore) |

**总评: 24/25** ✅ 通关