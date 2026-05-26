# -*- coding: utf-8 -*-
"""
Cohere 官方 SDK 模块

提供基于 cohere SDK 的 Cohere 大模型调用封装。

依赖安装：
    pip install cohere

文档参考：
    https://docs.cohere.com/docs
"""

from .client import CohereClient
from .providers import CohereOfficialClient, create_cohere_client

__all__ = [
    "CohereClient",
    "CohereOfficialClient",
    "create_cohere_client",
]
