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
    REQUEST_STREAM_CHUNK = "request_stream_chunk"
    RETRY_ATTEMPT = "retry_attempt"
    CIRCUIT_STATE_CHANGE = "circuit_state_change"
    FALLBACK_TRIGGERED = "fallback_triggered"
    RATE_LIMIT_WAIT = "rate_limit_wait"


@dataclass
class LLMEvent:
    """LLM 事件

    用于在 EventBus 中传递的统一事件载体。包含：
    - 调用元信息：provider（渠道）/ model（模型）/ backend（底层实现）/ method（方法）
    - 入参：prompt（提示词）/ params（kwargs 快照，已脱敏）
    - 出参：response（生成结果）/ tokens_used / latency_ms
    - 追踪：request_id（贯穿同一次调用的开始/结束事件）
    """
    event_type: EventType
    timestamp: datetime = field(default_factory=datetime.now)
    request_id: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    backend: Optional[str] = None
    method: Optional[str] = None
    prompt: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    response: Optional[str] = None
    latency_ms: Optional[float] = None
    tokens_used: Optional[int] = None
    error: Optional[Exception] = None
    retry_attempt: Optional[int] = None
    circuit_state: Optional[str] = None
    fallback_index: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
