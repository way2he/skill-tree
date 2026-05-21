#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day01 必写代码 1：协程基础与事件循环
功能：理解 async/await、协程、事件循环的核心机制

面试考点：
- 协程和线程的区别？
- 什么是事件循环？
- 串行 vs 并发的本质区别？
- create_task 和 await 的区别？
"""

import asyncio
import time


async def hello(name: str, delay: int) -> str:
    """
    最简单的异步函数
    核心规则：遇到 await 就暂停，让出 CPU 给其他协程
    """
    print(f"[{time.strftime('%X')}] Hello {name}, 等待 {delay} 秒...")
    
    # ✅ 正确：异步 sleep，不阻塞事件循环
    await asyncio.sleep(delay)
    
    # ❌ 错误：千万不要写 time.sleep()！会阻塞整个线程！
    # time.sleep(delay)  # 这会让所有协程一起卡住
    
    print(f"[{time.strftime('%X')}] {name} 完成！")
    return f"Hello {name}!"


async def demo_serial_vs_concurrent():
    """演示：串行 vs 并发的本质区别"""
    
    # ---------- 错误示范：串行执行 ----------
    print("=" * 60)
    print("❌ 串行执行（一个接一个等）：")
    print("=" * 60)
    start = time.time()
    await hello("Alice", 2)  # 等 2 秒
    await hello("Bob", 1)    # 再等 1 秒
    print(f"⏱️ 总耗时：{time.time() - start:.2f} 秒\n")  # 约 3 秒
    
    # ---------- 正确示范：create_task 并发 ----------
    print("=" * 60)
    print("✅ 并发执行（一起开跑）：")
    print("=" * 60)
    start = time.time()
    task1 = asyncio.create_task(hello("Charlie", 2))  # 立即开始
    task2 = asyncio.create_task(hello("David", 1))    # 立即开始
    await task1  # 等结果
    await task2  # 等结果
    print(f"⏱️ 总耗时：{time.time() - start:.2f} 秒\n")  # 约 2 秒
    
    # ---------- 最佳实践：gather 批量并发 ----------
    print("=" * 60)
    print("🚀 gather 批量并发（最常用）：")
    print("=" * 60)
    start = time.time()
    tasks = [hello(f"Person-{i}", 1) for i in range(5)]
    results = await asyncio.gather(*tasks)
    print(f"⏱️ 5 个任务总耗时：{time.time() - start:.2f} 秒")  # 约 1 秒！
    print(f"📦 结果：{results}\n")


# ⭐ 面试官追问：协程和线程的区别？
"""
3 分钟回答模板：

协程是用户态的轻量级任务，由 Python 解释器调度；线程是操作系统调度的执行单元。
核心区别有三点：

1. 调度方式：
   - 协程：协作式调度，遇到 await 才让出 CPU
   - 线程：抢占式调度，操作系统随时可能切换

2. 切换开销：
   - 协程：纯函数调用切换，开销极小（纳秒级）
   - 线程：上下文切换涉及内核态，开销大（微秒级）

3. 并发数：
   - 协程：可以轻松开几万个
   - 线程：受 OS 限制，通常几百个就会卡

什么时候用协程？IO 密集型场景（网络请求、文件读写、数据库查询）
什么时候用线程？CPU 密集型 + 必须用阻塞 API 的场景
"""


if __name__ == "__main__":
    import sys
    # ================================================
    # ⚠️ Windows 平台兼容性处理（重要！）
    # ================================================
    # Python 3.8+ 在 Windows 上默认使用 ProactorEventLoop，
    # 但某些操作可能出现 "Event loop is closed" 错误。
    # 
    # 两种事件循环策略对比：
    # ┌──────────────────┬──────────────────────────┐
    # │ SelectorEventLoop│ ProactorEventLoop       │
    # ├──────────────────┼──────────────────────────┤
    # │ 基于 select/poll │ 基于 Windows IOCP      │
    # │ 兼容性好         │ 性能更高但不稳定       │
    # │ 推荐使用         │ 仅特殊场景使用         │
    # └──────────────────┴──────────────────────────┘
    # 
    # 为什么需要这行？
    # 1. ProactorEventLoop 在某些场景下不稳定
    # 2. 程序退出时资源清理顺序可能导致错误
    # 3. 避免 RuntimeError: Event loop is closed
    # ================================================
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # 🚀 启动异步程序主入口
    # asyncio.run() 会创建新的事件循环，运行完毕后自动关闭
    asyncio.run(demo_serial_vs_concurrent())
