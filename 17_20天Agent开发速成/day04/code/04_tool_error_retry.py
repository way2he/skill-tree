# -*- coding: utf-8 -*-
"""
Day04 - 04: 工具调用错误处理与幂等设计
功能：演示 4 类工具错误的处理 + request_id 幂等
"""
import json
import time
import hashlib
from functools import wraps


# ============ 1. 工具错误类型 ============
class ToolError(Exception):
    """工具调用业务错误"""
    def __init__(self, code: str, message: str, hint: str = ""):
        self.code = code
        self.message = message
        self.hint = hint  # 给模型的修复建议


# ============ 2. 安全执行装饰器：统一错误格式返回给模型 ============
def safe_tool(func):
    """工具安全执行：把异常转成结构化 JSON 返回，模型可以理解并自纠正"""
    @wraps(func)
    def wrapper(**kwargs):
        try:
            result = func(**kwargs)
            return json.dumps({"ok": True, "data": result}, ensure_ascii=False)
        except ToolError as e:
            return json.dumps({
                "ok": False, "code": e.code,
                "message": e.message, "hint": e.hint
            }, ensure_ascii=False)
        except Exception as e:
            return json.dumps({
                "ok": False, "code": "UNKNOWN",
                "message": str(e), "hint": "请稍后重试或换个参数"
            }, ensure_ascii=False)
    return wrapper


# ============ 3. 幂等装饰器：request_id 去重 ============
_idempotency_cache = {}  # 生产环境用 Redis

def idempotent(ttl_seconds: int = 86400):
    """幂等装饰器：相同 request_id 直接返回上次结果"""
    def decorator(func):
        @wraps(func)
        def wrapper(request_id: str, **kwargs):
            now = time.time()
            # 清理过期
            for k in list(_idempotency_cache.keys()):
                if _idempotency_cache[k]["expires"] < now:
                    del _idempotency_cache[k]
            # 命中缓存
            if request_id in _idempotency_cache:
                cached = _idempotency_cache[request_id]
                print(f"  ⚡ 幂等命中：request_id={request_id}, 直接返回缓存")
                return cached["result"]
            # 执行
            result = func(**kwargs)
            _idempotency_cache[request_id] = {
                "result": result,
                "expires": now + ttl_seconds
            }
            return result
        return wrapper
    return decorator


# ============ 4. 业务函数示例 ============
@safe_tool
def get_weather(city: str) -> dict:
    """有参数校验的工具：错了会回灌 hint 让模型自纠正"""
    valid_cities = {"上海", "北京", "广州", "深圳", "成都"}
    if city not in valid_cities:
        raise ToolError(
            code="CITY_NOT_FOUND",
            message=f"城市 {city} 不在支持列表",
            hint=f"请改用以下城市之一：{', '.join(valid_cities)}"
        )
    return {"city": city, "temp": 22, "weather": "多云"}


@safe_tool
@idempotent(ttl_seconds=3600)
def create_order(product_id: str, quantity: int) -> dict:
    """幂等的下单接口：相同 request_id 不会重复扣款"""
    if quantity <= 0:
        raise ToolError(
            code="INVALID_QUANTITY",
            message="数量必须大于 0",
            hint="请传入 1 或更大的整数"
        )
    order_id = f"ORD-{hashlib.md5(f'{product_id}{quantity}{time.time()}'.encode()).hexdigest()[:8]}"
    return {"order_id": order_id, "product_id": product_id, "quantity": quantity, "status": "已创建"}


# ============ 5. 死循环防护示例 ============
class ToolLoopGuard:
    """死循环防护：MAX_ITERATIONS + 重复参数检测"""

    def __init__(self, max_iterations: int = 5):
        self.max_iterations = max_iterations
        self.iteration = 0
        self.seen = set()

    def check_and_run(self, name: str, args: dict, func):
        self.iteration += 1
        if self.iteration > self.max_iterations:
            return {"ok": False, "code": "MAX_ITER",
                    "hint": "达到最大调用次数，请基于已有信息回答用户"}

        args_key = json.dumps(args, sort_keys=True, ensure_ascii=False)
        key = (name, args_key)
        if key in self.seen:
            return {"ok": False, "code": "DUPLICATE",
                    "hint": "你已经用相同参数调过这个工具，请换思路或换参数"}
        self.seen.add(key)
        return json.loads(func(**args))


if __name__ == "__main__":
    print("=" * 60)
    print("场景 1：参数错误自动回灌 hint")
    print("=" * 60)
    print(get_weather(city="火星"))
    print(get_weather(city="上海"))

    print("\n" + "=" * 60)
    print("场景 2：幂等性 —— 相同 request_id 不会重复创建订单")
    print("=" * 60)
    r1 = create_order(request_id="req-001", product_id="P001", quantity=2)
    print(f"第 1 次：{r1}")
    r2 = create_order(request_id="req-001", product_id="P001", quantity=2)
    print(f"第 2 次：{r2}")
    print(f"是否相同：{r1 == r2}")

    print("\n" + "=" * 60)
    print("场景 3：死循环防护")
    print("=" * 60)
    guard = ToolLoopGuard(max_iterations=3)
    for i in range(5):
        result = guard.check_and_run("get_weather", {"city": "上海"}, get_weather)
        print(f"第 {i+1} 次：{result}")
