# -*- coding: utf-8 -*-
"""
Groq 官方 SDK 模块

提供基于 groq SDK 的 Groq 大模型调用封装。

依赖安装：
    pip install groq

文档参考：
    https://console.groq.com/docs
"""

from .client import GroqClient
from .providers import GroqOfficialClient, create_groq_client

__all__ = [
    "GroqClient",
    "GroqOfficialClient",
    "create_groq_client",
]
