# -*- coding: utf-8 -*-
"""
昆仑万维天工 Provider 客户端

同步和异步接口实现，兼容 OpenAI Chat API 格式。
API 文档: https://www.tiangong.cn/
"""

import json
import os
from typing import Any, AsyncIterator

import httpx
import requests

from .base import BaseProviderClient


class TiangongProvider(BaseProviderClient):
    """
    昆仑万维天工 Provider 客户端

    使用示例（同步）:
        provider = TiangongProvider(api_key="your-api-key")
        response = provider.generate("你好")

    使用示例（异步）:
        provider = TiangongProvider(api_key="your-api-key")
        response = await provider.agenerate("你好")

    类属性:
        PROVIDER_NAME: 厂商名称
        DEFAULT_MODEL: 默认模型

    Args:
        api_key: 天工 API 密钥，可通过环境变量 TIANGONG_API_KEY 设置
        model: 模型名称，如 "Skywork-72B", "tiangong-k2"
        system_prompt: 系统提示词，用于设置模型行为
        temperature: 温度参数，控制输出随机性 (0-1，默认0.7)
        timeout: 请求超时时间（秒），默认60秒
    """

    # 类属性
    PROVIDER_NAME: str = "tiangong"
    DEFAULT_MODEL: str = "Skywork-72B"

    def __init__(
        self,
        api_key: str | None = None,
        model: str = DEFAULT_MODEL,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("TIANGONG_API_KEY")
        if not self.api_key:
            raise ValueError("API Key 未设置，请设置 TIANGONG_API_KEY 环境变量")

        self.model = model
        self.base_url = "https://api.tiangong.cn/v1"
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

    def _get_headers(self) -> dict[str, str]:
        """
        获取请求头

        Returns:
            请求头字典
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _get_payload(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        """
        构建请求 payload

        Args:
            prompt: 用户提示词
            **kwargs: 可选参数

        Returns:
            请求 payload 字典
        """
        return {
            "model": kwargs.get("model", self.model),
            "messages": self._build_messages(prompt),
            "temperature": kwargs.get("temperature", self.temperature),
        }

    # =========================================================================
    # 同步方法
    # =========================================================================

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
        headers = self._get_headers()
        payload = self._get_payload(prompt, **kwargs)

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
        生成 JSON 格式回复（同步）

        Args:
            prompt: 用户输入的提示词文本
            schema: 可选的 JSON Schema 字典
            **kwargs: 可选参数

        Returns:
            符合指定 Schema 的 JSON 字符串
        """
        headers = self._get_headers()

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

    def generate_stream(self, prompt: str, **kwargs: Any):
        """
        流式生成（同步，OpenAI 兼容 SSE）

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Yields:
            逐个返回的文本片段
        """
        headers = {
            **self._get_headers(),
            "Accept": "text/event-stream",
        }
        payload = {
            **self._get_payload(prompt, **kwargs),
            "stream": True,
        }

        with requests.post(
            f"{self.base_url}/chat/completions",
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

    # =========================================================================
    # 异步方法
    # =========================================================================

    async def agenerate(self, prompt: str, **kwargs: Any) -> str:
        """
        生成文本回复（异步）

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数
                - temperature: 温度参数
                - max_tokens: 最大生成 token 数
                - timeout: 请求超时时间（秒）

        Returns:
            模型生成的文本响应字符串
        """
        headers = self._get_headers()
        payload = self._get_payload(prompt, **kwargs)

        async with httpx.AsyncClient(timeout=kwargs.get("timeout", self.timeout)) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            return str(response.json()["choices"][0]["message"]["content"])

    async def agenerate_stream(self, prompt: str, **kwargs: Any) -> AsyncIterator[str]:
        """
        流式生成（异步，OpenAI 兼容 SSE）

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Yields:
            逐个返回的文本片段
        """
        headers = {
            **self._get_headers(),
            "Accept": "text/event-stream",
        }
        payload = {
            **self._get_payload(prompt, **kwargs),
            "stream": True,
        }

        async with httpx.AsyncClient(timeout=kwargs.get("timeout", self.timeout)) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
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


# =============================================================================
# 向后兼容别名
# =============================================================================

TiangongClient = TiangongProvider
