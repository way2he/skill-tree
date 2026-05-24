# -*- coding: utf-8 -*-
"""
同步腾讯混元(Hunyuan)客户端
"""

import json
import os
import time
from typing import Any

import requests

from .base import BaseLLMClient


class HunyuanClient(BaseLLMClient):
    """
    同步腾讯混元 Hunyuan 客户端
    API 文档: https://cloud.tencent.com/document/product/1729

    使用示例:
        client = HunyuanClient(
            secret_id="your-secret-id",
            secret_key="your-secret-key",
            model="hunyuan-turbo"
        )
        response = client.generate("你好，请介绍一下自己")

    Args:
        secret_id: 腾讯云 SecretId，可通过环境变量 TENCENT_SECRET_ID 设置
        secret_key: 腾讯云 SecretKey，可通过环境变量 TENCENT_SECRET_KEY 设置
        model: 模型名称，如 "hunyuan-turbo", "hunyuan-pro"
        system_prompt: 系统提示词，用于设置模型行为
        temperature: 温度参数，控制输出随机性 (0-1，默认0.7)
        timeout: 请求超时时间（秒），默认60秒

    Note:
        腾讯混元使用腾讯云签名认证，需要 secret_id 和 secret_key
    """

    def __init__(
        self,
        secret_id: str | None = None,
        secret_key: str | None = None,
        model: str = "hunyuan-turbo",
        system_prompt: str | None = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.secret_id = secret_id or os.getenv("TENCENT_SECRET_ID")
        self.secret_key = secret_key or os.getenv("TENCENT_SECRET_KEY")
        if not self.secret_id or not self.secret_key:
            raise ValueError("Secret Id 和 Secret Key 未设置，请设置 TENCENT_SECRET_ID 和 TENCENT_SECRET_KEY 环境变量")
        self.model = model
        self.base_url = "https://hunyuan.tencentcloudapi.com"
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout

    def _generate_signature(self, timestamp: int) -> str:
        """
        生成腾讯云 API 签名（简化版）

        Args:
            timestamp: 时间戳

        Returns:
            签名字符串
        """
        import hashlib
        import hmac

        sign_str = f"ecret_id={self.secret_id}&secret_key={self.secret_key}&timestamp={timestamp}"
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            sign_str.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return signature

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
                - timeout: 请求超时时间（秒）

        Returns:
            模型生成的文本响应字符串
        """
        timestamp = int(time.time())

        headers: dict[str, str] = {
            "Content-Type": "application/json",
        }

        payload: dict[str, Any] = {
            "SecretId": self.secret_id,
            "Signature": self._generate_signature(timestamp),
            "Timestamp": timestamp,
            "Nonce": timestamp,
            "Model": self.model,
            "Messages": self._build_messages(prompt),
            "Temperature": kwargs.get("temperature", self.temperature),
        }

        response = requests.post(
            self.base_url,
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        return str(response.json()["Response"]["Choices"][0]["Message"]["Content"])

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
        timestamp = int(time.time())

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
            "SecretId": self.secret_id,
            "Signature": self._generate_signature(timestamp),
            "Timestamp": timestamp,
            "Nonce": timestamp,
            "Model": self.model,
            "Messages": messages,
            "Temperature": 0.3,
        }

        response = requests.post(
            self.base_url,
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        return str(response.json()["Response"]["Choices"][0]["Message"]["Content"])

    def generate_stream(self, prompt: str, **kwargs: Any):
        """流式生成（混元 SSE，与本类简化签名风格保持一致）"""
        timestamp = int(time.time())
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
        payload: dict[str, Any] = {
            "SecretId": self.secret_id,
            "Signature": self._generate_signature(timestamp),
            "Timestamp": timestamp,
            "Nonce": timestamp,
            "Model": self.model,
            "Messages": self._build_messages(prompt),
            "Temperature": kwargs.get("temperature", self.temperature),
            "Stream": True,
        }
        with requests.post(
            self.base_url,
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
                if data == "[DONE]":
                    break
                try:
                    obj = json.loads(data)
                    # 兼容大小写字段：Choices/choices、Delta/delta、Content/content
                    choices = obj.get("Choices") or obj.get("choices") or []
                    if not choices:
                        continue
                    delta = choices[0].get("Delta") or choices[0].get("delta") or {}
                    piece = delta.get("Content") or delta.get("content") or ""
                    if piece:
                        yield piece
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue
