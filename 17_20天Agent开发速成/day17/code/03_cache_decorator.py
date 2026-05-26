
"""
缓存装饰器示例
"""

import functools
import time
from collections import OrderedDict


def simple_cache(func):
    """简单缓存装饰器"""
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(sorted(kwargs.items()))
        
        if key in cache:
            print(f"缓存命中：{key}")
            return cache[key]
        
        result = func(*args, **kwargs)
        cache[key] = result
        print(f"缓存写入：{key}")
        return result
        
    return wrapper


class TTLCache:
    """带TTL的缓存"""
    
    def __init__(self, maxsize=128, ttl=300):
        self.cache = OrderedDict()
        self.maxsize = maxsize
        self.ttl = ttl
        
    def get(self, key):
        """获取缓存"""
        if key not in self.cache:
            return None
            
        value, expire_time = self.cache[key]
        
        if time.time() &gt; expire_time:
            del self.cache[key]
            return None
            
        self.cache.move_to_end(key)
        return value
        
    def set(self, key, value):
        """设置缓存"""
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) &gt;= self.maxsize:
                self.cache.popitem(last=False)
                
        expire_time = time.time() + self.ttl
        self.cache[key] = (value, expire_time)


def ttl_cache(ttl=300):
    """TTL缓存装饰器"""
    def decorator(func):
        cache = TTLCache(ttl=ttl)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(sorted(kwargs.items()))
            
            cached_value = cache.get(key)
            if cached_value is not None:
                print(f"缓存命中：{key}")
                return cached_value
                
            result = func(*args, **kwargs)
            cache.set(key, result)
            print(f"缓存写入：{key}")
            return result
            
        return wrapper
    return decorator


# 示例1：简单缓存
print("示例1：简单缓存")
@simple_cache
def expensive_calculation(x, y):
    print("执行昂贵的计算...")
    time.sleep(1)
    return x + y

print(expensive_calculation(1, 2))  # 第一次，慢
print(expensive_calculation(1, 2))  # 第二次，快
print(expensive_calculation(3, 4))  # 新参数，慢
print(expensive_calculation(1, 2))  # 缓存命中
print()


# 示例2：TTL缓存
print("示例2：TTL缓存（5秒过期）")
@ttl_cache(ttl=5)
def fetch_data(id):
    print(f"从数据库获取数据：{id}")
    time.sleep(1)
    return {"id": id, "data": "示例数据"}

print(fetch_data(1))  # 从数据库获取
print(fetch_data(1))  # 缓存命中
print("等待 6 秒...")
time.sleep(6)
print(fetch_data(1))  # 已过期，从数据库获取
