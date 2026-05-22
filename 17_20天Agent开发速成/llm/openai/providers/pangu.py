# -*- coding: utf-8 -*-
"""
华为盘古 - 不兼容 OpenAI 协议

华为盘古使用独立的 API 格式，不兼容 OpenAI Chat Completions API。
请使用以下方式调用：
- llm.requests.providers 中的 PanguClient（基于 requests 库）
- llm.aiohttp.providers 中的 AsyncPanguClient（基于 aiohttp 库）
- 华为盘古官方 SDK
"""


class PanguPlaceholder:
    """
    华为盘古占位类（不兼容 OpenAI 协议）

    此类仅作为占位符，不可直接使用。
    请使用 llm.requests.providers 或 llm.aiohttp.providers 中的对应客户端。
    """

    def __init__(self, **kwargs) -> None:
        raise NotImplementedError(
            "华为盘古不兼容 OpenAI 协议。"
            "请使用 llm.requests.providers.PanguClient 或 llm.aiohttp.providers.AsyncPanguClient。"
        )
