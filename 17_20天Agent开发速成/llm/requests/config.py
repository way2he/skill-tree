# -*- coding: utf-8 -*-
"""
LLM 配置模块
提供默认配置和便捷的客户端创建功能
"""

from typing import Any, Dict, Literal, Optional

from .clients import BaseLLMClient, create_llm_client

DEFAULT_PROVIDERS: Dict[str, Dict[str, Any]] = {
    "ollama": {"model": "qwen3.5:9b", "base_url": "http://localhost:11434"},
    "openai": {"model": "gpt-4o-mini", "base_url": "https://api.openai.com/v1"},
    "doubao": {"model": "doubao-pro-32k", "region": "cn-beijing"},
    "anthropic": {"model": "claude-sonnet-4-20250514"},
}


class LLMConfig:
    """
    LLM 配置类
    提供默认配置和便捷的客户端创建功能

    使用示例:
        # 使用默认配置
        config = LLMConfig()
        client = config.create_client()

        # 切换提供商
        config.provider = "openai"
        client = config.create_client()

        # 自定义模型参数
        config.set_model("qwen3.5:9b")
        client = config.create_client()
    """

    def __init__(
        self,
        provider: Literal["ollama", "openai", "doubao", "anthropic"] = "ollama",
        model: Optional[str] = None,
        **kwargs: Any,
    ):
        self.provider: Literal["ollama", "openai", "doubao", "anthropic"] = provider
        self._model = model
        self._extra_params: dict[str, Any] = kwargs

    def set_model(self, model: str) -> "LLMConfig":
        """设置模型名称"""
        self._model = model
        return self

    def set_provider(
        self, provider: Literal["ollama", "openai", "doubao", "anthropic"]
    ) -> "LLMConfig":
        """设置提供商"""
        self.provider = provider
        return self

    def add_params(self, **kwargs: Any) -> "LLMConfig":
        """添加额外参数"""
        self._extra_params.update(kwargs)
        return self

    def create_client(self) -> BaseLLMClient:
        """
        根据配置创建 LLM 客户端

        Returns:
            BaseLLMClient: 对应的 LLM 客户端实例
        """
        params = DEFAULT_PROVIDERS.get(self.provider, {}).copy()

        if self._model:
            params["model"] = self._model

        params.update(self._extra_params)

        return create_llm_client(self.provider, **params)

    @classmethod
    def from_env(cls) -> "LLMConfig":
        """
        从环境变量加载配置

        支持的环境变量:
            - LLM_PROVIDER: 提供商类型
            - LLM_MODEL: 模型名称
            - LLM_BASE_URL: API 端点
            - LLM_REGION: 区域（火山引擎）
        """
        import os

        provider_env = os.getenv("LLM_PROVIDER", "ollama")
        model = os.getenv("LLM_MODEL")
        base_url = os.getenv("LLM_BASE_URL")
        region = os.getenv("LLM_REGION")

        if provider_env in ("ollama", "openai", "doubao", "anthropic"):
            config = cls(provider=provider_env  # type: ignore[arg-type]
                         )
        else:
            config = cls(provider="ollama")

        if model:
            config.set_model(model)

        if base_url:
            config.add_params(base_url=base_url)

        if region:
            config.add_params(region=region)

        return config


def create_llm(
    provider: Literal["ollama", "openai", "doubao", "anthropic"] = "ollama",
    model: Optional[str] = None,
    **kwargs: Any,
) -> BaseLLMClient:
    """
    便捷函数：根据提供商创建 LLM 客户端

    Args:
        provider: 提供商类型
        model: 模型名称（可选，覆盖默认值）
        **kwargs: 额外参数

    Returns:
        BaseLLMClient: 对应的 LLM 客户端实例

    Examples:
        # 使用默认配置
        client = create_llm()

        # 指定提供商
        client = create_llm("openai")

        # 指定模型
        client = create_llm("ollama", model="qwen3.5:9b")

        # 添加额外参数
        client = create_llm("openai", base_url="https://custom.api.com/v1")
    """
    return LLMConfig(provider=provider, model=model, **kwargs).create_client()
