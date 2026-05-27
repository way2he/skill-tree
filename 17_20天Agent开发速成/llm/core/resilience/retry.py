"""
LLM 统一接口层 - 重试机制
指数退避 + Jitter
"""

import time
import random
import functools
from dataclasses import dataclass
from typing import Callable, Any, Type, Tuple, Optional

from ..exceptions import (
    LLMError,
    LLMRateLimitError,
    LLMServerError,
    LLMTimeoutError
)
from ..logging_utils import get_logger

# 模块级日志器
_logger = get_logger("retry")


@dataclass
class RetryPolicy:
    """重试策略配置"""
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True
    retryable_exceptions: Tuple[Type[Exception], ...] = (
        LLMRateLimitError,
        LLMServerError,
        LLMTimeoutError,
        ConnectionError,
        TimeoutError
    )
    non_retryable_exceptions: Tuple[Type[Exception], ...] = ()


def calculate_delay(attempt: int, policy: RetryPolicy) -> float:
    """计算重试延迟
    
    使用指数退避 + Jitter
    
    Args:
        attempt: 当前尝试次数（从0开始）
        policy: 重试策略
        
    Returns:
        延迟时间（秒）
    """
    # 指数退避
    delay = policy.base_delay * (policy.exponential_base ** attempt)
    
    # Jitter：添加随机扰动
    if policy.jitter:
        jitter_amount = random.uniform(0, delay * 0.5)
        delay += jitter_amount
    
    # 限制最大延迟
    return min(delay, policy.max_delay)


def with_retry(
    policy: RetryPolicy = RetryPolicy(),
    on_retry: Optional[Callable[[int, Exception], None]] = None
):
    """重试装饰器（同步版本）
    
    Args:
        policy: 重试策略
        on_retry: 重试回调函数
        
    Returns:
        装饰器
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(policy.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    # 检查是否可重试
                    is_retryable = (
                        isinstance(e, policy.retryable_exceptions) and
                        not isinstance(e, policy.non_retryable_exceptions)
                    )

                    # 记录不可重试异常
                    if not is_retryable:
                        _logger.debug(
                            "不可重试异常，直接抛出: attempt=%d exception=%s: %s",
                            attempt, type(e).__name__, e,
                        )

                    if not is_retryable or attempt >= policy.max_retries:
                        # 记录最终重试失败
                        if attempt >= policy.max_retries:
                            _logger.error(
                                "重试耗尽: max_retries=%d last_exception=%s: %s",
                                policy.max_retries, type(e).__name__, e,
                            )
                        raise

                    # 计算延迟
                    delay = calculate_delay(attempt, policy)

                    # 记录重试发生
                    _logger.warning(
                        "开始重试: attempt=%d/%s delay=%.2fs exception=%s: %s",
                        attempt + 1, policy.max_retries, delay,
                        type(e).__name__, e,
                    )

                    # 调用回调
                    if on_retry:
                        on_retry(attempt, e)

                    # 等待
                    time.sleep(delay)

            # 如果到这里，说明所有重试都失败了
            if last_exception:
                raise last_exception
            raise LLMError("重试失败")

        return wrapper
    return decorator


def with_async_retry(
    policy: RetryPolicy = RetryPolicy(),
    on_retry: Optional[Callable[[int, Exception], Any]] = None
):
    """重试装饰器（异步版本）
    
    Args:
        policy: 重试策略
        on_retry: 重试回调函数（可以是异步的）
        
    Returns:
        装饰器
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            import asyncio
            last_exception = None
            
            for attempt in range(policy.max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    # 检查是否可重试
                    is_retryable = (
                        isinstance(e, policy.retryable_exceptions) and
                        not isinstance(e, policy.non_retryable_exceptions)
                    )

                    # 记录不可重试异常
                    if not is_retryable:
                        _logger.debug(
                            "不可重试异常，直接抛出: attempt=%d exception=%s: %s",
                            attempt, type(e).__name__, e,
                        )

                    if not is_retryable or attempt >= policy.max_retries:
                        # 记录最终重试失败
                        if attempt >= policy.max_retries:
                            _logger.error(
                                "重试耗尽: max_retries=%d last_exception=%s: %s",
                                policy.max_retries, type(e).__name__, e,
                            )
                        raise

                    # 计算延迟
                    delay = calculate_delay(attempt, policy)

                    # 记录重试发生
                    _logger.warning(
                        "开始重试: attempt=%d/%s delay=%.2fs exception=%s: %s",
                        attempt + 1, policy.max_retries, delay,
                        type(e).__name__, e,
                    )

                    # 调用回调
                    if on_retry:
                        result = on_retry(attempt, e)
                        if hasattr(result, '__await__'):
                            await result

                    # 等待
                    await asyncio.sleep(delay)
            
            # 如果到这里，说明所有重试都失败了
            if last_exception:
                raise last_exception
            raise LLMError("重试失败")
        
        return wrapper
    return decorator
