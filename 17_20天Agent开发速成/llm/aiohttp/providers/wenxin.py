# -*- coding: utf-8 -*-
"""
异步百度文心一言客户端
"""

import json
import os
from typing import Any, List, Optional

import aiohttp

from .base import BaseAsyncLLMClient


class AsyncWenxinClient(BaseAsyncLLMClient):
    """
    异步百度文心一言客户端

    Args:
        api_key: 百度 API 密钥（Access Token）
        model: 模型名称
        system_prompt: 系统提示词
        temperature: 温度参数
        timeout: 请求超时时间（秒）
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "ernie-4.0-turbo-128k",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("BAIDU_ACCESS_TOKEN")
        if not self.api_key:
            raise ValueError("Access Token 未设置")
        self.model = model
        self.base_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat"
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """生成文本回复"""
        headers = {"Content-Type": "application/json"}

        messages: List[dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload: dict[str, Any] = {
            "messages": messages,
            "temperature": kwargs.get("temperature", self.temperature),
        }

        timeout = aiohttp.ClientTimeout(total=kwargs.get("timeout", self.timeout))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                f"{self.base_url}/{self.model}?access_token={self.api_key}",
                headers=headers,
                json=payload,
            ) as response:
                response.raise_for_status()
                result = await response.json()
                if "error_code" in result:
                    raise Exception(f"文心一言 API 错误: {result}")
                return str(result.get("result", ""))

    async def generate_json(
        self, prompt: str, schema: Optional[dict[str, Any]] = None, **kwargs: Any
    ) -> str:
        """生成 JSON 格式回复"""
        headers = {"Content-Type": "application/json"}

        full_prompt = prompt
        if schema:
            schema_str = json.dumps(schema, ensure_ascii=False)
            full_prompt = f"{prompt}\n\n请严格按照以下 JSON Schema 返回结果，只输出 JSON，不要有任何解释：\n{schema_str}"

        messages: List[dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": full_prompt})

        payload: dict[str, Any] = {
            "messages": messages,
            "temperature": 0.3,
        }

        timeout = aiohttp.ClientTimeout(total=kwargs.get("timeout", self.timeout))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                f"{self.base_url}/{self.model}?access_token={self.api_key}",
                headers=headers,
                json=payload,
            ) as response:
                response.raise_for_status()
                result = await response.json()
                if "error_code" in result:
                    raise Exception(f"文心一言 API 错误: {result}")
                return str(result.get("result", ""))
