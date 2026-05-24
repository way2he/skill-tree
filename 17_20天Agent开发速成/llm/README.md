# LLM 顶层接口文档

> 本目录是 **20 天 Agent 开发速成** 项目的"大模型统一接入层"，对外提供 **零参数即可使用**、**多厂商可切换**、**同步/异步/流式全覆盖** 的统一调用接口。
>
> 维护者：知识库 / 学习项目
> 最近更新：2026-05-23

---

## 📋 功能矩阵

| 能力 | 顶层入口 | 状态 | 说明 |
|------|----------|------|------|
| 零配置入口 | `get_llm()` / `get_async_llm()` | ✅ | 调用方不写厂商名，自动按环境变量解析 |
| 指定厂商入口 | `get_llm(ProviderName.DEEPSEEK)` / `create_llm("openai", …)` | ✅ | **枚举优先**，也兼容字符串。枚举动态从注册表生成，不写死 |
| 非流式响应 | `generate()` / `generate_with_response()` / `generate_json()` | ✅ | 所有适配器实现 |
| 流式响应 | `generate_stream()` | ✅ | **25 家全部补齐真流式**（8 个协议族：OpenAI SSE / Anthropic SSE / Ollama NDJSON / Cohere NDJSON / Gemini SSE / Hunyuan SSE / Wenxin SSE） |
| 同步调用 | `get_llm() / create_llm()` | ✅ | 默认入口 |
| 异步调用 | `get_async_llm() / create_async_llm()` | ✅ | 底层 `llm.aiohttp.providers`，**25 家全部注册且全部有异步流式** |

> 💡 **枚举优点**：IDE 能自动补全、拼写错误立即报错；枚举是从注册表动态生成的，新增厂商时自动出现，不需要修改定义。

---

## 🚀 1. 零配置入口（推荐）

**调用方一行代码搞定，不写厂商名、不写 apikey。**

```python
from llm.core import get_llm

print(get_llm().generate("你好"))
```

### 厂商解析优先级（在 `llm/core/default.py` 内部完成）

```
1. 函数显式入参   get_llm("openai")           ← 仅临时覆盖
2. 环境变量       LLM_PROVIDER=deepseek
3. 配置文件       llm/core/llm_config.yaml → default_provider
4. 兜底           "ollama"（本地无需 key）
```

### apikey 自动取值（底层封装）

各厂商 `XxxClient.__init__` 会自动 `os.getenv("XXX_API_KEY")`，调用方完全不感知：

| 厂商 | 环境变量 |
|------|----------|
| deepseek | `DEEPSEEK_API_KEY` |
| openai | `OPENAI_API_KEY` |
| anthropic | `ANTHROPIC_API_KEY` |
| qwen（阿里通义千问） | `DASHSCOPE_API_KEY` |
| glm（智谱） | `ZHIPU_API_KEY` |
| kimi（月之暗面） | `MOONSHOT_API_KEY` |
| doubao（豆包） | `ARK_API_KEY` |
| ollama（本地） | — 无需 |
| 其他 18 家 | 见各 `llm/requests/providers/*.py` 顶部注释 |

### 实用辅助函数

```python
from llm.core import get_llm, current_provider, list_providers

print("当前默认厂商：", current_provider())   # 看实际会用谁
print("全部已注册   ：", list_providers())    # 看支持哪些
```

### 典型场景

```powershell
# 业务代码长期固定用 deepseek，只改环境变量
$env:LLM_PROVIDER = "deepseek"
$env:DEEPSEEK_API_KEY = "***"
py -3 -m llm.demo.demo_zero_config "用一句话解释 RAG"
```

---

## 🎯 2. 指定厂商入口（枚举优先，不写死字符串）

```python
from llm.core import get_llm, ProviderName

llm = get_llm(ProviderName.DEEPSEEK)        # ✅ 枚举，IDE 补全
llm = get_llm("deepseek")                   # ✅ 字符串也兑现
llm = get_llm("deepseek-typo")              # ⚠️ 字符串不抦错（到运行期才倒）
# vs:
ProviderName("deepseek-typo")               # ❌ 立即 ValueError
```

### 枚举动态生成

`ProviderName` 在 `llm/core/providers.py` 里**从注册表动态构造**：

```python
from llm.core import ProviderName, list_providers

print(list_providers())            # 运行期动态查
# → ['anthropic','baichuan','cohere','deepseek',…,'yi']  （25 个）

print(list(ProviderName))          # 枚举同步生成
# → [<ProviderName.OLLAMA: 'ollama'>, <ProviderName.OPENAI: 'openai'>, …]
```

新增厂商只需在 `factory.py` 的 `_register_builtin_providers()` 里补一行，`ProviderName` 自动跳出新成员，调用方无需修改。

### 传参型别 `ProviderLike`

```python
from llm.core import ProviderLike       # = Union[str, ProviderName]

def ask(prompt: str, provider: ProviderLike | None = None) -> str:
    return get_llm(provider).generate(prompt)
```

### 多厂商对比示例

```python
from llm.core import get_llm, ProviderName

for name in [ProviderName.DEEPSEEK, ProviderName.QWEN, ProviderName.GLM]:
    try:
        resp = get_llm(name).generate_with_response("什么是 Function Calling")
        print(f"[{name.value}] {resp.latency_ms:.0f}ms\n{resp.content[:80]}\n")
    except Exception as e:
        print(f"[{name.value}] 跳过：{e}")
```

### 支持的 25 家厂商

| 分类 | 枚举成员 |
|------|-----------|
| 本地 | `OLLAMA` |
| 国际 | `OPENAI` / `ANTHROPIC` / `GOOGLE` / `META` / `COHERE` / `MISTRAL` / `TOGETHER` / `XAI` |
| 国内大厂 | `QWEN` / `WENXIN` / `DOUBAO` / `HUNYUAN` / `PANGU` / `SPARK` / `MILM` |
| 国内创业 | `DEEPSEEK` / `GLM` / `KIMI` / `MINIMAX` / `BAICHUAN` / `YI` |
| 其他 | `SHANGTANG` / `STEPFUN` / `TIANGONG` |

---

## 📦 3. 响应方式：非流式 vs 流式

### 3.1 非流式（一次性返回，默认）

三个重载，从轻量到重量：

```python
from llm.core import get_llm

llm = get_llm()

# 1. 只要纯文本
text = llm.generate("你好")

# 2. 要完整元数据（token / 延迟 / 模型名 / 提供商）
resp = llm.generate_with_response("你好")
print(resp.content, resp.model, resp.provider,
      resp.latency_ms, resp.total_tokens)

# 3. 要 JSON 结构化输出
schema = {"answer": "string", "confidence": "number"}
json_str = llm.generate_json("1+1=?", schema=schema)
```

### 3.2 流式（逐 chunk 打印）

```python
from llm.core import get_llm, ProviderName

llm = get_llm(ProviderName.DEEPSEEK)
for chunk in llm.generate_stream("写一首五绝"):
    print(chunk, end="", flush=True)
```

### 流式实现状态矩阵

✅ **25 家全部补齐真流式**（8 个协议族）：

| 协议族 | 底层格式 | 厂商 |
|--------|----------|------|
| OpenAI Chat Completions SSE | `data: {choices[0].delta.content}` | `openai`, `deepseek`, `qwen`, `kimi`, `baichuan`, `doubao`, `glm`, `meta`, `milm`, `minimax`, `mistral`, `pangu`, `shangtang`, `spark`, `stepfun`, `tiangong`, `together`, `xai`, `yi` |
| Anthropic SSE | `content_block_delta.delta.text` | `anthropic` |
| Ollama NDJSON | 逐行 JSON | `ollama` |
| Cohere NDJSON | `event_type=text-generation` | `cohere` |
| Google Gemini SSE | `:streamGenerateContent?alt=sse` | `google` |
| Tencent Hunyuan SSE | 大/小写 `Choices/Delta/Content` 均兼容 | `hunyuan` |
| Baidu Wenxin SSE | `data: {result, is_end}` | `wenxin` |

全部能以同一行代码调用：

```python
for chunk in get_llm(ProviderName.WENXIN).generate_stream("你好"):
    print(chunk, end="", flush=True)
```

### 补全其他厂商流式的模板

新增厂商时，只需在其 client 里补一个生成器函数（以 OpenAI 兼容 SSE 为例）：

```python
# llm/requests/providers/xxx.py
def generate_stream(self, prompt: str, **kwargs: Any):
    payload = {..., "stream": True}
    with requests.post(url, headers=headers, json=payload,
                       timeout=self.timeout, stream=True) as resp:
        resp.raise_for_status()
        for raw in resp.iter_lines(decode_unicode=True):
            if not raw or not raw.startswith("data:"):
                continue
            data = raw[5:].strip()
            if data == "[DONE]":
                break
            piece = json.loads(data)["choices"][0]["delta"].get("content") or ""
            if piece:
                yield piece
```

调用方代码一字不改，加完自动生效。

---

## ⚡ 4. 同步 vs 异步

### 4.1 同步入口（默认）

```python
from llm.core import get_llm

llm = get_llm()                                  # 默认同步
print(llm.generate("你好"))
```

底层：`llm/requests/providers/*.py`，走 `requests` 同步 HTTP。

### 4.2 异步入口

```python
import asyncio
from llm.core import get_async_llm

async def main():
    llm = get_async_llm()                        # 零参数，同样走环境变量
    text = await llm.generate("你好")
    print(text)

    # 或者拿完整响应
    resp = await llm.generate_with_response("你好")
    print(resp.content, resp.latency_ms)

asyncio.run(main())
```

指定厂商：

```python
llm = await create_async_llm("deepseek", model="deepseek-chat")
```

市异步流式：

```python
async for chunk in llm.generate_stream("写一首诗"):
    print(chunk, end="", flush=True)
```

底层：`llm/aiohttp/providers/*.py`，走 `aiohttp` 异步 HTTP。

> ⚠️ 现状：`factory.py` 在导入 `llm.aiohttp.providers` 失败时会静默跳过。现在 25 家异步都已注册且实现了异步流式（`generate_stream`是真正的 `async generator`）。若 `list_async_providers()` 为空，检查 `pip install aiohttp pydantic pyyaml requests`。

---

## 📜 调用日志（一行开关）

```python
from llm.core import get_llm, enable_logging

enable_logging()                                  # 控制台 INFO
# enable_logging(log_file="logs/llm.log")          # 同时写滚动文件
# enable_logging(level="DEBUG", log_response=False)

get_llm().generate("你好")
# 2026-05-24 11:39:24 [INFO] llm | [request_start]  rid=bfbc69... provider=deepseek model=deepseek-chat backend=requests method=generate prompt='你好' params={'api_key': 'sk-V***6789'}
# 2026-05-24 11:39:24 [INFO] llm | [request_success] rid=bfbc69... provider=deepseek model=deepseek-chat backend=requests method=generate latency=812.4ms response='你好！有什么我可以帮你的吗？'
```

**默认记录的字段**：

1. **渠道**（provider）、**调用模型**（model）、**底层实现**（backend）、**方法**（generate / generate_json / generate_stream）
2. **入参**：prompt + 全部 kwargs（api_key/secret/token 等敏感字段自动脱敏为 `sk-V***6789`）
3. **出参**：response 内容（包括流式全部 chunk 拼接），可配置截断长度
4. **耗时**：latency_ms；**错误**：error 类型 + 堆栈；**请求追踪**：request_id 串联同一次调用的 start↔success/failure

**拿累计指标**：

```python
from llm.core import get_metrics_handler
stats = get_metrics_handler().get_metrics()
# {'total_requests': 4, 'success_count': 3, 'failure_count': 1,
#  'avg_latency_ms': 612.3, 'success_rate': 0.75,
#  'providers': {'deepseek': {'count': 3, 'success': 3, ...}}}
```

**进阶用法**：

```python
from llm.core import EventType, LLMEvent, subscribe

def on_event(ev: LLMEvent):
    if ev.event_type == EventType.REQUEST_FAILURE:
        # 接入你自己的告警系统
        ...
subscribe(None, on_event)   # 订阅所有事件
```

架构说明：`BaseLLMAdapter` / `BaseAsyncLLMAdapter` 通过 `__init_subclass__` 自动插桩，所有现有和之后新增的适配器均默认启用，不需要修改 provider 客户端代码。可运行：`python -m llm.demo.demo_logging`。

---

## 🔌 顶层入口 API 速查

| 分类 | 导入 | 说明 |
|------|------|------|
| 零参数同步 | `from llm.core import get_llm` | 带缓存，业务首选 |
| 零参数异步 | `from llm.core import get_async_llm` | 同上，异步 |
| 指定厂商同步 | `from llm.core import create_llm` | 不缓存，可传完整参数 |
| 指定厂商异步 | `from llm.core import create_async_llm` | 同上 |
| 查当前厂商 | `from llm.core import current_provider` | 调试用 |
| 查所有厂商 | `from llm.core import list_providers, list_async_providers` | 调试用 |
| 从 YAML 创建 | `from llm.core import create_llm_from_config` | 多环境 / 难使用者 |
| 弹性装饰 | `from llm.core import resilient, ResilienceConfig` | 重试/熔断/限流 |
| 事件总线 | `from llm.core import EventBus, LoggingHandler, MetricsHandler` | 可观测 |
| **一键开启调用日志** | `from llm.core import enable_logging, disable_logging, get_metrics_handler` | 控制台+文件+脱敏+指标 |
| 面向开发者类型 | `from llm.core import LLMResponse, LLMProvider, AsyncLLMProvider` | 类型提示 |

---

## 🧮 运行现成 demo

| 文件 | 用途 |
|------|------|
| `llm/demo/demo_zero_config.py` | 零参数调用 + `--enum` 枚举演示 |
| `llm/demo/demo_stream.py` | 同步/异步流式 + `--list` 看注册 |
| `llm/demo/demo_basic.py` | 最小同步 demo |
| `llm/demo/demo_config.py` | YAML 配置驱动（同/异步） |
| `llm/demo/demo_compare.py` | 多厂商横向对比 |
| `llm/demo/demo_json.py` | `generate_json` + JSON Schema |
| `llm/demo/demo_register.py` | 外部注册自定义厂商 |
| `llm/demo/demo_resilience.py` | 重试 + 熔断 + 指标（基础弹性） |
| `llm/demo/demo_resilience_full.py` | 限流/降级/异步重试/异步组合 |
| `llm/demo/demo_logging.py` | 一键开启调用日志（控制台/文件/指标/自定义订阅） |
| `llm/demo/example.py` | 纯文档演示脚本 |

```powershell
cd C:\Users\robotAi\Documents\ClawWorksapce\knowledge-base\raw\skill-tree\17_20天Agent开发速成

# 看默认厂商 + 注册清单
py -3 -m llm.demo.demo_zero_config --list

# 零参数调用（先设环境变量）
$env:LLM_PROVIDER = "deepseek"
$env:DEEPSEEK_API_KEY = "***"
py -3 -m llm.demo.demo_zero_config "解释一下 ReAct 模式"
```

---

## 🏗️ 架构一眼看

```
调用方
   │
   ├── get_llm() / get_async_llm()        ← 顶层需要记住的入口（0 参数）
   │        ↓
   │    default.py 解析厂商
   │        ↓
   ├── create_llm(name) / create_async_llm(name)
   │        ↓
   │    factory.py 查注册表
   │        ↓
   ├── adapter/ 适配器                     ← 统一接口 (generate / stream / json)
   │        ↓
   └── requests/providers/xxx.py            ← 底层 client（apikey 自动从 env 取）
        aiohttp/providers/xxx.py             ← 异步 client
```

---

## 📝 变更记录

- 2026-05-24 上午：新增「一键开关调用日志」能力（`llm.core.enable_logging`），默认记录**调用渠道 / 模型 / 底层实现 / 入参(prompt+kwargs) / 出参 / 耗时 / 请求追踪ID**，敏感字段自动脱敏；同时可以拿到 MetricsHandler 看累计指标。适配器不需要改一行代码：BaseAdapter 通过 `__init_subclass__` 自动插桩。Demo: `python -m llm.demo.demo_logging`。
- 2026-05-23 晚：demo/ 补齐 `demo_json.py` / `demo_register.py` / `demo_resilience_full.py`，并使 `demo_zero_config.py` 支持 `--enum`、`demo_config.py` 支持 `--async`；**顶层 32 个入口全部被 demo 覆盖**。
- 2026-05-23 中午（二）：所有可运行示例从 `llm/core/` 迁出到独立的 `llm/demo/` 目录，调用命令改为 `python -m llm.demo.<name>`。
- 2026-05-23 晚上：**异步 25 家全部补齐 `generate_stream`**（aiohttp + `async for response.content`）；补上异步 `create_client` 工厂 + factory 注册名单扩到 25 家。
- 2026-05-23 中午：同步剩余 20 家厂商补齐 `generate_stream`，**全 25 家同步真流式**（8 个协议族）。
- 2026-05-23 下午：`ProviderName` 枚举（从注册表动态生成）；`openai/deepseek/qwen/ollama/anthropic` 5 家首批补齐真流式；新增 `demo_stream.py`。
- 2026-05-23 上午：新增 `get_llm` / `get_async_llm` 零参数入口；补齐顶层 README。
- 2026-05-22：`llm/core/` 统一接口层上线，收拢 26 家厂商 client。
