# -*- coding: utf-8 -*-
"""
Ollama Qwen3.5:4b 独立测试 - 每个测试可以单独运行

这些测试直接对应原来的 demo 文件:
- test_1_basic.py ← demo_basic.py
- test_2_stream.py ← demo_stream.py
- test_3_json.py ← demo_json.py
- test_4_zero_config.py ← demo_zero_config.py
- test_5_backend.py ← demo_backend_selector.py
- test_6_async.py ← demo_backend_async.py
- test_7_logging.py ← demo_logging.py
- test_8_resilience.py ← demo_resilience.py
- test_9_provider.py ← demo_ollama_requests.py
"""

import sys
import io
from pathlib import Path

# Windows 控制台中文友好
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# 测试配置
TEST_MODEL = "qwen3.5:4b"


def test_1_basic():
    """
    测试 1: 基础调用 (demo_basic.py)
    """
    print("\n" + "=" * 60)
    print("TEST 1/9: 基础调用 (demo_basic.py)")
    print("=" * 60)

    from llm.core import create_llm, list_providers

    print(f"已注册厂商: {list_providers()}")

    llm = create_llm("ollama", model=TEST_MODEL)

    text = llm.generate("用一句话解释什么是 AI")
    print(f"\ngenerate 返回:\n{text}")

    resp = llm.generate_with_response("1+1=?")
    print(f"\ngenerate_with_response:")
    print(f"  内容: {resp.content}")
    print(f"  模型: {resp.model}")


def test_2_stream():
    """
    测试 2: 流式响应 (demo_stream.py)
    """
    print("\n" + "=" * 60)
    print("TEST 2/9: 流式响应 (demo_stream.py)")
    print("=" * 60)

    from llm.core import get_llm

    llm = get_llm("ollama")

    print("\n流式生成:")
    for chunk in llm.generate_stream("用三句话介绍 Python"):
        print(chunk, end="", flush=True)
    print()


def test_3_json():
    """
    测试 3: JSON 生成 (demo_json.py)
    """
    print("\n" + "=" * 60)
    print("TEST 3/9: JSON 生成 (demo_json.py)")
    print("=" * 60)

    from llm.core import create_llm
    import json

    llm = create_llm("ollama", model=TEST_MODEL, temperature=0.3)

    prompt = """
    请以 JSON 格式输出：
    {
        "name": "Python",
        "year": 1991,
        "creator": "Guido van Rossum",
        "features": ["简单", "易学", "功能强大"]
    }
    """
    response = llm.generate_json(prompt)
    print(f"\nJSON 响应:\n{response}")

    parsed = json.loads(response)
    print(f"\n解析成功: {parsed}")


def test_4_zero_config():
    """
    测试 4: 零配置 (demo_zero_config.py)
    """
    print("\n" + "=" * 60)
    print("TEST 4/9: 零配置 (demo_zero_config.py)")
    print("=" * 60)

    from llm.core import get_llm, current_provider

    print(f"当前默认提供商: {current_provider()}")

    llm = get_llm()
    response = llm.generate("你好，零配置测试")
    print(f"\n响应: {response}")


def test_5_backend():
    """
    测试 5: Backend 选择器 (demo_backend_selector.py)
    """
    print("\n" + "=" * 60)
    print("TEST 5/9: Backend 选择器 (demo_backend_selector.py)")
    print("=" * 60)

    from llm.core import LLMClientBuilder, BackendType

    llm = (
        LLMClientBuilder()
        .with_provider("ollama")
        .with_model(TEST_MODEL)
        .with_backend(BackendType.REQUESTS)
        .build()
    )

    response = llm.generate("Builder 模式测试")
    print(f"\n响应: {response}")


def test_6_async():
    """
    测试 6: 异步调用 (demo_backend_async.py)
    """
    print("\n" + "=" * 60)
    print("TEST 6/9: 异步调用 (demo_backend_async.py)")
    print("=" * 60)

    import asyncio
    from llm.core import get_async_llm

    async def run():
        llm = get_async_llm("ollama")
        response = await llm.agenerate("异步调用测试")
        print(f"\n响应: {response}")

    asyncio.run(run())


def test_7_logging():
    """
    测试 7: 日志记录 (demo_logging.py)
    """
    print("\n" + "=" * 60)
    print("TEST 7/9: 日志记录 (demo_logging.py)")
    print("=" * 60)

    from llm.core import create_llm, enable_logging, is_logging_enabled

    enable_logging()
    print(f"日志已启用: {is_logging_enabled()}")

    llm = create_llm("ollama", model=TEST_MODEL)
    response = llm.generate("日志测试")
    print(f"\n响应: {response}")


def test_8_resilience():
    """
    测试 8: 弹性机制 (demo_resilience.py)
    """
    print("\n" + "=" * 60)
    print("TEST 8/9: 弹性机制 (demo_resilience.py)")
    print("=" * 60)

    from llm.core import create_llm
    from llm.core.resilience import with_retry

    llm = create_llm("ollama", model=TEST_MODEL)

    @with_retry(max_attempts=3)
    def resilient_call():
        return llm.generate("弹性机制测试")

    response = resilient_call()
    print(f"\n响应: {response}")


def test_9_provider():
    """
    测试 9: 直接 Provider 调用 (demo_ollama_requests.py)
    """
    print("\n" + "=" * 60)
    print("TEST 9/9: 直接 Provider 调用 (demo_ollama_requests.py)")
    print("=" * 60)

    from llm.requests.providers.ollama import OllamaClient

    client = OllamaClient(model=TEST_MODEL)
    response = client.generate("直接 Provider 调用测试")
    print(f"\n响应: {response}")


def main():
    """
    主函数：根据参数选择运行哪个测试
    """
    import argparse

    parser = argparse.ArgumentParser(description="Ollama Qwen3.5:4b 独立测试")
    parser.add_argument(
        "test", nargs="?", default="all",
        help="测试编号 (1-9) 或 'all' 运行所有测试"
    )

    args = parser.parse_args()

    tests = {
        "1": test_1_basic,
        "2": test_2_stream,
        "3": test_3_json,
        "4": test_4_zero_config,
        "5": test_5_backend,
        "6": test_6_async,
        "7": test_7_logging,
        "8": test_8_resilience,
        "9": test_9_provider,
    }

    if args.test == "all":
        print("=" * 60)
        print("Ollama Qwen3.5:4b 完整独立测试")
        print("=" * 60)
        for name, test_func in tests.items():
            try:
                test_func()
            except Exception as e:
                print(f"\n测试 {name} 失败: {e}")
    elif args.test in tests:
        tests[args.test]()
    else:
        print(f"未知测试: {args.test}")
        print("可用测试: 1-9 或 'all'")


if __name__ == "__main__":
    main()

