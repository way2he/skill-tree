# -*- coding: utf-8 -*-
"""
Ollama Qwen3.5:4b 完整测试套件

测试所有入口点：
- 基础调用 (demo_basic)
- 流式响应 (demo_stream)
- JSON 生成 (demo_json)
- 零配置 (demo_zero_config)
- Backend 选择器 (demo_backend_selector)
- 异步调用 (demo_backend_async)
- 日志记录 (demo_logging)
- 弹性机制 (demo_resilience)

前置条件：
    1. 安装并启动 Ollama: ollama serve
    2. 拉取模型: ollama pull qwen2.5:4b 或 qwen3.5:4b
"""

import sys
import io
import time
import asyncio
from pathlib import Path

# Windows 控制台中文友好
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# 测试配置
TEST_MODEL = "qwen2.5:4b"  # 实际可用模型
TEST_MODEL_ALT = "qwen3.5:4b"


def test_connection() -> bool:
    """
    测试 Ollama 服务连接

    Returns:
        bool: 连接成功返回 True
    """
    print("\n" + "=" * 60)
    print("TEST #0: Ollama 服务连接测试")
    print("=" * 60)

    import requests

    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            print(f"[OK] Ollama 服务已连接")
            print(f"[OK] 可用模型: {model_names}")

            # 检查测试模型是否可用
            if TEST_MODEL in model_names:
                print(f"[OK] 测试模型 {TEST_MODEL} 已存在")
            elif TEST_MODEL_ALT in model_names:
                print(f"[OK] 备用模型 {TEST_MODEL_ALT} 已存在")
                globals()["TEST_MODEL"] = TEST_MODEL_ALT
            else:
                print(f"[WARN] 测试模型未找到，请运行: ollama pull {TEST_MODEL}")

            return True
        else:
            print(f"[FAIL] Ollama 服务响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"[FAIL] 无法连接 Ollama 服务")
        print(f"       请确保已启动: ollama serve")
        return False
    except Exception as e:
        print(f"[FAIL] 连接测试失败: {e}")
        return False


def test_basic() -> bool:
    """
    测试基础调用 (demo_basic)

    Returns:
        bool: 测试通过返回 True
    """
    print("\n" + "=" * 60)
    print("TEST #1: 基础调用测试 (demo_basic)")
    print("=" * 60)

    try:
        from llm.core import create_llm, list_providers

        print(f"[OK] 已注册厂商: {list_providers()}")

        llm = create_llm("ollama", model=TEST_MODEL)

        text = llm.generate("用一句话解释什么是 AI")
        print(f"[OK] generate 返回: {text[:80]}...")

        resp = llm.generate_with_response("1+1=?")
        print(f"[OK] generate_with_response:")
        print(f"     内容: {resp.content}")
        print(f"     模型: {resp.model}")

        return True
    except Exception as e:
        print(f"[FAIL] 基础调用测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_stream() -> bool:
    """
    测试流式响应 (demo_stream)

    Returns:
        bool: 测试通过返回 True
    """
    print("\n" + "=" * 60)
    print("TEST #2: 流式响应测试 (demo_stream)")
    print("=" * 60)

    try:
        from llm.core import get_llm

        llm = get_llm("ollama")

        print(f"[OK] 开始流式生成:")
        t0 = time.time()
        chunks = 0
        full_text = ""
        for chunk in llm.generate_stream("用三句话介绍 Python"):
            print(chunk, end="", flush=True)
            full_text += chunk
            chunks += 1

        print(f"\n[OK] done | {(time.time()-t0)*1000:.0f} ms | {chunks} chunks")
        print(f"[OK] 完整内容长度: {len(full_text)}")

        return True
    except Exception as e:
        print(f"\n[FAIL] 流式响应测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_json() -> bool:
    """
    测试 JSON 生成 (demo_json)

    Returns:
        bool: 测试通过返回 True
    """
    print("\n" + "=" * 60)
    print("TEST #3: JSON 生成测试 (demo_json)")
    print("=" * 60)

    try:
        from llm.core import create_llm

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
        print(f"[OK] JSON 响应: {response[:150]}...")

        # 验证 JSON 格式
        import json
        parsed = json.loads(response)
        print(f"[OK] JSON 解析成功: {list(parsed.keys())}")

        return True
    except Exception as e:
        print(f"[FAIL] JSON 生成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_zero_config() -> bool:
    """
    测试零配置 (demo_zero_config)

    Returns:
        bool: 测试通过返回 True
    """
    print("\n" + "=" * 60)
    print("TEST #4: 零配置测试 (demo_zero_config)")
    print("=" * 60)

    try:
        from llm.core import get_llm, current_provider

        print(f"[OK] 当前默认提供商: {current_provider()}")

        llm = get_llm()  # 零配置调用
        response = llm.generate("你好")
        print(f"[OK] 零配置调用成功: {response[:60]}...")

        return True
    except Exception as e:
        print(f"[FAIL] 零配置测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_backend_selector() -> bool:
    """
    测试 Backend 选择器 (demo_backend_selector)

    Returns:
        bool: 测试通过返回 True
    """
    print("\n" + "=" * 60)
    print("TEST #5: Backend 选择器测试 (demo_backend_selector)")
    print("=" * 60)

    try:
        from llm.core import LLMClientBuilder, BackendType

        # Builder 模式
        llm = (
            LLMClientBuilder()
            .with_provider("ollama")
            .with_model(TEST_MODEL)
            .with_backend(BackendType.REQUESTS)
            .build()
        )

        response = llm.generate("Builder 模式测试")
        print(f"[OK] Builder 模式调用成功: {response[:60]}...")

        return True
    except Exception as e:
        print(f"[FAIL] Backend 选择器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_async() -> bool:
    """
    测试异步调用 (demo_backend_async)

    Returns:
        bool: 测试通过返回 True
    """
    print("\n" + "=" * 60)
    print("TEST #6: 异步调用测试 (demo_backend_async)")
    print("=" * 60)

    try:
        from llm.core import get_async_llm

        llm = get_async_llm("ollama")

        t0 = time.time()
        response = await llm.agenerate("异步调用测试")
        elapsed = (time.time() - t0) * 1000
        print(f"[OK] 异步调用成功: {response[:60]}...")
        print(f"[OK] 耗时: {elapsed:.0f} ms")

        return True
    except Exception as e:
        print(f"[FAIL] 异步调用测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_logging() -> bool:
    """
    测试日志记录 (demo_logging)

    Returns:
        bool: 测试通过返回 True
    """
    print("\n" + "=" * 60)
    print("TEST #7: 日志记录测试 (demo_logging)")
    print("=" * 60)

    try:
        from llm.core import create_llm, enable_logging, is_logging_enabled

        enable_logging()
        print(f"[OK] 日志已启用: {is_logging_enabled()}")

        llm = create_llm("ollama", model=TEST_MODEL)
        response = llm.generate("日志测试")
        print(f"[OK] 调用完成（查看上方日志）")

        return True
    except Exception as e:
        print(f"[FAIL] 日志记录测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_resilience() -> bool:
    """
    测试弹性机制 (demo_resilience)

    Returns:
        bool: 测试通过返回 True
    """
    print("\n" + "=" * 60)
    print("TEST #8: 弹性机制测试 (demo_resilience)")
    print("=" * 60)

    try:
        from llm.core import create_llm
        from llm.core.resilience import ResilienceConfig, with_retry

        llm = create_llm("ollama", model=TEST_MODEL)

        @with_retry(max_attempts=3)
        def resilient_call():
            return llm.generate("弹性机制测试")

        response = resilient_call()
        print(f"[OK] 弹性调用成功: {response[:60]}...")

        return True
    except Exception as e:
        print(f"[FAIL] 弹性机制测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_provider_direct() -> bool:
    """
    测试直接使用 Provider (requests/providers/ollama)

    Returns:
        bool: 测试通过返回 True
    """
    print("\n" + "=" * 60)
    print("TEST #9: 直接 Provider 调用测试")
    print("=" * 60)

    try:
        from llm.implementations.requests.providers.ollama import OllamaClient

        client = OllamaClient(model=TEST_MODEL)
        response = client.generate("直接 Provider 调用")
        print(f"[OK] 直接调用成功: {response[:60]}...")

        return True
    except Exception as e:
        print(f"[FAIL] 直接 Provider 调用失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_all_tests():
    """
    运行所有测试
    """
    print("\n" + "=" * 60)
    print("  Ollama Qwen3.5:4b 完整测试套件")
    print("=" * 60)

    results = {}

    # 测试 0: 连接
    results["连接"] = test_connection()
    if not results["连接"]:
        print("\n[FAIL] Ollama 服务未启动，无法继续测试")
        print("\n请先运行:")
        print("  1. ollama serve")
        print(f"  2. ollama pull {TEST_MODEL}")
        return

    # 测试 1-9
    results["基础调用"] = test_basic()
    results["流式响应"] = test_stream()
    results["JSON 生成"] = test_json()
    results["零配置"] = test_zero_config()
    results["Backend 选择器"] = test_backend_selector()
    results["异步调用"] = await test_async()
    results["日志记录"] = test_logging()
    results["弹性机制"] = test_resilience()
    results["直接 Provider"] = test_provider_direct()

    # 总结
    print("\n" + "=" * 60)
    print("  测试总结")
    print("=" * 60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for name, ok in results.items():
        status = "[OK]" if ok else "[FAIL]"
        print(f"{status} {name}")

    print("\n" + "=" * 60)
    print(f"  总计: {passed}/{total} 测试通过")
    print("=" * 60)

    if passed == total:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️  有 {total-passed} 个测试失败")


if __name__ == "__main__":
    asyncio.run(run_all_tests())

