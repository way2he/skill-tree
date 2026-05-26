# -*- coding: utf-8 -*-
"""
百度千帆官方 SDK 客户端基类

基于 qianfan SDK，提供百度文心大模型服务的统一封装。

依赖安装：
    pip install qianfan

文档参考：
    https://cloud.baidu.com/doc/WENXINWORKSHOP/s/clntwmv7t
"""

import os
from abc import ABC, abstractmethod
from typing import Any, Optional


class BaiduClient(ABC):
    """
    百度客户端抽象基类

    使用百度官方 SDK (qianfan) 进行调用。
    使用 AK/SK 鉴权方式。

    Args:
        ak: Access Key，可通过环境变量 QIANFAN_AK 设置
        sk: Secret Key，可通过环境变量 QIANFAN_SK 设置
        model: 模型名称，默认 "ERNIE-Bot-4"
        system_prompt: 系统提示词
        temperature: 温度参数 (0-1)
        max_tokens: 最大输出 token 数
    """

    def __init__(
        self,
        ak: Optional[str] = None,
        sk: Optional[str] = None,
        model: str = "ERNIE-Bot-4",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> None:
        """
        初始化百度客户端

        Args:
            ak: Access Key
            sk: Secret Key
            model: 模型名称
            system_prompt: 系统提示词
            temperature: 温度参数
            max_tokens: 最大输出 token 数
        """
        self.ak = ak or os.getenv("QIANFAN_AK")
        self.sk = sk or os.getenv("QIANFAN_SK")

        if not self.ak or not self.sk:
            raise ValueError(
                "AK 和 SK 未设置，请设置 QIANFAN_AK 和 QIANFAN_SK 环境变量"
            )

        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens

        # 初始化客户端
        self._init_client()

    @abstractmethod
    def _init_client(self) -> None:
        """
        初始化 qianfan 客户端（子类实现）
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
            符合百度千帆格式的消息列表
        """
        messages: list[dict[str, str]] = []

        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})

        messages.append({"role": "user", "content": prompt})

        return messages


# 别名，便于使用
QianfanClient = BaiduClient
