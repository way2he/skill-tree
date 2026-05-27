"""
LLM 统一接口层 - 限流器
令牌桶算法
"""

import time
import threading
from dataclasses import dataclass
from typing import Optional

from ..logging_utils import get_logger

# 模块级日志器
_logger = get_logger("rate_limiter")


@dataclass
class RateLimiterConfig:
    """限流器配置"""
    requests_per_minute: int = 60
    requests_per_second: Optional[int] = None
    burst_size: int = 10


class TokenBucketRateLimiter:
    """令牌桶限流器
    
    线程安全
    """
    
    def __init__(self, config: RateLimiterConfig = RateLimiterConfig()):
        """初始化令牌桶限流器
        
        Args:
            config: 限流器配置
        """
        self._config = config
        
        # 计算速率（令牌/秒）
        if config.requests_per_second:
            self._rate = config.requests_per_second
        else:
            self._rate = config.requests_per_minute / 60.0
        
        self._capacity = config.burst_size
        self._tokens = float(config.burst_size)
        self._last_refill = time.time()
        
        # 锁（线程安全）
        self._lock = threading.Lock()
        _logger.info(
            "限流器初始化: rate=%.2f req/s capacity=%d",
            self._rate, self._capacity,
        )
    
    def _refill(self):
        """补充令牌"""
        now = time.time()
        elapsed = now - self._last_refill
        
        # 计算应该补充的令牌数
        tokens_to_add = elapsed * self._rate
        self._tokens = min(self._capacity, self._tokens + tokens_to_add)
        self._last_refill = now
    
    def acquire(self, timeout: Optional[float] = None) -> bool:
        """获取令牌
        
        Args:
            timeout: 超时时间（秒），None 表示不等待
            
        Returns:
            是否成功获取
        """
        with self._lock:
            start_time = time.time()
            
            while True:
                self._refill()
                
                if self._tokens >= 1.0:
                    self._tokens -= 1.0
                    return True
                
                if timeout is None:
                    _logger.debug("限流拒绝: available_tokens=%.2f", self._tokens)
                    return False
                
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    return False
                
                # 计算需要等待的时间
                wait_time = (1.0 - self._tokens) / self._rate
                # 记录限流等待
                _logger.debug(
                    "限流等待: wait=%.3fs available_tokens=%.2f",
                    min(wait_time, timeout - elapsed),
                    self._tokens,
                )
                # 等待，但不超过剩余超时时间
                time.sleep(min(wait_time, timeout - elapsed))
    
    def try_acquire(self) -> bool:
        """尝试获取令牌（不等待）
        
        Returns:
            是否成功获取
        """
        return self.acquire(timeout=None)
    
    def reset(self):
        """重置限流器"""
        with self._lock:
            self._tokens = float(self._capacity)
            self._last_refill = time.time()
    
    @property
    def available_tokens(self) -> float:
        """获取当前可用令牌数"""
        with self._lock:
            self._refill()
            return self._tokens
    
    def __call__(self, func):
        """装饰器：应用限流器"""
        def wrapper(*args, **kwargs):
            if not self.acquire():
                # 这里可以抛出限流异常
                from ..exceptions import LLMRateLimitError
                raise LLMRateLimitError(
                    "请求被限流",
                    retry_after=1.0 / self._rate
                )
            return func(*args, **kwargs)
        
        return wrapper
