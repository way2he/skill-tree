# -*- coding: utf-8 -*-
"""
Anthropic Claude API 客户端

提供同步和异步方法调用 Claude 模型，支持流式输出。
API 文档: https://docs.anthropic.com/claude/reference/messages
"""

import json
import os
from typing import Any, AsyncIterator, Iterator

import httpx
import requests

from .base import BaseProviderClient


class AnthropicProvider(BaseProviderClient):
    """
    Anthropic Claude API 客户端

    提供同步和异步的文本生成方法，支持流式输出。

    使用示例:
        client = AnthropicProvider(
            api_key="sk-ant-xxx",
            model="claude-sonnet-4-20250514"
        )
        response = client.generate("你好，请介绍一下自己")

        # 异步调用
        import asyncio
        async def main():
            response = await client.agenerate("你好")

    Args:
        api_key: Anthropic API 密钥，可通过环境变量 ANTHROPIC_API_KEY 设置
        model: 模型名称，如 "claude-sonnet-4-20250514", "claude-3-5-sonnet"
        system_prompt: 系统提示词，用于设置模型行为
        temperature: 温度参数，控制输出随机性 (0-1，默认0.7)
        timeout: 请求超时时间（秒），默认60秒
    """

    # 类属性
    PROVIDER_NAME: str = "anthropic"
    DEFAULT_MODEL: str = "claude-sonnet-4-20250514"

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
        生成文本回复（同步）

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
            "model": kwargs.get("model", self.model),
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

    def generate_stream(self, prompt: str, **kwargs: Any) -> Iterator[str]:
        """
        流式生成（同步，Anthropic SSE）

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Yields:
            逐个返回的文本片段
        """
        headers: dict[str, str] = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
        payload: dict[str, Any] = {
            "model": kwargs.get("model", self.model),
            "max_tokens": kwargs.get("max_tokens", 4096),
            "temperature": kwargs.get("temperature", self.temperature),
            "system": self.system_prompt or "",
            "messages": [{"role": "user", "content": prompt}],
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
                try:
                    obj = json.loads(data)
                except json.JSONDecodeError:
                    continue
                if obj.get("type") == "content_block_delta":
                    piece = obj.get("delta", {}).get("text") or ""
                    if piece:
                        yield piece
                elif obj.get("type") == "message_stop":
                    break

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
            "model": kwargs.get("model", self.model),
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

        Raises:
            httpx.HTTPStatusError: HTTP 错误状态码
            httpx.RequestError: 请求错误
        """
        headers: dict[str, str] = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        payload: dict[str, Any] = {
            "model": kwargs.get("model", self.model),
            "max_tokens": kwargs.get("max_tokens", 4096),
            "temperature": kwargs.get("temperature", self.temperature),
            "system": self.system_prompt or "",
            "messages": [{"role": "user", "content": prompt}],
        }

        timeout = kwargs.get("timeout", self.timeout)

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                return str(response.json()["content"][0]["text"])
        except httpx.HTTPStatusError as e:
            raise ValueError(f"HTTP 错误: {e.response.status_code} - {e.response.text}") from e
        except httpx.RequestError as e:
            raise ValueError(f"请求错误: {str(e)}") from e

    async def agenerate_stream(self, prompt: str, **kwargs: Any) -> AsyncIterator[str]:
        """
        异步流式生成（Anthropic SSE）

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Yields:
            逐个返回的文本片段
        """
        headers: dict[str, str] = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
        payload: dict[str, Any] = {
            "model": kwargs.get("model", self.model),
            "max_tokens": kwargs.get("max_tokens", 4096),
            "temperature": kwargs.get("temperature", self.temperature),
            "system": self.system_prompt or "",
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
        }
        timeout = kwargs.get("timeout", self.timeout)

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                async with client.stream(
                    "POST",
                    self.base_url,
                    headers=headers,
                    json=payload,
                ) as resp:
                    resp.raise_for_status()
                    async for raw in resp.aiter_lines():
                        if not raw or not raw.startswith("data:"):
                            continue
                        data = raw[5:].strip()
                        try:
                            obj = json.loads(data)
                        except json.JSONDecodeError:
                            continue
                        if obj.get("type") == "content_block_delta":
                            piece = obj.get("delta", {}).get("text") or ""
                            if piece:
                                yield piece
                        elif obj.get("type") == "message_stop":
                            break
        except httpx.HTTPStatusError as e:
            raise ValueError(f"HTTP 错误: {e.response.status_code} - {e.response.text}") from e
        except httpx.RequestError as e:
            raise ValueError(f"请求错误: {str(e)}") from e

    async def agenerate_json(
        self,
        prompt: str,
        schema: dict[str, Any] | None = None,
        **kwargs: Any
    ) -> str:
        """
        异步生成 JSON 格式回复

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
            "model": kwargs.get("model", self.model),
            "max_tokens": kwargs.get("max_tokens", 4096),
            "temperature": 0.3,
            "system": (self.system_prompt or "") + json_instruction,
            "messages": [{"role": "user", "content": prompt}],
        }

        timeout = kwargs.get("timeout", self.timeout)

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                return str(response.json()["content"][0]["text"])
        except httpx.HTTPStatusError as e:
            raise ValueError(f"HTTP 错误: {e.response.status_code} - {e.response.text}") from e
        except httpx.RequestError as e:
            raise ValueError(f"请求错误: {str(e)}") from e


# 向后兼容别名
AnthropicClient = AnthropicProvider
