# -*- coding: utf-8 -*-
"""
llm.anthropic.providers.deepseek - DeepSeek Anthropic API 兼容 Provider 实现

DeepSeek 支持使用 Anthropic API 格式调用，通过修改 base_url 即可使用。
参考文档: https://api-docs.deepseek.com/zh-cn/guides/anthropic_api

继承 AnthropicSDKBaseClient，使用 anthropic 官方 SDK 作为底层客户端，
只需配置 DeepSeek 的 API 基础 URL。

使用方式：
    from llm.anthropic.providers import DeepSeekSDKClient

    client = DeepSeekSDKClient(api_key="sk-...")
    result = client.generate("你好")

环境变量：
    DEEPSEEK_API_KEY: DeepSeek API 密钥

默认模型：
    deepseek-chat
"""

import os
from typing import Any

import anthropic

from .base import AnthropicSDKBaseClient


class DeepSeekSDKClient(AnthropicSDKBaseClient):
    """
    DeepSeek Anthropic API 兼容 Provider 客户端

    基于 anthropic 官方 Python SDK，利用 DeepSeek 提供的 Anthropic API 兼容接口。
    继承 AnthropicSDKBaseClient 基类，提供 generate()、generate_json()、generate_stream() 三种调用方式。

    DeepSeek Anthropic API 特性：
    - 使用 Anthropic API 格式
    - 需要配置 DeepSeek 的 base_url
    - max_tokens 为必填参数（默认 4096）
    - system 为顶层参数，不在 messages 中
    """

    # DeepSeek Anthropic API 默认基础 URL
    DEFAULT_BASE_URL: str = "https://api.deepseek.com/v1"

    # DeepSeek 默认模型
    DEFAULT_MODEL: str = "deepseek-chat"

    def __init__(
        self,
        api_key: str | None = None,
        model: str = DEFAULT_MODEL,
        max_tokens: int = 4096,
        base_url: str | None = None,
        timeout: float | None = None,
        **kwargs,
    ) -> None:
        """
        初始化 DeepSeek Anthropic API 兼容客户端。

        Args:
            api_key: DeepSeek API 密钥。若为 None，从环境变量 DEEPSEEK_API_KEY 读取。
            model: 默认使用的模型名称。
            max_tokens: 默认最大生成 token 数（Anthropic 必填参数）。
            base_url: 自定义 API 基础 URL。默认为 DeepSeek Anthropic API 地址。
            timeout: 请求超时时间（秒）。
            **kwargs: 传递给 anthropic.Anthropic 的额外参数。
        """
        # 保存参数供 _create_client 使用
        self._api_key = api_key
        self._base_url = base_url or self.DEFAULT_BASE_URL
        self._timeout = timeout
        self._extra_kwargs = kwargs

        # 调用父类初始化（会触发 _create_client）
        super().__init__(model=model, max_tokens=max_tokens)

    def _create_client(self, **kwargs) -> anthropic.Anthropic:
        """
        创建 DeepSeek Anthropic API 兼容客户端实例。

        Args:
            **kwargs: 未使用的参数（由父类传入）。

        Returns:
            anthropic.Anthropic: Anthropic SDK 客户端实例（配置为 DeepSeek API）。

        Raises:
            ValueError: 当未提供 API 密钥时抛出。
        """
        # 获取 API 密钥
        resolved_key = self._api_key or os.environ.get("DEEPSEEK_API_KEY", "")
        if not resolved_key:
            raise ValueError(
                "未提供 API 密钥。请通过 api_key 参数传入，"
                "或设置环境变量 DEEPSEEK_API_KEY。"
            )

        # 构建 Anthropic 客户端参数（使用 DeepSeek 的 base_url）
        client_params: dict[str, Any] = {
            "api_key": resolved_key,
            "base_url": self._base_url,
        }

        if self._timeout is not None:
            client_params["timeout"] = self._timeout

        # 合并额外参数
        client_params.update(self._extra_kwargs)

        return anthropic.Anthropic(**client_params)