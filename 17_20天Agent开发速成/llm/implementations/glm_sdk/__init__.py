# -*- coding: utf-8 -*-
"""
智谱 AI 官方 SDK 模块

提供基于 zhipuai SDK 的 ChatGLM 大模型调用封装。

依赖安装：
    pip install zhipuai

文档参考：
    https://open.bigmodel.cn/dev/api
"""

from .client import ZhipuClient, ZhipuAIClient
from .providers import ChatGLMClient, create_zhipu_client

__all__ = [
    "ZhipuClient",
    "ZhipuAIClient",
    "ChatGLMClient",
    "create_zhipu_client",
]
