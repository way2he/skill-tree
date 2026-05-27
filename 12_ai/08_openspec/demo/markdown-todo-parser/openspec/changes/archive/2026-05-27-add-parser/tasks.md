## 1. 实现核心解析器

- [ ] 1.1 创建 `mdtodo/__init__.py`
- [ ] 1.2 创建 `mdtodo/parser.py`，实现 `parse_file(path: Path) -> list[TodoItem]`
- [ ] 1.3 定义 `TodoItem` dataclass：`status: Literal["open","done"]`、`text: str`、`line: int`、`section: str | None`
- [ ] 1.4 用正则 `^(\s*)-\s+\[([ xX])\]\s+(.*)$` 匹配每行
- [ ] 1.5 维护「当前最近标题」状态：遇到 `^(#{1,6})\s+(.*)$` 时更新

## 2. 单元测试

- [ ] 2.1 创建 `tests/test_parser.py`
- [ ] 2.2 覆盖 spec 中 5 个 Scenario
- [ ] 2.3 `pytest -q` 全部通过

## 3. CLI 入口

- [ ] 3.1 创建 `mdtodo/__main__.py`：`python -m mdtodo <file>` 打印结果
- [ ] 3.2 支持 `--json` 输出 JSON
- [ ] 3.3 README 加 3 行使用示例

## 4. 验收

- [ ] 4.1 对本目录的 `proposal.md` 跑一次，确认能识别其中的占位 TODO
- [ ] 4.2 `openspec validate add-parser` 通过
- [ ] 4.3 `openspec archive add-parser` 归档
