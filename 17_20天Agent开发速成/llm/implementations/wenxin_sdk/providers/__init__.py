# -*- coding: utf-8 -*-
"""
百度千帆官方 SDK 提供商模块

提供基于 qianfan SDK 的百度文心大模型调用封装。
"""

from typing import Any, Optional

from ..client import BaiduClient
from .wenxin import WenxinClient


def create_baidu_client(
    provider: str,
    ak: str,
    sk: str,
    model: Optional[str] = None,
    **kwargs: Any
) -> BaiduClient:
    """
    创建百度千帆官方 SDK 客户端

    Args:
        provider: 提供商名称，如 "wenxin"
        ak: Access Key
        sk: Secret Key
        model: 模型名称
        **kwargs: 其他参数

    Returns:
        BaiduClient 实例

    Raises:
        ValueError: 如果提供商不受支持

    Example:
        >>> client = create_baidu_client(
        ...     provider="wenxin",
        ...     ak="your-ak",
        ...     sk="your-sk",
        ...     model="ERNIE-Bot-4"
        ... )
        >>> response = client.generate("你好")
    """
    clients: dict[str, type[BaiduClient]] = {
        "wenxin": WenxinClient,
    }

    if provider not in clients:
        raise ValueError(
            f"不支持的百度提供商: {provider}，"
            f"支持的提供商: {list(clients.keys())}"
        )

    client_class = clients[provider]
    return client_class(ak=ak, sk=sk, model=model, **kwargs)


__all__ = [
    "WenxinClient",
    "create_baidu_client",
]
