#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM 模块初始化
支持 OpenAI、Doubao（火山引擎）、Ollama 多种协议
"""

from .client import (
    get_client,
    chat_completion,
    get_response_content,
    get_tool_call_args,
    set_api_key,
    generate_json,
)

__all__ = [
    "get_client",
    "chat_completion",
    "get_response_content",
    "get_tool_call_args",
    "set_api_key",
    "generate_json",
]