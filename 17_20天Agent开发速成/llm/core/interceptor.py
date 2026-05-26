# -*- coding: utf-8 -*-
"""
LLM 统一接口层 - 拦截器模式

通过拦截器解耦横切关注点（日志、事件、指标等），
使 UnifiedAdapter 不直接依赖具体的事件发布逻辑。

拦截点:
    BEFORE_REQUEST - 请求前
    AFTER_SUCCESS  - 成功后
    AFTER_FAILURE  - 失败后

使用示例:
    from llm.core.interceptor import InterceptorChain, LoggingInterceptor, EventInterceptor

    chain = InterceptorChain()
    chain.add(LoggingInterceptor())
    chain.add(EventInterceptor())

    adapter = UnifiedAdapter(client, interceptor_chain=chain)
"""

import time
from abc import ABC, abstractmethod
from typing import Any, List, Optional

from .types import InterceptorPoint, InvocationContext


# =============================================================================
# 拦截器基类
# =============================================================================

class Interceptor(ABC):
    """
    拦截器基类

    所有拦截器都需要实现 intercept 方法。
    拦截器不应抛出异常，避免影响主流程。
    """

    @abstractmethod
    def intercept(
        self,
        point: InterceptorPoint,
        context: InvocationContext,
        result: Any = None,
        error: Optional[Exception] = None,
    ) -> None:
        """
        拦截处理

        Args:
            point: 拦截点
            context: 调用上下文
            result: 调用结果（AFTER_SUCCESS 时有值）
            error: 异常对象（AFTER_FAILURE 时有值）
        """
        ...


# =============================================================================
# 内置拦截器
# =============================================================================

class LoggingInterceptor(Interceptor):
    """
    日志拦截器

    在控制台输出请求的开始、成功、失败信息。
    """

    def intercept(
        self,
        point: InterceptorPoint,
        context: InvocationContext,
        result: Any = None,
        error: Optional[Exception] = None,
    ) -> None:
        """日志拦截"""
        try:
            if point == InterceptorPoint.BEFORE_REQUEST:
                print(
                    f"[{context.request_id[:8]}] "
                    f"{context.provider}/{context.model} "
                    f"- 请求开始: {context.prompt[:50]}..."
                )
            elif point == InterceptorPoint.AFTER_SUCCESS:
                latency = (time.perf_counter() - context.start_time) * 1000
                print(
                    f"[{context.request_id[:8]}] "
                    f"{context.provider}/{context.model} "
                    f"- 成功 ({latency:.0f}ms)"
                )
            elif point == InterceptorPoint.AFTER_FAILURE:
                latency = (time.perf_counter() - context.start_time) * 1000
                print(
                    f"[{context.request_id[:8]}] "
                    f"{context.provider}/{context.model} "
                    f"- 失败: {error} ({latency:.0f}ms)"
                )
        except Exception:
            # 拦截器不应影响主流程
            pass


class EventInterceptor(Interceptor):
    """
    事件发布拦截器

    将请求事件发布到 EventBus（复用现有 observer 模块）。
    """

    def intercept(
        self,
        point: InterceptorPoint,
        context: InvocationContext,
        result: Any = None,
        error: Optional[Exception] = None,
    ) -> None:
        """事件拦截"""
        try:
            from .adapter.base import publish_llm_event

            if point == InterceptorPoint.BEFORE_REQUEST:
                publish_llm_event(
                    event_type="REQUEST_START",
                    provider=context.provider,
                    model=context.model,
                    prompt=context.prompt,
                    request_id=context.request_id,
                )
            elif point == InterceptorPoint.AFTER_SUCCESS:
                latency = (time.perf_counter() - context.start_time) * 1000
                response_text = result if isinstance(result, str) else str(result)
                publish_llm_event(
                    event_type="REQUEST_SUCCESS",
                    provider=context.provider,
                    model=context.model,
                    response=response_text,
                    latency_ms=latency,
                    request_id=context.request_id,
                )
            elif point == InterceptorPoint.AFTER_FAILURE:
                latency = (time.perf_counter() - context.start_time) * 1000
                publish_llm_event(
                    event_type="REQUEST_FAILURE",
                    provider=context.provider,
                    model=context.model,
                    error=error,
                    latency_ms=latency,
                    request_id=context.request_id,
                )
        except Exception:
            # 拦截器不应影响主流程
            pass


class MetricsInterceptor(Interceptor):
    """
    指标拦截器

    收集请求延迟、成功率等指标。
    """

    def __init__(self) -> None:
        """初始化指标拦截器"""
        self._request_count: int = 0
        self._success_count: int = 0
        self._failure_count: int = 0
        self._total_latency_ms: float = 0.0

    def intercept(
        self,
        point: InterceptorPoint,
        context: InvocationContext,
        result: Any = None,
        error: Optional[Exception] = None,
    ) -> None:
        """指标拦截"""
        try:
            if point == InterceptorPoint.BEFORE_REQUEST:
                self._request_count += 1
            elif point == InterceptorPoint.AFTER_SUCCESS:
                latency = (time.perf_counter() - context.start_time) * 1000
                self._success_count += 1
                self._total_latency_ms += latency
            elif point == InterceptorPoint.AFTER_FAILURE:
                latency = (time.perf_counter() - context.start_time) * 1000
                self._failure_count += 1
                self._total_latency_ms += latency
        except Exception:
            pass

    @property
    def stats(self) -> dict[str, Any]:
        """
        获取统计信息

        Returns:
            包含请求数、成功率、平均延迟的字典
        """
        avg_latency = (
            self._total_latency_ms / self._request_count
            if self._request_count > 0
            else 0.0
        )
        success_rate = (
            self._success_count / self._request_count * 100
            if self._request_count > 0
            else 0.0
        )
        return {
            "request_count": self._request_count,
            "success_count": self._success_count,
            "failure_count": self._failure_count,
            "avg_latency_ms": round(avg_latency, 2),
            "success_rate": round(success_rate, 1),
        }

    def reset(self) -> None:
        """重置统计"""
        self._request_count = 0
        self._success_count = 0
        self._failure_count = 0
        self._total_latency_ms = 0.0


# =============================================================================
# 拦截器链
# =============================================================================

class InterceptorChain:
    """
    拦截器链

    管理多个拦截器，按添加顺序执行。

    使用示例:
        chain = InterceptorChain()
        chain.add(LoggingInterceptor())
        chain.add(EventInterceptor())

        # 执行
        chain.execute(InterceptorPoint.BEFORE_REQUEST, context)
    """

    def __init__(self) -> None:
        """初始化拦截器链"""
        self._interceptors: List[Interceptor] = []

    def add(self, interceptor: Interceptor) -> "InterceptorChain":
        """
        添加拦截器

        Args:
            interceptor: 拦截器实例

        Returns:
            self（支持链式调用）
        """
        if not isinstance(interceptor, Interceptor):
            raise TypeError(
                f"期望 Interceptor 类型， got {type(interceptor).__name__}"
            )
        self._interceptors.append(interceptor)
        return self

    def remove(self, interceptor_type: type) -> "InterceptorChain":
        """
        移除指定类型的拦截器

        Args:
            interceptor_type: 拦截器类型

        Returns:
            self（支持链式调用）
        """
        self._interceptors = [
            i for i in self._interceptors
            if not isinstance(i, interceptor_type)
        ]
        return self

    def execute(
        self,
        point: InterceptorPoint,
        context: InvocationContext,
        result: Any = None,
        error: Optional[Exception] = None,
    ) -> None:
        """
        执行拦截器链

        Args:
            point: 拦截点
            context: 调用上下文
            result: 调用结果
            error: 异常对象
        """
        for interceptor in self._interceptors:
            try:
                interceptor.intercept(point, context, result, error)
            except Exception:
                # 拦截器不应影响主流程
                pass

    @property
    def interceptors(self) -> List[Interceptor]:
        """获取所有拦截器"""
        return list(self._interceptors)

    def clear(self) -> None:
        """清空拦截器链"""
        self._interceptors.clear()


# =============================================================================
# 默认拦截器链工厂
# =============================================================================

def create_default_chain() -> InterceptorChain:
    """
    创建默认拦截器链

    包含 EventInterceptor（复用现有事件系统）。

    Returns:
        配置好默认拦截器的 InterceptorChain
    """
    chain = InterceptorChain()
    chain.add(EventInterceptor())
    return chain
