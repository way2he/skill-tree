# -*- coding: utf-8 -*-
"""
llm/core 进阶 Demo —— 重试 / 熔断 / 限流 / 指标采集

运行：
    set DEEPSEEK_API_KEY=sk-xxx
    python -m llm.demo.demo_resilience
"""

import os
import sys
import io
import time

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from llm.core import (
    create_llm,
    resilient,
    ResilienceConfig,
    EventBus,
    LoggingHandler,
    MetricsHandler,
)


# 1. 装一个全局事件总线，挂上日志 + 指标两个 handler
bus = EventBus()
bus.subscribe(None, LoggingHandler(log_prompt=False))
metrics = MetricsHandler()
bus.subscribe(None, metrics)


# 2. 配一份弹性策略
resilience_cfg = ResilienceConfig(
    retry_max_retries=3,           # 失败最多重试 3 次
    retry_base_delay=1.0,          # 起始退避 1s
    circuit_breaker_enabled=True,  # 5 连失败后熔断
    circuit_breaker_failure_threshold=5,
    rate_limiter_enabled=True,     # 每分钟最多 60 次
    rate_limiter_requests_per_minute=60,
)


# 3. 用装饰器包装你的业务函数
llm = create_llm(
    "deepseek",
    api_key=os.getenv("DEEPSEEK_API_KEY", ""),
    model="deepseek-chat",
)


@resilient(resilience_cfg)
def ask(prompt: str) -> str:
    """带重试 / 熔断 / 限流保护的问答函数"""
    return llm.generate(prompt)


def main():
    questions = [
        "什么是 ReAct 模式？",
        "RAG 中 Rerank 的作用？",
        "解释一下 Plan-and-Execute。",
    ]
    for q in questions:
        t0 = time.time()
        try:
            ans = ask(q)
            print(f"\nQ: {q}\nA: {ans[:120]}...  ({(time.time()-t0)*1000:.0f} ms)")
        except Exception as e:
            print(f"\nQ: {q}\n失败: {e}")

    # 4. 看指标
    print("\n【指标快照】")
    for k, v in metrics.get_metrics().items():
        print(f"  {k:20s} = {v}")


if __name__ == "__main__":
    main()
