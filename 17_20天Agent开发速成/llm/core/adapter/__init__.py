# -*- coding: utf-8 -*-
"""
LLM 统一接口层 - 适配器模块

提供模型无关的统一适配器接口。
具体模型实现由底层 providers 提供。

导出:
    IProviderClient: 底层客户端协议
    IAdapter: 适配器接口
    LLMResult: 通用响应结构
    UnifiedAdapter: 统一适配器实现

向后兼容（旧适配器）:
    BaseLLMAdapter: 旧版同步适配器基类
    BaseAsyncLLMAdapter: 旧版异步适配器基类
    RequestsLLMAdapter: 旧版透传适配器
    AioHttpLLMAdapter: 旧版异步适配器
    OpenAILLMAdapter: 旧版 OpenAI 适配器
    AnthropicLLMAdapter: 旧版 Anthropic 适配器
    OllamaLLMAdapter: 旧版 Ollama 适配器
    SDKLLMAdapter: 旧版 SDK 适配器
"""

from .base import (
    IProviderClient,
    IAdapter,
    LLMResult,
    StreamChunk,
    publish_llm_event,
    # 向后兼容
    BaseLLMAdapter,
    BaseAsyncLLMAdapter,
)
from .unified_adapter import UnifiedAdapter
from .requests_adapter import RequestsLLMAdapter
from .aiohttp_adapter import AioHttpLLMAdapter
from .openai_adapter import OpenAILLMAdapter
from .anthropic_adapter import AnthropicLLMAdapter
from .ollama_adapter import OllamaLLMAdapter
from .sdk_adapter import SDKLLMAdapter

__all__ = [
    # 接口和类型
    "IProviderClient",
    "IAdapter",
    "LLMResult",
    "StreamChunk",
    # 实现
    "UnifiedAdapter",
    # 向后兼容
    "BaseLLMAdapter",
    "BaseAsyncLLMAdapter",
    "RequestsLLMAdapter",
    "AioHttpLLMAdapter",
    "OpenAILLMAdapter",
    "AnthropicLLMAdapter",
    "OllamaLLMAdapter",
    "SDKLLMAdapter",
    # 工具函数
    "publish_llm_event",
]
