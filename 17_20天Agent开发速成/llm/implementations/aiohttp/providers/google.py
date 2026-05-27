# -*- coding: utf-8 -*-
"""
异步 Google Gemini 客户端
"""

import json
import os
from typing import Any, List, Optional

import aiohttp

from .base import BaseAsyncProviderClient


class GoogleProvider(BaseAsyncProviderClient):
    """
    异步 Google Gemini 客户端

    Args:
        api_key: Google API 密钥
        model: 模型名称
        system_prompt: 系统提示词
        temperature: 温度参数
        timeout: 请求超时时间（秒）
    """

    PROVIDER_NAME = "google"
    DEFAULT_MODEL = "gemini-1.5-pro"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("API Key 未设置")
        self.model = model
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout

    async def agenerate(self, prompt: str, **kwargs: Any) -> str:
        """生成文本回复"""
        url = f"{self.base_url}?key={self.api_key}"
        headers = {"Content-Type": "application/json"}

        contents = [{"role": "user", "parts": [{"text": prompt}]}]
        if self.system_prompt:
            contents.insert(0, {"role": "model", "parts": [{"text": self.system_prompt}]})

        payload = {
            "contents": contents,
            "generationConfig": {"temperature": kwargs.get("temperature", self.temperature)},
        }

        timeout = aiohttp.ClientTimeout(total=kwargs.get("timeout", self.timeout))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, headers=headers, json=payload) as response:
                response.raise_for_status()
                result = await response.json()
                return str(result["candidates"][0]["content"]["parts"][0]["text"])

    async def agenerate_json(
        self, prompt: str, schema: Optional[dict[str, Any]] = None, **kwargs: Any
    ) -> str:
        """生成 JSON 格式回复"""
        url = f"{self.base_url}?key={self.api_key}"
        headers = {"Content-Type": "application/json"}

        if schema:
            prompt = f"{prompt}\n\n你是一个严格的 JSON 生成器。请按以下 Schema 返回 JSON：{json.dumps(schema, ensure_ascii=False)}。只输出 JSON。"

        contents = [{"role": "user", "parts": [{"text": prompt}]}]
        if self.system_prompt:
            contents.insert(0, {"role": "model", "parts": [{"text": self.system_prompt}]})

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.3,
                "responseMimeType": "application/json",
            },
        }

        timeout = aiohttp.ClientTimeout(total=kwargs.get("timeout", self.timeout))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, headers=headers, json=payload) as response:
                response.raise_for_status()
                result = await response.json()
                return str(result["candidates"][0]["content"]["parts"][0]["text"])

    async def agenerate_stream(self, prompt: str, **kwargs: Any):
        """流式生成（Gemini :streamGenerateContent + SSE，异步）"""
        import json as _json
        stream_url = self.base_url.replace(":generateContent", ":streamGenerateContent")
        url = f"{stream_url}?alt=sse&key={self.api_key}"
        headers = {
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
        timeout = aiohttp.ClientTimeout(total=kwargs.get("timeout", self.timeout))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, headers=headers, json=payload) as response:
                response.raise_for_status()
                async for raw in response.content:
                    line = raw.decode("utf-8", errors="ignore").strip()
                    if not line or not line.startswith("data:"):
                        continue
                    data = line[5:].strip()
                    if not data:
                        continue
                    try:
                        obj = _json.loads(data)
                        cands = obj.get("candidates") or []
                        if not cands:
                            continue
                        parts = (cands[0].get("content") or {}).get("parts") or []
                        for part in parts:
                            piece = part.get("text") or ""
                            if piece:
                                yield piece
                    except (_json.JSONDecodeError, KeyError, IndexError):
                        continue


# 向后兼容别名
class AsyncGoogleClient(GoogleProvider):
    pass
