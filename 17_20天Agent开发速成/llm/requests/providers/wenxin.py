# -*- coding: utf-8 -*-
"""
同步百度文心一言客户端
"""

import json
import os
from typing import Any

import requests

from .base import BaseLLMClient


class WenxinClient(BaseLLMClient):
    """
    同步百度文心一言客户端
    API 文档: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/flfmc9do2

    使用示例:
        client = WenxinClient(api_key="your-api-key", secret_key="your-secret-key", model="ernie-4.0-8k-latest")
        response = client.generate("你好，请介绍一下自己")

    Args:
        api_key: 百度 API Key，可通过环境变量 WENXIN_API_KEY 设置
        secret_key: 百度 Secret Key，可通过环境变量 WENXIN_SECRET_KEY 设置
        model: 模型名称，如 "ernie-4.0-8k-latest", "ernie-3.5-8k"
        system_prompt: 系统提示词，用于设置模型行为
        temperature: 温度参数，控制输出随机性 (0-1，默认0.7)
        timeout: 请求超时时间（秒），默认60秒

    Note:
        百度文心一言使用 access_token 认证，需要通过 api_key 和 secret_key 获取
    """

    def __init__(
        self,
        api_key: str | None = None,
        secret_key: str | None = None,
        model: str = "ernie-4.0-8k-latest",
        system_prompt: str | None = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("WENXIN_API_KEY")
        self.secret_key = secret_key or os.getenv("WENXIN_SECRET_KEY")
        if not self.api_key or not self.secret_key:
            raise ValueError("API Key 和 Secret Key 未设置，请设置 WENXIN_API_KEY 和 WENXIN_SECRET_KEY 环境变量")
        self.model = model
        self.base_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions"
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout
        self._access_token: str | None = None

    def _get_access_token(self) -> str:
        """
        获取 access_token

        Returns:
            access_token 字符串
        """
        if self._access_token:
            return self._access_token

        auth_url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key,
        }
        response = requests.post(auth_url, params=params, timeout=self.timeout)
        response.raise_for_status()
        self._access_token = response.json()["access_token"]
        return self._access_token

    def _build_messages(self, prompt: str) -> list[dict[str, str]]:
        """
        构建消息列表

        Args:
            prompt: 用户提示词

        Returns:
            消息列表
        """
        messages: list[dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "user", "content": self.system_prompt})
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
                - timeout: 请求超时时间（秒）

        Returns:
            模型生成的文本响应字符串
        """
        access_token = self._get_access_token()
        url = f"{self.base_url}?access_token={access_token}"

        headers: dict[str, str] = {
            "Content-Type": "application/json",
        }

        payload: dict[str, Any] = {
            "messages": self._build_messages(prompt),
            "temperature": kwargs.get("temperature", self.temperature),
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        return str(response.json()["result"])

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
        access_token = self._get_access_token()
        url = f"{self.base_url}?access_token={access_token}"

        headers: dict[str, str] = {
            "Content-Type": "application/json",
        }

        messages = self._build_messages(prompt)
        if schema:
            schema_str = json.dumps(schema, ensure_ascii=False)
            messages.append(
                {
                    "role": "user",
                    "content": f"你是一个严格的 JSON 生成器。必须返回有效的 JSON，格式如下：{schema_str}。只输出 JSON，不要有任何解释。",
                }
            )

        payload: dict[str, Any] = {
            "messages": messages,
            "temperature": 0.3,
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        return str(response.json()["result"])

    def generate_stream(self, prompt: str, **kwargs: Any):
        """流式生成（文心 SSE：data: {"result": "..."}）"""
        access_token = self._get_access_token()
        url = f"{self.base_url}?access_token={access_token}"
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
        payload: dict[str, Any] = {
            "messages": self._build_messages(prompt),
            "temperature": kwargs.get("temperature", self.temperature),
            "stream": True,
        }
        with requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
            stream=True,
        ) as resp:
            resp.raise_for_status()
            for raw in resp.iter_lines(decode_unicode=True):
                if not raw or not raw.startswith("data:"):
                    continue
                data = raw[5:].strip()
                if not data:
                    continue
                try:
                    obj = json.loads(data)
                    piece = obj.get("result") or ""
                    if piece:
                        yield piece
                    if obj.get("is_end"):
                        break
                except json.JSONDecodeError:
                    continue
