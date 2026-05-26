# -*- coding: utf-8 -*-
"""
LLM 统一接口层 - 类型定义（统一版）

集中定义所有 LLM 相关的类型、枚举、数据模型和 Protocol。
其他模块统一从此文件导入类型，避免分散定义。

变更说明:
    - 新增 StreamChunk 数据类
    - 新增 HTTPResponse / HTTPRequest 数据类（供 http_client 使用）
    - 新增 InvocationContext 数据类（供 interceptor 使用）
    - 新增 InterceptorPoint 枚举（供 interceptor 使用）
    - 新增 CacheConfig 数据类（供 cache 使用）
    - 新增 ResilienceOptions 数据类（供 unified_adapter 使用）
    - 保留所有旧类型，向后兼容
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import (
    Protocol,
    runtime_checkable,
    Optional,
    Dict,
    Any,
    Generator,
    AsyncGenerator,
    Iterator,
    AsyncIterator,
)


# =============================================================================
# 枚举类型
# =============================================================================

class ProviderType(str, Enum):
    """LLM 提供者类型枚举"""

    OPENAI = "openai"
    REQUESTS = "requests"
    AIOHTTP = "aiohttp"
    ANTHROPIC = "anthropic"
    BAIDU = "baidu"
    ALIBABA = "alibaba"
    ZHIPU = "zhipu"
    GOOGLE = "google"
    COHERE = "cohere"
    MISTRAL = "mistral"
    GROQ = "groq"
    VOLCENGINE = "volcengine"
    OLLAMA = "ollama"


class CircuitState(str, Enum):
    """熔断器状态枚举"""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class InterceptorPoint(str, Enum):
    """拦截点枚举"""

    BEFORE_REQUEST = "before_request"
    AFTER_SUCCESS = "after_success"
    AFTER_FAILURE = "after_failure"


# =============================================================================
# 数据模型 - LLM 请求/响应
# =============================================================================

@dataclass
class LLMRequest:
    """LLM 请求数据模型"""

    prompt: str
    system_prompt: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LLMResponse:
    """LLM 响应数据模型"""

    content: str
    model: Optional[str] = None
    provider: Optional[str] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    finish_reason: Optional[str] = None
    latency_ms: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StreamChunk:
    """
    流式响应块

    Attributes:
        content: 当前块的文本内容
        is_final: 是否为最后一个块
        usage: 当前块的 usage 信息
    """
    content: str
    is_final: bool = False
    usage: Optional[Dict[str, Any]] = None


# =============================================================================
# 数据模型 - HTTP 层
# =============================================================================

@dataclass
class HTTPRequest:
    """HTTP 请求数据模型"""

    method: str
    url: str
    headers: Dict[str, str] = field(default_factory=dict)
    json_body: Optional[Dict[str, Any]] = None
    timeout: Optional[float] = None
    stream: bool = False


@dataclass
class HTTPResponse:
    """
    HTTP 响应数据模型

    Attributes:
        status_code: HTTP 状态码
        headers: 响应头
        content: 原始字节内容
        text: 文本内容
    """
    status_code: int
    headers: Dict[str, str] = field(default_factory=dict)
    content: bytes = b""
    text: str = ""

    def json(self) -> Any:
        """解析 JSON 响应"""
        import json
        return json.loads(self.text)


# =============================================================================
# 数据模型 - 拦截器
# =============================================================================

@dataclass
class InvocationContext:
    """
    调用上下文

    Attributes:
        provider: 厂商名称
        model: 模型名称
        method: 调用方法名
        prompt: 输入提示词
        start_time: 开始时间
        request_id: 请求 ID
        kwargs: 其他参数
    """
    provider: str
    model: str
    method: str
    prompt: str
    start_time: float
    request_id: str
    kwargs: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# 数据模型 - 缓存
# =============================================================================

@dataclass
class CacheConfig:
    """
    缓存配置

    Attributes:
        enabled: 是否启用缓存
        ttl_seconds: 缓存过期时间（秒）
        max_size: 最大缓存条目数
        key_prefix: 缓存键前缀
    """
    enabled: bool = True
    ttl_seconds: int = 3600
    max_size: int = 1000
    key_prefix: str = "llm"


# =============================================================================
# 数据模型 - 弹性机制
# =============================================================================

@dataclass
class ResilienceOptions:
    """
    弹性配置选项

    Attributes:
        enable_circuit_breaker: 是否启用熔断器
        enable_rate_limiter: 是否启用限流器
        enable_retry: 是否启用重试
        circuit_breaker_failure_threshold: 熔断器失败阈值
        circuit_breaker_recovery_timeout: 熔断器恢复超时（秒）
        rate_limiter_rpm: 限流器每分钟请求数
        retry_max_retries: 最大重试次数
        retry_base_delay: 重试基础延迟（秒）
    """
    enable_circuit_breaker: bool = False
    enable_rate_limiter: bool = False
    enable_retry: bool = False
    circuit_breaker_failure_threshold: int = 5
    circuit_breaker_recovery_timeout: float = 30.0
    rate_limiter_rpm: int = 60
    retry_max_retries: int = 3
    retry_base_delay: float = 1.0


# =============================================================================
# Protocol 定义
# =============================================================================

@runtime_checkable
class LLMProvider(Protocol):
    """LLM 提供者 Protocol（同步版本）- 向后兼容"""

    @property
    def provider_name(self) -> str: ...

    @property
    def default_model(self) -> str: ...

    def generate(self, prompt: str, **kwargs) -> str: ...
    def generate_json(self, prompt: str, schema: Any = None, **kwargs) -> str: ...
    def generate_with_response(self, prompt: str, **kwargs) -> LLMResponse: ...
    def generate_stream(self, prompt: str, **kwargs) -> Generator[str, None, None]: ...


@runtime_checkable
class AsyncLLMProvider(Protocol):
    """LLM 提供者 Protocol（异步版本）- 向后兼容"""

    @property
    def provider_name(self) -> str: ...

    @property
    def default_model(self) -> str: ...

    async def generate(self, prompt: str, **kwargs) -> str: ...
    async def generate_json(self, prompt: str, schema: Any = None, **kwargs) -> str: ...
    async def generate_with_response(self, prompt: str, **kwargs) -> LLMResponse: ...
    async def generate_stream(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]: ...


@runtime_checkable
class StreamableLLMProvider(LLMProvider, Protocol):
    """可流式的 LLM 提供者 Protocol - 向后兼容"""

    def generate_stream(self, prompt: str, **kwargs) -> Generator[str, None, None]: ...
