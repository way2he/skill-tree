# -*- coding: utf-8 -*-
"""
llm.anthropic - Anthropic Claude SDK 客户端模块

本模块提供基于 Anthropic 官方 Python SDK 的客户端封装，
支持 Claude 系列模型的文本生成、JSON 结构化输出和流式输出。

使用方式：
    from llm.anthropic import AnthropicClient

    client = AnthropicClient(api_key="sk-ant-...")
    result = client.generate("你好，请介绍一下你自己")

环境变量：
    ANTHROPIC_API_KEY: Anthropic API 密钥

子模块：
    - client: AnthropicClient 主客户端
    - providers: 基于 Anthropic SDK 的 provider 实现
"""

from .client import AnthropicClient


def get_default_model() -> str:
    """
    获取 Anthropic 默认模型名称。

    Returns:
        str: 默认模型名称 "claude-sonnet-4-20250514"。
    """
    return "claude-sonnet-4-20250514"


def list_available_models() -> list[str]:
    """
    列出常用的 Anthropic Claude 模型。

    Returns:
        list[str]: 常用模型名称列表。
    """
    return [
        "claude-sonnet-4-20250514",
        "claude-opus-4-20250514",
        "claude-haiku-4-20250414",
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022",
        "claude-3-opus-20240229",
    ]


__all__ = [
    "AnthropicClient",
    "get_default_model",
    "list_available_models",
]
