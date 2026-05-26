
# -*- coding: utf-8 -*-
"""
Day07 Code 01：最简 LangGraph
"""

print("=" * 60)
print("Day07 - 最简 LangGraph")
print("=" * 60)

# 1. 模拟 LangGraph 核心概念
print("\nLangGraph 四大核心概念:")
print("  1. State: Agent 的记忆（对话历史、中间结果）")
print("  2. Node: 执行单元（纯函数优先）")
print("  3. Edge: 连接节点（条件边很强大）")
print("  4. Graph: 完整流程（State + Nodes + Edges）")

# 2. 模拟 State
print("\n" + "=" * 60)
print("State 示例:")
print("=" * 60)
state = {
    "messages": [
        {"type": "human", "content": "你好"},
        {"type": "ai", "content": "你好！有什么可以帮你？"}
    ],
    "step": 1,
    "is_done": False
}
print(f"State: {state}")

# 3. 模拟 Node
print("\n" + "=" * 60)
print("Node 示例（纯函数）:")
print("=" * 60)
def agent_node(state):
    messages = state["messages"]
    last_user_msg = [m for m in messages if m["type"] == "human"][-1]
    response = f"收到！你说：{last_user_msg['content']}"
    return {
        "messages": messages + [{"type": "ai", "content": response}],
        "step": state["step"] + 1
    }
new_state = agent_node(state)
print(f"Node 执行后 Step: {new_state['step']}")
print(f"最新消息: {new_state['messages'][-1]}")

print("\n" + "=" * 60)
print("LangChain vs LangGraph:")
print("=" * 60)
print("""
LangChain: Chain（链式调用）→ 简单线性流程
LangGraph: Graph（图/状态机）→ 复杂 Agent（循环、分支、显式状态）
""")
