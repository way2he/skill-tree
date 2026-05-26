# -*- coding: utf-8 -*-
"""
llm.ollama.providers.ollama_official - Ollama SDK Provider 实现

继承 OllamaSDKBaseClient，使用 ollama 官方 SDK 作为底层客户端。
"""

import json
import os
from typing import Any, Generator, Optional

from ollama import Client, AsyncClient

from .base import OllamaSDKBaseClient


DEFAULT_MODEL: str = "qwen2.5:7b"
DEFAULT_HOST: str = "http://localhost:11434"


class OllamaSDKClient(OllamaSDKBaseClient):
    """
    Ollama SDK Provider 客户端

    基于 ollama 官方 Python SDK，继承 OllamaSDKBaseClient 基类。
    提供 generate()、generate_json()、generate_stream()、chat()、chat_stream() 等方法。
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        host: Optional[str] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> None:
        """
        初始化 Ollama SDK Provider 客户端。

        Args:
            model: 默认使用的模型名称。
            host: Ollama 服务地址。
            timeout: 请求超时时间（秒）。
            **kwargs: 传递给 ollama.Client 的额外参数。
        """
        # 保存参数供 _create_client 使用
        self._host = host or DEFAULT_HOST
        self._timeout = timeout
        self._extra_kwargs = kwargs

        # 调用父类初始化
        super().__init__(model=model)

        # 创建客户端
        self._client = self._create_client()

    def _create_client(self, **kwargs) -> Client:
        """
        创建 Ollama SDK 客户端实例。

        Args:
            **kwargs: 未使用的参数（由父类传入）。

        Returns:
            ollama.Client: Ollama SDK 客户端实例。
        """
        client_params: dict[str, Any] = {"host": self._host}

        if self._timeout is not None:
            client_params["timeout"] = self._timeout

        client_params.update(self._extra_kwargs)

        return Client(**client_params)

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
        生成文本回复（非流式）。
        """
        if not isinstance(prompt, str):
            raise TypeError(
                f"prompt 参数必须为字符串，实际传入类型为 {type(prompt).__name__}"
            )
        if not prompt.strip():
            raise ValueError("prompt 参数不能为空字符串")

        request_params: dict[str, Any] = {
            "model": model or self._model,
            "prompt": prompt,
        }

        if system is not None:
            if not isinstance(system, str):
                raise TypeError("system 参数必须为字符串")
            request_params["system"] = system

        if temperature is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["temperature"] = temperature

        if top_p is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["top_p"] = top_p

        if max_tokens is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["num_predict"] = max_tokens

        request_params.update(kwargs)

        response = self._client.generate(**request_params)
        return response.get("response", "")

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
        生成 JSON 格式回复。
        """
        if not isinstance(prompt, str):
            raise TypeError(
                f"prompt 参数必须为字符串，实际传入类型为 {type(prompt).__name__}"
            )
        if not prompt.strip():
            raise ValueError("prompt 参数不能为空字符串")

        json_instruction = (
            "\n\n请以纯 JSON 格式返回结果，不要包含任何额外的说明文字、"
            "markdown 代码块标记或其他非 JSON 内容。"
            "直接输出 JSON 对象即可。"
        )

        final_system: Optional[str] = None
        if system is not None:
            final_system = system + json_instruction
        else:
            final_system = "你是一个 JSON 数据生成助手。" + json_instruction

        request_params: dict[str, Any] = {
            "model": model or self._model,
            "prompt": prompt,
            "system": final_system,
            "format": "json",
            "stream": False,
        }

        if temperature is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["temperature"] = temperature

        request_params.update(kwargs)

        response = self._client.generate(**request_params)
        raw_text = response.get("response", "")

        if not raw_text.strip() and "thinking" in response:
            raw_text = str(response.get("thinking", ""))

        if not raw_text.strip():
            raise ValueError("Ollama 返回的响应为空")

        try:
            json.loads(raw_text)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"模型输出不是有效的 JSON 格式。原始输出: {raw_text[:200]}"
            ) from e

        return raw_text

    def generate_stream(
        self,
        prompt: str,
        system: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> Generator[str, None, None]:
        """
        流式生成文本回复。
        """
        if not isinstance(prompt, str):
            raise TypeError(
                f"prompt 参数必须为字符串，实际传入类型为 {type(prompt).__name__}"
            )
        if not prompt.strip():
            raise ValueError("prompt 参数不能为空字符串")

        request_params: dict[str, Any] = {
            "model": model or self._model,
            "prompt": prompt,
            "stream": True,
        }

        if system is not None:
            if not isinstance(system, str):
                raise TypeError("system 参数必须为字符串")
            request_params["system"] = system

        if temperature is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["temperature"] = temperature

        if top_p is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["top_p"] = top_p

        if max_tokens is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["num_predict"] = max_tokens

        request_params.update(kwargs)

        stream = self._client.generate(**request_params)

        for chunk in stream:
            if "response" in chunk:
                yield chunk["response"]

    def chat(
        self,
        messages: list[dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """
        聊天模式（非流式）。
        """
        if not isinstance(messages, list):
            raise TypeError("messages 参数必须为列表")

        request_params: dict[str, Any] = {
            "model": model or self._model,
            "messages": messages,
        }

        if temperature is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["temperature"] = temperature

        if top_p is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["top_p"] = top_p

        if max_tokens is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["num_predict"] = max_tokens

        request_params.update(kwargs)

        response = self._client.chat(**request_params)
        message = response.get("message", {})
        return message.get("content", "")

    def chat_stream(
        self,
        messages: list[dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> Generator[str, None, None]:
        """
        聊天模式（流式）。
        """
        if not isinstance(messages, list):
            raise TypeError("messages 参数必须为列表")

        request_params: dict[str, Any] = {
            "model": model or self._model,
            "messages": messages,
            "stream": True,
        }

        if temperature is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["temperature"] = temperature

        if top_p is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["top_p"] = top_p

        if max_tokens is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["num_predict"] = max_tokens

        request_params.update(kwargs)

        stream = self._client.chat(**request_params)

        for chunk in stream:
            message = chunk.get("message", {})
            if "content" in message:
                yield message["content"]


class AsyncOllamaSDKClient(OllamaSDKBaseClient):
    """
    Ollama SDK Provider 异步客户端

    基于 ollama 官方 Python SDK，继承 OllamaSDKBaseClient 基类。
    提供异步版本的生成方法。
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        host: Optional[str] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> None:
        """
        初始化 Ollama SDK Provider 异步客户端。

        Args:
            model: 默认使用的模型名称。
            host: Ollama 服务地址。
            timeout: 请求超时时间（秒）。
            **kwargs: 传递给 ollama.AsyncClient 的额外参数。
        """
        # 保存参数供 _create_client 使用
        self._host = host or DEFAULT_HOST
        self._timeout = timeout
        self._extra_kwargs = kwargs

        # 调用父类初始化
        super().__init__(model=model)

        # 创建客户端
        self._client = self._create_client()

    def _create_client(self, **kwargs) -> AsyncClient:
        """
        创建 Ollama SDK 异步客户端实例。

        Args:
            **kwargs: 未使用的参数（由父类传入）。

        Returns:
            ollama.AsyncClient: Ollama SDK 异步客户端实例。
        """
        client_params: dict[str, Any] = {"host": self._host}

        if self._timeout is not None:
            client_params["timeout"] = self._timeout

        client_params.update(self._extra_kwargs)

        return AsyncClient(**client_params)

    async def generate(
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
        异步生成文本回复（非流式）。
        """
        if not isinstance(prompt, str):
            raise TypeError(
                f"prompt 参数必须为字符串，实际传入类型为 {type(prompt).__name__}"
            )
        if not prompt.strip():
            raise ValueError("prompt 参数不能为空字符串")

        request_params: dict[str, Any] = {
            "model": model or self._model,
            "prompt": prompt,
        }

        if system is not None:
            if not isinstance(system, str):
                raise TypeError("system 参数必须为字符串")
            request_params["system"] = system

        if temperature is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["temperature"] = temperature

        if top_p is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["top_p"] = top_p

        if max_tokens is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["num_predict"] = max_tokens

        request_params.update(kwargs)

        response = await self._client.generate(**request_params)
        return response.get("response", "")

    async def generate_json(
        self,
        prompt: str,
        schema: Optional[dict[str, Any]] = None,
        system: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.0,
        **kwargs,
    ) -> str:
        """
        异步生成 JSON 格式回复。
        """
        if not isinstance(prompt, str):
            raise TypeError(
                f"prompt 参数必须为字符串，实际传入类型为 {type(prompt).__name__}"
            )
        if not prompt.strip():
            raise ValueError("prompt 参数不能为空字符串")

        json_instruction = (
            "\n\n请以纯 JSON 格式返回结果，不要包含任何额外的说明文字、"
            "markdown 代码块标记或其他非 JSON 内容。"
            "直接输出 JSON 对象即可。"
        )

        final_system: Optional[str] = None
        if system is not None:
            final_system = system + json_instruction
        else:
            final_system = "你是一个 JSON 数据生成助手。" + json_instruction

        request_params: dict[str, Any] = {
            "model": model or self._model,
            "prompt": prompt,
            "system": final_system,
            "format": "json",
            "stream": False,
        }

        if temperature is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["temperature"] = temperature

        request_params.update(kwargs)

        response = await self._client.generate(**request_params)
        raw_text = response.get("response", "")

        if not raw_text.strip() and "thinking" in response:
            raw_text = str(response.get("thinking", ""))

        if not raw_text.strip():
            raise ValueError("Ollama 返回的响应为空")

        try:
            json.loads(raw_text)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"模型输出不是有效的 JSON 格式。原始输出: {raw_text[:200]}"
            ) from e

        return raw_text

    async def generate_stream(
        self,
        prompt: str,
        system: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ):
        """
        异步流式生成文本回复。
        """
        if not isinstance(prompt, str):
            raise TypeError(
                f"prompt 参数必须为字符串，实际传入类型为 {type(prompt).__name__}"
            )
        if not prompt.strip():
            raise ValueError("prompt 参数不能为空字符串")

        request_params: dict[str, Any] = {
            "model": model or self._model,
            "prompt": prompt,
            "stream": True,
        }

        if system is not None:
            if not isinstance(system, str):
                raise TypeError("system 参数必须为字符串")
            request_params["system"] = system

        if temperature is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["temperature"] = temperature

        if top_p is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["top_p"] = top_p

        if max_tokens is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["num_predict"] = max_tokens

        request_params.update(kwargs)

        stream = await self._client.generate(**request_params)

        async for chunk in stream:
            if "response" in chunk:
                yield chunk["response"]

    async def chat(
        self,
        messages: list[dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """
        异步聊天模式（非流式）。
        """
        if not isinstance(messages, list):
            raise TypeError("messages 参数必须为列表")

        request_params: dict[str, Any] = {
            "model": model or self._model,
            "messages": messages,
        }

        if temperature is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["temperature"] = temperature

        if top_p is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["top_p"] = top_p

        if max_tokens is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["num_predict"] = max_tokens

        request_params.update(kwargs)

        response = await self._client.chat(**request_params)
        message = response.get("message", {})
        return message.get("content", "")

    async def chat_stream(
        self,
        messages: list[dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ):
        """
        异步聊天模式（流式）。
        """
        if not isinstance(messages, list):
            raise TypeError("messages 参数必须为列表")

        request_params: dict[str, Any] = {
            "model": model or self._model,
            "messages": messages,
            "stream": True,
        }

        if temperature is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["temperature"] = temperature

        if top_p is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["top_p"] = top_p

        if max_tokens is not None:
            request_params["options"] = request_params.get("options", {})
            request_params["options"]["num_predict"] = max_tokens

        request_params.update(kwargs)

        stream = await self._client.chat(**request_params)

        async for chunk in stream:
            message = chunk.get("message", {})
            if "content" in message:
                yield message["content"]
