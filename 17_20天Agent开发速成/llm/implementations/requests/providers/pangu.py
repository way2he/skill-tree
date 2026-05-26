# -*- coding: utf-8 -*-
"""
华为盘古客户端

同步和异步支持的华为盘古大模型 API 客户端。
API 文档: https://support.huaweicloud.com/productdesc-pangu/
"""

import json
import os
from typing import Any, AsyncIterator

import httpx
import requests

from .base import BaseProviderClient


class PanguProvider(BaseProviderClient):
    """
    华为盘古 Pangu Provider

    使用示例（同步）:
        client = PanguProvider(api_key="your-api-key", model="pangu-Σ")
        response = client.generate("你好，请介绍一下自己")

    使用示例（异步）:
        client = PanguProvider(api_key="your-api-key", model="pangu-Σ")
        response = await client.agenerate("你好，请介绍一下自己")

    Args:
        api_key: 华为云 API 密钥，可通过环境变量 HUAWEI_API_KEY 设置
        model: 模型名称，如 "pangu-Σ", "pangu-ui"
        region: 区域标识，默认 "cn-north-4"
        system_prompt: 系统提示词，用于设置模型行为
        temperature: 温度参数，控制输出随机性 (0-1，默认0.7)
        timeout: 请求超时时间（秒），默认60秒
    """

    # 类属性：厂商名称和默认模型
    PROVIDER_NAME: str = "pangu"
    DEFAULT_MODEL: str = "pangu-Σ"

    # 支持的区域列表
    REGIONS = {
        "cn-north-4": "my-huaweicloud.com",
        "cn-east-3": "myhuaweicloud.com",
        "cn-south-1": "myhuaweicloud.com",
    }

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "pangu-Σ",
        region: str = "cn-north-4",
        system_prompt: str | None = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        """
        初始化华为盘古客户端

        Args:
            api_key: 华为云 API 密钥
            model: 模型名称
            region: 区域标识
            system_prompt: 系统提示词
            temperature: 温度参数
            timeout: 超时时间（秒）
        """
        self.api_key = api_key or os.getenv("HUAWEI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key 未设置，请设置 HUAWEI_API_KEY 环境变量")

        self.model = model
        self.region = region
        self.domain = self.REGIONS.get(region, "my-huaweicloud.com")
        self.base_url = f"https://pangu.{self.domain}/v1/chat"
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
        生成文本回复（同步）

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
            self.base_url,
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
        生成 JSON 格式回复（同步）

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
            self.base_url,
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        return str(response.json()["choices"][0]["message"]["content"])

    def generate_stream(self, prompt: str, **kwargs: Any):
        """
        流式生成（同步，OpenAI 兼容 SSE）

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Yields:
            逐个返回的文本片段
        """
        headers: dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": self._build_messages(prompt),
            "temperature": kwargs.get("temperature", self.temperature),
            "stream": True,
        }
        with requests.post(
            self.base_url,
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
            stream=True,
        ) as resp:
            resp.raise_for_status()
            for raw in resp.iter_lines(decode_unicode=True):
                if not raw or not raw.startswith("data:"):
                    continue
                data = raw[5:].strip()
                if data == "[DONE]":
                    break
                try:
                    obj = json.loads(data)
                    delta = obj["choices"][0].get("delta", {})
                    piece = delta.get("content") or ""
                    if piece:
                        yield piece
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue

    async def agenerate(self, prompt: str, **kwargs: Any) -> str:
        """
        异步生成文本回复

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

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=kwargs.get("timeout", self.timeout),
            )
            response.raise_for_status()
            return str(response.json()["choices"][0]["message"]["content"])

    async def agenerate_stream(self, prompt: str, **kwargs: Any) -> AsyncIterator[str]:
        """
        异步流式生成

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Yields:
            逐个返回的文本片段
        """
        headers: dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": self._build_messages(prompt),
            "temperature": kwargs.get("temperature", self.temperature),
            "stream": True,
        }

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                self.base_url,
                headers=headers,
                json=payload,
                timeout=kwargs.get("timeout", self.timeout),
            ) as resp:
                resp.raise_for_status()
                async for raw in resp.aiter_lines():
                    if not raw or not raw.startswith("data:"):
                        continue
                    data = raw[5:].strip()
                    if data == "[DONE]":
                        break
                    try:
                        obj = json.loads(data)
                        delta = obj["choices"][0].get("delta", {})
                        piece = delta.get("content") or ""
                        if piece:
                            yield piece
                    except (json.JSONDecodeError, KeyError, IndexError):
                        continue


# 向后兼容别名
PanguClient = PanguProvider
