# -*- coding: utf-8 -*-
"""
科大讯飞星火 OpenAI SDK 客户端
通过 OpenAI 兼容协议调用科大讯飞星火的 Spark 系列模型
"""

import os
from typing import Any, Optional

from .base import OpenAICompatibleClient


class SparkClient(OpenAICompatibleClient):
    """
    科大讯飞星火客户端

    基于 OpenAI SDK 兼容协议，调用科大讯飞提供的星火 (Spark) 系列大语言模型。
    官方文档: https://www.xfyun.cn/doc/spark/

    Attributes:
        PROVIDER_NAME: 提供者名称
        DEFAULT_BASE_URL: 默认 API 基础地址
        DEFAULT_MODEL: 默认模型名称
        ENV_API_KEY: API Key 对应的环境变量名
    """

    PROVIDER_NAME: str = "spark"
    DEFAULT_BASE_URL: str = "https://spark-api.xf-yun.com/v1"
    DEFAULT_MODEL: str = "spark-4.0-ultra"
    ENV_API_KEY: str = "XUNFEI_API_KEY"

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
        初始化科大讯飞星火客户端

        Args:
            api_key: API 密钥，若为 None 则从环境变量 XUNFEI_API_KEY 读取
            model: 模型名称，默认使用 spark-4.0-ultra
            base_url: API 基础地址，默认使用 https://spark-api.xf-yun.com/v1
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


# Provider alias for factory registration
SparkProvider = SparkClient
