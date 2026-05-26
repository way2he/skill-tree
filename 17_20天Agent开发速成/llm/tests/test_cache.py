# -*- coding: utf-8 -*-
"""
测试 cache 模块
"""

import pytest
import sys
from pathlib import Path

# 添加父目录到路径
llm_dir = Path(__file__).parent.parent
sys.path.insert(0, str(llm_dir))


def test_cache_import():
    """测试 cache 模块可以导入"""
    from core import cache
    assert cache is not None


def test_cache_config_exists():
    """测试 CacheConfig 存在"""
    from core.cache import CacheConfig
    
    config = CacheConfig(ttl_seconds=3600, max_size=100)
    assert config.ttl_seconds == 3600
    assert config.max_size == 100


def test_cache_class_exists():
    """测试 LLMCache 存在"""
    from core.cache import LLMCache, CacheConfig
    
    config = CacheConfig(ttl_seconds=60, max_size=10)
    cache = LLMCache(config)
    
    # 基本功能测试
    cache.set("openai", "gpt-4", "hello", "world")
    result = cache.get("openai", "gpt-4", "hello")
    
    assert result == "world"


def test_cache_miss():
    """测试缓存未命中"""
    from core.cache import LLMCache, CacheConfig
    
    config = CacheConfig(ttl_seconds=60, max_size=10)
    cache = LLMCache(config)
    
    result = cache.get("openai", "gpt-4", "not_in_cache")
    assert result is None


def test_cache_size_limit():
    """测试缓存大小限制"""
    from core.cache import LLMCache, CacheConfig
    
    config = CacheConfig(ttl_seconds=3600, max_size=3)
    cache = LLMCache(config)
    
    # 添加 4 个
    cache.set("test", "model", "key1", "val1")
    cache.set("test", "model", "key2", "val2")
    cache.set("test", "model", "key3", "val3")
    cache.set("test", "model", "key4", "val4")
    
    # 应该不超过 max_size
    assert cache.size <= 3


def test_cache_delete():
    """测试删除缓存"""
    from core.cache import LLMCache, CacheConfig
    
    config = CacheConfig(ttl_seconds=60, max_size=10)
    cache = LLMCache(config)
    
    cache.set("test", "model", "key", "val")
    assert cache.get("test", "model", "key") == "val"
    
    # 删除
    deleted = cache.delete("test", "model", "key")
    assert deleted is True
    
    # 应该没有了
    assert cache.get("test", "model", "key") is None


def test_cache_stats():
    """测试缓存统计"""
    from core.cache import LLMCache, CacheConfig
    
    config = CacheConfig(ttl_seconds=60, max_size=10)
    cache = LLMCache(config)
    
    # 一些操作
    cache.set("test", "model", "key1", "val1")
    cache.get("test", "model", "key1")  # 命中
    cache.get("test", "model", "key2")  # 未命中
    
    stats = cache.stats
    assert stats["hits"] >= 1
    assert stats["misses"] >= 1


def test_global_cache():
    """测试全局缓存"""
    from core.cache import get_global_cache
    
    cache1 = get_global_cache()
    cache2 = get_global_cache()
    
    # 应该是单例
    assert cache1 is cache2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
