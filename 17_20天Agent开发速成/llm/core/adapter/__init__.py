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
    BaseLLMAdapter: 适配器基类（用于自定义适配器）
    BaseAsyncLLMAdapter: 异步适配器基类（用于自定义适配器）
"""

from .base import (
    IProviderClient,
    IAdapter,
    LLMResult,
    StreamChunk,
    publish_llm_event,
    BaseLLMAdapter,
    BaseAsyncLLMAdapter,
)
from .unified_adapter import UnifiedAdapter

__all__ = [
    # 接口和类型
    "IProviderClient",
    "IAdapter",
    "LLMResult",
    "StreamChunk",
    # 实现
    "UnifiedAdapter",
    # 适配器基类（用于自定义适配器）
    "BaseLLMAdapter",
    "BaseAsyncLLMAdapter",
    # 工具函数
    "publish_llm_event",
]
