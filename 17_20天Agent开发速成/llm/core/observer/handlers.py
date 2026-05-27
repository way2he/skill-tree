"""
LLM 统一接口层 - 事件处理器
内置处理器：日志、指标采集
"""

import logging
import re
import time
from collections import defaultdict
from typing import Any, Dict, Iterable, Optional

from .events import EventType, LLMEvent


# 模块级日志器
logger = logging.getLogger("llm")


# =============================================================================
# 敏感字段脱敏
# =============================================================================

# 默认需要脱敏的字段名（小写）
_DEFAULT_SENSITIVE_KEYS = (
    "api_key", "apikey", "secret", "secret_key", "sk", "access_key", "ak",
    "token", "authorization", "password", "passwd",
)


def _mask_value(value: Any) -> str:
    """
    脱敏单个值

    长字符串保留前 4 + 后 4 字符，中间用 *** 代替；短字符串整体 ***
    """
    if value is None:
        return ""
    s = str(value)
    if len(s) <= 8:
        return "***"
    return f"{s[:4]}***{s[-4:]}"


def redact_params(
    params: Optional[Dict[str, Any]],
    sensitive_keys: Iterable[str] = _DEFAULT_SENSITIVE_KEYS,
) -> Dict[str, Any]:
    """
    脱敏参数字典中的敏感字段

    Args:
        params: 原始参数字典
        sensitive_keys: 需要脱敏的字段名集合（不区分大小写）

    Returns:
        脱敏后的参数字典副本
    """
    if not params:
        return {}
    keys = {k.lower() for k in sensitive_keys}
    out: Dict[str, Any] = {}
    for k, v in params.items():
        if k.lower() in keys:
            out[k] = _mask_value(v)
        else:
            out[k] = v
    return out


def _truncate(text: Optional[str], limit: int) -> str:
    """截断文本到指定长度，超出部分用 ...(N more chars) 标记"""
    if not text:
        return ""
    if limit <= 0 or len(text) <= limit:
        return text
    return f"{text[:limit]}...(+{len(text) - limit} chars)"


# =============================================================================
# LoggingHandler
# =============================================================================

class LoggingHandler:
    """日志处理器

    把 LLMEvent 格式化后写入 Python logging 系统。

    支持：
    - 记录调用模型、渠道（provider）、底层实现（backend）、方法名
    - 记录入参（prompt + kwargs，敏感字段自动脱敏）
    - 记录出参（response 内容，自动截断）
    - 记录耗时、token 用量、错误信息
    - 记录请求追踪 ID（同一次调用的 start/success/failure 共用一个 request_id）
    """

    def __init__(
        self,
        log_level: int = logging.INFO,
        log_prompt: bool = True,
        log_response: bool = True,
        log_params: bool = True,
        prompt_max_chars: int = 500,
        response_max_chars: int = 500,
        sensitive_keys: Iterable[str] = _DEFAULT_SENSITIVE_KEYS,
        target_logger: Optional[logging.Logger] = None,
    ) -> None:
        """初始化日志处理器

        Args:
            log_level: 日志级别（默认 INFO）
            log_prompt: 是否记录入参 prompt
            log_response: 是否记录出参 response
            log_params: 是否记录调用 kwargs
            prompt_max_chars: prompt 截断长度（<=0 表示不截断）
            response_max_chars: response 截断长度（<=0 表示不截断）
            sensitive_keys: 敏感字段名（用于脱敏）
            target_logger: 目标 logger（默认使用 "llm" 模块 logger）
        """
        self._log_level = log_level
        self._log_prompt = log_prompt
        self._log_response = log_response
        self._log_params = log_params
        self._prompt_max = prompt_max_chars
        self._response_max = response_max_chars
        self._sensitive_keys = tuple(sensitive_keys)
        self._logger = target_logger or logger

    def __call__(self, event: LLMEvent) -> None:
        """处理事件"""
        parts: list[str] = [f"[{event.event_type.value}]"]

        # 添加 trace_id（如果存在）
        try:
            from ..trace import get_trace_id
            tid = get_trace_id()
            if tid:
                parts.append(f"trace={tid[:8]}")
        except ImportError:
            pass

        if event.request_id:
            parts.append(f"rid={event.request_id}")
        if event.provider:
            parts.append(f"provider={event.provider}")
        if event.model:
            parts.append(f"model={event.model}")
        if event.backend:
            parts.append(f"backend={event.backend}")
        if event.method:
            parts.append(f"method={event.method}")
        if event.latency_ms is not None:
            parts.append(f"latency={event.latency_ms:.2f}ms")
        if event.tokens_used is not None:
            parts.append(f"tokens={event.tokens_used}")
        if event.retry_attempt is not None:
            parts.append(f"retry={event.retry_attempt}")
        if event.circuit_state:
            parts.append(f"circuit={event.circuit_state}")
        if event.fallback_index is not None:
            parts.append(f"fallback={event.fallback_index}")

        # 入参：prompt
        if self._log_prompt and event.prompt:
            parts.append(f"prompt={_truncate(event.prompt, self._prompt_max)!r}")

        # 入参：kwargs（脱敏后）
        if self._log_params and event.params:
            safe_params = redact_params(event.params, self._sensitive_keys)
            parts.append(f"params={safe_params}")

        # 出参：response
        if self._log_response and event.response is not None:
            parts.append(
                f"response={_truncate(event.response, self._response_max)!r}"
            )

        # 错误
        if event.error is not None:
            parts.append(
                f"error={type(event.error).__name__}: {event.error}"
            )

        message = " ".join(parts)

        # 错误级别使用 ERROR
        if event.event_type == EventType.REQUEST_FAILURE:
            self._logger.error(message, exc_info=event.error is not None)
        else:
            self._logger.log(self._log_level, message)


# =============================================================================
# MetricsHandler
# =============================================================================

class MetricsHandler:
    """指标处理器

    采集和存储指标数据：请求数、成功/失败数、平均耗时、按 provider 维度的明细
    """

    def __init__(self) -> None:
        self._request_count: int = 0
        self._success_count: int = 0
        self._failure_count: int = 0
        self._latencies: list = []
        self._provider_metrics: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {'count': 0, 'success': 0, 'failure': 0, 'latencies': []}
        )
        self._start_time = time.time()

    def __call__(self, event: LLMEvent) -> None:
        if event.event_type == EventType.REQUEST_START:
            self._request_count += 1
            if event.provider:
                self._provider_metrics[event.provider]['count'] += 1

        elif event.event_type == EventType.REQUEST_SUCCESS:
            self._success_count += 1
            if event.latency_ms is not None:
                self._latencies.append(event.latency_ms)
            if event.provider:
                self._provider_metrics[event.provider]['success'] += 1
                if event.latency_ms is not None:
                    self._provider_metrics[event.provider]['latencies'].append(event.latency_ms)

        elif event.event_type == EventType.REQUEST_FAILURE:
            self._failure_count += 1
            if event.provider:
                self._provider_metrics[event.provider]['failure'] += 1

    def get_metrics(self) -> Dict[str, Any]:
        """获取累计指标"""
        total_time = time.time() - self._start_time

        avg_latency = (
            sum(self._latencies) / len(self._latencies)
            if self._latencies else None
        )
        qps = self._request_count / total_time if total_time > 0 else None
        success_rate = (
            self._success_count / self._request_count
            if self._request_count > 0 else None
        )

        provider_metrics: Dict[str, Any] = {}
        for provider, data in self._provider_metrics.items():
            provider_avg_latency = (
                sum(data['latencies']) / len(data['latencies'])
                if data['latencies'] else None
            )
            provider_success_rate = (
                data['success'] / data['count']
                if data['count'] > 0 else None
            )
            provider_metrics[provider] = {
                'count': data['count'],
                'success': data['success'],
                'failure': data['failure'],
                'avg_latency_ms': provider_avg_latency,
                'success_rate': provider_success_rate,
            }

        return {
            'total_requests': self._request_count,
            'success_count': self._success_count,
            'failure_count': self._failure_count,
            'avg_latency_ms': avg_latency,
            'qps': qps,
            'success_rate': success_rate,
            'uptime_seconds': total_time,
            'providers': provider_metrics,
        }

    def reset(self) -> None:
        """重置指标"""
        self._request_count = 0
        self._success_count = 0
        self._failure_count = 0
        self._latencies = []
        self._provider_metrics.clear()
        self._start_time = time.time()
