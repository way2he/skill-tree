"""
LLM 统一接口层 - 事件总线
发布/订阅模式
"""

import threading
from typing import Dict, List, Callable, Optional, Any

from .events import EventType, LLMEvent
from ..logging_utils import get_logger

# 模块级日志器
_logger = get_logger("event_bus")


class EventBus:
    """事件总线
    
    线程安全的发布/订阅系统
    """
    
    def __init__(self):
        """初始化事件总线"""
        self._subscribers: Dict[EventType, List[Callable[[LLMEvent], Any]]] = {}
        self._all_subscribers: List[Callable[[LLMEvent], Any]] = []
        self._lock = threading.Lock()
    
    def subscribe(
        self,
        event_type: Optional[EventType],
        handler: Callable[[LLMEvent], Any]
    ):
        """订阅事件
        
        Args:
            event_type: 事件类型，None 表示订阅所有事件
            handler: 事件处理函数
        """
        with self._lock:
            if event_type is None:
                self._all_subscribers.append(handler)
                _logger.debug("订阅事件: event_type=%s handler=%s",
                             event_type.value if event_type else "*",
                             getattr(handler, '__name__', repr(handler)))
            else:
                if event_type not in self._subscribers:
                    self._subscribers[event_type] = []
                self._subscribers[event_type].append(handler)
                _logger.debug("订阅事件: event_type=%s handler=%s",
                             event_type.value if event_type else "*",
                             getattr(handler, '__name__', repr(handler)))
    
    def unsubscribe(
        self,
        event_type: Optional[EventType],
        handler: Callable[[LLMEvent], Any]
    ):
        """取消订阅
        
        Args:
            event_type: 事件类型，None 表示取消订阅所有事件
            handler: 事件处理函数
        """
        with self._lock:
            if event_type is None:
                if handler in self._all_subscribers:
                    self._all_subscribers.remove(handler)
                    _logger.debug("取消订阅: event_type=%s handler=%s",
                                 event_type.value if event_type else "*",
                                 getattr(handler, '__name__', repr(handler)))
            else:
                if event_type in self._subscribers:
                    if handler in self._subscribers[event_type]:
                        self._subscribers[event_type].remove(handler)
                        _logger.debug("取消订阅: event_type=%s handler=%s",
                                     event_type.value if event_type else "*",
                                     getattr(handler, '__name__', repr(handler)))
    
    def publish(self, event: LLMEvent):
        """发布事件
        
        Args:
            event: 事件对象
        """
        # 获取订阅者列表（在锁外调用）
        subscribers = []
        with self._lock:
            # 订阅特定事件的
            if event.event_type in self._subscribers:
                subscribers.extend(self._subscribers[event.event_type])
            # 订阅所有事件的
            subscribers.extend(self._all_subscribers)
        
        # 调用所有订阅者
        for handler in subscribers:
            try:
                handler(event)
            except Exception as exc:
                # 记录 handler 执行异常，不再静默吞掉
                _logger.error(
                    "事件处理器执行异常: handler=%s event_type=%s error=%s: %s",
                    getattr(handler, '__name__', repr(handler)),
                    event.event_type.value,
                    type(exc).__name__,
                    exc,
                    exc_info=True,
                )
    
    def clear(self):
        """清空所有订阅者"""
        with self._lock:
            self._subscribers.clear()
            self._all_subscribers.clear()


# 全局事件总线实例
_event_bus = EventBus()


# 便捷函数
def subscribe(
    event_type: Optional[EventType],
    handler: Callable[[LLMEvent], Any]
):
    """订阅事件（便捷函数）"""
    _event_bus.subscribe(event_type, handler)


def unsubscribe(
    event_type: Optional[EventType],
    handler: Callable[[LLMEvent], Any]
):
    """取消订阅（便捷函数）"""
    _event_bus.unsubscribe(event_type, handler)


def publish(event: LLMEvent):
    """发布事件（便捷函数）"""
    _event_bus.publish(event)
