# -*- coding: utf-8 -*-
"""
百度文心一言 - 不兼容 OpenAI 协议

百度文心一言使用独立的 API 格式，不兼容 OpenAI Chat Completions API。
请使用以下方式调用：
- llm.requests.providers 中的 WenxinClient（基于 requests 库）
- llm.aiohttp.providers 中的 AsyncWenxinClient（基于 aiohttp 库）
- 百度文心一言官方 SDK
"""


class WenxinPlaceholder:
    """
    百度文心一言占位类（不兼容 OpenAI 协议）

    此类仅作为占位符，不可直接使用。
    请使用 llm.requests.providers 或 llm.aiohttp.providers 中的对应客户端。
    """

    def __init__(self, **kwargs) -> None:
        raise NotImplementedError(
            "百度文心一言不兼容 OpenAI 协议。"
            "请使用 llm.requests.providers.WenxinClient 或 llm.aiohttp.providers.AsyncWenxinClient。"
        )
