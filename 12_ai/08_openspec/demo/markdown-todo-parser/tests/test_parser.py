"""覆盖 spec 中全部 5 个 Scenario."""
from pathlib import Path

import pytest

from mdtodo import parse_text, parse_file


def test_scenario_open_todo():
    items = parse_text("- [ ] 写测试\n")
    assert len(items) == 1
    assert items[0].status == "open"
    assert items[0].text == "写测试"
    assert items[0].line == 1


def test_scenario_done_todo():
    items = parse_text("- [x] 已修复 bug\n")
    assert items[0].status == "done"
    assert items[0].text == "已修复 bug"


def test_scenario_file_not_found(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        parse_file(tmp_path / "nope.md")


def test_scenario_section_context():
    md = "## 开发任务\n- [ ] foo\n"
    items = parse_text(md)
    assert items[0].section == "开发任务"


def test_scenario_no_heading():
    items = parse_text("- [ ] 孤儿 TODO\n")
    assert items[0].section is None


def test_mixed_sections():
    md = (
        "# 总览\n"
        "- [ ] 顶层任务\n"
        "## 子任务\n"
        "- [x] 完成的子任务\n"
        "- [ ] 待办子任务\n"
    )
    items = parse_text(md)
    assert [i.section for i in items] == ["总览", "子任务", "子任务"]
    assert [i.status for i in items] == ["open", "done", "open"]
