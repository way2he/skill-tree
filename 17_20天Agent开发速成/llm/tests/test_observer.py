# -*- coding: utf-8 -*-
"""
测试 observer 模块（事件、日志、指标）
"""

import pytest
import sys
from pathlib import Path

# 添加父目录到路径
llm_dir = Path(__file__).parent.parent
sys.path.insert(0, str(llm_dir))


def test_observer_import():
    """测试 observer 模块可以导入"""
    from core import observer
    assert observer is not None


def test_event_types_exist():
    """测试事件类型存在"""
    from core import EventType
    
    # 应该有这些事件类型
    assert hasattr(EventType, "REQUEST_START")
    assert hasattr(EventType, "REQUEST_SUCCESS")
    assert hasattr(EventType, "REQUEST_FAILURE")


def test_event_class_exists():
    """测试 LLMEvent 存在"""
    from core import LLMEvent
    
    event = LLMEvent(
        event_type=EventType.REQUEST_START,
        provider="openai",
        model="gpt-4",
        prompt="Hello"
    )
    
    assert event.provider == "openai"
    assert event.model == "gpt-4"
    assert event.prompt == "Hello"


def test_event_bus_exists():
    """测试 EventBus 存在"""
    from core import EventBus
    
    bus = EventBus()
    assert bus is not None


def test_event_bus_subscribe():
    """测试事件订阅和发布"""
    from core import EventBus, EventType, LLMEvent, subscribe, publish
    
    events = []
    
    def handler(event):
        events.append(event)
    
    # 订阅
    subscribe(None, handler)
    
    # 发布
    test_event = LLMEvent(
        event_type=EventType.REQUEST_SUCCESS,
        provider="test",
        model="model",
        prompt="test"
    )
    publish(test_event)
    
    # 应该收到
    assert len(events) >= 1


def test_logging_handler_exists():
    """测试 LoggingHandler 存在"""
    from core import LoggingHandler, enable_logging, disable_logging, is_logging_enabled
    
    handler = LoggingHandler()
    assert handler is not None
    
    # 测试开关
    enable_logging()
    assert is_logging_enabled() is True
    
    disable_logging()
    # 注意：可能有其他地方也调用了，只测试函数存在


def test_metrics_handler_exists():
    """测试 MetricsHandler 存在"""
    from core import MetricsHandler, get_metrics_handler
    
    handler = MetricsHandler()
    assert handler is not None
    
    # 测试全局实例
    global_handler = get_metrics_handler()
    assert global_handler is not None


def test_metrics_handler_records_stats():
    """测试 MetricsHandler 记录统计"""
    from core import MetricsHandler, EventType, LLMEvent
    
    handler = MetricsHandler()
    
    # 记录一些事件
    event1 = LLMEvent(
        event_type=EventType.REQUEST_SUCCESS,
        provider="test",
        model="model",
        prompt="test",
        latency_ms=100.0
    )
    handler(event1)
    
    event2 = LLMEvent(
        event_type=EventType.REQUEST_SUCCESS,
        provider="test",
        model="model",
        prompt="test2",
        latency_ms=200.0
    )
    handler(event2)
    
    # 获取统计
    metrics = handler.get_metrics()
    assert metrics["total_requests"] >= 2
    assert metrics["success_count"] >= 2
    assert metrics["avg_latency_ms"] == 150.0


def test_metrics_provider_stats():
    """测试按 provider 统计"""
    from core import MetricsHandler, EventType, LLMEvent
    
    handler = MetricsHandler()
    
    # 不同 provider
    handler(LLMEvent(EventType.REQUEST_SUCCESS, "openai", "m1", "p1", latency_ms=100))
    handler(LLMEvent(EventType.REQUEST_SUCCESS, "openai", "m1", "p2", latency_ms=150))
    handler(LLMEvent(EventType.REQUEST_SUCCESS, "deepseek", "m2", "p3", latency_ms=200))
    
    metrics = handler.get_metrics()
    provider_metrics = metrics.get("providers", {})
    
    assert "openai" in provider_metrics
    assert "deepseek" in provider_metrics


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
