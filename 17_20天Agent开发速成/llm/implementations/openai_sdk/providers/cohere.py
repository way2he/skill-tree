# -*- coding: utf-8 -*-
"""
Cohere - 不兼容 OpenAI 协议

Cohere 使用独立的 API 格式，不兼容 OpenAI Chat Completions API。
请使用以下方式调用：
- llm.requests.providers 中的 CohereClient（基于 requests 库）
- llm.aiohttp.providers 中的 AsyncCohereClient（基于 aiohttp 库）
- Cohere 官方 SDK
"""


class CoherePlaceholder:
    """
    Cohere 占位类（不兼容 OpenAI 协议）

    此类仅作为占位符，不可直接使用。
    请使用 llm.requests.providers 或 llm.aiohttp.providers 中的对应客户端。
    """

    def __init__(self, **kwargs) -> None:
        raise NotImplementedError(
            "Cohere 不兼容 OpenAI 协议。"
            "请使用 llm.requests.providers.CohereClient 或 llm.aiohttp.providers.AsyncCohereClient。"
        )
