# -*- coding: utf-8 -*-
"""
Cohere 官方 SDK 提供商模块

提供基于 cohere SDK 的 Cohere 大模型调用封装。
"""

from typing import Any, Optional

from ..client import CohereClient
from .cohere_official import CohereOfficialClient


def create_cohere_client(
    provider: str,
    api_key: str,
    model: Optional[str] = None,
    **kwargs: Any
) -> CohereClient:
    """
    创建 Cohere 官方 SDK 客户端

    Args:
        provider: 提供商名称，如 "cohere"
        api_key: API Key
        model: 模型名称
        **kwargs: 其他参数

    Returns:
        CohereClient 实例

    Raises:
        ValueError: 如果提供商不受支持

    Example:
        >>> client = create_cohere_client(
        ...     provider="cohere",
        ...     api_key="your-api-key",
        ...     model="command-r"
        ... )
        >>> response = client.generate("你好")
    """
    clients: dict[str, type[CohereClient]] = {
        "cohere": CohereOfficialClient,
    }

    if provider not in clients:
        raise ValueError(
            f"不支持的 Cohere 提供商: {provider}，"
            f"支持的提供商: {list(clients.keys())}"
        )

    client_class = clients[provider]
    return client_class(api_key=api_key, model=model, **kwargs)


__all__ = [
    "CohereOfficialClient",
    "create_cohere_client",
]
