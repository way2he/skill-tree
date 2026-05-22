# 第1章 SDK 架构与设计哲学

## 概述

本章是《OpenAI vs Anthropic LLM API 全方位对比报告》的开篇，聚焦于两家公司官方 Python SDK 的**架构设计**与背后的**设计哲学**差异。我们将从包结构、客户端模型、API 风格、HTTP 底层、类型系统等多个维度展开对比，帮助开发者在动手集成之前建立全局认知，从而根据项目需求做出更合理的技术选型。

---

## OpenAI SDK 架构

### 包结构树

```
openai/
├── __init__.py              # 顶层导出：OpenAI, AsyncOpenAI 等
├── _client.py               # 同步客户端 OpenAI 的实现
├── _async_client.py         # 异步客户端 AsyncOpenAI 的实现
├── _base_client.py          # 共享基类（HTTP 请求、认证、重试逻辑）
├── types/                   # Pydantic 响应模型 & TypedDict 请求体
│   ├── chat/
│   │   ├── chat_completion.py
│   │   └── ...
│   ├── responses/
│   │   ├── response.py
│   │   └── ...
│   ├── image/
│   ├── audio/
│   ├── fine_tuning/
│   ├── moderation/
│   ├── batch/
│   └── shared_params.py
├── resources/               # 资源式 API 命名空间
│   ├── chat/
│   │   ├── completions.py
│   │   └── ...
│   ├── responses/
│   ├── images/
│   ├── audio/
│   ├── fine_tuning/
│   ├── moderations/
│   ├── batches/
│   ├── uploads/
│   └── ...
├── _models/                 # 内部共享模型
├── _utils/                  # 工具函数（日志、类型转换等）
├── _streaming.py            # SSE 流式处理
└── py.typed                 # PEP 561 类型标记
```

### 客户端设计

OpenAI SDK 提供两个顶层入口：

- **`OpenAI()`** — 同步客户端，适用于传统请求-响应场景。
- **`AsyncOpenAI()`** — 异步客户端，适用于 `asyncio` / FastAPI 等异步框架。

两者共享 `_base_client.py` 中的核心逻辑（认证、重试、超时、HTTP 连接池），仅在 `httpx` 层面区分同步与异步传输。

```python
from openai import OpenAI, AsyncOpenAI

# 同步
client = OpenAI(api_key="sk-...")

# 异步
client = AsyncOpenAI(api_key="sk-...")
```

### 资源式 API 设计

OpenAI SDK 采用**资源式（Resource-based）** 风格，API 路径映射为嵌套的属性链：

```python
# Responses API（2025 年新推出的统一接口）
response = client.responses.create(
    model="gpt-4o",
    input="Hello, world!"
)

# Chat Completions API（经典接口）
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Images API
result = client.images.generate(
    model="dall-e-3",
    prompt="A sunset over the ocean"
)

# Audio API
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=open("audio.mp3", "rb")
)
```

这种设计的优势在于：**API 路径与代码结构一一对应**，开发者可以直接从 OpenAI REST API 文档映射到 SDK 调用。

### SDK 自动生成机制

OpenAI SDK 由 [Stainless](https://stainlessapi.com/) 从 OpenAI 的 OpenAPI 规范**自动生成**。这意味着：

- SDK 的 API 覆盖率与 OpenAPI 规范保持同步。
- 每次发布新 API 端点，SDK 可快速跟进。
- 代码风格统一，但自定义灵活性较低。

### HTTP 底层

- **核心传输层**：`httpx`（同时支持同步和异步）。
- **可选后端**：在异步模式下可切换为 `aiohttp`（通过 `http_client` 参数注入）。
- 内置**自动重试**（指数退避）、**连接池管理**、**超时控制**。

### 类型系统

| 层面 | 技术 | 说明 |
|------|------|------|
| 请求体 | `TypedDict` | 轻量级类型提示，运行时无开销 |
| 响应体 | `Pydantic v1/v2` | 提供数据验证、序列化、IDE 补全 |
| 流式事件 | `Stream` 泛型迭代器 | 逐块产出 SSE 事件对象 |

---

## Anthropic SDK 架构

### 包结构树

```
anthropic/
├── __init__.py              # 顶层导出：Anthropic, AsyncAnthropic
├── _client.py               # 同步客户端 Anthropic 的实现
├── _async_client.py         # 异步客户端 AsyncAnthropic 的实现
├── _base_client.py          # 共享基类
├── types/                   # Pydantic 响应模型 & TypedDict 请求体
│   ├── message.py
│   ├── message_stream_event.py
│   ├── raw_message_stream_event.py
│   ├── content_block.py
│   ├── tool_use_block.py
│   ├── tool_result_block_param.py
│   └── ...
├── resources/               # 扁平式 API 命名空间
│   ├── messages.py          # 核心：Messages API
│   ├── messages/
│   │   └── ...              # Messages 子资源
│   ├── count_tokens.py      # Token 计数
│   └── ...
├── _models/                 # 内部共享模型
├── _utils/                  # 工具函数
├── lib/
│   ├── streaming/
│   │   ├── _messages.py     # Messages 流式处理
│   │   └── ...
│   └── ...
└── py.typed                 # PEP 561 类型标记
```

### 客户端设计

与 OpenAI 类似，Anthropic 提供同步与异步两个入口：

```python
from anthropic import Anthropic, AsyncAnthropic

# 同步
client = Anthropic(api_key="sk-ant-...")

# 异步
client = AsyncAnthropic(api_key="sk-ant-...")
```

### 扁平式 API 设计

Anthropic SDK 采用**扁平式（Flat）** 风格，API 调用路径更短、更直观：

```python
# Messages API — 核心接口
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)

# Messages 流式
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# Token 计数
token_count = client.messages.count_tokens(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

Anthropic 的 API 设计围绕 **Messages** 这一核心概念展开，所有功能（文本生成、流式输出、工具调用、Token 计数）都从 `client.messages.*` 出发。

### SDK 自动生成机制

Anthropic SDK 同样由 **Stainless** 自动生成。值得注意的是，Anthropic 在 2024 年**收购了 Stainless**，因此两家 SDK 的生成基础设施实际上来自同一家公司，代码风格和工程规范高度一致。

### HTTP 底层

- **核心传输层**：`httpx`（同步和异步）。
- 内置**自动重试**（指数退避）、**连接池管理**、**超时控制**。
- 与 OpenAI 不同，Anthropic SDK **不提供 aiohttp 后端切换**。

### 类型系统

| 层面 | 技术 | 说明 |
|------|------|------|
| 请求体 | `TypedDict` | 与 OpenAI 一致 |
| 响应体 | `Pydantic v1/v2` | 与 OpenAI 一致 |
| 流式事件 | `MessageStream` 上下文管理器 | 提供更高级的流式抽象（text_stream、event_stream） |

---

## 核心差异对比表

| 维度 | OpenAI SDK | Anthropic SDK |
|------|-----------|---------------|
| **包名** | `openai` | `anthropic` |
| **PyPI 大小** | ~15 MB（含所有资源模块） | ~8 MB（模块更精简） |
| **核心模块数** | 20+ 资源模块 | 3-5 个核心模块 |
| **API 风格** | 资源式（`client.chat.completions.create()`） | 扁平式（`client.messages.create()`） |
| **覆盖能力** | Chat、Responses、Images、Audio、Embeddings、Fine-tuning、Moderations、Batches、Uploads、Realtime 等 | Messages（文本 + 工具调用 + 流式）、Token 计数 |
| **扩展方式** | SDK 内新增资源模块 | MCP 协议扩展（Tool Use、Computer Use 等） |
| **流式抽象** | `Stream` 迭代器 + `for chunk in stream` | `MessageStream` 上下文管理器 + `text_stream` / `event_stream` |
| **异步支持** | `AsyncOpenAI` + 可选 `aiohttp` | `AsyncAnthropic`（仅 httpx） |
| **代码生成** | Stainless 自动生成 | Stainless 自动生成（Anthropic 收购了 Stainless） |
| **社区生态** | 更大（更多教程、集成、第三方封装） | 较小但增长迅速 |
| **Beta 功能** | 通过 `default_headers` 传入 beta 标志 | 通过 `beta` 参数传入 |

---

## 设计哲学差异

### OpenAI：平台化思维

OpenAI 的 SDK 设计体现了**平台化（Platform）** 思维：

1. **一个 SDK 覆盖所有能力**：从文本生成（Chat Completions、Responses）到图像生成（DALL-E）、语音识别（Whisper）、语音合成（TTS）、向量嵌入（Embeddings）、模型微调（Fine-tuning）、内容审核（Moderations）、批量处理（Batches）、实时对话（Realtime）——所有能力都封装在同一个 `openai` 包中。

2. **资源式 API 映射 REST 路径**：SDK 的方法链直接对应 REST API 的 URL 路径，降低了从 API 文档到代码的转换成本。

3. **快速迭代，功能优先**：OpenAI 频繁推出新 API（如 2025 年的 Responses API），SDK 通过自动生成快速跟进，保持功能覆盖的完整性。

4. **SDK 即文档**：由于从 OpenAPI 规范生成，SDK 的类型签名本身就是最准确的 API 文档。

### Anthropic：聚焦思维

Anthropic 的 SDK 设计体现了**聚焦（Focus）** 思维：

1. **围绕 Messages API 核心**：SDK 的主体就是 `client.messages`，所有文本生成、工具调用、流式输出、Token 计数都围绕这一核心展开。没有图像生成、没有语音处理、没有微调接口。

2. **通过协议而非 SDK 扩展能力**：Anthropic 将复杂能力（如 Computer Use、MCP 工具集成）通过**协议层**（Tool Use、MCP）而非 SDK 内置模块来实现。这意味着 SDK 保持精简，而扩展能力由协议和生态驱动。

3. **流式体验优先**：Anthropic 的 `MessageStream` 上下文管理器提供了比 OpenAI 更高级的流式抽象，内置 `text_stream`（纯文本流）和 `event_stream`（完整事件流），开发者无需手动处理 SSE 解析。

4. **安全与可控**：Anthropic 在 SDK 层面内置了更多安全相关参数（如 `anthropic-dangerous-direct-browser-access`），体现了其对安全边界的重视。

---

## 代码示例：Hello World 对比

### OpenAI

```python
from openai import OpenAI

client = OpenAI()  # 自动读取 OPENAI_API_KEY 环境变量

response = client.responses.create(
    model="gpt-4o",
    input="你好，请用一句话介绍你自己。"
)

print(response.output_text)
```

### Anthropic

```python
from anthropic import Anthropic

client = Anthropic()  # 自动读取 ANTHROPIC_API_KEY 环境变量

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "你好，请用一句话介绍你自己。"}]
)

print(message.content[0].text)
```

### 关键差异速览

| 差异点 | OpenAI | Anthropic |
|--------|--------|-----------|
| 环境变量 | `OPENAI_API_KEY` | `ANTHROPIC_API_KEY` |
| 调用方法 | `client.responses.create(input=...)` | `client.messages.create(messages=...)` |
| 输入格式 | `input` 参数（字符串或结构化内容） | `messages` 参数（消息数组） |
| Token 限制 | 模型内部处理 | 需显式指定 `max_tokens` |
| 输出提取 | `response.output_text` | `message.content[0].text` |

---

## 要点总结

1. **底层同源，上层分化**：两家 SDK 都由 Stainless 自动生成，共享相似的工程基础（httpx 传输、TypedDict + Pydantic 类型系统、自动重试），但在 API 组织方式上走上了不同道路。

2. **OpenAI 做加法，Anthropic 做减法**：OpenAI SDK 像一个"全家桶"，一个包覆盖文本、图像、音频、微调等所有能力；Anthropic SDK 像一把"手术刀"，精简聚焦于 Messages API，其他能力通过协议扩展。

3. **API 风格反映产品策略**：OpenAI 的资源式 API 适合平台化扩展（新增资源模块即可）；Anthropic 的扁平式 API 降低了学习成本，适合快速上手。

4. **流式体验 Anthropic 更友好**：`MessageStream` 上下文管理器提供了 `text_stream` 等高级抽象，减少了样板代码；OpenAI 的流式 API 更底层，灵活性更高但需要更多手动处理。

5. **选型建议**：如果项目需要多模态能力（文本 + 图像 + 音音），OpenAI SDK 是更自然的选择；如果项目以文本对话为核心且重视 SDK 精简性，Anthropic SDK 更合适；如果需要同时支持两家，建议封装统一抽象层。
