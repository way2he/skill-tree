# -*- coding: utf-8 -*-
"""
依赖安装验证脚本

运行此脚本检查所有核心依赖是否正确安装。
"""

import sys
from typing import Dict, List, Tuple


def check_import(module_name: str) -> Tuple[bool, str]:
    """检查模块是否可以导入"""
    try:
        __import__(module_name)
        return True, "✅ OK"
    except ImportError as e:
        return False, f"❌ 缺失 - {e}"


def check_package_version(package_name: str) -> str:
    """获取包的版本"""
    try:
        import importlib.metadata
        return importlib.metadata.version(package_name)
    except Exception:
        return "unknown"


def main() -> None:
    print("=" * 50)
    print("Agent开发环境验证")
    print("=" * 50)
    
    print(f"\nPython版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    
    # 核心依赖检查
    core_deps = [
        ("requests", "requests"),
        ("aiohttp", "aiohttp"),
        ("pydantic", "pydantic"),
        ("tenacity", "tenacity"),
        ("numpy", "numpy"),
    ]
    
    # LLM相关
    llm_deps = [
        ("openai", "openai"),
        ("anthropic", "anthropic"),
        ("langchain", "langchain"),
        ("langchain_openai", "langchain-openai"),
        ("langgraph", "langgraph"),
        ("tiktoken", "tiktoken"),
    ]
    
    # 向量数据库
    vectordb_deps = [
        ("faiss", "faiss-cpu"),
        ("qdrant_client", "qdrant-client"),
        ("chromadb", "chromadb"),
        ("sentence_transformers", "sentence-transformers"),
    ]
    
    # 部署和工具
    dev_deps = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("loguru", "loguru"),
        ("dotenv", "python-dotenv"),
    ]
    
    # 测试依赖
    test_deps = [
        ("pytest", "pytest"),
        ("pytest_asyncio", "pytest-asyncio"),
    ]
    
    categories = [
        ("核心库", core_deps),
        ("LLM框架", llm_deps),
        ("向量数据库", vectordb_deps),
        ("部署工具", dev_deps),
        ("测试工具", test_deps),
    ]
    
    all_passed = True
    for category, deps in categories:
        print(f"\n{category}:")
        for module_name, package_name in deps:
            status, message = check_import(module_name)
            version = check_package_version(package_name)
            if not status:
                all_passed = False
            print(f"  {package_name:25} {message:15} (版本: {version})")
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ 所有核心依赖安装成功！")
        print("\n你现在可以:")
        print("1. 复制 .env.example 为 .env")
        print("2. 填入你的 API 密钥")
        print("3. 开始 Day01 的学习！")
    else:
        print("❌ 部分依赖缺失，请运行:")
        print("pip install -e \".[dev]\"")
    print("=" * 50)


if __name__ == "__main__":
    main()
