# -*- coding: utf-8 -*-
"""
llm.ollama - Ollama 官方 SDK 模块

基于 ollama 官方 Python SDK 封装的模块，提供同步和异步的客户端。
"""

from .client import (
    OllamaOfficialClient,
    AsyncOllamaOfficialClient,
    DEFAULT_MODEL,
    DEFAULT_HOST,
)

__all__ = [
    "OllamaOfficialClient",
    "AsyncOllamaOfficialClient",
    "DEFAULT_MODEL",
    "DEFAULT_HOST",
]
