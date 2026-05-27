# -*- coding: utf-8 -*-
"""
LLM 统一接口层 - Logger 工厂

提供统一的 logger 获取函数，确保所有模块使用一致的命名规范。
命名规范: llm.{module}，例如 llm.retry、llm.circuit_breaker、llm.cache。
"""

import logging


def get_logger(name: str) -> logging.Logger:
    """
    获取 llm 包内的 logger

    自动添加 "llm." 前缀，确保命名规范统一。
    如果传入的 name 已经包含 "llm." 前缀，则不再重复添加。

    Args:
        name: 模块名称（如 "retry"、"circuit_breaker"、"cache"）

    Returns:
        命名为 "llm.{name}" 的 Logger 实例

    Example:
        >>> from llm.core.logging_utils import get_logger
        >>> logger = get_logger("retry")
        >>> logger.info("重试第 3 次")
    """
    if not isinstance(name, str):
        raise TypeError(f"name 必须是字符串，got {type(name).__name__}")

    name = name.strip()
    if not name:
        raise ValueError("name 不能为空字符串")

    # 避免重复前缀
    if name.startswith("llm."):
        full_name = name
    else:
        full_name = f"llm.{name}"

    return logging.getLogger(full_name)
