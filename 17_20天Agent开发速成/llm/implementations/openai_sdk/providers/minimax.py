# -*- coding: utf-8 -*-
"""
MiniMax OpenAI SDK 客户端
"""

import os
from typing import Any, Optional

from .base import OpenAICompatibleClient


class MiniMaxClient(OpenAICompatibleClient):
    """
    MiniMax 客户端

    使用 MiniMax 官方 API，支持 abab6.5s-chat、abab6.5-chat 等模型。
    通过设置 MINIMAX_API_KEY 环境变量或传入 api_key 参数进行认证。

    Attributes:
        PROVIDER_NAME: 提供者名称
        DEFAULT_BASE_URL: 默认 API 基础地址
        DEFAULT_MODEL: 默认使用的模型名称
        ENV_API_KEY: 环境变量中 API Key 的名称
    """

    PROVIDER_NAME: str = "minimax"
    DEFAULT_BASE_URL: str = "https://api.minimax.chat/v1"
    DEFAULT_MODEL: str = "abab6.5s-chat"
    ENV_API_KEY: str = "MINIMAX_API_KEY"

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
        初始化 MiniMax 客户端

        Args:
            api_key: API 密钥，若为 None 则从环境变量 MINIMAX_API_KEY 获取
            model: 模型名称，默认为 abab6.5s-chat
            base_url: API 基础地址，默认为 https://api.minimax.chat/v1
            system_prompt: 系统提示词
            temperature: 温度参数，控制生成随机性 (0-2)
            max_tokens: 最大输出 token 数

        Raises:
            ValueError: 当 API Key 未设置时抛出
            TypeError: 当参数类型不正确时抛出
        """
        if temperature is not None and not isinstance(temperature, (int, float)):
            raise TypeError(f"temperature 必须为数值类型，当前类型为 {type(temperature).__name__}")

        # 优先使用传入的 api_key，否则从环境变量获取
        api_key = api_key or os.getenv(self.ENV_API_KEY)
        if not api_key:
            raise ValueError(f"API Key 未设置，请设置 {self.ENV_API_KEY} 环境变量")

        super().__init__(
            api_key=api_key,
            model=model or self.DEFAULT_MODEL,
            base_url=base_url or self.DEFAULT_BASE_URL,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )


# Provider alias for factory registration
MiniMaxProvider = MiniMaxClient
