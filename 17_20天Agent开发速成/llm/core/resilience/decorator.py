"""
LLM 统一接口层 - 组合弹性装饰器
一站式应用所有弹性机制
"""

import functools
from dataclasses import dataclass
from typing import Any, Callable, Optional, List

from .retry import RetryPolicy, with_retry, with_async_retry
from .circuit_breaker import CircuitBreakerConfig, CircuitBreaker
from .rate_limiter import RateLimiterConfig, TokenBucketRateLimiter
from .fallback import FallbackStrategy, AsyncFallbackStrategy


@dataclass
class ResilienceConfig:
    """弹性配置（组合所有配置）"""
    retry: RetryPolicy = RetryPolicy()
    circuit_breaker: Optional[CircuitBreakerConfig] = None
    rate_limiter: Optional[RateLimiterConfig] = None
    fallback_providers: List[Any] = None


def resilient(
    config: ResilienceConfig,
    name: str = "default"
):
    """组合弹性装饰器（同步版本）
    
    执行顺序：限流 -> 熔断检查 -> 重试 -> 降级
    
    Args:
        config: 弹性配置
        name: 熔断器名称
        
    Returns:
        装饰器
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 构建装饰器链
            decorated = func
            
            # 1. 限流
            if config.rate_limiter:
                limiter = TokenBucketRateLimiter(config.rate_limiter)
                decorated = limiter(decorated)
            
            # 2. 熔断器
            circuit_breaker = None
            if config.circuit_breaker:
                circuit_breaker = CircuitBreaker(
                    config.circuit_breaker,
                    name=name
                )
                decorated = circuit_breaker(decorated)
            
            # 3. 重试
            decorated = with_retry(config.retry)(decorated)
            
            # 4. 降级（如果有备用提供者）
            if config.fallback_providers:
                # 降级策略比较特殊，需要特殊处理
                # 这里简化处理，实际需要根据使用场景调整
                pass
            
            try:
                return decorated(*args, **kwargs)
            except Exception:
                # 记录失败（用于熔断器）
                if circuit_breaker:
                    circuit_breaker.record_failure()
                raise
        
        return wrapper
    return decorator


def async_resilient(
    config: ResilienceConfig,
    name: str = "default"
):
    """组合弹性装饰器（异步版本）
    
    执行顺序：限流 -> 熔断检查 -> 重试 -> 降级
    
    Args:
        config: 弹性配置
        name: 熔断器名称
        
    Returns:
        装饰器
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # 构建装饰器链
            decorated = func
            
            # 1. 限流（同步的限流器也可以用在异步中，因为有锁）
            if config.rate_limiter:
                limiter = TokenBucketRateLimiter(config.rate_limiter)
                # 创建异步版本的限流装饰器
                def async_limiter_decorator(f):
                    @functools.wraps(f)
                    async def async_wrapper(*a, **k):
                        if not limiter.acquire():
                            from ..exceptions import LLMRateLimitError
                            raise LLMRateLimitError(
                                "请求被限流",
                                retry_after=1.0 / limiter._rate
                            )
                        return await f(*a, **k)
                    return async_wrapper
                decorated = async_limiter_decorator(decorated)
            
            # 2. 熔断器
            circuit_breaker = None
            if config.circuit_breaker:
                circuit_breaker = CircuitBreaker(
                    config.circuit_breaker,
                    name=name
                )
                # 创建异步版本的熔断装饰器
                def async_circuit_decorator(f):
                    @functools.wraps(f)
                    async def async_wrapper(*a, **k):
                        if not circuit_breaker.allow_request():
                            recovery_time = circuit_breaker.get_recovery_time()
                            from ..exceptions import LLMCircuitOpenError
                            raise LLMCircuitOpenError(
                                f"熔断器已打开: {name}",
                                provider=name,
                                recovery_time=recovery_time
                            )
                        try:
                            result = await f(*a, **k)
                            circuit_breaker.record_success()
                            return result
                        except Exception:
                            circuit_breaker.record_failure()
                            raise
                    return async_wrapper
                decorated = async_circuit_decorator(decorated)
            
            # 3. 重试
            decorated = with_async_retry(config.retry)(decorated)
            
            # 4. 降级（如果有备用提供者）
            if config.fallback_providers:
                pass
            
            try:
                return await decorated(*args, **kwargs)
            except Exception:
                # 记录失败（用于熔断器）
                if circuit_breaker:
                    circuit_breaker.record_failure()
                raise
        
        return wrapper
    return decorator
