"""
LLM 统一接口层 - 适配器基类
定义了同步和异步适配器的基础接口

本文件同时提供“子类方法自动插桩”能力：所有适配器的
``generate`` / ``generate_json`` / ``generate_stream`` 会被自动包装，
在调用前后向全局 EventBus 发布 ``REQUEST_START`` /
``REQUEST_SUCCESS`` / ``REQUEST_FAILURE`` 事件，以供 LoggingHandler
、MetricsHandler 等订阅者使用。
子类无需手动接入 logging。
"""

import functools
import inspect
import time
import uuid
from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Callable, Generator

from ..exceptions import LLMError
from ..types import LLMResponse
from ..observer.event_bus import publish as _publish_event
from ..observer.events import EventType as _EventType, LLMEvent as _LLMEvent


# =============================================================================
# 内部工具：适配器方法自动插桩
# =============================================================================

_INSTRUMENTED_FLAG = "__llm_instrumented__"
_SYNC_METHODS = ("generate", "generate_json", "generate_stream")
_ASYNC_METHODS = ("generate", "generate_json", "generate_stream")


def _safe_str(value: Any, limit: int = 4096) -> str:
    """安全地将任意值转为字符串，避免调用失败"""
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
    backend = getattr(self, "backend_name", None) or getattr(
        self.__class__, "_default_backend_name", None
    )
    return _LLMEvent(
        event_type=_EventType.REQUEST_START,
        request_id=uuid.uuid4().hex,
        provider=provider,
        model=model,
        backend=backend,
        method=method,
        prompt=_safe_str(prompt) if prompt is not None else None,
        params={k: v for k, v in kwargs.items() if k != "prompt"},
    )


def _publish_success(start_event: _LLMEvent, response: Any, latency_ms: float) -> None:
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
        latency_ms=latency_ms,
    ))


def _publish_failure(start_event: _LLMEvent, error: BaseException, latency_ms: float) -> None:
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
        latency_ms=latency_ms,
    ))


def _instrument_sync_method(func: Callable[..., Any], method_name: str) -> Callable[..., Any]:
    """同步方法包装器：发布 start / success / failure 事件"""
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
                latency = (time.perf_counter() - t0) * 1000
                _publish_failure(start, e, latency)
                raise
            else:
                latency = (time.perf_counter() - t0) * 1000
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
            latency = (time.perf_counter() - t0) * 1000
            _publish_failure(start, e, latency)
            raise
        else:
            latency = (time.perf_counter() - t0) * 1000
            _publish_success(start, result, latency)
            return result
    return wrapper


def _instrument_async_method(func: Callable[..., Any], method_name: str) -> Callable[..., Any]:
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
                latency = (time.perf_counter() - t0) * 1000
                _publish_failure(start, e, latency)
                raise
            else:
                latency = (time.perf_counter() - t0) * 1000
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
            latency = (time.perf_counter() - t0) * 1000
            _publish_failure(start, e, latency)
            raise
        else:
            latency = (time.perf_counter() - t0) * 1000
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
        # 跳过抽象方法（子类实现后才需要包装）
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
    """LLM 适配器基类（同步版本）
    
    所有同步适配器的基类，提供了通用的功能和接口

    子类的 ``generate`` / ``generate_json`` / ``generate_stream`` 会被
    自动插桩，在调用前后向 EventBus 发布事件（供 LoggingHandler /
    MetricsHandler 使用）。子类无需手动加日志。
    """

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        _instrument_subclass(cls, async_mode=False)
    
    def __init__(self, inner_client: Any):
        """初始化适配器
        
        Args:
            inner_client: 被适配的底层客户端实例
        """
        self._inner_client = inner_client
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """提供者名称（抽象属性）"""
        ...
    
    @property
    @abstractmethod
    def default_model(self) -> str:
        """默认模型名称（抽象属性）"""
        ...
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """生成文本（抽象方法）
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Returns:
            生成的文本
        """
        ...
    
    @abstractmethod
    def generate_json(self, prompt: str, schema: Any = None, **kwargs) -> str:
        """生成 JSON 格式的文本（抽象方法）
        
        Args:
            prompt: 输入提示词
            schema: JSON Schema（可选）
            **kwargs: 其他参数
            
        Returns:
            JSON 格式的字符串
        """
        ...
    
    def generate_with_response(self, prompt: str, **kwargs) -> LLMResponse:
        """生成文本并返回完整响应（模板方法）
        
        包含计时逻辑
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Returns:
            完整的 LLM 响应对象
        """
        start_time = time.perf_counter()
        
        try:
            content = self.generate(prompt, **kwargs)
            latency_ms = (time.perf_counter() - start_time) * 1000
            
            return LLMResponse(
                content=content,
                model=kwargs.get('model', self.default_model),
                provider=self.provider_name,
                latency_ms=latency_ms
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
        """流式生成文本（可选实现）
        
        默认抛出 NotImplementedError
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Yields:
            生成的文本片段
        """
        raise NotImplementedError(
            f"{self.provider_name} 适配器不支持流式生成"
        )


class BaseAsyncLLMAdapter(ABC):
    """LLM 适配器基类（异步版本）
    
    所有异步适配器的基类，提供了通用的功能和接口

    子类的 ``generate`` / ``generate_json`` / ``generate_stream`` 会被
    自动插桩，在调用前后向 EventBus 发布事件。
    """

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        _instrument_subclass(cls, async_mode=True)
    
    def __init__(self, inner_client: Any):
        """初始化适配器
        
        Args:
            inner_client: 被适配的底层客户端实例
        """
        self._inner_client = inner_client
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """提供者名称（抽象属性）"""
        ...
    
    @property
    @abstractmethod
    def default_model(self) -> str:
        """默认模型名称（抽象属性）"""
        ...
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """异步生成文本（抽象方法）
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Returns:
            生成的文本
        """
        ...
    
    @abstractmethod
    async def generate_json(self, prompt: str, schema: Any = None, **kwargs) -> str:
        """异步生成 JSON 格式的文本（抽象方法）
        
        Args:
            prompt: 输入提示词
            schema: JSON Schema（可选）
            **kwargs: 其他参数
            
        Returns:
            JSON 格式的字符串
        """
        ...
    
    async def generate_with_response(self, prompt: str, **kwargs) -> LLMResponse:
        """异步生成文本并返回完整响应（模板方法）
        
        包含计时逻辑
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Returns:
            完整的 LLM 响应对象
        """
        start_time = time.perf_counter()
        
        try:
            content = await self.generate(prompt, **kwargs)
            latency_ms = (time.perf_counter() - start_time) * 1000
            
            return LLMResponse(
                content=content,
                model=kwargs.get('model', self.default_model),
                provider=self.provider_name,
                latency_ms=latency_ms
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
        """异步流式生成文本（可选实现）
        
        默认抛出 NotImplementedError
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Yields:
            生成的文本片段
        """
        raise NotImplementedError(
            f"{self.provider_name} 适配器不支持流式生成"
        )
