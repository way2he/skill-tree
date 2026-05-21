# 📁 Day01 代码目录

## 代码清单

| 文件名 | 功能说明 | 对应知识点 |
|--------|---------|-----------|
| `01_coroutine_basics.py` | 协程基础与事件循环 | - async/await<br>- create_task、gather<br>- 串行 vs 并发 |
| `02_async_traps.py` | async/await 6 个常见坑 | - 忘记 await<br>- time.sleep 误用<br>- 循环串行陷阱<br>- 异常处理 |
| `03_aiohttp_basics.py` | aiohttp 异步 HTTP 请求 | - ClientSession 复用<br>- GET/POST 请求<br>- 超时配置 |
| `04_semaphore_timeout.py` | 信号量并发控制 + 超时机制 | - asyncio.Semaphore<br>- asyncio.wait_for |
| `05_production_crawler.py` | 生产级异步爬虫（压轴）| - 信号量并发控制<br>- 超时机制<br>- 指数退避重试<br>- 错误分类处理 |

---

## 学习顺序

```
01_coroutine_basics.py（理解协程）
    ↓
02_async_traps.py（避开常见坑）
    ↓
03_aiohttp_basics.py（学异步 HTTP）
    ↓
04_semaphore_timeout.py（学并发控制）
    ↓
05_production_crawler.py（综合压轴 ⭐）
```

---

## 每个代码文件的学习要点

### 📌 01_coroutine_basics.py
- 理解 `async/await` 的运行机制
- 对比串行 vs `create_task` vs `gather` 三种方式
- 能讲清楚协程和线程的区别
- 知道为什么不能用 `time.sleep()`

### 📌 02_async_traps.py
- 6 个最常见的异步编程坑及解法
- 重点：忘记 await、循环里 await、return_exceptions
- 理解协程函数 vs 协程对象的区别
- CPU 密集任务为什么不适合 async

### 📌 03_aiohttp_basics.py
- 理解为什么用 aiohttp 不用 requests
- 必须复用 ClientSession（生产级最佳实践）
- GET/POST/JSON/Headers 完整用法
- 全局超时配置 `ClientTimeout`

### 📌 04_semaphore_timeout.py
- 理解信号量的工作原理（计数器 + 等待队列）
- `Semaphore(N)` 限制最大并发数
- `asyncio.wait_for(coro, timeout=N)` 实现超时
- `TimeoutError` 异常处理

### 📌 05_production_crawler.py（⭐ 面试压轴）
- **必须能闭眼写出来**：信号量 + 超时 + 重试 + 错误分类
- 4xx 不重试、5xx 和网络错误重试的判断
- 指数退避 + jitter 抖动的完整实现
- Agent 开发中 90% 的 API 调用都是这个模式！

---

## 面试必背代码

以下 2 段代码是面试高频，必须能默写：

### 1. 生产级 fetch_with_retry 函数（05 文件）
重点：信号量获取 → 请求 → 4xx/5xx/超时分类处理 → 指数退避重试

### 2. 并发爬虫主入口
重点：创建 Session（全局唯一） → 创建信号量 → 创建任务 → gather 并发

---

## 拓展思考

1. 如果要支持自定义重试策略（线性 vs 指数）怎么改？
2. 如果要做断点续传（失败后从上次位置继续）怎么实现？
3. 如果某些 URL 优先级更高（先爬完），怎么用优先队列？
4. 如果遇到大量 429（限流），怎么动态降速？

---

**💡 提示：这 5 段代码是 Agent 开发的「IO 基本功」，所有 LLM 调用、RAG 检索、工具调用都建立在这之上！**
