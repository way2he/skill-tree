# -*- coding: utf-8 -*-
"""
同步Ollama本地模型客户端
"""

import json
import os
from typing import Any, Iterator

import requests

from .base import BaseLLMClient


class OllamaClient(BaseLLMClient):
    """
    同步 Ollama 本地模型客户端
    API 文档: https://github.com/ollama/ollama/blob/main/docs/api.md

    使用示例:
        client = OllamaClient(model="qwen3.5:9b", base_url="http://localhost:11434")
        response = client.generate("你好，请介绍一下自己")

    Args:
        model: 模型名称，如 "qwen3.5:9b", "llama3:8b", "mistral:7b"
        base_url: Ollama 服务地址，默认 http://localhost:11434
        system_prompt: 系统提示词，用于设置模型行为
        temperature: 温度参数，控制输出随机性 (0-2，默认0.7)
        timeout: 请求超时时间（秒），默认120秒
    """

    def __init__(
        self,
        model: str = "qwen3.5:9b",
        base_url: str = "http://localhost:11434",
        system_prompt: str | None = None,
        temperature: float = 0.7,
        timeout: int = 600,
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout

    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        生成文本回复

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数
                - temperature: 温度参数
                - timeout: 请求超时时间（秒）

        Returns:
            模型生成的文本响应字符串
        """
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "system": self.system_prompt,
            "temperature": kwargs.get("temperature", self.temperature),
            "stream": False,
        }

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        return str(response.json()["response"])

    def generate_stream(self, prompt: str, **kwargs: Any) -> Iterator[str]:
        """流式生成（Ollama NDJSON，每行一个 JSON）"""
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "system": self.system_prompt,
            "temperature": kwargs.get("temperature", self.temperature),
            "stream": True,
        }
        with requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
            stream=True,
        ) as resp:
            resp.raise_for_status()
            for raw in resp.iter_lines(decode_unicode=True):
                if not raw:
                    continue
                try:
                    obj = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                piece = obj.get("response") or ""
                if piece:
                    yield piece
                if obj.get("done"):
                    break

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
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "system": self.system_prompt,
            "temperature": 0.3,
            "format": "json",
            "stream": False,
        }

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()

        response_json = response.json()
        response_str = str(response_json.get("response", ""))

        if not response_str.strip() and "thinking" in response_json:
            response_str = str(response_json.get("thinking", ""))

        if not response_str.strip():
            raise ValueError("Ollama 返回的响应为空")

        return response_str
