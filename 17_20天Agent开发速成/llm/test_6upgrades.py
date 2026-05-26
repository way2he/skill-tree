# -*- coding: utf-8 -*-
"""
LLM 架构 6 大优化验证测试

验证:
    1. 统一类型定义 (types.py)
    2. HTTP 客户端抽象 + 连接池 (http_client.py)
    3. 拦截器模式 (interceptor.py)
    4. 缓存机制 (cache.py)
    5. 弹性机制集成 (unified_adapter.py)
    6. 向后兼容
"""

import asyncio
from typing import AsyncIterator, Iterator


# =============================================================================
# Mock Provider
# =============================================================================

class MockProvider:
    """Mock Provider"""

    PROVIDER_NAME = "mock"
    DEFAULT_MODEL = "mock-v1"
    call_count: int = 0

    @property
    def provider_name(self) -> str:
        return self.PROVIDER_NAME

    @property
    def default_model(self) -> str:
        return self.DEFAULT_MODEL

    def generate(self, prompt: str, **kwargs) -> str:
        self.call_count += 1
        return f"Response to: {prompt}"

    def generate_stream(self, prompt: str, **kwargs) -> Iterator[str]:
        self.call_count += 1
        yield "chunk1"
        yield "chunk2"

    async def agenerate(self, prompt: str, **kwargs) -> str:
        self.call_count += 1
        return f"Async response to: {prompt}"

    async def agenerate_stream(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        self.call_count += 1
        yield "achunk1"
        yield "achunk2"


# =============================================================================
# 测试 1: 统一类型定义
# =============================================================================

def test_types():
    """验证统一类型定义"""
    print("1. 统一类型定义...")

    from llm.core.types import (
        ProviderType, CircuitState, InterceptorPoint,
        LLMRequest, LLMResponse, StreamChunk,
        HTTPRequest, HTTPResponse,
        InvocationContext, CacheConfig, ResilienceOptions,
        LLMProvider, AsyncLLMProvider, StreamableLLMProvider,
    )

    # 枚举
    assert ProviderType.OPENAI.value == "openai"
    assert CircuitState.CLOSED.value == "closed"
    assert InterceptorPoint.BEFORE_REQUEST.value == "before_request"

    # 数据类
    req = LLMRequest(prompt="Hello", model="gpt-4")
    assert req.prompt == "Hello"

    resp = LLMResponse(content="Hi", model="gpt-4", latency_ms=100.0)
    assert resp.content == "Hi"

    chunk = StreamChunk(content="hello", is_final=True)
    assert chunk.is_final is True

    http_req = HTTPRequest(method="POST", url="https://api.openai.com/v1/chat/completions")
    assert http_req.method == "POST"

    http_resp = HTTPResponse(status_code=200, text='{"ok": true}')
    assert http_resp.json() == {"ok": True}

    ctx = InvocationContext(provider="openai", model="gpt-4", method="generate",
                            prompt="Hello", start_time=0.0, request_id="abc")
    assert ctx.provider == "openai"

    cache_cfg = CacheConfig(ttl_seconds=1800, max_size=500)
    assert cache_cfg.ttl_seconds == 1800

    res_opts = ResilienceOptions(enable_retry=True, retry_max_retries=5)
    assert res_opts.enable_retry is True

    # Protocol
    assert hasattr(LLMProvider, "generate")
    assert hasattr(AsyncLLMProvider, "generate")

    print("   ✓ 统一类型定义验证通过")


# =============================================================================
# 测试 2: HTTP 客户端抽象 + 连接池
# =============================================================================

def test_http_client():
    """验证 HTTP 客户端抽象"""
    print("2. HTTP 客户端抽象 + 连接池...")

    from llm.core.http_client import (
        BaseHTTPClient, RequestsHTTPClient, HttpxHTTPClient,
        ConnectionPoolManager,
    )

    # 抽象基类
    assert hasattr(BaseHTTPClient, "request")
    assert hasattr(BaseHTTPClient, "arequest")
    assert hasattr(BaseHTTPClient, "stream_request")
    assert hasattr(BaseHTTPClient, "astream_request")

    # RequestsHTTPClient 实例化
    client = RequestsHTTPClient()
    assert isinstance(client, BaseHTTPClient)
    client.close()

    # 连接池管理器（单例）
    pool1 = ConnectionPoolManager()
    pool2 = ConnectionPoolManager()
    assert pool1 is pool2  # 单例

    # 获取 session
    session = pool1.get_requests_session("openai")
    assert session is not None
    assert len(pool1.list_pools()) >= 1

    # 清理
    pool1.close_all()
    assert len(pool1.list_pools()) == 0

    print("   ✓ HTTP 客户端抽象 + 连接池验证通过")


# =============================================================================
# 测试 3: 拦截器模式
# =============================================================================

def test_interceptor():
    """验证拦截器模式"""
    print("3. 拦截器模式...")

    from llm.core.interceptor import (
        Interceptor, InterceptorChain,
        LoggingInterceptor, EventInterceptor, MetricsInterceptor,
        create_default_chain,
    )
    from llm.core.types import InterceptorPoint, InvocationContext

    # MetricsInterceptor
    metrics = MetricsInterceptor()
    assert isinstance(metrics, Interceptor)

    # 拦截器链
    chain = InterceptorChain()
    chain.add(metrics)
    chain.add(LoggingInterceptor())

    assert len(chain.interceptors) == 2

    # 执行拦截
    ctx = InvocationContext(
        provider="mock", model="mock-v1", method="generate",
        prompt="Hello", start_time=0.0, request_id="test-123",
    )
    chain.execute(InterceptorPoint.BEFORE_REQUEST, ctx)
    chain.execute(InterceptorPoint.AFTER_SUCCESS, ctx, result="ok")

    stats = metrics.stats
    assert stats["request_count"] == 1
    assert stats["success_count"] == 1

    # 移除拦截器
    chain.remove(MetricsInterceptor)
    assert len(chain.interceptors) == 1

    # 默认链
    default_chain = create_default_chain()
    assert len(default_chain.interceptors) >= 1

    print("   ✓ 拦截器模式验证通过")


# =============================================================================
# 测试 4: 缓存机制
# =============================================================================

def test_cache():
    """验证缓存机制"""
    print("4. 缓存机制...")

    from llm.core.cache import LLMCache, CacheConfig, get_global_cache

    # 基本缓存
    cache = LLMCache(CacheConfig(ttl_seconds=60, max_size=100))

    # 未命中
    result = cache.get("openai", "gpt-4", "Hello")
    assert result is None

    # 写入
    cache.set("openai", "gpt-4", "Hello", "Hi there!")
    assert cache.size == 1

    # 命中
    result = cache.get("openai", "gpt-4", "Hello")
    assert result == "Hi there!"

    # 不同参数不命中
    result = cache.get("openai", "gpt-4", "Hello", temperature=0.9)
    assert result is None

    # 统计
    stats = cache.stats
    assert stats["hits"] == 1
    assert stats["misses"] == 2

    # 删除
    assert cache.delete("openai", "gpt-4", "Hello") is True
    assert cache.size == 0

    # 全局缓存
    global_cache = get_global_cache()
    assert global_cache is get_global_cache()  # 单例

    print("   ✓ 缓存机制验证通过")


# =============================================================================
# 测试 5: 弹性机制集成
# =============================================================================

def test_resilience_integration():
    """验证弹性机制集成到 UnifiedAdapter"""
    print("5. 弹性机制集成...")

    from llm.core.adapter import UnifiedAdapter
    from llm.core.types import ResilienceOptions
    from llm.core.cache import LLMCache, CacheConfig
    from llm.core.interceptor import InterceptorChain, MetricsInterceptor

    provider = MockProvider()

    # 基础用法（向后兼容）
    adapter = UnifiedAdapter(provider)
    result = adapter.generate("Hello")
    assert "Response to" in result

    # 带弹性机制
    opts = ResilienceOptions(
        enable_circuit_breaker=True,
        enable_retry=True,
        retry_max_retries=2,
    )
    provider2 = MockProvider()
    adapter2 = UnifiedAdapter(provider2, resilience=opts)
    result2 = adapter2.generate("Hello")
    assert "Response to" in result2

    # 带缓存
    cache = LLMCache(CacheConfig(ttl_seconds=60))
    provider3 = MockProvider()
    adapter3 = UnifiedAdapter(provider3, cache=cache)
    r1 = adapter3.generate("Cache me")
    r2 = adapter3.generate("Cache me")
    assert r1 == r2
    assert provider3.call_count == 1  # 只调用了一次

    # 带自定义拦截器
    chain = InterceptorChain()
    metrics = MetricsInterceptor()
    chain.add(metrics)
    provider4 = MockProvider()
    adapter4 = UnifiedAdapter(provider4, interceptor_chain=chain)
    adapter4.generate("Hello")
    assert metrics.stats["request_count"] == 1

    print("   ✓ 弹性机制集成验证通过")


# =============================================================================
# 测试 6: 向后兼容
# =============================================================================

async def test_backward_compat():
    """验证向后兼容"""
    print("6. 向后兼容...")

    from llm.core.adapter import (
        IProviderClient, IAdapter, LLMResult, StreamChunk,
        UnifiedAdapter,
        BaseLLMAdapter, BaseAsyncLLMAdapter,
    )
    from llm.core.types import (
        LLMProvider, AsyncLLMProvider, StreamableLLMProvider,
        LLMRequest, LLMResponse,
        ProviderType, CircuitState,
    )

    # 旧类型仍然可用
    assert LLMRequest is not None
    assert LLMResponse is not None
    assert ProviderType.OPENAI == "openai"
    assert CircuitState.CLOSED == "closed"

    # 旧适配器基类仍然可用
    assert BaseLLMAdapter is not None
    assert BaseAsyncLLMAdapter is not None

    # UnifiedAdapter 仍然支持旧接口
    provider = MockProvider()
    adapter = UnifiedAdapter(provider)

    # 同步
    result = adapter.generate("Hello")
    assert "Response to" in result

    # 流式
    chunks = list(adapter.generate_stream("Hello"))
    assert len(chunks) == 2

    # JSON
    json_result = adapter.generate_json("Hello")
    assert "Response to" in json_result

    # with_response
    llm_result = adapter.generate_with_response("Hello")
    assert isinstance(llm_result, LLMResult)

    # 异步
    async_result = await adapter.agenerate("Hello")
    assert "Async response" in async_result

    # 异步流式
    async_chunks = [c async for c in adapter.agenerate_stream("Hello")]
    assert len(async_chunks) == 2

    print("   ✓ 向后兼容验证通过")


# =============================================================================
# 运行所有测试
# =============================================================================

async def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("LLM 架构 6 大优化验证测试")
    print("=" * 60)

    test_types()
    test_http_client()
    test_interceptor()
    test_cache()
    test_resilience_integration()
    await test_backward_compat()

    print("=" * 60)
    print("全部 6 项优化验证通过！✓")
    print("=" * 60)
    print()
    print("优化清单:")
    print("  ✓ 1. 统一类型定义 (core/types.py)")
    print("  ✓ 2. HTTP 客户端抽象 + 连接池 (core/http_client.py)")
    print("  ✓ 3. 拦截器模式 (core/interceptor.py)")
    print("  ✓ 4. 缓存机制 (core/cache.py)")
    print("  ✓ 5. 弹性机制集成 (unified_adapter.py)")
    print("  ✓ 6. 向后兼容")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
