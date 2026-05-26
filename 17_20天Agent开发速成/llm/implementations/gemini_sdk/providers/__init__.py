# -*- coding: utf-8 -*-
"""
Google Gemini 官方 SDK 提供商模块

提供基于 google-generativeai SDK 的 Gemini 大模型调用封装。
"""

from typing import Any, Optional

from ..client import GoogleClient
from .gemini import GeminiOfficialClient


def create_google_client(
    provider: str,
    api_key: str,
    model: Optional[str] = None,
    **kwargs: Any
) -> GoogleClient:
    """
    创建 Google Gemini 官方 SDK 客户端

    Args:
        provider: 提供商名称，如 "gemini"
        api_key: API Key
        model: 模型名称
        **kwargs: 其他参数

    Returns:
        GoogleClient 实例

    Raises:
        ValueError: 如果提供商不受支持

    Example:
        >>> client = create_google_client(
        ...     provider="gemini",
        ...     api_key="your-api-key",
        ...     model="gemini-pro"
        ... )
        >>> response = client.generate("你好")
    """
    clients: dict[str, type[GoogleClient]] = {
        "gemini": GeminiOfficialClient,
    }

    if provider not in clients:
        raise ValueError(
            f"不支持的 Google 提供商: {provider}，"
            f"支持的提供商: {list(clients.keys())}"
        )

    client_class = clients[provider]
    return client_class(api_key=api_key, model=model, **kwargs)


__all__ = [
    "GeminiOfficialClient",
    "create_google_client",
]
