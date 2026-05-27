"""
LLM 统一接口层 - 熔断器
CLOSED/OPEN/HALF_OPEN 状态机
"""

import time
import threading
from dataclasses import dataclass
from typing import Optional, Callable

from ..types import CircuitState
from ..exceptions import LLMCircuitOpenError
from ..logging_utils import get_logger

# 模块级日志器
_logger = get_logger("circuit_breaker")


@dataclass
class CircuitBreakerConfig:
    """熔断器配置"""
    failure_threshold: int = 5
    recovery_timeout: float = 30.0
    half_open_max_calls: int = 3
    success_threshold: int = 2


class CircuitBreaker:
    """熔断器
    
    状态机：CLOSED -> OPEN -> HALF_OPEN -> CLOSED
    线程安全
    """
    
    def __init__(
        self,
        config: CircuitBreakerConfig = CircuitBreakerConfig(),
        name: str = "default",
        on_state_change: Optional[Callable[[CircuitState, CircuitState], None]] = None
    ):
        """初始化熔断器
        
        Args:
            config: 熔断器配置
            name: 熔断器名称
            on_state_change: 状态变化回调
        """
        self._config = config
        self._name = name
        self._on_state_change = on_state_change
        
        # 状态
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._opened_at: Optional[float] = None
        
        # 锁（线程安全）
        self._lock = threading.Lock()
    
    @property
    def state(self) -> CircuitState:
        """获取当前状态（自动检查半开转换）"""
        with self._lock:
            if self._state == CircuitState.OPEN:
                # 检查是否可以转换到半开状态
                if self._opened_at and time.time() - self._opened_at >= self._config.recovery_timeout:
                    old_state = self._state
                    self._state = CircuitState.HALF_OPEN
                    self._success_count = 0
                    _logger.warning(
                        "熔断器状态变更: name=%s %s -> %s (recovery_timeout=%.1fs reached)",
                        self._name, old_state.value, self._state.value,
                        self._config.recovery_timeout,
                    )
                    if self._on_state_change:
                        self._on_state_change(old_state, self._state)
            return self._state
    
    def allow_request(self) -> bool:
        """检查是否允许请求
        
        Returns:
            是否允许
        """
        current_state = self.state
        
        if current_state == CircuitState.CLOSED:
            return True
        elif current_state == CircuitState.HALF_OPEN:
            # 在半开状态，只允许有限次数的请求
            with self._lock:
                if self._success_count < self._config.half_open_max_calls:
                    return True
                return False
        else:  # OPEN
            _logger.warning(
                "请求被熔断拒绝: name=%s state=OPEN",
                self._name,
            )
            return False
    
    def record_success(self):
        """记录成功"""
        with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                self._success_count += 1
                # 检查是否可以关闭熔断器
                if self._success_count >= self._config.success_threshold:
                    old_state = self._state
                    self._state = CircuitState.CLOSED
                    self._failure_count = 0
                    self._success_count = 0
                    self._opened_at = None
                    _logger.info(
                        "熔断器状态变更: name=%s %s -> %s (探测成功, success_count=%d/%d)",
                        self._name, old_state.value, self._state.value,
                        self._success_count, self._config.success_threshold,
                    )
                    if self._on_state_change:
                        self._on_state_change(old_state, self._state)
            elif self._state == CircuitState.CLOSED:
                # 重置失败计数
                self._failure_count = 0
    
    def record_failure(self):
        """记录失败"""
        with self._lock:
            if self._state == CircuitState.CLOSED:
                self._failure_count += 1
                # 检查是否需要打开熔断器
                if self._failure_count >= self._config.failure_threshold:
                    old_state = self._state
                    self._state = CircuitState.OPEN
                    self._opened_at = time.time()
                    _logger.warning(
                        "熔断器状态变更: name=%s %s -> %s (failure_count=%d >= threshold=%d)",
                        self._name, old_state.value, self._state.value,
                        self._failure_count, self._config.failure_threshold,
                    )
                    if self._on_state_change:
                        self._on_state_change(old_state, self._state)
            elif self._state == CircuitState.HALF_OPEN:
                # 半开状态下失败，立即回到打开状态
                old_state = self._state
                self._state = CircuitState.OPEN
                self._opened_at = time.time()
                _logger.warning(
                    "熔断器状态变更: name=%s %s -> %s (半开探测失败)",
                    self._name, old_state.value, self._state.value,
                )
                if self._on_state_change:
                    self._on_state_change(old_state, self._state)
    
    def get_recovery_time(self) -> Optional[float]:
        """获取剩余恢复时间
        
        Returns:
            剩余恢复时间（秒），如果不是打开状态则返回 None
        """
        with self._lock:
            if self._state != CircuitState.OPEN or not self._opened_at:
                return None
            elapsed = time.time() - self._opened_at
            remaining = max(0.0, self._config.recovery_timeout - elapsed)
            return remaining
    
    def reset(self):
        """重置熔断器"""
        with self._lock:
            old_state = self._state
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._success_count = 0
            self._opened_at = None
            if self._on_state_change and old_state != self._state:
                self._on_state_change(old_state, self._state)
    
    def __call__(self, func):
        """装饰器：应用熔断器"""
        def wrapper(*args, **kwargs):
            if not self.allow_request():
                recovery_time = self.get_recovery_time()
                raise LLMCircuitOpenError(
                    f"熔断器已打开: {self._name}",
                    provider=self._name,
                    recovery_time=recovery_time
                )
            
            try:
                result = func(*args, **kwargs)
                self.record_success()
                return result
            except Exception:
                self.record_failure()
                raise
        
        return wrapper
