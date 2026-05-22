# -*- coding: utf-8 -*-
"""
Mistral AI 官方 SDK 模块

提供基于 mistralai SDK 的 Mistral 大模型调用封装。

依赖安装：
    pip install mistralai

文档参考：
    https://docs.mistral.ai/
"""

from .client import MistralClient
from .providers import MistralOfficialClient, create_mistral_client

__all__ = [
    "MistralClient",
    "MistralOfficialClient",
    "create_mistral_client",
]
