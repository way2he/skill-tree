# -*- coding: utf-8 -*-
"""
LLM 统一接口层 - 适配器基类

定义模型无关接口和向后兼容的旧适配器基类。

新版架构：
    - IProviderClient: 底层客户端协议
    - IAdapter: 适配器接口
    - UnifiedAdapter: 统一适配器实现

旧版（向后兼容）：
    - BaseLLMAdapter: 旧版同步适配器基类
    - BaseAsyncLLMAdapter: 旧版异步适配器基类
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, AsyncGenerator, Generator, Iterator, AsyncIterator, TypeVar, Protocol, runtime_checkable


# =============================================================================
# 类型定义
# =============================================================================

T = TypeVar('T')


@dataclass
class LLMResult:
    """
    通用 LLM 响应结构
    """
    content: str
    raw_response: Any = None
    model: str | None = None
    usage: dict | None = None
    finish_reason: str | None = None


@dataclass
class StreamChunk:
    """
    流式响应块
    """
    content: str
    is_final: bool = False
    usage: dict | None = None


# =============================================================================
# 底层客户端接口
# =============================================================================

@runtime_checkable
class IProviderClient(Protocol):
    """底层客户端协议"""
    @property
    def provider_name(self) -> str: ...
    @property
    def default_model(self) -> str: ...
    def generate(self, prompt: str, **kwargs) -> str: ...
    def generate_stream(self, prompt: str, **kwargs) -> Iterator[str]: ...
    async def agenerate(self, prompt: str, **kwargs) -> str: ...
    async def agenerate_stream(self, prompt: str, **kwargs) -> AsyncIterator[str]: ...


class IAdapter(ABC):
    """适配器接口"""
    def __init__(self, client: IProviderClient) -> None:
        self._client = client

    @property
    def provider_name(self) -> str:
        return self._client.provider_name

    @property
    def default_model(self) -> str:
        return self._client.default_model

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str: ...

    @abstractmethod
    async def agenerate(self, prompt: str, **kwargs) -> str: ...


# =============================================================================
# 事件发布
# =============================================================================

def publish_llm_event(
    event_type: str,
    provider: str,
    model: str | None,
    prompt: str | None = None,
    response: str | None = None,
    error: Exception | None = None,
    latency: float | None = None,
    request_id: str | None = None,
) -> None:
    """发布 LLM 事件到 EventBus"""
    try:
        from ..observer.event_bus import publish
        from ..observer.events import EventType, LLMEvent
        import uuid

        event_type_map = {
            "REQUEST_START": EventType.REQUEST_START,
            "REQUEST_SUCCESS": EventType.REQUEST_SUCCESS,
            "REQUEST_FAILURE": EventType.REQUEST_FAILURE,
        }
        event_enum = event_type_map.get(event_type, EventType.REQUEST_START)

        event = LLMEvent(
            event_type=event_enum,
            request_id=request_id or uuid.uuid4().hex,
            provider=provider,
            model=model,
            method="generate",
            prompt=prompt[:4096] if prompt else None,
            params={},
            response=response[:4096] if response else None,
            error=error,
            latency=latency,
        )
        publish(event)
    except ImportError:
        pass


# =============================================================================
# 向后兼容：旧的适配器基类
# =============================================================================

import functools
import time
import uuid

from ..exceptions import LLMError
from ..types import LLMResponse
from ..observer.event_bus import publish as _publish_event
from ..observer.events import EventType as _EventType, LLMEvent as _LLMEvent


_INSTRUMENTED_FLAG = "__llm_instrumented__"
_SYNC_METHODS = ("generate", "generate_json", "generate_stream")
_ASYNC_METHODS = ("generate", "generate_json", "generate_stream")


def _safe_str(value: Any, limit: int = 4096) -> str:
    """安全地将任意值转为字符串"""
    try:
        s = value if isinstance(value, str) else str(value)
    except Exception:
        return "<unrepr>"
    if len(s) > limit:
        return s[:limit] + f"...(+{len(s) - limit} chars)"
    return s


def _build_start_event(self: Any, method: str, prompt: Any, kwargs: dict) -> _LLMEvent:
    """构建 REQUEST_START 事件"""
    provider = getattr(self, "provider_name", None)
    model = kwargs.get("model") or getattr(self, "default_model", None)
    return _LLMEvent(
        event_type=_EventType.REQUEST_START,
        request_id=uuid.uuid4().hex,
        provider=provider,
        model=model,
        method=method,
        prompt=_safe_str(prompt) if prompt is not None else None,
        params={k: v for k, v in kwargs.items() if k != "prompt"},
    )


def _publish_success(start_event: _LLMEvent, response: Any, latency: float) -> None:
    """发布 REQUEST_SUCCESS"""
    _publish_event(_LLMEvent(
        event_type=_EventType.REQUEST_SUCCESS,
        request_id=start_event.request_id,
        provider=start_event.provider,
        model=start_event.model,
        backend=start_event.backend,
        method=start_event.method,
        prompt=start_event.prompt,
        params=start_event.params,
        response=_safe_str(response) if response is not None else None,
        latency=latency,
    ))


def _publish_failure(start_event: _LLMEvent, error: BaseException, latency: float) -> None:
    """发布 REQUEST_FAILURE"""
    _publish_event(_LLMEvent(
        event_type=_EventType.REQUEST_FAILURE,
        request_id=start_event.request_id,
        provider=start_event.provider,
        model=start_event.model,
        backend=start_event.backend,
        method=start_event.method,
        prompt=start_event.prompt,
        params=start_event.params,
        error=error if isinstance(error, Exception) else None,
        latency=latency,
    ))


def _instrument_sync_method(func: Any, method_name: str) -> Any:
    """同步方法包装器"""
    if method_name == "generate_stream":
        @functools.wraps(func)
        def stream_wrapper(self: Any, prompt: Any = None, *args: Any, **kwargs: Any) -> Generator[Any, None, None]:
            start = _build_start_event(self, method_name, prompt, kwargs)
            _publish_event(start)
            t0 = time.perf_counter()
            chunks: list[str] = []
            try:
                for chunk in func(self, prompt, *args, **kwargs):
                    try:
                        chunks.append(chunk if isinstance(chunk, str) else str(chunk))
                    except Exception:
                        pass
                    yield chunk
            except BaseException as e:
                latency = (time.perf_counter() - t0)
                _publish_failure(start, e, latency)
                raise
            else:
                latency = (time.perf_counter() - t0)
                _publish_success(start, "".join(chunks), latency)
        return stream_wrapper

    @functools.wraps(func)
    def wrapper(self: Any, prompt: Any = None, *args: Any, **kwargs: Any) -> Any:
        start = _build_start_event(self, method_name, prompt, kwargs)
        _publish_event(start)
        t0 = time.perf_counter()
        try:
            result = func(self, prompt, *args, **kwargs)
        except BaseException as e:
            latency = (time.perf_counter() - t0)
            _publish_failure(start, e, latency)
            raise
        else:
            latency = (time.perf_counter() - t0)
            _publish_success(start, result, latency)
            return result
    return wrapper


def _instrument_async_method(func: Any, method_name: str) -> Any:
    """异步方法包装器"""
    if method_name == "generate_stream":
        @functools.wraps(func)
        async def async_stream_wrapper(self: Any, prompt: Any = None, *args: Any, **kwargs: Any) -> AsyncGenerator[Any, None]:
            start = _build_start_event(self, method_name, prompt, kwargs)
            _publish_event(start)
            t0 = time.perf_counter()
            chunks: list[str] = []
            try:
                async for chunk in func(self, prompt, *args, **kwargs):
                    try:
                        chunks.append(chunk if isinstance(chunk, str) else str(chunk))
                    except Exception:
                        pass
                    yield chunk
            except BaseException as e:
                latency = (time.perf_counter() - t0)
                _publish_failure(start, e, latency)
                raise
            else:
                latency = (time.perf_counter() - t0)
                _publish_success(start, "".join(chunks), latency)
        return async_stream_wrapper

    @functools.wraps(func)
    async def async_wrapper(self: Any, prompt: Any = None, *args: Any, **kwargs: Any) -> Any:
        start = _build_start_event(self, method_name, prompt, kwargs)
        _publish_event(start)
        t0 = time.perf_counter()
        try:
            result = await func(self, prompt, *args, **kwargs)
        except BaseException as e:
            latency = (time.perf_counter() - t0)
            _publish_failure(start, e, latency)
            raise
        else:
            latency = (time.perf_counter() - t0)
            _publish_success(start, result, latency)
            return result
    return async_wrapper


def _instrument_subclass(cls: type, async_mode: bool) -> None:
    """为适配器子类自动包装 generate / generate_json / generate_stream"""
    method_names = _ASYNC_METHODS if async_mode else _SYNC_METHODS
    for name in method_names:
        func = cls.__dict__.get(name)
        if func is None:
            continue
        if getattr(func, _INSTRUMENTED_FLAG, False):
            continue
        if getattr(func, "__isabstractmethod__", False):
            continue
        wrapped = (
            _instrument_async_method(func, name)
            if async_mode
            else _instrument_sync_method(func, name)
        )
        setattr(wrapped, _INSTRUMENTED_FLAG, True)
        setattr(cls, name, wrapped)


class BaseLLMAdapter(ABC):
    """LLM 适配器基类（同步版本）- 向后兼容"""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        _instrument_subclass(cls, async_mode=False)

    def __init__(self, inner_client: Any):
        self._inner_client = inner_client

    @property
    @abstractmethod
    def provider_name(self) -> str: ...

    @property
    @abstractmethod
    def default_model(self) -> str: ...

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str: ...

    @abstractmethod
    def generate_json(self, prompt: str, schema: Any = None, **kwargs) -> str: ...

    def generate_with_response(self, prompt: str, **kwargs) -> LLMResponse:
        start_time = time.perf_counter()
        try:
            content = self.generate(prompt, **kwargs)
            latency = (time.perf_counter() - start_time)
            return LLMResponse(
                content=content,
                model=kwargs.get('model', self.default_model),
                provider=self.provider_name,
                latency=latency
            )
        except Exception as e:
            if isinstance(e, LLMError):
                raise
            raise LLMError(
                f"调用 {self.provider_name} 失败: {str(e)}",
                provider=self.provider_name,
                cause=e
            )

    def generate_stream(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        raise NotImplementedError(
            f"{self.provider_name} 适配器不支持流式生成"
        )


class BaseAsyncLLMAdapter(ABC):
    """LLM 适配器基类（异步版本）- 向后兼容"""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        _instrument_subclass(cls, async_mode=True)

    def __init__(self, inner_client: Any):
        self._inner_client = inner_client

    @property
    @abstractmethod
    def provider_name(self) -> str: ...

    @property
    @abstractmethod
    def default_model(self) -> str: ...

    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str: ...

    @abstractmethod
    async def generate_json(self, prompt: str, schema: Any = None, **kwargs) -> str: ...

    async def generate_with_response(self, prompt: str, **kwargs) -> LLMResponse:
        start_time = time.perf_counter()
        try:
            content = await self.generate(prompt, **kwargs)
            latency = (time.perf_counter() - start_time)
            return LLMResponse(
                content=content,
                model=kwargs.get('model', self.default_model),
                provider=self.provider_name,
                latency=latency
            )
        except Exception as e:
            if isinstance(e, LLMError):
                raise
            raise LLMError(
                f"调用 {self.provider_name} 失败: {str(e)}",
                provider=self.provider_name,
                cause=e
            )

    async def generate_stream(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        raise NotImplementedError(
            f"{self.provider_name} 适配器不支持流式生成"
        )
