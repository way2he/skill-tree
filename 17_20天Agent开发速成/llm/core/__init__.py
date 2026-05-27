# -*- coding: utf-8 -*-
import warnings
"""
LLM 统一接口层

为多个 LLM 提供者提供统一的接口，支持同步和异步调用。

架构分层:
    ┌─────────────────────────────────────────┐
    │  用户代码 (create_llm)                  │
    └─────────────────┬───────────────────────┘
                      │
                      ▼
    ┌─────────────────────────────────────────┐
    │  UnifiedAdapter (core/adapter/)         │
    │  - 事件发布 (LoggingHandler)            │
    │  - 错误统一包装                         │
    │  - 参数透传                             │
    └─────────────────┬───────────────────────┘
                      │
                      ▼
    ┌─────────────────────────────────────────┐
    │  Provider (requests/providers/)        │
    │  - API 调用                             │
    │  - 响应解析                             │
    │  - 模型默认值                           │
    └─────────────────────────────────────────┘
"""

__version__ = "1.2.0"

# 导出异常
from .exceptions import (
    LLMError,
    LLMConnectionError,
    LLMAuthError,
    LLMRateLimitError,
    LLMServerError,
    LLMTimeoutError,
    LLMResponseError,
    LLMCircuitOpenError,
    LLMProviderNotFoundError,
    LLMConfigError
)

# 导出类型
from .types import (
    ProviderType,
    CircuitState,
    LLMRequest,
    LLMResponse,
    LLMProvider,
    AsyncLLMProvider,
    StreamableLLMProvider
)

# 导出配置
from .config import (
    load_config,
    create_llm_from_config,
    create_llm_async_from_config
)

# 导出工厂
from .factory import (
    register_provider,
    create_llm,
    list_providers
)

# 弃用警告：create_llm / create_client 请使用 get_llm
_warn_msg = "`{old}` 已弃用，请使用 `get_llm()` 作为统一入口"

# 兼容别名
def create_client(*args, **kwargs):
    """[已弃用] 请使用 get_llm()"""
    warnings.warn(_warn_msg.format(old="create_client"), DeprecationWarning, stacklevel=2)
    return get_llm(*args, **kwargs)

def create_async_client(*args, **kwargs):
    """[已弃用] 请使用 get_async_llm()"""
    warnings.warn(_warn_msg.format(old="create_async_client"), DeprecationWarning, stacklevel=2)
    return get_async_llm(*args, **kwargs)

# 导出默认实例工厂（调用方零参数获取 LLM）
from .default import (
    get_llm,
    get_async_llm,
    current_provider,
    resolve_provider,
    current_backend,
    resolve_provider_and_backend,
)

# 导出底层实现选择器（一键配置、Builder、Switcher）
from .backend import (
    # 枚举和类型
    BackendType,
    BackendLike,
    BackendConfig,
    # 一键配置 API
    set_default_backend,
    get_default_backend,
    reset_default_backend,
    resolve_backend,
    # Builder 模式
    LLMClientBuilder,
    # 便捷函数
    create_client,
    create_async_client,
    # 运行时切换
    BackendSwitcher,
)

# 导出厂商枚举（动态生成，避免硬编码字符串）
from .providers import ProviderName, ProviderLike

# 导出统一适配器（推荐使用）
from .adapter import (
    IProviderClient,
    IAdapter,
    LLMResult,
    StreamChunk,
    UnifiedAdapter,
)

# 导出适配器（向后兼容，已废弃）
from .adapter import (
    BaseLLMAdapter,
    BaseAsyncLLMAdapter,
    RequestsLLMAdapter,
    AioHttpLLMAdapter,
    OpenAILLMAdapter,
    AnthropicLLMAdapter,
    OllamaLLMAdapter,
    SDKLLMAdapter,
)

# 导出弹性机制
from .resilience import (
    # 重试
    RetryPolicy,
    calculate_delay,
    with_retry,
    with_async_retry,
    # 熔断
    CircuitBreakerConfig,
    CircuitBreaker,
    # 限流
    RateLimiterConfig,
    TokenBucketRateLimiter,
    # 降级
    FallbackStrategy,
    AsyncFallbackStrategy,
    # 装饰器
    ResilienceConfig,
    resilient,
    async_resilient
)

# 导出观察者
from .observer import (
    EventType,
    LLMEvent,
    EventBus,
    LoggingHandler,
    MetricsHandler,
    enable_logging,
    disable_logging,
    is_logging_enabled,
    get_metrics_handler,
    subscribe,
    unsubscribe,
    publish,
)

# 导出日志工具
from .logging_utils import get_logger
from .trace import new_trace_id, get_trace_id, set_trace_id, trace_context, TraceFilter

# 导出模型注册表（符合 MEMORY.md 规则）
from .model_registry import (
    ModelRegistry,
    ModelInfo,
    get_model_registry,
    validate_model,
    get_latest_model,
)

__all__ = [
    # 异常
    "LLMError",
    "LLMConnectionError",
    "LLMAuthError",
    "LLMRateLimitError",
    "LLMServerError",
    "LLMTimeoutError",
    "LLMResponseError",
    "LLMCircuitOpenError",
    "LLMProviderNotFoundError",
    "LLMConfigError",
    # 类型
    "ProviderType",
    "CircuitState",
    "LLMRequest",
    "LLMResponse",
    "LLMProvider",
    "AsyncLLMProvider",
    "StreamableLLMProvider",
    # 配置
    "load_config",
    "create_llm_from_config",
    "create_llm_async_from_config",
    # 工厂
    "register_provider",
    "create_llm",
    "list_providers",
    "get_llm",
    "get_async_llm",
    "current_provider",
    "resolve_provider",
    "current_backend",
    "resolve_provider_and_backend",
    "ProviderName",
    "ProviderLike",
    # 底层实现选择器
    "BackendType",
    "BackendLike",
    "BackendConfig",
    "set_default_backend",
    "get_default_backend",
    "reset_default_backend",
    "resolve_backend",
    "LLMClientBuilder",
    "create_client",
    "create_async_client",
    "BackendSwitcher",
    # 统一适配器（推荐使用）
    "IProviderClient",
    "IAdapter",
    "LLMResult",
    "StreamChunk",
    "UnifiedAdapter",
    # 适配器（向后兼容，已废弃）
    "BaseLLMAdapter",
    "BaseAsyncLLMAdapter",
    "RequestsLLMAdapter",
    "AioHttpLLMAdapter",
    "OpenAILLMAdapter",
    "AnthropicLLMAdapter",
    "OllamaLLMAdapter",
    "SDKLLMAdapter",
    # 弹性机制 - 重试
    "RetryPolicy",
    "calculate_delay",
    "with_retry",
    "with_async_retry",
    # 弹性机制 - 熔断
    "CircuitBreakerConfig",
    "CircuitBreaker",
    # 弹性机制 - 限流
    "RateLimiterConfig",
    "TokenBucketRateLimiter",
    # 弹性机制 - 降级
    "FallbackStrategy",
    "AsyncFallbackStrategy",
    # 弹性机制 - 装饰器
    "ResilienceConfig",
    "resilient",
    "async_resilient",
    # 观察者
    "EventType",
    "LLMEvent",
    "EventBus",
    "LoggingHandler",
    "MetricsHandler",
    "enable_logging",
    "disable_logging",
    "is_logging_enabled",
    "get_metrics_handler",
    "subscribe",
    "unsubscribe",
    "publish",
    # 日志工具
    "get_logger",
    "new_trace_id",
    "get_trace_id",
    "set_trace_id",
    "trace_context",
    "TraceFilter",
    # 模型注册表
    "ModelRegistry",
    "ModelInfo",
    "get_model_registry",
    "validate_model",
    "get_latest_model",
]
