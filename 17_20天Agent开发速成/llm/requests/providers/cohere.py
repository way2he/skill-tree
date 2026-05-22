# -*- coding: utf-8 -*-
"""
同步Cohere客户端
"""

import json
import os
from typing import Any

import requests

from .base import BaseLLMClient


class CohereClient(BaseLLMClient):
    """
    同步 Cohere 客户端
    API 文档: https://docs.cohere.com/

    使用示例:
        client = CohereClient(api_key="your-api-key", model="command-r-plus")
        response = client.generate("Hello, how are you?")

    Args:
        api_key: Cohere API 密钥，可通过环境变量 COHERE_API_KEY 设置
        model: 模型名称，如 "command-r-plus", "command-r", "command"
        system_prompt: 系统提示词，用于设置模型行为
        temperature: 温度参数，控制输出随机性 (0-2，默认0.7)
        timeout: 请求超时时间（秒），默认60秒
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "command-r-plus",
        system_prompt: str | None = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("API Key 未设置，请设置 COHERE_API_KEY 环境变量")
        self.model = model
        self.base_url = "https://api.cohere.com/v1"
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout

    def _build_messages(self, prompt: str) -> list[dict[str, str]]:
        """
        构建消息列表（Cohere 格式）

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
            "Cohere-Version": "2024-05-22",
        }

        # 构建对话格式
        chat_history = []
        preamble = self.system_prompt

        payload: dict[str, Any] = {
            "model": self.model,
            "message": prompt,
            "temperature": kwargs.get("temperature", self.temperature),
            "preamble": preamble,
        }

        response = requests.post(
            f"{self.base_url}/chat",
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        return str(response.json()["text"])

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
            "Cohere-Version": "2024-05-22",
        }

        if schema:
            schema_str = json.dumps(schema, ensure_ascii=False)
            prompt = f"{prompt}\n\n你是一个严格的 JSON 生成器。必须返回有效的 JSON，格式如下：{schema_str}。只输出 JSON，不要有任何解释。"

        payload: dict[str, Any] = {
            "model": self.model,
            "message": prompt,
            "temperature": 0.3,
            "preamble": self.system_prompt,
            "response_format": {"type": "json_object"},
        }

        response = requests.post(
            f"{self.base_url}/chat",
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        return str(response.json()["text"])
