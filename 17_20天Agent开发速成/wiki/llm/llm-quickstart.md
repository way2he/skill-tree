---
title: LLM 统一接口层 — 使用教程
category: skill-tree/20天Agent速成/llm
tags: [LLM, Agent, 大模型, 统一接口, DeepSeek, OpenAI, Claude, Qwen]
created: 2026-05-23
updated: 2026-05-23
status: stable
source: raw/skill-tree/17_20天Agent开发速成/llm/
---

# 📘 LLM 统一接口层 — 使用教程

> 项目位置：`raw/skill-tree/17_20天Agent开发速成/llm/`
> 适用人群：想用一行代码统一调用 25 家大模型的开发者
> 最近更新：2026-05-23

---

## 🎯 1. 它能干什么

| 维度 | 能力 |
|------|------|
| 多厂商 | **25 家**统一接口（OpenAI/Claude/DeepSeek/Qwen/GLM/Kimi/豆包... 国内外全覆盖） |
| 调用模式 | 同步 / 异步 / 流式 / JSON 结构化 |
| 底层实现可选 | requests · aiohttp · OpenAI SDK · 厂商原生 SDK，**4 选 1** |
| 弹性 | 重试 / 熔断 / 限流 / 降级，装饰器一行接入 |
| 可观测 | 事件总线 + 日志 + 指标采集 |
| 调用方简洁度 | 从 `get_llm()` 一行调用到 Builder 链式构造，按场景选 |

---

## 🚀 2. 5 分钟上手（零参数）

### 准备

```bash
cd raw/skill-tree/17_20天Agent开发速成
pip install -e .            # 或: pip install requests aiohttp pydantic pyyaml
```

### 设置环境变量

```powershell
$env:LLM_PROVIDER     = "deepseek"     # 默认用哪家
$env:DEEPSEEK_API_KEY = "***"          # 对应的 key（每家厂商名都不同，见表）
```

### 调用代码（真的就 2 行）

```python
from llm.core import get_llm

print(get_llm().generate("用一句话解释 RAG"))
```

直接运行内置 demo：

```bash
py -3 -m llm.demo.demo_zero_config "解释一下 ReAct 模式"
py -3 -m llm.demo.demo_zero_config --list   # 看所有支持厂商
py -3 -m llm.demo.demo_zero_config --enum   # 看 ProviderName 枚举用法
```

### 厂商 → 环境变量速查

| 厂商 | env | 默认模型 |
|------|-----|---------|
| openai | `OPENAI_API_KEY` | gpt-4o-mini |
| deepseek | `DEEPSEEK_API_KEY` | deepseek-chat |
| anthropic | `ANTHROPIC_API_KEY` | claude-sonnet-4 |
| qwen | `DASHSCOPE_API_KEY` | qwen-plus |
| glm | `ZHIPU_API_KEY` | glm-4 |
| kimi | `MOONSHOT_API_KEY` | moonshot-v1-32k |
| doubao | `ARK_API_KEY` | doubao-pro-32k |
| ollama | （无需） | qwen2.5:7b |
| 其余 17 家 | 各自 client 顶部注释 | — |

---

## 🧭 3. 三种“指定厂商”的写法（按场景选）

```python
from llm.core import get_llm, ProviderName, create_llm

# 写法 ①：零参数（业务首选，由环境/YAML 决定）
llm = get_llm()

# 写法 ②：枚举（多厂商切换，IDE 自动补全，拼写错立即报错）
llm = get_llm(ProviderName.DEEPSEEK)

# 写法 ③：字符串 + 自定义参数（需要传 model/base_url 等）
llm = create_llm("openai", model="gpt-4o-mini", base_url="https://api.openai.com/v1")
```

**`get_llm` vs `create_llm`：**

- `get_llm` — 带 lru_cache，三种等价写法命中同一个实例（业务常用）
- `create_llm` — 不缓存、可传完整参数（参数化定制时用）

---

## 💬 4. 四种调用方式

### 4.1 非流式

```python
text = llm.generate("你好")                          # 只要字符串
resp = llm.generate_with_response("你好")             # 拿到 token/延迟/模型名
print(resp.content, resp.model, resp.latency_ms, resp.total_tokens)
```

### 4.2 JSON 结构化（带 Schema）

```python
import json
schema = {"intent": "string", "confidence": "number", "keywords": ["string"]}
raw = llm.generate_json("我想订一束生日鲜花", schema=schema)
data = json.loads(raw)        # {'intent': '鲜花订购', ...}
```

👉 看完整示例：`py -3 -m llm.demo.demo_json`

### 4.3 同步流式

```python
for chunk in llm.generate_stream("写一首五绝"):
    print(chunk, end="", flush=True)
```

### 4.4 异步流式

```python
import asyncio
from llm.core import get_async_llm, ProviderName

async def main():
    llm = get_async_llm(ProviderName.DEEPSEEK)
    async for chunk in llm.generate_stream("写一首五绝"):
        print(chunk, end="", flush=True)

asyncio.run(main())
```

> ⚙️ **25 家全部已实现真流式**（OpenAI/Anthropic/Ollama/Cohere/Gemini/Hunyuan/Wenxin 7 个协议族）。

---

## 🔌 5. 底层实现可选（Backend Selector）

每家厂商可以走 4 种底层实现：

| Backend | 用途 | 适合场景 |
|---------|------|---------|
| `requests` | 同步 HTTP | 默认；脚本/小工具 |
| `aiohttp` | 异步 HTTP | 高并发 / Agent 多任务 |
| `openai_sdk` | OpenAI 官方 SDK | 厂商提供了 OpenAI 兼容接口（DeepSeek/Qwen 等） |
| `native_sdk` | 厂商原生 SDK | 用厂商专属能力（如 Anthropic tool use） |

### 5.1 一键设置全局默认（推荐）

```python
from llm.core import set_default_backend, get_llm
set_default_backend("aiohttp")           # 全局生效
llm = get_llm("deepseek")                # 自动用 aiohttp
```

或者环境变量：

```powershell
$env:LLM_BACKEND = "openai_sdk"
```

或者 YAML（最持久）：

```yaml
# llm/core/llm_config.yaml
default_backend: openai_sdk
providers:
  deepseek:
    backend: openai_sdk    # 厂商级覆盖全局
```

### 5.2 Builder 链式（参数多时用）

```python
from llm.core import LLMClientBuilder

client = (LLMClientBuilder()
    .provider("deepseek")
    .openai_sdk()                        # 等价于 .backend("openai_sdk")
    .api_key("sk-***")
    .base_url("https://api.deepseek.com/v1")
    .model("deepseek-chat")
    .temperature(0.7)
    .timeout(30)
    .build())
```

### 5.3 运行时切换 + 故障转移

```python
from llm.core import BackendSwitcher

switcher = (BackendSwitcher("deepseek")
    .add_backend("requests",  api_key="sk-***")
    .add_backend("openai_sdk", api_key="sk-***", base_url="..."))

# 故障转移：按顺序尝试，第一个成功的返回
client = switcher.get_client_with_fallback(["openai_sdk", "requests"])
```

👉 看完整示例：`py -3 -m llm.demo.demo_backend_selector`

### Backend 解析优先级

```
1. Builder/便捷函数显式 backend=
2. YAML providers.<name>.backend
3. set_default_backend(...)
4. 环境变量 LLM_BACKEND
5. YAML default_backend
6. 兜底：同步=requests，异步=aiohttp
```

---

## 🛡️ 6. 弹性机制（重试 / 熔断 / 限流 / 降级）

### 6.1 一行装饰器（最简单）

```python
from llm.core import get_llm, resilient, ResilienceConfig

@resilient(ResilienceConfig(
    retry_max_retries=3,
    rate_limiter_requests_per_minute=60,
))
def ask(q: str) -> str:
    return get_llm().generate(q)
```

### 6.2 单独组件

```python
from llm.core import (
    RetryPolicy, with_retry,                              # 重试
    CircuitBreaker, CircuitBreakerConfig,                  # 熔断
    TokenBucketRateLimiter, RateLimiterConfig,             # 限流
    FallbackStrategy, AsyncFallbackStrategy,               # 降级
    with_async_retry, async_resilient,                     # 异步版
)

# 重试
@with_retry(RetryPolicy(max_retries=3, base_delay=1.0))
def call(): ...

# 限流
limiter = TokenBucketRateLimiter(RateLimiterConfig(requests_per_second=2))
@limiter
def call(): ...

# 降级
fb = FallbackStrategy(
    primary=client_a,
    fallbacks=[client_b, client_c],
    on_fallback=lambda i, e: print(f"降到 #{i}：{e}"),
)
text = fb.generate("hi")
```

👉 看完整示例：

- `py -3 -m llm.demo.demo_resilience`（基础）
- `py -3 -m llm.demo.demo_resilience_full`（限流/降级/异步组合，**离线可跑**）

---

## 👁️ 7. 可观测（事件总线 + 指标）

```python
from llm.core import EventBus, LoggingHandler, MetricsHandler

bus = EventBus()
bus.subscribe(None, LoggingHandler(log_prompt=False))  # 自动日志
metrics = MetricsHandler()
bus.subscribe(None, metrics)                            # 自动指标

# … 业务调用之后 …
print(metrics.get_metrics())
# {'total_requests': 10, 'success_rate': 0.9, 'avg_latency_ms': 423.7, ...}
```

---

## 📂 8. 配置文件驱动（YAML）

`llm/core/llm_config.yaml`：

```yaml
default_provider: deepseek
default_backend: requests

providers:
  deepseek:
    api_key: ${DEEPSEEK_API_KEY}      # 支持环境变量替换
    model: deepseek-chat
    backend: openai_sdk                # 厂商级覆盖
  openai:
    api_key: ${OPENAI_API_KEY}
    model: gpt-4o-mini

resilience:
  retry_max_retries: 3
  rate_limiter_requests_per_minute: 60
```

调用：

```python
from llm.core import create_llm_from_config, create_llm_async_from_config

llm = create_llm_from_config("llm/core/llm_config.yaml")
# 异步
async_llm = create_llm_async_from_config("llm/core/llm_config.yaml")
```

👉 看完整示例：`py -3 -m llm.demo.demo_config`

---

## 🧩 9. 扩展自定义厂商（私有模型 / Mock）

把自己的 client 类注册进框架，就能被 `get_llm` 统一调度。

```python
from llm.core import register_provider, create_llm, RequestsLLMAdapter

class MyClient:
    default_model = "my-v1"
    def __init__(self, prefix="[echo] ", **_):
        self.prefix, self.model = prefix, self.default_model
    def generate(self, prompt, **kw):       return self.prefix + prompt
    def generate_json(self, prompt, schema=None, **kw):
        import json; return json.dumps({"echo": prompt})
    def generate_stream(self, prompt, **kw):
        for ch in self.prefix + prompt: yield ch

# 注册（1 行）
register_provider("myllm", MyClient, RequestsLLMAdapter)

# 使用（和官方 25 家一模一样）
llm = create_llm("myllm", prefix="🎉 ")
print(llm.generate("hello"))                    # 🎉 hello
for ch in llm.generate_stream("流式"): print(ch, end="")
```

异步同理：`register_async_provider(name, AsyncClient, AioHttpLLMAdapter)`

👉 看完整示例：`py -3 -m llm.demo.demo_register`

---

## 🚨 10. 异常处理

```python
from llm.core import (
    LLMError,                     # 所有异常基类
    LLMConnectionError,           # 网络断
    LLMAuthError,                 # API Key 错
    LLMRateLimitError,            # 被限流
    LLMServerError,               # 5xx
    LLMTimeoutError,              # 超时
    LLMResponseError,             # 解析失败
    LLMCircuitOpenError,          # 熔断器打开
    LLMProviderNotFoundError,     # 未注册的厂商
    LLMConfigError,               # 配置文件错
)

try:
    text = get_llm().generate("hi")
except LLMTimeoutError:
    text = "超时了，请稍后重试"
except LLMRateLimitError as e:
    text = f"被限流，建议 retry-after={e.retry_after}s"
except LLMError as e:                 # 兜底
    text = f"调用失败：{e}"
```

---

## 🗺️ 11. 全部 11 个 Demo 速查

| Demo | 命令 | 演示 |
|------|------|------|
| 零参数 | `py -3 -m llm.demo.demo_zero_config` | `get_llm()` + 枚举 + `--list` |
| 流式 | `py -3 -m llm.demo.demo_stream "你的问题" --async` | 同/异步流式 + 枚举 |
| 最小同步 | `py -3 -m llm.demo.demo_basic` | `create_llm` + 三种 `generate` |
| YAML 配置 | `py -3 -m llm.demo.demo_config` | 同/异步 YAML 驱动 |
| 多厂商对比 | `py -3 -m llm.demo.demo_compare "你的问题"` | 一题多答横向对比 |
| JSON 结构化 | `py -3 -m llm.demo.demo_json --async` | `generate_json` + Schema |
| 扩展注册 | `py -3 -m llm.demo.demo_register` | 自定义 client（离线可跑） |
| 弹性基础 | `py -3 -m llm.demo.demo_resilience` | 重试 + 熔断 + 指标 |
| 弹性进阶 | `py -3 -m llm.demo.demo_resilience_full` | 限流/降级/异步组合（**离线可跑**） |
| Backend 选择器 | `py -3 -m llm.demo.demo_backend_selector` | 一键配置 + Builder + 切换 |
| 异步 Backend | `py -3 -m llm.demo.demo_backend_async` | 异步 Builder + 最佳实践 |

---

## 🏗️ 12. 一张图看架构

```
你的业务代码
    │
    ├── get_llm() / get_async_llm()         ← 零参数（业务首选）
    │       ↓ default.py 解析 provider
    │
    ├── get_llm(ProviderName.DEEPSEEK)      ← 枚举（IDE 补全）
    │
    ├── create_llm("openai", model=...)     ← 显式参数
    │
    ├── LLMClientBuilder().provider(...)...build()   ← 链式 Builder
    │
    └── BackendSwitcher(...)                ← 运行时切换 / 故障转移
              │
              ↓ factory.py 查注册表 + backend.py 选实现
              ↓
        adapter/ 适配器（统一接口）
              │
              ↓ 4 选 1
   ┌──────────┼──────────┬──────────────┐
   ↓          ↓          ↓              ↓
 requests   aiohttp   openai_sdk    native_sdk
 (同步HTTP) (异步HTTP) (OpenAI兼容)   (厂商SDK)
   │          │          │              │
   ↓          ↓          ↓              ↓
        llm/requests/providers/*.py
        llm/aiohttp/providers/*.py
        … 25 家 client（apikey 自动 os.getenv）
```

---

## 🧠 13. 常见使用决策表

| 我想... | 用这个 |
|---------|--------|
| 业务代码尽量简洁 | `get_llm().generate(...)` + 环境变量 |
| 多厂商切换 / 不写死字符串 | `get_llm(ProviderName.DEEPSEEK)` |
| 同一段代码跑多家做对比 | `for p in [ProviderName.QWEN, ...]: get_llm(p)...` |
| 异步 + 高并发 | `set_default_backend("aiohttp")` + `get_async_llm()` |
| 用 OpenAI 官方 SDK 接 DeepSeek | `set_default_backend("openai_sdk")` |
| 私有部署的模型 | `register_provider("myllm", MyClient, ...)` |
| 多环境（dev/prod 用不同 key） | YAML 配置 + `create_llm_from_config` |
| 加自动重试 | `@resilient(ResilienceConfig(retry_max_retries=3))` |
| 想知道每次调用花多久、用了多少 token | `MetricsHandler` + `EventBus` |
| Demo 不真调 API 也能跑 | `demo_register` / `demo_resilience_full` |

---

## ⚠️ 14. 三个常见坑

1. **`py -3 -m llm.demo.xxx` 必须在项目根目录跑** — 即 `17_20天Agent开发速成/`，否则 `llm.` 包路径会找不到
2. **环境变量必须设对** — 厂商名 ≠ 环境变量名（例如 `qwen` 对应 `DASHSCOPE_API_KEY`，不是 `QWEN_API_KEY`）
3. **`list_providers()` 返回空？** — 缺依赖：`pip install requests aiohttp pydantic pyyaml`

---

## 📚 15. 进一步阅读

| 文档 | 路径 |
|------|------|
| 顶层入口文档 | `llm/README.md` |
| 实现细节 + 设计模式 | `llm/core/README.md` |
| YAML 配置样例 | `llm/core/llm_config.yaml` |
| 同步实现源码 | `llm/requests/providers/*.py`（25 家） |
| 异步实现源码 | `llm/aiohttp/providers/*.py`（25 家） |
| Backend 选择器源码 | `llm/core/backend.py` |

---

## 🎬 最后一段：一分钟跑通

```powershell
# 1. 切到项目根
cd raw\skill-tree\17_20天Agent开发速成

# 2. 装依赖
pip install -e .

# 3. 配 key（任选一家）
$env:LLM_PROVIDER     = "deepseek"
$env:DEEPSEEK_API_KEY = "***"

# 4. 跑
py -3 -m llm.demo.demo_zero_config "用一句话解释 RAG"
py -3 -m llm.demo.demo_stream "写一首五绝" --async
py -3 -m llm.demo.demo_register             # 不要 key 也能跑，看注册机制
py -3 -m llm.demo.demo_resilience_full      # 不要 key 也能跑，看弹性机制
```

跑通这 4 条命令，整个 `llm/` 框架的 80% 用法你就吃透了。剩下 20% 看 `demo_backend_selector` / `demo_backend_async` / `demo_config` 即可。

