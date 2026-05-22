# -*- coding: utf-8 -*-
"""
异步 LLM 配置模块
提供默认配置和便捷的客户端创建功能
"""

import os
from typing import Any, Dict, Literal, Optional

from .providers import (
    BaseAsyncLLMClient,
    AsyncOllamaClient,
    AsyncOpenAIClient,
    AsyncAnthropicClient,
    AsyncDoubaoClient,
    AsyncQwenClient,
    AsyncGLMClient,
    AsyncWenxinClient,
    AsyncKimiClient,
    AsyncDeepSeekClient,
    AsyncMiniMaxClient,
    AsyncXAIClient,
    AsyncCohereClient,
    AsyncHunyuanOpenAIClient,
    AsyncPanguClient,
    AsyncMistralClient,
    AsyncTogetherClient,
    AsyncMiLMClient,
)

# 默认配置
DEFAULT_PROVIDERS: Dict[str, Dict[str, Any]] = {
    "ollama": {"model": "qwen3.5:9b", "base_url": "http://localhost:11434"},
    "openai": {"model": "gpt-4o-mini", "base_url": "https://api.openai.com/v1"},
    "anthropic": {"model": "claude-sonnet-4-20250514"},
    "doubao": {"model": "doubao-seed-2-0-code-preview-260215", "region": "cn-beijing"},
    "qwen": {"model": "qwen-plus"},
    "glm": {"model": "glm-4"},
    "wenxin": {"model": "ernie-4.0-turbo-128k"},
    "kimi": {"model": "moonshot-v1-8k"},
    "deepseek": {"model": "deepseek-chat"},
    "minimax": {"model": "abab6.5s-chat"},
    "xai": {"model": "grok-3-beta", "base_url": "https://api.x.ai/v1"},
    "cohere": {"model": "command-r-plus-08-2024", "base_url": "https://api.cohere.com/v1"},
    "hunyuan": {"model": "hunyuan-turbo"},
    "pangu": {"model": "pangu-large"},
    "mistral": {"model": "mistral-large-latest", "base_url": "https://api.mistral.ai/v1"},
    "together": {"model": "meta-llama/Llama-3.3-70B-Instruct-Turbo", "base_url": "https://api.together.xyz/v1"},
    "milm": {"model": "milm-pro", "base_url": "https://api.mi.ai/v1"},
}


class AsyncLLMConfig:
    """
    异步 LLM 配置类
    提供默认配置和便捷的客户端创建功能

    使用示例:
        # 使用默认配置
        config = AsyncLLMConfig()
        client = config.create_client()

        # 切换提供商
        config.provider = "openai"
        client = config.create_client()

        # 自定义模型参数
        config.set_model("qwen3.5:9b")
        client = config.create_client()
    """

    def __init__(
        self,
        provider: Literal[
            "ollama",
            "openai",
            "anthropic",
            "doubao",
            "qwen",
            "glm",
            "wenxin",
            "kimi",
            "deepseek",
            "minimax",
            "xai",
            "cohere",
            "hunyuan",
            "pangu",
            "mistral",
            "together",
            "milm",
        ] = "ollama",
        model: Optional[str] = None,
        **kwargs: Any,
    ):
        self.provider = provider
        self._model = model
        self._extra_params: Dict[str, Any] = kwargs

    def set_model(self, model: str) -> "AsyncLLMConfig":
        """设置模型名称"""
        self._model = model
        return self

    def set_provider(
        self,
        provider: Literal[
            "ollama",
            "openai",
            "anthropic",
            "doubao",
            "qwen",
            "glm",
            "wenxin",
            "kimi",
            "deepseek",
            "minimax",
            "xai",
            "cohere",
            "hunyuan",
            "pangu",
            "mistral",
            "together",
            "milm",
        ],
    ) -> "AsyncLLMConfig":
        """设置提供商"""
        self.provider = provider
        return self

    def add_params(self, **kwargs: Any) -> "AsyncLLMConfig":
        """添加额外参数"""
        self._extra_params.update(kwargs)
        return self

    def create_client(self) -> BaseAsyncLLMClient:
        """
        根据配置创建异步 LLM 客户端

        Returns:
            BaseAsyncLLMClient: 对应的异步 LLM 客户端实例
        """
        params = DEFAULT_PROVIDERS.get(self.provider, {}).copy()

        if self._model:
            params["model"] = self._model

        params.update(self._extra_params)

        return create_async_llm_client(self.provider, **params)

    @classmethod
    def from_env(cls) -> "AsyncLLMConfig":
        """
        从环境变量加载配置

        支持的环境变量:
            - LLM_PROVIDER: 提供商类型
            - LLM_MODEL: 模型名称
            - LLM_BASE_URL: API 端点
            - LLM_REGION: 区域（火山引擎）
        """
        provider_env = os.getenv("LLM_PROVIDER", "ollama")
        model = os.getenv("LLM_MODEL")
        base_url = os.getenv("LLM_BASE_URL")
        region = os.getenv("LLM_REGION")

        valid_providers = [
            "ollama",
            "openai",
            "anthropic",
            "doubao",
            "qwen",
            "glm",
            "wenxin",
            "kimi",
            "deepseek",
            "minimax",
            "xai",
            "cohere",
            "hunyuan",
            "pangu",
            "mistral",
            "together",
            "milm",
        ]
        if provider_env not in valid_providers:
            provider_env = "ollama"

        config = cls(provider=provider_env)  # type: ignore

        if model:
            config.set_model(model)

        if base_url:
            config.add_params(base_url=base_url)

        if region:
            config.add_params(region=region)

        return config


def create_async_llm_client(
    provider: Literal[
        "ollama",
        "openai",
        "anthropic",
        "doubao",
        "qwen",
        "glm",
        "wenxin",
        "kimi",
        "deepseek",
        "minimax",
        "xai",
        "cohere",
        "hunyuan",
        "pangu",
        "mistral",
        "together",
        "milm",
    ],
    **kwargs: Any,
) -> BaseAsyncLLMClient:
    """
    创建异步 LLM 客户端工厂函数

    Args:
        provider: 提供商类型
            - "ollama": 本地 Ollama 模型
            - "openai": OpenAI / Azure OpenAI
            - "anthropic": Anthropic Claude
            - "doubao": 火山引擎豆包
            - "qwen": 阿里云通义千问
            - "glm": 智谱 AI GLM
            - "wenxin": 百度文心一言
            - "kimi": 月之暗面 Kimi
            - "deepseek": 深度求索 DeepSeek
            - "minimax": MiniMax
            - "xai": xAI / Grok
            - "cohere": Cohere
            - "hunyuan": 腾讯云混元
            - "pangu": 华为云盘古
            - "mistral": Mistral AI
            - "together": Together.ai（开源模型平台）
            - "milm": 小米小爱大模型

    Returns:
        对应的异步 LLM 客户端实例
    """
    clients: Dict[str, Any] = {
        "ollama": AsyncOllamaClient,
        "openai": AsyncOpenAIClient,
        "anthropic": AsyncAnthropicClient,
        "doubao": AsyncDoubaoClient,
        "qwen": AsyncQwenClient,
        "glm": AsyncGLMClient,
        "wenxin": AsyncWenxinClient,
        "kimi": AsyncKimiClient,
        "deepseek": AsyncDeepSeekClient,
        "minimax": AsyncMiniMaxClient,
        "xai": AsyncXAIClient,
        "cohere": AsyncCohereClient,
        "hunyuan": AsyncHunyuanOpenAIClient,
        "pangu": AsyncPanguClient,
        "mistral": AsyncMistralClient,
        "together": AsyncTogetherClient,
        "milm": AsyncMiLMClient,
    }

    if provider not in clients:
        raise ValueError(
            f"不支持的 provider: {provider}，支持的选项: {list(clients.keys())}"
        )

    return clients[provider](**kwargs)


async def async_llm_generate(
    prompt: str,
    provider: Literal[
        "ollama",
        "openai",
        "anthropic",
        "doubao",
        "qwen",
        "glm",
        "wenxin",
        "kimi",
        "deepseek",
        "minimax",
        "xai",
        "cohere",
        "hunyuan",
        "pangu",
        "mistral",
        "together",
        "milm",
    ] = "ollama",
    **kwargs: Any,
) -> str:
    """
    统一的异步 LLM 生成接口（便捷函数）

    Args:
        prompt: 用户提示词
        provider: 提供商类型
        **kwargs: 传递给客户端的其他参数

    Returns:
        模型生成的文本
    """
    client = create_async_llm_client(provider, **kwargs)
    return await client.generate(prompt)


async def async_llm_generate_json(
    prompt: str,
    schema: Optional[Dict[str, Any]] = None,
    provider: Literal[
        "ollama",
        "openai",
        "anthropic",
        "doubao",
        "qwen",
        "glm",
        "wenxin",
        "kimi",
        "deepseek",
        "minimax",
        "xai",
        "cohere",
        "hunyuan",
        "pangu",
        "mistral",
        "together",
        "milm",
    ] = "ollama",
    **kwargs: Any,
) -> str:
    """
    统一的异步 JSON 生成接口

    Args:
        prompt: 用户提示词
        schema: JSON Schema
        provider: 提供商类型
        **kwargs: 传递给客户端的其他参数

    Returns:
        模型生成的 JSON 字符串
    """
    client = create_async_llm_client(provider, **kwargs)
    return await client.generate_json(prompt, schema)
