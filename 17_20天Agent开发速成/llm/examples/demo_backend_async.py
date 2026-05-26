# -*- coding: utf-8 -*-
"""
异步客户端使用示例

演示如何使用异步 API 和底层实现选择器
"""

import asyncio
import os
from llm.core import (
    LLMClientBuilder,
    BackendType,
    create_async_client,
    set_default_backend,
    reset_default_backend,
)


async def demo_async_builder():
    """演示异步 Builder 模式"""
    print("=" * 60)
    print("异步 Builder 模式示例")
    print("=" * 60)

    # 示例 1：使用 aiohttp 创建异步客户端
    print("\n--- 示例 1：aiohttp 异步客户端 ---")
    builder = (
        LLMClientBuilder()
        .provider("deepseek")
        .aiohttp()  # 异步 HTTP 实现
        .api_key("${DEEPSEEK_API_KEY}")
        .model("deepseek-chat")
    )
    print(f"配置: provider={builder.get_config().provider}, "
          f"backend={builder.get_config().backend}")
    # async_client = builder.build_async()
    # response = await async_client.generate("你好")

    # 示例 2：使用 BackendType 枚举
    print("\n--- 示例 2：BackendType.AIOHTTP ---")
    builder2 = (
        LLMClientBuilder()
        .provider("openai")
        .backend(BackendType.AIOHTTP)
        .api_key("${OPENAI_API_KEY}")
    )
    print(f"配置: provider={builder2.get_config().provider}, "
          f"backend={builder2.get_config().backend}")


async def demo_async_convenience():
    """演示异步便捷函数"""
    print("\n" + "=" * 60)
    print("异步便捷函数示例")
    print("=" * 60)

    print("\n--- 创建异步客户端 ---")
    print("async_client = create_async_client('deepseek', 'aiohttp', api_key='sk-xxx')")

    print("\n--- 使用全局默认 backend ---")
    set_default_backend("aiohttp")
    print("set_default_backend('aiohttp')")
    print("async_client = create_async_client('deepseek', api_key='sk-xxx')")
    print("# 自动使用 aiohttp 实现")
    reset_default_backend()


async def demo_async_patterns():
    """演示异步使用模式"""
    print("\n" + "=" * 60)
    print("异步使用模式")
    print("=" * 60)

    print("""
--- 模式 1：简单异步调用 ---

async def ask_llm(prompt: str):
    client = create_async_client('deepseek', 'aiohttp', api_key='sk-xxx')
    return await client.generate(prompt)

result = await ask_llm("你好")

--- 模式 2：并发请求 ---

async def batch_generate(prompts: list[str]):
    client = create_async_client('deepseek', 'aiohttp', api_key='sk-xxx')
    tasks = [client.generate(p) for p in prompts]
    return await asyncio.gather(*tasks)

results = await batch_generate(["问题1", "问题2", "问题3"])

--- 模式 3：上下文管理器 ---

async with create_async_client('deepseek', 'aiohttp', api_key='sk-xxx') as client:
    response = await client.generate("你好")

--- 模式 4：流式响应 ---

async for chunk in async_client.generate_stream("你好"):
    print(chunk, end='', flush=True)
""")


async def demo_async_backend_switcher():
    """演示异步运行时切换"""
    print("\n" + "=" * 60)
    print("异步运行时切换")
    print("=" * 60)

    print("""
    --- 异步切换器使用 ---

    from llm.core import BackendSwitcher

    switcher = (
        BackendSwitcher("deepseek")
        .add_backend("aiohttp", api_key="sk-xxx")
        .add_backend("openai_sdk", api_key="sk-xxx", base_url="...")
    )

    # 获取异步客户端
    async_client = switcher.get_async_client()
    response = await async_client.generate("你好")

    # 切换实现
    switcher.switch_to("openai_sdk")
    async_client = switcher.get_async_client()
    response = await async_client.generate("你好")
    """)


async def demo_async_best_practices():
    """演示异步最佳实践"""
    print("\n" + "=" * 60)
    print("异步最佳实践")
    print("=" * 60)

    print("""
--- 最佳实践 1：复用客户端 ---

# 推荐：创建一次，多次使用
client = create_async_client('deepseek', 'aiohttp', api_key='sk-xxx')

async def process_batch(prompts):
    tasks = [client.generate(p) for p in prompts]
    return await asyncio.gather(*tasks)

# 不推荐：每次调用都创建新客户端
async def process_batch_bad(prompts):
    tasks = [
        create_async_client('deepseek', 'aiohttp', api_key='sk-xxx').generate(p)
        for p in prompts
    ]
    return await asyncio.gather(*tasks)

--- 最佳实践 2：错误处理 ---

from llm.core import LLMError, LLMTimeoutError

async def safe_generate(prompt: str):
    try:
        client = create_async_client('deepseek', 'aiohttp', api_key='sk-xxx')
        return await client.generate(prompt)
    except LLMTimeoutError:
        return "请求超时"
    except LLMError as e:
        return f"LLM 错误: {e}"

--- 最佳实践 3：超时控制 ---

async def generate_with_timeout(prompt: str, timeout: float = 30.0):
    client = create_async_client(
        'deepseek', 'aiohttp',
        api_key='sk-xxx',
        timeout=timeout
    )
    return await asyncio.wait_for(
        client.generate(prompt),
        timeout=timeout
    )

--- 最佳实践 4：优雅关闭 ---

async def main():
    client = create_async_client('deepseek', 'aiohttp', api_key='sk-xxx')
    try:
        response = await client.generate("你好")
        print(response)
    finally:
        # 如果有 close 方法，确保关闭
        if hasattr(client, 'close'):
            await client.close()
""")


async def main():
    """主函数"""
    await demo_async_builder()
    await demo_async_convenience()
    await demo_async_patterns()
    await demo_async_backend_switcher()
    await demo_async_best_practices()

    print("\n" + "=" * 60)
    print("异步示例演示完成！")
    print("=" * 60)
    print("\n提示：实际调用 LLM 需要有效的 API 密钥")
    print("      本示例仅展示 API 用法，未实际调用 LLM")


if __name__ == "__main__":
    asyncio.run(main())
