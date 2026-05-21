---
name: Day01 - Python异步编程深度（面试高频考点）
description: Day01 完整学习计划：精确到分钟，每个知识点对应面试考点，代码实战+面试话术一条龙
type: learning
tags: ["Python", "异步编程", "aiohttp", "面试", "并发控制"]
created_at: 2026-05-19
updated_at: 2026-05-21
version: interview
---

# 🚀 Day 01：Python 异步编程深度

- **学习日期**：第 1 天 / 共 20 天
- **学习时长**：8 小时
- **核心目标**：闭着眼写出带并发控制、超时、重试的异步请求函数，所有异步面试题全部搞定

***

## 📋 今日学习清单

|  序号 | 学习内容                      | 完成情况 |
| :-: | ------------------------- | ---- |
|  1  | 异步编程核心概念                  | ✅    |
|  2  | async/await 语法实战 + 常见坑    | ✅    |
|  3  | aiohttp 异步 HTTP 请求实战      | ✅    |
|  4  | 信号量 Semaphore 并发控制原理 + 实战 | ✅    |
|  5  | 超时机制 + 指数退避重试原理 + 实战      | ✅    |
|  6  | 完整异步批量请求项目实战              | ✅    |
|  7  | 【面试题专项】10 道异步编程面试题        | ✅    |
|  8  | 复盘 + 整理面试话术 + 写心得         | ✅    |

💡 **学习建议**：按顺序学习效果最佳，但您可以根据自己的节奏自由安排！

***

## 🎯 一、异步编程核心概念

### 📝 核心知识点 + 对应面试考点

| 知识点           | 面试考点               | 回答要点                                                                                                      |
| :------------ | :----------------- | --------------------------------------------------------------------------------------------------------- |
| **什么是协程？**    | 协程和线程的区别？分别适用什么场景？ | - 协程是用户态调度，线程是内核态调度 - 协程切换开销极小（函数调用级），线程切换开销大 - 协程数量可以开到 10 万+，线程一般几百个就到瓶颈**场景**：协程适合 IO 密集型，线程适合 CPU 密集型 |
| **什么是事件循环？**  | 事件循环的工作原理是什么？      | - 单线程跑所有协程 - 不断循环：检查哪些协程就绪了 → 执行就绪的协程 - 遇到 IO 等待就切走，不阻塞 - 本质：用单线程模拟并发，避免线程切换开销                            |
| **什么是可等待对象？** | await 到底在等什么？      | - 协程函数、Task、Future 都是可等待对象 - 遇到 await，当前协程暂停，让事件循环去跑别的 - 等 await 的东西完成了，再回来继续跑后面的代码                       |
| **并发 vs 并行**  | 并发和并行的区别？          | - 并发：交替执行，看起来同时在跑（单线程） - 并行：真的同时在跑（多核 CPU） - Agent 开发 90% 是 IO 密集型，所以并发更重要                                |

### 💡 类比理解

- **协程 = 你在家烧水 + 切菜 + 煮饭**
  - 水烧上了不等，去切菜（遇到 await 切走）
  - 菜切到一半饭熟了响了，去关火（IO 完成，切回来继续）
  - 一个人同时干多件事 = 单线程并发
- **线程 = 雇 3 个工人，一人干一件事**
  - 开销大，人多了工资高（内存占用大）、调度麻烦（上下文切换）

### ✅ 本小节验收

- \[✅] 能流利说出协程和线程的 3 个核心区别
- \[✅] 能解释清楚事件循环的工作原理
- \[✅] 能说出什么场景用协程，什么场景用线程

***

## 🎯 二、async/await 语法实战 + 常见坑

### 📝 核心知识点 + 对应面试考点

| 知识点                        | 面试考点                            | 回答要点                                                                       |
| -------------------------- | ------------------------------- | -------------------------------------------------------------------------- |
| **async def 定义协程**         | 调用 async def 函数得到了什么？直接调用会发生什么？ | 1. 不是直接执行，返回一个协程对象2. 直接调用不 await 会报警告：`coroutine was never awaited`        |
| **await 语法**               | 什么东西可以 await？不 await 会怎么样？      | 1. 只有可等待对象才能 await：协程、Task、Future2. 不 await = 协程永远不执行，资源泄漏                 |
| **asyncio.create\_task()** | create\_task() 和直接 await 的区别？   | 1. 直接 await = 串行执行，一个完了才能下一个2. create\_task() = 并发执行，交给事件循环调度3. 这是实现并发的核心！ |

### 💻 必写代码 1：串行 vs 并发对比

```python
# -*- coding: utf-8 -*-
import asyncio
import time

async def hello(name, delay):
    print(f"开始: {name}, 时间: {time.time() - start:.2f}s")
    await asyncio.sleep(delay)
    print(f"完成: {name}, 时间: {time.time() - start:.2f}s")

async def main_serial():
    """串行执行：总耗时 2+1 = 3秒"""
    print("\n=== 串行执行 ===")
    await hello("A", 2)
    await hello("B", 1)

async def main_concurrent():
    """并发执行：总耗时 max(2,1) = 2秒"""
    print("\n=== 并发执行 ===")
    task1 = asyncio.create_task(hello("A", 2))
    task2 = asyncio.create_task(hello("B", 1))
    await task1
    await task2

if __name__ == "__main__":
    start = time.time()
    
    # Windows 平台加这行，避免 Event Loop is closed 错误
    import sys
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main_serial())
    asyncio.run(main_concurrent())
    
    print(f"\n✅ 结论：并发比串行快 {round((3/2 - 1)*100)}%！")
```

### ⚠️ 常见坑 1：忘了 await

```python
# ❌ 错误：协程创建了但永远不执行
async def bad():
    hello("A", 2)  # 没 await！RuntimeWarning

# ✅ 正确
async def good():
    await hello("A", 2)
```

### ⚠️ 常见坑 2：不要用 time.sleep()

```python
# ❌ 错误：time.sleep() 是同步的，会阻塞整个事件循环
async def bad():
    time.sleep(2)  # 所有协程都卡住了！

# ✅ 正确：用 asyncio.sleep()
async def good():
    await asyncio.sleep(2)
```

### ✅ 本小节验收

- \[✅] 能写出上面的代码，理解串行 vs 并发的区别
- \[✅] 能说出 create\_task() 的作用
- \[✅] 知道 2 个最常见的异步坑

***

## 🎯 aiohttp 异步 HTTP 请求实战

### 📝 核心知识点 + 对应面试考点

| 知识点                     | 面试考点                               | 回答要点                                                                                       |
| ----------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------ |
| **aiohttp vs requests** | 为什么要用 aiohttp 不用 requests？         | 1. requests 是同步的，发请求的时候整个线程卡住2. aiohttp 是异步的，等响应的时候可以跑别的协程3. 并发 100 个请求的时候，aiohttp 快 100 倍 |
| **ClientSession 复用**    | ClientSession 为什么要复用？每个请求新建一个会怎么样？ | 1. TCP 连接复用，减少三次握手开销2. 每个请求新建 = 每次都握手，慢 2-3 倍3. 连接太多会耗尽本地端口                                |
| **async with 上下文管理器**   | async with 和 with 的区别？             | 1. with 是同步的上下文管理器2. async with 是异步的，`__aenter__` 和 `__aexit__` 是协程3. 保证异常时资源也能正确释放        |

### 💻 必写代码 2：aiohttp 基础

```python
# -*- coding: utf-8 -*-
import asyncio
import aiohttp

async def fetch_url(session, url):
    async with session.get(url) as response:
        print(f"URL: {url}, 状态码: {response.status}")
        return await response.text()

async def main():
    # ✅ 正确：整个应用共用一个 ClientSession，复用 TCP 连接
    async with aiohttp.ClientSession() as session:
        html1 = await fetch_url(session, "https://httpbin.org/get")
        html2 = await fetch_url(session, "https://httpbin.org/delay/1")
        print(f"响应1长度: {len(html1)}, 响应2长度: {len(html2)}")

if __name__ == "__main__":
    import sys
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
```

### ❌ 错误写法示范（千万不要这么写）

```python
# ❌ 错误：每个请求新建一个 ClientSession，每次都三次握手
async def bad():
    urls = ["https://httpbin.org/get" for _ in range(10)]
    for url in urls:
        async with aiohttp.ClientSession() as session:  # 每次新建 = 慢 2-3 倍！
            await session.get(url)
```

### ✅ 本小节验收

- \[✅] 能写出上面的 aiohttp 基础代码
- \[✅] 能说出 ClientSession 为什么要复用
- \[✅] 能说出 aiohttp 相比 requests 的优势

***

## 🎯 信号量 Semaphore 并发控制原理 + 实战

### 📝 核心知识点 + 对应面试考点

| 知识点                               | 面试考点         | 回答要点                                                                                           |
| --------------------------------- | ------------ | ---------------------------------------------------------------------------------------------- |
| **为什么需要控制并发？**                    | 不控制并发会怎么样？   | 1. 服务器有 QPS 限制，并发太高会被封 IP2. 本地端口有限，TCP 连接数有限3. 太多并发会导致超时反而更多                                   |
| **信号量工作原理**                       | 信号量的工作原理是什么？ | 1. 类似许可证，比如 3 个许可证2. 每个协程进来先拿许可证，拿到了才能执行3. 执行完归还许可证，下一个协程才能拿4. 许可证没了就排队等                       |
| **Semaphore vs BoundedSemaphore** | 两者的区别？推荐用哪个？ | 1. Semaphore 可以 release() 多次，许可证数会超过初始值2. BoundedSemaphore 不允许超过初始值，更安全3. 推荐用 BoundedSemaphore |

### 💻 必写代码 3：信号量控制并发

```python
# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import time

MAX_CONCURRENT = 3  # 最多同时 3 个请求

async def fetch_with_semaphore(semaphore, session, url):
    async with semaphore:  # 先拿许可证，没拿到就在这等
        print(f"开始请求: {url}")
        async with session.get(url) as response:
            await asyncio.sleep(1)  # 模拟耗时
            print(f"完成请求: {url}, 状态码: {response.status}")
            return response.status

async def main():
    semaphore = asyncio.BoundedSemaphore(MAX_CONCURRENT)
    timeout = aiohttp.ClientTimeout(total=10)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        urls = [f"https://httpbin.org/delay/1?i={i}" for i in range(10)]
        tasks = [fetch_with_semaphore(semaphore, session, url) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    import sys
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    start = time.time()
    asyncio.run(main())
    print(f"\n✅ 总耗时: {time.time() - start:.2f} 秒")
    print(f"✅ 观察：同时最多只有 {MAX_CONCURRENT} 个请求在执行！")
```

### ✅ 运行后你会看到

- 同时只有 3 个请求在跑
- 3 个完成了，接下来 3 个才开始
- 总耗时约 4 秒（10 个请求 / 3 并发 = 3.33 轮）

### ✅ 本小节验收

- [x] 能写出上面的信号量控制代码
- [x] 能解释清楚信号量的工作原理
- [x] 知道为什么需要控制并发

***

## 🎯 超时机制 + 指数退避重试原理 + 实战

### 📝 核心知识点 + 对应面试考点

| 知识点          | 面试考点                      | 回答要点                                                                       |
| ------------ | ------------------------- | -------------------------------------------------------------------------- |
| **为什么需要超时？** | 不加超时会怎么样？所有外部 IO 都要加超时吗？  | 1. 网络是不可靠的，请求可能永远回不来2. 协程永远挂住，整个系统卡住3. 是的！所有外部 IO 必须加超时                    |
| **为什么需要重试？** | 重试策略有哪些？                  | 1. 网络抖动、服务器临时故障都可能失败2. 重试策略：立即重试、固定间隔、指数退避3. 不是所有错误都要重试（4xx 不要重试，5xx 可以重试） |
| **指数退避原理**   | 指数退避为什么是 2 的幂次？固定间隔重试的问题？ | 1. 重试间隔越来越长，给服务器恢复的时间2. 固定间隔 = 大家同时重试，服务器雪崩3. 指数退避 = 重试越来越稀疏，避免风暴          |

### 💻 必写代码 4：指数退避重试完整实现

```python
# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import logging
from aiohttp import ClientTimeout

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

MAX_RETRIES = 3
INITIAL_DELAY = 1  # 初始 1 秒
MAX_CONCURRENT = 3

async def fetch_with_retry(session, url, max_retries=MAX_RETRIES):
    """带指数退避重试的异步请求"""
    for attempt in range(max_retries):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    logger.info(f"✅ 成功: {url}, 第 {attempt+1} 次尝试")
                    return await response.json()
                else:
                    logger.warning(f"⚠️ 状态码 {response.status}: {url}")
                    if 400 <= response.status < 500:
                        return None  # 4xx 客户端错误，不重试
                    
        except Exception as e:
            logger.warning(f"❌ 失败: {url}, 第 {attempt+1} 次尝试, 错误: {str(e)}")
        
        # 指数退避等待
        if attempt < max_retries - 1:
            delay = INITIAL_DELAY * (2 ** attempt)  # 1s → 2s → 4s
            logger.info(f"⏳ {delay} 秒后重试...")
            await asyncio.sleep(delay)
    
    logger.error(f"❌ 最终失败: {url}, 重试了 {max_retries} 次")
    return None

async def main():
    semaphore = asyncio.BoundedSemaphore(MAX_CONCURRENT)
    timeout = ClientTimeout(total=10)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        urls = [
            "https://httpbin.org/status/500",  # 会失败重试
            "https://httpbin.org/status/404",  # 4xx，不重试
            "https://httpbin.org/delay/2",     # 正常
        ]
        tasks = [fetch_with_retry(session, url) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    import sys
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
```

### ✅ 运行后你会看到

- 500 错误会重试 3 次，间隔 1s → 2s → 4s
- 404 错误直接放弃，不重试
- 正常请求一次成功

### ✅ 本小节验收

- [x] 能写出上面的指数退避重试代码
- [x] 能说出为什么 4xx 不重试，5xx 可以重试
- [x] 能解释清楚指数退避为什么是 2 的幂次

***

## 🎯 完整异步批量请求项目实战

### 💻 终极代码：Day01 完整版（面试必背！）

完整代码见：`code/async_complete.py`

**包含功能（面试写出来直接加分！）**：

1. ✅ 信号量并发控制
2. ✅ 超时控制
3. ✅ 指数退避重试
4. ✅ 4xx/5xx 错误分类处理
5. ✅ 进度打印和日志
6. ✅ 成功/失败统计

### ✅ 本小节验收

- [x] 完整代码能跑通，没有报错
- [x] 能解释清楚代码里每一行的作用
- [x] 能在 10 分钟内默写出核心逻辑

***

## 🎯【面试题专项】10 道异步编程面试题

### 🔥 高频面试题（必须全部能答出来！）

| #  | 面试题                                     | 难度   | 答案位置          |
| -- | --------------------------------------- | ---- | ------------- |
| 1  | 协程和线程的区别？分别适用什么场景？                      | ⭐⭐   | `面试题_标准答案.md` |
| 2  | async/await 到底在做什么？await 到底在等什么？        | ⭐⭐   | `面试题_标准答案.md` |
| 3  | 为什么要用 aiohttp 不用 requests？aiohttp 快在哪里？ | ⭐⭐   | `面试题_标准答案.md` |
| 4  | ClientSession 为什么要复用？每个请求新建一个会怎么样？      | ⭐⭐⭐  | `面试题_标准答案.md` |
| 5  | 信号量的工作原理？为什么需要控制并发？                     | ⭐⭐⭐  | `面试题_标准答案.md` |
| 6  | 指数退避重试为什么是 2 的幂次？固定间隔重试的问题？             | ⭐⭐⭐  | `面试题_标准答案.md` |
| 7  | 不加超时会怎么样？所有外部 IO 都要加超时吗？                | ⭐⭐   | `面试题_标准答案.md` |
| 8  | asyncio.create\_task() 和直接 await 的区别？   | ⭐⭐   | `面试题_标准答案.md` |
| 9  | 什么是事件循环？它的工作原理是什么？                      | ⭐⭐⭐  | `面试题_标准答案.md` |
| 10 | 手写：带并发控制、超时、重试的异步请求函数                   | ⭐⭐⭐⭐ | `面试题_标准答案.md` |

### ✅ 本小节验收

- [x] 全部 10 道题都能流利回答
- [x] 第 10 道代码题能在 10 分钟内写对

***

## 🎯 八、复盘 + 整理面试话术

### 📝 3 分钟面试回答模板（背下来！）

- **面试官问**：你做过异步编程吗？说说你对 Python 异步的理解？

**你的回答（3 分钟版本，一字不差背下来！）**：

- "我对 Python 异步编程有比较深入的理解和实战经验。简单说，异步编程就是在单线程里利用 IO 等待的时间来同时处理多个任务，特别适合 IO 密集型场景，比如调用大模型 API、批量 HTTP 请求这种场景。
- 核心概念有三个：协程、事件循环、可等待对象。协程可以暂停和恢复，开销很小；事件循环是调度器，单线程跑所有协程；遇到 await 的时候当前协程暂停，让事件循环去跑别的就绪的协程，等 IO 完成了再切回来。
- 我实战中用 aiohttp 写过异步批量请求，做了三层优化：第一是 ClientSession 复用，避免每次新建 TCP 连接的三次握手开销；第二是用 BoundedSemaphore 信号量控制并发数，避免并发太高被服务器封或者本地端口耗尽；第三是加了超时控制和指数退避重试，1 秒、2 秒、4 秒间隔重试，4xx 客户端错误不重试，5xx 和网络错误才重试。
- 最后效果是原来同步请求 100 次要 100 秒，用异步优化后只需要 5-10 秒，性能提升了 10-20 倍。"

### ✅ Day01 最终验收标准（全部做到才能进入 Day02！）

#### 代码能力

- [x] 能闭着眼写出带并发控制、超时、重试的异步请求函数（10 分钟内写完）
- [x] 完整代码能跑通，没有报错
- [x] 能解释清楚代码里每一行的作用

#### 理论理解

- [x] 能说出协程和线程的 3 个核心区别
- [x] 能解释清楚信号量的工作原理
- [x] 能说出指数退避重试为什么是 2 的幂次
- [x] 能说出为什么 ClientSession 要复用

#### 面试话术

- [x] 能流利地用 3 分钟说完上面的面试回答模板
- [x] 上面 10 道面试题全部能答对

### 📝 写今日心得（写到 `今日心得.md`）

1. 今天学到了什么？
2. 遇到了什么坑？怎么解决的？
3. 还有什么不懂的地方？

***

## 📎 相关文件

- 📖 完整代码：`code/async_complete.py`
- 📖 面试题：`面试题.md`
- 📖 面试题标准答案：`面试题_标准答案.md`
- 📖 今日心得：`今日心得.md`

***

**🎉 恭喜完成 Day01！你已经搞定了 Agent 开发最核心的基础能力，明天继续 Day02：Prompt 工程精通 + 过拟合与正则化！ 🚀**
