# -*- coding: utf-8 -*-
"""
异步 MiniMax 客户端
"""

import json
import os
from typing import Any, List, Optional

import aiohttp

from .base import BaseAsyncLLMClient


class AsyncMiniMaxClient(BaseAsyncLLMClient):
    """
    异步 MiniMax 客户端

    Args:
        api_key: MiniMax API 密钥
        model: 模型名称
        system_prompt: 系统提示词
        temperature: 温度参数
        timeout: 请求超时时间（秒）
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "abab6.5s-chat",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("MINIMAX_API_KEY")
        if not self.api_key:
            raise ValueError("API Key 未设置")
        self.model = model
        self.base_url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
        self.group_id = os.getenv("MINIMAX_GROUP_ID")
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
        if self.group_id:
            payload["group_id"] = self.group_id

        timeout = aiohttp.ClientTimeout(total=kwargs.get("timeout", self.timeout))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                self.base_url, headers=headers, json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                if result.get("base_resp", {}).get("status_code") != 0:
                    raise Exception(f"MiniMax API 错误: {result}")
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
        }
        if self.group_id:
            payload["group_id"] = self.group_id

        timeout = aiohttp.ClientTimeout(total=kwargs.get("timeout", self.timeout))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                self.base_url, headers=headers, json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                if result.get("base_resp", {}).get("status_code") != 0:
                    raise Exception(f"MiniMax API 错误: {result}")
                return str(result["choices"][0]["message"]["content"])

    async def generate_stream(self, prompt: str, **kwargs: Any):
        """流式生成（OpenAI 兼容 SSE，异步）"""
        import json as _json
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": self._build_messages(prompt),
            "temperature": kwargs.get("temperature", self.temperature),
            "stream": True,
        }
        timeout = aiohttp.ClientTimeout(total=kwargs.get("timeout", self.timeout))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                self.base_url, headers=headers, json=payload
            ) as response:
                response.raise_for_status()
                async for raw in response.content:
                    line = raw.decode("utf-8", errors="ignore").strip()
                    if not line or not line.startswith("data:"):
                        continue
                    data = line[5:].strip()
                    if data == "[DONE]":
                        break
                    try:
                        obj = _json.loads(data)
                        delta = obj["choices"][0].get("delta", {})
                        piece = delta.get("content") or ""
                        if piece:
                            yield piece
                    except (_json.JSONDecodeError, KeyError, IndexError):
                        continue
