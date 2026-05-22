# -*- coding: utf-8 -*-
"""
同步字节跳动豆包(Doubao)客户端
"""

import json
import os
from typing import Any

import requests

from .base import BaseLLMClient


class DoubaoClient(BaseLLMClient):
    """
    同步火山引擎豆包大模型客户端
    API 文档: https://www.volcengine.com/docs/82379/1263482

    使用示例:
        client = DoubaoClient(
            api_key="your-api-key",
            model="doubao-pro-32k",
            region="cn-beijing"
        )
        response = client.generate("你好，请介绍一下自己")

    Args:
        api_key: 火山引擎 API 密钥，可通过环境变量 VOLCENGINE_API_KEY 设置
        model: 模型名称，如 "doubao-pro-32k", "doubao-seed-2-0-code-preview-260215"
        region: 区域标识，支持 cn-beijing, cn-guangzhou, cn-shanghai, cn-hangzhou
        system_prompt: 系统提示词，用于设置模型行为
        temperature: 温度参数，控制输出随机性 (0-2，默认0.7)
        timeout: 请求超时时间（秒），默认60秒
    """

    SUPPORTED_REGIONS = {
        "cn-beijing": "ark.cn-beijing.volces.com",
        "cn-guangzhou": "ark.cn-guangzhou.volces.com",
        "cn-shanghai": "ark.cn-shanghai.volces.com",
        "cn-hangzhou": "ark.cn-hangzhou.volces.com",
    }

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "doubao-seed-2-0-code-preview-260215",
        region: str = "cn-beijing",
        system_prompt: str | None = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("VOLCENGINE_API_KEY")
        if not self.api_key:
            raise ValueError("API Key 未设置，请设置 VOLCENGINE_API_KEY 环境变量")
        self.model = model
        self.region = region
        self.base_url = f"https://{self.SUPPORTED_REGIONS.get(region, region)}/api/v3"
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

        messages: list[dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})

        if schema:
            schema_str = json.dumps(schema, ensure_ascii=False)
            messages.append(
                {
                    "role": "system",
                    "content": f"你是一个严格的 JSON 生成器。必须返回有效的 JSON，格式如下：{schema_str}。只输出 JSON，不要有任何解释。",
                }
            )

        messages.append({"role": "user", "content": prompt})

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
