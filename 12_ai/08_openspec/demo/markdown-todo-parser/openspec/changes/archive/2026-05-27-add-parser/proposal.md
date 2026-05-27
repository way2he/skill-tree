## Why

知识库每天产出大量 markdown 笔记，文中散落着 `- [ ] xxx` 形式的 TODO，但没有统一工具汇总。手动 grep 不够智能（无法识别上下文、分类、紧急度），导致很多 TODO 被遗忘。

## What Changes

- 新增 `mdtodo` Python 工具，扫描指定目录的所有 markdown 文件
- 提取所有 `- [ ]` 未完成项与 `- [x]` 已完成项
- 输出 JSON / 控制台表格两种格式

## Capabilities

### New Capabilities
- `todo-parser`: 解析单个 markdown 文件中的 TODO 项，返回结构化数据（含上下文、行号、所属章节）

### Modified Capabilities
（无）

## Impact

- 新增依赖：仅 Python 标准库（无第三方）
- 影响代码：新增 `mdtodo/parser.py` 单文件
- 不影响现有任何工具
