# -*- coding: utf-8 -*-
"""
OpenAI SDK 兼容基类
所有兼容 OpenAI Chat Completions API 的厂商客户端都继承此基类
"""

import json
from abc import ABC
from typing import Any, Generator, Optional

from openai import OpenAI


class OpenAICompatibleClient(ABC):
    """
    OpenAI SDK 兼容客户端基类

    基于 openai.OpenAI SDK，通过设置不同的 base_url 和 api_key
    来适配各种兼容 OpenAI 协议的厂商。

    Args:
        api_key: API 密钥
        model: 模型名称
        base_url: API 基础地址
        system_prompt: 系统提示词
        temperature: 温度参数 (0-2)
        max_tokens: 最大输出 token 数

    Attributes:
        PROVIDER_NAME: 厂商名称（子类必须定义）
        DEFAULT_MODEL: 默认模型名称（子类必须定义）
    """

    # 子类必须定义
    PROVIDER_NAME: str = ""
    DEFAULT_MODEL: str = ""

    @property
    def provider_name(self) -> str:
        """厂商名称"""
        return self.PROVIDER_NAME

    @property
    def default_model(self) -> str:
        """默认模型"""
        return getattr(self, "model", None) or self.DEFAULT_MODEL

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        base_url: str = "https://api.openai.com/v1",
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> None:
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens

        # 初始化 OpenAI SDK 客户端
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    def _build_messages(self, prompt: str) -> list[dict[str, str]]:
        """
        构建消息列表

        Args:
            prompt: 用户提示词

        Returns:
            符合 OpenAI 格式的消息列表
        """
        messages: list[dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})
        return messages

    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        生成文本回复

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数
                - temperature: 温度参数
                - max_tokens: 最大生成 token 数

        Returns:
            模型生成的文本响应字符串
        """
        # 构建请求参数
        create_kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": self._build_messages(prompt),
            "temperature": kwargs.get("temperature", self.temperature),
        }

        # max_tokens 可选
        if self.max_tokens is not None:
            create_kwargs["max_tokens"] = self.max_tokens
        if "max_tokens" in kwargs:
            create_kwargs["max_tokens"] = kwargs["max_tokens"]

        # 调用 OpenAI SDK
        response = self.client.chat.completions.create(**create_kwargs)

        # 提取文本内容
        content = response.choices[0].message.content
        if content is None:
            raise ValueError("模型返回内容为空")

        return str(content)

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
        messages = self._build_messages(prompt)

        # 如果有 schema，添加 JSON 生成指令
        if schema:
            schema_str = json.dumps(schema, ensure_ascii=False)
            messages.append({
                "role": "system",
                "content": f"你是一个严格的 JSON 生成器。必须返回有效的 JSON，格式如下：{schema_str}。只输出 JSON，不要有任何解释。",
            })

        # 构建请求参数
        create_kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.3,
            "response_format": {"type": "json_object"},
        }

        if self.max_tokens is not None:
            create_kwargs["max_tokens"] = self.max_tokens

        # 调用 OpenAI SDK
        response = self.client.chat.completions.create(**create_kwargs)

        content = response.choices[0].message.content
        if content is None:
            raise ValueError("模型返回内容为空")

        return str(content)

    def generate_stream(self, prompt: str, **kwargs: Any) -> Generator[str, None, None]:
        """
        流式生成文本回复

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Yields:
            每次生成的文本增量
        """
        create_kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": self._build_messages(prompt),
            "temperature": kwargs.get("temperature", self.temperature),
            "stream": True,
        }

        if self.max_tokens is not None:
            create_kwargs["max_tokens"] = self.max_tokens

        # 流式调用
        stream = self.client.chat.completions.create(**create_kwargs)

        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content is not None:
                yield str(delta.content)
