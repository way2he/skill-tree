# -*- coding: utf-8 -*-
"""
Meta Llama (via Together AI) OpenAI SDK 客户端
通过 Together AI 平台的 OpenAI 兼容协议调用 Meta Llama 系列模型
"""

import os
from typing import Any, Optional

from .base import OpenAICompatibleClient


class MetaClient(OpenAICompatibleClient):
    """
    Meta Llama (via Together AI) 客户端

    基于 OpenAI SDK 兼容协议，通过 Together AI 平台调用 Meta 提供的 Llama 系列大语言模型。
    Together AI 官方文档: https://docs.together.ai/
    Meta Llama 官方文档: https://llama.meta.com/

    Attributes:
        DEFAULT_BASE_URL: 默认 API 基础地址 (Together AI 端点)
        DEFAULT_MODEL: 默认模型名称
        ENV_API_KEY: API Key 对应的环境变量名 (Together AI)
    """

    DEFAULT_BASE_URL: str = "https://api.together.xyz/v1"
    DEFAULT_MODEL: str = "meta-llama/Llama-3-70b-chat-hf"
    ENV_API_KEY: str = "TOGETHER_API_KEY"

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
        初始化 Meta Llama (via Together AI) 客户端

        Args:
            api_key: Together AI API 密钥，若为 None 则从环境变量 TOGETHER_API_KEY 读取
            model: 模型名称，默认使用 meta-llama/Llama-3-70b-chat-hf
            base_url: API 基础地址，默认使用 https://api.together.xyz/v1
            system_prompt: 系统提示词
            temperature: 温度参数，控制生成随机性，范围 0-2
            max_tokens: 最大输出 token 数

        Raises:
            ValueError: 当 API Key 未设置时抛出
        """
        # 优先使用传入的 api_key，否则从环境变量获取
        api_key = api_key or os.getenv(self.ENV_API_KEY)
        if not api_key:
            raise ValueError(f"API Key 未设置，请设置 {self.ENV_API_KEY} 环境变量")

        # 调用父类初始化
        super().__init__(
            api_key=api_key,
            model=model or self.DEFAULT_MODEL,
            base_url=base_url or self.DEFAULT_BASE_URL,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )
