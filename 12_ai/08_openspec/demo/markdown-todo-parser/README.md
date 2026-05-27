# Demo A: Markdown TODO 解析器

> 🚧 占位目录，Day 1 启动

## 项目目标
~200 行 Python，从 markdown 文件提取 `- [ ] TODO` 项并分类。

## OpenSpec Changes 规划
1. `add-parser` — 核心解析器
2. `add-cli` — 命令行入口
3. `add-export` — 导出为 JSON/CSV
4. `add-stats` — 统计摘要

## 启动命令（Day 1 执行）
```bash
cd demo/markdown-todo-parser
openspec init
openspec new add-parser
```
