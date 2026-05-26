# -*- coding: utf-8 -*-
"""
流式响应 Demo —— 同步 / 异步 / 枚举入参 三合一

亮点：
    1. 厂商用 ProviderName 枚举，IDE 自动补全，不写硬编码字符串
    2. 同一段调用代码，支持 5 家厂商真实流式：openai / deepseek / qwen / ollama / anthropic
    3. 异步流式（aiohttp 底层）

运行：
    cd 17_20天Agent开发速成

    # 默认用 ollama（本地不需要 key）
    py -3 -m llm.demo.demo_stream

    # 指定厂商
    py -3 -m llm.demo.demo_stream deepseek "用三句话讲讲 LangGraph"

    # 异步流式
    py -3 -m llm.demo.demo_stream qwen "写一首五绝" --async
"""

import asyncio
import sys
import io
import time

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from llm.core import (
    get_llm, get_async_llm,
    ProviderName, current_provider,
    list_providers, list_async_providers,
)


def parse_argv():
    """解析：[provider] [prompt] [--async]"""
    args = [a for a in sys.argv[1:] if a not in ("--async", "-a")]
    is_async = any(a in ("--async", "-a") for a in sys.argv[1:])
    provider = args[0] if len(args) >= 1 else None
    prompt = args[1] if len(args) >= 2 else "用三句话介绍一下你自己"
    return provider, prompt, is_async


def run_sync(provider, prompt: str) -> None:
    llm = get_llm(provider)                          # ← 接受 str 或 ProviderName
    real = provider if provider else current_provider()
    print(f"🎯 [{real}] 同步流式：{prompt}\n")
    t0 = time.time()
    chunks = 0
    for chunk in llm.generate_stream(prompt):
        print(chunk, end="", flush=True)
        chunks += 1
    print(f"\n\n✅ done | {(time.time()-t0)*1000:.0f} ms | {chunks} chunks")


async def run_async(provider, prompt: str) -> None:
    llm = get_async_llm(provider)
    real = provider if provider else current_provider()
    print(f"🎯 [{real}] 异步流式：{prompt}\n")
    t0 = time.time()
    chunks = 0
    async for chunk in llm.generate_stream(prompt):
        print(chunk, end="", flush=True)
        chunks += 1
    print(f"\n\n✅ done | {(time.time()-t0)*1000:.0f} ms | {chunks} chunks")


def main() -> None:
    # 子命令：查看注册清单
    if len(sys.argv) > 1 and sys.argv[1] in ("--list", "-l", "list"):
        print("同步已注册 (sync) :", sorted(list_providers()))
        print("异步已注册 (async):", sorted(list_async_providers()))
        print("默认提供商        :", current_provider())
        return

    provider, prompt, is_async = parse_argv()

    # 演示：把字符串入参转成枚举（如果在已注册列表里）
    if isinstance(provider, str):
        try:
            provider = ProviderName(provider)        # 字符串 → 枚举（拼写错误立即抛 ValueError）
        except ValueError:
            print(f"❌ 未知厂商 {provider!r}，可选：{[p.value for p in ProviderName]}")
            sys.exit(1)

    if is_async:
        asyncio.run(run_async(provider, prompt))
    else:
        run_sync(provider, prompt)


if __name__ == "__main__":
    main()
