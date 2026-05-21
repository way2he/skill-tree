# asyncio介绍

**asyncio** 是 Python 标准库中的异步 I/O 框架，用于编写并发代码。核心特点：

- **单线程并发**：使用事件循环（Event Loop）在单线程中调度多个任务
- **协程（Coroutine）**：通过 `async def` 定义的函数，可以在执行过程中挂起/恢复
- **非阻塞 I/O**：网络请求、文件读写等操作不会阻塞整个程序

```python
import asyncio

async def hello():
    print("Hello")
    await asyncio.sleep(1)  # 挂起，让出控制权
    print("World")

# 运行协程
asyncio.run(hello())
```

---

# aiohttp介绍

**aiohttp** 是基于 asyncio 的异步 HTTP 客户端/服务器库：

- **客户端**：发起异步 HTTP 请求，支持连接池、会话保持
- **服务器**：构建高性能异步 Web 服务
- **与 requests 对比**：requests 是同步阻塞的，aiohttp 是异步非阻塞的

```python
import aiohttp
import asyncio

async def fetch():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.github.com') as resp:
            return await resp.json()

# 并发请求多个 URL
async def main():
    urls = ['url1', 'url2', 'url3']
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
```

---

# async跟await介绍

**async** 和 **await** 是 Python 异步编程的核心关键字：

| 关键字 | 作用 |
|--------|------|
| `async def` | 定义一个协程函数，调用时返回协程对象 |
| `await` | 等待一个可等待对象（协程、Task、Future）完成，期间让出控制权 |

```python
import asyncio

# async 定义协程
async def say_after(delay, what):
    await asyncio.sleep(delay)  # await 挂起当前协程
    print(what)

async def main():
    # 顺序执行（共 3 秒）
    await say_after(1, 'hello')
    await say_after(2, 'world')

    # 并发执行（共 2 秒）
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))
    await task1
    await task2

asyncio.run(main())
```

---

# Semaphore vs BoundedSemaphore

两者都是 asyncio 提供的信号量，用于控制并发数量：

| 特性 | Semaphore | BoundedSemaphore |
|------|-----------|------------------|
| **功能** | 限制同时访问资源的任务数 | 限制同时访问资源的任务数 |
| **释放次数** | 释放次数可以超过获取次数 | 释放次数不能超过获取次数 |
| **安全性** | 可能因编程错误导致计数器异常增大 | 更安全，防止计数器无限增长 |

```python
import asyncio

# Semaphore 示例 - 限制最多 3 个并发请求
semaphore = asyncio.Semaphore(3)

async def fetch(url):
    async with semaphore:  # 获取信号量
        print(f"Fetching {url}")
        await asyncio.sleep(1)
        # 自动释放信号量

# BoundedSemaphore 示例 - 更安全的版本
bounded_sem = asyncio.BoundedSemaphore(3)

async def safe_fetch(url):
    async with bounded_sem:
        print(f"Safe fetching {url}")
        await asyncio.sleep(1)
```

**推荐使用 BoundedSemaphore**：它能防止因代码逻辑错误（如重复释放）导致信号量计数器异常增大，从而失去限流作用。
