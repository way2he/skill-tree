# -*- coding: utf-8 -*-
"""
同步Anthropic Claude API客户端
"""

import json
import os
from typing import Any

import requests

from .base import BaseLLMClient


class AnthropicClient(BaseLLMClient):
    """
    同步 Anthropic Claude API 客户端
    API 文档: https://docs.anthropic.com/claude/reference/messages

    使用示例:
        client = AnthropicClient(
            api_key="sk-ant-xxx",
            model="claude-sonnet-4-20250514"
        )
        response = client.generate("你好，请介绍一下自己")

    Args:
        api_key: Anthropic API 密钥，可通过环境变量 ANTHROPIC_API_KEY 设置
        model: 模型名称，如 "claude-sonnet-4-20250514", "claude-3-5-sonnet"
        system_prompt: 系统提示词，用于设置模型行为
        temperature: 温度参数，控制输出随机性 (0-1，默认0.7)
        timeout: 请求超时时间（秒），默认60秒
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "claude-sonnet-4-20250514",
        system_prompt: str | None = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("API Key 未设置，请设置 ANTHROPIC_API_KEY 环境变量")
        self.model = model
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout

    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        生成文本回复

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数
                - temperature: 温度参数（Claude 范围 0-1）
                - max_tokens: 最大生成 token 数
                - timeout: 请求超时时间（秒）

        Returns:
            模型生成的文本响应字符串
        """
        headers: dict[str, str] = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        payload: dict[str, Any] = {
            "model": self.model,
            "max_tokens": kwargs.get("max_tokens", 4096),
            "temperature": kwargs.get("temperature", self.temperature),
            "system": self.system_prompt or "",
            "messages": [{"role": "user", "content": prompt}],
        }

        response = requests.post(
            self.base_url,
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        return str(response.json()["content"][0]["text"])

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
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        if schema:
            schema_str = json.dumps(schema, ensure_ascii=False)
            json_instruction = (
                f"\n\n你是一个严格的 JSON 生成器。必须返回有效的 JSON，"
                f"格式如下：{schema_str}。只输出 JSON，不要有任何解释。"
            )
        else:
            json_instruction = "\n\n请以有效的 JSON 格式输出响应。"

        payload: dict[str, Any] = {
            "model": self.model,
            "max_tokens": kwargs.get("max_tokens", 4096),
            "temperature": 0.3,
            "system": (self.system_prompt or "") + json_instruction,
            "messages": [{"role": "user", "content": prompt}],
        }

        response = requests.post(
            self.base_url,
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        return str(response.json()["content"][0]["text"])
