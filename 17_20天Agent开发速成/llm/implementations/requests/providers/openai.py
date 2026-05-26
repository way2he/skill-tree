# -*- coding: utf-8 -*-
"""
OpenAI API Provider（兼容 Azure OpenAI）

实现 BaseProviderClient 接口，支持同步/异步调用。
API 文档: https://platform.openai.com/docs/api-reference

使用示例:
    # 直接使用
    provider = OpenAIProvider(api_key="sk-xxx", model="gpt-4o-mini")
    result = provider.generate("Hello")

    # 通过 UnifiedAdapter 使用
    from llm.core.adapter import UnifiedAdapter
    adapter = UnifiedAdapter(provider)
    result = adapter.generate("Hello")

    # 异步使用
    result = await provider.agenerate("Hello")
"""

import json
import os
from typing import Any, Iterator, AsyncIterator

import requests

from .base import BaseProviderClient


class OpenAIProvider(BaseProviderClient):
    """
    OpenAI API Provider

    同步/异步 OpenAI API 客户端（兼容 Azure OpenAI）

    Args:
        api_key: OpenAI API 密钥，可通过环境变量 OPENAI_API_KEY 设置
        model: 模型名称，如 "gpt-4o-mini", "gpt-4"
        base_url: API 基础地址，默认 https://api.openai.com/v1
        system_prompt: 系统提示词，用于设置模型行为
        temperature: 温度参数，控制输出随机性 (0-2，默认0.7)
        timeout: 请求超时时间（秒），默认60秒
    """

    # 实现 IProviderClient 协议
    PROVIDER_NAME = "openai"
    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-4o-mini",
        base_url: str = "https://api.openai.com/v1",
        system_prompt: str | None = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key 未设置，请设置 OPENAI_API_KEY 环境变量")
        self.model = model
        self.base_url = base_url.rstrip("/")
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
        同步生成文本回复

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Returns:
            模型生成的文本响应字符串
        """
        headers: dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload: dict[str, Any] = {
            "model": kwargs.get("model", self.model),
            "messages": self._build_messages(prompt),
            "temperature": kwargs.get("temperature", self.temperature),
        }

        # 添加可选参数
        if "max_tokens" in kwargs:
            payload["max_tokens"] = kwargs["max_tokens"]

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        return str(response.json()["choices"][0]["message"]["content"])

    def generate_stream(self, prompt: str, **kwargs: Any) -> Iterator[str]:
        """
        同步流式生成（SSE）

        按 OpenAI Chat Completions SSE 协议逐 chunk 返回 delta.content。

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
            "model": kwargs.get("model", self.model),
            "messages": self._build_messages(prompt),
            "temperature": kwargs.get("temperature", self.temperature),
            "stream": True,
        }

        # 添加可选参数
        if "max_tokens" in kwargs:
            payload["max_tokens"] = kwargs["max_tokens"]

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

    def generate_json(
        self,
        prompt: str,
        schema: dict[str, Any] | None = None,
        **kwargs: Any
    ) -> str:
        """
        生成 JSON 格式回复

        使用 OpenAI 的 response_format 功能。

        Args:
            prompt: 用户输入的提示词文本
            schema: 可选的 JSON Schema 字典
            **kwargs: 可选参数

        Returns:
            JSON 字符串
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
            "model": kwargs.get("model", self.model),
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

    # =========================================================================
    # 异步方法
    # =========================================================================

    async def agenerate(self, prompt: str, **kwargs: Any) -> str:
        """
        异步生成文本回复

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Returns:
            模型生成的文本响应字符串
        """
        try:
            import httpx
        except ImportError:
            raise ImportError("异步调用需要安装 httpx: pip install httpx")

        headers: dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload: dict[str, Any] = {
            "model": kwargs.get("model", self.model),
            "messages": self._build_messages(prompt),
            "temperature": kwargs.get("temperature", self.temperature),
        }

        # 添加可选参数
        if "max_tokens" in kwargs:
            payload["max_tokens"] = kwargs["max_tokens"]

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
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
        try:
            import httpx
        except ImportError:
            raise ImportError("异步调用需要安装 httpx: pip install httpx")

        headers: dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

        payload: dict[str, Any] = {
            "model": kwargs.get("model", self.model),
            "messages": self._build_messages(prompt),
            "temperature": kwargs.get("temperature", self.temperature),
            "stream": True,
        }

        # 添加可选参数
        if "max_tokens" in kwargs:
            payload["max_tokens"] = kwargs["max_tokens"]

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            ) as response:
                response.raise_for_status()
                async for raw in response.aiter_lines():
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
# 向后兼容：保留旧类名
# =============================================================================

class OpenAIClient(OpenAIProvider):
    """
    向后兼容别名

    旧代码使用 OpenAIClient，新代码应使用 OpenAIProvider。
    """
    pass
