# -*- coding: utf-8 -*-
"""
异步 LLM 客户端 providers 模块

支持的厂商：
- 国际厂商: OpenAI, Anthropic, Google, Meta, Cohere, Mistral, Together, XAI
- 国内大厂: 阿里云(通义千问), 百度(文心一言), 字节跳动(豆包), 腾讯(混元), 华为(盘古), 科大讯飞(星火), 小米
- 国内创业公司: DeepSeek, 智谱AI(GLM), 月之暗面(Kimi), MiniMax, 百川智能, 零一万物
- 其他厂商: 商汤科技, 阶跃星辰, 昆仑万维(天工)
"""

from .base import (
    AsyncLLMResponse,
    BaseAsyncLLMClient,
    BaseAsyncProviderClient,
)
from .ollama import OllamaProvider, AsyncOllamaClient
from .openai import OpenAIProvider, AsyncOpenAIClient
from .anthropic import AnthropicProvider, AsyncAnthropicClient
from .doubao import DoubaoProvider, AsyncDoubaoClient
from .qwen import QwenProvider, AsyncQwenClient
from .glm import GLMProvider, AsyncGLMClient
from .wenxin import WenxinProvider, AsyncWenxinClient
from .kimi import KimiProvider, AsyncKimiClient
from .deepseek import DeepSeekProvider, AsyncDeepSeekClient
from .minimax import MiniMaxProvider, AsyncMiniMaxClient
from .xai import XAIProvider, AsyncXAIClient
from .cohere import CohereProvider, AsyncCohereClient
from .hunyuan import HunyuanProvider, AsyncHunyuanOpenAIClient
from .pangu import PanguProvider, AsyncPanguClient
from .mistral import MistralProvider, AsyncMistralClient
from .together import TogetherProvider, AsyncTogetherClient
from .milm import MiLMProvider, AsyncMiLMClient
from .google import GoogleProvider, AsyncGoogleClient
from .meta import MetaProvider, AsyncMetaClient
from .shangtang import ShangtangProvider, AsyncShangtangClient
from .stepfun import StepfunProvider, AsyncStepfunClient
from .tiangong import TiangongProvider, AsyncTiangongClient
from .spark import SparkProvider, AsyncSparkClient
from .baichuan import BaichuanProvider, AsyncBaichuanClient
from .yi import YiProvider, AsyncYiClient

__all__ = [
    # 基础类
    "AsyncLLMResponse",
    "BaseAsyncLLMClient",
    "BaseAsyncProviderClient",
    # Provider 类（新）
    "OllamaProvider",
    "OpenAIProvider",
    "AnthropicProvider",
    "DoubaoProvider",
    "QwenProvider",
    "GLMProvider",
    "WenxinProvider",
    "KimiProvider",
    "DeepSeekProvider",
    "MiniMaxProvider",
    "XAIProvider",
    "CohereProvider",
    "HunyuanProvider",
    "PanguProvider",
    "MistralProvider",
    "TogetherProvider",
    "MiLMProvider",
    "GoogleProvider",
    "MetaProvider",
    "ShangtangProvider",
    "StepfunProvider",
    "TiangongProvider",
    "SparkProvider",
    "BaichuanProvider",
    "YiProvider",
    # 厂商客户端（向后兼容）
    "AsyncOllamaClient",
    "AsyncOpenAIClient",
    "AsyncAnthropicClient",
    "AsyncDoubaoClient",
    "AsyncQwenClient",
    "AsyncGLMClient",
    "AsyncWenxinClient",
    "AsyncKimiClient",
    "AsyncDeepSeekClient",
    "AsyncMiniMaxClient",
    "AsyncXAIClient",
    "AsyncCohereClient",
    "AsyncHunyuanOpenAIClient",
    "AsyncPanguClient",
    "AsyncMistralClient",
    "AsyncTogetherClient",
    "AsyncMiLMClient",
    "AsyncGoogleClient",
    "AsyncMetaClient",
    "AsyncShangtangClient",
    "AsyncStepfunClient",
    "AsyncTiangongClient",
    "AsyncSparkClient",
    "AsyncBaichuanClient",
    "AsyncYiClient",
    # 工厂函数
    "create_client",
]


_CLIENT_MAP = {
    "ollama": OllamaProvider,
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "doubao": DoubaoProvider,
    "qwen": QwenProvider,
    "glm": GLMProvider,
    "wenxin": WenxinProvider,
    "kimi": KimiProvider,
    "deepseek": DeepSeekProvider,
    "minimax": MiniMaxProvider,
    "xai": XAIProvider,
    "cohere": CohereProvider,
    "hunyuan": HunyuanProvider,
    "pangu": PanguProvider,
    "mistral": MistralProvider,
    "together": TogetherProvider,
    "milm": MiLMProvider,
    "google": GoogleProvider,
    "meta": MetaProvider,
    "shangtang": ShangtangProvider,
    "stepfun": StepfunProvider,
    "tiangong": TiangongProvider,
    "spark": SparkProvider,
    "baichuan": BaichuanProvider,
    "yi": YiProvider,
}


def create_client(provider: str, **kwargs) -> BaseAsyncProviderClient:
    """异步 LLM 客户端工厂函数。

    Args:
        provider: 提供商名称（小写），如 "openai", "deepseek", "qwen" 等
        **kwargs: 传递给客户端的参数

    Returns:
        对应的异步 LLM 客户端实例

    Raises:
        ValueError: provider 未注册
    """
    name = provider.lower()
    if name not in _CLIENT_MAP:
        raise ValueError(
            f"不支持的 async provider: {provider}，可选: {list(_CLIENT_MAP.keys())}"
        )
    return _CLIENT_MAP[name](**kwargs)
