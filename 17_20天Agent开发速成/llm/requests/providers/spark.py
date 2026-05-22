# -*- coding: utf-8 -*-
"""
同步科大讯飞星火客户端
"""

import json
import os
from typing import Any

import requests

from .base import BaseLLMClient


class SparkClient(BaseLLMClient):
    """
    同步科大讯飞星火客户端
    API 文档: https://www.xfyun.cn/doc/spark/Web.html

    使用示例:
        client = SparkClient(api_key="your-api-key", api_secret="your-api-secret", model="spark-4.0-ultra")
        response = client.generate("你好，请介绍一下自己")

    Args:
        api_key: 讯飞 API Key，可通过环境变量 XUNFEI_API_KEY 设置
        api_secret: 讯飞 API Secret，可通过环境变量 XUNFEI_API_SECRET 设置
        model: 模型名称，如 "spark-4.0-ultra", "spark-4.0-pro", "spark-4.0-max", "spark-4.0-lite"
        system_prompt: 系统提示词，用于设置模型行为
        temperature: 温度参数，控制输出随机性 (0-1，默认0.7)
        timeout: 请求超时时间（秒），默认60秒

    Note:
        科大讯飞使用 API Key + API Secret 的签名认证方式
    """

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        model: str = "spark-4.0-ultra",
        system_prompt: str | None = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("XUNFEI_API_KEY")
        self.api_secret = api_secret or os.getenv("XUNFEI_API_SECRET")
        if not self.api_key or not self.api_secret:
            raise ValueError("API Key 和 API Secret 未设置，请设置 XUNFEI_API_KEY 和 XUNFEI_API_SECRET 环境变量")
        self.model = model
        self.base_url = "https://spark-api.xf-yun.com/v1"
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout

    def _build_messages(self, prompt: str) -> list[dict[str, str]]:
        """
        构建消息列表

        Args:
            prompt: 用户提示词

        Returns:
            消息列表
        """
        messages: list[dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})
        return messages

    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        生成文本回复

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数
                - temperature: 温度参数
                - max_tokens: 最大生成 token 数
                - timeout: 请求超时时间（秒）

        Returns:
            模型生成的文本响应字符串
        """
        headers: dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": self._build_messages(prompt),
            "temperature": kwargs.get("temperature", self.temperature),
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        return str(response.json()["choices"][0]["message"]["content"])

    def generate_json(
        self, prompt: str, schema: dict[str, Any] | None = None, **kwargs: Any
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
        headers: dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = self._build_messages(prompt)
        if schema:
            schema_str = json.dumps(schema, ensure_ascii=False)
            messages.append(
                {
                    "role": "system",
                    "content": f"你是一个严格的 JSON 生成器。必须返回有效的 JSON，格式如下：{schema_str}。只输出 JSON，不要有任何解释。",
                }
            )

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.3,
            "response_format": {"type": "json_object"},
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        return str(response.json()["choices"][0]["message"]["content"])
