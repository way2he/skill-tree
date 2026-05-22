# -*- coding: utf-8 -*-
"""
异步 LLM 客户端基础组件
包含 AsyncLLMResponse 和 BaseAsyncLLMClient
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

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


class BaseAsyncLLMClient(ABC):
    """异步 LLM 客户端抽象基类"""

    @abstractmethod
    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        生成文本回复

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数
                - temperature: 温度参数，控制输出随机性
                - max_tokens: 最大生成 token 数
                - timeout: 请求超时时间（秒）

        Returns:
            模型生成的文本响应字符串
        """
        pass

    @abstractmethod
    async def generate_json(
        self, prompt: str, schema: Optional[dict[str, Any]] = None, **kwargs: Any
    ) -> str:
        """
        生成 JSON 格式回复

        Args:
            prompt: 用户输入的提示词文本
            schema: 可选的 JSON Schema 字典
            **kwargs: 可选参数

        Returns:
            符合指定 Schema 的 JSON 字符串
        """
        pass

    async def generate_with_response(
        self, prompt: str, **kwargs: Any
    ) -> AsyncLLMResponse:
        """
        生成文本回复并返回完整响应对象

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Returns:
            AsyncLLMResponse 对象
        """
        content = await self.generate(prompt, **kwargs)
        return AsyncLLMResponse(content=content, model=getattr(self, "model", None))
