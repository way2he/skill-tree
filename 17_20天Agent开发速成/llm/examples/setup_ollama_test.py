# -*- coding: utf-8 -*-
"""
Ollama 测试环境快速配置和检查

运行方式：
    1. 检查环境: python setup_ollama_test.py check
    2. 启动服务: python setup_ollama_test.py serve
    3. 拉取模型: python setup_ollama_test.py pull
    4. 一键全部: python setup_ollama_test.py all
"""

import sys
import io
import subprocess
import time
import requests
from pathlib import Path

# Windows 控制台中文友好
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# 测试配置
TEST_MODEL = "qwen3.5:4b"


def check_ollama_installed() -> bool:
    """检查 Ollama 是否已安装"""
    print("\n[1/4] 检查 Ollama 安装...")
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"[OK] Ollama 已安装: {result.stdout.strip()}")
            return True
        else:
            print(f"[FAIL] Ollama 检查失败")
            return False
    except FileNotFoundError:
        print(f"[FAIL] 未找到 Ollama")
        print(f"       请下载安装: https://ollama.com/download")
        return False
    except Exception as e:
        print(f"[FAIL] 检查失败: {e}")
        return False


def check_ollama_running() -> bool:
    """检查 Ollama 服务是否正在运行"""
    print("\n[2/4] 检查 Ollama 服务...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print(f"[OK] Ollama 服务正在运行")
            models = response.json().get("models", [])
            print(f"[OK] 已加载模型: {[m['name'] for m in models]}")
            return True
        else:
            print(f"[FAIL] Ollama 服务响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"[FAIL] 无法连接 Ollama 服务")
        print(f"       请运行: ollama serve")
        return False
    except Exception as e:
        print(f"[FAIL] 检查失败: {e}")
        return False


def pull_model(model_name: str = TEST_MODEL) -> bool:
    """拉取测试模型"""
    print(f"\n[3/4] 拉取模型 {model_name}...")
    try:
        print(f"[INFO] 正在拉取 {model_name} (这可能需要几分钟)...")
        result = subprocess.run(
            ["ollama", "pull", model_name],
            timeout=600  # 10 分钟超时
        )
        if result.returncode == 0:
            print(f"[OK] 模型 {model_name} 拉取成功")
            return True
        else:
            print(f"[FAIL] 模型拉取失败")
            return False
    except Exception as e:
        print(f"[FAIL] 拉取失败: {e}")
        return False


def check_model_available(model_name: str = TEST_MODEL) -> bool:
    """检查模型是否可用"""
    print(f"\n[4/4] 检查模型 {model_name}...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            if model_name in model_names:
                print(f"[OK] 模型 {model_name} 已就绪")
                return True
            else:
                print(f"[FAIL] 模型 {model_name} 未找到")
                print(f"[INFO] 可用模型: {model_names}")
                return False
        return False
    except Exception as e:
        print(f"[FAIL] 检查失败: {e}")
        return False


def print_setup_guide():
    """打印配置指南"""
    print("\n" + "=" * 60)
    print("Ollama 测试环境配置指南")
    print("=" * 60)
    print("\n步骤 1: 安装 Ollama")
    print("  下载地址: https://ollama.com/download")
    print("\n步骤 2: 启动 Ollama 服务")
    print("  运行命令: ollama serve")
    print(f"\n步骤 3: 拉取模型 {TEST_MODEL}")
    print(f"  运行命令: ollama pull {TEST_MODEL}")
    print("\n步骤 4: 运行测试")
    print("  完整测试: python test_ollama_qwen35.py")
    print("  独立测试: python test_ollama_independent.py all")
    print("=" * 60)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="Ollama 测试环境配置工具")
    parser.add_argument(
        "command", nargs="?", default="check",
        help="命令: check (检查), pull (拉取), all (全部)"
    )
    parser.add_argument(
        "--model", default=TEST_MODEL,
        help=f"模型名称 (默认: {TEST_MODEL})"
    )

    args = parser.parse_args()

    if args.command == "check":
        print("\n" + "=" * 60)
        print("Ollama 环境检查")
        print("=" * 60)

        check_ollama_installed()
        check_ollama_running()
        check_model_available(args.model)

        print_setup_guide()

    elif args.command == "pull":
        print("\n" + "=" * 60)
        print(f"拉取模型 {args.model}")
        print("=" * 60)

        if not check_ollama_installed():
            return
        if not check_ollama_running():
            return

        pull_model(args.model)
        check_model_available(args.model)

    elif args.command == "all":
        print("\n" + "=" * 60)
        print("Ollama 环境一键配置")
        print("=" * 60)

        if not check_ollama_installed():
            print_setup_guide()
            return

        if not check_ollama_running():
            print("\n[INFO] 请先启动 Ollama 服务: ollama serve")
            print_setup_guide()
            return

        pull_model(args.model)
        check_model_available(args.model)

        print("\n[OK] 环境配置完成！")
        print("\n现在可以运行测试:")
        print("  python test_ollama_qwen35.py")

    else:
        print(f"未知命令: {args.command}")
        print("可用命令: check, pull, all")


if __name__ == "__main__":
    main()

