#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day01 必写代码 4：信号量并发控制 + 超时机制
功能：限制最大并发数 + 防止任务无限等待

面试考点：
- 为什么需要控制并发数？不控制会怎样？
- 信号量的工作原理？
- asyncio.wait_for 怎么工作？
- TimeoutError 怎么处理？
"""

import asyncio
import time

# ============================================================
# 场景 1：不控制并发的灾难
# ============================================================
async def fetch_no_limit(idx: int) -> str:
    """模拟一个慢请求"""
    print(f"[{time.strftime('%X')}] 任务 {idx} 开始")
    await asyncio.sleep(1)
    print(f"[{time.strftime('%X')}] 任务 {idx} 结束")
    return f"result-{idx}"


async def demo_no_limit():
    """❌ 不限并发：100 个请求一起发，可能被 API 限流/封 IP"""
    print("=" * 60)
    print("❌ 不限并发（100 个请求一起发）")
    print("=" * 60)
    
    start = time.time()
    tasks = [fetch_no_limit(i) for i in range(10)]  # 演示用 10 个
    await asyncio.gather(*tasks)
    print(f"⏱️ 耗时：{time.time() - start:.2f} 秒")
    print("⚠️ 真实场景下 100+ 并发会被 API 拒绝或封 IP\n")


# ============================================================
# 场景 2：用信号量控制并发数
# ============================================================
async def fetch_with_semaphore(
    semaphore: asyncio.Semaphore,
    idx: int
) -> str:
    """带信号量的请求：同时只能跑 N 个"""
    async with semaphore:  # 获取许可证（满了就排队等）
        print(f"[{time.strftime('%X')}] 任务 {idx} 获得许可，开始执行")
        await asyncio.sleep(1)
        print(f"[{time.strftime('%X')}] 任务 {idx} 完成，释放许可")
        return f"result-{idx}"


async def demo_with_semaphore():
    """✅ 用信号量控制并发，每次最多跑 3 个"""
    print("=" * 60)
    print("✅ 信号量控制并发（最多 3 个同时跑）")
    print("=" * 60)
    
    semaphore = asyncio.Semaphore(3)  # 最多 3 个并发
    
    start = time.time()
    tasks = [fetch_with_semaphore(semaphore, i) for i in range(10)]
    await asyncio.gather(*tasks)
    elapsed = time.time() - start
    print(f"⏱️ 耗时：{elapsed:.2f} 秒（约 4 秒 = 10 个任务 / 3 并发 × 1 秒/个）")


# ============================================================
# 场景 3：超时控制
# ============================================================
async def slow_api_call(name: str, delay: int) -> str:
    """模拟一个慢 API（用户希望最多等 3 秒）"""
    await asyncio.sleep(delay)
    return f"{name} 完成"


async def call_with_timeout(name: str, delay: int, timeout: int):
    """带超时的 API 调用"""
    try:
        result = await asyncio.wait_for(
            slow_api_call(name, delay),
            timeout=timeout
        )
        print(f"✅ {name}：成功，结果={result}")
        return result
    except asyncio.TimeoutError:
        print(f"⏰ {name}：超时（>{timeout} 秒），自动取消")
        return None


async def demo_timeout():
    """演示超时机制"""
    print("\n" + "=" * 60)
    print("⏰ 超时机制演示")
    print("=" * 60)
    
    # 并发调用，每个都有独立超时
    await asyncio.gather(
        call_with_timeout("快任务", delay=1, timeout=3),  # ✅ 1 < 3，成功
        call_with_timeout("慢任务", delay=5, timeout=3),  # ⏰ 5 > 3，超时
        call_with_timeout("中等任务", delay=2, timeout=3),  # ✅ 2 < 3，成功
    )


# ============================================================
# 综合演示：信号量 + 超时 一起用
# ============================================================
async def production_grade_fetch(
    semaphore: asyncio.Semaphore,
    idx: int,
    timeout: int = 3
) -> dict:
    """生产级请求函数：信号量 + 超时"""
    async with semaphore:
        try:
            # 模拟有时快有时慢
            delay = 1 if idx % 3 != 0 else 5  # 1/3 的请求会很慢
            await asyncio.wait_for(
                asyncio.sleep(delay),
                timeout=timeout
            )
            return {"idx": idx, "success": True}
        except asyncio.TimeoutError:
            return {"idx": idx, "success": False, "error": "timeout"}

async def demo_production():
    """生产级综合演示"""
    print("\n" + "=" * 60)
    print("🏭 生产级综合：信号量 + 超时")
    print("=" * 60)
    
    semaphore = asyncio.Semaphore(3)
    
    start = time.time()
    tasks = [production_grade_fetch(semaphore, i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start
    
    success = sum(1 for r in results if r["success"])
    failed = sum(1 for r in results if not r["success"])
    
    print(f"\n📊 统计：")
    print(f"  ✅ 成功：{success}")
    print(f"  ❌ 超时失败：{failed}")
    print(f"  ⏱️ 总耗时：{elapsed:.2f} 秒")


# ⭐ 面试官追问：信号量的工作原理？
"""
3 分钟回答模板：

信号量本质上是一个计数器，初始化时给它 N 个「许可证」。

工作流程：
1. 协程要进入临界区时，调用 acquire() 拿一个许可证
2. 如果计数器 > 0，立刻拿到，计数器减 1
3. 如果计数器 = 0，协程被挂起，加入等待队列
4. 退出临界区时调用 release()，计数器加 1，唤醒等待队列里的第一个协程

Python 的 async with semaphore 就是 acquire/release 的语法糖。

应用场景：
1. 限制 API 调用频率（如 OpenAI 限 100 QPS）
2. 限制数据库连接数（避免连接池耗尽）
3. 限制下载并发（避免被封 IP）

注意：信号量是协程级的，不是线程级的，跨线程要用 threading.Semaphore。
"""


async def main():
    # await demo_no_limit()
    # await demo_with_semaphore()
    # await demo_timeout()
    await demo_production()


if __name__ == "__main__":
    import sys
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
