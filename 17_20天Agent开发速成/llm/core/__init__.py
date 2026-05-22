"""
LLM 统一接口层
为多个 LLM 提供者提供统一的接口，支持同步和异步调用
"""

__version__ = "1.0.0"

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
    register_async_provider,
    create_llm,
    create_async_llm,
    list_providers,
    list_async_providers
)

# 导出适配器
from .adapter import (
    BaseLLMAdapter,
    BaseAsyncLLMAdapter,
    RequestsLLMAdapter,
    AioHttpLLMAdapter,
    OpenAILLMAdapter,
    AnthropicLLMAdapter,
    OllamaLLMAdapter,
    SDKLLMAdapter
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
    MetricsHandler
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
    "register_async_provider",
    "create_llm",
    "create_async_llm",
    "list_providers",
    "list_async_providers",
    # 适配器
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
    "MetricsHandler"
]
