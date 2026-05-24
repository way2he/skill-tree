# LLM 统一接口层（core）

`llm/core/` 是顶层统一接入层的**实现细节**。如果你是调用方，建议先看 [`llm/README.md`](../README.md)。

---

## 1. 顶层调用入口（4 个就够）

| 场景 | 入口 |
|------|------|
| 同步、零参数 | `get_llm()` |
| 同步、指定厂商（**枚举**） | `get_llm(ProviderName.DEEPSEEK)` |
| 同步、可传参数 | `create_llm("openai", model=..., base_url=...)` |
| 异步、零参数 | `get_async_llm()` |
| 异步、指定厂商 | `get_async_llm(ProviderName.QWEN)` |
| 异步、可传参数 | `create_async_llm("openai", ...)` |

```python
from llm.core import get_llm, ProviderName

llm = get_llm()                                # 零参数
llm = get_llm(ProviderName.DEEPSEEK)           # 枚举（推荐）
llm = get_llm("deepseek")                      # 字符串（兼容）

print(llm.generate("你好"))
print(llm.generate_with_response("你好").latency_ms)

for chunk in llm.generate_stream("写一句诗"):    # 真流式（5 家已实现）
    print(chunk, end="", flush=True)
```

---

## 2. 厂商解析优先级（在 `default.py`）

```
1. get_llm(ProviderName.XXX) / get_llm("xxx")    显式入参
2. 环境变量 LLM_PROVIDER
3. llm_config.yaml 里 default_provider
4. 兜底 "ollama"
```

apikey 由各 `XxxClient.__init__` 自动 `os.getenv` 取，调用方完全不感知。

---

## 3. `ProviderName` 枚举：动态生成、永不写死

`llm/core/providers.py` 在导入时扫描 `factory` 注册表，**动态构造枚举**：

```python
from llm.core import ProviderName, list_providers

list_providers()       # ['anthropic','baichuan',...,'yi']  运行期实际值
list(ProviderName)     # 同步生成的枚举成员
ProviderName.DEEPSEEK  # <ProviderName.DEEPSEEK: 'deepseek'>
ProviderName("typo")   # ❌ 立即 ValueError —— 拼写错误第一时间被拦
```

新加厂商只需在 `factory._register_builtin_providers()` 注册一行，`ProviderName` 自动出现对应成员。

类型别名：

```python
from llm.core import ProviderLike     # = Union[str, ProviderName]

def ask(prompt: str, provider: ProviderLike | None = None) -> str:
    return get_llm(provider).generate(prompt)
```

---

## 4. 目录结构

```
llm/
├── core/                    统一接入层
│   ├── __init__.py          顶层导出
│   ├── default.py           get_llm / get_async_llm（零参数 + 枚举入参）
│   ├── providers.py         ProviderName 枚举（动态生成）
│   ├── factory.py           注册表 + create_llm / create_async_llm
│   ├── config.py            YAML/JSON 配置加载
│   ├── llm_config.yaml      示例配置
│   ├── types.py             LLMRequest / LLMResponse / Protocol
│   ├── exceptions.py        统一异常
│   ├── adapter/             厂商接口适配
│   ├── resilience/          重试 / 熔断 / 限流 / 降级
│   └── observer/            事件总线 + 日志/指标 handler
└── demo/                    可运行示例（10 个，覆盖全部顶层入口）
    ├── demo_zero_config.py     零参数 + ProviderName 枚举（`--enum`）
    ├── demo_stream.py          同步/异步流式 + 枚举 + `--list`
    ├── demo_basic.py           最小同步（create_llm + generate*）
    ├── demo_config.py          YAML 配置驱动（同/异步路径）
    ├── demo_compare.py         多厂商横向对比
    ├── demo_json.py            generate_json + JSON Schema（同/异步）
    ├── demo_register.py        register_provider / register_async_provider
    ├── demo_resilience.py      重试 + 熔断 + 指标（基础弹性）
    ├── demo_resilience_full.py 限流/降级/异步重试/异步组合（进阶弹性）
    └── example.py              纯文档演示脚本
```

---

## 5. 设计模式

| 模式 | 应用位置 |
|------|----------|
| 策略模式 | 适配器 + 弹性策略 |
| 工厂模式 | `LLMRegistry` / `factory.py` |
| 适配器模式 | `adapter/` |
| 装饰器模式 | `@resilient()` |
| 观察者模式 | `EventBus` |
| 状态机模式 | `CircuitBreaker` |
| 模板方法 | `BaseLLMAdapter.generate_with_response()`（自动计时） |
| 单例 + 缓存 | `get_llm()` 用 `lru_cache` |
| 动态枚举 | `ProviderName` 从注册表生成 |

---

## 6. 流式实现矩阵

✅ **25 家全部补齐真流式**（8 个协议族）

| 协议族 | 底层格式 | 厂商 |
|--------|----------|------|
| OpenAI Chat Completions SSE | `data: {choices[0].delta.content}` | `openai` · `deepseek` · `qwen` · `kimi` · `baichuan` · `doubao` · `glm` · `meta` · `milm` · `minimax` · `mistral` · `pangu` · `shangtang` · `spark` · `stepfun` · `tiangong` · `together` · `xai` · `yi` |
| Anthropic SSE | `content_block_delta.delta.text` | `anthropic` |
| Ollama NDJSON | 逐行 JSON | `ollama` |
| Cohere NDJSON | `event_type=text-generation` | `cohere` |
| Google Gemini SSE | `:streamGenerateContent?alt=sse` | `google` |
| Tencent Hunyuan SSE | 大/小写字段都兼容 | `hunyuan` |
| Baidu Wenxin SSE | `data: {result, is_end}` | `wenxin` |

适配器层预留 fallback：若底层 client 未实现会自动退化为一次性返回（当前无此场景，代码预留以防未来新增厂商未补全）。

**异步实现**：全部 25 家同步实现都有对应异步版本（`llm/aiohttp/providers/*.py`），走 `aiohttp` + `async for response.content` 逐行消费。调用方：

```python
from llm.core import get_async_llm, ProviderName
async for chunk in get_async_llm(ProviderName.DEEPSEEK).generate_stream("hi"):
    print(chunk, end="", flush=True)
```

**补全模板**（直接复制改 URL/字段即可）：

```python
def generate_stream(self, prompt: str, **kwargs: Any) -> Iterator[str]:
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

调用方代码完全不变，补完即自动启用真流式。

---

## 7. 弹性 / 观察者快用

```python
from llm.core import (
    get_llm, resilient, ResilienceConfig,
    EventBus, LoggingHandler, MetricsHandler,
)

bus = EventBus()
bus.subscribe(None, LoggingHandler())
metrics = MetricsHandler()
bus.subscribe(None, metrics)

cfg = ResilienceConfig(
    retry={"max_retries": 3},
    rate_limiter={"requests_per_minute": 60},
)

@resilient(cfg)
def ask(q: str) -> str:
    return get_llm().generate(q)

print(ask("Hello"))
print(metrics.get_metrics())
```

---

## 8. 配置文件（可选）

参见 `llm_config.yaml`。常用于多环境/多账号切换；只用 `get_llm()` 时不需要也能跑。
