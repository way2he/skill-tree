# -*- coding: utf-8 -*-
"""
Day01 - Python 异步编程完整示例
Python 3.12 兼容
包含三个层级：基础入门 → 进阶用法 → 工程化完整实现
"""
import asyncio
import aiohttp
from aiohttp import ClientTimeout
import time
# Python 3.9+ 直接使用内置类型，不需要从 typing 导入
# 参考：PEP 585


# ============================================================
# 🎯 第一层级：基础入门 - 理解 async/await 核心概念
# ============================================================

async def hello(name: str, delay: int) -> str:
    """
    最简单的异步函数
    核心：遇到 await 就暂停，让出 CPU 给其他协程
    """
    print(f"[{time.strftime('%X')}] Hello {name}, 等待 {delay} 秒...")
    await asyncio.sleep(delay)  # ❌ 绝对不能写 time.sleep()！会阻塞整个线程
    print(f"[{time.strftime('%X')}] {name} 完成！")
    return f"Hello {name}!"


async def demo1_basic_async():
    """Demo 1: 串行 vs 并发的本质区别"""
    print("=" * 60)
    print("🎯 Demo 1: 基础异步 - 串行 vs 并发")
    print("=" * 60)
    
    # ---------- 串行执行（错误示范）----------
    print("\n❌ 串行执行（很慢）:")
    start = time.time()
    await hello("Alice", 2)
    await hello("Bob", 1)
    print(f"总耗时: {time.time() - start:.2f} 秒")
    
    # ---------- 并发执行（正确示范）----------
    print("\n✅ 并发执行（很快）:")
    start = time.time()
    # create_task = 把任务交给事件循环调度
    task1 = asyncio.create_task(hello("Charlie", 2))
    task2 = asyncio.create_task(hello("David", 1))
    await task1
    await task2
    print(f"总耗时: {time.time() - start:.2f} 秒")
    
    # ---------- gather 批量并发 ----------
    print("\n🚀 批量并发执行:")
    start = time.time()
    tasks = [hello(f"Person {i}", 1) for i in range(5)]
    await asyncio.gather(*tasks)
    print(f"5个任务总耗时: {time.time() - start:.2f} 秒")


# ============================================================
# 🚀 第二层级：进阶用法 - 超时控制、信号量、错误处理
# ============================================================

async def with_timeout(name: str, delay: int, timeout: int):
    """带超时保护的异步函数 - 防止无限等待"""
    try:
        result = await asyncio.wait_for(hello(name, delay), timeout=timeout)
        print(f"✅ {name} 成功执行")
        return result
    except asyncio.TimeoutError:
        print(f"❌ {name} 执行超时！(超过 {timeout} 秒)")
        return None


async def demo2_advanced_features():
    """Demo 2: 进阶功能演示"""
    print("\n" + "=" * 60)
    print("🚀 Demo 2: 进阶功能 - 超时控制")
    print("=" * 60)
    
    await with_timeout("慢任务", delay=5, timeout=3)  # 会超时
    await with_timeout("快任务", delay=1, timeout=3)  # 不会超时


# ============================================================
# 🏭 第三层级：工程化完整实现 - aiohttp + 并发控制 + 重试
# ============================================================

# ---------------- 配置常量 ----------------
MAX_CONCURRENT = 3        # 最大并发数（信号量）
TIMEOUT_SECONDS = 10      # 单次请求超时
MAX_RETRIES = 3            # 最大重试次数

# 测试 URLs
TEST_URLS = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/0.5",
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/404",
    "https://httpbin.org/json",
    "https://httpbin.org/headers",
    "https://httpbin.org/user-agent",
    "https://httpbin.org/get?foo=bar",
    "https://httpbin.org/anything",
]


async def fetch_with_retry(
    session: aiohttp.ClientSession,
    url: str,
    semaphore: asyncio.Semaphore,
    retry_count: int = 0
) -> dict[str, any]:
    """
    ✨ 工程级异步请求函数
    包含：信号量并发控制 + 超时 + 指数退避重试 + 错误分类处理
    
    Agent 开发中 90% 的 API 调用都长这样！
    """
    try:
        # 1. 获取并发许可证（信号量控制同时跑的数量）
        async with semaphore:
            print(f"🔍 请求: {url} (第 {retry_count + 1} 次尝试)")
            
            # 2. 发送 HTTP 请求
            async with session.get(url) as response:
                # 3. 状态码检查
                response.raise_for_status()  # 非 2xx 抛异常
                
                # 4. 解析响应
                data = await response.json()
                print(f"✅ 成功: {url}")
                return {
                    "url": url,
                    "success": True,
                    "status": response.status,
                    "data": data
                }
                
    except asyncio.TimeoutError:
        # 超时错误：指数退避重试
        if retry_count < MAX_RETRIES - 1:
            delay = 1 * (2 ** retry_count)  # 1s → 2s → 4s
            print(f"⏰ 超时: {url}, {delay} 秒后重试...")
            await asyncio.sleep(delay)
            return await fetch_with_retry(session, url, semaphore, retry_count + 1)
        else:
            print(f"❌ 超时失败: {url} (已重试 {MAX_RETRIES} 次)")
            return {"url": url, "success": False, "error": "timeout"}
            
    except aiohttp.ClientResponseError as e:
        # HTTP 错误：4xx 不重试（客户端问题），5xx 可以重试
        if e.status >= 500 and retry_count < MAX_RETRIES - 1:
            delay = 1 * (2 ** retry_count)
            print(f"⚠️ 服务器错误 {e.status}: {url}, {delay} 秒后重试...")
            await asyncio.sleep(delay)
            return await fetch_with_retry(session, url, semaphore, retry_count + 1)
        else:
            print(f"❌ HTTP 错误: {url}, 状态码 {e.status}")
            return {"url": url, "success": False, "error": f"HTTP {e.status}"}
            
    except Exception as e:
        # 其他错误：网络问题、连接问题
        print(f"❌ 错误: {url}, {str(e)}")
        return {"url": url, "success": False, "error": str(e)}


async def demo3_engineering():
    """Demo 3: 工程化完整实现"""
    print("\n" + "=" * 60)
    print("🏭 Demo 3: 工程化完整实现 - 并发控制 + 超时 + 重试")
    print("=" * 60)
    
    start_time = time.time()
    
    # 1. 创建信号量（并发控制器）
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    print(f"📊 最大并发数: {MAX_CONCURRENT}")
    
    # 2. 创建带超时配置的 ClientSession（整个应用共用一个！）
    timeout = ClientTimeout(total=TIMEOUT_SECONDS)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # 3. 创建所有任务
        tasks = [
            fetch_with_retry(session, url, semaphore)
            for url in TEST_URLS
        ]
        
        # 4. 并发执行所有任务
        results = await asyncio.gather(*tasks)
    
    # 5. 统计结果
    elapsed = time.time() - start_time
    success_count = sum(1 for r in results if r["success"])
    
    print("\n" + "=" * 60)
    print("📊 执行结果统计")
    print("=" * 60)
    print(f"   总请求: {len(TEST_URLS)}")
    print(f"   ✅ 成功: {success_count}")
    print(f"   ❌ 失败: {len(TEST_URLS) - success_count}")
    print(f"   ⏱️  总耗时: {elapsed:.2f} 秒")
    print(f"   ⚡ QPS: {len(TEST_URLS) / elapsed:.2f}")
    print(f"   🚀 并发加速比: 理论串行约 7 秒，实际 {elapsed:.2f} 秒")
    print("=" * 60)


# ============================================================
# 🎮 运行入口
# ============================================================

async def main():
    """主函数：按顺序运行所有 Demo"""
    
    print("\n" + "🎊" * 30)
    print("🎉 Day01 - Python 异步编程完整示例（Python 3.12 兼容）🎉")
    print("🎊" * 30 + "\n")
    
    # 依次运行三个层级的 Demo
    await demo1_basic_async()    # 基础入门
    await demo2_advanced_features()  # 进阶用法
    await demo3_engineering()    # 工程化完整实现
    
    print("\n" + "✅" * 30)
    print("💯 所有 Demo 运行完成！恭喜掌握 Day01 核心内容！")
    print("✅" * 30)


# ============================================================
# ❗ 启动入口 - Python 3.12 最佳实践
# ============================================================

if __name__ == "__main__":
    # Windows 平台特殊处理（Python 3.12 兼容）
    import sys
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # 启动事件循环
    asyncio.run(main())
