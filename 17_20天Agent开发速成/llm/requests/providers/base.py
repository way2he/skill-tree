# -*- coding: utf-8 -*-
"""
同步 LLM 客户端基础组件
包含 LLMResponse 和 BaseLLMClient
"""

from abc import ABC, abstractmethod
from typing import Any

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


class BaseLLMClient(ABC):
    """同步 LLM 客户端抽象基类"""

    @abstractmethod
    def generate(self, prompt: str, **kwargs: Any) -> str:
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
    def generate_json(
        self, prompt: str, schema: dict[str, Any] | None = None, **kwargs: Any
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
        return LLMResponse(content=content, model=getattr(self, "model", None))
