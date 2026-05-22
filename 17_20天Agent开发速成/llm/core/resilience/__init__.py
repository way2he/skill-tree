"""
LLM 统一接口层 - 弹性机制模块
提供重试、熔断、限流、降级等功能
"""

from .retry import (
    RetryPolicy,
    calculate_delay,
    with_retry,
    with_async_retry
)
from .circuit_breaker import (
    CircuitBreakerConfig,
    CircuitBreaker
)
from .rate_limiter import (
    RateLimiterConfig,
    TokenBucketRateLimiter
)
from .fallback import (
    FallbackStrategy,
    AsyncFallbackStrategy
)
from .decorator import (
    ResilienceConfig,
    resilient,
    async_resilient
)

__all__ = [
    # 重试
    "RetryPolicy",
    "calculate_delay",
    "with_retry",
    "with_async_retry",
    # 熔断
    "CircuitBreakerConfig",
    "CircuitBreaker",
    # 限流
    "RateLimiterConfig",
    "TokenBucketRateLimiter",
    # 降级
    "FallbackStrategy",
    "AsyncFallbackStrategy",
    # 装饰器
    "ResilienceConfig",
    "resilient",
    "async_resilient"
]
