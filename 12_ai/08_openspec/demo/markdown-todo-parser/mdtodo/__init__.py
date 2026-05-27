"""Markdown TODO Parser - 学习 OpenSpec 用的最小可用工具。

Spec: openspec/changes/add-parser/specs/todo-parser/spec.md
"""
from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Literal

__all__ = ["TodoItem", "parse_file", "parse_text"]

_TODO_RE = re.compile(r"^\s*-\s+\[([ xX])\]\s+(.*?)\s*$")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")


@dataclass
class TodoItem:
    status: Literal["open", "done"]
    text: str
    line: int  # 1-indexed
    section: str | None

    def to_dict(self) -> dict:
        return asdict(self)


def parse_text(text: str) -> list[TodoItem]:
    """从字符串解析 TODO 项。"""
    items: list[TodoItem] = []
    current_section: str | None = None

    for idx, line in enumerate(text.splitlines(), start=1):
        h = _HEADING_RE.match(line)
        if h:
            current_section = h.group(2).strip()
            continue

        m = _TODO_RE.match(line)
        if m:
            mark, todo_text = m.groups()
            status: Literal["open", "done"] = "done" if mark.lower() == "x" else "open"
            items.append(
                TodoItem(
                    status=status,
                    text=todo_text.strip(),
                    line=idx,
                    section=current_section,
                )
            )
    return items


def parse_file(path: str | Path) -> list[TodoItem]:
    """从 markdown 文件解析 TODO 项。文件不存在抛 FileNotFoundError。"""
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {p}")
    return parse_text(p.read_text(encoding="utf-8"))
