# -*- coding: utf-8 -*-
"""
LLM 公共模块
提供统一的大模型调用接口，支持国内外25+种提供商

支持的厂商:
- 国内大厂: 阿里云(通义千问), 百度(文心一言), 字节跳动(豆包), 腾讯(混元), 华为(盘古), 科大讯飞(星火), 小米
- 国际厂商: OpenAI, Anthropic, Google, Meta, Cohere, Mistral, Together, XAI
- 创业公司: DeepSeek, 智谱AI(GLM), 月之暗面(Kimi), MiniMax, 百川智能, 零一万物
- 其他: 商汤科技, 阶跃星辰, 昆仑万维(天工), Ollama本地模型
"""

from .clients import (
    # 基础类
    BaseLLMClient,
    LLMResponse,
    # 厂商客户端
    OllamaClient,
    OpenAIClient,
    AnthropicClient,
    DoubaoClient,
    QwenClient,
    GLMClient,
    WenxinClient,
    KimiClient,
    DeepSeekClient,
    MiniMaxClient,
    CohereClient,
    HunyuanClient,
    PanguClient,
    MistralClient,
    TogetherClient,
    MiLMClient,
    XAIClient,
    GoogleClient,
    MetaClient,
    ShangtangClient,
    StepfunClient,
    TiangongClient,
    SparkClient,
    BaichuanClient,
    YiClient,
    # 工厂函数
    create_llm_client,
    llm_generate,
    llm_generate_json,
    load_env_config,
)
from .config import LLMConfig, create_llm
from .utils import generate_from_pydantic, generate_with_retry, validate_json_output

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
    # 工厂函数
    "create_llm_client",
    # 便捷函数
    "llm_generate",
    "llm_generate_json",
    "load_env_config",
    # 工具函数
    "validate_json_output",
    "generate_with_retry",
    "generate_from_pydantic",
    # 配置模块
    "LLMConfig",
    "create_llm",
]
