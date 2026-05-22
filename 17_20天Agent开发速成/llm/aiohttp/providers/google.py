# -*- coding: utf-8 -*-
"""
异步 Google Gemini 客户端
"""

import json
import os
from typing import Any, List, Optional

import aiohttp

from .base import BaseAsyncLLMClient


class AsyncGoogleClient(BaseAsyncLLMClient):
    """
    异步 Google Gemini 客户端

    Args:
        api_key: Google API 密钥
        model: 模型名称
        system_prompt: 系统提示词
        temperature: 温度参数
        timeout: 请求超时时间（秒）
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-1.5-pro",
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

    async def generate(self, prompt: str, **kwargs: Any) -> str:
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

    async def generate_json(
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
