"""
LLM 统一接口层 - 事件处理器
内置处理器：日志、指标采集
"""

import logging
import time
from typing import Dict, Any, Optional
from collections import defaultdict

from .events import EventType, LLMEvent


# 配置日志
logger = logging.getLogger(__name__)


class LoggingHandler:
    """日志处理器
    
    将事件记录到日志
    """
    
    def __init__(
        self,
        log_level: int = logging.INFO,
        log_prompt: bool = False
    ):
        """初始化日志处理器
        
        Args:
            log_level: 日志级别
            log_prompt: 是否记录提示词
        """
        self._log_level = log_level
        self._log_prompt = log_prompt
    
    def __call__(self, event: LLMEvent):
        """处理事件
        
        Args:
            event: 事件对象
        """
        # 构建日志消息
        message_parts = [f"[{event.event_type.value}"]
        
        if event.provider:
            message_parts.append(f"provider={event.provider}")
        
        if event.model:
            message_parts.append(f"model={event.model}")
        
        if event.latency_ms is not None:
            message_parts.append(f"latency={event.latency_ms:.2f}ms")
        
        if event.tokens_used is not None:
            message_parts.append(f"tokens={event.tokens_used}")
        
        if event.retry_attempt is not None:
            message_parts.append(f"retry={event.retry_attempt}")
        
        if event.circuit_state:
            message_parts.append(f"circuit={event.circuit_state}")
        
        if event.fallback_index is not None:
            message_parts.append(f"fallback={event.fallback_index}")
        
        if event.error:
            message_parts.append(f"error={type(event.error).__name__}: {event.error}")
        
        if self._log_prompt and event.prompt:
            # 截断过长的提示词
            truncated_prompt = event.prompt[:100]
            if len(event.prompt) > 100:
                truncated_prompt += "..."
            message_parts.append(f"prompt={repr(truncated_prompt)}")
        
        message = " ".join(message_parts)
        logger.log(self._log_level, message)


class MetricsHandler:
    """指标处理器
    
    采集和存储指标数据
    """
    
    def __init__(self):
        """初始化指标处理器"""
        self._request_count: int = 0
        self._success_count: int = 0
        self._failure_count: int = 0
        self._latencies: list = []
        self._provider_metrics: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {'count': 0, 'success': 0, 'failure': 0, 'latencies': []}
        )
        self._start_time = time.time()
    
    def __call__(self, event: LLMEvent):
        """处理事件
        
        Args:
            event: 事件对象
        """
        if event.event_type == EventType.REQUEST_START:
            self._request_count += 1
        
        elif event.event_type == EventType.REQUEST_SUCCESS:
            self._success_count += 1
            if event.latency_ms is not None:
                self._latencies.append(event.latency_ms)
            if event.provider:
                self._provider_metrics[event.provider]['count'] += 1
                self._provider_metrics[event.provider]['success'] += 1
                if event.latency_ms is not None:
                    self._provider_metrics[event.provider]['latencies'].append(event.latency_ms)
        
        elif event.event_type == EventType.REQUEST_FAILURE:
            self._failure_count += 1
            if event.provider:
                self._provider_metrics[event.provider]['count'] += 1
                self._provider_metrics[event.provider]['failure'] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """获取指标
        
        Returns:
            指标字典
        """
        total_time = time.time() - self._start_time
        
        # 计算平均延迟
        avg_latency = None
        if self._latencies:
            avg_latency = sum(self._latencies) / len(self._latencies)
        
        # 计算 QPS
        qps = None
        if total_time > 0:
            qps = self._request_count / total_time
        
        # 计算成功率
        success_rate = None
        if self._request_count > 0:
            success_rate = self._success_count / self._request_count
        
        # 提供者指标
        provider_metrics = {}
        for provider, data in self._provider_metrics.items():
            provider_avg_latency = None
            if data['latencies']:
                provider_avg_latency = sum(data['latencies']) / len(data['latencies'])
            provider_success_rate = None
            if data['count'] > 0:
                provider_success_rate = data['success'] / data['count']
            provider_metrics[provider] = {
                    'count': data['count'],
                    'success': data['success'],
                    'failure': data['failure'],
                    'avg_latency_ms': provider_avg_latency,
                    'success_rate': provider_success_rate
                }
        
        return {
            'total_requests': self._request_count,
            'success_count': self._success_count,
            'failure_count': self._failure_count,
            'avg_latency_ms': avg_latency,
            'qps': qps,
            'success_rate': success_rate,
            'uptime_seconds': total_time,
            'providers': provider_metrics
        }
    
    def reset(self):
        """重置指标"""
        self._request_count = 0
        self._success_count = 0
        self._failure_count = 0
        self._latencies = []
        self._provider_metrics.clear()
        self._start_time = time.time()
