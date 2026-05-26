
# Day08 示例 1：LangGraph 图编译
from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):
    input: str
    output: str
    steps: list[str]

def node1(state: State) -&gt; State:
    state["steps"].append("node1")
    state["output"] = "第一步完成"
    return state

def node2(state: State) -&gt; State:
    state["steps"].append("node2")
    state["output"] = "第二步完成"
    return state

# 构建图
graph = StateGraph(State)
graph.add_node("node1", node1)
graph.add_node("node2", node2)
graph.set_entry_point("node1")
graph.add_edge("node1", "node2")
graph.add_edge("node2", END)

# 编译
app = graph.compile()

# 执行
result = app.invoke({"input": "test", "steps": [], "output": ""})
print(result)
