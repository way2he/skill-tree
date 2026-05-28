# -*- coding: utf-8 -*-
"""
LLM 统一适配器 - UnifiedAdapter（增强版）

集成 6 大优化:
    1. 拦截器模式 - 解耦事件发布、日志、指标
    2. 弹性机制 - 熔断、限流、重试开箱即用
    3. 缓存机制 - 减少重复 API 调用
    4. 连接池 - 通过 HTTP 客户端抽象支持
    5. 统一类型 - 使用 core/types 集中定义
    6. 向后兼容 - 旧接口完全保留

使用示例:
    # 基础用法（向后兼容）
    adapter = UnifiedAdapter(client)
    result = adapter.generate("Hello")

    # 带弹性机制
    from llm.core.types import ResilienceOptions
    opts = ResilienceOptions(
        enable_circuit_breaker=True,
        enable_retry=True,
    )
    adapter = UnifiedAdapter(client, resilience=opts)

    # 带缓存
    from llm.core.cache import LLMCache, CacheConfig
    cache = LLMCache(CacheConfig(ttl_seconds=1800))
    adapter = UnifiedAdapter(client, cache=cache)

    # 带自定义拦截器
    from llm.core.interceptor import InterceptorChain, LoggingInterceptor
    chain = InterceptorChain()
    chain.add(LoggingInterceptor())
    adapter = UnifiedAdapter(client, interceptor_chain=chain)
"""

import time
import uuid
from typing import Any, AsyncGenerator, Generator, Iterator, AsyncIterator, Optional

from .base import IProviderClient, LLMResult
from ..exceptions import LLMError, LLMRateLimitError, LLMCircuitOpenError
from ..types import (
    InterceptorPoint,
    InvocationContext,
    ResilienceOptions,
)


class UnifiedAdapter:
    """
    统一适配器（增强版）

    包装任意 IProviderClient 实现，提供：
    - 拦截器链（事件、日志、指标）
    - 弹性机制（熔断、限流、重试）
    - 缓存（减少重复调用）
    - 错误统一包装

    Attributes:
        provider_name: 厂商名称
        default_model: 默认模型
    """

    def __init__(
        self,
        client: IProviderClient,
        resilience: Optional[ResilienceOptions] = None,
        cache: Optional[Any] = None,
        interceptor_chain: Optional[Any] = None,
    ) -> None:
        """
        初始化统一适配器

        Args:
            client: 底层客户端（实现 IProviderClient 接口）
            resilience: 弹性配置选项（None 则不启用）
            cache: 缓存实例（None 则不启用）
            interceptor_chain: 拦截器链（None 则使用默认链）
        """
        self._client = client
        self._current_request_id: str | None = None

        # 弹性机制
        self._resilience = resilience or ResilienceOptions()
        self._circuit_breaker: Optional[Any] = None
        self._rate_limiter: Optional[Any] = None
        self._retry_policy: Optional[Any] = None
        self._init_resilience()

        # 缓存
        self._cache = cache

        # 拦截器链
        if interceptor_chain is not None:
            self._interceptor_chain = interceptor_chain
        else:
            from ..interceptor import create_default_chain
            self._interceptor_chain = create_default_chain()

    # =========================================================================
    # 属性
    # =========================================================================

    @property
    def provider_name(self) -> str:
        """厂商名称（委托给底层）"""
        return self._client.provider_name

    @property
    def default_model(self) -> str:
        """默认模型（委托给底层）"""
        return self._client.default_model

    # =========================================================================
    # 初始化弹性机制
    # =========================================================================

    def _init_resilience(self) -> None:
        """根据配置初始化弹性组件"""
        opts = self._resilience

        if opts.enable_circuit_breaker:
            try:
                from ..resilience import CircuitBreaker, CircuitBreakerConfig
                config = CircuitBreakerConfig(
                    failure_threshold=opts.circuit_breaker_failure_threshold,
                    recovery_timeout=opts.circuit_breaker_recovery_timeout,
                )
                self._circuit_breaker = CircuitBreaker(
                    config=config,
                    name=self._client.provider_name,
                )
            except ImportError:
                pass

        if opts.enable_rate_limiter:
            try:
                from ..resilience import RateLimiterConfig, TokenBucketRateLimiter
                config = RateLimiterConfig(
                    requests_per_minute=opts.rate_limiter_rpm,
                )
                self._rate_limiter = TokenBucketRateLimiter(config=config)
            except ImportError:
                pass

        if opts.enable_retry:
            try:
                from ..resilience import RetryPolicy
                self._retry_policy = RetryPolicy(
                    max_retries=opts.retry_max_retries,
                    base_delay=opts.retry_base_delay,
                )
            except ImportError:
                pass

    # =========================================================================
    # 弹性检查
    # =========================================================================

    def _check_rate_limit(self) -> None:
        """限流检查，超限抛出 LLMRateLimitError"""
        if self._rate_limiter is not None:
            if not self._rate_limiter.acquire(timeout=0):
                raise LLMRateLimitError(
                    f"请求被限流: {self.provider_name}",
                    provider=self.provider_name,
                )

    def _check_circuit_breaker(self) -> None:
        """熔断检查，熔断打开抛出 LLMCircuitOpenError"""
        if self._circuit_breaker is not None:
            if not self._circuit_breaker.allow_request():
                recovery_time = getattr(
                    self._circuit_breaker, "_opened_at", None
                )
                raise LLMCircuitOpenError(
                    f"熔断器已打开: {self.provider_name}",
                    provider=self.provider_name,
                    recovery_time=recovery_time,
                )

    def _record_success(self) -> None:
        """记录成功（熔断器状态更新）"""
        if self._circuit_breaker is not None:
            self._circuit_breaker.record_success()

    def _record_failure(self) -> None:
        """记录失败（熔断器状态更新）"""
        if self._circuit_breaker is not None:
            self._circuit_breaker.record_failure()

    # =========================================================================
    # 缓存
    # =========================================================================

    def _get_from_cache(
        self, prompt: str, model: str, kwargs: dict
    ) -> Optional[str]:
        """尝试从缓存获取"""
        if self._cache is None:
            return None
        if kwargs.get("stream"):
            return None
        if not kwargs.get("use_cache", True):
            return None
        return self._cache.get(self.provider_name, model, prompt, **kwargs)

    def _set_to_cache(
        self, prompt: str, model: str, value: str, kwargs: dict
    ) -> None:
        """写入缓存"""
        if self._cache is None:
            return
        if kwargs.get("stream"):
            return
        if not kwargs.get("use_cache", True):
            return
        self._cache.set(self.provider_name, model, prompt, value, **kwargs)

    # =========================================================================
    # 拦截器
    # =========================================================================

    def _build_context(
        self, prompt: str, model: str, method: str, kwargs: dict
    ) -> InvocationContext:
        """构建调用上下文"""
        # 获取底层客户端类型信息
        client_class = type(self._client)
        client_type = client_class.__name__
        
        # 从客户端获取 backend 信息（如果可用）
        backend = getattr(self._client, 'backend', None)
        
        # 如果没有显式设置 backend，从类名推断
        if backend is None:
            if 'aiohttp' in client_class.__module__.lower():
                backend = 'aiohttp'
            elif 'openai_sdk' in client_class.__module__.lower():
                backend = 'openai_sdk'
            elif 'native' in client_type.lower():
                backend = 'native_sdk'
            else:
                backend = 'requests'
        
        return InvocationContext(
            provider=self.provider_name,
            model=model,
            method=method,
            prompt=prompt,
            start_time=time.perf_counter(),
            request_id=self._current_request_id or uuid.uuid4().hex,
            kwargs=kwargs,
            backend=backend,
            client_type=client_type,
        )

    def _fire_before(self, context: InvocationContext) -> None:
        """触发 BEFORE_REQUEST 拦截器"""
        self._interceptor_chain.execute(
            InterceptorPoint.BEFORE_REQUEST, context
        )

    def _fire_success(self, context: InvocationContext, result: Any) -> None:
        """触发 AFTER_SUCCESS 拦截器"""
        self._interceptor_chain.execute(
            InterceptorPoint.AFTER_SUCCESS, context, result=result
        )

    def _fire_failure(self, context: InvocationContext, error: Exception) -> None:
        """触发 AFTER_FAILURE 拦截器"""
        self._interceptor_chain.execute(
            InterceptorPoint.AFTER_FAILURE, context, error=error
        )

    # =========================================================================
    # 同步方法
    # =========================================================================

    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        同步生成文本

        执行流程: 缓存 -> 限流 -> 熔断 -> 重试 -> 调用 -> 缓存写入

        Args:
            prompt: 输入提示词
            **kwargs: 透传给底层

        Returns:
            生成的文本
        """
        model = kwargs.get("model", self.default_model)
        self._current_request_id = uuid.uuid4().hex
        context = self._build_context(prompt, model, "generate", kwargs)

        # 缓存检查
        cached = self._get_from_cache(prompt, model, kwargs)
        if cached is not None:
            return cached

        # 弹性检查
        self._check_rate_limit()
        self._check_circuit_breaker()

        # 前置拦截
        self._fire_before(context)

        try:
            # 带重试的调用
            if self._retry_policy is not None:
                result = self._call_with_retry_sync(prompt, kwargs)
            else:
                result = self._client.generate(prompt, **kwargs)

            # 成功后处理
            self._record_success()
            self._fire_success(context, result)
            self._set_to_cache(prompt, model, result, kwargs)
            return result

        except Exception as e:
            self._record_failure()
            self._fire_failure(context, e)
            raise self._wrap_error(e)

    def _call_with_retry_sync(self, prompt: str, kwargs: dict) -> str:
        """同步带重试的调用"""
        from ..resilience import calculate_delay

        last_error: Exception | None = None
        for attempt in range(self._retry_policy.max_retries + 1):
            try:
                return self._client.generate(prompt, **kwargs)
            except Exception as e:
                last_error = e
                # 不可重试的异常直接抛出
                if not self._is_retryable(e):
                    raise
                if attempt < self._retry_policy.max_retries:
                    delay = calculate_delay(attempt, self._retry_policy)
                    time.sleep(delay)
        raise last_error  # type: ignore

    def generate_stream(self, prompt: str, **kwargs: Any) -> Generator[str, None, None]:
        """
        同步流式生成

        Args:
            prompt: 输入提示词
            **kwargs: 透传给底层

        Yields:
            生成的文本片段
        """
        model = kwargs.get("model", self.default_model)
        self._current_request_id = uuid.uuid4().hex
        context = self._build_context(prompt, model, "generate_stream", kwargs)

        self._check_rate_limit()
        self._check_circuit_breaker()
        self._fire_before(context)

        chunks: list[str] = []
        try:
            for chunk in self._client.generate_stream(prompt, **kwargs):
                if isinstance(chunk, str):
                    chunks.append(chunk)
                yield chunk

            self._record_success()
            self._fire_success(context, "".join(chunks))

        except Exception as e:
            self._record_failure()
            self._fire_failure(context, e)
            raise self._wrap_error(e)

    def generate_json(
        self,
        prompt: str,
        schema: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> str:
        """生成 JSON 格式的文本"""
        if schema is not None:
            kwargs["schema"] = schema
        if hasattr(self._client, "generate_json"):
            return self._client.generate_json(prompt, schema, **kwargs)
        return self.generate(prompt, **kwargs)

    def generate_with_response(self, prompt: str, **kwargs: Any) -> LLMResult:
        """生成文本并返回完整响应对象"""
        start_time = time.perf_counter()
        content = self.generate(prompt, **kwargs)
        latency = (time.perf_counter() - start_time)
        return LLMResult(
            content=content,
            model=kwargs.get("model", self.default_model),
            usage=None,
            finish_reason=None,
        )

    # =========================================================================
    # 异步方法
    # =========================================================================

    async def agenerate(self, prompt: str, **kwargs: Any) -> str:
        """
        异步生成文本

        执行流程: 缓存 -> 限流 -> 熔断 -> 重试 -> 调用 -> 缓存写入

        Args:
            prompt: 输入提示词
            **kwargs: 透传给底层

        Returns:
            生成的文本
        """
        model = kwargs.get("model", self.default_model)
        self._current_request_id = uuid.uuid4().hex
        context = self._build_context(prompt, model, "agenerate", kwargs)

        # 缓存检查
        cached = self._get_from_cache(prompt, model, kwargs)
        if cached is not None:
            return cached

        # 弹性检查
        self._check_rate_limit()
        self._check_circuit_breaker()

        # 前置拦截
        self._fire_before(context)

        try:
            if self._retry_policy is not None:
                result = await self._call_with_retry_async(prompt, kwargs)
            else:
                result = await self._client.agenerate(prompt, **kwargs)

            self._record_success()
            self._fire_success(context, result)
            self._set_to_cache(prompt, model, result, kwargs)
            return result

        except Exception as e:
            self._record_failure()
            self._fire_failure(context, e)
            raise self._wrap_error(e)

    async def _call_with_retry_async(self, prompt: str, kwargs: dict) -> str:
        """异步带重试的调用"""
        import asyncio
        from ..resilience import calculate_delay

        last_error: Exception | None = None
        for attempt in range(self._retry_policy.max_retries + 1):
            try:
                return await self._client.agenerate(prompt, **kwargs)
            except Exception as e:
                last_error = e
                if not self._is_retryable(e):
                    raise
                if attempt < self._retry_policy.max_retries:
                    delay = calculate_delay(attempt, self._retry_policy)
                    await asyncio.sleep(delay)
        raise last_error  # type: ignore

    async def agenerate_stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[str, None]:
        """异步流式生成"""
        model = kwargs.get("model", self.default_model)
        self._current_request_id = uuid.uuid4().hex
        context = self._build_context(prompt, model, "agenerate_stream", kwargs)

        self._check_rate_limit()
        self._check_circuit_breaker()
        self._fire_before(context)

        chunks: list[str] = []
        try:
            async for chunk in self._client.agenerate_stream(prompt, **kwargs):
                if isinstance(chunk, str):
                    chunks.append(chunk)
                yield chunk

            self._record_success()
            self._fire_success(context, "".join(chunks))

        except Exception as e:
            self._record_failure()
            self._fire_failure(context, e)
            raise self._wrap_error(e)

    async def agenerate_json(
        self,
        prompt: str,
        schema: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> str:
        """异步生成 JSON 格式的文本"""
        if schema is not None:
            kwargs["schema"] = schema
        if hasattr(self._client, "agenerate_json"):
            return await self._client.agenerate_json(prompt, schema, **kwargs)
        return await self.agenerate(prompt, **kwargs)

    async def agenerate_with_response(self, prompt: str, **kwargs: Any) -> LLMResult:
        """异步生成文本并返回完整响应对象"""
        start_time = time.perf_counter()
        content = await self.agenerate(prompt, **kwargs)
        latency = (time.perf_counter() - start_time)
        return LLMResult(
            content=content,
            model=kwargs.get("model", self.default_model),
            usage=None,
            finish_reason=None,
        )

    # =========================================================================
    # 工具方法
    # =========================================================================

    def _wrap_error(self, error: Exception) -> Exception:
        """统一包装错误"""
        if isinstance(error, LLMError):
            return error
        return LLMError(
            f"调用 {self.provider_name} 失败: {str(error)}",
            provider=self.provider_name,
            cause=error,
        )

    def _is_retryable(self, error: Exception) -> bool:
        """判断异常是否可重试"""
        if self._retry_policy is None:
            return False
        retryable = self._retry_policy.retryable_exceptions
        non_retryable = self._retry_policy.non_retryable_exceptions
        # 不可重试的异常优先判断
        if non_retryable and isinstance(error, non_retryable):
            return False
        return isinstance(error, retryable)
