# -*- coding: utf-8 -*-
"""
通用 LLM 客户端模块
支持 Ollama、OpenAI、火山引擎(豆包)、Anthropic 多种协议
"""

import json
import os
from abc import ABC, abstractmethod
from typing import Any, Literal

import requests
from pydantic import BaseModel


class LLMResponse(BaseModel):
    """
    大模型响应数据结构

    Attributes:
        content: 模型返回的文本内容
        model: 使用的模型名称
        prompt_tokens: 输入提示词的 token 数量
        completion_tokens: 生成响应的 token 数量
        total_tokens: 总 token 数量
        finish_reason: 响应结束原因 (stop/tool_call/timeout等)
    """
    content: str
    model: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    finish_reason: str | None = None


class BaseLLMClient(ABC):
    """LLM 客户端抽象基类"""

    @abstractmethod
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        生成文本回复

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数
                - temperature: 温度参数，控制输出随机性
                  * 范围: 0.0 - 2.0（部分模型支持更大范围）
                  * 值越小越确定性（0.0-0.3），输出更保守、重复
                  * 值越大越随机（0.7-1.5），输出更多样、有创意
                  * 默认值: 0.7（平衡确定性和创造性）
                - max_tokens: 最大生成 token 数
                  * 限制单次响应的最大长度
                  * 不同模型有不同的上下文窗口限制
                  * 默认值: 根据模型而定，通常为 2048 或 4096
                - top_p: 核采样（Nucleus Sampling）概率阈值
                  * 范围: 0.0 - 1.0
                  * 控制从概率分布的前 P% token 中随机采样
                  * 0.1 表示只从概率最高的 10% token 中选择
                  * 1.0 表示考虑所有可能的 token
                  * 默认值: 1.0（不限制）
                - timeout: 请求超时时间（秒）
                  * 防止请求长时间阻塞
                  * 根据网络情况和模型响应速度调整
                  * 默认值: 60 秒

        Returns:
            模型生成的文本响应字符串
        """
        pass

    @abstractmethod
    def generate_json(self, prompt: str, schema: dict[str, Any] | None = None, **kwargs: Any) -> str:
        """
        生成 JSON 格式回复

        Args:
            prompt: 用户输入的提示词文本
            schema: 可选的 JSON Schema 字典，用于约束输出格式
                    示例: {"type": "object", "properties": {...}, "required": [...]}
            **kwargs: 可选参数
                - temperature: 温度参数，JSON生成时建议设为较低值 (默认0.3)
                - timeout: 请求超时时间（秒）

        Returns:
            符合指定 Schema 的 JSON 字符串
        """
        pass

    def generate_with_response(self, prompt: str, **kwargs: Any) -> LLMResponse:
        """
        生成文本回复并返回完整响应对象（包含 token 信息）

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数，同 generate 方法

        Returns:
            LLMResponse 对象，包含内容和元数据
        """
        content = self.generate(prompt, **kwargs)
        return LLMResponse(content=content, model=getattr(self, 'model', None))


class OllamaClient(BaseLLMClient):
    """
    Ollama 本地模型客户端
    API 文档: https://github.com/ollama/ollama/blob/main/docs/api.md

    使用示例:
        client = OllamaClient(model="qwen3.5:9b", base_url="http://localhost:11434")
        response = client.generate("你好，请介绍一下自己")

    Args:
        model: 模型名称，如 "qwen3.5:9b", "llama3.3:8b", "gemma2:9b"
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
        timeout: int = 120,
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
                - temperature: 温度参数，控制输出随机性
                  * 范围: 0.0 - 2.0
                  * 值越小越确定性（0.0-0.3），输出更保守、重复
                  * 值越大越随机（0.7-1.5），输出更多样、有创意
                  * 默认值: 0.7
                - max_tokens: 最大生成 token 数（Ollama 不强制限制）
                - timeout: 请求超时时间（秒）
                  * 默认值: 120 秒（本地模型响应较慢，设置较长超时）

        Returns:
            模型生成的文本响应字符串

        Raises:
            requests.exceptions.HTTPError: HTTP 请求失败时抛出
            json.JSONDecodeError: 响应解析失败时抛出
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

    def generate_json(self, prompt: str, schema: dict[str, Any] | None = None, **kwargs: Any) -> str:
        """
        生成 JSON 格式回复

        Args:
            prompt: 用户输入的提示词文本
            schema: 可选的 JSON Schema 字典，用于约束输出格式
                    示例: {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}
            **kwargs: 可选参数
                - timeout: 请求超时时间（秒），默认120秒

        Returns:
            符合指定 Schema 的 JSON 字符串

        Raises:
            requests.exceptions.HTTPError: HTTP 请求失败时抛出
            json.JSONDecodeError: 响应解析失败时抛出
            ValueError: 响应为空时抛出

        说明:
            - 使用 Ollama 的 format=json 参数强制 JSON 输出
            - temperature 固定为 0.3，确保输出稳定性
            - 如果已设置 system_prompt，不再重复添加 JSON 格式指令
        """
        # 如果已经有 system_prompt，直接使用，不重复添加 JSON 指令
        full_prompt = prompt

        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": full_prompt,
            "system": self.system_prompt,
            "temperature": 0.3,
            "format": "json",
            "stream": False,
        }
        print(f"[DEBUG] 请求 URL: {self.base_url}/api/generate")
        print(f"[DEBUG] 请求模型: {self.model}")

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()

        response_json = response.json()
        print(f"[DEBUG] 完整响应 JSON: {response_json}")

        # 优先从 response 字段获取，如果为空则尝试从 thinking 字段获取（某些模型如 qwen3.5 使用 thinking 机制）
        response_str = str(response_json.get("response", ""))
        
        if not response_str.strip() and "thinking" in response_json:
            print(f"[DEBUG] 响应字段为空，尝试从 thinking 字段获取")
            response_str = str(response_json.get("thinking", ""))
            
        print(f"[DEBUG] 提取的响应: {repr(response_str)}")

        if not response_str.strip():
            raise ValueError("Ollama 返回的响应为空，请检查：\n1. 模型是否已正确加载\n2. 系统提示词是否合理\n3. 模型版本是否支持 format=json 参数")

        return response_str


class OpenAIClient(BaseLLMClient):
    """
    OpenAI API 客户端 (兼容 Azure OpenAI)
    API 文档: https://platform.openai.com/docs/api-reference

    使用示例:
        # OpenAI
        client = OpenAIClient(api_key="sk-xxx", model="gpt-4o-mini")
        # Azure OpenAI
        client = OpenAIClient(api_key="xxx", model="gpt-4o-mini", base_url="https://xxx.openai.azure.com/openai/deployments/gpt-4o-mini")

    Args:
        api_key: OpenAI API 密钥，可通过环境变量 OPENAI_API_KEY 设置
        model: 模型名称，如 "gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"
        base_url: API 基础地址，默认 https://api.openai.com/v1
        system_prompt: 系统提示词，用于设置模型行为
        temperature: 温度参数，控制输出随机性 (0-2，默认0.7)
        timeout: 请求超时时间（秒），默认60秒
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-4o-mini",
        base_url: str = "https://api.openai.com/v1",
        system_prompt: str | None = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout

    def _build_messages(self, prompt: str) -> list[dict[str, str]]:
        """
        构建 OpenAI API 格式的消息列表

        Args:
            prompt: 用户提示词

        Returns:
            消息列表，格式: [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
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
                - temperature: 温度参数，控制输出随机性
                  * 范围: 0.0 - 2.0
                  * 值越小越确定性（0.0-0.3），适合需要精确回答的场景
                  * 值越大越随机（0.7-1.5），适合创意写作、头脑风暴
                  * 默认值: 0.7
                - max_tokens: 最大生成 token 数
                  * GPT-4o-mini 最大支持 128K token
                  * GPT-4 最大支持 8K/32K/128K（取决于模型版本）
                  * 默认值: 不限制（由模型决定）
                - top_p: 核采样概率阈值
                  * 范围: 0.0 - 1.0
                  * 与 temperature 配合使用，通常不同时调整两者
                  * 推荐值: 0.9（从概率最高的 90% token 中采样）
                  * 默认值: 1.0（不限制）
                - timeout: 请求超时时间（秒）
                  * 默认值: 60 秒

        Returns:
            模型生成的文本响应字符串

        Raises:
            requests.exceptions.HTTPError: HTTP 请求失败时抛出
            KeyError: 响应结构不符合预期时抛出
        """
        headers: dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": self._build_messages(prompt),
            "temperature": kwargs.get("temperature", self.temperature),
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        print("响应:", response.json())
        response.raise_for_status()
        # 解析 JSON 响应，提取 LLM 返回的内容
        # 响应结构: {"choices": [{"message": {"content": "..."}}]}
        return str(response.json()["choices"][0]["message"]["content"])

    def generate_json(self, prompt: str, schema: dict[str, Any] | None = None, **kwargs: Any) -> str:
        """
        生成 JSON 格式回复

        Args:
            prompt: 用户输入的提示词文本
            schema: 可选的 JSON Schema 字典，用于约束输出格式
                    示例: {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}
            **kwargs: 可选参数
                - timeout: 请求超时时间（秒），默认60秒

        Returns:
            符合指定 Schema 的 JSON 字符串

        Raises:
            requests.exceptions.HTTPError: HTTP 请求失败时抛出
            KeyError: 响应结构不符合预期时抛出

        说明:
            - 使用 OpenAI 的 response_format={"type": "json_object"} 参数强制 JSON 输出
            - temperature 固定为 0.3，确保输出稳定性
            - 若提供 schema，会在消息中添加格式约束指令
        """
        headers: dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = self._build_messages(prompt)

        if schema:
            schema_str = json.dumps(schema, ensure_ascii=False)
            messages.append(
                {
                    "role": "system",
                    "content": f"你是一个严格的 JSON 生成器。必须返回有效的 JSON，格式如下：{schema_str}。只输出 JSON，不要有任何解释。",
                }
            )

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.3,
            "response_format": {"type": "json_object"},
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        # 解析 JSON 响应，提取 LLM 返回的内容
        # 响应结构: {"choices": [{"message": {"content": "..."}}]}
        return str(response.json()["choices"][0]["message"]["content"])


class DoubaoClient(BaseLLMClient):
    """
    火山引擎豆包大模型客户端
    API 文档: https://www.volcengine.com/docs/82379/1263482

    使用示例:
        client = DoubaoClient(
            api_key="your-api-key",
            model="doubao-pro-32k",
            region="cn-beijing"
        )
        response = client.generate("你好，请介绍一下自己")

    Args:
        api_key: 火山引擎 API 密钥，可通过环境变量 VOLCENGINE_API_KEY 设置
        model: 模型名称，如 "doubao-pro-32k", "doubao-seed-2-0-code-preview-260215"
        region: 区域标识，支持 cn-beijing, cn-guangzhou, cn-shanghai, cn-hangzhou
        system_prompt: 系统提示词，用于设置模型行为
        temperature: 温度参数，控制输出随机性 (0-2，默认0.7)
        timeout: 请求超时时间（秒），默认60秒

    Attributes:
        SUPPORTED_REGIONS: 支持的区域映射字典
    """

    SUPPORTED_REGIONS = {
        "cn-beijing": "ark.cn-beijing.volces.com",
        "cn-guangzhou": "ark.cn-guangzhou.volces.com",
        "cn-shanghai": "ark.cn-shanghai.volces.com",
        "cn-hangzhou": "ark.cn-hangzhou.volces.com",
    }

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "doubao-seed-2-0-code-preview-260215",
        region: str = "cn-beijing",
        system_prompt: str | None = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("VOLCENGINE_API_KEY")
        self.model = model
        self.region = region
        self.base_url = f"https://{self.SUPPORTED_REGIONS.get(region, region)}/api/v3"
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout

    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        生成文本回复

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数
                - temperature: 温度参数，控制输出随机性
                  * 范围: 0.0 - 2.0
                  * 值越小越确定性（0.0-0.3），输出更精确、可预测
                  * 值越大越随机（0.7-1.5），输出更多样、有创意
                  * 默认值: 0.7
                - max_tokens: 最大生成 token 数
                  * doubao-pro-32k 支持 32K token 上下文
                  * 默认值: 不限制
                - timeout: 请求超时时间（秒）
                  * 默认值: 60 秒

        Returns:
            模型生成的文本响应字符串

        Raises:
            requests.exceptions.HTTPError: HTTP 请求失败时抛出
            KeyError: 响应结构不符合预期时抛出
        """
        headers: dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages: list[dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", self.temperature),
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        # 解析 JSON 响应，提取 LLM 返回的内容
        # 响应结构: {"choices": [{"message": {"content": "..."}}]}
        return str(response.json()["choices"][0]["message"]["content"])

    def generate_json(self, prompt: str, schema: dict[str, Any] | None = None, **kwargs: Any) -> str:
        """
        生成 JSON 格式回复

        Args:
            prompt: 用户输入的提示词文本
            schema: 可选的 JSON Schema 字典，用于约束输出格式
                    示例: {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}
            **kwargs: 可选参数
                - timeout: 请求超时时间（秒），默认60秒

        Returns:
            符合指定 Schema 的 JSON 字符串

        Raises:
            requests.exceptions.HTTPError: HTTP 请求失败时抛出
            KeyError: 响应结构不符合预期时抛出

        说明:
            - 使用 response_format={"type": "json_object"} 参数强制 JSON 输出
            - temperature 固定为 0.3，确保输出稳定性
        """
        headers: dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages: list[dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})

        if schema:
            schema_str = json.dumps(schema, ensure_ascii=False)
            messages.append(
                {
                    "role": "system",
                    "content": f"你是一个严格的 JSON 生成器。必须返回有效的 JSON，格式如下：{schema_str}。只输出 JSON，不要有任何解释。",
                }
            )

        messages.append({"role": "user", "content": prompt})

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.3,
            "response_format": {"type": "json_object"},
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        # 解析 JSON 响应，提取 LLM 返回的内容
        # 响应结构: {"choices": [{"message": {"content": "..."}}]}
        return str(response.json()["choices"][0]["message"]["content"])


class AnthropicClient(BaseLLMClient):
    """
    Anthropic Claude API 客户端
    API 文档: https://docs.anthropic.com/claude/reference/messages

    使用示例:
        client = AnthropicClient(
            api_key="sk-ant-xxx",
            model="claude-sonnet-4-20250514"
        )
        response = client.generate("你好，请介绍一下自己")

    Args:
        api_key: Anthropic API 密钥，可通过环境变量 ANTHROPIC_API_KEY 设置
        model: 模型名称，如 "claude-sonnet-4-20250514", "claude-3-5-sonnet"
        system_prompt: 系统提示词，用于设置模型行为
        temperature: 温度参数，控制输出随机性 (0-1，默认0.7)
        timeout: 请求超时时间（秒），默认60秒
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "claude-sonnet-4-20250514",
        system_prompt: str | None = None,
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout

    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        生成文本回复

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数
                - temperature: 温度参数，控制输出随机性（Anthropic 特有范围）
                  * 范围: 0.0 - 1.0（与其他模型不同，Claude 的温度范围是 0-1）
                  * 值越小越确定性（0.0-0.3），输出更精确、一致
                  * 值越大越随机（0.7-1.0），输出更多样、有创意
                  * 默认值: 0.7
                - max_tokens: 最大生成 token 数
                  * Claude 3.5 Sonnet 支持 200K token 上下文
                  * 默认值: 4096（平衡响应速度和完整性）
                - timeout: 请求超时时间（秒）
                  * 默认值: 60 秒

        Returns:
            模型生成的文本响应字符串

        Raises:
            requests.exceptions.HTTPError: HTTP 请求失败时抛出
            KeyError: 响应结构不符合预期时抛出
        """
        headers: dict[str, str] = {
            "x-api-key": self.api_key or "",
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        payload: dict[str, Any] = {
            "model": self.model,
            "max_tokens": kwargs.get("max_tokens", 4096),
            "temperature": kwargs.get("temperature", self.temperature),
            "system": self.system_prompt or "",
            "messages": [{"role": "user", "content": prompt}],
        }

        response = requests.post(
            self.base_url,
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        return str(response.json()["content"][0]["text"])

    def generate_json(self, prompt: str, schema: dict[str, Any] | None = None, **kwargs: Any) -> str:
        """
        生成 JSON 格式回复

        Args:
            prompt: 用户输入的提示词文本
            schema: 可选的 JSON Schema 字典，用于约束输出格式
                    示例: {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}
            **kwargs: 可选参数
                - max_tokens: 最大生成 token 数，默认4096
                - timeout: 请求超时时间（秒），默认60秒

        Returns:
            符合指定 Schema 的 JSON 字符串

        Raises:
            requests.exceptions.HTTPError: HTTP 请求失败时抛出
            KeyError: 响应结构不符合预期时抛出

        说明:
            - Anthropic Claude 原生支持 JSON 格式输出
            - temperature 固定为 0.3，确保输出稳定性
            - JSON 格式指令追加到 system prompt 中
        """
        headers: dict[str, str] = {
            "x-api-key": self.api_key or "",
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        if schema:
            schema_str = json.dumps(schema, ensure_ascii=False)
            json_instruction = (
                f"\n\n你是一个严格的 JSON 生成器。必须返回有效的 JSON，"
                f"格式如下：{schema_str}。只输出 JSON，不要有任何解释。"
            )
        else:
            json_instruction = "\n\n请以有效的 JSON 格式输出响应。"

        payload: dict[str, Any] = {
            "model": self.model,
            "max_tokens": kwargs.get("max_tokens", 4096),
            "temperature": 0.3,
            "system": (self.system_prompt or "") + json_instruction,
            "messages": [{"role": "user", "content": prompt}],
        }

        response = requests.post(
            self.base_url,
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", self.timeout),
        )
        response.raise_for_status()
        return str(response.json()["content"][0]["text"])


def create_llm_client(
    provider: Literal["ollama", "openai", "doubao", "anthropic"],
    **kwargs: Any,
) -> BaseLLMClient:
    """
    创建 LLM 客户端工厂函数

    Args:
        provider: 提供商类型
            - "ollama": 本地 Ollama 模型
            - "openai": OpenAI / Azure OpenAI
            - "doubao": 火山引擎豆包
            - "anthropic": Anthropic Claude

    Returns:
        对应的 LLM 客户端实例
    """
    clients: dict[str, type[BaseLLMClient]] = {
        "ollama": OllamaClient,
        "openai": OpenAIClient,
        "doubao": DoubaoClient,
        "anthropic": AnthropicClient,
    }

    if provider not in clients:
        raise ValueError(
            f"不支持的 provider: {provider}，支持的选项: {list(clients.keys())}"
        )

    return clients[provider](**kwargs)


def llm_generate(
    prompt: str,
    provider: Literal["ollama", "openai", "doubao", "anthropic"] = "ollama",
    **kwargs: Any,
) -> str:
    """
    统一的 LLM 生成接口（便捷函数）

    Args:
        prompt: 用户提示词
        provider: 提供商类型
        **kwargs: 传递给客户端的其他参数

    Returns:
        模型生成的文本
    """
    client = create_llm_client(provider, **kwargs)
    return client.generate(prompt)


def llm_generate_json(
    prompt: str,
    schema: dict[str, Any] | None = None,
    provider: Literal["ollama", "openai", "doubao", "anthropic"] = "ollama",
    **kwargs: Any,
) -> str:
    """
    统一的 JSON 生成接口

    Args:
        prompt: 用户提示词
        schema: JSON Schema
        provider: 提供商类型
        **kwargs: 传递给客户端的其他参数

    Returns:
        模型生成的 JSON 字符串
    """
    client = create_llm_client(provider, **kwargs)
    return client.generate_json(prompt, schema)


def load_env_config(prefix: str = "LLM_") -> dict[str, str | None]:
    """
    从环境变量加载 LLM 配置

    支持的环境变量:
        - LLM_PROVIDER: 提供商类型 (ollama/openai/doubao/anthropic)
        - LLM_MODEL: 模型名称
        - LLM_API_KEY: API 密钥
        - LLM_BASE_URL: API 端点
        - LLM_REGION: 区域
        - LLM_SYSTEM_PROMPT: 系统提示词
    """
    return {
        "provider": os.getenv(f"{prefix}PROVIDER", "ollama"),
        "model": os.getenv(f"{prefix}MODEL"),
        "api_key": os.getenv(f"{prefix}API_KEY"),
        "base_url": os.getenv(f"{prefix}BASE_URL"),
        "region": os.getenv(f"{prefix}REGION"),
        "system_prompt": os.getenv(f"{prefix}SYSTEM_PROMPT"),
    }
