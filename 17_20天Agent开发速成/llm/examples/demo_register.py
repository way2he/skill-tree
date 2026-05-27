# -*- coding: utf-8 -*-
"""
外部扩展厂商 demo —— 覆盖 register_provider / register_async_provider

业务自定义一个 client 类，注册进 llm.core，即可被 get_llm / create_llm 统一调度。

运行：
    py -3 -m llm.examples.demo_register
"""

import sys
import io
import asyncio
from typing import Any, Iterator, AsyncGenerator

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from llm.core import (
    register_provider,
    register_async_provider,
    create_llm,
    create_async_llm,
    list_providers,
    list_async_providers,
)


# ---------- 1. 自定义同步 client（这里用 echo 假实现，便于离线演示）----------
class EchoClient:
    """一个最小可用的 client：把输入原样返回。"""

    default_model = "echo-v1"

    def __init__(self, prefix: str = "[echo] ", **_):
        self.prefix = prefix
        self.model = self.default_model

    def generate(self, prompt: str, **kwargs: Any) -> str:
        return self.prefix + prompt

    def generate_json(self, prompt: str, schema=None, **kwargs: Any) -> str:
        import json as _json

        return _json.dumps({"echo": prompt, "schema": schema}, ensure_ascii=False)

    def generate_stream(self, prompt: str, **kwargs: Any) -> Iterator[str]:
        for ch in self.prefix + prompt:
            yield ch


# ---------- 2. 自定义异步 client ----------
class AsyncEchoClient:
    default_model = "echo-async-v1"

    def __init__(self, prefix: str = "[async-echo] ", **_):
        self.prefix = prefix
        self.model = self.default_model

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        return self.prefix + prompt

    async def generate_json(self, prompt: str, schema=None, **kwargs: Any) -> str:
        import json as _json

        return _json.dumps({"echo": prompt, "schema": schema}, ensure_ascii=False)

    async def generate_stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[str, None]:
        for ch in self.prefix + prompt:
            yield ch


def main_sync():
    print("=== register_provider 演示 ===")
    print("注册前：", "echo" in list_providers())

    # 注册自定义 Provider
    # 注意：register_provider 只接受 name 和 provider_class 两个参数
    register_provider("echo", EchoClient)

    print("注册后：", "echo" in list_providers())

    # 直接用 create_llm 取实例
    llm = create_llm("echo", prefix="🎉 ")
    print("generate           :", llm.generate("hello"))
    print("generate_json      :", llm.generate_json("hi"))
    print("generate_stream    :", "".join(llm.generate_stream("流式 echo")))


async def main_async():
    print("\n=== register_async_provider 演示 ===")
    print("注册前：", "async-echo" in list_async_providers())

    # 注册自定义异步 Provider
    register_async_provider("async-echo", AsyncEchoClient)

    print("注册后：", "async-echo" in list_async_providers())

    llm = create_async_llm("async-echo", prefix="🚀 ")
    print("await generate           :", await llm.generate("hello"))
    print("await generate_json      :", await llm.generate_json("hi"))
    print("async for stream chunks  :", end=" ")
    async for ch in llm.generate_stream("异步流式 echo"):
        print(ch, end="", flush=True)
    print()


if __name__ == "__main__":
    main_sync()
    asyncio.run(main_async())
