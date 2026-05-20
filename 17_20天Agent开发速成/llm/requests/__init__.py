# -*- coding: utf-8 -*-
"""
LLM 公共模块
提供统一的大模型调用接口，支持多种提供商
"""

from .clients import (
    AnthropicClient,
    BaseLLMClient,
    DoubaoClient,
    OllamaClient,
    OpenAIClient,
    create_llm_client,
    llm_generate,
    llm_generate_json,
    load_env_config,
)
from .config import LLMConfig, create_llm
from .utils import generate_from_pydantic, generate_with_retry, validate_json_output

__all__ = [
    # 客户端类
    "BaseLLMClient",
    "OllamaClient",
    "OpenAIClient",
    "DoubaoClient",
    "AnthropicClient",
    # 工厂函数
    "create_llm_client",
    # 便捷函数
    "llm_generate",
    "llm_generate_json",
    "load_env_config",
    # 工具函数
    "validate_json_output",
    "generate_with_retry",
    "generate_from_pydantic",
    # 配置模块
    "LLMConfig",
    "create_llm",
]
