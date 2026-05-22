# -*- coding: utf-8 -*-
"""
小米小爱大模型（MiLM）异步客户端
小米开放平台提供的大模型 API，接口兼容 OpenAI 格式
"""

import os
import json
from typing import Optional, Dict, Any, List

import aiohttp

from .base import BaseAsyncLLMClient, AsyncLLMResponse


class AsyncMiLMClient(BaseAsyncLLMClient):
    """小米小爱大模型异步客户端"""

    DEFAULT_BASE_URL = "https://api.mi.ai/v1"
    DEFAULT_MODEL = "milm-pro"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: int = 60,
    ):
        """
        初始化小米小爱大模型客户端

        Args:
            api_key: 小米开放平台 API Key，如果不传则从环境变量 XIAOMI_API_KEY 获取
            base_url: API 基础地址，默认为小米开放平台地址
            model: 默认使用的模型名称
            timeout: 请求超时时间（秒）
        """
        self.api_key = api_key or os.getenv("XIAOMI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key 未提供，请设置 XIAOMI_API_KEY 环境变量或传入 api_key 参数")

        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.model = model or self.DEFAULT_MODEL
        self.timeout = timeout

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
        stream: bool = False,
        **kwargs,
    ) -> AsyncLLMResponse:
        """
        调用小米小爱大模型生成文本

        Args:
            prompt: 用户输入的提示词
            system_prompt: 系统提示词
            model: 模型名称，如果不传则使用初始化时的默认模型
            temperature: 温度参数，控制随机性
            max_tokens: 最大生成 token 数
            top_p: top_p 采样参数
            stream: 是否使用流式输出（暂未支持）
            **kwargs: 其他传递给 API 的参数

        Returns:
            AsyncLLMResponse: 包含生成结果和元数据的响应对象
        """
        if stream:
            raise NotImplementedError("流式输出暂未支持")

        # 构建消息列表
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # 构建请求体
        payload = {
            "model": model or self.model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        # 添加其他参数
        payload.update(kwargs)

        # 发送请求
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=payload,
                headers=headers,
                timeout=self.timeout,
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API 请求失败: {response.status} - {error_text}")

                result = await response.json()

                # 解析响应
                content = result["choices"][0]["message"]["content"]
                usage = result.get("usage", {})

                return AsyncLLMResponse(
                    content=content,
                    model=result.get("model", model or self.model),
                    usage=usage,
                    raw_response=result,
                )

    async def generate_async(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
        stream: bool = False,
        **kwargs,
    ) -> AsyncLLMResponse:
        """
        异步生成文本（与 generate 方法相同，保持接口兼容）
        """
        return await self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=stream,
            **kwargs,
        )
