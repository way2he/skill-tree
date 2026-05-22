#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM OpenAI 模块初始化
支持 OpenAI SDK 兼容协议的厂商调用

子模块：
- client: 原有客户端（基于 requests，向后兼容）
- providers: 基于 OpenAI SDK 的厂商客户端（新增）
"""

# 保留原有导出（向后兼容）
from .client import (
    get_client,
    chat_completion,
    get_response_content,
    get_tool_call_args,
    set_api_key,
    generate_json,
)

# 新增 providers 模块导出
from .providers import (
    OpenAICompatibleClient,
    OpenAIClient,
    DeepSeekClient,
    QwenClient,
    DoubaoClient,
    GLMClient,
    KimiClient,
    MiniMaxClient,
    MiLMClient,
    TogetherClient,
    XAIClient,
    MistralClient,
    ShangtangClient,
    StepfunClient,
    TiangongClient,
    BaichuanClient,
    YiClient,
    SparkClient,
    MetaClient,
    create_openai_client,
)

__all__ = [
    # 原有导出（向后兼容）
    "get_client",
    "chat_completion",
    "get_response_content",
    "get_tool_call_args",
    "set_api_key",
    "generate_json",
    # 新增 providers 导出
    "OpenAICompatibleClient",
    "OpenAIClient",
    "DeepSeekClient",
    "QwenClient",
    "DoubaoClient",
    "GLMClient",
    "KimiClient",
    "MiniMaxClient",
    "MiLMClient",
    "TogetherClient",
    "XAIClient",
    "MistralClient",
    "ShangtangClient",
    "StepfunClient",
    "TiangongClient",
    "BaichuanClient",
    "YiClient",
    "SparkClient",
    "MetaClient",
    "create_openai_client",
]
