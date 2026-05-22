"""
LLM 统一接口层 - 事件定义
事件类型和事件数据类
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Any, Dict
from datetime import datetime


class EventType(str, Enum):
    """事件类型"""
    REQUEST_START = "request_start"
    REQUEST_SUCCESS = "request_success"
    REQUEST_FAILURE = "request_failure"
    RETRY_ATTEMPT = "retry_attempt"
    CIRCUIT_STATE_CHANGE = "circuit_state_change"
    FALLBACK_TRIGGERED = "fallback_triggered"
    RATE_LIMIT_WAIT = "rate_limit_wait"


@dataclass
class LLMEvent:
    """LLM 事件"""
    event_type: EventType
    timestamp: datetime = field(default_factory=datetime.now)
    provider: Optional[str] = None
    model: Optional[str] = None
    prompt: Optional[str] = None
    latency_ms: Optional[float] = None
    tokens_used: Optional[int] = None
    error: Optional[Exception] = None
    retry_attempt: Optional[int] = None
    circuit_state: Optional[str] = None
    fallback_index: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
