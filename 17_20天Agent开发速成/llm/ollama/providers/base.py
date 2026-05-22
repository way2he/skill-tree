# -*- coding: utf-8 -*-
"""
llm.ollama.providers.base - Ollama SDK Provider 基类

为 Ollama 官方 SDK 提供一个统一的基类，方便扩展和维护。
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class OllamaSDKBaseClient(ABC):
    """
    Ollama SDK Provider 基类

    定义 Ollama 官方 SDK 客户端的基本接口。
    """

    def __init__(
        self,
        model: str,
    ) -> None:
        """
        初始化基类。

        Args:
            model: 默认使用的模型名称。
        """
        if not isinstance(model, str) or not model.strip():
            raise ValueError("model 参数必须为非空字符串")

        self._model = model.strip()

    @property
    def model(self) -> str:
        """获取当前默认模型名称。"""
        return self._model

    @abstractmethod
    def _create_client(self, **kwargs) -> Any:
        """
        创建 Ollama 客户端实例的抽象方法。

        子类需要实现这个方法来创建具体的同步或异步客户端。

        Args:
            **kwargs: 额外的参数。

        Returns:
            客户端实例。
        """
        pass

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """
        生成文本回复（非流式）的抽象方法。

        Args:
            prompt: 用户输入的提示文本。
            system: 系统提示词。
            model: 覆盖默认模型名称。
            temperature: 采样温度。
            top_p: 核采样概率阈值。
            max_tokens: 最大生成 token 数。
            **kwargs: 传递给 API 的额外参数。

        Returns:
            模型生成的文本内容。
        """
        pass

    @abstractmethod
    def generate_json(
        self,
        prompt: str,
        schema: Optional[dict[str, Any]] = None,
        system: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.0,
        **kwargs,
    ) -> str:
        """
        生成 JSON 格式回复的抽象方法。

        Args:
            prompt: 用户输入的提示文本。
            schema: 可选的 JSON Schema 字典。
            system: 系统提示词。
            model: 覆盖默认模型名称。
            temperature: 采样温度。
            **kwargs: 传递给 API 的额外参数。

        Returns:
            符合指定 Schema 的 JSON 字符串。
        """
        pass
