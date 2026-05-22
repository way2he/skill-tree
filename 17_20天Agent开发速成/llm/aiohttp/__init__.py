# -*- coding: utf-8 -*-
"""
异步 LLM 客户端
支持 Ollama、OpenAI、Anthropic、火山引擎(豆包)、通义千问、智谱 AI、文心一言、月之暗面、深度求索、MiniMax

使用示例:
    import asyncio
    from llm.aiohttp import create_async_llm_client, async_llm_generate

    async def main():
        # 方式1: 使用工厂函数创建客户端
        client = create_async_llm_client("ollama", model="qwen3.5:9b")
        response = await client.generate("你好，请介绍一下自己")
        print(response)

        # 方式2: 使用便捷函数
        response = await async_llm_generate(
            "你好",
            provider="openai",
            model="gpt-4o-mini",
            api_key="sk-xxx"
        )
        print(response)

        # 方式3: 生成 JSON
        json_str = await async_llm_generate_json(
            "生成一个用户对象",
            provider="doubao",
            schema={"type": "object", "properties": {"name": {"type": "string"}}}
        )
        print(json_str)

    if __name__ == "__main__":
        asyncio.run(main())
"""

from .providers import (
    AsyncLLMResponse,
    BaseAsyncLLMClient,
    AsyncOllamaClient,
    AsyncOpenAIClient,
    AsyncAnthropicClient,
    AsyncDoubaoClient,
    AsyncQwenClient,
    AsyncGLMClient,
    AsyncWenxinClient,
    AsyncKimiClient,
    AsyncDeepSeekClient,
    AsyncMiniMaxClient,
    AsyncXAIClient,
    AsyncCohereClient,
    AsyncHunyuanOpenAIClient,
    AsyncPanguClient,
    AsyncMistralClient,
    AsyncTogetherClient,
    AsyncMiLMClient,
)
from .config import (
    AsyncLLMConfig,
    create_async_llm_client,
    async_llm_generate,
    async_llm_generate_json,
)
from .utils import (
    validate_json_output,
    async_generate_with_retry,
    async_generate_from_pydantic,
    AsyncRateLimiter,
)

__all__ = [
    "AsyncLLMResponse",
    "BaseAsyncLLMClient",
    "AsyncOllamaClient",
    "AsyncOpenAIClient",
    "AsyncAnthropicClient",
    "AsyncDoubaoClient",
    "AsyncQwenClient",
    "AsyncGLMClient",
    "AsyncWenxinClient",
    "AsyncKimiClient",
    "AsyncDeepSeekClient",
    "AsyncMiniMaxClient",
    "AsyncXAIClient",
    "AsyncCohereClient",
    "AsyncHunyuanOpenAIClient",
    "AsyncPanguClient",
    "AsyncMistralClient",
    "AsyncTogetherClient",
    "AsyncMiLMClient",
    "AsyncLLMConfig",
    "create_async_llm_client",
    "async_llm_generate",
    "async_llm_generate_json",
    "validate_json_output",
    "async_generate_with_retry",
    "async_generate_from_pydantic",
    "AsyncRateLimiter",
]
