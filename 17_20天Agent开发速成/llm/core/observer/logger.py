"""
LLM 统一接口层 - 日志便捷入口

提供一行代码开关 LLM 调用日志的能力：
    from llm.core import enable_logging
    enable_logging()                              # 控制台 INFO
    enable_logging(log_file="logs/llm.log")       # 同时写文件
    enable_logging(level="DEBUG", log_response=False)

日志内容包含：
- 调用方法（generate / generate_json / generate_stream）
- 渠道（provider，如 deepseek、openai、anthropic）
- 调用模型（model）
- 底层实现（backend，如 requests / aiohttp / openai_sdk）
- 入参（prompt + kwargs，敏感字段自动脱敏）
- 出参（response 内容，可截断）
- 耗时（latency_ms）、token 用量、错误信息
- 请求追踪 ID（request_id，串联同一次调用的 start/success/failure）

设计上完全基于已有的 EventBus / LoggingHandler / MetricsHandler，
不侵入任何 provider 客户端代码。
"""

from __future__ import annotations

import logging
import os
import threading
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Iterable, Optional, Union

from .event_bus import subscribe, unsubscribe
from .handlers import LoggingHandler, MetricsHandler, _DEFAULT_SENSITIVE_KEYS


__all__ = [
    "enable_logging",
    "disable_logging",
    "is_logging_enabled",
    "get_metrics_handler",
    "DEFAULT_LOG_FORMAT",
    "DEFAULT_DATE_FORMAT",
]


DEFAULT_LOG_FORMAT = "%(asctime)s [%(trace_id)s] %(levelname)s [%(name)s] %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ============================================================================= 
# 内部状态（线程安全）
# ============================================================================= 

_state_lock = threading.Lock()
_installed_handler: Optional[LoggingHandler] = None
_installed_metrics: Optional[MetricsHandler] = None
_logger_name = "llm"
_handlers_added: list[logging.Handler] = []


def _level_to_int(level: Union[int, str]) -> int:
    """把字符串/数字级别归一化为 logging 整数级别"""
    if isinstance(level, int):
        return level
    name = str(level).strip().upper()
    mapping = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "WARN": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }
    if name not in mapping:
        raise ValueError(f"不支持的日志级别: {level}")
    return mapping[name]


def _ensure_logger(
    level: int,
    log_file: Optional[Path],
    console: bool,
    file_max_bytes: int,
    file_backup_count: int,
    file_encoding: str,
) -> logging.Logger:
    """
    准备 `llm` logger 与 handler

    - 关闭 propagate，避免重复输出
    - 总是清理本模块之前安装的 handler（防止重复 enable_logging 累积）
    - 按需挂载 console / file handler
    """
    lg = logging.getLogger(_logger_name)
    lg.setLevel(level)
    lg.propagate = False

    # 移除本模块之前安装的 handler
    for h in list(_handlers_added):
        try:
            lg.removeHandler(h)
            h.close()
        except Exception:
            pass
    _handlers_added.clear()

    fmt = logging.Formatter(DEFAULT_LOG_FORMAT, datefmt=DEFAULT_DATE_FORMAT)
    from ..trace import TraceFilter
    trace_filter = TraceFilter()

    if console:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(fmt)
        ch.addFilter(trace_filter)
        lg.addHandler(ch)
        _handlers_added.append(ch)

    if log_file is not None:
        log_file = Path(log_file).expanduser().resolve()
        log_file.parent.mkdir(parents=True, exist_ok=True)
        fh = RotatingFileHandler(
            str(log_file),
            maxBytes=file_max_bytes,
            backupCount=file_backup_count,
            encoding=file_encoding,
        )
        fh.setLevel(level)
        fh.setFormatter(fmt)
        fh.addFilter(trace_filter)
        lg.addHandler(fh)
        _handlers_added.append(fh)

    return lg


# ============================================================================= 
# 公开 API
# ============================================================================= 

def enable_logging(
    level: Union[int, str] = "INFO",
    *,
    log_file: Optional[Union[str, os.PathLike]] = None,
    console: bool = True,
    log_prompt: bool = True,
    log_response: bool = True,
    log_params: bool = True,
    prompt_max_chars: int = 500,
    response_max_chars: int = 500,
    sensitive_keys: Iterable[str] = _DEFAULT_SENSITIVE_KEYS,
    enable_metrics: bool = True,
    file_max_bytes: int = 10 * 1024 * 1024,
    file_backup_count: int = 5,
    file_encoding: str = "utf-8",
) -> logging.Logger:
    """
    一键开启 LLM 调用日志

    会向全局 EventBus 注册一个 LoggingHandler（可选 MetricsHandler），
    所有适配器在执行 generate / generate_json / generate_stream 时
    会自动发布事件并被记录。

    Args:
        level: 日志级别（"INFO" / "DEBUG" / "ERROR" 等，或 logging 模块的常量）
        log_file: 日志文件路径（None 表示只输出到控制台）
        console: 是否输出到控制台
        log_prompt: 是否记录入参 prompt
        log_response: 是否记录出参 response
        log_params: 是否记录调用 kwargs（敏感字段自动脱敏）
        prompt_max_chars: prompt 截断长度（<=0 表示不截断）
        response_max_chars: response 截断长度（<=0 表示不截断）
        sensitive_keys: 需要脱敏的字段名集合
        enable_metrics: 是否同时安装 MetricsHandler（可通过 get_metrics_handler() 拿到）
        file_max_bytes: 日志文件单文件最大字节数（默认 10MB）
        file_backup_count: 滚动日志保留数量
        file_encoding: 日志文件编码（默认 utf-8）

    Returns:
        配置好的 `llm` logger 实例

    示例：
        >>> from llm.core import enable_logging, get_llm
        >>> enable_logging(log_file="logs/llm.log")
        >>> client = get_llm("deepseek")
        >>> client.generate("你好")
        # 控制台和文件会同时输出：
        # 2026-05-24 11:30:00 [INFO] llm | [request_start] rid=... provider=deepseek model=deepseek-chat backend=requests method=generate prompt='你好'
        # 2026-05-24 11:30:01 [INFO] llm | [request_success] rid=... provider=deepseek ... latency=850.12ms response='你好！...'
    """
    global _installed_handler, _installed_metrics

    int_level = _level_to_int(level)

    with _state_lock:
        # 先卸载旧的（如果有），避免重复
        _disable_locked()

        # 准备底层 logger
        target_logger = _ensure_logger(
            level=int_level,
            log_file=Path(log_file) if log_file is not None else None,
            console=console,
            file_max_bytes=file_max_bytes,
            file_backup_count=file_backup_count,
            file_encoding=file_encoding,
        )

        # 创建并订阅 LoggingHandler
        handler = LoggingHandler(
            log_level=int_level,
            log_prompt=log_prompt,
            log_response=log_response,
            log_params=log_params,
            prompt_max_chars=prompt_max_chars,
            response_max_chars=response_max_chars,
            sensitive_keys=sensitive_keys,
            target_logger=target_logger,
        )
        subscribe(None, handler)  # 订阅所有事件
        _installed_handler = handler

        # 可选 MetricsHandler
        if enable_metrics:
            metrics = MetricsHandler()
            subscribe(None, metrics)
            _installed_metrics = metrics

        target_logger.info("LLM logging system enabled: level=%s console=%s log_file=%s metrics=%s",
                          logging.getLevelName(int_level), console,
                          str(log_file) if log_file else "None",
                          enable_metrics)

        return target_logger


def _disable_locked() -> None:
    """关闭日志（假设调用者已持锁）"""
    global _installed_handler, _installed_metrics

    if _installed_handler is not None:
        unsubscribe(None, _installed_handler)
        _installed_handler = None
    if _installed_metrics is not None:
        unsubscribe(None, _installed_metrics)
        _installed_metrics = None

    lg = logging.getLogger(_logger_name)
    for h in list(_handlers_added):
        try:
            lg.removeHandler(h)
            h.close()
        except Exception:
            pass
    _handlers_added.clear()
    lg.info("LLM logging system disabled")


def disable_logging() -> None:
    """
    关闭 LLM 调用日志

    移除 EventBus 上的 LoggingHandler / MetricsHandler，
    并卸载本模块安装的控制台/文件 handler。
    """
    with _state_lock:
        _disable_locked()


def is_logging_enabled() -> bool:
    """当前是否已开启日志"""
    return _installed_handler is not None


def get_metrics_handler() -> Optional[MetricsHandler]:
    """
    获取当前安装的 MetricsHandler 实例

    Returns:
        若 enable_logging(enable_metrics=True) 已开启则返回实例，
        否则返回 None。可调用 .get_metrics() 获取累计指标。
    """
    return _installed_metrics
