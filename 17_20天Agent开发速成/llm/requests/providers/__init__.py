# -*- coding: utf-8 -*-
"""
同步 LLM 客户端 providers 模块

支持的厂商：
- 国际厂商: OpenAI, Anthropic, Google, Meta, Cohere, Mistral, Together, XAI
- 国内大厂: 阿里云(通义千问), 百度(文心一言), 字节跳动(豆包), 腾讯(混元), 华为(盘古), 科大讯飞(星火), 小米
- 国内创业公司: DeepSeek, 智谱AI(GLM), 月之暗面(Kimi), MiniMax, 百川智能, 零一万物
- 其他厂商: 商汤科技, 阶跃星辰, 昆仑万维(天工)

使用示例:
    from llm.requests.providers import (
        OpenAIClient,
        DeepSeekClient,
        QwenClient,
        create_client
    )

    # 创建客户端
    client = OpenAIClient(api_key="sk-xxx")

    # 生成文本
    response = client.generate("你好")
"""

from .base import (
    BaseLLMClient,
    LLMResponse,
)
from .ollama import OllamaClient
from .openai import OpenAIClient
from .anthropic import AnthropicClient
from .doubao import DoubaoClient
from .qwen import QwenClient
from .glm import GLMClient
from .wenxin import WenxinClient
from .kimi import KimiClient
from .deepseek import DeepSeekClient
from .minimax import MiniMaxClient
from .cohere import CohereClient
from .hunyuan import HunyuanClient
from .pangu import PanguClient
from .mistral import MistralClient
from .together import TogetherClient
from .milm import MiLMClient
from .xai import XAIClient
from .google import GoogleClient
from .meta import MetaClient
from .shangtang import ShangtangClient
from .stepfun import StepfunClient
from .tiangong import TiangongClient
from .spark import SparkClient
from .baichuan import BaichuanClient
from .yi import YiClient

__all__ = [
    # 基础类
    "BaseLLMClient",
    "LLMResponse",
    # 厂商客户端
    "OllamaClient",
    "OpenAIClient",
    "AnthropicClient",
    "DoubaoClient",
    "QwenClient",
    "GLMClient",
    "WenxinClient",
    "KimiClient",
    "DeepSeekClient",
    "MiniMaxClient",
    "CohereClient",
    "HunyuanClient",
    "PanguClient",
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
]


def create_client(
    provider: str,
    **kwargs,
) -> BaseLLMClient:
    """
    创建 LLM 客户端工厂函数

    Args:
        provider: 提供商名称
            - "ollama": Ollama 本地模型
            - "openai": OpenAI / Azure OpenAI
            - "anthropic": Anthropic Claude
            - "doubao": 字节跳动豆包
            - "qwen": 阿里云通义千问
            - "glm": 智谱AI
            - "wenxin": 百度文心一言
            - "kimi": 月之暗面Kimi
            - "deepseek": 深度求索
            - "minimax": MiniMax
            - "cohere": Cohere
            - "hunyuan": 腾讯混元
            - "pangu": 华为盘古
            - "mistral": Mistral AI
            - "together": Together AI
            - "milm": 小米
            - "xai": X AI
            - "google": Google
            - "meta": Meta
            - "shangtang": 商汤科技
            - "stepfun": 阶跃星辰
            - "tiangong": 昆仑万维天工
            - "spark": 科大讯飞星火
            - "baichuan": 百川智能
            - "yi": 零一万物
        **kwargs: 传递给客户端的其他参数

    Returns:
        对应的 LLM 客户端实例

    Raises:
        ValueError: 不支持的 provider
    """
    clients = {
        "ollama": OllamaClient,
        "openai": OpenAIClient,
        "anthropic": AnthropicClient,
        "doubao": DoubaoClient,
        "qwen": QwenClient,
        "glm": GLMClient,
        "wenxin": WenxinClient,
        "kimi": KimiClient,
        "deepseek": DeepSeekClient,
        "minimax": MiniMaxClient,
        "cohere": CohereClient,
        "hunyuan": HunyuanClient,
        "pangu": PanguClient,
        "mistral": MistralClient,
        "together": TogetherClient,
        "milm": MiLMClient,
        "xai": XAIClient,
        "google": GoogleClient,
        "meta": MetaClient,
        "shangtang": ShangtangClient,
        "stepfun": StepfunClient,
        "tiangong": TiangongClient,
        "spark": SparkClient,
        "baichuan": BaichuanClient,
        "yi": YiClient,
    }

    provider_lower = provider.lower()
    if provider_lower not in clients:
        raise ValueError(
            f"不支持的 provider: {provider}，支持的选项: {list(clients.keys())}"
        )

    return clients[provider_lower](**kwargs)
