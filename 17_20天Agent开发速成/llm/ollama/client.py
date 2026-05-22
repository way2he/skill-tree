# -*- coding: utf-8 -*-
"""
llm.ollama.client - Ollama 官方 SDK 客户端

基于 Ollama 官方 Python SDK (pip install ollama) 封装的客户端。

Ollama SDK 特性:
- 支持同步和异步调用 (Client 和 AsyncClient)
- 支持 chat 和 generate 两种模式
- 支持流式响应
- 支持 JSON 格式输出

环境变量:
- OLLAMA_HOST: Ollama 服务地址 (默认: http://localhost:11434)
- OLLAMA_API_KEY: Ollama API 密钥 (用于云端模型)

默认模型:
- qwen2.5:7b
"""

import json
from typing import Any, Generator, Optional

from ollama import Client, AsyncClient


DEFAULT_MODEL: str = "qwen3.5:9b"
DEFAULT_HOST: str = "http://localhost:11434"


class OllamaOfficialClient:
    """
    Ollama 官方 SDK 同步客户端

    基于 ollama 官方 Python SDK 封装，提供简洁的接口用于调用 Ollama 本地模型。
    支持:
    - 普通文本生成 (generate)
    - JSON 结构化输出 (generate_json)
    - 流式文本生成 (generate_stream)
    - 聊天模式 (chat)
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        host: Optional[str] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> None:
        """
        初始化 Ollama 客户端。

        Args:
            model: 默认使用的模型名称。
            host: Ollama 服务地址 (默认: http://localhost:11434)。
            timeout: 请求超时时间（秒）。
            **kwargs: 传递给 ollama.Client 的额外参数。
        """
        if not isinstance(model, str) or not model.strip():
            raise ValueError("model 参数必须为非空字符串")

        self._model = model.strip()
        self._host = host or DEFAULT_HOST

        # 构建 Ollama 客户端参数
        client_params: dict[str, Any] = {"host": self._host}
        if timeout is not None:
            client_params["timeout"] = timeout
        client_params.update(kwargs)

        # 初始化 Ollama SDK 客户端
        self._client = Client(**client_params)

    @property
    def model(self) -> str:
        """获取当前默认模型名称。"""
        return self._model

    @property
    def host(self) -> str:
        """获取当前 Ollama 服务地址。"""
        return self._host

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

        Args:
            prompt: 用户输入的提示文本。
            system: 系统提示词。
            model: 覆盖默认模型名称。
            temperature: 采样温度（0.0 ~ 2.0）。
            top_p: 核采样概率阈值。
            max_tokens: 最大生成 token 数。
            **kwargs: 传递给 Ollama API 的额外参数。

        Returns:
            str: 模型生成的文本内容。

        Raises:
            TypeError: 当 prompt 参数类型不正确时抛出。
            ValueError: 当 prompt 为空字符串时抛出。
        """
        if not isinstance(prompt, str):
            raise TypeError(
                f"prompt 参数必须为字符串，实际传入类型为 {type(prompt).__name__}"
            )
        if not prompt.strip():
            raise ValueError("prompt 参数不能为空字符串")

        # 构建请求参数
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

        # 调用 Ollama generate API
        response = self._client.generate(**request_params)

        # 返回生成的文本
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

        Args:
            prompt: 用户输入的提示文本。
            schema: 可选的 JSON Schema 字典（当前未使用，保留参数）。
            system: 系统提示词。
            model: 覆盖默认模型名称。
            temperature: 采样温度，默认 0.0 以确保输出稳定性。
            **kwargs: 传递给 Ollama API 的额外参数。

        Returns:
            str: 符合指定 Schema 的 JSON 字符串。

        Raises:
            TypeError: 当 prompt 参数类型不正确时抛出。
            ValueError: 当 prompt 为空或模型输出不是有效 JSON 时抛出。
        """
        if not isinstance(prompt, str):
            raise TypeError(
                f"prompt 参数必须为字符串，实际传入类型为 {type(prompt).__name__}"
            )
        if not prompt.strip():
            raise ValueError("prompt 参数不能为空字符串")

        # 构建 JSON 格式要求的 system prompt
        json_instruction = (
            "\n\n请以纯 JSON 格式返回结果，不要包含任何额外的说明文字、"
            "markdown 代码块标记或其他非 JSON 内容。"
            "直接输出 JSON 对象即可。"
        )

        # 合并用户提供的 system 和 JSON 指令
        final_system: Optional[str] = None
        if system is not None:
            final_system = system + json_instruction
        else:
            final_system = "你是一个 JSON 数据生成助手。" + json_instruction

        # 调用 generate 获取文本，设置 format="json" 让 Ollama 强制返回 JSON
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

        # 验证 JSON 格式
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

        通过 Ollama 的 streaming API 逐块返回生成的文本内容。

        Args:
            prompt: 用户输入的提示文本。
            system: 系统提示词。
            model: 覆盖默认模型名称。
            temperature: 采样温度（0.0 ~ 2.0）。
            top_p: 核采样概率阈值。
            max_tokens: 最大生成 token 数。
            **kwargs: 传递给 Ollama API 的额外参数。

        Yields:
            str: 每次生成的文本片段。

        Raises:
            TypeError: 当 prompt 参数类型不正确时抛出。
            ValueError: 当 prompt 为空字符串时抛出。
        """
        if not isinstance(prompt, str):
            raise TypeError(
                f"prompt 参数必须为字符串，实际传入类型为 {type(prompt).__name__}"
            )
        if not prompt.strip():
            raise ValueError("prompt 参数不能为空字符串")

        # 构建请求参数
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

        # 使用 Ollama streaming API
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

        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}]。
            model: 覆盖默认模型名称。
            temperature: 采样温度（0.0 ~ 2.0）。
            top_p: 核采样概率阈值。
            max_tokens: 最大生成 token 数。
            **kwargs: 传递给 Ollama API 的额外参数。

        Returns:
            str: 模型生成的回复内容。
        """
        if not isinstance(messages, list):
            raise TypeError("messages 参数必须为列表")

        # 构建请求参数
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

        # 调用 Ollama chat API
        response = self._client.chat(**request_params)

        # 返回消息内容
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

        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}]。
            model: 覆盖默认模型名称。
            temperature: 采样温度（0.0 ~ 2.0）。
            top_p: 核采样概率阈值。
            max_tokens: 最大生成 token 数。
            **kwargs: 传递给 Ollama API 的额外参数。

        Yields:
            str: 每次生成的文本片段。
        """
        if not isinstance(messages, list):
            raise TypeError("messages 参数必须为列表")

        # 构建请求参数
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

        # 使用 Ollama streaming chat API
        stream = self._client.chat(**request_params)

        for chunk in stream:
            message = chunk.get("message", {})
            if "content" in message:
                yield message["content"]


class AsyncOllamaOfficialClient:
    """
    Ollama 官方 SDK 异步客户端

    基于 ollama.AsyncClient 封装，提供异步接口用于调用 Ollama 本地模型。
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        host: Optional[str] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> None:
        """
        初始化 Ollama 异步客户端。

        Args:
            model: 默认使用的模型名称。
            host: Ollama 服务地址 (默认: http://localhost:11434)。
            timeout: 请求超时时间（秒）。
            **kwargs: 传递给 ollama.AsyncClient 的额外参数。
        """
        if not isinstance(model, str) or not model.strip():
            raise ValueError("model 参数必须为非空字符串")

        self._model = model.strip()
        self._host = host or DEFAULT_HOST

        # 构建 Ollama 客户端参数
        client_params: dict[str, Any] = {"host": self._host}
        if timeout is not None:
            client_params["timeout"] = timeout
        client_params.update(kwargs)

        # 初始化 Ollama SDK 异步客户端
        self._client = AsyncClient(**client_params)

    @property
    def model(self) -> str:
        """获取当前默认模型名称。"""
        return self._model

    @property
    def host(self) -> str:
        """获取当前 Ollama 服务地址。"""
        return self._host

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
