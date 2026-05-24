# -*- coding: utf-8 -*-
"""
llm.core.providers —— 厂商名枚举（动态生成，避免硬编码字符串）

调用方写法：
    from llm.core import get_llm, ProviderName

    llm = get_llm(ProviderName.DEEPSEEK)     # ✅ IDE 自动补全 / 拼写错误立即报错
    llm = get_llm("deepseek")                # ✅ 兼容字符串
    llm = get_llm()                          # ✅ 零参数

枚举成员从 factory 的注册表动态生成，新增厂商时自动出现，无需改这里。
"""

from __future__ import annotations

from enum import Enum
from typing import Union

from .factory import list_providers, list_async_providers


def _build_enum() -> type[Enum]:
    """从注册表动态构建 ProviderName 枚举"""
    members = {}
    seen: set[str] = set()
    for name in list_providers() + list_async_providers():
        name = name.lower()
        if name in seen:
            continue
        seen.add(name)
        # 枚举成员名：大写；成员值：小写字符串
        members[name.upper().replace("-", "_")] = name
    if not members:
        # 兜底，避免空枚举创建失败
        members["OLLAMA"] = "ollama"
    return Enum("ProviderName", members, type=str)


ProviderName = _build_enum()
"""动态生成的厂商名枚举，成员值即可直接传给 create_llm / get_llm"""


# 接受字符串或枚举，统一返回字符串
ProviderLike = Union[str, ProviderName]


def normalize(provider: "ProviderLike | None") -> str | None:
    """把 ProviderName 或 str 统一成小写字符串；None 透传"""
    if provider is None:
        return None
    if isinstance(provider, Enum):
        return str(provider.value).lower()
    return str(provider).strip().lower()


__all__ = ["ProviderName", "ProviderLike", "normalize"]
