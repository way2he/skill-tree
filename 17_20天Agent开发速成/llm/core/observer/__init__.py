"""
LLM 统一接口层 - 观察者模块
提供事件总线、事件处理器、以及一行代码开关日志的便捷入口
"""

from .events import EventType, LLMEvent
from .event_bus import EventBus, subscribe, unsubscribe, publish
from .handlers import LoggingHandler, MetricsHandler, redact_params
from .logger import (
    enable_logging,
    disable_logging,
    is_logging_enabled,
    get_metrics_handler,
    DEFAULT_LOG_FORMAT,
    DEFAULT_DATE_FORMAT,
)

__all__ = [
    # 事件
    "EventType",
    "LLMEvent",
    # 总线
    "EventBus",
    "subscribe",
    "unsubscribe",
    "publish",
    # 处理器
    "LoggingHandler",
    "MetricsHandler",
    "redact_params",
    # 一键开关
    "enable_logging",
    "disable_logging",
    "is_logging_enabled",
    "get_metrics_handler",
    "DEFAULT_LOG_FORMAT",
    "DEFAULT_DATE_FORMAT",
]
