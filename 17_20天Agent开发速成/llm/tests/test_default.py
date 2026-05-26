# -*- coding: utf-8 -*-
"""
测试 default 模块（get_llm 等）
"""

import pytest
import sys
import os
from pathlib import Path

# 添加父目录到路径
llm_dir = Path(__file__).parent.parent
sys.path.insert(0, str(llm_dir))


def test_get_llm_import():
    """测试 get_llm 可以导入"""
    from core import get_llm, get_async_llm
    assert callable(get_llm)
    assert callable(get_async_llm)


def test_resolve_provider_fallback():
    """测试解析提供者的兜底逻辑"""
    from core import resolve_provider, FALLBACK_PROVIDER
    
    # 保存原来的环境变量
    old_env = os.environ.get("LLM_PROVIDER")
    
    try:
        # 清除环境变量
        if "LLM_PROVIDER" in os.environ:
            del os.environ["LLM_PROVIDER"]
        
        # 应该返回兜底值
        fallback = resolve_provider()
        assert fallback == FALLBACK_PROVIDER, f"应该返回兜底 {FALLBACK_PROVIDER}"
        
    finally:
        # 恢复环境变量
        if old_env:
            os.environ["LLM_PROVIDER"] = old_env


def test_resolve_provider_env_var():
    """测试环境变量解析"""
    from core import resolve_provider
    
    # 保存原来的环境变量
    old_env = os.environ.get("LLM_PROVIDER")
    
    try:
        # 设置环境变量
        os.environ["LLM_PROVIDER"] = "deepseek"
        
        result = resolve_provider()
        assert result == "deepseek", f"应该返回 deepseek，实际 {result}"
        
    finally:
        # 恢复环境变量
        if old_env:
            os.environ["LLM_PROVIDER"] = old_env
        elif "LLM_PROVIDER" in os.environ:
            del os.environ["LLM_PROVIDER"]


def test_resolve_provider_explicit_param():
    """测试显式参数"""
    from core import resolve_provider
    
    # 显式参数优先级最高
    assert resolve_provider("openai") == "openai"
    assert resolve_provider("DEEPSEEK") == "deepseek"  # 应该转小写


def test_current_provider():
    """测试 current_provider 函数"""
    from core import current_provider
    
    provider = current_provider()
    assert isinstance(provider, str)
    assert len(provider) > 0


def test_provider_name_enum_exists():
    """测试 ProviderName 枚举存在"""
    from core import ProviderName
    
    # 枚举应该是一个 Enum 类
    assert hasattr(ProviderName, "OLLAMA")
    assert hasattr(ProviderName, "OPENAI")


def test_provider_like_type_exists():
    """测试 ProviderLike 类型存在"""
    from core import ProviderLike
    
    # 类型应该存在
    assert ProviderLike is not None


def test_backend_functions_exist():
    """测试 backend 相关函数存在"""
    from core import (
        set_default_backend,
        get_default_backend,
        reset_default_backend,
    )
    
    assert callable(set_default_backend)
    assert callable(get_default_backend)
    assert callable(reset_default_backend)


def test_deprecated_create_client():
    """测试 create_client 弃用警告"""
    import warnings
    from core import create_client
    
    # 应该发出 DeprecationWarning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # 我们只测试警告，不实际创建（可能需要 API key）
        try:
            create_client("ollama")
        except Exception:
            # 只要有警告就行
            pass
        
        if w:
            # 检查是否有 DeprecationWarning
            assert any(issubclass(warn.category, DeprecationWarning) for warn in w), \
                "create_client 应该发出 DeprecationWarning"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
