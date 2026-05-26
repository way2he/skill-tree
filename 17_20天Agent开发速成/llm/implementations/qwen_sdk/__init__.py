# -*- coding: utf-8 -*-
"""
阿里云灵积模型服务官方 SDK 模块

提供基于 dashscope SDK 的阿里云大模型调用封装。

依赖安装：
    pip install dashscope

文档参考：
    https://help.aliyun.com/zh/dashscope/developer-reference/api-details
"""

from .client import AlibabaClient, DashscopeClient
from .providers import QwenClient, create_alibaba_client

__all__ = [
    "AlibabaClient",
    "DashscopeClient",
    "QwenClient",
    "create_alibaba_client",
]
