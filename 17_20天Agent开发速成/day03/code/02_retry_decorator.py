#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day03 必写代码 2：指数退避重试装饰器
功能：带 jitter（随机抖动）的指数退避重试机制
"""

import time
import random
from functools import wraps


def retry_with_exponential_backoff(
    max_retries=5,
    initial_delay=1,
    max_delay=30,
    backoff_factor=2,
    jitter=True
):
    """
    指数退避重试装饰器
    
    Args:
        max_retries: 最大重试次数
        initial_delay: 初始延迟（秒）
        max_delay: 最大延迟（秒）
        backoff_factor: 延迟增长因子
        jitter: 是否加随机抖动
    
    Returns:
        装饰器函数
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        # 最后一次重试失败，抛出异常
                        raise
                    
                    # 计算延迟时间
                    if jitter:
                        # 加随机抖动，避免惊群效应
                        delay = min(max_delay, delay * backoff_factor) * random.uniform(0.5, 1.5)
                    else:
                        delay = min(max_delay, delay * backoff_factor)
                    
                    print(f"第 {attempt + 1} 次尝试失败，{delay:.1f}秒后重试：{str(e)}")
                    time.sleep(delay)
            
            return None
        return wrapper
    return decorator


# 使用示例
if __name__ == "__main__":
    from openai import OpenAI
    
    client = OpenAI(api_key="your-api-key")
    
    @retry_with_exponential_backoff(max_retries=5)
    def chat_with_retry(messages):
        return client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
    
    # 测试
    messages = [{"role": "user", "content": "你好"}]
    try:
        response = chat_with_retry(messages)
        print("成功获取响应：", response.choices[0].message.content)
    except Exception as e:
        print(f"重试 {5} 次后仍然失败：{str(e)}")
