# -*- coding: utf-8 -*-
"""
异步 LLM 客户端基础组件
包含 AsyncLLMResponse 和 BaseAsyncLLMClient，以及 BaseAsyncProviderClient
"""

from abc import ABC, abstractmethod
from typing import Any, Optional, Iterator, AsyncIterator

from pydantic import BaseModel


class AsyncLLMResponse(BaseModel):
    """
    大模型响应数据结构

    Attributes:
        content: 模型返回的文本内容
        model: 使用的模型名称
        prompt_tokens: 输入提示词的 token 数量
        completion_tokens: 生成响应的 token 数量
        total_tokens: 总 token 数量
        finish_reason: 响应结束原因
    """

    content: str
    model: Optional[str] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    finish_reason: Optional[str] = None


class BaseAsyncProviderClient(ABC):
    """
    AioHttp 层 Provider 基类

    实现 core.adapter.base.IProviderClient 接口。
    负责：
    - HTTP 请求处理
    - API 协议实现
    - 响应解析
    - 特定模型的默认值

    子类必须设置类属性:
        PROVIDER_NAME: 厂商名称
        DEFAULT_MODEL: 默认模型
    """

    # 子类必须设置
    PROVIDER_NAME: str = ""
    DEFAULT_MODEL: str = ""

    @property
    def provider_name(self) -> str:
        """厂商名称"""
        return self.PROVIDER_NAME

    @property
    def default_model(self) -> str:
        """默认模型"""
        # 优先使用实例属性（通过构造函数传入的配置），否则使用类属性默认值
        return getattr(self, "model", None) or self.DEFAULT_MODEL

    @abstractmethod
    async def agenerate(self, prompt: str, **kwargs: Any) -> str:
        """
        异步生成文本回复

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数
                - model: 模型名称（覆盖默认）
                - temperature: 温度参数，控制输出随机性
                - max_tokens: 最大生成 token 数
                - timeout: 请求超时时间（秒）

        Returns:
            模型生成的文本响应字符串
        """
        pass

    @abstractmethod
    async def agenerate_stream(self, prompt: str, **kwargs: Any) -> AsyncIterator[str]:
        """
        异步流式生成

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Yields:
            逐个返回的文本片段
        """
        pass

    async def agenerate_json(
        self,
        prompt: str,
        schema: dict[str, Any] | None = None,
        **kwargs: Any
    ) -> str:
        """
        异步生成 JSON 格式回复

        默认实现：使用普通 agenerate。
        子类可覆盖以提供更优实现。

        Args:
            prompt: 用户输入的提示词文本
            schema: 可选的 JSON Schema 字典
            **kwargs: 可选参数

        Returns:
            符合指定 Schema 的 JSON 字符串
        """
        return await self.agenerate(prompt, **kwargs)

    async def agenerate_with_response(self, prompt: str, **kwargs: Any) -> AsyncLLMResponse:
        """
        异步生成文本回复并返回完整响应对象

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Returns:
            AsyncLLMResponse 对象
        """
        content = await self.agenerate(prompt, **kwargs)
        return AsyncLLMResponse(
            content=content,
            model=getattr(self, "model", None) or self.DEFAULT_MODEL,
        )

    # =========================================================================
    # 同步方法（通过 asyncio.run 实现，用于适配 IProviderClient）
    # =========================================================================

    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        同步生成文本回复（通过 asyncio.run 调用异步方法）

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Returns:
            模型生成的文本响应字符串
        """
        import asyncio
        return asyncio.run(self.agenerate(prompt, **kwargs))

    def generate_stream(self, prompt: str, **kwargs: Any) -> Iterator[str]:
        """
        同步流式生成（通过 asyncio.run 调用异步方法）

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Yields:
            逐个返回的文本片段
        """
        import asyncio
        from typing import AsyncGenerator

        async def _wrapper():
            async for chunk in self.agenerate_stream(prompt, **kwargs):
                yield chunk

        gen = _wrapper()

        try:
            while True:
                yield asyncio.run(gen.__anext__())
        except StopAsyncIteration:
            pass

    def generate_json(
        self,
        prompt: str,
        schema: dict[str, Any] | None = None,
        **kwargs: Any
    ) -> str:
        """
        同步生成 JSON 格式回复

        Args:
            prompt: 用户输入的提示词文本
            schema: 可选的 JSON Schema 字典
            **kwargs: 可选参数

        Returns:
            符合指定 Schema 的 JSON 字符串
        """
        import asyncio
        return asyncio.run(self.agenerate_json(prompt, schema, **kwargs))


class BaseAsyncLLMClient(BaseAsyncProviderClient):
    """
    向后兼容别名

    旧代码使用 BaseAsyncLLMClient，新代码应使用 BaseAsyncProviderClient。
    """
    pass
