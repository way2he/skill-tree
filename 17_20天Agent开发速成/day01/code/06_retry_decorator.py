#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import random
from functools import wraps
from typing import Callable, Any


def retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    backoff_factor: float = 2.0,
    jitter_range: tuple = (0.5, 1.5),
    retry_on_exceptions: tuple = (Exception,)
):
    """
    指数退避重试装饰器（带 jitter 随机抖动）
    
    Args:
        max_retries: 最大重试次数
        base_delay: 初始延迟（秒）
        backoff_factor: 退避因子，默认 2.0（指数退避）
        jitter_range: jitter 随机范围，默认 (0.5, 1.5)
        retry_on_exceptions: 需要重试的异常类型元组
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except retry_on_exceptions as e:
                    if attempt == max_retries - 1:
                        raise  # 最后一次重试失败，抛出异常
                    # 指数退避计算
                    delay = base_delay * (backoff_factor ** attempt)
                    # 添加 jitter 随机抖动，避免惊群效应
                    delay *= random.uniform(*jitter_range)
                    print(f"第 {attempt + 1} 次失败，{delay:.1f} 秒后重试: {e}")
                    await asyncio.sleep(delay)
                except Exception as e:
                    # 非预期异常，直接抛出
                    raise
        return wrapper
    return decorator


# 使用示例
@retry(max_retries=3, base_delay=1.0)
async def fetch_data(session, url):
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.json()


# ==================== 简单测试 ====================
async def test_retry():
    """简单测试：模拟失败后重试成功"""
    attempt = 0
    
    @retry(max_retries=3, base_delay=0.1)
    async def mock_api():
        nonlocal attempt
        attempt += 1
        if attempt < 3:
            raise Exception(f"第 {attempt} 次调用失败")
        return {"success": True, "attempts": attempt}
    
    result = await mock_api()
    print(f"测试结果: {result}")
    print(f"Jitter 效果: 重试延迟被随机化，避免惊群效应")


if __name__ == "__main__":
    import sys
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(test_retry())