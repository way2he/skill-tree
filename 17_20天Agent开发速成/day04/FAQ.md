---
name: Day04 FAQ 常见疑问深度解答
description: Day04 Function Calling + 多工具 Agent 7 个高频疑问深度回答
type: faq
tags: ["FAQ", "Function Calling", "Agent"]
created_at: 2026-05-22
updated_at: 2026-05-22
---

# 🤔 Day04 FAQ：Function Calling 深度疑问

---

## Q1：Function Calling 和 Structured Output（JSON Mode）有什么区别？

**短答**：Function Calling 是"模型决定调用哪个工具+生成参数"，Structured Output 是"模型按 schema 输出最终响应"，目的完全不同。

**详答**：

| 维度 | Function Calling | Structured Output |
|------|------------------|-------------------|
| 输出位置 | `tool_calls[].arguments` | `message.content` |
| 触发方式 | 模型自主决定调用 | 强制按 schema 输出 |
| 典型场景 | 调外部 API、查数据库 | 提取实体、分类标签、表单填写 |
| 后续动作 | 需本地执行后回灌 | 直接拿到结果用 |
| 多选支持 | 一次可返回多个 tool_call | 单一 JSON 结果 |

**实战建议**：
- 提取邮件中的姓名/电话/金额 → 用 Structured Output（`response_format={"type":"json_schema",...}`）
- 让模型查天气、发邮件 → 用 Function Calling
- 两者可以混用：FC 拿到外部数据，最终用 Structured Output 格式化输出给前端

---

## Q2：parallel_tool_calls 真的能加速吗？什么时候关闭它？

**短答**：能！但有 3 种场景必须关：依赖关系、幂等性差、调试期。

**详答**：

OpenAI 默认开启 parallel tool calls，模型可一次返回多个工具调用，你可以**并发执行**：

```python
import asyncio
async def run_parallel(tool_calls):
    tasks = [execute_async(tc) for tc in tool_calls]
    return await asyncio.gather(*tasks)
```

**性能收益**：3 个工具串行 1.5s × 3 = 4.5s，并行 1.5s，**节省 67% 时间**。

**3 种该关掉的场景**：

1. **工具间有依赖**：B 需要 A 的输出 → 必须串行
   ```python
   # 比如：先查用户ID，再用 ID 查订单
   client.chat.completions.create(parallel_tool_calls=False, ...)
   ```

2. **工具非幂等且涉及写操作**：并发可能导致冲突
   - 比如：同时调两次"创建订单"可能写两条相同记录

3. **调试阶段**：并行调用日志混乱，难以追踪
   - 上线前先关掉，调好再打开

---

## Q3：tool_choice 的 4 种取值分别什么时候用？

**短答**：`"auto"`（默认）、`"required"`（必调）、`"none"`（禁用）、指定工具名（强制调）。

**详答**：

| 取值 | 含义 | 典型场景 |
|------|------|---------|
| `"auto"` | 模型自主决定调不调、调哪个 | 99% 场景的默认选择 |
| `"required"` | 必须调用某个工具（不能直接回答） | 强制 Agent 走工具路径，避免乱编 |
| `"none"` | 禁用所有工具，纯文本回答 | 收尾轮次、纯总结场景 |
| `{type:"function",function:{name:"x"}}` | 强制调用指定工具 | 单步任务、调试某个工具 |

**实战技巧**：

1. **第一轮 `auto`，最后一轮 `none`**：避免模型在收尾时还在调工具
2. **强制 `required` 防止幻觉直接编答案**：比如"必须调天气工具不能瞎说天气"
3. **指定工具用于 A/B 测试**：测试单个工具的稳定性

---

## Q4：模型把字符串参数填成 JSON 字符串、把数字填成字符串怎么办？

**短答**：用 Pydantic 做参数校验 + 自动类型转换，错了就把校验错误回灌让模型自纠正。

**详答**：

**常见错填**：
- 数字字段填成字符串：`{"age": "25"}` 而不是 `{"age": 25}`
- 数组字段填成 JSON 字符串：`{"tags": "[\"a\",\"b\"]"}` 而不是 `{"tags": ["a","b"]}`
- 布尔值填成字符串：`{"is_vip": "true"}` 而不是 `true`

**解决方案**：用 Pydantic 兜底

```python
from pydantic import BaseModel, ValidationError, field_validator
import json

class WeatherArgs(BaseModel):
    city: str
    days: int = 1

    @field_validator("days", mode="before")
    @classmethod
    def coerce_int(cls, v):
        if isinstance(v, str):
            return int(v)  # 自动把 "3" 转成 3
        return v

def safe_call(args_json: str):
    try:
        args = WeatherArgs.model_validate_json(args_json)
        return get_weather(**args.model_dump())
    except ValidationError as e:
        return f"ERROR: 参数校验失败 {e.errors()}, 请检查后重试"
```

**进阶**：把 Pydantic schema 自动转成 OpenAI tools schema，避免手写两份：
```python
tools = [{"type": "function", "function": {
    "name": "get_weather",
    "parameters": WeatherArgs.model_json_schema()
}}]
```

---


## Q5：流式 Function Calling 怎么处理？arguments 是一段段拼出来的怎么解析？

**短答**：流式 tool_calls 是 delta 增量推送，要按 index 累积每个工具调用的 arguments 字符串，全部接收完再 json.loads。

**详答**：

OpenAI 流式协议下，每个 chunk 长这样：
`python
{
    "choices": [{
        "delta": {
            "tool_calls": [{
                "index": 0,                              # 第几个工具调用
                "id": "call_abc" 或 None,
                "function": {
                    "name": "get_weather" 或 None,
                    "arguments": "{\"city\":"            # 增量片段！
                }
            }]
        }
    }]
}
`

**累积代码**：

`python
def stream_with_tools(messages, tools):
    response = client.chat.completions.create(
        model="gpt-5.4", messages=messages, tools=tools, stream=True
    )
    tool_calls = {}  # {index: {id, name, arguments_str}}
    for chunk in response:
        delta = chunk.choices[0].delta
        if not delta.tool_calls:
            continue
        for tc_delta in delta.tool_calls:
            idx = tc_delta.index
            if idx not in tool_calls:
                tool_calls[idx] = {"id": "", "name": "", "args": ""}
            if tc_delta.id:
                tool_calls[idx]["id"] = tc_delta.id
            if tc_delta.function.name:
                tool_calls[idx]["name"] = tc_delta.function.name
            if tc_delta.function.arguments:
                tool_calls[idx]["args"] += tc_delta.function.arguments
    # 全部接收完后解析
    return [{
        "id": tc["id"], "name": tc["name"],
        "args": json.loads(tc["args"])
    } for tc in tool_calls.values()]
`

**常见踩坑**：
1. 不能边接收边解析 JSON（半截 JSON 报错）
2. 必须按 index 区分多个并行调用
3. id/name 可能在第 1 个 chunk 给，arguments 在后续 chunks 拼接

---

## Q6：怎么调试 Function Calling 链路？哪些信息必须打日志？

**短答**：完整记录 5 类信息：tool_calls 决策、参数值、执行耗时、错误堆栈、最终响应。

**详答**：

**5 类必打日志**：

1. **每轮模型的决策**
   `python
   logger.info({
       "iter": iteration,
       "model_decision": [tc.function.name for tc in msg.tool_calls],
       "raw_args": [tc.function.arguments for tc in msg.tool_calls]
   })
   `

2. **每个工具的执行情况**
   `python
   start = time.time()
   try:
       result = execute(tc)
       logger.info({"tool": tc.function.name, "args": args, "duration_ms": (time.time()-start)*1000, "success": True})
   except Exception as e:
       logger.error({"tool": tc.function.name, "args": args, "error": str(e), "traceback": traceback.format_exc()})
   `

3. **token 消耗**
   `python
   logger.info({"prompt_tokens": resp.usage.prompt_tokens, "completion_tokens": resp.usage.completion_tokens})
   `

4. **死循环检测命中**
   `python
   if key in seen:
       logger.warning({"event": "duplicate_call", "tool": tc.function.name, "args_hash": hash(args)})
   `

5. **最终响应 + 总耗时**

**进阶工具**：
- **LangSmith / LangFuse**：可视化整个 Agent 调用链路
- **OpenTelemetry**：标准化分布式追踪
- **自建**：把每次对话存成 trace.json，关键 case 可回放

---

## Q7：Function Calling 适合做"长流程任务"吗？比如自动写一个完整项目代码？

**短答**：不直接适合。FC 是单轮工具调用，长流程要靠 **Agent 框架（LangGraph / AutoGen）做状态管理 + Plan-Execute-Reflect 模式**。

**详答**：

**FC 单轮的局限**：
- 单次对话最多 5-10 个 tool_calls，复杂任务远不够
- 没有持久化状态，每次都从头思考
- 没有"反思修正"机制，错了就错了

**长流程的标准范式（Plan-Execute-Reflect）**：

`
1. Plan：模型先生成 N 步骤计划（不调工具，只规划）
2. Execute：逐步执行每个步骤（每步可能含多个 FC）
3. Reflect：每步执行后让模型检查结果，决定下一步
4. Loop：直到任务完成或触发上限
`

**典型框架**：
- **LangGraph**：基于状态机的 Agent，每个节点可调 FC，节点间用 condition edge 流转
- **AutoGen**：多 Agent 协作，PlannerAgent + CoderAgent + ReviewerAgent 配合
- **OpenAI Swarm**：轻量级多 Agent 框架
- **Claude Code**：Anthropic 官方实现的长流程编码 Agent

**实战经验**：
1. **任务拆解颗粒度**：单步 5-10 分钟可完成，超过就再拆
2. **持久化状态**：用 Redis/SQLite 存中间结果，便于断点续传
3. **人工 checkpoint**：关键节点（如要花钱、改数据库）必须人工确认
4. **预算控制**：单任务设 token / 时间 / 调用次数上限

**这部分是 Day05 ~ Day10 的重点内容**，FC 只是底层积木，Agent 框架才是组装方案。

---

## 📚 延伸阅读

- [README.md](README.md) 第 15:00-16:00 节：OpenAI vs Anthropic 协议对比
- [Function_Calling底层原理与协议.md](Function_Calling底层原理与协议.md)：深度协议解析
- OpenAI Cookbook - Function Calling: <https://cookbook.openai.com/examples/function_calling_with_an_openapi_spec>
- Anthropic Tool Use Best Practices: <https://docs.anthropic.com/en/docs/build-with-claude/tool-use>

---

**🧠 记住：FAQ 不是边角料，往往是面试官最爱深挖的地方。能讲清楚这 7 个问题，意味着你真的吃透了 Function Calling。**