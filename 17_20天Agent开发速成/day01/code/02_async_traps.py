#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day01 必写代码 2：async/await 常见坑
功能：演示 6 个最常踩的异步编程坑及正确写法

面试考点：
- await 到底在等什么？不 await 会怎么样？
- 为什么用了 async 反而变慢了？
- 协程函数和协程对象的区别？
"""

import asyncio
import time


# ============================================================
# 坑 1：忘记 await（最常见！）
# ============================================================
async def task_demo():
    await asyncio.sleep(1)
    return "done"


async def trap_1_forget_await():
    """坑 1：调用 async 函数但忘了 await"""
    print("\n--- 坑 1：忘记 await ---")
    
    # ❌ 错误：没有 await，返回的是协程对象，不是结果
    result = task_demo()
    print(f"结果类型：{type(result)}")  # <class 'coroutine'>
    print(f"结果值：{result}")  # <coroutine object ...>
    # 还会有警告：RuntimeWarning: coroutine 'task_demo' was never awaited
    
    # ✅ 正确：必须 await
    result = await task_demo()
    print(f"正确结果：{result}")


# ============================================================
# 坑 2：在异步函数里用 time.sleep
# ============================================================
async def slow_task(name: str):
    print(f"[{time.strftime('%X')}] {name} 开始")
    # ❌ 错误：time.sleep 会阻塞整个事件循环！
    # time.sleep(2)  # 所有协程都会卡住
    
    # ✅ 正确：用 asyncio.sleep
    await asyncio.sleep(2)
    print(f"[{time.strftime('%X')}] {name} 结束")


async def trap_2_sync_sleep():
    """坑 2：用了同步阻塞调用，并发失效"""
    print("\n--- 坑 2：time.sleep vs asyncio.sleep ---")
    
    start = time.time()
    await asyncio.gather(slow_task("A"), slow_task("B"), slow_task("C"))
    elapsed = time.time() - start
    print(f"⏱️ 耗时：{elapsed:.2f} 秒（应该约 2 秒，不是 6 秒）")


# ============================================================
# 坑 3：串行 await（异步当同步用）
# ============================================================
async def fetch_data(item_id: int) -> int:
    await asyncio.sleep(1)
    return item_id * 2


async def trap_3_serial_await():
    """坑 3：在循环里 await，变成串行了"""
    print("\n--- 坑 3：循环里 await（串行）vs gather（并发）---")
    
    # ❌ 错误：串行 await
    start = time.time()
    results = []
    for i in range(5):
        result = await fetch_data(i)  # 一个一个等
        results.append(result)
    print(f"❌ 串行：{time.time() - start:.2f} 秒，结果={results}")  # 约 5 秒
    
    # ✅ 正确：先创建所有协程，gather 并发
    start = time.time()
    tasks = [fetch_data(i) for i in range(5)]
    results = await asyncio.gather(*tasks)
    print(f"✅ 并发：{time.time() - start:.2f} 秒，结果={results}")  # 约 1 秒


# ============================================================
# 坑 4：异常处理不当，一个任务挂全部挂
# ============================================================
async def risky_task(idx: int) -> int:
    await asyncio.sleep(0.5)
    if idx == 2:
        raise ValueError(f"任务 {idx} 出错了！")
    return idx * 10


async def trap_4_exception_handling():
    """坑 4：异常处理 - return_exceptions 的妙用"""
    print("\n--- 坑 4：异常处理 ---")
    
    # ❌ 默认行为：一个异常导致 gather 整体失败
    try:
        results = await asyncio.gather(*[risky_task(i) for i in range(5)])
    except ValueError as e:
        print(f"❌ 没有 return_exceptions：整批挂了，错误：{e}")
    
    # ✅ 正确：用 return_exceptions=True，异常也作为结果返回
    results = await asyncio.gather(
        *[risky_task(i) for i in range(5)],
        return_exceptions=True
    )
    print(f"✅ 有 return_exceptions：")
    for i, r in enumerate(results):
        if isinstance(r, Exception):
            print(f"  任务 {i}：❌ {r}")
        else:
            print(f"  任务 {i}：✅ 结果={r}")


# ============================================================
# 坑 5：把 await 当线程用，过度异步化
# ============================================================
async def cpu_heavy_task(n: int) -> int:
    """CPU 密集任务用 async 没用！"""
    # ❌ 错误认知：以为 async 能加速 CPU 计算
    total = sum(i * i for i in range(n))
    return total


async def trap_5_cpu_bound():
    """坑 5：CPU 密集任务用 async 没意义"""
    print("\n--- 坑 5：CPU 密集任务不要用 async ---")
    
    start = time.time()
    results = await asyncio.gather(*[cpu_heavy_task(10_000_000) for _ in range(3)])
    elapsed = time.time() - start
    print(f"⚠️ CPU 任务并发：{elapsed:.2f} 秒（async 帮不上忙，应用多进程）")


# ============================================================
# 坑 6：协程函数 vs 协程对象傻傻分不清
# ============================================================
async def my_coro():
    return 42


async def trap_6_coro_object():
    """坑 6：协程函数和协程对象的区别"""
    print("\n--- 坑 6：协程函数 vs 协程对象 ---")
    
    # my_coro 是「协程函数」
    print(f"my_coro 是：{type(my_coro)}")  # <class 'function'>
    
    # my_coro() 是「协程对象」（一次性的！）
    coro1 = my_coro()
    print(f"my_coro() 是：{type(coro1)}")  # <class 'coroutine'>
    
    result = await coro1
    print(f"第一次 await 结果：{result}")
    
    # ❌ 错误：协程对象不能 await 两次！
    try:
        result = await coro1  # RuntimeError
    except RuntimeError as e:
        print(f"❌ 不能重复 await：{e}")
    
    # ✅ 正确：每次都重新调用协程函数
    result = await my_coro()
    print(f"✅ 重新创建协程对象后：{result}")


async def main():
    await trap_1_forget_await()
    await trap_2_sync_sleep()
    await trap_3_serial_await()
    await trap_4_exception_handling()
    # await trap_5_cpu_bound()  # 注释掉，太慢
    await trap_6_coro_object()


if __name__ == "__main__":
    import sys
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
