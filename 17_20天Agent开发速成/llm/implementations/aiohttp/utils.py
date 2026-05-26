# -*- coding: utf-8 -*-
"""
异步 LLM 工具函数模块
提供 JSON 校验、异步重试机制等通用功能
"""

import asyncio
import json
import time
from typing import Any, Callable, Optional, Type

from pydantic import BaseModel


def validate_json_output(
    json_str: str, model_class: Optional[Type[BaseModel]] = None
) -> Any:
    """
    校验 JSON 输出是否符合格式

    Args:
        json_str: 模型输出的 JSON 字符串
        model_class: 可选的 Pydantic 模型类，用于校验和解析

    Returns:
        如果提供了 model_class，返回模型实例；否则返回 dict
        如果校验失败返回 None
    """
    try:
        json_str = json_str.strip()

        if json_str.startswith("```json"):
            json_str = json_str[7:]
        if json_str.startswith("```"):
            json_str = json_str[3:]
        if json_str.endswith("```"):
            json_str = json_str[:-3]
        json_str = json_str.strip()

        if model_class:
            return model_class.model_validate_json(json_str)
        else:
            return json.loads(json_str)
    except Exception as e:
        print(f"[ERROR] 校验失败: {e}")
        return None


async def async_generate_with_retry(
    generate_func: Callable[..., Any],
    model_class: Optional[Type[BaseModel]] = None,
    max_retries: int = 3,
    backoff: float = 1.0,
) -> Any:
    """
    带重试的异步生成函数

    Args:
        generate_func: 实际调用大模型的异步函数
        model_class: 可选的 Pydantic 模型类，用于校验输出
        max_retries: 最大重试次数
        backoff: 退避时间（秒）

    Returns:
        校验后的结果，如果全部重试失败返回 None
    """
    for attempt in range(max_retries):
        try:
            output = await generate_func()
            if model_class:
                result = validate_json_output(output, model_class)
            else:
                result = validate_json_output(output)
            if result:
                print(f"[SUCCESS] 第 {attempt + 1} 次尝试成功！")
                return result
        except Exception as e:
            print(f"[WARNING] 第 {attempt + 1} 次尝试失败: {e}")

        if attempt < max_retries - 1:
            sleep_time = backoff * (2**attempt)
            print(f"[INFO] {sleep_time} 秒后重试...")
            await asyncio.sleep(sleep_time)

    print(f"[ERROR] {max_retries} 次重试全部失败")
    return None


async def async_generate_from_pydantic(
    prompt: str,
    model_class: Type[BaseModel],
    provider: str = "ollama",
    max_retries: int = 3,
    **kwargs: Any,
) -> Any:
    """
    基于 Pydantic 模型的异步生成函数

    Args:
        prompt: 用户提示词
        model_class: Pydantic 模型类，用于定义输出格式
        provider: LLM 提供商类型
        max_retries: 最大重试次数
        **kwargs: 传递给 LLM 客户端的其他参数

    Returns:
        模型实例，如果失败返回 None
    """
    from .config import async_llm_generate_json

    json_schema = model_class.model_json_schema()

    async def generate_func() -> str:
        return await async_llm_generate_json(
            prompt, schema=json_schema, provider=provider, **kwargs
        )

    return await async_generate_with_retry(generate_func, model_class, max_retries)


class AsyncRateLimiter:
    """
    异步速率限制器
    用于控制 API 调用频率
    """

    def __init__(self, calls: int, period: float):
        """
        Args:
            calls: 在 period 秒内允许的调用次数
            period: 时间窗口（秒）
        """
        self.calls = calls
        self.period = period
        self.timestamps: list[float] = []
        self.lock = asyncio.Lock()

    async def acquire(self) -> None:
        """获取令牌，可能会阻塞直到可以调用"""
        async with self.lock:
            now = time.time()
            # 移除过期的时间戳
            self.timestamps = [t for t in self.timestamps if now - t < self.period]

            if len(self.timestamps) >= self.calls:
                # 需要等待
                wait_time = self.period - (now - self.timestamps[0])
                await asyncio.sleep(wait_time)
                # 再次清理
                now = time.time()
                self.timestamps = [t for t in self.timestamps if now - t < self.period]

            self.timestamps.append(time.time())
