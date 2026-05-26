# -*- coding: utf-8 -*-
"""
智谱 AI 官方 SDK 提供商模块

提供基于 zhipuai SDK 的 ChatGLM 大模型调用封装。
"""

from typing import Any, Optional

from ..client import ZhipuClient
from .chatglm import ChatGLMClient


def create_zhipu_client(
    provider: str,
    api_key: str,
    model: Optional[str] = None,
    **kwargs: Any
) -> ZhipuClient:
    """
    创建智谱 AI 官方 SDK 客户端

    Args:
        provider: 提供商名称，如 "chatglm"
        api_key: API Key
        model: 模型名称
        **kwargs: 其他参数

    Returns:
        ZhipuClient 实例

    Raises:
        ValueError: 如果提供商不受支持

    Example:
        >>> client = create_zhipu_client(
        ...     provider="chatglm",
        ...     api_key="your-api-key",
        ...     model="glm-4"
        ... )
        >>> response = client.generate("你好")
    """
    clients: dict[str, type[ZhipuClient]] = {
        "chatglm": ChatGLMClient,
    }

    if provider not in clients:
        raise ValueError(
            f"不支持的智谱 AI 提供商: {provider}，"
            f"支持的提供商: {list(clients.keys())}"
        )

    client_class = clients[provider]
    return client_class(api_key=api_key, model=model, **kwargs)


__all__ = [
    "ChatGLMClient",
    "create_zhipu_client",
]
