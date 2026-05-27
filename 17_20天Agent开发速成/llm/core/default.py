# -*- coding: utf-8 -*-
"""
llm.core.default —— 默认 LLM 实例工厂

让调用方无需写厂商名，或用 ProviderName 枚举（避免拼写错误）：

    from llm.core import get_llm, ProviderName

    print(get_llm().generate("你好"))                       # 零参数
    print(get_llm(ProviderName.DEEPSEEK).generate("你好"))  # 枚举
    print(get_llm("deepseek").generate("你好"))             # 字符串（兼容）

厂商解析优先级（在本模块内部完成，调用方不感知）：
    1. 显式入参 provider=（ProviderName 或 str）
    2. 环境变量 LLM_PROVIDER
    3. 配置文件 llm/core/llm_config.yaml 里的 default_provider
    4. 兜底 "ollama"

apikey 由各 XxxClient.__init__ 自动 os.getenv 拿，无需调用方关心。

新增：支持 backend 解析（一键配置底层实现）
    from llm.core import set_default_backend, get_llm
    set_default_backend("openai_sdk")  # 全局设置
    client = get_llm("deepseek")       # 自动使用 openai_sdk
"""

from __future__ import annotations

import os
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Optional, Union

from .factory import create_llm, create_async_llm, _registry
from .backend import (
    BackendType,
    BackendLike,
    resolve_backend as _resolve_backend,
    _get_backend_from_yaml_provider,
    _get_backend_from_yaml_default,
    _BackendGlobal
)
from .logging_utils import get_logger

# 模块级日志器
_logger = get_logger("default")


PROVIDER_ENV = "LLM_PROVIDER"
BACKEND_ENV = "LLM_BACKEND"
CONFIG_PATH = Path(__file__).with_name("llm_config.yaml")
FALLBACK_PROVIDER = "ollama"


def _read_default_from_yaml() -> Optional[str]:
    """尝试从 llm_config.yaml 读 default_provider，读不到返回 None"""
    if not CONFIG_PATH.exists():
        return None
    try:
        from .config import load_config
        return load_config(str(CONFIG_PATH)).default_provider
    except Exception as e:
        _logger.warning("YAML 配置读取失败: path=%s error=%s: %s", CONFIG_PATH, type(e).__name__, e)
        return None


def _normalize(provider) -> Optional[str]:
    """把 str / ProviderName / None 统一成小写 str 或 None"""
    if provider is None:
        return None
    if isinstance(provider, Enum):
        return str(provider.value).strip().lower()
    return str(provider).strip().lower()


def resolve_provider(provider=None) -> str:
    """按优先级解析当前提供商名

    1. 显式入参（str 或 ProviderName）
    2. 环境变量 LLM_PROVIDER
    3. llm_config.yaml 里的 default_provider
    4. 兜底 "ollama"
    """
    name = _normalize(provider)
    if name:
        _logger.debug("Provider 解析: source=入参 value=%s", name)
        return name

    env_val = os.getenv(PROVIDER_ENV, "").strip().lower()
    if env_val:
        _logger.debug("Provider 解析: source=环境变量 value=%s", env_val)
        return env_val

    yaml_val = _read_default_from_yaml()
    if yaml_val:
        _logger.debug("Provider 解析: source=YAML value=%s", yaml_val.strip().lower())
        return yaml_val.strip().lower()

    _logger.debug("Provider 解析: source=兜底 value=%s", FALLBACK_PROVIDER)
    return FALLBACK_PROVIDER


# ========== 新增：Backend 解析支持 ==========

def resolve_provider_and_backend(
    provider: Optional[Union[str, Enum]] = None,
    backend: Optional[BackendLike] = None,
    is_async: bool = False
) -> tuple[str, BackendType]:
    """
    按优先级解析 provider 和 backend

    Args:
        provider: 厂商名称（可选）
        backend: 底层实现类型（可选）
        is_async: 是否为异步模式

    Returns:
        (provider_name, backend_type) 元组
    """
    # 解析 provider
    provider_name = resolve_provider(provider)

    # 解析 backend
    backend_type = _resolve_backend(
        backend=backend,
        provider=provider_name,
        is_async=is_async
    )

    return provider_name, backend_type


# —— 缓存层 ——
# 把缓存 key 锁定为「解析后的字符串」，这样
#   get_llm()、get_llm(ProviderName.OLLAMA)、get_llm("ollama")
# 三种写法在解析为同一个 name + backend 后，会命中同一个实例。
@lru_cache(maxsize=16)
def _build_sync(name: str, backend: Optional[str] = None):
    """构建同步 LLM 实例"""
    # 使用 factory 模块的 create_llm 函数创建实例
    if backend:
        return create_llm(name, implementation=backend)
    return create_llm(name)


@lru_cache(maxsize=16)
def _build_async(name: str, backend: Optional[str] = None):
    """构建异步 LLM 实例"""
    # 使用 factory 模块的 create_async_llm 函数创建实例
    if backend:
        return create_async_llm(name, implementation=backend)
    return create_async_llm(name)


def get_llm(provider=None, backend: Optional[BackendLike] = None):
    """获取默认同步 LLM 实例（支持 backend 选择）

    等价入参（None / ProviderName / str）会命中同一个缓存实例。

    Args:
        provider: 厂商名称（None / ProviderName / str）
        backend: 底层实现类型（可选，默认使用全局配置）

    Returns:
        同步 LLM 适配器实例
    """
    provider_name, backend_type = resolve_provider_and_backend(
        provider=provider,
        backend=backend,
        is_async=False
    )
    return _build_sync(provider_name, backend_type.value)


def get_async_llm(provider=None, backend: Optional[BackendLike] = None):
    """获取默认异步 LLM 实例（支持 backend 选择）

    Args:
        provider: 厂商名称（None / ProviderName / str）
        backend: 底层实现类型（可选，默认使用全局配置）

    Returns:
        异步 LLM 适配器实例
    """
    provider_name, backend_type = resolve_provider_and_backend(
        provider=provider,
        backend=backend,
        is_async=True
    )
    return _build_async(provider_name, backend_type.value)


def current_provider() -> str:
    """返回当前 get_llm() 实际会用的厂商名（用于日志/排查）"""
    return resolve_provider()


def current_backend() -> Optional[BackendType]:
    """返回当前默认 backend（用于日志/排查）"""
    return _BackendGlobal().get()
