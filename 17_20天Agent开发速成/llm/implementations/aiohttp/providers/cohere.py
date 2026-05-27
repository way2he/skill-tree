# -*- coding: utf-8 -*-
"""
异步 Cohere API 客户端
"""

import json
import os
from typing import Any, Dict, List, Optional

import aiohttp

from .base import BaseAsyncProviderClient


class CohereProvider(BaseAsyncProviderClient):
    """
    异步 Cohere API 客户端

    Args:
        api_key: Cohere API 密钥
        model: 模型名称
        base_url: API 基础地址
        system_prompt: 系统提示词
        temperature: 温度参数
        timeout: 请求超时时间（秒）
    """

    PROVIDER_NAME = "cohere"
    DEFAULT_MODEL = "command-r-plus-08-2024"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        base_url: str = "https://api.cohere.com/v1",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("API Key 未设置")
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout

    def _build_messages(self, prompt: str) -> List[Dict[str, str]]:
        """构建消息列表"""
        messages: List[Dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})
        return messages

    async def agenerate(self, prompt: str, **kwargs: Any) -> str:
        """生成文本回复"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = self._build_messages(prompt)

        payload: Dict[str, Any] = {
            "model": kwargs.get("model", self.model),
            "messages": messages,
            "temperature": kwargs.get("temperature", self.temperature),
        }

        timeout = aiohttp.ClientTimeout(total=kwargs.get("timeout", self.timeout))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                f"{self.base_url}/chat", headers=headers, json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                return str(result["text"])

    async def agenerate_json(
        self, prompt: str, schema: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> str:
        """生成 JSON 格式回复"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages: List[Dict[str, str]] = []
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

        payload: Dict[str, Any] = {
            "model": kwargs.get("model", self.model),
            "messages": messages,
            "temperature": 0.3,
        }

        timeout = aiohttp.ClientTimeout(total=kwargs.get("timeout", self.timeout))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                f"{self.base_url}/chat", headers=headers, json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                return str(result["text"])

    async def agenerate_stream(self, prompt: str, **kwargs: Any):
        """流式生成（Cohere v1/chat NDJSON，异步）"""
        import json as _json
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Cohere-Version": "2024-05-22",
            "Accept": "application/json",
        }
        payload: dict[str, Any] = {
            "model": kwargs.get("model", self.model),
            "message": prompt,
            "temperature": kwargs.get("temperature", self.temperature),
            "preamble": self.system_prompt,
            "stream": True,
        }
        timeout = aiohttp.ClientTimeout(total=kwargs.get("timeout", self.timeout))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                f"{self.base_url}/chat", headers=headers, json=payload
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
                    if obj.get("event_type") == "text-generation":
                        piece = obj.get("text") or ""
                        if piece:
                            yield piece
                    elif obj.get("event_type") == "stream-end":
                        break


# 向后兼容别名
class AsyncCohereClient(CohereProvider):
    pass
