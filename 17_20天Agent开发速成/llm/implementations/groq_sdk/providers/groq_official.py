# -*- coding: utf-8 -*-
"""
Groq 官方 SDK 客户端

基于 groq SDK 实现，使用 API Key 鉴权。

依赖安装：
    pip install groq

文档参考：
    https://console.groq.com/docs
"""

import json
from typing import Any, Optional

from ..client import GroqClient


class GroqOfficialClient(GroqClient):
    """
    Groq 官方 SDK 客户端

    使用 groq.Groq 进行模型调用。

    Args:
        api_key: API Key
        model: 模型名称，如 "llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"
        system_prompt: 系统提示词
        temperature: 温度参数 (0-2)
        max_tokens: 最大输出 token 数
    """

    def _init_client(self) -> None:
        """
        初始化 groq 客户端
        """
        try:
            from groq import Groq

            # 初始化客户端
            self.client = Groq(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "groq 未安装，请运行: pip install groq"
            )

    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        生成文本回复

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数，如 temperature, max_tokens

        Returns:
            模型生成的文本响应字符串

        Example:
            >>> client = GroqOfficialClient(api_key="your-api-key")
            >>> response = client.generate("你好，请介绍一下自己")
            >>> print(response)
        """
        messages = self._build_messages(prompt)

        # 构建请求参数
        params: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }

        # 添加可选参数
        if self.temperature is not None:
            params["temperature"] = kwargs.get("temperature", self.temperature)

        if self.max_tokens is not None:
            params["max_tokens"] = kwargs.get("max_tokens", self.max_tokens)

        # 调用 API
        response = self.client.chat.completions.create(**params)

        # 提取文本响应
        if response and response.choices and len(response.choices) > 0:
            message = response.choices[0].message
            return str(message.content) if message else ""

        return ""

    def generate_json(
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

        Example:
            >>> client = GroqOfficialClient(api_key="your-api-key")
            >>> schema = {
            ...     "type": "object",
            ...     "properties": {
            ...         "name": {"type": "string"},
            ...         "age": {"type": "integer"}
            ...     }
            ... }
            >>> response = client.generate_json(
            ...     "生成一个用户信息",
            ...     schema=schema
            ... )
        """
        # 构建 JSON 格式提示词
        json_prompt = prompt
        if schema:
            json_prompt = (
                f"{prompt}\\n\\n"
                f"请严格按照以下 JSON Schema 格式返回结果：\\n"
                f"{json.dumps(schema, ensure_ascii=False, indent=2)}\\n"
                f"只返回 JSON 字符串，不要包含其他内容。"
            )

        messages = self._build_messages(json_prompt)

        # 构建请求参数
        params: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }

        # 添加可选参数
        if self.temperature is not None:
            params["temperature"] = kwargs.get("temperature", self.temperature)

        if self.max_tokens is not None:
            params["max_tokens"] = kwargs.get("max_tokens", self.max_tokens)

        # 调用 API
        response = self.client.chat.completions.create(**params)

        # 提取并解析 JSON 响应
        if response and response.choices and len(response.choices) > 0:
            message = response.choices[0].message
            result = str(message.content) if message else "{}"

            # 尝试提取 JSON 部分
            try:
                start = result.find("{")
                end = result.rfind("}")
                if start != -1 and end != -1:
                    json_str = result[start:end + 1]
                    # 验证 JSON 格式
                    parsed = json.loads(json_str)
                    return json.dumps(parsed, ensure_ascii=False)
            except json.JSONDecodeError:
                pass

            return result

        return "{}"
