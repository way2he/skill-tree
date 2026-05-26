# -*- coding: utf-8 -*-
"""
Groq 官方 SDK 提供商模块

提供基于 groq SDK 的 Groq 大模型调用封装。
"""

from typing import Any, Optional

from ..client import GroqClient
from .groq_official import GroqOfficialClient


def create_groq_client(
    provider: str,
    api_key: str,
    model: Optional[str] = None,
    **kwargs: Any
) -> GroqClient:
    """
    创建 Groq 官方 SDK 客户端

    Args:
        provider: 提供商名称，如 "groq"
        api_key: API Key
        model: 模型名称
        **kwargs: 其他参数

    Returns:
        GroqClient 实例

    Raises:
        ValueError: 如果提供商不受支持

    Example:
        >>> client = create_groq_client(
        ...     provider="groq",
        ...     api_key="your-api-key",
        ...     model="llama3-8b-8192"
        ... )
        >>> response = client.generate("你好")
    """
    clients: dict[str, type[GroqClient]] = {
        "groq": GroqOfficialClient,
    }

    if provider not in clients:
        raise ValueError(
            f"不支持的 Groq 提供商: {provider}，"
            f"支持的提供商: {list(clients.keys())}"
        )

    client_class = clients[provider]
    return client_class(api_key=api_key, model=model, **kwargs)


__all__ = [
    "GroqOfficialClient",
    "create_groq_client",
]
