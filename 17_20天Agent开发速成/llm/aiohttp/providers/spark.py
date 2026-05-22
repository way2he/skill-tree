# -*- coding: utf-8 -*-
"""
异步科大讯飞星火客户端
"""

import json
import os
from typing import Any, List, Optional

import aiohttp

from .base import BaseAsyncLLMClient


class AsyncSparkClient(BaseAsyncLLMClient):
    """
    异步科大讯飞星火客户端

    Args:
        api_key: 讯飞 API Key
        api_secret: 讯飞 API Secret
        model: 模型名称
        system_prompt: 系统提示词
        temperature: 温度参数
        timeout: 请求超时时间（秒）
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        model: str = "spark-4.0-ultra",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("XUNFEI_API_KEY")
        self.api_secret = api_secret or os.getenv("XUNFEI_API_SECRET")
        if not self.api_key or not self.api_secret:
            raise ValueError("API Key 和 API Secret 未设置")
        self.model = model
        self.base_url = "https://spark-api.xf-yun.com/v1"
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """生成文本回复"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages: List[dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", self.temperature),
        }

        timeout = aiohttp.ClientTimeout(total=kwargs.get("timeout", self.timeout))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                f"{self.base_url}/chat/completions", headers=headers, json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                return str(result["choices"][0]["message"]["content"])

    async def generate_json(
        self, prompt: str, schema: Optional[dict[str, Any]] = None, **kwargs: Any
    ) -> str:
        """生成 JSON 格式回复"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages: List[dict[str, str]] = []
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

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.3,
            "response_format": {"type": "json_object"},
        }

        timeout = aiohttp.ClientTimeout(total=kwargs.get("timeout", self.timeout))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                f"{self.base_url}/chat/completions", headers=headers, json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                return str(result["choices"][0]["message"]["content"])
