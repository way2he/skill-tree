# -*- coding: utf-8 -*-
"""
llm.anthropic.client - Anthropic Claude SDK 客户端

基于 Anthropic 官方 Python SDK (import anthropic) 封装的客户端。

Anthropic API 与 OpenAI 的关键差异：
1. max_tokens 是必填参数（默认 4096）
2. system 是顶层参数，不在 messages 数组中
3. 输出格式为 content 数组，需要通过 message.content[0].text 获取文本
4. 使用 anthropic.Anthropic 作为主客户端类

环境变量：
    ANTHROPIC_API_KEY: Anthropic API 密钥

默认模型：
    claude-sonnet-4-20250514
"""

import json
import os
from typing import Any, Generator

import anthropic


# Anthropic 默认模型
DEFAULT_MODEL: str = "claude-sonnet-4-20250514"

# Anthropic 默认最大 token 数（必填参数）
DEFAULT_MAX_TOKENS: int = 4096


class AnthropicClient:
    """
    Anthropic Claude SDK 客户端

    基于 anthropic 官方 Python SDK 封装，提供简洁的接口用于调用 Claude 模型。
    支持：
    - 普通文本生成 (generate)
    - JSON 结构化输出 (generate_json)
    - 流式文本生成 (generate_stream)
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = DEFAULT_MODEL,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        base_url: str | None = None,
        timeout: float | None = None,
        **kwargs,
    ) -> None:
        """
        初始化 Anthropic 客户端。

        Args:
            api_key: Anthropic API 密钥。若为 None，从环境变量 ANTHROPIC_API_KEY 读取。
            model: 默认使用的模型名称。
            max_tokens: 默认最大生成 token 数（Anthropic 必填参数）。
            base_url: 自定义 API 基础 URL（用于代理或私有部署）。
            timeout: 请求超时时间（秒）。
            **kwargs: 传递给 anthropic.Anthropic 的额外参数。
        """
        if not isinstance(model, str) or not model.strip():
            raise ValueError("model 参数必须为非空字符串")

        if not isinstance(max_tokens, int) or max_tokens <= 0:
            raise ValueError("max_tokens 参数必须为正整数")

        # 获取 API 密钥
        resolved_key = api_key or os.environ.get("ANTTHROPIC_API_KEY", "")
        if not resolved_key:
            raise ValueError(
                "未提供 API 密钥。请通过 api_key 参数传入，"
                "或设置环境变量 ANTHROPIC_API_KEY。"
            )

        self._model = model.strip()
        self._max_tokens = max_tokens

        # 构建 Anthropic 客户端参数
        client_params: dict[str, Any] = {"api_key": resolved_key}
        if base_url is not None:
            client_params["base_url"] = base_url
        if timeout is not None:
            client_params["timeout"] = timeout
        client_params.update(kwargs)

        # 初始化 Anthropic SDK 客户端
        self._client = anthropic.Anthropic(**client_params)

    @property
    def model(self) -> str:
        """获取当前默认模型名称。"""
        return self._model

    @property
    def max_tokens(self) -> int:
        """获取当前默认最大 token 数。"""
        return self._max_tokens

    def generate(
        self,
        prompt: str,
        system: str | None = None,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        stop_sequences: list[str] | None = None,
        **kwargs,
    ) -> str:
        """
        生成文本回复（非流式）。

        Args:
            prompt: 用户输入的提示文本。
            system: 系统提示词（Anthropic 顶层参数，不在 messages 中）。
            model: 覆盖默认模型名称。
            max_tokens: 覆盖默认最大 token 数。
            temperature: 采样温度（0.0 ~ 1.0）。
            top_p: 核采样概率阈值。
            stop_sequences: 停止序列列表。
            **kwargs: 传递给 Anthropic API 的额外参数。

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
            "max_tokens": max_tokens or self._max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }

        # Anthropic 的 system 是顶层参数
        if system is not None:
            if not isinstance(system, str):
                raise TypeError("system 参数必须为字符串")
            request_params["system"] = system

        # 可选参数
        if temperature is not None:
            request_params["temperature"] = temperature
        if top_p is not None:
            request_params["top_p"] = top_p
        if stop_sequences is not None:
            request_params["stop_sequences"] = stop_sequences

        request_params.update(kwargs)

        # 调用 Anthropic API
        message = self._client.messages.create(**request_params)

        # Anthropic 输出是 content 数组，取第一个 text block
        return message.content[0].text

    def generate_json(
        self,
        prompt: str,
        system: str | None = None,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float = 0.0,
        **kwargs,
    ) -> dict[str, Any]:
        """
        生成 JSON 结构化输出。

        通过在 system prompt 中指定 JSON 输出格式，并使用低温度采样，
        确保模型返回有效的 JSON 数据。

        Args:
            prompt: 用户输入的提示文本。
            system: 系统提示词。若提供，会在其后追加 JSON 格式要求。
            model: 覆盖默认模型名称。
            max_tokens: 覆盖默认最大 token 数。
            temperature: 采样温度，默认 0.0 以确保输出稳定性。
            **kwargs: 传递给 Anthropic API 的额外参数。

        Returns:
            dict[str, Any]: 解析后的 JSON 字典。

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
        final_system: str | None = None
        if system is not None:
            final_system = system + json_instruction
        else:
            final_system = "你是一个 JSON 数据生成助手。" + json_instruction

        # 调用 generate 获取文本
        raw_text = self.generate(
            prompt=prompt,
            system=final_system,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs,
        )

        # 尝试解析 JSON
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"模型输出不是有效的 JSON 格式。原始输出: {raw_text[:200]}"
            ) from e

    def generate_stream(
        self,
        prompt: str,
        system: str | None = None,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        **kwargs,
    ) -> Generator[str, None, None]:
        """
        流式生成文本回复。

        通过 Anthropic 的 streaming API 逐块返回生成的文本内容。

        Args:
            prompt: 用户输入的提示文本。
            system: 系统提示词（Anthropic 顶层参数）。
            model: 覆盖默认模型名称。
            max_tokens: 覆盖默认最大 token 数。
            temperature: 采样温度（0.0 ~ 1.0）。
            top_p: 核采样概率阈值。
            **kwargs: 传递给 Anthropic API 的额外参数。

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
            "max_tokens": max_tokens or self._max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }

        # Anthropic 的 system 是顶层参数
        if system is not None:
            if not isinstance(system, str):
                raise TypeError("system 参数必须为字符串")
            request_params["system"] = system

        # 可选参数
        if temperature is not None:
            request_params["temperature"] = temperature
        if top_p is not None:
            request_params["top_p"] = top_p

        request_params.update(kwargs)

        # 使用 Anthropic streaming API
        with self._client.messages.stream(**request_params) as stream:
            for text in stream.text_stream:
                yield text
