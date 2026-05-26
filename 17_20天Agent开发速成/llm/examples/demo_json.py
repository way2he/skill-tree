# -*- coding: utf-8 -*-
"""
JSON 结构化输出 demo —— 覆盖 generate_json

适配器层 generate_json 会让模型强制返回有效 JSON，可附带 Schema 约束。

运行：
    cd 17_20天Agent开发速成

    # 同步
    set LLM_PROVIDER=deepseek
    set DEEPSEEK_API_KEY=***
    py -3 -m llm.demo.demo_json

    # 异步
    py -3 -m llm.demo.demo_json --async
"""

import asyncio
import json
import sys
import io

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from llm.core import get_llm, get_async_llm, current_provider

# JSON Schema 示例
SCHEMA = {
    "type": "object",
    "properties": {
        "intent":     {"type": "string", "description": "用户意图分类"},
        "confidence": {"type": "number", "description": "0-1 置信度"},
        "keywords":   {"type": "array", "items": {"type": "string"}},
    },
    "required": ["intent", "confidence", "keywords"],
}

PROMPT = "我想给妈妈订一束生日鲜花，今天下午就要送到。请提取意图和关键词。"


def run_sync():
    llm = get_llm()
    print(f"🎯 同步 [{current_provider()}]")
    raw = llm.generate_json(PROMPT, schema=SCHEMA)
    print("原始 JSON 字符串：", raw)
    try:
        parsed = json.loads(raw)
        print("解析后：", json.dumps(parsed, ensure_ascii=False, indent=2))
    except json.JSONDecodeError as e:
        print("⚠️ JSON 解析失败：", e)


async def run_async():
    llm = get_async_llm()
    print(f"🎯 异步 [{current_provider()}]")
    raw = await llm.generate_json(PROMPT, schema=SCHEMA)
    print("原始 JSON 字符串：", raw)
    try:
        parsed = json.loads(raw)
        print("解析后：", json.dumps(parsed, ensure_ascii=False, indent=2))
    except json.JSONDecodeError as e:
        print("⚠️ JSON 解析失败：", e)


def main():
    is_async = any(a in ("--async", "-a") for a in sys.argv[1:])
    if is_async:
        asyncio.run(run_async())
    else:
        run_sync()


if __name__ == "__main__":
    main()
