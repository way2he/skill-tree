# -*- coding: utf-8 -*-
"""
火山引擎 Providers 模块

包含基于 volcengine-python-sdk 的厂商客户端。
"""

from .doubao import DoubaoClient

__all__ = ["DoubaoClient"]


def create_volcengine_client(
    provider: str,
    ak: str,
    sk: str,
    region: str = "cn-beijing",
    **kwargs
):
    """
    创建火山引擎客户端工厂函数

    Args:
        provider: 提供商名称，如 "doubao"
        ak: Access Key
        sk: Secret Key
        region: 区域，默认 "cn-beijing"
        **kwargs: 其他参数

    Returns:
        对应的火山引擎客户端实例
    """
    clients = {
        "doubao": DoubaoClient,
    }

    provider_lower = provider.lower()
    if provider_lower not in clients:
        raise ValueError(
            f"不支持的 provider: {provider}，支持的选项: {list(clients.keys())}"
        )

    return clients[provider_lower](ak=ak, sk=sk, region=region, **kwargs)
