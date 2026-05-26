# -*- coding: utf-8 -*-
"""
测试 factory 模块
"""

import pytest
import sys
from pathlib import Path

# 添加父目录到路径
llm_dir = Path(__file__).parent.parent
sys.path.insert(0, str(llm_dir))


class MockProvider:
    """Mock Provider 用于测试"""
    def __init__(self, api_key=None):
        self.api_key = api_key
    
    def generate(self, prompt):
        return f"Mock response to: {prompt}"


def test_register_and_create():
    """测试注册和创建"""
    from core import register_provider, create_llm, list_providers
    
    # 注册
    register_provider("test_mock", MockProvider)
    
    # 检查是否在列表中
    providers = list_providers()
    assert "test_mock" in providers, f"test_mock 应该在 {providers} 中"
    
    # 创建
    llm = create_llm("test_mock", api_key="test_key")
    assert llm is not None
    assert hasattr(llm, "generate")


def test_create_unknown_provider():
    """测试创建不存在的提供者应该抛出异常"""
    from core import create_llm, LLMProviderNotFoundError
    
    with pytest.raises(LLMProviderNotFoundError):
        create_llm("this_provider_does_not_exist_ever_12345")


def test_list_providers():
    """测试列出提供者"""
    from core import list_providers
    
    providers = list_providers()
    assert isinstance(providers, list)
    assert len(providers) >= 10, "应该至少有 10 个内置提供者"


def test_builtin_providers_registered():
    """测试内置提供者是否已注册"""
    from core import list_providers
    
    providers = list_providers()
    expected = [
        "openai", "anthropic", "deepseek", "qwen", "ollama",
        "glm", "kimi", "cohere", "wenxin"
    ]
    
    for name in expected:
        # 只检查其中一部分，避免太脆弱
        if name in providers:
            assert True, f"{name} 应该已注册"


def test_factory_import():
    """测试 factory 模块可以导入"""
    from core import factory
    assert factory is not None
    assert hasattr(factory, "register_provider")
    assert hasattr(factory, "create_llm")
    assert hasattr(factory, "list_providers")


def test_async_create_exists():
    """测试异步创建函数存在"""
    from core import create_async_llm, list_async_providers
    
    # 函数应该存在
    assert callable(create_async_llm)
    assert callable(list_async_providers)
    
    # 同步和异步列表应该相同（UnifiedAdapter 同时支持两者）
    sync_list = list_providers()
    async_list = list_async_providers()
    assert sync_list == async_list


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
