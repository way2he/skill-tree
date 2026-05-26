# -*- coding: utf-8 -*-
"""
llm.anthropic.providers - Anthropic SDK Provider 实现

本模块提供基于 Anthropic SDK 的 provider 实现，
继承自统一的 Anthropic SDK 兼容基类。

使用方式：
    from llm.anthropic.providers import AnthropicSDKClient

    client = AnthropicSDKClient(api_key="sk-ant-...")
    result = client.generate("你好")
"""

from .anthropic import AnthropicSDKClient
from .deepseek import DeepSeekSDKClient


__all__ = [
    "AnthropicSDKClient",
    "DeepSeekSDKClient",
]
