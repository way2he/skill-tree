# -*- coding: utf-8 -*-
"""
火山引擎 (Volcengine) 官方 SDK 模块

基于 volcengine-python-sdk，提供火山引擎大模型服务（豆包等）的原生调用。

与 OpenAI 兼容方式的区别：
- 使用 AK/SK 鉴权（非 API Key）
- 使用火山引擎签名认证
- 支持更多火山引擎特有功能

安装依赖：
    pip install volcengine-python-sdk

使用示例：
    from llm.volcengine import DoubaoClient
    
    client = DoubaoClient(
        ak="your-access-key",
        sk="your-secret-key",
        region="cn-beijing"
    )
    response = client.generate("你好")
"""

from .client import VolcengineClient
from .providers import DoubaoClient, create_volcengine_client

__all__ = [
    "VolcengineClient",
    "DoubaoClient",
    "create_volcengine_client",
]
