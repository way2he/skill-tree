# -*- coding: utf-8 -*-
"""
异步 Anthropic Claude API 客户端
"""

import json
import os
from typing import Any, Optional

import aiohttp

from .base import BaseAsyncLLMClient


class AsyncAnthropicClient(BaseAsyncLLMClient):
    """
    异步 Anthropic Claude API 客户端

    Args:
        api_key: Anthropic API 密钥
        model: 模型名称
        system_prompt: 系统提示词
        temperature: 温度参数
        timeout: 请求超时时间（秒）
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-20250514",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("API Key 未设置")
        self.model = model
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """生成文本回复"""
        headers = {
            "x-api-key": self.api_key or "",
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        payload: dict[str, Any] = {
            "model": self.model,
            "max_tokens": kwargs.get("max_tokens", 4096),
            "temperature": kwargs.get("temperature", self.temperature),
            "system": self.system_prompt or "",
            "messages": [{"role": "user", "content": prompt}],
        }

        timeout = aiohttp.ClientTimeout(total=kwargs.get("timeout", self.timeout))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                self.base_url, headers=headers, json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                return str(result["content"][0]["text"])

    async def generate_json(
        self, prompt: str, schema: Optional[dict[str, Any]] = None, **kwargs: Any
    ) -> str:
        """生成 JSON 格式回复"""
        headers = {
            "x-api-key": self.api_key or "",
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        json_instruction = ""
        if schema:
            schema_str = json.dumps(schema, ensure_ascii=False)
            json_instruction = f"\n\n你是一个严格的 JSON 生成器。必须返回有效的 JSON，格式如下：{schema_str}。只输出 JSON，不要有任何解释。"
        else:
            json_instruction = "\n\n请以有效的 JSON 格式输出响应。"

        payload: dict[str, Any] = {
            "model": self.model,
            "max_tokens": kwargs.get("max_tokens", 4096),
            "temperature": 0.3,
            "system": (self.system_prompt or "") + json_instruction,
            "messages": [{"role": "user", "content": prompt}],
        }

        timeout = aiohttp.ClientTimeout(total=kwargs.get("timeout", self.timeout))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                self.base_url, headers=headers, json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                return str(result["content"][0]["text"])

    async def generate_stream(self, prompt: str, **kwargs: Any):
        """流式生成（Anthropic SSE，异步）"""
        import json as _json
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
        payload: dict[str, Any] = {
            "model": self.model,
            "max_tokens": kwargs.get("max_tokens", 4096),
            "temperature": kwargs.get("temperature", self.temperature),
            "system": self.system_prompt or "",
            "messages": [{"role": "user", "content": prompt}],
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
                    try:
                        obj = _json.loads(data)
                    except _json.JSONDecodeError:
                        continue
                    if obj.get("type") == "content_block_delta":
                        piece = obj.get("delta", {}).get("text") or ""
                        if piece:
                            yield piece
                    elif obj.get("type") == "message_stop":
                        break
