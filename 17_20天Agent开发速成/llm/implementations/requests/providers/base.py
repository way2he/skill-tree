# -*- coding: utf-8 -*-
"""
同步 LLM 客户端基础组件

定义底层 Provider 的基础接口，实现 IProviderClient 协议。
各厂商 Provider 继承此类并实现具体的 API 调用逻辑。
"""

from abc import ABC, abstractmethod
from typing import Any, Iterator, AsyncIterator

from pydantic import BaseModel


class LLMResponse(BaseModel):
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
    model: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    finish_reason: str | None = None


class BaseProviderClient(ABC):
    """
    Requests 层 Provider 基类

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
        return self.DEFAULT_MODEL

    @abstractmethod
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        同步生成文本回复

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
    def generate_stream(self, prompt: str, **kwargs: Any) -> Iterator[str]:
        """
        同步流式生成

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Yields:
            逐个返回的文本片段
        """
        pass

    def generate_json(
        self,
        prompt: str,
        schema: dict[str, Any] | None = None,
        **kwargs: Any
    ) -> str:
        """
        生成 JSON 格式回复

        默认实现：使用普通 generate，通过 prompt 引导 JSON 输出。
        子类可覆盖以提供更优实现（如 response_format）。

        Args:
            prompt: 用户输入的提示词文本
            schema: 可选的 JSON Schema 字典
            **kwargs: 可选参数

        Returns:
            符合指定 Schema 的 JSON 字符串
        """
        # 默认实现：子类可覆盖
        return self.generate(prompt, **kwargs)

    def generate_with_response(self, prompt: str, **kwargs: Any) -> LLMResponse:
        """
        生成文本回复并返回完整响应对象

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Returns:
            LLMResponse 对象
        """
        content = self.generate(prompt, **kwargs)
        return LLMResponse(
            content=content,
            model=getattr(self, "model", None) or self.DEFAULT_MODEL,
        )

    # =========================================================================
    # 异步方法（使用 httpx 实现）
    # =========================================================================

    @abstractmethod
    async def agenerate(self, prompt: str, **kwargs: Any) -> str:
        """
        异步生成文本回复

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

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

    async def agenerate_with_response(self, prompt: str, **kwargs: Any) -> LLMResponse:
        """
        异步生成文本回复并返回完整响应对象

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Returns:
            LLMResponse 对象
        """
        content = await self.agenerate(prompt, **kwargs)
        return LLMResponse(
            content=content,
            model=getattr(self, "model", None) or self.DEFAULT_MODEL,
        )


# =============================================================================
# 向后兼容：保留旧的 BaseLLMClient
# =============================================================================

class BaseLLMClient(BaseProviderClient):
    """
    向后兼容别名

    旧代码使用 BaseLLMClient，新代码应使用 BaseProviderClient。
    """
    pass
