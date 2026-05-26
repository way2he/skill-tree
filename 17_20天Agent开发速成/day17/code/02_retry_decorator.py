
"""
重试装饰器示例
"""

import time
import functools
import random


def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """重试装饰器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            last_exception = None
            
            while attempts &lt; max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    last_exception = e
                    print(f"尝试 {attempts}/{max_attempts} 失败：{e}")
                    
                    if attempts &lt; max_attempts:
                        time.sleep(delay)
                        
            raise last_exception
        return wrapper
    return decorator


def retry_exponential_backoff(max_attempts=5, base_delay=1, max_delay=60):
    """指数退避重试装饰器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            last_exception = None
            
            while attempts &lt; max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    last_exception = e
                    
                    if attempts &lt; max_attempts:
                        delay = min(base_delay * (2 ** (attempts - 1)), max_delay)
                        print(f"尝试 {attempts}/{max_attempts} 失败，等待 {delay} 秒...")
                        time.sleep(delay)
                        
            raise last_exception
        return wrapper
    return decorator


# 示例1：简单重试
print("示例1：简单重试")
@retry(max_attempts=3, delay=1)
def unstable_function():
    if random.random() &lt; 0.7:
        raise Exception("临时错误")
    return "成功！"

try:
    result = unstable_function()
    print(f"结果：{result}")
except Exception as e:
    print(f"最终失败：{e}")

print()


# 示例2：指数退避重试
print("示例2：指数退避重试")
@retry_exponential_backoff(max_attempts=4, base_delay=1, max_delay=10)
def another_unstable_function():
    if random.random() &lt; 0.6:
        raise Exception("临时错误")
    return "成功！"

try:
    result = another_unstable_function()
    print(f"结果：{result}")
except Exception as e:
    print(f"最终失败：{e}")
