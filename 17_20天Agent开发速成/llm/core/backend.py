# -*- coding: utf-8 -*-
"""
LLM 底层实现选择器

支持灵活选择底层实现方式：
- requests: 使用 requests 库同步 HTTP 调用
- aiohttp: 使用 aiohttp 库异步 HTTP 调用
- openai_sdk: 使用 OpenAI 官方 SDK
- native_sdk: 使用厂商自己的 SDK

一键配置功能：
- 环境变量 LLM_BACKEND
- YAML 配置 default_backend
- 代码全局设置 set_default_backend()

使用示例：
    # 一键配置（全局生效）
    from llm.core import set_default_backend, get_llm
    set_default_backend("openai_sdk")
    client = get_llm("deepseek")  # 自动使用 openai_sdk

    # Builder 模式
    from llm.core import LLMClientBuilder
    client = (LLMClientBuilder()
        .provider("deepseek")
        .openai_sdk()
        .api_key("sk-xxx")
        .build())

    # 运行时切换
    from llm.core import BackendSwitcher
    switcher = BackendSwitcher("deepseek").add_backend("requests").add_backend("openai_sdk")
    switcher.switch_to("openai_sdk")
    client = switcher.get_client()
"""

from __future__ import annotations

import os
import threading
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .exceptions import LLMConfigError, LLMProviderNotFoundError
from .logging_utils import get_logger

# 模块级日志器
_logger = get_logger("backend")


# =============================================================================
# BackendType 枚举
# =============================================================================

class BackendType(str, Enum):
    """
    底层实现类型枚举

    定义了四种底层实现方式：
    - REQUESTS: 使用 requests 库同步 HTTP 调用
    - AIOHTTP: 使用 aiohttp 库异步 HTTP 调用
    - OPENAI_SDK: 使用 OpenAI 官方 SDK
    - NATIVE_SDK: 使用厂商自己的 SDK（如 anthropic、google 等）
    """

    REQUESTS = "requests"
    AIOHTTP = "aiohttp"
    OPENAI_SDK = "openai_sdk"
    NATIVE_SDK = "native_sdk"

    @classmethod
    def from_string(cls, value: str) -> "BackendType":
        """
        从字符串解析实现类型

        Args:
            value: 字符串值（支持多种别名）

        Returns:
            BackendType 枚举值

        Raises:
            ValueError: 无效的实现类型
        """
        mapping = {
            # requests 别名
            "requests": cls.REQUESTS,
            "request": cls.REQUESTS,
            "http": cls.REQUESTS,
            "sync": cls.REQUESTS,
            # aiohttp 别名
            "aiohttp": cls.AIOHTTP,
            "async": cls.AIOHTTP,
            "asyncio": cls.AIOHTTP,
            # openai_sdk 别名
            "openai_sdk": cls.OPENAI_SDK,
            "openai": cls.OPENAI_SDK,
            "openai-sdk": cls.OPENAI_SDK,
            # native_sdk 别名
            "native_sdk": cls.NATIVE_SDK,
            "native": cls.NATIVE_SDK,
            "native-sdk": cls.NATIVE_SDK,
            "sdk": cls.NATIVE_SDK,
        }

        normalized = value.lower().strip().replace("-", "_")
        if normalized not in mapping:
            raise ValueError(
                f"无效的实现类型: {value}，"
                f"支持的选项: {[e.value for e in cls]}"
            )
        return mapping[normalized]

    def is_async(self) -> bool:
        """
        判断是否为异步实现

        Returns:
            True 表示异步实现，False 表示同步实现
        """
        return self == BackendType.AIOHTTP

    def is_sdk(self) -> bool:
        """
        判断是否为 SDK 实现

        Returns:
            True 表示 SDK 实现，False 表示 HTTP 实现
        """
        return self in (BackendType.OPENAI_SDK, BackendType.NATIVE_SDK)


# 类型别名
BackendLike = Union[BackendType, str]
"""实现类型输入：枚举或字符串"""


# =============================================================================
# 全局默认 Backend 管理（线程安全）
# =============================================================================

class _BackendGlobal:
    """
    全局默认 Backend 管理器（内部类）

    线程安全的单例模式，管理全局默认 backend 设置。
    """

    _instance: Optional["_BackendGlobal"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls) -> "_BackendGlobal":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._default_backend: Optional[BackendType] = None
        return cls._instance

    def set(self, backend: BackendLike) -> None:
        """设置全局默认 backend"""
        old = self._default_backend
        if isinstance(backend, BackendType):
            self._default_backend = backend
        else:
            self._default_backend = BackendType.from_string(backend)
        _logger.info("全局 backend 设置: %s -> %s", old, self._default_backend)

    def get(self) -> Optional[BackendType]:
        """获取全局默认 backend"""
        return self._default_backend

    def reset(self) -> None:
        """重置为 None"""
        self._default_backend = None


def set_default_backend(backend: BackendLike) -> None:
    """
    设置全局默认底层实现

    设置后，所有不指定 backend 的客户端创建都会自动使用该实现。

    Args:
        backend: 实现类型（BackendType 枚举或字符串）

    示例：
        >>> from llm.core import set_default_backend
        >>> set_default_backend("openai_sdk")
        >>> # 或
        >>> set_default_backend(BackendType.OPENAI_SDK)
    """
    _BackendGlobal().set(backend)


def get_default_backend() -> Optional[BackendType]:
    """
    获取当前全局默认底层实现

    Returns:
        当前全局默认 backend，未设置则返回 None

    示例：
        >>> from llm.core import get_default_backend
        >>> backend = get_default_backend()
        >>> print(backend)  # BackendType.OPENAI_SDK 或 None
    """
    return _BackendGlobal().get()


def reset_default_backend() -> None:
    """
    重置全局默认底层实现为 None

    重置后，将使用其他方式（环境变量、YAML配置、兜底值）解析 backend。

    示例：
        >>> from llm.core import reset_default_backend
        >>> reset_default_backend()
    """
    _BackendGlobal().reset()


# =============================================================================
# Backend 解析（按优先级）
# =============================================================================

def resolve_backend(
    backend: Optional[BackendLike] = None,
    provider: Optional[str] = None,
    is_async: bool = False
) -> BackendType:
    """
    按优先级解析最终使用的 backend

    优先级（从高到低）：
    1. 显式传入的 backend 参数
    2. YAML 配置中该厂商的 backend 字段
    3. 代码 set_default_backend() 设置的全局默认
    4. 环境变量 LLM_BACKEND
    5. YAML 配置中的 default_backend 字段
    6. 兜底值: requests（同步）/ aiohttp（异步）

    Args:
        backend: 显式指定的 backend（最高优先级）
        provider: 厂商名称（用于读取 YAML 厂商级配置）
        is_async: 是否为异步模式（影响兜底值）

    Returns:
        解析后的 BackendType
    """
    # 1. 显式指定（最高优先级）
    if backend is not None:
        if isinstance(backend, BackendType):
            _logger.debug("Backend 解析: source=显式参数 value=%s", backend.value)
            return backend
        result = BackendType.from_string(backend)
        _logger.debug("Backend 解析: source=显式参数 value=%s", result.value)
        return result

    # 2. YAML 厂商级配置
    if provider:
        yaml_backend = _get_backend_from_yaml_provider(provider)
        if yaml_backend:
            _logger.debug("Backend 解析: source=YAML厂商配置 provider=%s value=%s", provider, yaml_backend.value)
            return yaml_backend

    # 3. 代码全局设置
    global_backend = _BackendGlobal().get()
    if global_backend is not None:
        _logger.debug("Backend 解析: source=全局设置 value=%s", global_backend.value)
        return global_backend

    # 4. 环境变量
    env_backend = os.getenv("LLM_BACKEND", "").strip()
    if env_backend:
        result = BackendType.from_string(env_backend)
        _logger.debug("Backend 解析: source=环境变量 value=%s", result.value)
        return result

    # 5. YAML 全局默认
    yaml_default = _get_backend_from_yaml_default()
    if yaml_default:
        _logger.debug("Backend 解析: source=YAML全局默认 value=%s", yaml_default.value)
        return yaml_default

    # 6. 兜底值
    fallback = BackendType.AIOHTTP if is_async else BackendType.REQUESTS
    _logger.debug("Backend 解析: source=兜底 value=%s (is_async=%s)", fallback.value, is_async)
    return fallback


def _get_backend_from_yaml_provider(provider: str) -> Optional[BackendType]:
    """从 YAML 配置读取厂商级 backend"""
    try:
        from .config import load_config, CONFIG_PATH

        config_path = Path(CONFIG_PATH) if CONFIG_PATH else None
        if not config_path or not config_path.exists():
            return None

        config = load_config(str(config_path))
        provider_config = config.providers.get(provider.lower())
        if provider_config and provider_config.backend:
            return BackendType.from_string(provider_config.backend)
    except Exception as e:
        _logger.debug("YAML backend 配置读取失败: error=%s: %s", type(e).__name__, e)
    return None


def _get_backend_from_yaml_default() -> Optional[BackendType]:
    """从 YAML 配置读取全局默认 backend"""
    try:
        from .config import load_config, CONFIG_PATH

        config_path = Path(CONFIG_PATH) if CONFIG_PATH else None
        if not config_path or not config_path.exists():
            return None

        config = load_config(str(config_path))
        if config.default_backend:
            return BackendType.from_string(config.default_backend)
    except Exception as e:
        _logger.debug("YAML backend 配置读取失败: error=%s: %s", type(e).__name__, e)
    return None


# =============================================================================
# BackendConfig 配置类
# =============================================================================

@dataclass
class BackendConfig:
    """
    实现层配置模型

    封装了创建客户端所需的所有配置信息
    """

    # 基础配置
    provider: str
    """厂商名称（如 openai、deepseek、anthropic）"""

    backend: BackendType = field(default_factory=lambda: BackendType.REQUESTS)
    """底层实现类型"""

    # 认证配置
    api_key: Optional[str] = None
    """API 密钥"""

    base_url: Optional[str] = None
    """API 基础地址"""

    ak: Optional[str] = None
    """Access Key（部分厂商需要）"""

    sk: Optional[str] = None
    """Secret Key（部分厂商需要）"""

    # 模型配置
    model: Optional[str] = None
    """模型名称"""

    system_prompt: Optional[str] = None
    """系统提示词"""

    temperature: Optional[float] = None
    """温度参数"""

    max_tokens: Optional[int] = None
    """最大输出 token 数"""

    timeout: Optional[float] = None
    """请求超时时间（秒）"""

    # 扩展配置
    extra: Dict[str, Any] = field(default_factory=dict)
    """额外参数"""

    def to_kwargs(self) -> Dict[str, Any]:
        """
        转换为客户端构造参数

        Returns:
            过滤掉 None 值的参数字典
        """
        kwargs: Dict[str, Any] = {}

        # 基础参数
        if self.api_key is not None:
            kwargs["api_key"] = self.api_key
        if self.base_url is not None:
            kwargs["base_url"] = self.base_url
        if self.ak is not None:
            kwargs["ak"] = self.ak
        if self.sk is not None:
            kwargs["sk"] = self.sk

        # 模型参数
        if self.model is not None:
            kwargs["model"] = self.model
        if self.system_prompt is not None:
            kwargs["system_prompt"] = self.system_prompt
        if self.temperature is not None:
            kwargs["temperature"] = self.temperature
        if self.max_tokens is not None:
            kwargs["max_tokens"] = self.max_tokens
        if self.timeout is not None:
            kwargs["timeout"] = self.timeout

        # 扩展参数
        kwargs.update(self.extra)

        return kwargs


# =============================================================================
# LLMClientBuilder 构建器
# =============================================================================

class LLMClientBuilder:
    """
    LLM 客户端构建器

    使用 Builder 模式提供流式 API 构建客户端配置

    使用示例：
        # 同步客户端
        client = (LLMClientBuilder()
            .provider("deepseek")
            .backend("requests")
            .api_key("sk-xxx")
            .model("deepseek-chat")
            .build())

        # 异步客户端
        async_client = (LLMClientBuilder()
            .provider("openai")
            .backend(BackendType.AIOHTTP)
            .api_key("sk-xxx")
            .build_async())

        # 使用 OpenAI SDK
        sdk_client = (LLMClientBuilder()
            .provider("deepseek")
            .openai_sdk()
            .api_key("sk-xxx")
            .base_url("https://api.deepseek.com/v1")
            .build())
    """

    def __init__(self) -> None:
        """初始化构建器"""
        self._config = BackendConfig(provider="")

    # ========== 厂商配置 ==========

    def provider(self, name: str) -> "LLMClientBuilder":
        """
        设置厂商名称

        Args:
            name: 厂商名称（如 openai、deepseek、anthropic）

        Returns:
            构建器实例（支持链式调用）
        """
        self._config.provider = name.lower().strip()
        return self

    # ========== 实现层选择 ==========

    def backend(self, backend_type: BackendLike) -> "LLMClientBuilder":
        """
        设置底层实现类型

        Args:
            backend_type: 实现类型（枚举或字符串）

        Returns:
            构建器实例（支持链式调用）

        Raises:
            ValueError: 无效的实现类型
        """
        if isinstance(backend_type, BackendType):
            self._config.backend = backend_type
        else:
            self._config.backend = BackendType.from_string(backend_type)
        return self

    def requests(self) -> "LLMClientBuilder":
        """
        使用 requests 库（同步 HTTP）

        Returns:
            构建器实例（支持链式调用）
        """
        self._config.backend = BackendType.REQUESTS
        return self

    def aiohttp(self) -> "LLMClientBuilder":
        """
        使用 aiohttp 库（异步 HTTP）

        Returns:
            构建器实例（支持链式调用）
        """
        self._config.backend = BackendType.AIOHTTP
        return self

    def openai_sdk(self) -> "LLMClientBuilder":
        """
        使用 OpenAI SDK

        Returns:
            构建器实例（支持链式调用）
        """
        self._config.backend = BackendType.OPENAI_SDK
        return self

    def native_sdk(self) -> "LLMClientBuilder":
        """
        使用厂商原生 SDK

        Returns:
            构建器实例（支持链式调用）
        """
        self._config.backend = BackendType.NATIVE_SDK
        return self

    # ========== 认证配置 ==========

    def api_key(self, key: str) -> "LLMClientBuilder":
        """
        设置 API 密钥

        Args:
            key: API 密钥

        Returns:
            构建器实例（支持链式调用）
        """
        self._config.api_key = key
        return self

    def base_url(self, url: str) -> "LLMClientBuilder":
        """
        设置 API 基础地址

        Args:
            url: API 基础地址

        Returns:
            构建器实例（支持链式调用）
        """
        self._config.base_url = url
        return self

    def credentials(self, ak: str, sk: str) -> "LLMClientBuilder":
        """
        设置 AK/SK 认证信息

        Args:
            ak: Access Key
            sk: Secret Key

        Returns:
            构建器实例（支持链式调用）
        """
        self._config.ak = ak
        self._config.sk = sk
        return self

    # ========== 模型配置 ==========

    def model(self, model_name: str) -> "LLMClientBuilder":
        """
        设置模型名称

        Args:
            model_name: 模型名称

        Returns:
            构建器实例（支持链式调用）
        """
        self._config.model = model_name
        return self

    def system_prompt(self, prompt: str) -> "LLMClientBuilder":
        """
        设置系统提示词

        Args:
            prompt: 系统提示词

        Returns:
            构建器实例（支持链式调用）
        """
        self._config.system_prompt = prompt
        return self

    def temperature(self, temp: float) -> "LLMClientBuilder":
        """
        设置温度参数

        Args:
            temp: 温度值（0-2）

        Returns:
            构建器实例（支持链式调用）

        Raises:
            ValueError: 温度值超出范围
        """
        if not 0 <= temp <= 2:
            raise ValueError(f"温度参数必须在 0-2 之间，当前值: {temp}")
        self._config.temperature = temp
        return self

    def max_tokens(self, tokens: int) -> "LLMClientBuilder":
        """
        设置最大输出 token 数

        Args:
            tokens: 最大 token 数

        Returns:
            构建器实例（支持链式调用）

        Raises:
            ValueError: token 数不合法
        """
        if tokens < 1:
            raise ValueError(f"max_tokens 必须大于 0，当前值: {tokens}")
        self._config.max_tokens = tokens
        return self

    def timeout(self, seconds: float) -> "LLMClientBuilder":
        """
        设置请求超时时间

        Args:
            seconds: 超时秒数

        Returns:
            构建器实例（支持链式调用）

        Raises:
            ValueError: 超时时间不合法
        """
        if seconds <= 0:
            raise ValueError(f"超时时间必须大于 0，当前值: {seconds}")
        self._config.timeout = seconds
        return self

    # ========== 扩展配置 ==========

    def extra(self, **kwargs) -> "LLMClientBuilder":
        """
        设置额外参数

        Args:
            **kwargs: 额外参数键值对

        Returns:
            构建器实例（支持链式调用）
        """
        self._config.extra.update(kwargs)
        return self

    # ========== 构建方法 ==========

    def build(self):
        """
        构建同步客户端

        Returns:
            同步 LLM 适配器实例

        Raises:
            LLMConfigError: 配置错误
            LLMProviderNotFoundError: 厂商未注册
        """
        # 如果没有显式设置 backend，使用解析逻辑
        if not self._config.provider:
            raise LLMConfigError("必须指定厂商名称")

        # 解析最终 backend（如果没有显式设置）
        if self._config.backend == BackendType.REQUESTS and not hasattr(self, '_backend_explicitly_set'):
            # 检查是否显式设置了 backend
            pass  # 保持当前值，由 _create_client_from_config 处理

        return _create_client_from_config(self._config, async_mode=False)

    def build_async(self):
        """
        构建异步客户端

        Returns:
            异步 LLM 适配器实例

        Raises:
            LLMConfigError: 配置错误
            LLMProviderNotFoundError: 厂商未注册
        """
        if not self._config.provider:
            raise LLMConfigError("必须指定厂商名称")

        return _create_client_from_config(self._config, async_mode=True)

    def get_config(self) -> BackendConfig:
        """
        获取当前配置（用于调试）

        Returns:
            当前配置对象
        """
        return self._config

    def reset(self) -> "LLMClientBuilder":
        """
        重置构建器

        Returns:
            构建器实例（支持链式调用）
        """
        self._config = BackendConfig(provider="")
        return self


# =============================================================================
# 客户端创建函数
# =============================================================================

def _create_client_from_config(config: BackendConfig, async_mode: bool = False):
    """
    根据配置创建客户端实例

    Args:
        config: 实现层配置
        async_mode: 是否创建异步客户端

    Returns:
        LLM 适配器实例（UnifiedAdapter）

    Raises:
        LLMConfigError: 配置错误
        LLMProviderNotFoundError: 厂商未注册
    """
    from .factory import create_llm, create_async_llm

    # 验证厂商名称
    if not config.provider:
        raise LLMConfigError("必须指定厂商名称")

    provider_name = config.provider.lower()

    # 解析最终使用的 backend
    final_backend = resolve_backend(
        backend=config.backend,
        provider=provider_name,
        is_async=async_mode
    )

    # 从配置读取参数
    kwargs = config.to_kwargs()

    # 使用 factory 模块创建客户端
    if async_mode:
        return create_async_llm(
            provider_name,
            implementation=final_backend.value,
            **kwargs
        )
    else:
        return create_llm(
            provider_name,
            implementation=final_backend.value,
            **kwargs
        )





# =============================================================================
# 便捷函数
# =============================================================================

def create_client(
    provider: str,
    backend: Optional[BackendLike] = None,
    **kwargs
):
    """
    创建同步客户端（便捷函数）

    一行代码创建客户端：
        client = create_client("deepseek", "requests", api_key="sk-xxx")
        client = create_client("openai", BackendType.OPENAI_SDK, api_key="sk-xxx")

    Args:
        provider: 厂商名称
        backend: 实现类型（默认使用全局配置或 requests）
        **kwargs: 客户端构造参数

    Returns:
        同步 LLM 适配器实例
    """
    builder = LLMClientBuilder()
    builder.provider(provider)

    if backend is not None:
        builder.backend(backend)

    # 处理 kwargs
    for key, value in kwargs.items():
        if hasattr(builder, key) and callable(getattr(builder, key)):
            getattr(builder, key)(value)
        else:
            builder.extra(**{key: value})

    return builder.build()


def create_async_client(
    provider: str,
    backend: Optional[BackendLike] = None,
    **kwargs
):
    """
    创建异步客户端（便捷函数）

    一行代码创建异步客户端：
        async_client = create_async_client("deepseek", "aiohttp", api_key="sk-xxx")

    Args:
        provider: 厂商名称
        backend: 实现类型（默认使用全局配置或 aiohttp）
        **kwargs: 客户端构造参数

    Returns:
        异步 LLM 适配器实例
    """
    builder = LLMClientBuilder()
    builder.provider(provider)

    if backend is not None:
        builder.backend(backend)

    # 处理 kwargs
    for key, value in kwargs.items():
        if hasattr(builder, key) and callable(getattr(builder, key)):
            getattr(builder, key)(value)
        else:
            builder.extra(**{key: value})

    return builder.build_async()


# =============================================================================
# BackendSwitcher 切换器
# =============================================================================

class BackendSwitcher:
    """
    实现层切换器

    支持运行时切换底层实现，适用于：
    - A/B 测试不同实现
    - 故障转移
    - 性能对比

    使用示例：
        switcher = BackendSwitcher("deepseek")
            .add_backend("requests", api_key="sk-xxx")
            .add_backend("openai_sdk", api_key="sk-xxx", base_url="...")

        # 使用默认实现
        client = switcher.get_client()

        # 切换实现
        switcher.switch_to("openai_sdk")
        client = switcher.get_client()

        # 自动故障转移
        client = switcher.get_client_with_fallback(["openai_sdk", "requests"])
    """

    def __init__(self, provider: str) -> None:
        """
        初始化切换器

        Args:
            provider: 厂商名称
        """
        self._provider = provider
        self._backends: Dict[str, BackendConfig] = {}
        self._current_backend: Optional[str] = None
        self._clients: Dict[str, Any] = {}

    def add_backend(
        self,
        backend: BackendLike,
        **kwargs
    ) -> "BackendSwitcher":
        """
        添加实现层配置

        Args:
            backend: 实现类型
            **kwargs: 客户端构造参数

        Returns:
            切换器实例（支持链式调用）
        """
        backend_type = (
            backend if isinstance(backend, BackendType)
            else BackendType.from_string(backend)
        )

        config = BackendConfig(
            provider=self._provider,
            backend=backend_type,
            **kwargs
        )

        self._backends[backend_type.value] = config

        # 如果是第一个实现，设为默认
        if self._current_backend is None:
            self._current_backend = backend_type.value

        return self

    def switch_to(self, backend: BackendLike) -> "BackendSwitcher":
        """
        切换到指定实现

        Args:
            backend: 实现类型

        Returns:
            切换器实例（支持链式调用）

        Raises:
            LLMConfigError: 实现未配置
        """
        backend_value = (
            backend.value if isinstance(backend, BackendType)
            else BackendType.from_string(backend).value
        )

        if backend_value not in self._backends:
            raise LLMConfigError(
                f"实现层未配置: {backend_value}，"
                f"已配置: {list(self._backends.keys())}"
            )

        old_current = self._current_backend
        self._current_backend = backend_value
        _logger.info("BackendSwitcher 切换: provider=%s %s -> %s",
                    self._provider, old_current, backend_value)
        return self

    def get_client(self):
        """
        获取当前实现的客户端

        Returns:
            同步客户端实例
        """
        if self._current_backend is None:
            raise LLMConfigError("未配置任何实现层")

        return self._get_or_create_client(self._current_backend, async_mode=False)

    def get_async_client(self):
        """
        获取当前实现的异步客户端

        Returns:
            异步客户端实例
        """
        if self._current_backend is None:
            raise LLMConfigError("未配置任何实现层")

        return self._get_or_create_client(self._current_backend, async_mode=True)

    def get_client_with_fallback(
        self,
        fallback_order: Optional[List[BackendLike]] = None
    ):
        """
        获取客户端（支持故障转移）

        按优先级尝试创建客户端，成功则返回

        Args:
            fallback_order: 实现优先级列表（默认按添加顺序）

        Returns:
            客户端实例

        Raises:
            LLMConfigError: 所有实现都失败
        """
        order = fallback_order or list(self._backends.keys())
        errors = []

        for backend in order:
            backend_value = (
                backend.value if isinstance(backend, BackendType)
                else BackendType.from_string(backend).value
            )

            try:
                return self._get_or_create_client(backend_value, async_mode=False)
            except Exception as e:
                errors.append(f"{backend_value}: {str(e)}")
                _logger.warning("故障转移失败: backend=%s error=%s: %s", backend_value, type(e).__name__, e)

        raise LLMConfigError(
            f"所有实现层都失败: {', '.join(errors)}"
        )

    def _get_or_create_client(
        self,
        backend: str,
        async_mode: bool
    ):
        """
        获取或创建客户端（带缓存）

        Args:
            backend: 实现类型值
            async_mode: 是否异步

        Returns:
            客户端实例
        """
        cache_key = f"{backend}:{'async' if async_mode else 'sync'}"

        if cache_key not in self._clients:
            config = self._backends[backend]
            client = _create_client_from_config(config, async_mode)
            self._clients[cache_key] = client

        return self._clients[cache_key]

    def list_backends(self) -> List[str]:
        """
        列出所有已配置的实现层

        Returns:
            实现类型列表
        """
        return list(self._backends.keys())

    def current_backend(self) -> Optional[str]:
        """
        获取当前实现类型

        Returns:
            当前实现类型值
        """
        return self._current_backend
