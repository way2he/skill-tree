# -*- coding: utf-8 -*-
"""
LLM 统一接口层 - 工厂与注册表

提供提供者注册和创建功能。
支持使用 UnifiedAdapter 统一包装底层 Provider。

使用示例:
    from llm.core.factory import create_llm, register_provider

    # 注册提供者
    from llm.implementations.requests.providers import OpenAIProvider
    register_provider("openai", OpenAIProvider)

    # 创建实例
    llm = create_llm("openai", api_key="xxx")

    # 使用
    result = llm.generate("Hello")
"""

from typing import Any, Callable, Type, Optional

from .exceptions import LLMProviderNotFoundError
from .adapter import UnifiedAdapter, IProviderClient
from .logging_utils import get_logger

# 模块级日志器
_logger = get_logger("factory")

# 默认实现方式
_DEFAULT_IMPLEMENTATION = "requests"


class ProviderRegistry:
    """
    提供者注册表

    管理提供者的注册和创建。
    """

    def __init__(self) -> None:
        """初始化注册表"""
        self._providers: dict[str, Type[IProviderClient]] = {}

    def register(
        self,
        name: str,
        provider_class: Type[IProviderClient]
    ) -> None:
        """
        注册提供者

        Args:
            name: 提供者名称
            provider_class: Provider 类（实现 IProviderClient）
        """
        self._providers[name] = provider_class
        _logger.debug("Provider 注册: name=%s class=%s", name, provider_class.__name__)

    def create(self, name: str, **kwargs: Any) -> UnifiedAdapter:
        """
        创建 UnifiedAdapter 实例

        Args:
            name: 提供者名称
            **kwargs: Provider 构造参数

        Returns:
            UnifiedAdapter 实例
        """
        if name not in self._providers:
            supported = list(self._providers.keys())
            _logger.error("Provider 未找到: name=%s supported=%s", name, supported)
            raise LLMProviderNotFoundError(
                f"未知提供者: {name}，支持的选项: {supported}",
                provider=name
            )

        # 创建底层 Provider
        provider_class = self._providers[name]
        provider = provider_class(**kwargs)

        # 包装为 UnifiedAdapter
        adapter = UnifiedAdapter(provider)
        _logger.info("Provider 创建成功: name=%s", name)
        return adapter

    def list_providers(self) -> list[str]:
        """列出所有已注册的提供者"""
        return list(self._providers.keys())

    def get_provider_class(self, name: str) -> Type[IProviderClient]:
        """获取提供者类"""
        if name not in self._providers:
            raise LLMProviderNotFoundError(
                f"未知提供者: {name}",
                provider=name
            )
        return self._providers[name]


# =============================================================================
# 全局注册表
# =============================================================================

_registry = ProviderRegistry()


# =============================================================================
# 便捷函数
# =============================================================================

def register_provider(
    name: str,
    provider_class: Type[IProviderClient]
) -> None:
    """
    注册提供者（便捷函数）

    Args:
        name: 提供者名称
        provider_class: Provider 类
    """
    _registry.register(name, provider_class)


def create_llm(name: str, implementation: Optional[str] = None, **kwargs: Any) -> UnifiedAdapter:
    """
    创建 LLM 实例（便捷函数）

    Args:
        name: 提供者名称
        implementation: 实现方式（"requests" | "aiohttp" | "openai_sdk" | ...）
        **kwargs: Provider 构造参数

    Returns:
        UnifiedAdapter 实例

    Example:
        from llm.core.factory import create_llm

        # 使用默认实现（requests）
        openai = create_llm("openai", api_key="sk-xxx")

        # 切换到 aiohttp 实现
        openai = create_llm("openai", implementation="aiohttp", api_key="sk-xxx")

        # 切换到 OpenAI SDK 实现
        openai = create_llm("openai", implementation="openai_sdk", api_key="sk-xxx")

        # 使用
        result = openai.generate("Hello")
        async_result = await openai.agenerate("Hello")
    """
    impl = implementation or _DEFAULT_IMPLEMENTATION
    
    # 先尝试按实现方式动态导入
    if impl != "requests":
        try:
            _try_register_implementation(impl)
        except ImportError:
            pass
    
    return _registry.create(name, **kwargs)


def list_providers() -> list[str]:
    """
    列出所有已注册的提供者

    Returns:
        提供者名称列表
    """
    return _registry.list_providers()


def list_async_providers() -> list[str]:
    """
    列出所有已注册的异步提供者

    注意：UnifiedAdapter 同时支持同步和异步调用，
    所以所有提供者都支持异步。

    Returns:
        提供者名称列表
    """
    return _registry.list_providers()


def create_async_llm(name: str, **kwargs: Any) -> UnifiedAdapter:
    """
    创建异步 LLM 实例（便捷函数）

    注意：返回的 UnifiedAdapter 同时支持同步和异步调用。
    异步调用请使用 await adapter.agenerate()。

    Args:
        name: 提供者名称
        **kwargs: Provider 构造参数

    Returns:
        UnifiedAdapter 实例
    """
    return _registry.create(name, **kwargs)


# =============================================================================
# 实现方式切换支持
# =============================================================================

def _try_register_implementation(implementation: str) -> None:
    """尝试注册指定实现方式的 providers"""
    try:
        if implementation == "requests":
            from llm.implementations.requests.providers import (
                OpenAIProvider,
                AnthropicProvider,
                DeepSeekProvider,
                QwenProvider,
                GLMProvider,
                KimiProvider,
                DoubaoProvider,
                WenxinProvider,
                HunyuanProvider,
                MiniMaxProvider,
                CohereProvider,
                OllamaProvider,
                MistralProvider,
                TogetherProvider,
                MiLMProvider,
                XAIProvider,
                GoogleProvider,
                MetaProvider,
                ShangtangProvider,
                StepfunProvider,
                TiangongProvider,
                SparkProvider,
                BaichuanProvider,
                YiProvider,
                PanguProvider,
            )
            providers = [
                ("openai", OpenAIProvider),
                ("anthropic", AnthropicProvider),
                ("deepseek", DeepSeekProvider),
                ("qwen", QwenProvider),
                ("glm", GLMProvider),
                ("kimi", KimiProvider),
                ("doubao", DoubaoProvider),
                ("wenxin", WenxinProvider),
                ("hunyuan", HunyuanProvider),
                ("minimax", MiniMaxProvider),
                ("cohere", CohereProvider),
                ("ollama", OllamaProvider),
                ("mistral", MistralProvider),
                ("together", TogetherProvider),
                ("milm", MiLMProvider),
                ("xai", XAIProvider),
                ("google", GoogleProvider),
                ("meta", MetaProvider),
                ("shangtang", ShangtangProvider),
                ("stepfun", StepfunProvider),
                ("tiangong", TiangongProvider),
                ("spark", SparkProvider),
                ("baichuan", BaichuanProvider),
                ("yi", YiProvider),
                ("pangu", PanguProvider),
            ]
            for name, provider_class in providers:
                register_provider(name, provider_class)
        
        elif implementation == "aiohttp":
            from llm.implementations.aiohttp.providers import (
                OpenAIProvider,
                AnthropicProvider,
                QwenProvider,
                GLMProvider,
                DoubaoProvider,
                WenxinProvider,
                DeepSeekProvider,
                KimiProvider,
                HunyuanProvider,
                MiniMaxProvider,
                CohereProvider,
                OllamaProvider,
                MistralProvider,
                TogetherProvider,
                MiLMProvider,
                XAIProvider,
                GoogleProvider,
                MetaProvider,
                ShangtangProvider,
                StepfunProvider,
                TiangongProvider,
                SparkProvider,
                BaichuanProvider,
                YiProvider,
                PanguProvider,
            )
            providers = [
                ("openai", OpenAIProvider),
                ("anthropic", AnthropicProvider),
                ("deepseek", DeepSeekProvider),
                ("qwen", QwenProvider),
                ("glm", GLMProvider),
                ("kimi", KimiProvider),
                ("doubao", DoubaoProvider),
                ("wenxin", WenxinProvider),
                ("hunyuan", HunyuanProvider),
                ("minimax", MiniMaxProvider),
                ("cohere", CohereProvider),
                ("ollama", OllamaProvider),
                ("mistral", MistralProvider),
                ("together", TogetherProvider),
                ("milm", MiLMProvider),
                ("xai", XAIProvider),
                ("google", GoogleProvider),
                ("meta", MetaProvider),
                ("shangtang", ShangtangProvider),
                ("stepfun", StepfunProvider),
                ("tiangong", TiangongProvider),
                ("spark", SparkProvider),
                ("baichuan", BaichuanProvider),
                ("yi", YiProvider),
                ("pangu", PanguProvider),
            ]
            for name, provider_class in providers:
                register_provider(name, provider_class)
        
        elif implementation == "openai_sdk":
            from llm.implementations.openai_sdk.providers import (
                OpenAIProvider,
                OllamaProvider,
                DeepSeekProvider,
                QwenProvider,
                DoubaoProvider,
                GLMProvider,
                KimiProvider,
                MiniMaxProvider,
                MiLMProvider,
                TogetherProvider,
                XAIProvider,
                MistralProvider,
                ShangtangProvider,
                StepfunProvider,
                TiangongProvider,
                BaichuanProvider,
                YiProvider,
                SparkProvider,
                MetaProvider,
            )
            providers = [
                ("openai", OpenAIProvider),
                ("ollama", OllamaProvider),
                ("deepseek", DeepSeekProvider),
                ("qwen", QwenProvider),
                ("doubao", DoubaoProvider),
                ("glm", GLMProvider),
                ("kimi", KimiProvider),
                ("minimax", MiniMaxProvider),
                ("milm", MiLMProvider),
                ("together", TogetherProvider),
                ("xai", XAIProvider),
                ("mistral", MistralProvider),
                ("shangtang", ShangtangProvider),
                ("stepfun", StepfunProvider),
                ("tiangong", TiangongProvider),
                ("baichuan", BaichuanProvider),
                ("yi", YiProvider),
                ("spark", SparkProvider),
                ("meta", MetaProvider),
            ]
            for name, provider_class in providers:
                register_provider(name, provider_class)
        
        elif implementation == "anthropic_sdk":
            from llm.implementations.anthropic_sdk.providers.anthropic import AnthropicProvider
            register_provider("anthropic", AnthropicProvider)
        
        elif implementation == "qwen_sdk":
            from llm.implementations.qwen_sdk.providers.qwen import QwenProvider
            register_provider("qwen", QwenProvider)
        
        elif implementation == "glm_sdk":
            from llm.implementations.glm_sdk.providers.glm import GLMProvider
            register_provider("glm", GLMProvider)
        
        elif implementation == "wenxin_sdk":
            from llm.implementations.wenxin_sdk.providers.wenxin import WenxinProvider
            register_provider("wenxin", WenxinProvider)
        
        elif implementation == "doubao_sdk":
            from llm.implementations.doubao_sdk.providers.doubao import DoubaoProvider
            register_provider("doubao", DoubaoProvider)
    
    except ImportError as e:
        _logger.warning("实现方式导入失败: implementation=%s error=%s", implementation, e)


# =============================================================================
# 内置注册
# =============================================================================

def _register_builtin_providers() -> None:
    """注册内置提供者（默认使用 requests 实现）"""
    _logger.debug("开始注册内置 providers: implementation=%s", _DEFAULT_IMPLEMENTATION)
    _try_register_implementation(_DEFAULT_IMPLEMENTATION)
    _logger.debug("内置 providers 注册完成: count=%d", len(_registry.list_providers()))


# 注册内置提供者
_register_builtin_providers()
