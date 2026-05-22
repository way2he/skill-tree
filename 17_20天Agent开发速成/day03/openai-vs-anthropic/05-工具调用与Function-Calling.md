# 05 - 工具调用与 Function Calling

## 概述

工具调用（Tool Use / Function Calling）是 Agent 开发的核心能力。它允许大语言模型在对话过程中"调用"外部函数，从而获取实时数据、执行操作或与外部系统交互。

OpenAI 和 Anthropic 都支持工具调用，但在**定义方式、执行流程、结果回传格式**等方面存在显著差异。理解这些差异是构建跨平台 Agent 的关键。

| 维度 | OpenAI | Anthropic |
|------|--------|-----------|
| 术语 | Function Calling / Tool Use | Tool Use |
| 首次引入 | 2023 年 6 月（Chat Completions） | 2024 年 3 月 |
| 核心价值 | 让模型结构化地输出函数调用意图 | 让模型在对话中无缝使用外部工具 |

---

## OpenAI 工具调用

OpenAI 提供了两套 API 来支持工具调用：**Responses API**（新版）和 **Chat Completions API**（经典版）。两者的工具定义格式和响应解析方式有所不同。

### Responses API 中的工具定义

Responses API 是 OpenAI 于 2025 年推出的新一代 API，工具定义更加扁平化。

#### 工具定义格式

```json
{
  "type": "function",
  "name": "get_weather",
  "description": "获取指定城市的当前天气信息",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "城市名称，例如：北京、上海"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"],
        "description": "温度单位"
      }
    },
    "required": ["city"]
  }
}
```

注意：Responses API 中，`name` 和 `description` 直接位于工具对象的顶层，无需额外的 `function` 嵌套。

#### 代码示例：定义并调用 get_weather 工具

```python
from openai import OpenAI

client = OpenAI()

# 定义工具
tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "获取指定城市的当前天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，例如：北京、上海"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "温度单位"
                }
            },
            "required": ["city"]
        }
    }
]

# 发起请求
response = client.responses.create(
    model="gpt-4o",
    input="今天北京天气怎么样？",
    tools=tools
)

# 解析工具调用
for item in response.output:
    if item.type == "function_call":
        print(f"调用函数: {item.name}")
        print(f"参数: {item.arguments}")
        # 输出示例:
        # 调用函数: get_weather
        # 参数: {"city": "北京"}
```

#### 将工具结果传回

在 Responses API 中，工具结果通过在 `input` 列表中添加 `role="tool"` 的消息来传回：

```python
from openai import OpenAI

client = OpenAI()

# 第一次调用：获取工具调用请求
response = client.responses.create(
    model="gpt-4o",
    input="今天北京天气怎么样？",
    tools=tools
)

# 提取工具调用
function_call = None
for item in response.output:
    if item.type == "function_call":
        function_call = item
        break

if function_call:
    # 模拟执行工具
    weather_result = {"city": "北京", "temperature": 25, "condition": "晴"}

    # 将结果传回，继续对话
    final_response = client.responses.create(
        model="gpt-4o",
        input=[
            {"role": "user", "content": "今天北京天气怎么样？"},
            response,  # 包含工具调用的完整响应
            {
                "role": "tool",
                "tool_call_id": function_call.call_id,
                "content": str(weather_result)
            }
        ],
        tools=tools
    )
    print(final_response.output_text)
```

### Chat Completions API 中的工具定义

Chat Completions API 是 OpenAI 的经典接口，工具定义多了一层 `function` 嵌套。

#### 工具定义格式

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "获取指定城市的当前天气信息",
    "parameters": {
      "type": "object",
      "properties": {
        "city": {
          "type": "string",
          "description": "城市名称"
        }
      },
      "required": ["city"]
    }
  }
}
```

**关键区别**：Chat Completions API 中，`name`、`description`、`parameters` 都嵌套在 `function` 字段内部。

#### 完整的工具调用循环代码示例

```python
from openai import OpenAI
import json

client = OpenAI()

# 定义工具（注意 function 嵌套）
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的当前天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，例如：北京、上海"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# 模拟的工具执行函数
def get_weather(city: str, unit: str = "celsius") -> dict:
    """模拟天气查询"""
    return {"city": city, "temperature": 25, "unit": unit, "condition": "晴"}

# 工具映射表
tool_map = {
    "get_weather": get_weather
}

# 第一步：发送用户消息
messages = [{"role": "user", "content": "北京和上海今天天气怎么样？"}]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools
)

assistant_message = response.choices[0].message
messages.append(assistant_message)

# 第二步：检查并执行工具调用
if assistant_message.tool_calls:
    for tool_call in assistant_message.tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        # 执行工具
        result = tool_map[function_name](**function_args)

        # 将工具结果添加到消息列表
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result, ensure_ascii=False)
        })

    # 第三步：将工具结果传回，获取最终回复
    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools
    )
    print(final_response.choices[0].message.content)
```

**要点说明**：
- 响应中通过 `message.tool_calls` 列表获取工具调用信息
- 每个工具调用包含 `id`、`function.name`、`function.arguments`
- 工具结果通过 `role="tool"` 的消息回传，必须携带 `tool_call_id`

---

## Anthropic 工具调用

Anthropic 的工具调用设计更加简洁直接，与 OpenAI 在格式上有明显差异。

### 工具定义

#### 工具定义格式

```json
{
  "name": "get_weather",
  "description": "获取指定城市的当前天气信息",
  "input_schema": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "城市名称，例如：北京、上海"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"],
        "description": "温度单位"
      }
    },
    "required": ["city"]
  }
}
```

**关键区别**：
- 没有 `type` 字段（默认就是工具）
- 没有 `function` 嵌套层
- 使用 `input_schema` 而非 `parameters` 来定义参数的 JSON Schema

#### 代码示例：定义 get_weather 工具

```python
import anthropic

client = anthropic.Anthropic()

# 定义工具（注意 input_schema）
tools = [
    {
        "name": "get_weather",
        "description": "获取指定城市的当前天气信息",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，例如：北京、上海"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "温度单位"
                }
            },
            "required": ["city"]
        }
    }
]
```

### 执行流程

Anthropic 的工具调用结果回传方式与 OpenAI 有本质区别：它使用 `content` 列表中的 `tool_result` 类型元素，而非独立的 `role="tool"` 消息。

#### 完整的工具调用循环代码示例

```python
import anthropic
import json

client = anthropic.Anthropic()

# 定义工具
tools = [
    {
        "name": "get_weather",
        "description": "获取指定城市的当前天气信息",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，例如：北京、上海"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "温度单位"
                }
            },
            "required": ["city"]
        }
    }
]

# 模拟的工具执行函数
def get_weather(city: str, unit: str = "celsius") -> dict:
    """模拟天气查询"""
    return {"city": city, "temperature": 25, "unit": unit, "condition": "晴"}

# 工具映射表
tool_map = {
    "get_weather": get_weather
}

# 第一步：发送用户消息
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": "北京和上海今天天气怎么样？"}
    ]
)

# 第二步：检查并执行工具调用
# Anthropic 的响应 content 是一个列表，可能包含 text 和 tool_use 类型的元素
has_tool_use = any(block.type == "tool_use" for block in response.content)

if has_tool_use:
    # 构建工具结果列表
    tool_results = []

    for block in response.content:
        if block.type == "tool_use":
            function_name = block.name
            function_args = block.input  # 注意：直接是 dict，无需 json.loads

            # 执行工具
            result = tool_map[function_name](**function_args)

            # 构建 tool_result 内容块
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,  # 必须携带 tool_use_id 进行关联
                "content": json.dumps(result, ensure_ascii=False)
            })

    # 第三步：将 assistant 消息和工具结果一起传回
    final_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        tools=tools,
        messages=[
            {"role": "user", "content": "北京和上海今天天气怎么样？"},
            {"role": "assistant", "content": response.content},  # 包含 tool_use 块
            {"role": "user", "content": tool_results}            # tool_result 列表
        ]
    )
    print(final_response.content[0].text)
```

**要点说明**：
- 响应中 `content` 是一个列表，包含不同类型的 `block`（`text`、`tool_use` 等）
- 工具调用参数通过 `block.input` 直接获取（已经是 dict 类型，无需 JSON 解析）
- 工具结果通过 `role="user"` 消息中的 `type="tool_result"` 元素回传
- 必须携带 `tool_use_id` 来关联对应的工具调用

---

## 关键差异对比表

| 对比维度 | OpenAI (Chat Completions) | OpenAI (Responses API) | Anthropic |
|---------|--------------------------|----------------------|-----------|
| **参数 Schema 字段名** | `parameters` | `parameters` | `input_schema` |
| **嵌套层级** | 多一层 `function` 嵌套 | 扁平化（无 `function` 嵌套） | 扁平化（无额外嵌套） |
| **工具调用标识** | `type: "function"` | `type: "function_call"` | `type: "tool_use"` |
| **结果回传方式** | `role: "tool"` 的独立消息 | `role: "tool"` 的消息 | `role: "user"` 消息中嵌入 `type: "tool_result"` |
| **ID 关联方式** | `tool_call_id` | `call_id` | `tool_use_id` |
| **参数解析** | 需 `json.loads(arguments)` | 需 `json.loads(arguments)` | 直接 `block.input`（已是 dict） |
| **并行工具调用** | 支持（`tool_calls` 数组） | 支持（`output` 中多个 `function_call`） | 支持（`content` 中多个 `tool_use`） |
| **工具选择控制** | `tool_choice` | `tool_choice` | `tool_choice` |

### 格式差异速记

```
OpenAI Chat Completions:
  定义: tools[].function.parameters
  调用: message.tool_calls[].function.name / .arguments (JSON string)
  回传: {"role": "tool", "tool_call_id": "...", "content": "..."}

OpenAI Responses API:
  定义: tools[].parameters
  调用: output[].name / .arguments (JSON string)
  回传: {"role": "tool", "tool_call_id": "...", "content": "..."}

Anthropic:
  定义: tools[].input_schema
  调用: content[].name / .input (dict)
  回传: {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "...", "content": "..."}]}
```

---

## 工具选择控制

工具选择控制（`tool_choice`）允许开发者决定模型在何时、如何使用工具。两家 API 都支持此参数，但可选值有所不同。

### OpenAI 的 tool_choice

| 值 | 说明 |
|----|------|
| `"auto"` | 模型自行决定是否调用工具（默认值） |
| `"none"` | 模型不会调用任何工具，只生成文本 |
| `"required"` | 模型必须调用至少一个工具 |
| `{"type": "function", "function": {"name": "get_weather"}}` | 模型必须调用指定的工具 |

```python
# OpenAI: 强制调用指定工具
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice={"type": "function", "function": {"name": "get_weather"}}
)

# OpenAI: 禁止调用任何工具
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice="none"
)

# OpenAI: 要求必须调用某个工具
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice="required"
)
```

### Anthropic 的 tool_choice

| 值 | 说明 |
|----|------|
| `"auto"` | 模型自行决定是否调用工具（默认值） |
| `"any"` | 模型必须调用至少一个工具（类似 OpenAI 的 `required`） |
| `{"type": "tool", "name": "get_weather"}` | 模型必须调用指定的工具 |
| `{"type": "auto"}` | 等同于 `"auto"`，但可附加 `disable_parallel_tool_use: true` 禁止并行调用 |

```python
# Anthropic: 强制调用指定工具
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=messages,
    tool_choice={"type": "tool", "name": "get_weather"}
)

# Anthropic: 禁止并行工具调用（但允许自动选择）
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=messages,
    tool_choice={"type": "auto", "disable_parallel_tool_use": True}
)

# Anthropic: 要求必须调用某个工具
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=messages,
    tool_choice="any"
)
```

### tool_choice 对比总结

| 功能 | OpenAI | Anthropic |
|------|--------|-----------|
| 自动选择 | `"auto"` | `"auto"` |
| 禁止工具 | `"none"` | 不传 `tools` 参数即可 |
| 强制调用某个工具 | `"required"` | `"any"` |
| 指定工具 | `{"type": "function", "function": {"name": "..."}}` | `{"type": "tool", "name": "..."}` |
| 禁止并行调用 | 不支持（需自行处理） | `{"type": "auto", "disable_parallel_tool_use": true}` |

---

## Agent 工具调用循环模式

Agent 的核心是一个持续运行的循环：**定义工具 -> 调用 LLM -> 检查工具调用 -> 执行工具 -> 回传结果 -> 继续循环**，直到模型给出最终文本回复。

以下是两家 SDK 的完整 Agent 循环实现对比。

### OpenAI Agent 循环（Chat Completions API）

```python
import json
from openai import OpenAI

client = OpenAI()

# ========== 1. 定义工具 ==========
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的当前天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_restaurant",
            "description": "搜索指定城市的餐厅",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"},
                    "cuisine": {"type": "string", "description": "菜系类型"}
                },
                "required": ["city"]
            }
        }
    }
]

# 工具执行函数
def get_weather(city: str) -> dict:
    """模拟天气查询"""
    weather_db = {"北京": {"temp": 25, "condition": "晴"}, "上海": {"temp": 28, "condition": "多云"}}
    return weather_db.get(city, {"temp": 20, "condition": "未知"})

def search_restaurant(city: str, cuisine: str = "") -> dict:
    """模拟餐厅搜索"""
    return {"city": city, "cuisine": cuisine or "不限", "results": ["餐厅A", "餐厅B"]}

tool_map = {"get_weather": get_weather, "search_restaurant": search_restaurant}

# ========== 2. Agent 循环 ==========
def run_agent(user_query: str, max_iterations: int = 5) -> str:
    """
    运行 OpenAI Agent 循环

    Args:
        user_query: 用户查询内容
        max_iterations: 最大循环次数，防止无限循环

    Returns:
        最终的文本回复
    """
    messages = [{"role": "user", "content": user_query}]

    for i in range(max_iterations):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools
        )

        assistant_message = response.choices[0].message
        messages.append(assistant_message)

        # 检查是否有工具调用
        if not assistant_message.tool_calls:
            # 没有工具调用，返回最终文本回复
            return assistant_message.content

        # 执行所有工具调用
        for tool_call in assistant_message.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)

            print(f"[迭代 {i+1}] 调用工具: {fn_name}({fn_args})")

            # 执行工具
            result = tool_map[fn_name](**fn_args)

            # 回传工具结果
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, ensure_ascii=False)
            })

    return "达到最大迭代次数，Agent 循环终止。"

# ========== 3. 运行 ==========
result = run_agent("北京今天天气怎么样？帮我推荐一家适合的好餐厅")
print(f"\n最终回复: {result}")
```

### Anthropic Agent 循环

```python
import json
import anthropic

client = anthropic.Anthropic()

# ========== 1. 定义工具 ==========
tools = [
    {
        "name": "get_weather",
        "description": "获取指定城市的当前天气信息",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "search_restaurant",
        "description": "搜索指定城市的餐厅",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称"},
                "cuisine": {"type": "string", "description": "菜系类型"}
            },
            "required": ["city"]
        }
    }
]

# 工具执行函数
def get_weather(city: str) -> dict:
    """模拟天气查询"""
    weather_db = {"北京": {"temp": 25, "condition": "晴"}, "上海": {"temp": 28, "condition": "多云"}}
    return weather_db.get(city, {"temp": 20, "condition": "未知"})

def search_restaurant(city: str, cuisine: str = "") -> dict:
    """模拟餐厅搜索"""
    return {"city": city, "cuisine": cuisine or "不限", "results": ["餐厅A", "餐厅B"]}

tool_map = {"get_weather": get_weather, "search_restaurant": search_restaurant}

# ========== 2. Agent 循环 ==========
def run_agent(user_query: str, max_iterations: int = 5) -> str:
    """
    运行 Anthropic Agent 循环

    Args:
        user_query: 用户查询内容
        max_iterations: 最大循环次数，防止无限循环

    Returns:
        最终的文本回复
    """
    messages = [{"role": "user", "content": user_query}]

    for i in range(max_iterations):
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        # 检查是否有工具调用
        has_tool_use = any(block.type == "tool_use" for block in response.content)

        if not has_tool_use:
            # 没有工具调用，提取并返回最终文本回复
            text_blocks = [block.text for block in response.content if block.type == "text"]
            return "\n".join(text_blocks)

        # 将 assistant 的响应（包含 tool_use 块）添加到消息历史
        messages.append({"role": "assistant", "content": response.content})

        # 构建工具结果
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                fn_name = block.name
                fn_args = block.input  # 直接是 dict

                print(f"[迭代 {i+1}] 调用工具: {fn_name}({fn_args})")

                # 执行工具
                result = tool_map[fn_name](**fn_args)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result, ensure_ascii=False)
                })

        # 将工具结果作为 user 消息回传
        messages.append({"role": "user", "content": tool_results})

    return "达到最大迭代次数，Agent 循环终止。"

# ========== 3. 运行 ==========
result = run_agent("北京今天天气怎么样？帮我推荐一家适合的好餐厅")
print(f"\n最终回复: {result}")
```

### Agent 循环差异要点

| 环节 | OpenAI | Anthropic |
|------|--------|-----------|
| **消息历史构建** | `messages` 列表，每条消息独立 | `messages` 列表，assistant 消息的 `content` 是 block 列表 |
| **检测工具调用** | `message.tool_calls` 是否存在 | `content` 中是否有 `type=="tool_use"` 的 block |
| **获取参数** | `json.loads(tool_call.function.arguments)` | `block.input`（已是 dict） |
| **回传结果** | 独立的 `role="tool"` 消息 | `role="user"` 消息中嵌入 `type="tool_result"` 的 block 列表 |
| **终止条件** | `message.tool_calls` 为空 | `content` 中无 `tool_use` block |
| **提取最终文本** | `message.content` | 遍历 `content`，提取 `type=="text"` 的 block |

---

## 要点总结

1. **定义格式不同**：OpenAI 使用 `parameters`，Anthropic 使用 `input_schema`；OpenAI Chat Completions 多一层 `function` 嵌套，Anthropic 和 OpenAI Responses API 都是扁平结构。

2. **结果回传方式不同**：OpenAI 使用独立的 `role="tool"` 消息；Anthropic 在 `role="user"` 消息中嵌入 `type="tool_result"` 内容块。

3. **参数解析方式不同**：OpenAI 返回的是 JSON 字符串，需要 `json.loads()` 解析；Anthropic 直接返回 dict 对象。

4. **ID 关联字段名不同**：OpenAI 用 `tool_call_id`（Chat Completions）或 `call_id`（Responses API）；Anthropic 用 `tool_use_id`。

5. **并行工具调用**：两家都支持，但 Anthropic 可以通过 `disable_parallel_tool_use` 显式禁止并行调用，OpenAI 需要开发者自行处理。

6. **tool_choice 差异**：功能相似但命名不同——OpenAI 的 `required` 对应 Anthropic 的 `any`；OpenAI 的 `none` 在 Anthropic 中通过不传 `tools` 参数实现。

7. **Agent 循环模式**：核心逻辑一致（循环检测 -> 执行 -> 回传），但消息构建方式不同。在构建跨平台 Agent 框架时，需要做一层适配来统一这些差异。
