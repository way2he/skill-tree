# -*- coding: utf-8 -*-
"""
Ollama OpenAI SDK 客户端

Ollama 本地大模型部署工具，支持通过 OpenAI 兼容 API 调用。
Ollama 默认监听 http://localhost:11434，提供 /v1 端点兼容 OpenAI 协议。

使用示例:
    >>> from llm.implementations.openai_sdk.providers import OllamaClient
    >>> client = OllamaClient(model="qwen3:4b")
    >>> response = client.generate("你好")
    >>> print(response)

环境变量:
    OLLAMA_HOST: Ollama 服务地址，默认为 http://localhost:11434
"""

import os
from typing import Any, Optional

from .base import OpenAICompatibleClient


class OllamaClient(OpenAICompatibleClient):
    """
    Ollama 客户端（OpenAI SDK 兼容模式）

    通过 OpenAI 兼容 API 调用本地 Ollama 服务。
    Ollama 默认监听 localhost:11434，api_key 可为任意字符串（不验证）。

    Attributes:
        PROVIDER_NAME: 提供者名称
        DEFAULT_BASE_URL: 默认 API 基础地址
        DEFAULT_MODEL: 默认使用的模型名称
        ENV_API_KEY: 环境变量中 API Key 的名称（可选）
        ENV_HOST: 环境变量中 Ollama 主机地址的名称

    Examples:
        >>> # 基本用法
        >>> client = OllamaClient(model="llama3.2")
        >>> print(client.generate("你好"))

        >>> # 指定自定义地址
        >>> client = OllamaClient(
        ...     base_url="http://192.168.1.100:11434/v1",
        ...     model="qwen3:4b"
        ... )

        >>> # 使用环境变量
        >>> # export OLLAMA_HOST=http://localhost:11434
        >>> client = OllamaClient(model="deepseek-r1:7b")
    """

    PROVIDER_NAME: str = "ollama"
    DEFAULT_BASE_URL: str = "http://localhost:11434/v1"
    DEFAULT_MODEL: str = "llama3.2"
    ENV_API_KEY: str = "OLLAMA_API_KEY"
    ENV_HOST: str = "OLLAMA_HOST"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> None:
        """
        初始化 Ollama 客户端

        Args:
            api_key: API 密钥，Ollama 不强制验证，可为任意字符串或 None
            model: 模型名称，如 "llama3.2", "qwen3:4b", "deepseek-r1:7b"
            base_url: API 基础地址，默认从 OLLAMA_HOST 环境变量或 localhost 获取
            system_prompt: 系统提示词
            temperature: 温度参数，控制生成随机性 (0-2)
            max_tokens: 最大输出 token 数

        Raises:
            TypeError: 当参数类型不正确时抛出
            ValueError: 当 base_url 格式不正确时抛出

        Note:
            - api_key 对 Ollama 本地服务不敏感，可传任意字符串
            - 优先使用传入的 base_url，其次从 OLLAMA_HOST 环境变量获取
            - 默认地址为 http://localhost:11434/v1
        """
        # 参数类型校验
        if temperature is not None and not isinstance(temperature, (int, float)):
            raise TypeError(
                f"temperature 必须为数值类型，当前类型为 {type(temperature).__name__}"
            )

        if api_key is not None and not isinstance(api_key, str):
            raise TypeError(
                f"api_key 必须为字符串类型，当前类型为 {type(api_key).__name__}"
            )

        # 确定 base_url：传入值 > 环境变量 > 默认值
        final_base_url = base_url
        if final_base_url is None:
            # 从环境变量获取主机地址
            host = os.getenv(self.ENV_HOST)
            if host:
                # 确保主机地址以 /v1 结尾
                final_base_url = f"{host.rstrip('/')}/v1"
            else:
                final_base_url = self.DEFAULT_BASE_URL

        # 验证 base_url 格式
        if not isinstance(final_base_url, str):
            raise TypeError(
                f"base_url 必须为字符串类型，当前类型为 {type(final_base_url).__name__}"
            )

        if not final_base_url.startswith(("http://", "https://")):
            raise ValueError(
                f"base_url 必须以 http:// 或 https:// 开头，当前值为: {final_base_url}"
            )

        # Ollama 的 api_key 可为空字符串或任意值（本地服务不验证）
        final_api_key = api_key or os.getenv(self.ENV_API_KEY) or "ollama"

        # 调用父类初始化
        super().__init__(
            api_key=final_api_key,
            model=model or self.DEFAULT_MODEL,
            base_url=final_base_url,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )


# Provider alias for factory registration
OllamaProvider = OllamaClient
