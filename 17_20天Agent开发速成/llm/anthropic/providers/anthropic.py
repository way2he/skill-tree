# -*- coding: utf-8 -*-
"""
llm.anthropic.providers.anthropic - Anthropic SDK Provider 实现

继承 AnthropicSDKBaseClient，使用 anthropic 官方 SDK 作为底层客户端。

使用方式：
    from llm.anthropic.providers import AnthropicSDKClient

    client = AnthropicSDKClient(api_key="sk-ant-...")
    result = client.generate("你好")

环境变量：
    ANTHROPIC_API_KEY: Anthropic API 密钥

默认模型：
    claude-sonnet-4-20250514
"""

import os
from typing import Any

import anthropic

from .base import AnthropicSDKBaseClient


class AnthropicSDKClient(AnthropicSDKBaseClient):
    """
    Anthropic SDK Provider 客户端

    基于 anthropic 官方 Python SDK，继承 AnthropicSDKBaseClient 基类。
    提供 generate()、generate_json()、generate_stream() 三种调用方式。

    特性：
    - max_tokens 为必填参数（默认 4096）
    - system 为顶层参数，不在 messages 中
    - 输出为 content 数组，通过 message.content[0].text 获取文本
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 4096,
        base_url: str | None = None,
        timeout: float | None = None,
        **kwargs,
    ) -> None:
        """
        初始化 Anthropic SDK Provider 客户端。

        Args:
            api_key: Anthropic API 密钥。若为 None，从环境变量 ANTHROPIC_API_KEY 读取。
            model: 默认使用的模型名称。
            max_tokens: 默认最大生成 token 数（Anthropic 必填参数）。
            base_url: 自定义 API 基础 URL（用于代理或私有部署）。
            timeout: 请求超时时间（秒）。
            **kwargs: 传递给 anthropic.Anthropic 的额外参数。
        """
        # 保存 API 密钥供 _create_client 使用
        self._api_key = api_key
        self._base_url = base_url
        self._timeout = timeout
        self._extra_kwargs = kwargs

        # 调用父类初始化（会触发 _create_client）
        super().__init__(model=model, max_tokens=max_tokens)

    def _create_client(self, **kwargs) -> anthropic.Anthropic:
        """
        创建 Anthropic SDK 客户端实例。

        Args:
            **kwargs: 未使用的参数（由父类传入）。

        Returns:
            anthropic.Anthropic: Anthropic SDK 客户端实例。

        Raises:
            ValueError: 当未提供 API 密钥时抛出。
        """
        # 获取 API 密钥
        resolved_key = self._api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        if not resolved_key:
            raise ValueError(
                "未提供 API 密钥。请通过 api_key 参数传入，"
                "或设置环境变量 ANTHROPIC_API_KEY。"
            )

        # 构建 Anthropic 客户端参数
        client_params: dict[str, Any] = {"api_key": resolved_key}

        if self._base_url is not None:
            client_params["base_url"] = self._base_url
        if self._timeout is not None:
            client_params["timeout"] = self._timeout

        # 合并额外参数
        client_params.update(self._extra_kwargs)

        return anthropic.Anthropic(**client_params)
