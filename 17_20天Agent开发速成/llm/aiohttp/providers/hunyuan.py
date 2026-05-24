# -*- coding: utf-8 -*-
"""
异步腾讯云混元大模型客户端
"""

import json
import os
from typing import Any, Dict, List, Optional

import aiohttp

from .base import BaseAsyncLLMClient


class AsyncHunyuanClient(BaseAsyncLLMClient):
    """
    异步腾讯云混元大模型客户端

    Args:
        api_key: 腾讯云混元 API 密钥 (SecretId)
        api_secret: 腾讯云 API 密钥 (SecretKey)
        model: 模型名称
        region: 区域，默认 ap-guangzhou
        system_prompt: 系统提示词
        temperature: 温度参数
        timeout: 请求超时时间（秒）
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        model: str = "hunyuan-turbo",
        region: str = "ap-guangzhou",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("TENCENT_SECRET_ID")
        self.api_secret = api_secret or os.getenv("TENCENT_SECRET_KEY")
        if not self.api_key or not self.api_secret:
            raise ValueError("API Key 和 Secret 未设置")
        self.model = model
        self.region = region
        self.base_url = f"https://hunyuan.tencentcloudapi.com"
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """生成文本回复"""
        # 注意：腾讯云混元需要特殊的签名，这里我们暂时简化实现
        # 真实实现需要使用腾讯云 SDK 或者正确的签名
        raise NotImplementedError(
            "腾讯云混元暂时需要使用腾讯云官方 SDK，或请使用 OpenAI 兼容的接口"
        )

    async def generate_json(
        self, prompt: str, schema: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> str:
        """生成 JSON 格式回复"""
        raise NotImplementedError(
            "腾讯云混元暂时需要使用腾讯云官方 SDK，或请使用 OpenAI 兼容的接口"
        )


class AsyncHunyuanOpenAIClient(BaseAsyncLLMClient):
    """
    使用 OpenAI 兼容接口的腾讯云混元客户端（简化版）

    Args:
        api_key: API 密钥
        model: 模型名称
        base_url: OpenAI 兼容接口地址
        system_prompt: 系统提示词
        temperature: 温度参数
        timeout: 请求超时时间（秒）
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "hunyuan-turbo",
        base_url: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("TENCENT_HUNYUAN_API_KEY")
        if not self.api_key:
            raise ValueError("API Key 未设置")
        self.model = model
        self.base_url = base_url or os.getenv("TENCENT_HUNYUAN_BASE_URL")
        if not self.base_url:
            raise ValueError("需要提供 OpenAI 兼容的 Base URL")
        self.base_url = self.base_url.rstrip("/")
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """生成文本回复"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages: List[Dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload: Dict[str, Any] = {
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
                f"{self.base_url}/chat/completions", headers=headers, json=payload
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
