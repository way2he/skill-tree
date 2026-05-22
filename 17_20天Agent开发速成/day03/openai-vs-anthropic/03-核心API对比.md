# 03 - 核心 API 对比

## 概述

OpenAI 和 Anthropic 分别提供了两套风格迥异的 API 来与大语言模型交互。理解它们的异同，是构建 Agent 应用的基本功。

| 维度 | OpenAI | Anthropic |
|------|--------|-----------|
| **新一代 API** | Responses API（2025 年推出，推荐） | Messages API（持续迭代） |
| **经典 API** | Chat Completions API（兼容性好） | — |
| **SDK 语言** | Python / Node.js / REST | Python / Node.js / REST |
| **系统指令** | `instructions` 字段 或 `developer` 角色 | `system` 顶层字段 |
| **输出结构** | `output` 数组 或 `choices[0].message` | `content` 数组（统一） |
| **必填参数** | `model` + `input`（或 `messages`） | `model` + `max_tokens` + `messages` |

> **核心差异一句话总结**：OpenAI 倾向于"智能默认值"（如自动截断），Anthropic 倾向于"显式声明"（必须指定 `max_tokens`）。

---

## OpenAI：Responses API（新一代推荐）

Responses API 是 OpenAI 在 2025 年推出的新一代接口，旨在统一并简化此前 Chat Completions API 的诸多设计。官方推荐新项目优先使用。

### 基础调用

```python
from openai import OpenAI

client = OpenAI()  # 默认读取 OPENAI_API_KEY 环境变量

response = client.responses.create(
    model="gpt-4o",
    instructions="你是一个专业的翻译助手，只输出翻译结果。",
    input="将以下英文翻译为中文：Hello, world!",
)

print(response.output_text)
# 输出：你好，世界！
```

**关键字段说明**：
- `model`：模型名称，如 `"gpt-4o"`、`"gpt-4o-mini"`、`"o3-mini"`
- `instructions`：系统级指令，定义 AI 的角色和行为约束
- `input`：用户输入，可以是字符串或消息数组
- `response.output_text`：快捷属性，直接获取文本输出

### 多轮对话

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4o",
    instructions="你是一个 Python 编程导师。",
    input=[
        {"role": "user", "content": "什么是列表推导式？"},
        {"role": "assistant", "content": "列表推导式是 Python 中用一行代码创建列表的简洁语法..."},
        {"role": "user", "content": "能给我一个带条件的例子吗？"},
    ],
)

print(response.output_text)
```

### 请求参数详解

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `str` | 是 | 模型 ID，如 `"gpt-4o"` |
| `instructions` | `str` | 否 | 系统级指令，等价于旧版 `developer` 角色消息 |
| `input` | `str \| list` | 是 | 用户输入，字符串或消息对象数组 |
| `tools` | `list` | 否 | 工具定义列表（函数调用 / 文件搜索 / 代码执行等） |
| `response_format` | `object` | 否 | 输出格式约束，如 `{"type": "json_object"}` |
| `stream` | `bool` | 否 | 是否流式返回，默认 `False` |
| `temperature` | `float` | 否 | 采样温度，0~2，默认 `1` |
| `max_output_tokens` | `int` | 否 | 最大输出 token 数 |
| `top_p` | `float` | 否 | 核采样概率，默认 `1` |
| `previous_response_id` | `str` | 否 | 关联上一轮对话，实现有状态多轮 |
| `reasoning` | `object` | 否 | 推理模型（如 o3）的推理配置 |

### 响应对象结构

```python
# response 对象的核心字段
response.id              # "resp_abc123"
response.model           # "gpt-4o"
response.status          # "completed"
response.output          # [{"type": "message", "role": "assistant", "content": [...]}]
response.output_text     # "你好，世界！"（快捷属性，拼接所有文本内容）
response.usage           # Usage(input_tokens=15, output_tokens=8, total_tokens=23)
```

---

## OpenAI：Chat Completions API（经典接口）

Chat Completions API 是 OpenAI 最经典的接口，生态兼容性最好，大量第三方库和教程仍基于此 API。

### 基础调用

```python
from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "你是一个专业的翻译助手。"},
        {"role": "user", "content": "将以下英文翻译为中文：Hello, world!"},
    ],
)

print(completion.choices[0].message.content)
# 输出：你好，世界！
```

### 角色体系

Chat Completions API 使用 `role` 字段区分消息来源：

| 角色 | 说明 | 使用场景 |
|------|------|----------|
| `system` | 系统指令（旧版） | 定义 AI 行为约束 |
| `developer` | 开发者指令（新版推荐） | 替代 `system`，优先级更高 |
| `user` | 用户消息 | 用户的实际输入 |
| `assistant` | AI 回复 | 模型的输出（多轮对话时回传） |
| `tool` | 工具返回 | 函数调用的结果 |

```python
messages = [
    {"role": "developer", "content": "你是一个严谨的数据分析师。"},
    {"role": "user", "content": "分析这组数据的趋势：[1, 3, 5, 7, 9]"},
    {"role": "assistant", "content": "这组数据呈现明显的线性增长趋势..."},
    {"role": "user", "content": "预测下一个值是多少？"},
]
```

### 响应对象结构

```python
completion.id               # "chatcmpl-abc123"
completion.model            # "gpt-4o"
completion.object           # "chat.completion"
completion.choices          # 列表，通常只有一个元素
completion.choices[0].message.role       # "assistant"
completion.choices[0].message.content    # "你好，世界！"
completion.choices[0].finish_reason      # "stop"
completion.usage            # Usage(prompt_tokens=15, completion_tokens=8, total_tokens=23)
```

---

## Anthropic：Messages API

Messages API 是 Anthropic 唯一的消息接口，设计简洁一致，所有输出（文本、工具调用、工具结果）统一在 `content` 数组中。

### 基础调用

```python
import anthropic

client = anthropic.Anthropic()  # 默认读取 ANTHROPIC_API_KEY 环境变量

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "将以下英文翻译为中文：Hello, world!"},
    ],
)

print(message.content[0].text)
# 输出：你好，世界！
```

### system 作为顶层参数

与 OpenAI 将系统指令放在 `messages` 数组中不同，Anthropic 将 `system` 作为独立的顶层参数：

```python
# Anthropic 的写法 —— system 是独立字段
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="你是一个专业的翻译助手，只输出翻译结果。",
    messages=[
        {"role": "user", "content": "Hello, world!"},
    ],
)

# OpenAI 的写法 —— system 是 messages 中的第一条
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "你是一个专业的翻译助手，只输出翻译结果。"},
        {"role": "user", "content": "Hello, world!"},
    ],
)
```

**设计意图**：将系统指令从对话历史中分离，使其语义更清晰，也便于 API 层面做不同的处理（如更长的 system 上下文窗口）。

### 请求参数详解

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `str` | 是 | 模型 ID，如 `"claude-sonnet-4-20250514"` |
| `max_tokens` | `int` | **是** | 最大输出 token 数（Anthropic 唯一必填的数值参数） |
| `messages` | `list` | 是 | 消息数组，角色为 `user` / `assistant` |
| `system` | `str` | 否 | 系统指令（顶层参数，不在 messages 中） |
| `tools` | `list` | 否 | 工具定义列表 |
| `stream` | `bool` | 否 | 是否流式返回，默认 `False` |
| `temperature` | `float` | 否 | 采样温度，0~1，默认 `1` |
| `top_p` | `float` | 否 | 核采样概率，默认不启用 |
| `top_k` | `int` | 否 | Top-K 采样（Anthropic 独有参数） |
| `stop_sequences` | `list[str]` | 否 | 自定义停止序列 |

### 响应对象结构

```python
message.id               # "msg_abc123"
message.type             # "message"
message.role             # "assistant"
message.model            # "claude-sonnet-4-20250514"
message.content          # [{"type": "text", "text": "你好，世界！"}]
message.stop_reason      # "end_turn"
message.usage            # Usage(input_tokens=15, output_tokens=8)
```

### content 是一个列表

Anthropic 的 `content` 始终是一个数组，每个元素根据 `type` 字段区分不同类型：

```python
# 纯文本输出
message.content = [
    {"type": "text", "text": "你好，世界！"}
]

# 包含工具调用
message.content = [
    {"type": "text", "text": "让我帮你查一下天气。"},
    {
        "type": "tool_use",
        "id": "toolu_abc123",
        "name": "get_weather",
        "input": {"city": "北京"}
    }
]

# 工具结果（作为 user 消息的一部分传回）
messages.append({
    "role": "user",
    "content": [
        {
            "type": "tool_result",
            "tool_use_id": "toolu_abc123",
            "content": "北京今天晴，25°C"
        }
    ]
})
```

| content type | 说明 | 出现位置 |
|-------------|------|----------|
| `text` | 文本内容 | 模型输出 |
| `tool_use` | 工具调用请求 | 模型输出 |
| `tool_result` | 工具调用结果 | 用户回传 |
| `image` | 图片（Base64 或 URL） | 用户输入 |

---

## 关键差异对比表

| 对比维度 | OpenAI（Responses API） | OpenAI（Chat Completions） | Anthropic（Messages） |
|---------|----------------------|--------------------------|---------------------|
| **API 入口** | `client.responses.create()` | `client.chat.completions.create()` | `client.messages.create()` |
| **系统指令** | `instructions` 参数 | `messages` 中 `developer`/`system` 角色 | `system` 顶层参数 |
| **输入参数名** | `input` | `messages` | `messages` |
| **输出获取** | `response.output_text` | `completion.choices[0].message.content` | `message.content[0].text` |
| **必填参数** | `model` + `input` | `model` + `messages` | `model` + `max_tokens` + `messages` |
| **max_tokens** | 可选（有默认值） | 可选（有默认值） | **必填**（无默认值） |
| **停止原因** | `status` 字段 | `finish_reason` 字段 | `stop_reason` 字段 |
| **停止枚举值** | `"completed"` / `"incomplete"` / `"failed"` | `"stop"` / `"length"` / `"tool_calls"` / `"content_filter"` | `"end_turn"` / `"max_tokens"` / `"stop_sequence"` / `"tool_use"` |
| **角色体系** | `user` / `assistant` | `developer` / `user` / `assistant` / `tool` | `user` / `assistant` |
| **输出结构** | `output` 数组 | `choices[0].message` | `content` 数组 |
| **温度范围** | 0 ~ 2 | 0 ~ 2 | 0 ~ 1 |
| **独有参数** | `previous_response_id` | `logprobs` / `frequency_penalty` | `top_k` / `stop_sequences` |

---

## 结构化输出对比

### OpenAI：原生支持

OpenAI 提供了多种结构化输出方式：

**方式一：JSON Mode**

```python
response = client.responses.create(
    model="gpt-4o",
    instructions="你是一个信息提取助手。",
    input="提取以下文本中的姓名和年龄：张三今年25岁。",
    response_format={"type": "json_object"},
)

import json
data = json.loads(response.output_text)
# {"name": "张三", "age": 25}
```

**方式二：Pydantic 模型解析（推荐）**

```python
from pydantic import BaseModel

class PersonInfo(BaseModel):
    name: str
    age: int

response = client.responses.parse(
    model="gpt-4o",
    instructions="你是一个信息提取助手。",
    input="提取以下文本中的姓名和年龄：张三今年25岁。",
    text_format=PersonInfo,
)

person = response.output_parsed
print(person.name)  # "张三"
print(person.age)   # 25
```

### Anthropic：Prompt 约束 + 工具调用

Anthropic 不提供原生的 JSON Mode，但可以通过以下方式实现类似效果：

**方式一：在 Prompt 中要求 JSON 输出**

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="你是一个信息提取助手。请始终以 JSON 格式输出。",
    messages=[
        {"role": "user", "content": "提取以下文本中的姓名和年龄：张三今年25岁。"},
    ],
)

import json
data = json.loads(message.content[0].text)
```

> 注意：这种方式不保证输出一定是合法 JSON，需要自己做异常处理。

**方式二：通过 tool_use 约束输出结构（推荐）**

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[
        {
            "name": "extract_person_info",
            "description": "提取人物信息",
            "input_schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "姓名"},
                    "age": {"type": "integer", "description": "年龄"},
                },
                "required": ["name", "age"],
            },
        }
    ],
    messages=[
        {"role": "user", "content": "提取以下文本中的姓名和年龄：张三今年25岁。"},
    ],
)

# 从 tool_use 类型的 content 中提取结构化数据
for block in message.content:
    if block.type == "tool_use":
        print(block.name)   # "extract_person_info"
        print(block.input)  # {"name": "张三", "age": 25}
```

**结构化输出对比总结**：

| 对比维度 | OpenAI | Anthropic |
|---------|--------|-----------|
| 原生 JSON Mode | 支持（`response_format`） | 不支持 |
| Schema 约束 | `response_format` + JSON Schema / Pydantic | 通过 `tool_use` 的 `input_schema` 间接实现 |
| 输出保证 | 强保证（JSON Mode 下一定返回合法 JSON） | 弱保证（Prompt 方式需自行验证，tool_use 方式可靠） |
| 推荐方式 | `client.responses.parse()` + Pydantic | `tool_use` + `input_schema` |

---

## 代码对照：同一功能的两种写法

下面以"发送一条消息并获取回复"为例，展示两家 SDK 的完整代码。

### OpenAI（Responses API）

```python
"""
OpenAI Responses API —— 发送消息并获取回复
"""
from openai import OpenAI


def chat_with_openai(user_message: str, system_prompt: str = "你是一个有帮助的助手。") -> str:
    """
    使用 OpenAI Responses API 发送消息并获取回复。

    Args:
        user_message: 用户输入的消息文本。
        system_prompt: 系统级指令，定义 AI 角色。

    Returns:
        模型生成的回复文本。
    """
    client = OpenAI()

    response = client.responses.create(
        model="gpt-4o",
        instructions=system_prompt,
        input=user_message,
    )

    return response.output_text


if __name__ == "__main__":
    result = chat_with_openai("用一句话介绍 Python。")
    print(result)
```

### Anthropic（Messages API）

```python
"""
Anthropic Messages API —— 发送消息并获取回复
"""
import anthropic


def chat_with_anthropic(user_message: str, system_prompt: str = "你是一个有帮助的助手。") -> str:
    """
    使用 Anthropic Messages API 发送消息并获取回复。

    Args:
        user_message: 用户输入的消息文本。
        system_prompt: 系统级指令，定义 AI 角色。

    Returns:
        模型生成的回复文本。
    """
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message},
        ],
    )

    return message.content[0].text


if __name__ == "__main__":
    result = chat_with_anthropic("用一句话介绍 Python。")
    print(result)
```

### 并排对比

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        OpenAI vs Anthropic 代码对照                         │
├──────────────────────────────────┬──────────────────────────────────────────┤
│  OpenAI (Responses API)          │  Anthropic (Messages API)               │
├──────────────────────────────────┼──────────────────────────────────────────┤
│  from openai import OpenAI       │  import anthropic                       │
│                                  │                                          │
│  client = OpenAI()               │  client = anthropic.Anthropic()         │
│                                  │                                          │
│  response = client.responses     │  message = client.messages.create(      │
│    .create(                      │    model="claude-sonnet-4-20250514",    │
│      model="gpt-4o",             │    max_tokens=1024,          ◄── 必填!  │
│      instructions="...",         │    system="...",                        │
│      input="...",                │    messages=[                          │
│  )                               │      {"role": "user",                  │
│                                  │       "content": "..."},               │
│  return response.output_text     │    ],                                   │
│                                  │  )                                      │
│                                  │                                          │
│                                  │  return message.content[0].text         │
├──────────────────────────────────┼──────────────────────────────────────────┤
│  输出: response.output_text      │  输出: message.content[0].text          │
│  (直接字符串)                     │  (需从 content 数组取)                   │
├──────────────────────────────────┼──────────────────────────────────────────┤
│  系统指令: instructions 参数      │  系统指令: system 顶层参数               │
├──────────────────────────────────┼──────────────────────────────────────────┤
│  max_tokens: 可选                │  max_tokens: 必填                       │
└──────────────────────────────────┴──────────────────────────────────────────┘
```

---

## 要点总结

1. **API 设计哲学不同**：OpenAI 追求"开箱即用"（智能默认值、自动截断），Anthropic 追求"显式可控"（必须声明 `max_tokens`、系统指令独立于消息）。

2. **系统指令的处理方式**：OpenAI Responses API 使用 `instructions` 参数，Chat Completions 使用 `developer`/`system` 角色消息；Anthropic 使用 `system` 顶层参数，语义更清晰。

3. **输出结构差异**：OpenAI Responses API 提供 `output_text` 快捷属性；Anthropic 的 `content` 始终是数组，需要按 `type` 字段遍历处理。

4. **max_tokens 是 Anthropic 的必填项**：这是迁移时最容易遗漏的参数。OpenAI 有合理的默认值，Anthropic 则要求开发者明确指定。

5. **结构化输出**：OpenAI 原生支持 JSON Mode 和 Pydantic 解析，保证输出合法；Anthropic 推荐通过 `tool_use` 的 `input_schema` 间接实现，同样可靠。

6. **角色体系**：OpenAI 有 `developer` / `user` / `assistant` / `tool` 四种角色；Anthropic 只有 `user` / `assistant` 两种，工具结果作为 `user` 消息中的 `tool_result` 类型传入。

7. **迁移建议**：如果需要同时支持两家 API，建议封装一个统一的抽象层，内部处理参数映射（如 `max_tokens` 自动填充、系统指令字段转换、输出结构统一）。
