#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAI 模块初始化
"""

from .client import (
    get_client,
    chat_completion,
    get_response_content,
    get_tool_call_args,
    set_api_key,
)

__all__ = [
    "get_client",
    "chat_completion",
    "get_response_content",
    "get_tool_call_args",
    "set_api_key",
]