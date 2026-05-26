# -*- coding: utf-8 -*-
"""
LLM Providers - 各厂商 Provider 实现

导出所有厂商的 Provider 类。

使用示例:
    from llm.requests.providers import OpenAIProvider, AnthropicProvider

    # 直接使用
    openai = OpenAIProvider(api_key="xxx")
    result = openai.generate("Hello")

    # 通过 UnifiedAdapter 使用
    from llm.core.adapter import UnifiedAdapter
    adapter = UnifiedAdapter(openai)
"""

from typing import Any

# 导入所有 Provider 类
from .openai import OpenAIProvider, OpenAIClient  # noqa: F401
from .anthropic import AnthropicProvider, AnthropicClient  # noqa: F401
from .deepseek import DeepSeekProvider, DeepSeekClient  # noqa: F401
from .qwen import QwenProvider, QwenClient  # noqa: F401
from .glm import GLMProvider, GLMClient  # noqa: F401
from .kimi import KimiProvider, KimiClient  # noqa: F401
from .doubao import DoubaoProvider, DoubaoClient  # noqa: F401
from .wenxin import WenxinProvider, WenxinClient  # noqa: F401
from .hunyuan import HunyuanProvider, HunyuanClient  # noqa: F401
from .minimax import MiniMaxProvider, MiniMaxClient  # noqa: F401
from .cohere import CohereProvider, CohereClient  # noqa: F401
from .ollama import OllamaProvider, OllamaClient  # noqa: F401
from .mistral import MistralProvider, MistralClient  # noqa: F401
from .together import TogetherProvider, TogetherClient  # noqa: F401
from .milm import MiLMProvider, MiLMClient  # noqa: F401
from .xai import XAIProvider, XAIClient  # noqa: F401
from .google import GoogleProvider, GoogleClient  # noqa: F401
from .meta import MetaProvider, MetaClient  # noqa: F401
from .shangtang import ShangtangProvider, ShangtangClient  # noqa: F401
from .stepfun import StepfunProvider, StepfunClient  # noqa: F401
from .tiangong import TiangongProvider, TiangongClient  # noqa: F401
from .spark import SparkProvider, SparkClient  # noqa: F401
from .baichuan import BaichuanProvider, BaichuanClient  # noqa: F401
from .yi import YiProvider, YiClient  # noqa: F401
from .pangu import PanguProvider, PanguClient  # noqa: F401

# 基础类
from .base import BaseProviderClient, BaseLLMClient, LLMResponse  # noqa: F401


# =============================================================================
# 工厂函数
# =============================================================================

def create_client(provider_name: str, **kwargs: Any) -> BaseProviderClient:
    """
    创建 LLM 客户端（工厂函数）

    Args:
        provider_name: 厂商名称
        **kwargs: 客户端构造参数

    Returns:
        Provider 实例
    """
    provider_map: dict[str, type] = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "deepseek": DeepSeekProvider,
        "qwen": QwenProvider,
        "glm": GLMProvider,
        "kimi": KimiProvider,
        "doubao": DoubaoProvider,
        "wenxin": WenxinProvider,
        "hunyuan": HunyuanProvider,
        "minimax": MiniMaxProvider,
        "cohere": CohereProvider,
        "ollama": OllamaProvider,
        "mistral": MistralProvider,
        "together": TogetherProvider,
        "milm": MiLMProvider,
        "xai": XAIProvider,
        "google": GoogleProvider,
        "meta": MetaProvider,
        "shangtang": ShangtangProvider,
        "stepfun": StepfunProvider,
        "tiangong": TiangongProvider,
        "spark": SparkProvider,
        "baichuan": BaichuanProvider,
        "yi": YiProvider,
        "pangu": PanguProvider,
    }

    cls = provider_map.get(provider_name)
    if cls is None:
        raise ValueError(
            f"未知厂商: {provider_name}，"
            f"支持的厂商: {list(provider_map.keys())}"
        )
    return cls(**kwargs)

__all__ = [
    # Provider 类
    "OpenAIProvider",
    "AnthropicProvider",
    "DeepSeekProvider",
    "QwenProvider",
    "GLMProvider",
    "KimiProvider",
    "DoubaoProvider",
    "WenxinProvider",
    "HunyuanProvider",
    "MiniMaxProvider",
    "CohereProvider",
    "OllamaProvider",
    "MistralProvider",
    "TogetherProvider",
    "MiLMProvider",
    "XAIProvider",
    "GoogleProvider",
    "MetaProvider",
    "ShangtangProvider",
    "StepfunProvider",
    "TiangongProvider",
    "SparkProvider",
    "BaichuanProvider",
    "YiProvider",
    "PanguProvider",
    # 向后兼容别名
    "OpenAIClient",
    "AnthropicClient",
    "DeepSeekClient",
    "QwenClient",
    "GLMClient",
    "KimiClient",
    "DoubaoClient",
    "WenxinClient",
    "HunyuanClient",
    "MiniMaxClient",
    "CohereClient",
    "OllamaClient",
    "MistralClient",
    "TogetherClient",
    "MiLMClient",
    "XAIClient",
    "GoogleClient",
    "MetaClient",
    "ShangtangClient",
    "StepfunClient",
    "TiangongClient",
    "SparkClient",
    "BaichuanClient",
    "YiClient",
    "PanguClient",
    # 基础类
    "BaseProviderClient",
    "BaseLLMClient",
    "LLMResponse",
    # 工厂函数
    "create_client",
]
