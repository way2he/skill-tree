# -*- coding: utf-8 -*-
"""
Google Gemini 官方 SDK 客户端

基于 google-generativeai SDK 实现，使用 API Key 鉴权。

依赖安装：
    pip install google-generativeai

文档参考：
    https://ai.google.dev/gemini-api/docs
"""

import json
from typing import Any, Optional

from ..client import GoogleClient


class GeminiOfficialClient(GoogleClient):
    """
    Google Gemini 官方 SDK 客户端

    使用 google.generativeai.GenerativeModel 进行模型调用。

    Args:
        api_key: API Key
        model: 模型名称，如 "gemini-pro", "gemini-pro-vision"
        system_prompt: 系统提示词
        temperature: 温度参数 (0-2)
        max_tokens: 最大输出 token 数
    """

    def _init_client(self) -> None:
        """
        初始化 google-generativeai 客户端
        """
        try:
            import google.generativeai as genai

            # 配置 API Key
            genai.configure(api_key=self.api_key)

            # 初始化模型
            self.model_instance = genai.GenerativeModel(
                model_name=self.model,
                system_instruction=self.system_prompt
            )
        except ImportError:
            raise ImportError(
                "google-generativeai 未安装，请运行: pip install google-generativeai"
            )

    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        生成文本回复

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数，如 temperature, max_output_tokens

        Returns:
            模型生成的文本响应字符串

        Example:
            >>> client = GeminiOfficialClient(api_key="your-api-key")
            >>> response = client.generate("你好，请介绍一下自己")
            >>> print(response)
        """
        # 构建生成配置
        generation_config: dict[str, Any] = {}

        if self.temperature is not None:
            generation_config["temperature"] = kwargs.get("temperature", self.temperature)

        if self.max_tokens is not None:
            generation_config["max_output_tokens"] = kwargs.get("max_tokens", self.max_tokens)

        # 调用 API
        response = self.model_instance.generate_content(
            prompt,
            generation_config=generation_config if generation_config else None
        )

        # 提取文本响应
        if response and response.text:
            return str(response.text)

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
            >>> client = GeminiOfficialClient(api_key="your-api-key")
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

        # 构建生成配置
        generation_config: dict[str, Any] = {}

        if self.temperature is not None:
            generation_config["temperature"] = kwargs.get("temperature", self.temperature)

        if self.max_tokens is not None:
            generation_config["max_output_tokens"] = kwargs.get("max_tokens", self.max_tokens)

        # 调用 API
        response = self.model_instance.generate_content(
            json_prompt,
            generation_config=generation_config if generation_config else None
        )

        # 提取并解析 JSON 响应
        if response and response.text:
            result = str(response.text)

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
