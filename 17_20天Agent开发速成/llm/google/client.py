# -*- coding: utf-8 -*-
"""
Google Gemini 官方 SDK 客户端基类

基于 google-generativeai SDK，提供 Gemini 大模型服务的统一封装。

依赖安装：
    pip install google-generativeai

文档参考：
    https://ai.google.dev/gemini-api/docs
"""

import os
from abc import ABC, abstractmethod
from typing import Any, Optional


class GoogleClient(ABC):
    """
    Google 客户端抽象基类

    使用 Google 官方 SDK (google-generativeai) 进行调用。
    使用 API Key 鉴权方式。

    Args:
        api_key: API Key，可通过环境变量 GOOGLE_API_KEY 设置
        model: 模型名称，默认 "gemini-pro"
        system_prompt: 系统提示词
        temperature: 温度参数 (0-2)
        max_tokens: 最大输出 token 数
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-pro",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> None:
        """
        初始化 Google 客户端

        Args:
            api_key: API Key
            model: 模型名称
            system_prompt: 系统提示词
            temperature: 温度参数
            max_tokens: 最大输出 token 数
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")

        if not self.api_key:
            raise ValueError(
                "API Key 未设置，请设置 GOOGLE_API_KEY 环境变量"
            )

        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens

        # 初始化客户端
        self._init_client()

    @abstractmethod
    def _init_client(self) -> None:
        """
        初始化 google-generativeai 客户端（子类实现）
        """
        pass

    @abstractmethod
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        生成文本回复

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Returns:
            模型生成的文本响应字符串
        """
        pass

    @abstractmethod
    def generate_json(
        self, prompt: str, schema: Optional[dict[str, Any]] = None, **kwargs: Any
    ) -> str:
        """
        生成 JSON 格式回复

        Args:
            prompt: 用户输入的提示词文本
            schema: 可选的 JSON Schema 字典
            **kwargs: 可选参数

        Returns:
            符合指定 Schema 的 JSON 字符串
        """
        pass


# 别名，便于使用
GeminiClient = GoogleClient
