# -*- coding: utf-8 -*-
"""
腾讯混元 - 不兼容 OpenAI 协议

腾讯混元使用独立的 API 格式，不兼容 OpenAI Chat Completions API。
请使用以下方式调用：
- llm.requests.providers 中的 HunyuanClient（基于 requests 库）
- llm.aiohttp.providers 中的 AsyncHunyuanOpenAIClient（基于 aiohttp 库）
- 腾讯混元官方 SDK
"""


class HunyuanPlaceholder:
    """
    腾讯混元占位类（不兼容 OpenAI 协议）

    此类仅作为占位符，不可直接使用。
    请使用 llm.requests.providers 或 llm.aiohttp.providers 中的对应客户端。
    """

    def __init__(self, **kwargs) -> None:
        raise NotImplementedError(
            "腾讯混元不兼容 OpenAI 协议。"
            "请使用 llm.requests.providers.HunyuanClient 或 llm.aiohttp.providers.AsyncHunyuanOpenAIClient。"
        )
