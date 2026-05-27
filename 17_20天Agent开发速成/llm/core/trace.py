# -*- coding: utf-8 -*-
"""
LLM 统一接口层 - 轻量级 trace_id 管理

基于 contextvars 实现跨调用链的 trace_id 追踪。
零额外依赖，仅使用 Python 标准库。

使用示例:
    from llm.core.trace import trace_context, get_trace_id

    with trace_context():
        # 此上下文内所有日志自动携带同一个 trace_id
        client.generate("你好")
        print(get_trace_id())  # e.g. "a1b2c3d4e5f6"
"""

from __future__ import annotations

import logging
import uuid
from contextvars import ContextVar
from typing import Optional


# 当前上下文的 trace_id
_trace_id_var: ContextVar[str] = ContextVar("llm_trace_id", default="")


def new_trace_id() -> str:
    """
    生成新的 trace_id

    使用 uuid4 的 hex 表示（32 字符），确保全局唯一。

    Returns:
        32 字符的十六进制 trace_id 字符串
    """
    return uuid.uuid4().hex


def get_trace_id() -> str:
    """
    获取当前上下文的 trace_id

    Returns:
        当前 trace_id，未设置时返回空字符串
    """
    try:
        return _trace_id_var.get("")
    except LookupError:
        return ""


def set_trace_id(tid: Optional[str]) -> None:
    """
    设置当前上下文的 trace_id

    Args:
        tid: trace_id 字符串，传 None 则清除当前 trace_id
    """
    if tid is None:
        tid = ""
    if not isinstance(tid, str):
        raise TypeError(f"trace_id 必须是字符串或 None，got {type(tid).__name__}")
    _trace_id_var.set(tid)


class trace_context:
    """
    trace_id 上下文管理器

    进入时自动创建新的 trace_id（或使用指定的），退出时恢复之前的值。

    Args:
        tid: 可选的 trace_id，不传则自动生成新的

    Example:
        >>> with trace_context():
        ...     print(get_trace_id())  # 自动生成的 id
        >>> with trace_context("my-custom-id"):
        ...     print(get_trace_id())  # "my-custom-id"
    """

    def __init__(self, tid: Optional[str] = None) -> None:
        self._new_tid = tid if tid is not None else new_trace_id()
        self._old_tid: Optional[str] = None
        self._token = None

    def __enter__(self) -> str:
        """进入上下文，设置新的 trace_id"""
        self._old_tid = get_trace_id()
        self._token = _trace_id_var.set(self._new_tid)
        return self._new_tid

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """退出上下文，恢复之前的 trace_id"""
        if self._token is not None:
            _trace_id_var.reset(self._token)


class TraceFilter(logging.Filter):
    """
    logging.Filter 实现，将 trace_id 注入每条日志的 record

    使用方式:
        logger = logging.getLogger("llm")
        logger.addFilter(TraceFilter())
        # 之后每条日志的 record.trace_id 都会被自动设置
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """为日志记录注入 trace_id"""
        record.trace_id = get_trace_id() or "-"
        return True
