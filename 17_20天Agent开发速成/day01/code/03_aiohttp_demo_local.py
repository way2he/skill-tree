#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示：Session 复用 vs 每次新建（本地模拟）
"""

import asyncio
import time


class MockSession:
    """模拟 Session，记录创建和连接开销"""
    creation_cost = 1 
    reuse_cost = 0.01   

    def __init__(self):
        self.created_at = time.time()
        self.connection_count = 0
        print(f"  [Session] 新建 Session，开销: {self.creation_cost:.2f}s")

    async def get(self, url):
        """模拟 HTTP GET 请求"""
        self.connection_count += 1
        if self.connection_count == 1:
            await asyncio.sleep(self.creation_cost)
        else:
            await asyncio.sleep(self.reuse_cost)
        return {"url": url, "session_created": self.created_at}

    async def close(self):
        """关闭 Session"""
        await asyncio.sleep(0.05)


async def fetch_bad(url: str) -> dict:
    """错误：每次都新建 Session"""
    session = MockSession()
    try:
        return await session.get(url)
    finally:
        await session.close()


async def fetch_good(session: MockSession, url: str) -> dict:
    """正确：复用 Session"""
    return await session.get(url)


async def demo_session_reuse():
    """演示：Session 复用 vs 每次新建"""
    urls = ["http://example.com"] * 10
    print("测试规模：10 个请求")
    
    # ---------- 错误方式：每次新建 ----------
    print("\n" + "=" * 60)
    print("[ERROR] 每次新建 Session（慢、浪费资源）")
    print("=" * 60)
    start = time.time()
    results = await asyncio.gather(*[fetch_bad(url) for url in urls])
    elapsed = time.time() - start
    print(f"[TIME] 耗时：{elapsed:.2f} 秒, 成功: {len(results)}")
    
    # ---------- 正确方式：复用 Session ----------
    print("\n" + "=" * 60)
    print("[OK] 复用 Session（快、节省资源）")
    print("=" * 60)
    start = time.time()
    session = MockSession()
    try:
        results = await asyncio.gather(*[fetch_good(session, url) for url in urls])
    finally:
        await session.close()
    elapsed = time.time() - start
    print(f"[TIME] 耗时：{elapsed:.2f} 秒, 成功: {len(results)}")


asyncio.run(demo_session_reuse())