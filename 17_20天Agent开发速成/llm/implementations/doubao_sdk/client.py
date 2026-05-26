# -*- coding: utf-8 -*-
"""
火山引擎官方 SDK 客户端基类

基于 volcengine-python-sdk 的 MaasService，提供火山引擎大模型服务的统一封装。

依赖安装：
    pip install volcengine-python-sdk

文档参考：
    https://www.volcengine.com/docs/82379/1263482
"""

import os
from abc import ABC, abstractmethod
from typing import Any, Optional


class VolcengineClient(ABC):
    """
    火山引擎客户端抽象基类

    使用火山引擎官方 SDK (volcengine-python-sdk) 进行调用。
    与 OpenAI 兼容方式的主要区别：
    - 使用 AK/SK 鉴权（非 API Key）
    - 使用火山引擎签名认证机制

    Args:
        ak: Access Key，可通过环境变量 VOLCENGINE_AK 设置
        sk: Secret Key，可通过环境变量 VOLCENGINE_SK 设置
        region: 区域，默认 "cn-beijing"
        model: 模型名称
        system_prompt: 系统提示词
        temperature: 温度参数 (0-1)
        max_tokens: 最大输出 token 数
    """

    def __init__(
        self,
        ak: Optional[str] = None,
        sk: Optional[str] = None,
        region: str = "cn-beijing",
        model: str = "doubao-pro-32k",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> None:
        """
        初始化火山引擎客户端

        Args:
            ak: Access Key
            sk: Secret Key
            region: 区域
            model: 模型名称
            system_prompt: 系统提示词
            temperature: 温度参数
            max_tokens: 最大输出 token 数
        """
        self.ak = ak or os.getenv("VOLCENGINE_AK")
        self.sk = sk or os.getenv("VOLCENGINE_SK")

        if not self.ak or not self.sk:
            raise ValueError(
                "AK 和 SK 未设置，请设置 VOLCENGINE_AK 和 VOLCENGINE_SK 环境变量"
            )

        self.region = region
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens

        # 初始化 MaasService
        self._init_maas_service()

    @abstractmethod
    def _init_maas_service(self) -> None:
        """
        初始化 MaasService（子类实现）

        使用 volcengine.maas.MaasService 初始化服务。
        """
        pass

    @abstractmethod
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        生成文本回复

        Args:
            prompt: 用户输入的提示词文本
            **kwargs: 可选参数

        Returns:
            模型生成的文本响应字符串
        """
        pass

    @abstractmethod
    def generate_json(
        self, prompt: str, schema: Optional[dict[str, Any]] = None, **kwargs: Any
    ) -> str:
        """
        生成 JSON 格式回复

        Args:
            prompt: 用户输入的提示词文本
            schema: 可选的 JSON Schema 字典
            **kwargs: 可选参数

        Returns:
            符合指定 Schema 的 JSON 字符串
        """
        pass

    def _build_messages(self, prompt: str) -> list[dict[str, str]]:
        """
        构建消息列表

        Args:
            prompt: 用户提示词

        Returns:
            符合火山引擎格式的消息列表
        """
        messages: list[dict[str, str]] = []

        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})

        messages.append({"role": "user", "content": prompt})

        return messages
