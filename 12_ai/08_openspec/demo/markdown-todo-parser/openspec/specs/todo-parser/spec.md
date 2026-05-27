# todo-parser Specification

## Purpose
TBD - created by archiving change add-parser. Update Purpose after archive.
## Requirements
### Requirement: 解析 Markdown 文件提取 TODO 项
系统 SHALL 读取指定的 markdown 文件，提取所有形如 `- [ ]` 或 `- [x]` 的待办/已完成项，返回结构化数据列表。

#### Scenario: 文件含未完成 TODO
- **WHEN** 输入 markdown 文件包含 `- [ ] 写测试` 这一行
- **THEN** 返回的项中应包含一条 `{status: "open", text: "写测试", line: <行号>}`

#### Scenario: 文件含已完成项
- **WHEN** 输入 markdown 文件包含 `- [x] 已修复 bug`
- **THEN** 返回项应包含 `{status: "done", text: "已修复 bug", line: <行号>}`

#### Scenario: 文件不存在
- **WHEN** 调用解析函数传入不存在的路径
- **THEN** 抛出 `FileNotFoundError`

### Requirement: 携带章节上下文
系统 SHALL 为每个 TODO 项附带其所属的最近上级 markdown 标题（H1-H6），便于后续分类。

#### Scenario: TODO 在某二级标题下
- **WHEN** markdown 文件存在 `## 开发任务` 标题，紧随其后是 `- [ ] foo`
- **THEN** 返回项的 `section` 字段等于 `"开发任务"`

#### Scenario: TODO 在文件开头无标题
- **WHEN** TODO 项出现在任何标题之前
- **THEN** `section` 字段等于 `None` 或空字符串

