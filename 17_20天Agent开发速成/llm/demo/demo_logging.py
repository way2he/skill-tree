# -*- coding: utf-8 -*-
"""
demo_logging.py - 一键开启 LLM 调用日志

特性：
- 一行 enable_logging() 全局生效，自动覆盖所有适配器
- 日志内容包含：渠道（provider）、调用模型（model）、底层实现（backend）、
  方法名、入参（prompt + kwargs）、出参（response）、耗时、错误、request_id
- 敏感字段（api_key / secret / token 等）自动脱敏
- 支持控制台 + 滚动文件双输出
- 同时安装 MetricsHandler，可随时拿到累计指标
"""

import os
import sys
import io

# Windows 控制台 UTF-8
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# 添加 llm 包路径
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))

from llm.core import enable_logging, disable_logging, get_metrics_handler  # noqa: E402


def demo_basic_console():
    """场景 1：控制台 INFO 日志"""
    print("\n=== 场景 1：控制台 INFO ===")
    enable_logging(level="INFO")

    try:
        from llm.core import get_llm
        client = get_llm()  # 使用配置文件里的默认 provider
        resp = client.generate("用一句话介绍你自己")
        print(f">> 返回: {resp[:80]}...")
    except Exception as e:
        print(f">> 调用失败（可能是 API key 未配置）: {e}")
    finally:
        disable_logging()


def demo_file_logging():
    """场景 2：同时写入文件，DEBUG 级别"""
    print("\n=== 场景 2：文件 + 控制台 DEBUG ===")
    log_path = os.path.join(HERE, "logs", "llm_calls.log")
    enable_logging(
        level="DEBUG",
        log_file=log_path,
        log_prompt=True,
        log_response=True,
        log_params=True,
        prompt_max_chars=200,
        response_max_chars=300,
    )

    try:
        from llm.core import get_llm
        client = get_llm()
        client.generate("Python 3.12 有哪些亮点？", temperature=0.5, max_tokens=200)
    except Exception as e:
        print(f">> 调用失败: {e}")
    finally:
        print(f">> 日志已写入：{log_path}")
        disable_logging()


def demo_metrics():
    """场景 3：累计指标"""
    print("\n=== 场景 3：指标采集 ===")
    enable_logging(level="WARNING", enable_metrics=True)  # 静默日志，只看指标

    try:
        from llm.core import get_llm
        client = get_llm()
        for q in ["你好", "1+1=?", "再见"]:
            try:
                client.generate(q)
            except Exception:
                pass
    finally:
        m = get_metrics_handler()
        if m:
            stats = m.get_metrics()
            print(f"  总请求数：{stats['total_requests']}")
            print(f"  成功 / 失败：{stats['success_count']} / {stats['failure_count']}")
            print(f"  平均耗时：{stats['avg_latency_ms']}")
            print(f"  按渠道：{stats['providers']}")
        disable_logging()


def demo_custom_handler():
    """场景 4：自定义事件订阅（无需 enable_logging）"""
    print("\n=== 场景 4：自定义事件订阅 ===")
    from llm.core import EventType, LLMEvent, subscribe, unsubscribe

    events = []

    def my_hook(ev: LLMEvent):
        events.append(ev)

    subscribe(None, my_hook)
    try:
        from llm.core import get_llm
        client = get_llm()
        try:
            client.generate("hi")
        except Exception:
            pass
    finally:
        unsubscribe(None, my_hook)

    for ev in events:
        print(f"  {ev.event_type.value:>20s} | rid={ev.request_id} | "
              f"provider={ev.provider} model={ev.model} method={ev.method}")


if __name__ == "__main__":
    demo_basic_console()
    demo_file_logging()
    demo_metrics()
    demo_custom_handler()
