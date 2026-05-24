# -*- coding: utf-8 -*-
"""
异步 Ollama 本地模型客户端
"""

import os
from typing import Any, Optional

import aiohttp

from .base import BaseAsyncLLMClient


class AsyncOllamaClient(BaseAsyncLLMClient):
    """
    异步 Ollama 本地模型客户端

    Args:
        model: 模型名称
        base_url: Ollama 服务地址
        system_prompt: 系统提示词
        temperature: 温度参数
        timeout: 请求超时时间（秒）
    """

    def __init__(
        self,
        model: str = "qwen3.5:9b",
        base_url: str = "http://localhost:11434",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        timeout: int = 120,
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """生成文本回复"""
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "system": self.system_prompt,
            "temperature": kwargs.get("temperature", self.temperature),
            "stream": False,
        }

        timeout = aiohttp.ClientTimeout(total=kwargs.get("timeout", self.timeout))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                f"{self.base_url}/api/generate", json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                return str(result.get("response", ""))

    async def generate_json(
        self, prompt: str, schema: Optional[dict[str, Any]] = None, **kwargs: Any
    ) -> str:
        """生成 JSON 格式回复"""
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "system": self.system_prompt,
            "temperature": 0.3,
            "format": "json",
            "stream": False,
        }

        timeout = aiohttp.ClientTimeout(total=kwargs.get("timeout", self.timeout))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                f"{self.base_url}/api/generate", json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                response_str = str(result.get("response", ""))
                if not response_str.strip() and "thinking" in result:
                    response_str = str(result.get("thinking", ""))
                if not response_str.strip():
                    raise ValueError("Ollama 返回的响应为空")
                return response_str

    async def generate_stream(self, prompt: str, **kwargs: Any):
        """流式生成（Ollama NDJSON，异步）"""
        import json as _json
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "system": self.system_prompt,
            "temperature": kwargs.get("temperature", self.temperature),
            "stream": True,
        }
        timeout = aiohttp.ClientTimeout(total=kwargs.get("timeout", self.timeout))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                f"{self.base_url}/api/generate", json=payload
            ) as response:
                response.raise_for_status()
                async for raw in response.content:
                    line = raw.decode("utf-8", errors="ignore").strip()
                    if not line:
                        continue
                    try:
                        obj = _json.loads(line)
                    except _json.JSONDecodeError:
                        continue
                    piece = obj.get("response") or ""
                    if piece:
                        yield piece
                    if obj.get("done"):
                        break
