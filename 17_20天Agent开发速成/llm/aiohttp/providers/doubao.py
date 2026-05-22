# -*- coding: utf-8 -*-
"""
异步火山引擎豆包大模型客户端
"""

import json
import os
from typing import Any, List, Optional

import aiohttp

from .base import BaseAsyncLLMClient


class AsyncDoubaoClient(BaseAsyncLLMClient):
    """
    异步火山引擎豆包大模型客户端

    Args:
        api_key: 火山引擎 API 密钥
        model: 模型名称
        region: 区域标识
        system_prompt: 系统提示词
        temperature: 温度参数
        timeout: 请求超时时间（秒）
    """

    SUPPORTED_REGIONS = {
        "cn-beijing": "ark.cn-beijing.volces.com",
        "cn-guangzhou": "ark.cn-guangzhou.volces.com",
        "cn-shanghai": "ark.cn-shanghai.volces.com",
        "cn-hangzhou": "ark.cn-hangzhou.volces.com",
    }

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "doubao-seed-2-0-code-preview-260215",
        region: str = "cn-beijing",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("VOLCENGINE_API_KEY")
        if not self.api_key:
            raise ValueError("API Key 未设置")
        self.model = model
        self.region = region
        self.base_url = f"https://{self.SUPPORTED_REGIONS.get(region, region)}/api/v3"
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

        payload: dict[str, Any] = {
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

        payload: dict[str, Any] = {
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
