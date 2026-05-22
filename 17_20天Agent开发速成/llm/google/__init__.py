# -*- coding: utf-8 -*-
"""
Google Gemini 官方 SDK 模块

提供基于 google-generativeai SDK 的 Gemini 大模型调用封装。

依赖安装：
    pip install google-generativeai

文档参考：
    https://ai.google.dev/gemini-api/docs
"""

from .client import GoogleClient, GeminiClient
from .providers import GeminiOfficialClient, create_google_client

__all__ = [
    "GoogleClient",
    "GeminiClient",
    "GeminiOfficialClient",
    "create_google_client",
]
