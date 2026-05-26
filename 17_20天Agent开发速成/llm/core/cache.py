# -*- coding: utf-8 -*-
"""
LLM 统一接口层 - 响应缓存

基于内存的 LLM 响应缓存，减少重复 API 调用。
支持 TTL 过期、最大容量限制、手动清除。

使用示例:
    from llm.core.cache import LLMCache, CacheConfig, cached_generate

    # 方式1: 直接使用缓存
    cache = LLMCache(CacheConfig(ttl_seconds=1800))
    result = cache.get("openai", "gpt-4", "Hello")
    if result is None:
        result = provider.generate("Hello")
        cache.set("openai", "gpt-4", "Hello", result)

    # 方式2: 装饰器
    adapter = UnifiedAdapter(client)
    adapter.generate = cached_generate(cache)(adapter.generate)
"""

import hashlib
import json
import threading
import time
from typing import Any, Callable, Dict, Optional

from .types import CacheConfig


# =============================================================================
# LLM 缓存
# =============================================================================

class LLMCache:
    """
    LLM 响应缓存（线程安全）

    基于内存的缓存实现，支持 TTL 过期和容量限制。
    可扩展为 Redis 等外部缓存。

    Attributes:
        config: 缓存配置
        hits: 缓存命中次数
        misses: 缓存未命中次数
    """

    def __init__(self, config: Optional[CacheConfig] = None) -> None:
        """
        初始化缓存

        Args:
            config: 缓存配置，默认使用 CacheConfig()
        """
        self.config = config or CacheConfig()
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

        # 统计
        self._hits: int = 0
        self._misses: int = 0

    def _make_key(
        self,
        provider: str,
        model: str,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """
        生成缓存键

        基于 provider + model + prompt + 参数生成 SHA256 哈希。

        Args:
            provider: 厂商名称
            model: 模型名称
            prompt: 提示词
            **kwargs: 其他参数

        Returns:
            缓存键字符串
        """
        # 过滤掉不影响结果的参数
        filtered_kwargs = {
            k: v for k, v in sorted(kwargs.items())
            if k not in ("stream", "use_cache", "request_id")
        }
        cache_data = {
            "provider": provider,
            "model": model,
            "prompt": prompt,
            "kwargs": filtered_kwargs,
        }
        data_str = json.dumps(cache_data, sort_keys=True, ensure_ascii=False)
        hash_key = hashlib.sha256(data_str.encode("utf-8")).hexdigest()[:16]
        return f"{self.config.key_prefix}:{provider}:{hash_key}"

    def get(
        self,
        provider: str,
        model: str,
        prompt: str,
        **kwargs: Any,
    ) -> Optional[str]:
        """
        获取缓存

        Args:
            provider: 厂商名称
            model: 模型名称
            prompt: 提示词
            **kwargs: 其他参数

        Returns:
            缓存的响应文本，未命中返回 None
        """
        if not self.config.enabled:
            return None

        key = self._make_key(provider, model, prompt, **kwargs)

        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                # 检查是否过期
                if time.time() - entry["timestamp"] < self.config.ttl_seconds:
                    self._hits += 1
                    return entry["value"]
                else:
                    # 删除过期条目
                    del self._cache[key]

        self._misses += 1
        return None

    def set(
        self,
        provider: str,
        model: str,
        prompt: str,
        value: str,
        **kwargs: Any,
    ) -> None:
        """
        设置缓存

        Args:
            provider: 厂商名称
            model: 模型名称
            prompt: 提示词
            value: 响应文本
            **kwargs: 其他参数
        """
        if not self.config.enabled:
            return

        key = self._make_key(provider, model, prompt, **kwargs)

        with self._lock:
            # 容量检查
            if len(self._cache) >= self.config.max_size:
                self._cleanup_locked()

            self._cache[key] = {
                "value": value,
                "timestamp": time.time(),
            }

    def delete(
        self,
        provider: str,
        model: str,
        prompt: str,
        **kwargs: Any,
    ) -> bool:
        """
        删除指定缓存

        Args:
            provider: 厂商名称
            model: 模型名称
            prompt: 提示词
            **kwargs: 其他参数

        Returns:
            是否成功删除
        """
        key = self._make_key(provider, model, prompt, **kwargs)

        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
        return False

    def clear(self) -> None:
        """清空所有缓存"""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0

    def _cleanup_locked(self) -> None:
        """
        清理过期条目（需在锁内调用）

        删除过期条目，如果仍超容量则删除最旧的条目。
        """
        now = time.time()

        # 删除过期条目
        expired_keys = [
            k for k, v in self._cache.items()
            if now - v["timestamp"] > self.config.ttl_seconds
        ]
        for k in expired_keys:
            del self._cache[k]

        # 如果仍然超容量，删除最旧的条目
        if len(self._cache) >= self.config.max_size:
            sorted_items = sorted(
                self._cache.items(),
                key=lambda x: x[1]["timestamp"],
            )
            to_remove = len(self._cache) - self.config.max_size + 1
            for k, _ in sorted_items[:to_remove]:
                del self._cache[k]

    @property
    def size(self) -> int:
        """当前缓存条目数"""
        return len(self._cache)

    @property
    def stats(self) -> dict[str, Any]:
        """
        获取缓存统计

        Returns:
            包含 hits, misses, hit_rate, size 的字典
        """
        total = self._hits + self._misses
        hit_rate = (self._hits / total * 100) if total > 0 else 0.0
        return {
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": round(hit_rate, 1),
            "size": self.size,
            "max_size": self.config.max_size,
        }


# =============================================================================
# 全局缓存实例
# =============================================================================

_global_cache: Optional[LLMCache] = None
_global_cache_lock = threading.Lock()


def get_global_cache() -> LLMCache:
    """
    获取全局缓存实例（单例）

    Returns:
        全局 LLMCache 实例
    """
    global _global_cache
    if _global_cache is None:
        with _global_cache_lock:
            if _global_cache is None:
                _global_cache = LLMCache()
    return _global_cache


# =============================================================================
# 缓存装饰器
# =============================================================================

def cached_generate(
    cache: Optional[LLMCache] = None,
    ttl_seconds: Optional[int] = None,
) -> Callable:
    """
    缓存装饰器工厂

    为 generate 方法添加缓存能力。

    Args:
        cache: 缓存实例，默认使用全局缓存
        ttl_seconds: 覆盖缓存 TTL

    Returns:
        装饰器函数

    Example:
        cache = LLMCache(CacheConfig(ttl_seconds=1800))

        # 装饰实例方法
        adapter.generate = cached_generate(cache)(adapter.generate)
    """

    def decorator(func: Callable) -> Callable:
        import functools

        @functools.wraps(func)
        def wrapper(self: Any, prompt: str, *args: Any, **kwargs: Any) -> str:
            # 跳过流式请求和显式禁用缓存
            if kwargs.get("stream") or not kwargs.get("use_cache", True):
                return func(self, prompt, *args, **kwargs)

            _cache = cache or get_global_cache()
            provider = getattr(self, "provider_name", "unknown")
            model = kwargs.get("model") or getattr(self, "default_model", "unknown")

            # 尝试从缓存获取
            cached = _cache.get(provider, model, prompt, **kwargs)
            if cached is not None:
                return cached

            # 执行实际调用
            result = func(self, prompt, *args, **kwargs)

            # 缓存结果
            _cache.set(provider, model, prompt, result, **kwargs)

            return result

        return wrapper

    return decorator


def async_cached_generate(
    cache: Optional[LLMCache] = None,
    ttl_seconds: Optional[int] = None,
) -> Callable:
    """
    异步缓存装饰器工厂

    为 agenerate 方法添加缓存能力。

    Args:
        cache: 缓存实例，默认使用全局缓存
        ttl_seconds: 覆盖缓存 TTL

    Returns:
        装饰器函数
    """

    def decorator(func: Callable) -> Callable:
        import functools

        @functools.wraps(func)
        async def wrapper(self: Any, prompt: str, *args: Any, **kwargs: Any) -> str:
            if kwargs.get("stream") or not kwargs.get("use_cache", True):
                return await func(self, prompt, *args, **kwargs)

            _cache = cache or get_global_cache()
            provider = getattr(self, "provider_name", "unknown")
            model = kwargs.get("model") or getattr(self, "default_model", "unknown")

            cached = _cache.get(provider, model, prompt, **kwargs)
            if cached is not None:
                return cached

            result = await func(self, prompt, *args, **kwargs)
            _cache.set(provider, model, prompt, result, **kwargs)

            return result

        return wrapper

    return decorator
