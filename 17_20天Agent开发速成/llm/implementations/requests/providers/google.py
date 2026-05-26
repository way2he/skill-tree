# -*- coding: utf-8 -*-
"""
同步/异步 Google Gemini 客户端
"""

import json
import os
from typing import Any, AsyncIterator

import httpx
import requests

from .base import BaseProviderClient


class GoogleProvider(BaseProviderClient):
    """
    同步/异步 Google Gemini 客户端
    API 文档: https://ai.google.dev/gemini-api/docs

    使用示例:
        client = GoogleProvider(api_key="your-api-key")
        response = client.generate("Hello, how are you?")

        # 异步用法
        async def main():
            response = await client.agenerate("Hello, how are you?")

    Args:
        api_key: Google API 密钥，可通过环境变量 GOOGLE_API_KEY 设置
        model: 模型名称，如 "gemini-pro", "gemini-pro-vision", "gemini-1.5-pro"
        system_prompt: 系统提示词，用于设置模型行为
        temperature: 温度参数，控制输出随机性 (0-1，默认0.7)
        timeout: 请求超时时间（秒），默认60秒

    Class Attributes:
        PROVIDER_NAME: 厂商名称标识
        DEFAULT_MODEL: 默认模型
    """

    # 类属性定义
    PROVIDER_NAME: str = "google"
    DEFAULT_MODEL: str = "gemini-1.5-pro"

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("API Key 未设置，请设置 GOOGLE_API_KEY 环境变量")

        # 使用传入的 model 或默认值
        self.model = model or self.DEFAULT_MODEL
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout

    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        同步生成文本回复

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数
                - temperature: 温度参数
                - max_tokens: 最大生成 token 数
                - timeout: 请求超时时间（秒）

        Returns:
            模型生成的文本响应字符串
        """
        url = f"{self.base_url}?key={self.api_key}"

        headers: dict[str, str] = {
            "Content-Type": "application/json",
        }

        contents = [{"role": "user", "parts": [{"text": prompt}]}]
        if self.system_prompt:
            contents.insert(0, {"role": "model", "parts": [{"text": self.system_prompt}]})

        payload: dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": kwargs.get("temperature", self.temperature),
            },
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        return str(response.json()["candidates"][0]["content"]["parts"][0]["text"])

    def generate_json(
        self, prompt: str, schema: dict[str, Any] | None = None, **kwargs: Any
    ) -> str:
        """
        同步生成 JSON 格式回复

        Args:
            prompt: 用户输入的提示词文本
            schema: 可选的 JSON Schema 字典
            **kwargs: 可选参数

        Returns:
            符合指定 Schema 的 JSON 字符串
        """
        url = f"{self.base_url}?key={self.api_key}"

        headers: dict[str, str] = {
            "Content-Type": "application/json",
        }

        if schema:
            prompt = f"{prompt}\n\n你是一个严格的 JSON 生成器。请按以下 Schema 返回 JSON：{json.dumps(schema, ensure_ascii=False)}。只输出 JSON。"

        contents = [{"role": "user", "parts": [{"text": prompt}]}]
        if self.system_prompt:
            contents.insert(0, {"role": "model", "parts": [{"text": self.system_prompt}]})

        payload: dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.3,
                "responseMimeType": "application/json",
            },
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        return str(response.json()["candidates"][0]["content"]["parts"][0]["text"])

    def generate_stream(self, prompt: str, **kwargs: Any):
        """
        同步流式生成（Gemini :streamGenerateContent + SSE）

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Yields:
            逐个返回的文本片段
        """
        stream_url = self.base_url.replace(":generateContent", ":streamGenerateContent")
        url = f"{stream_url}?alt=sse&key={self.api_key}"
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
        contents = [{"role": "user", "parts": [{"text": prompt}]}]
        if self.system_prompt:
            contents.insert(0, {"role": "model", "parts": [{"text": self.system_prompt}]})
        payload: dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": kwargs.get("temperature", self.temperature),
            },
        }
        with requests.post(
            url,
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
                if not data:
                    continue
                try:
                    obj = json.loads(data)
                    cands = obj.get("candidates") or []
                    if not cands:
                        continue
                    parts = (cands[0].get("content") or {}).get("parts") or []
                    for part in parts:
                        piece = part.get("text") or ""
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
        url = f"{self.base_url}?key={self.api_key}"

        headers: dict[str, str] = {
            "Content-Type": "application/json",
        }

        contents = [{"role": "user", "parts": [{"text": prompt}]}]
        if self.system_prompt:
            contents.insert(0, {"role": "model", "parts": [{"text": self.system_prompt}]})

        payload: dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": kwargs.get("temperature", self.temperature),
            },
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                json=payload,
                timeout=kwargs.get("timeout", self.timeout),
            )
            response.raise_for_status()
            return str(response.json()["candidates"][0]["content"]["parts"][0]["text"])

    async def agenerate_stream(self, prompt: str, **kwargs: Any) -> AsyncIterator[str]:
        """
        异步流式生成（Gemini :streamGenerateContent + SSE）

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Yields:
            逐个返回的文本片段
        """
        stream_url = self.base_url.replace(":generateContent", ":streamGenerateContent")
        url = f"{stream_url}?alt=sse&key={self.api_key}"
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
        contents = [{"role": "user", "parts": [{"text": prompt}]}]
        if self.system_prompt:
            contents.insert(0, {"role": "model", "parts": [{"text": self.system_prompt}]})
        payload: dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": kwargs.get("temperature", self.temperature),
            },
        }

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                url,
                headers=headers,
                json=payload,
                timeout=kwargs.get("timeout", self.timeout),
            ) as resp:
                resp.raise_for_status()
                async for raw in resp.aiter_lines():
                    if not raw or not raw.startswith("data:"):
                        continue
                    data = raw[5:].strip()
                    if not data:
                        continue
                    try:
                        obj = json.loads(data)
                        cands = obj.get("candidates") or []
                        if not cands:
                            continue
                        parts = (cands[0].get("content") or {}).get("parts") or []
                        for part in parts:
                            piece = part.get("text") or ""
                            if piece:
                                yield piece
                    except (json.JSONDecodeError, KeyError, IndexError):
                        continue


# 向后兼容别名
GoogleClient = GoogleProvider
