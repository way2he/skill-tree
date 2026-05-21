#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day01 必写代码 5：生产级异步爬虫
功能：信号量 + 超时 + 指数退避重试 + 错误分类处理

面试考点：
- 手写一个带并发控制、超时、重试的异步请求函数
- 怎么区分可重试错误和不可重试错误？
- 指数退避为什么是 2 的幂次？

⭐ 这是 Day01 的「面试压轴代码」，必须能闭着眼写出来！
"""

import asyncio
import random
import time
import aiohttp
from aiohttp import ClientTimeout


# ============================================================
# 配置
# ============================================================
MAX_CONCURRENT = 5     # 最大并发数
TIMEOUT_SECONDS = 10   # 单次请求超时
MAX_RETRIES = 3        # 最大重试次数
INITIAL_DELAY = 1      # 初始重试延迟
BACKOFF_FACTOR = 2     # 退避因子


# ============================================================
# 核心：生产级 fetch 函数
# ============================================================
async def fetch_with_retry(
    session: aiohttp.ClientSession,
    url: str,
    semaphore: asyncio.Semaphore,
    retry_count: int = 0,
) -> dict:
    """
    🌟 生产级异步请求函数（面试必背）
    
    功能：
    - 信号量并发控制
    - 超时保护
    - 指数退避重试（带 jitter 抖动）
    - 错误分类处理（4xx 不重试，5xx 和超时重试）
    
    Agent 开发中 90% 的 API 调用都是这个模式！
    """
    try:
        # 1️⃣ 拿并发许可
        async with semaphore:
            print(f"🔍 [{retry_count + 1}/{MAX_RETRIES}] {url}")
            
            # 2️⃣ 发送请求
            async with session.get(url) as response:
                response.raise_for_status()  # 非 2xx 抛异常
                data = await response.json()
                
                print(f"✅ 成功：{url}")
                return {
                    "url": url,
                    "success": True,
                    "status": response.status,
                    "data": data,
                }
    
    except asyncio.TimeoutError:
        # ⏰ 超时：可重试
        if retry_count < MAX_RETRIES - 1:
            delay = INITIAL_DELAY * (BACKOFF_FACTOR ** retry_count)
            # Jitter 随机抖动：将 delay 乘以 0.5~1.5 之间的随机数
            # 作用：避免「惊群效应」(Thundering Herd)
            # 场景：100个请求同时失败，如果都按精确的 1s、2s、4s 重试，
            #       会同时打向服务器，导致服务永远无法恢复
            # 效果：每个请求的重试时间被分散开，服务可以平滑恢复
            delay *= random.uniform(0.5, 1.5)
            print(f"⏰ 超时：{url}，{delay:.1f}s 后重试")
            await asyncio.sleep(delay)
            return await fetch_with_retry(session, url, semaphore, retry_count + 1)
        return {"url": url, "success": False, "error": "timeout"}
    
    except aiohttp.ClientResponseError as e:
        # 🚫 4xx 客户端错误：不重试
        if 400 <= e.status < 500:
            print(f"❌ 客户端错误 {e.status}：{url}（不重试）")
            return {"url": url, "success": False, "error": f"HTTP {e.status}"}
        
        # ⚠️ 5xx 服务端错误：重试
        if e.status >= 500 and retry_count < MAX_RETRIES - 1:
            delay = INITIAL_DELAY * (BACKOFF_FACTOR ** retry_count)
            delay *= random.uniform(0.5, 1.5)
            print(f"⚠️ 服务端错误 {e.status}：{url}，{delay:.1f}s 后重试")
            await asyncio.sleep(delay)
            return await fetch_with_retry(session, url, semaphore, retry_count + 1)
        
        return {"url": url, "success": False, "error": f"HTTP {e.status}"}
    
    except aiohttp.ClientError as e:
        # 🌐 网络/连接错误：重试
        if retry_count < MAX_RETRIES - 1:
            delay = INITIAL_DELAY * (BACKOFF_FACTOR ** retry_count)
            delay *= random.uniform(0.5, 1.5)
            print(f"🌐 网络错误：{url}，{delay:.1f}s 后重试，原因={e}")
            await asyncio.sleep(delay)
            return await fetch_with_retry(session, url, semaphore, retry_count + 1)
        return {"url": url, "success": False, "error": str(e)}
    
    except Exception as e:
        # 🔥 其他未知错误：不重试，直接报告
        print(f"🔥 未知错误：{url}, {e}")
        return {"url": url, "success": False, "error": str(e)}


# ============================================================
# 批量爬取入口
# ============================================================
async def crawl_batch(urls: list[str]) -> list[dict]:
    """批量并发爬取（生产级）"""
    
    # 1️⃣ 创建信号量
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    
    # 2️⃣ 创建 Session（全局唯一）
    timeout = ClientTimeout(total=TIMEOUT_SECONDS)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # 3️⃣ 创建所有任务
        tasks = [
            fetch_with_retry(session, url, semaphore)
            for url in urls
        ]
        
        # 4️⃣ 并发执行
        results = await asyncio.gather(*tasks, return_exceptions=True)
    
    return results


# ============================================================
# 演示
# ============================================================
async def main():
    print("\n" + "=" * 60)
    print("🏭 Day01 压轴代码：生产级异步爬虫")
    print("=" * 60)
    
    # 测试 URLs（包含成功、失败、慢的情况）
    test_urls = [
        "https://httpbin.org/json",            # ✅ 成功
        "https://httpbin.org/delay/1",         # ✅ 慢但成功
        "https://httpbin.org/status/200",      # ✅ 成功
        "https://httpbin.org/status/404",      # ❌ 4xx 不重试
        "https://httpbin.org/status/500",      # ⚠️ 5xx 重试
        "https://httpbin.org/delay/3",         # ✅ 慢但成功
        "https://httpbin.org/headers",         # ✅ 成功
        "https://httpbin.org/user-agent",      # ✅ 成功
        "https://httpbin.org/get?foo=bar",     # ✅ 成功
        "https://httpbin.org/anything",        # ✅ 成功
    ]
    
    start = time.time()
    results = await crawl_batch(test_urls)
    elapsed = time.time() - start
    
    # 统计
    success = sum(1 for r in results if isinstance(r, dict) and r.get("success"))
    failed = len(results) - success
    
    print("\n" + "=" * 60)
    print("📊 爬取统计")
    print("=" * 60)
    print(f"  总请求：{len(test_urls)}")
    print(f"  ✅ 成功：{success}")
    print(f"  ❌ 失败：{failed}")
    print(f"  ⏱️ 总耗时：{elapsed:.2f} 秒")
    print(f"  ⚡ 平均：{elapsed / len(test_urls):.2f} 秒/请求")
    print("=" * 60)


# ⭐ 面试官追问：指数退避为什么是 2 的幂次？
"""
3 分钟回答模板：

指数退避是分布式系统的经典重试策略，公式：delay = initial_delay × base^retry_count

为什么用 2 的幂次（base=2）？
1. 数学上：2^n 增长速度合适——既不像线性增长（base=1）那么慢、对服务恢复友好；
   又不像 3^n、4^n 那样增长太快导致等待时间过长
2. 工程上：每次重试间隔翻倍，给服务足够的恢复时间
3. 实践上：Google、AWS、OpenAI 的官方 SDK 都用 base=2

为什么要加 jitter（随机抖动）？
避免「惊群效应」：100 个请求同时失败，如果都按精确的 1s、2s、4s 重试，
会同时打过去，服务永远恢复不了。
加 jitter 后，每个请求重试时间分散开，服务能平滑恢复。

为什么 4xx 不重试？
- 4xx 是客户端错误（参数错、认证失败、资源不存在），重试结果一样
- 重试只浪费资源，应该直接报错让上层处理
- 只有 5xx（服务端错误）和网络错误才值得重试
"""


if __name__ == "__main__":
    import sys
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
