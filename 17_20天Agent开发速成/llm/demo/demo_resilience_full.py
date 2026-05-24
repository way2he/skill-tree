# -*- coding: utf-8 -*-
"""
弹性进阶 demo —— 覆盖剩余弹性 API

包括：
- RateLimiterConfig / TokenBucketRateLimiter   限流
- FallbackStrategy / AsyncFallbackStrategy     降级
- with_async_retry / async_resilient            异步重试 / 异步组合

无需任何真实 LLM 调用：用本地 echo 函数演示弹性机制本身。

运行：
    py -3 -m llm.demo.demo_resilience_full
"""

import asyncio
import sys
import io
import random
import time

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from llm.core import (
    RetryPolicy, with_retry, with_async_retry,
    CircuitBreaker, CircuitBreakerConfig,
    RateLimiterConfig, TokenBucketRateLimiter,
    FallbackStrategy, AsyncFallbackStrategy,
    ResilienceConfig, resilient, async_resilient,
)


# ----------------- 1. 限流 -----------------
def demo_rate_limiter():
    print("=== 1. 令牌桶限流（每秒 2 次）===")
    limiter = TokenBucketRateLimiter(
        RateLimiterConfig(requests_per_second=2, burst_size=2)
    )

    @limiter
    def call(i):
        return f"#{i} ok @ {time.strftime('%H:%M:%S')}"

    t0 = time.time()
    for i in range(5):
        try:
            print("   ", call(i))
        except Exception as e:
            print("    rate-limited:", e)
    print(f"    总耗时 {time.time()-t0:.2f}s")


# ----------------- 2. 降级 -----------------
def demo_fallback():
    print("\n=== 2. FallbackStrategy（主失败 → 备 1 → 备 2）===")

    class FailClient:
        def __init__(self, name): self.name = name
        def generate(self, prompt, **kwargs):
            raise RuntimeError(f"{self.name} 故意失败")

    class OkClient:
        def __init__(self, name): self.name = name
        def generate(self, prompt, **kwargs):
            return f"{self.name} 救场：{prompt}"

    fb = FallbackStrategy(
        primary=FailClient("primary"),
        fallbacks=[FailClient("backup_1"), OkClient("backup_2")],
        on_fallback=lambda i, e: print(f"    → fallback #{i}: {e}"),
    )
    print("    结果:", fb.generate("hi"))


async def demo_async_fallback():
    print("\n=== 3. AsyncFallbackStrategy ===")

    class FailClient:
        async def generate(self, prompt, **kwargs):
            raise RuntimeError("async primary 失败")

    class OkClient:
        async def generate(self, prompt, **kwargs):
            return f"async backup 救场：{prompt}"

    fb = AsyncFallbackStrategy(
        primary=FailClient(),
        fallbacks=[OkClient()],
        on_fallback=lambda i, e: print(f"    → fallback #{i}: {e}"),
    )
    print("    结果:", await fb.generate("hi"))


# ----------------- 3. 异步重试 / 异步组合 -----------------
async def demo_async_retry():
    print("\n=== 4. with_async_retry（前 2 次失败，第 3 次成功）===")
    counter = {"n": 0}

    @with_async_retry(RetryPolicy(max_retries=3, base_delay=0.1, jitter=False))
    async def flaky():
        counter["n"] += 1
        if counter["n"] < 3:
            raise ConnectionError(f"假装失败 #{counter['n']}")
        return f"成功 @ 第 {counter['n']} 次"

    print("    结果:", await flaky())


async def demo_async_resilient():
    print("\n=== 5. async_resilient（重试 + 限流 + 熔断 组合）===")
    counter = {"n": 0}
    cfg = ResilienceConfig(
        retry=RetryPolicy(max_retries=2, base_delay=0.1, jitter=False),
        circuit_breaker=CircuitBreakerConfig(failure_threshold=3, recovery_timeout=1.0),
        rate_limiter=RateLimiterConfig(requests_per_second=5, burst_size=5),
    )

    @async_resilient(cfg, name="demo-async")
    async def call(i):
        counter["n"] += 1
        if random.random() < 0.4:
            raise ConnectionError("偶发抖动")
        return f"async ok #{i} (内部尝试 {counter['n']} 次)"

    for i in range(4):
        try:
            print("   ", await call(i))
        except Exception as e:
            print("    失败：", e)


def main():
    demo_rate_limiter()
    demo_fallback()
    asyncio.run(demo_async_fallback())
    asyncio.run(demo_async_retry())
    asyncio.run(demo_async_resilient())


if __name__ == "__main__":
    main()
