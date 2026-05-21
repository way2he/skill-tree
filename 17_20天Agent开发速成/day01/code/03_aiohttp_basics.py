#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day01 必写代码 3：aiohttp 异步 HTTP 请求
功能：演示 aiohttp 基础用法 + Session 复用最佳实践

面试考点：
- 为什么用 aiohttp 不用 requests？
- ClientSession 为什么要复用？
- 异步 HTTP 客户端的设计要点？
"""

import asyncio
import time
import aiohttp


# ============================================================
# 错误示范：每个请求新建 Session（开销大、内存泄漏）
# ============================================================
async def fetch_bad(url: str) -> dict:
    """❌ 错误：每次都新建 ClientSession"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


# ============================================================
# 正确示范：共享 Session（生产环境必备）
# ============================================================
async def fetch_good(session: aiohttp.ClientSession, url: str) -> dict:
    """✅ 正确：复用 Session，传入函数"""
    async with session.get(url) as response:
        # ================================================
        # 🚨 raise_for_status()：HTTP 状态码检查
        # ================================================
        # 作用：如果响应状态码 >= 400（客户端错误）或 >= 500（服务器错误），
        #       立即抛出 aiohttp.ClientResponseError 异常
        # 
        # 常见状态码：
        # ┌───────────────────────────────────────────────┐
        # │ 2xx 成功：不抛异常，正常继续执行              │
        # │ 4xx 客户端错误：如 400/401/403/404           │
        # │ 5xx 服务器错误：如 500/502/503/504           │
        # └───────────────────────────────────────────────┘
        # 
        # 为什么必须加？
        # 1. 避免静默失败：服务器返回错误但代码继续执行
        # 2. 统一错误处理：配合 try-except 捕获所有 HTTP 错误
        # 3. 快速失败：错误尽早暴露，便于调试
        # ================================================
        response.raise_for_status()
        return await response.json()


async def demo_session_reuse():
    """演示：Session 复用 vs 每次新建"""
    urls = ["https://httpbin.org/get"] * 20
    
    # ---------- 错误方式：每次新建 ----------
    print("=" * 60)
    print("[ERROR] 每次新建 Session（慢、浪费资源）")
    print("=" * 60)
    start = time.time()
    results = await asyncio.gather(*[fetch_bad(url) for url in urls])
    print(f"[TIME] 耗时：{time.time() - start:.2f} 秒, 成功: {len(results)}\n")
    
    # ---------- 正确方式：复用 Session ----------
    print("=" * 60)
    print("[OK] 复用 Session（快、节省资源）")
    print("=" * 60)
    start = time.time()
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*[fetch_good(session, url) for url in urls])
    print(f"[TIME] 耗时：{time.time() - start:.2f} 秒, 成功: {len(results)}")


# ============================================================
# 完整的 HTTP 客户端：POST、Header、JSON、超时
# ============================================================
async def http_client_demo():
    """演示 aiohttp 的常用功能"""
    print("\n" + "=" * 60)
    print("🚀 aiohttp 常用功能演示")
    print("=" * 60)
    
    # 全局超时配置
    timeout = aiohttp.ClientTimeout(total=10, connect=3)
    
    # 自定义请求头
    headers = {
        "User-Agent": "MyAgent/1.0",
        "Accept": "application/json",
    }
    
    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        
        # 1. GET 请求
        print("\n📥 GET 请求：")
        async with session.get("https://httpbin.org/get?key=value") as r:
            data = await r.json()
            print(f"  状态码：{r.status}")
            print(f"  args: {data.get('args')}")
        
        # 2. POST JSON
        print("\n📤 POST JSON 请求：")
        payload = {"name": "Agent", "version": "1.0"}
        async with session.post("https://httpbin.org/post", json=payload) as r:
            data = await r.json()
            print(f"  状态码：{r.status}")
            print(f"  收到的 json：{data.get('json')}")
        
        # 3. 带 Query 参数
        print("\n🔍 带 Query 参数：")
        params = {"q": "python", "page": 1}
        async with session.get("https://httpbin.org/get", params=params) as r:
            data = await r.json()
            print(f"  URL：{data.get('url')}")


# ⭐ 面试官追问：为什么用 aiohttp 不用 requests？
"""
3 分钟回答模板：

requests 是同步阻塞库，aiohttp 是异步非阻塞库，核心差别在于「并发能力」。

在 Agent 开发中，我们经常需要并发调用多个 API：比如同时查 RAG、调用工具、查询数据库。

如果用 requests：
- 每个请求阻塞当前协程/线程
- 即使开 100 个线程也只能并发 100 个请求
- 线程切换开销大

如果用 aiohttp：
- 一个协程就能管几千个请求
- 遇到 IO 等待自动让出 CPU
- 完美适配 asyncio 生态（OpenAI SDK、LangChain 都用 async）

实测数据：100 个 HTTP 请求
- requests + 线程池：约 5-10 秒
- aiohttp：约 1 秒

所以 Agent 开发里所有 IO 操作必须用异步库，aiohttp 是标配。
"""


async def main():
    # await demo_session_reuse()
    await http_client_demo()


if __name__ == "__main__":
    import sys
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
