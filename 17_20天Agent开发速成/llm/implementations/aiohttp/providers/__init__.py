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
)
from .ollama import AsyncOllamaClient
from .openai import AsyncOpenAIClient
from .anthropic import AsyncAnthropicClient
from .doubao import AsyncDoubaoClient
from .qwen import AsyncQwenClient
from .glm import AsyncGLMClient
from .wenxin import AsyncWenxinClient
from .kimi import AsyncKimiClient
from .deepseek import AsyncDeepSeekClient
from .minimax import AsyncMiniMaxClient
from .xai import AsyncXAIClient
from .cohere import AsyncCohereClient
from .hunyuan import AsyncHunyuanOpenAIClient
from .pangu import AsyncPanguClient
from .mistral import AsyncMistralClient
from .together import AsyncTogetherClient
from .milm import AsyncMiLMClient
from .google import AsyncGoogleClient
from .meta import AsyncMetaClient
from .shangtang import AsyncShangtangClient
from .stepfun import AsyncStepfunClient
from .tiangong import AsyncTiangongClient
from .spark import AsyncSparkClient
from .baichuan import AsyncBaichuanClient
from .yi import AsyncYiClient

__all__ = [
    # 基础类
    "AsyncLLMResponse",
    "BaseAsyncLLMClient",
    # 厂商客户端
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
    "ollama": AsyncOllamaClient,
    "openai": AsyncOpenAIClient,
    "anthropic": AsyncAnthropicClient,
    "doubao": AsyncDoubaoClient,
    "qwen": AsyncQwenClient,
    "glm": AsyncGLMClient,
    "wenxin": AsyncWenxinClient,
    "kimi": AsyncKimiClient,
    "deepseek": AsyncDeepSeekClient,
    "minimax": AsyncMiniMaxClient,
    "xai": AsyncXAIClient,
    "cohere": AsyncCohereClient,
    "hunyuan": AsyncHunyuanOpenAIClient,
    "pangu": AsyncPanguClient,
    "mistral": AsyncMistralClient,
    "together": AsyncTogetherClient,
    "milm": AsyncMiLMClient,
    "google": AsyncGoogleClient,
    "meta": AsyncMetaClient,
    "shangtang": AsyncShangtangClient,
    "stepfun": AsyncStepfunClient,
    "tiangong": AsyncTiangongClient,
    "spark": AsyncSparkClient,
    "baichuan": AsyncBaichuanClient,
    "yi": AsyncYiClient,
}


def create_client(provider: str, **kwargs) -> BaseAsyncLLMClient:
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
