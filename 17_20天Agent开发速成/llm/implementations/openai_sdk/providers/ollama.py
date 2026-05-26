# -*- coding: utf-8 -*-
"""
Ollama - 不兼容 OpenAI 协议

Ollama 使用独立的 API 格式，不兼容 OpenAI Chat Completions API。
请使用以下方式调用：
- llm.requests.providers 中的 OllamaClient（基于 requests 库）
- llm.aiohttp.providers 中的 AsyncOllamaClient（基于 aiohttp 库）
- Ollama 官方 SDK
"""


class OllamaPlaceholder:
    """
    Ollama 占位类（不兼容 OpenAI 协议）

    此类仅作为占位符，不可直接使用。
    请使用 llm.requests.providers 或 llm.aiohttp.providers 中的对应客户端。
    """

    def __init__(self, **kwargs) -> None:
        raise NotImplementedError(
            "Ollama 不兼容 OpenAI 协议。"
            "请使用 llm.requests.providers.OllamaClient 或 llm.aiohttp.providers.AsyncOllamaClient。"
        )
