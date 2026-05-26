# -*- coding: utf-8 -*-
"""
阿里云灵积官方 SDK 提供商模块

提供基于 dashscope SDK 的阿里云大模型调用封装。
"""

from typing import Any, Optional

from ..client import AlibabaClient
from .qwen import QwenClient


def create_alibaba_client(
    provider: str,
    api_key: str,
    model: Optional[str] = None,
    **kwargs: Any
) -> AlibabaClient:
    """
    创建阿里云灵积官方 SDK 客户端

    Args:
        provider: 提供商名称，如 "qwen"
        api_key: API Key
        model: 模型名称
        **kwargs: 其他参数

    Returns:
        AlibabaClient 实例

    Raises:
        ValueError: 如果提供商不受支持

    Example:
        >>> client = create_alibaba_client(
        ...     provider="qwen",
        ...     api_key="your-api-key",
        ...     model="qwen-turbo"
        ... )
        >>> response = client.generate("你好")
    """
    clients: dict[str, type[AlibabaClient]] = {
        "qwen": QwenClient,
    }

    if provider not in clients:
        raise ValueError(
            f"不支持的阿里云提供商: {provider}，"
            f"支持的提供商: {list(clients.keys())}"
        )

    client_class = clients[provider]
    return client_class(api_key=api_key, model=model, **kwargs)


__all__ = [
    "QwenClient",
    "create_alibaba_client",
]
