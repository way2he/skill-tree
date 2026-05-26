# -*- coding: utf-8 -*-
"""
百度千帆大模型平台官方 SDK 模块

提供基于 qianfan SDK 的百度文心大模型调用封装。

依赖安装：
    pip install qianfan

文档参考：
    https://cloud.baidu.com/doc/WENXINWORKSHOP/s/clntwmv7t
"""

from .client import BaiduClient, QianfanClient
from .providers import WenxinClient, create_baidu_client

__all__ = [
    "BaiduClient",
    "QianfanClient",
    "WenxinClient",
    "create_baidu_client",
]
