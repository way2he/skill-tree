
---
name: LangGraph核心概念
description: LangGraph核心概念详解：State、Node、Edge、Graph
type: learning-material
tags: ["LangGraph", "Agent", "State", "Node", "Edge"]
summary: LangGraph核心概念详解，包含State、Node、Edge、Graph
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# LangGraph 核心概念详解 🚀

&gt; 📖 **本讲学习目标**：理解 LangGraph 的核心概念，能从零搭一个带条件跳转的 Graph  
&gt; ⏰ **预计学习时间**：3 小时

---

## LangChain vs LangGraph

| 维度 | LangChain | LangGraph |
|------|-----------|-----------|
| **范式** | Chain（链式调用） | Graph（图，状态机） |
| **循环** | 困难，容易无限循环 | 原生支持，可控 |
| **状态** | 隐式，容易混乱 | 显式，State 管理 |
| **分支** | 复杂 | 原生支持条件跳转 |
| **可观测性** | 一般 | 好，每个节点状态都看得到 |
| **适用** | 简单线性流程 | 复杂 Agent 流程 |

---

## LangGraph 核心概念

### 1. State（状态）⭐⭐⭐⭐⭐

**什么是 State？**
Agent 的"记忆"，保存所有信息。

**State 里存什么？**
- 对话历史（messages）
- 中间结果（retrieved_docs、tool_results）
- 任务状态（step、is_done）

**State 设计最佳实践**
1. ✅ TypedDict/Pydantic 定义类型
2. ✅ 字段名清晰
3. ✅ 不要存太多冗余字段

**示例**
```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "add"]
    step: int
    is_done: bool
```

---

### 2. Node（节点）⭐⭐⭐⭐⭐

**什么是 Node？**
执行单元，输入 State，输出更新后的 State。

**两种 Node**
| 类型 | 说明 | 优点 |
|------|------|------|
| **纯函数 Node** | 无副作用，只根据输入计算 | 好测试、可复现、推荐 |
| **带副作用 Node** | 调用外部 API、读写数据库 | 功能强，谨慎用 |

**Node 示例**
```python
def my_node(state: AgentState) -&gt; AgentState:
    """纯函数 Node：输入 State，输出更新后的 State"""
    messages = state["messages"]
    new_message = AIMessage(content="你好！")
    return {
        "messages": messages + [new_message],
        "step": state["step"] + 1
    }
```

---

### 3. Edge（边）⭐⭐⭐⭐⭐

**什么是 Edge？**
连接节点的边，定义流程。

**两种 Edge**
| 类型 | 说明 |
|------|------|
| **普通 Edge** | 无条件从 A → B |
| **条件 Edge** | 根据条件决定下一步走哪个分支 |

**条件 Edge 示例**
```python
def should_continue(state: AgentState) -&gt; Literal["tool", "end"]:
    """条件边：决定下一步调用工具还是结束"""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool"
    return "end"
```

---

### 4. Graph（图）⭐⭐⭐⭐⭐

**什么是 Graph？**
完整的 Agent 流程：State + Nodes + Edges。

**Graph 构建步骤**
```python
from langgraph.graph import StateGraph

# Step 1：定义 State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "add"]

# Step 2：创建 Graph
graph = StateGraph(AgentState)

# Step 3：添加 Nodes
graph.add_node("agent", agent_node)
graph.add_node("tool", tool_node)

# Step 4：添加 Edges
graph.set_entry_point("agent")
graph.add_conditional_edges(
    "agent",
    should_continue,
    {"tool": "tool", "end": END}
)
graph.add_edge("tool", "agent")

# Step 5：编译 Graph
app = graph.compile()
```

---

## 完整的 LangGraph 示例

```python
# -*- coding: utf-8 -*-
"""
LangGraph 最简示例
"""

from typing import TypedDict, Annotated, Sequence, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

# 1. 定义 State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "add"]
    step: int

# 2. 定义 Node
def agent_node(state: AgentState) -&gt; AgentState:
    """Agent 节点"""
    messages = state["messages"]
    last_user_msg = [m for m in messages if m.type == "human"][-1]
    response = f"收到！你说：{last_user_msg.content}"
    return {
        "messages": [AIMessage(content=response)],
        "step": state["step"] + 1
    }

# 3. 构建 Graph
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.add_edge("agent", END)  # agent 执行完直接结束
app = graph.compile()

# 4. 运行
initial_state = {
    "messages": [HumanMessage(content="你好")],
    "step": 0
}
result = app.invoke(initial_state)
print("结果:")
for m in result["messages"]:
    print(f"{m.type}: {m.content}")
print(f"步数: {result['step']}")
```

---

## 本讲小结 ✅

### LangGraph 四大核心概念
1. **State**：Agent 的记忆
2. **Node**：执行单元（纯函数优先）
3. **Edge**：连接节点（条件边很强大）
4. **Graph**：完整流程（State + Nodes + Edges）

### 下讲预告
ML 基础：梯度下降 + 反向传播 + 激活函数
