# -*- coding: utf-8 -*-
"""
通用 LLM 客户端模块
支持国内外25+大模型厂商

主要模块：
- requests/providers: 各厂商专用客户端
    - 国内大厂: 阿里云(通义千问), 百度(文心一言), 字节跳动(豆包), 腾讯(混元), 华为(盘古), 科大讯飞(星火), 小米
    - 国际厂商: OpenAI, Anthropic, Google, Meta, Cohere, Mistral, Together, XAI
    - 创业公司: DeepSeek, 智谱AI(GLM), 月之暗面(Kimi), MiniMax, 百川智能, 零一万物
    - 其他: 商汤科技, 阶跃星辰, 昆仑万维(天工)

使用示例:
    from llm.requests import create_llm_client, llm_generate

    # 方式1: 使用工厂函数
    client = create_llm_client("deepseek", api_key="sk-xxx")
    response = client.generate("你好")

    # 方式2: 直接导入
    from llm.requests.providers import DeepSeekClient
    client = DeepSeekClient(api_key="sk-xxx")
    response = client.generate("你好")
"""

import json
import os
from typing import Any, Literal

# 从 providers 模块导出所有客户端和工厂函数
from .providers import (
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
    create_client,
)

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
    "llm_generate",
    "llm_generate_json",
    "load_env_config",
]


# 向后兼容：保留旧的 create_llm_client 函数
def create_llm_client(
    provider: Literal[
        "ollama",
        "openai",
        "anthropic",
        "doubao",
        "qwen",
        "glm",
        "wenxin",
        "kimi",
        "deepseek",
        "minimax",
        "cohere",
        "hunyuan",
        "pangu",
        "mistral",
        "together",
        "milm",
        "xai",
        "google",
        "meta",
        "shangtang",
        "stepfun",
        "tiangong",
        "spark",
        "baichuan",
        "yi",
    ],
    **kwargs: Any,
) -> BaseLLMClient:
    """
    创建 LLM 客户端工厂函数

    Args:
        provider: 提供商类型
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
    """
    return create_client(provider, **kwargs)


def llm_generate(
    prompt: str,
    provider: Literal[
        "ollama",
        "openai",
        "anthropic",
        "doubao",
        "qwen",
        "glm",
        "wenxin",
        "kimi",
        "deepseek",
        "minimax",
        "cohere",
        "hunyuan",
        "pangu",
        "mistral",
        "together",
        "milm",
        "xai",
        "google",
        "meta",
        "shangtang",
        "stepfun",
        "tiangong",
        "spark",
        "baichuan",
        "yi",
    ] = "ollama",
    **kwargs: Any,
) -> str:
    """
    统一的 LLM 生成接口（便捷函数）

    Args:
        prompt: 用户提示词
        provider: 提供商类型
        **kwargs: 传递给客户端的其他参数

    Returns:
        模型生成的文本
    """
    client = create_llm_client(provider, **kwargs)
    return client.generate(prompt)


def llm_generate_json(
    prompt: str,
    schema: dict[str, Any] | None = None,
    provider: Literal[
        "ollama",
        "openai",
        "anthropic",
        "doubao",
        "qwen",
        "glm",
        "wenxin",
        "kimi",
        "deepseek",
        "minimax",
        "cohere",
        "hunyuan",
        "pangu",
        "mistral",
        "together",
        "milm",
        "xai",
        "google",
        "meta",
        "shangtang",
        "stepfun",
        "tiangong",
        "spark",
        "baichuan",
        "yi",
    ] = "ollama",
    **kwargs: Any,
) -> str:
    """
    统一的 JSON 生成接口

    Args:
        prompt: 用户提示词
        schema: JSON Schema
        provider: 提供商类型
        **kwargs: 传递给客户端的其他参数

    Returns:
        模型生成的 JSON 字符串
    """
    client = create_llm_client(provider, **kwargs)
    return client.generate_json(prompt, schema)


def load_env_config(prefix: str = "LLM_") -> dict[str, str | None]:
    """
    从环境变量加载 LLM 配置

    支持的环境变量:
        - LLM_PROVIDER: 提供商类型
        - LLM_MODEL: 模型名称
        - LLM_API_KEY: API 密钥
        - LLM_BASE_URL: API 端点
        - LLM_REGION: 区域
        - LLM_SYSTEM_PROMPT: 系统提示词
        - LLM_SECRET_ID: 腾讯云 SecretId（仅腾讯）
        - LLM_SECRET_KEY: 腾讯云 SecretKey（仅腾讯）

    Returns:
        配置字典
    """
    return {
        "provider": os.getenv(f"{prefix}PROVIDER", "ollama"),
        "model": os.getenv(f"{prefix}MODEL"),
        "api_key": os.getenv(f"{prefix}API_KEY"),
        "base_url": os.getenv(f"{prefix}BASE_URL"),
        "region": os.getenv(f"{prefix}REGION"),
        "system_prompt": os.getenv(f"{prefix}SYSTEM_PROMPT"),
        "secret_id": os.getenv(f"{prefix}SECRET_ID"),
        "secret_key": os.getenv(f"{prefix}SECRET_KEY"),
    }
