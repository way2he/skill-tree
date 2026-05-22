# -*- coding: utf-8 -*-
"""
llm.openai.providers - OpenAI 兼容协议客户端集合

本模块导出所有兼容 OpenAI Chat Completions API 的客户端类，
以及 create_openai_client 工厂函数用于快速创建客户端实例。

支持的厂商（共18个）：
- openai: OpenAI 官方
- deepseek: DeepSeek 深度求索
- qwen: 通义千问
- doubao: 豆包（字节跳动）
- glm: 智谱 GLM
- kimi: Moonshot Kimi
- minimax: MiniMax
- milm: 小米大模型
- together: Together AI
- xai: xAI (Grok)
- mistral: Mistral AI
- shangtang: 商汤日日新
- stepfun: 阶跃星辰
- tiangong: 天工 AI
- baichuan: 百川智能
- yi: 零一万物
- spark: 讯飞星火
- meta: Meta Llama
"""

from .base import OpenAICompatibleClient
from .openai import OpenAIClient
from .deepseek import DeepSeekClient
from .qwen import QwenClient
from .doubao import DoubaoClient
from .glm import GLMClient
from .kimi import KimiClient
from .minimax import MiniMaxClient
from .milm import MiLMClient
from .together import TogetherClient
from .xai import XAIClient
from .mistral import MistralClient
from .shangtang import ShangtangClient
from .stepfun import StepfunClient
from .tiangong import TiangongClient
from .baichuan import BaichuanClient
from .yi import YiClient
from .spark import SparkClient
from .meta import MetaClient


# 厂商名（小写）到客户端类的映射表
_VENDOR_CLIENT_MAP: dict[str, type[OpenAICompatibleClient]] = {
    "openai": OpenAIClient,
    "deepseek": DeepSeekClient,
    "qwen": QwenClient,
    "doubao": DoubaoClient,
    "glm": GLMClient,
    "kimi": KimiClient,
    "minimax": MiniMaxClient,
    "milm": MiLMClient,
    "together": TogetherClient,
    "xai": XAIClient,
    "mistral": MistralClient,
    "shangtang": ShangtangClient,
    "stepfun": StepfunClient,
    "tiangong": TiangongClient,
    "baichuan": BaichuanClient,
    "yi": YiClient,
    "spark": SparkClient,
    "meta": MetaClient,
}


def create_openai_client(
    vendor: str,
    api_key: str | None = None,
    base_url: str | None = None,
    model: str | None = None,
    **kwargs,
) -> OpenAICompatibleClient:
    """
    工厂函数：根据厂商名创建对应的 OpenAI 兼容客户端实例。

    Args:
        vendor: 厂商名称（小写），如 "openai"、"deepseek"、"qwen" 等。
        api_key: API 密钥。若为 None，则尝试从对应环境变量读取。
        base_url: 自定义 API 基础 URL。若为 None，使用各厂商默认地址。
        model: 默认模型名称。若为 None，使用各厂商默认模型。
        **kwargs: 传递给客户端构造函数的额外参数。

    Returns:
        OpenAICompatibleClient: 对应厂商的客户端实例。

    Raises:
        ValueError: 当 vendor 不在支持的厂商列表中时抛出。
        TypeError: 当 vendor 参数类型不正确时抛出。
    """
    if not isinstance(vendor, str):
        raise TypeError(
            f"vendor 参数必须为字符串，实际传入类型为 {type(vendor).__name__}"
        )

    vendor_lower = vendor.strip().lower()

    client_cls = _VENDOR_CLIENT_MAP.get(vendor_lower)
    if client_cls is None:
        supported = ", ".join(sorted(_VENDOR_CLIENT_MAP.keys()))
        raise ValueError(
            f"不支持的厂商: '{vendor}'。"
            f"支持的厂商有: {supported}"
        )

    # 构造客户端初始化参数
    init_params: dict = {}
    if api_key is not None:
        init_params["api_key"] = api_key
    if base_url is not None:
        init_params["base_url"] = base_url
    if model is not None:
        init_params["model"] = model
    init_params.update(kwargs)

    return client_cls(**init_params)


__all__ = [
    # 基类
    "OpenAICompatibleClient",
    # 18个兼容客户端
    "OpenAIClient",
    "DeepSeekClient",
    "QwenClient",
    "DoubaoClient",
    "GLMClient",
    "KimiClient",
    "MiniMaxClient",
    "MiLMClient",
    "TogetherClient",
    "XAIClient",
    "MistralClient",
    "ShangtangClient",
    "StepfunClient",
    "TiangongClient",
    "BaichuanClient",
    "YiClient",
    "SparkClient",
    "MetaClient",
    # 工厂函数
    "create_openai_client",
    # 映射表
    "_VENDOR_CLIENT_MAP",
]
