# -*- coding: utf-8 -*-
"""
Ollama 同步客户端测试 Demo

运行方式（在 17_20天Agent开发速成/ 目录下）：
    python -m llm.demo.demo_ollama_requests

前置条件：
    1. 安装并启动 Ollama 服务：ollama serve
    2. 拉取模型：ollama pull qwen3.5:9b（或其他模型）
"""

import sys
import io

# Windows 控制台中文友好
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from llm.requests.providers.ollama import OllamaClient


def test_generate() -> None:
    """
    测试同步生成方法

    Returns:
        None
    """
    print("=" * 50)
    print("【测试 generate() 同步生成】")
    print("=" * 50)

    # 初始化客户端
    client = OllamaClient(
        model="qwen3.5:4b",
        base_url="http://localhost:11434",
        system_prompt="你是一个友好的助手，回答简洁明了。",
        temperature=0.7,
        timeout=120,
    )

    try:
        # 发送请求
        response = client.generate("你好，请用一句话介绍你自己。")
        print(f"响应内容: {response}")
        print("✅ generate() 测试通过\n")

    except Exception as e:
        print(f"❌ generate() 测试失败: {e}\n")


def test_generate_stream() -> None:
    """
    测试流式生成方法

    Returns:
        None
    """
    print("=" * 50)
    print("【测试 generate_stream() 流式生成】")
    print("=" * 50)

    # 初始化客户端
    client = OllamaClient(
        model="qwen3.5:9b",
        base_url="http://localhost:11434",
        temperature=0.7,
        timeout=60,
    )

    try:
        print("响应内容: ", end="", flush=True)

        # 流式接收响应
        for chunk in client.generate_stream("请用三句话介绍 Python 语言的特点。"):
            print(chunk, end="", flush=True)

        print("\n✅ generate_stream() 测试通过\n")

    except Exception as e:
        print(f"\n❌ generate_stream() 测试失败: {e}\n")


def test_generate_json() -> None:
    """
    测试 JSON 格式生成方法

    Returns:
        None
    """
    print("=" * 50)
    print("【测试 generate_json() JSON 格式生成】")
    print("=" * 50)

    # 初始化客户端
    client = OllamaClient(
        model="qwen3.5:9b",
        base_url="http://localhost:11434",
        temperature=0.3,  # JSON 生成建议用较低温度
        timeout=60,
    )

    try:
        # 发送 JSON 格式请求
        prompt = """
        请以 JSON 格式输出以下信息：
        - name: Python 语言
        - year: 发布年份
        - creator: 创造者
        - features: 三个主要特点（数组）
        """
        response = client.generate_json(prompt)
        print(f"响应内容: {response}")
        print("✅ generate_json() 测试通过\n")

    except Exception as e:
        print(f"❌ generate_json() 测试失败: {e}\n")


def test_connection() -> bool:
    """
    测试 Ollama 服务连接

    Returns:
        bool: 连接成功返回 True，否则返回 False
    """
    print("=" * 50)
    print("【测试 Ollama 服务连接】")
    print("=" * 50)

    import requests

    try:
        # 尝试连接 Ollama 服务
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Ollama 服务已连接")
            print(f"   可用模型: {[m['name'] for m in models]}")
            return True
        else:
            print(f"❌ Ollama 服务响应异常: {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ 无法连接 Ollama 服务")
        print("   请确保已启动 Ollama: ollama serve")
        return False

    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False


def main() -> None:
    """
    主函数入口

    Returns:
        None
    """
    print("\n" + "=" * 50)
    print("  Ollama 同步客户端测试")
    print("=" * 50 + "\n")

    # 1. 测试连接
    if not test_connection():
        print("\n⚠️  请先启动 Ollama 服务并拉取模型")
        print("   启动服务: ollama serve")
        print("   拉取模型: ollama pull qwen3.5:9b")
        return

    print()

    # 2. 测试同步生成
    test_generate()

    # 3. 测试流式生成
    test_generate_stream()

    # 4. 测试 JSON 生成
    test_generate_json()

    print("=" * 50)
    print("  测试完成")
    print("=" * 50)


if __name__ == "__main__":
    main()
