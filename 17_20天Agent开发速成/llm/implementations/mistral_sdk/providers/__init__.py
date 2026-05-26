# -*- coding: utf-8 -*-
"""
Mistral AI 官方 SDK 提供商模块

提供基于 mistralai SDK 的 Mistral 大模型调用封装。
"""

from typing import Any, Optional

from ..client import MistralClient
from .mistral_official import MistralOfficialClient


def create_mistral_client(
    provider: str,
    api_key: str,
    model: Optional[str] = None,
    **kwargs: Any
) -> MistralClient:
    """
    创建 Mistral AI 官方 SDK 客户端

    Args:
        provider: 提供商名称，如 "mistral"
        api_key: API Key
        model: 模型名称
        **kwargs: 其他参数

    Returns:
        MistralClient 实例

    Raises:
        ValueError: 如果提供商不受支持

    Example:
        >>> client = create_mistral_client(
        ...     provider="mistral",
        ...     api_key="your-api-key",
        ...     model="mistral-medium"
        ... )
        >>> response = client.generate("你好")
    """
    clients: dict[str, type[MistralClient]] = {
        "mistral": MistralOfficialClient,
    }

    if provider not in clients:
        raise ValueError(
            f"不支持的 Mistral 提供商: {provider}，"
            f"支持的提供商: {list(clients.keys())}"
        )

    client_class = clients[provider]
    return client_class(api_key=api_key, model=model, **kwargs)


__all__ = [
    "MistralOfficialClient",
    "create_mistral_client",
]
